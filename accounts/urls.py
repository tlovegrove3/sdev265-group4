from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # Task 8 — REQ-1: Registration (custom view)
    path("register/", views.register, name="register"),
    # Task 9 — REQ-2: Login (Django built-in)
    # Uses LoginView which handles:
    #   - Session creation
    #   - CSRF protection
    #   - Redirect to LOGIN_REDIRECT_URL (/events/) on success
    #   - "next" parameter support (redirect back to where user came from)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    # Task 10 — REQ-3: Logout (Django built-in)
    # Uses LogoutView which handles:
    #   - Session destruction
    #   - Redirect to LOGOUT_REDIRECT_URL (/accounts/login/)
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
