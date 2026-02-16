from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    """
    Handle user registration (REQ-1).

    GET:  Display empty registration form.
    POST: Validate form, create user, log them in, redirect to event list.

    Why log in immediately after registration?
    - Better UX: user doesn't have to log in twice
    - Django's login() sets the session cookie securely

    Why redirect to /events/?
    - LOGIN_REDIRECT_URL in settings already points there
    - Event list is effectively our "home page"
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("events:event_list")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
