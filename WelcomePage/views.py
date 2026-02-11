from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import TicketForm


def home_view(request):
    """Landing page — shows WelcomePage for anonymous users,
    MenuPage (with feedback form) for authenticated users.
    """
    form = TicketForm()

    if not request.user.is_authenticated:
        return render(request, 'WelcomePage.html', {'form': form})

    # --- Handle feedback form submission for all users ---
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Associate with user if authenticated, otherwise leave null
            if request.user.is_authenticated:
                ticket.user = request.user
            ticket.save()
            return redirect('home')

    # Redirect users who haven't finished profile setup
    profile_completed = False
    if hasattr(request.user, 'student'):
        profile_completed = request.user.student.profile_completed
    elif hasattr(request.user, 'parent'):
        profile_completed = request.user.parent.profile_completed
    elif hasattr(request.user, 'teacher'):
        profile_completed = True  # teachers have no extra profile step

    if not request.user.is_staff and not profile_completed:
        return redirect('choose_user_type')

    return render(request, 'MenuPage.html', {'form': form})
