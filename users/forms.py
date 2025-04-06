from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class RegisterForm(UserCreationForm):
    """
    Custom user registration form that extends Django's built-in
    UserCreationForm.

    This form allows users to sign up with the following fields:
    - Username
    - Email
    - Password (password1 & password2)
    - First Name
    - Last Name
    - Country of Residence (using django-countries)

    All fields are styled with Bootstrap's "form-control" class for better UI
    consistency.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")


    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        ]
        widgets = {
            "username": forms.TextInput(),  
            "email": forms.EmailInput(), 
            "password1": forms.PasswordInput(),  
            "password2": forms.PasswordInput(),  
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply Bootstrap styling to all fields.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class LoginForm(forms.Form):  # No need to inherit from AuthenticationForm
    """Form for user login with username or email identifier."""

    identifier = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username or email"}  # noqa: E501
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )

    def clean(self):
        """Validates the user's credentials."""
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")

        # Validate user input (username or email)
        user = None
        if User.objects.filter(email=identifier).exists():
            user = User.objects.get(email=identifier)
        elif User.objects.filter(username=identifier).exists():
            user = User.objects.get(username=identifier)

        if user:
            authenticated_user = authenticate(
                username=user.username, password=password
            )
            if authenticated_user:
                return cleaned_data

        raise forms.ValidationError("Invalid username/email or password.")


class ContactForm(forms.Form):
    """Form for users to send contact messages."""

    name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        required=True
    )
