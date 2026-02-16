import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from itertools import zip_longest

from .models import LearningModule, SubModule, BASIC_MODULES_NAME
from ProgressTracker.models import ModuleProgress, ProgressTracker
from UserManagement.models import Student

logger = logging.getLogger(__name__)


def _get_student_or_redirect(request):
    """Return (Student, ProgressTracker) for the logged-in user.

    Returns ``None`` if the user is not a student so callers can
    redirect gracefully instead of crashing with a 500.
    """
    try:
        student = request.user.student
    except ObjectDoesNotExist:
        return None
    tracker, _ = ProgressTracker.objects.get_or_create(student=student)
    return student, tracker


@login_required(login_url='/login/')
def lecture_view(request, submodule_id):
    """
    Display a single submodule (lesson) and optionally mark another as complete.

    Raises clear 404 errors instead of the generic Django messages so tests
    and users get more helpful feedback.
    """
    try:
        submodule = SubModule.objects.get(pk=submodule_id)
    except SubModule.DoesNotExist:
        raise Http404("Submodule not found")

    module = submodule.parent_module

    # Mark current submodule complete (if requested via query param)
    complete_submodule_id = request.GET.get('complete_current')
    if complete_submodule_id:
        try:
            completed_sub = SubModule.objects.get(pk=complete_submodule_id)
        except SubModule.DoesNotExist:
            raise Http404("Completed submodule not found")

        result = _get_student_or_redirect(request)
        if result is None:
            return redirect('home')
        _student, tracker = result

        module_progress, _created = ModuleProgress.objects.get_or_create(
            progress_tracker=tracker,
            module=completed_sub.parent_module,
        )
        module_progress.add_completed_submodule(completed_sub)

        if not completed_sub.next_submodule:
            return redirect('module_handler')

    return render(request, 'Submodules.html', {
        'submodule': submodule,
        'module': module,
    })


@login_required(login_url='/login/')
def basic_module_menu_view(request):
    result = _get_student_or_redirect(request)
    if result is None:
        return redirect('home')
    _student, tracker = result

    basic_module = get_object_or_404(
        LearningModule,
        name=BASIC_MODULES_NAME,
    )

    module_progress, _created = ModuleProgress.objects.get_or_create(
        progress_tracker=tracker,
        module=basic_module,
    )
    return render(request, 'BasicModulesPage.html', {
        'module_progress': module_progress,
    })


@login_required(login_url='/login/')
def concept_module_menu_view(request):
    result = _get_student_or_redirect(request)
    if result is None:
        return redirect('home')
    _student, tracker = result

    all_modules = LearningModule.objects.all()
    user_module_progresses = tracker.module_progress.all()

    module_progresses_with_dummies = []
    module_count = 0
    finished_count = 0

    for module in all_modules:
        if module.name == BASIC_MODULES_NAME:
            continue
        module_count += 1

        user_progress = user_module_progresses.filter(module=module).first()
        if user_progress:
            module_progresses_with_dummies.append(user_progress)
            if user_progress.is_completed():
                finished_count += 1
        else:
            module_progresses_with_dummies.append(
                ModuleProgress(module=module, progress=0)
            )

    grouped_module_progresses = list(
        zip_longest(*[iter(module_progresses_with_dummies)] * 3)
    )
    return render(request, 'ConceptModulesPage.html', {
        'grouped_module_progresses': grouped_module_progresses,
        'module_count': module_count,
        'finished_count': finished_count,
    })


@login_required(login_url='/login/')
def concept_module_view(request, module_id):
    module = get_object_or_404(LearningModule, id=module_id)
    if module.name == BASIC_MODULES_NAME:
        return redirect('learning_modules')

    result = _get_student_or_redirect(request)
    if result is None:
        return redirect('home')
    _student, tracker = result

    module_progress, _created = ModuleProgress.objects.get_or_create(
        progress_tracker=tracker, module=module,
    )
    return render(request, 'ConceptModule.html', {
        'module': module,
        'module_progress': module_progress,
        'sub_modules': module.ordered_submodules(),
    })


@login_required(login_url='/login/')
def module_handler(request):
    result = _get_student_or_redirect(request)
    if result is None:
        return redirect('home')
    _student, tracker = result

    basic_module = LearningModule.objects.filter(name=BASIC_MODULES_NAME).first()
    if not basic_module:
        return redirect('concept_modules')

    module_progress, _created = ModuleProgress.objects.get_or_create(
        progress_tracker=tracker,
        module=basic_module,
    )

    if module_progress.is_completed():
        return redirect('concept_modules')
    return redirect('learning_modules')
