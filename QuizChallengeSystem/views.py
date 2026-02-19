from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.utils import timezone

# import for run challenge code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from LearningResource.models import LearningModule, SubModule, BASIC_MODULES_NAME
from .models import Quiz, Question, UserAnswer, Choice, QuizResult, Challenge
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
from itertools import zip_longest

from UserManagement.models import Student
from CodeVenture.services.judge0_service import Judge0Service
from CodeVenture.services.rate_limiter import is_over_limit_for_request
from ProgressTracker.models import ProgressTracker, ModuleProgress


@login_required
def quiz_view(request, quiz_id):
    # View for taking a quiz and recording the results.
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if not hasattr(request.user, 'student'):
        return redirect('home')

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            total_questions = len(questions)
            score = 0
            quiz_result = QuizResult.objects.create(
                quiz=quiz,
                user=request.user.student,
                score=0,
                total_questions=total_questions,
            )

            for question in questions:
                selected_answer_id = form.cleaned_data.get(f"question_{question.id}")
                is_correct_answer = False
                selected_answer_text = ""

                try:
                    if selected_answer_id is not None:
                        choice_obj = Choice.objects.get(id=selected_answer_id)
                        selected_answer_text = choice_obj.text

                        correct_choice = question.choices.get(is_correct=True)
                        if correct_choice.id == choice_obj.id:
                            is_correct_answer = True
                            score += 1
                except Choice.DoesNotExist:
                    # If either the selected or correct choice is missing,
                    # treat the answer as incorrect but continue processing.
                    selected_answer_text = selected_answer_text or ""

                UserAnswer.objects.create(
                    quiz_result=quiz_result,
                    question=question,
                    selected_answer=selected_answer_text,
                    is_correct=is_correct_answer
                )

            quiz_result.score = score
            quiz_result.save()

            return redirect('quiz_result', result_id=quiz_result.id)

    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'quiz': quiz, 'form': form})


@login_required
def quiz_result_view(request, result_id):
    # View for displaying quiz results.



    quiz_result = get_object_or_404(QuizResult, id=result_id)

    user_answers = quiz_result.user_answers.all()

    total_questions = quiz_result.total_questions
    score = quiz_result.score

    results = []
    less_than_40 = 0
    between_40_and_80 = 0

    for answer in user_answers:
        choices = [
            {
                'text': f"{chr(65 + index)}) {choice.text}",
                'is_correct': choice.is_correct
            }
            for index, choice in enumerate(answer.question.choices.all())
        ]

        # Identify the selected answer's index and prefix it
        selected_answer_index = next(
            (index for index, choice in enumerate(answer.question.choices.all()) if
             choice.text == answer.selected_answer),
            None)
        selected_answer = f"{chr(65 + selected_answer_index)}) {answer.selected_answer}" if selected_answer_index is not None else answer.selected_answer

        results.append({
            'question': answer.question.text,
            'answer': selected_answer,
            'is_correct': answer.is_correct,
            'choices': choices
        })

    if score < (total_questions * 0.4):
        less_than_40 = (total_questions * 0.4)
    elif score < (total_questions * 0.8):
        between_40_and_80 = (total_questions * 0.8)

    context = {
        'score': score,
        'total_questions': total_questions,
        'results': results,
        'less_than_40': less_than_40,
        'between_40_and_80': between_40_and_80,
        'quiz': quiz_result.quiz
    }

    return render(request, 'quiz_result.html', context)


def modules_list_quiz(request):
    concept_modules = LearningModule.objects.exclude(name=BASIC_MODULES_NAME).all()

    grouped_module = list(zip_longest(*[iter(concept_modules)] * 3))

    context = {
        'grouped_module': grouped_module
    }

    return render(request, 'module_list_quiz.html', context)


def quiz_list(request, module_id):
    module = get_object_or_404(LearningModule, id=module_id)
    sub_modules = module.sub_modules.all()

    # If the user is a student, only show quizzes for submodules they've completed.
    # When none are completed yet, we still render the page with a clear message
    # explaining how to unlock quizzes.
    student = None
    module_progress = None
    next_submodule_to_complete = None
    quiz_sub_modules = []

    if hasattr(request.user, "student"):
        student = request.user.student
        tracker, _ = ProgressTracker.objects.get_or_create(student=student)
        module_progress, _ = ModuleProgress.objects.get_or_create(
            progress_tracker=tracker,
            module=module,
        )
        next_submodule_to_complete = module_progress.current_submodule()
        completed = set(module_progress.completed_submodules.all())
        quiz_sub_modules = [
            sm for sm in sub_modules
            if getattr(sm, "quiz", None) and sm in completed
        ]
    else:
        # Non-students (e.g. parent/teacher) can view quizzes list without gating.
        quiz_sub_modules = [
            sm for sm in sub_modules
            if getattr(sm, "quiz", None)
        ]

    context = {
        'module': module,
        'sub_modules': sub_modules,
        'quiz_sub_modules': quiz_sub_modules,
        'module_progress': module_progress,
        'next_submodule_to_complete': next_submodule_to_complete,
    }
    return render(request, 'quiz_list.html', context)


def quiz_summary_view(request, quiz_id):
    """
    View for displaying a summary of quiz attempts.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = None
    if hasattr(request.user, 'student'):
        student = request.user.student
    elif hasattr(request.user, 'parent'):
        student = request.user.parent.get_children().first()
    elif hasattr(request.user, 'teacher'):
        student = request.user.teacher.get_students().first()

    if student is None:
        return redirect('home')

    attempts = QuizResult.objects.filter(user=student, quiz=quiz)
    now = timezone.now()

    # Check if a new attempt is allowed:
    # 1. No previous attempts exist.
    # 2. Results are not yet available (deadline hasn't passed OR no deadline exists).
    # 3. User is a student.
    is_deadline_future = quiz.deadline is None or quiz.deadline > now

    if not attempts.exists() and is_deadline_future and hasattr(request.user, 'student'):
        # For the first attempt, go straight to the quiz-taking view.
        return redirect('quiz_view', quiz_id=quiz.id)

    module = quiz.sub_module.parent_module
    best_score = attempts.aggregate(Max('score'))['score__max']

    context = {
        'attempts': attempts,
        'quiz': quiz,
        'module': module,
        'best_score': best_score,
        'now': now
    }

    return render(request, 'quiz_summary.html', context)


def start_new_attempt(request, sub_module_id):
    sub_modules = get_object_or_404(SubModule, id=sub_module_id)
    quiz = get_object_or_404(Quiz, id=sub_module_id)

    context = {
        'sub_modules': sub_modules,
        'quiz': quiz
    }
    # Redirect the user to the quiz page to begin the new attempt
    return render(request, 'quiz.html', context)


def challenge_view(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    context = {"challenge": challenge}
    return render(request, 'challenge.html', context)


@csrf_exempt
def challenge_run_code(request):
    """
    Executes the user's code against a predefined challenge using the Judge0 Service.
    """
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST method is supported.'}, status=405)

    # Lightweight guardrail to avoid excessive Judge0 usage in demos.
    if is_over_limit_for_request(request, prefix="challenge_run", limit=3):
        return JsonResponse(
            {
                'error': 'Demo rate limit exceeded. '
                         'This endpoint only allows a few code runs per day.'
            },
            status=429,
        )

    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        code = body_data.get('code', '')
        challenge_id = body_data.get('challenge_id')

        if not challenge_id:
            return JsonResponse({'error': 'Challenge ID is required.'}, status=400)

        # Retrieve the challenge object
        challenge = get_object_or_404(Challenge, id=challenge_id)

        # Handle Standard Input (stdin)
        stdin = ""
        if challenge.std_in:
            try:
                stdin = challenge.std_in.encode().decode('unicode_escape')
            except Exception as e:
                print(f"Error decoding stdin for challenge {challenge.id}: {e}")
                stdin = challenge.std_in

        # Handle Expected Output
        expected_output = ""
        if challenge.expected_output:
            try:
                expected_output = challenge.expected_output.encode().decode('unicode_escape')
            except Exception as e:
                print(f"Error decoding expected_output for challenge {challenge.id}: {e}")
                expected_output = challenge.expected_output

        # Execute using Service
        service = Judge0Service()
        result_data = service.run_code(
            code,
            stdin=stdin,
            expected_output=expected_output
        )

        if 'error' in result_data and 'status_id' not in result_data:
            return JsonResponse(result_data, status=500)

        status_id = result_data.get('status_id')
        success = result_data.get('success', False)

        # Format response for frontend
        context = {
            'stdout': result_data.get('stdout', ''),
            'result': success,
            'expected_output': result_data.get('expected_output'),
            'status_id': status_id,
            'status_description': result_data.get('description', 'Unknown')
        }

        # Append error message if present (e.g. syntax error)
        if 'error_message' in result_data:
            context['stdout'] += f"\nError:\n{result_data['error_message']}"

        return JsonResponse(context)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body.'}, status=400)
    except Challenge.DoesNotExist:
        return JsonResponse({'error': 'Challenge not found.'}, status=404)
    except Exception as e:
        print(f"Internal Run Code Error: {e}")
        return JsonResponse({'error': f'An internal error occurred: {str(e)}'}, status=500)


def challenges_list_view(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenge_list.html', {'challenges': challenges})
