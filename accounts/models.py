from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model for the Event Management System.

    Currently uses Django's default fields (username, email, password, etc.)
    with no extensions. Using AbstractUser now so we can add fields later
    (e.g., bio, avatar, phone) without painful migration issues.

    Setup requirement:
        Add to config/settings.py BEFORE first migration:
        AUTH_USER_MODEL = 'accounts.User'
    """

    class Meta:
        db_table = "accounts_user"

    def __str__(self):
        return self.username
