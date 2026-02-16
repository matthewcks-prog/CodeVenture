from django.shortcuts import render, redirect

from UserManagement.services import get_onboarding_redirect

from .forms import TicketForm


def home_view(request):
    """Landing page — shows WelcomePage for anonymous users,
    MenuPage (with feedback form) for authenticated users who have completed onboarding.
    """
    form = TicketForm()

    if not request.user.is_authenticated:
        return render(request, "WelcomePage.html", {"form": form})

    # Handle feedback form submission for authenticated users
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")

    # Single source of truth: UserManagement decides if user must complete onboarding
    redirect_target = get_onboarding_redirect(request.user)
    if redirect_target:
        return redirect(redirect_target)

    return render(request, "MenuPage.html", {"form": form})
