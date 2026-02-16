import logging
from itertools import zip_longest
from urllib.parse import quote

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import ModuleProgress, ProgressTracker
from LearningResource.models import LearningModule, BASIC_MODULES_NAME
from UserManagement.models import Parent, Student, Teacher

logger = logging.getLogger(__name__)


@login_required(login_url='/login/')
def download_report(request, student_id):
    """Generate a PDF progress report for a student."""
    student = get_object_or_404(Student, id=student_id)

    try:
        progress_tracker = ProgressTracker.objects.get(student=student)
    except ProgressTracker.DoesNotExist:
        progress_tracker = ProgressTracker.objects.create(student=student)

    modules_progress = progress_tracker.module_progress.all()

    response = HttpResponse(content_type='application/pdf')
    filename = f"progress_report_{student.full_name()}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    def estimate_module_space(module):
        return 85 + len(module.completed_submodules.all()) * 25

    def check_space(y_offset, space_required):
        if height - y_offset <= space_required:
            p.showPage()
            y_offset = 80
            p.setFont("Helvetica", 16)
        return y_offset

    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 80, f"Progress Report for {student.full_name()}")

    p.setFont("Helvetica", 16)
    p.drawString(
        100, height - 150,
        f"Overall Progress: {progress_tracker.overall_progress * 100:.2f}%",
    )

    y_offset = 190
    for module in modules_progress:
        space_required = estimate_module_space(module)
        y_offset = check_space(y_offset, space_required)
        y_offset = check_space(y_offset, 100)

        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, height - y_offset, f"Module: {module.module.name}")
        y_offset += 30

        p.setFont("Helvetica", 16)
        p.drawString(100, height - y_offset, f"Progress: {module.progress * 100:.2f}%")
        y_offset += 30

        p.drawString(100, height - y_offset, "Completed Submodules:")
        y_offset += 25

        for submodule in module.completed_submodules.all():
            p.setFont("Helvetica", 14)
            p.drawString(120, height - y_offset, f"\u2022 {submodule.name}")
            y_offset += 25

        y_offset += 15

    p.showPage()
    p.save()
    return response


@login_required(login_url='/login/')
def parent_concept_modules_view(request):
    """Progress overview for parents and teachers viewing their students."""
    user = request.user

    if hasattr(user, 'parent'):
        students = user.parent.get_children()
    elif hasattr(user, 'teacher'):
        students = user.teacher.get_students()
    else:
        # Students or users with no role — redirect to home
        return redirect('home')

    all_modules = LearningModule.objects.all()
    children_data = []

    for child in students:
        try:
            tracker = ProgressTracker.objects.get(student=child)
        except ProgressTracker.DoesNotExist:
            tracker = ProgressTracker.objects.create(student=child)

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

        children_data.append({
            'student': child,
            'grouped_module_progresses': list(
                zip_longest(*[iter(module_progresses_with_dummies)] * 3)
            ),
            'module_count': module_count,
            'finished_count': finished_count,
        })

    return render(request, 'parent_progress_tracker.html', {
        'children_data': children_data,
    })
