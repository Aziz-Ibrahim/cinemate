from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError




class RegisterForm(UserCreationForm):
    """
    Custom user registration form with email uniqueness validation.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Required."
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Required."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'last_name',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

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
