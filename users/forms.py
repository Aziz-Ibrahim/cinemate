from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class RegisterForm(UserCreationForm):
    """
    Custom user registration form that extends Django's built-in UserCreationForm.
    
    This form allows users to sign up with the following fields:
    - Username
    - Email
    - Password (password1 & password2)
    - First Name
    - Last Name
    - Country of Residence (using django-countries)

    All fields are styled with Bootstrap's "form-control" class for better UI consistency.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "country"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply Bootstrap styling to all fields.
        This ensures a consistent UI appearance without manually adding 
        classes to each field individually.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})  # Adds Bootstrap styling

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )