from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to include an optional email field.

    Why UserCreationForm?
    - Handles password hashing (never store plaintext)
    - Validates password strength using AUTH_PASSWORD_VALIDATORS from settings
    - Confirms password match (password1 == password2)
    - Uses get_user_model() so it works with our custom AbstractUser

    Why not just a plain ModelForm?
    - We'd have to manually handle password hashing and validation
    - UserCreationForm already does this correctly and securely
    """

    class Meta:
        model = User
        fields = ("username", "email")
        # password1 and password2 are added automatically by UserCreationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email explicitly optional (it already is via AbstractUser,
        # but this makes the intent clear in the form)
        self.fields["email"].required = False
        self.fields["email"].help_text = "Optional. Used for account recovery."
