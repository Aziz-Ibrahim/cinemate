import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from .forms import RegisterForm
from .models import FavoriteMovie, Profile




# Home view.
def home(request):
    return render(request, "users/home.html")



# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)  # Configure logging
logger = logging.getLogger(__name__)  # Get logger for this module


#Registeration view
class RegisterView(CreateView):
    """
    Handles user registration using Django's built-in CreateView.
    Automatically creates a user profile and logs in the user after registration.
    """
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        logger.debug("✅ DEBUG: Form is valid, creating user...")

        user = form.save()
        logger.debug(f"✅ DEBUG: User {user.username} created successfully!")

        # ✅ Ensure country is stored in Profile
        country = form.cleaned_data.get("country")
        profile, created = Profile.objects.get_or_create(user=user)
        profile.country = country  # ✅ Explicitly set country
        profile.save()  # ✅ Save profile with country

        logger.debug(f"✅ DEBUG: Profile saved with country: {profile.country}")

        login(self.request, user)
        messages.success(self.request, "Registration successful! Please log in.")

        return redirect(self.success_url)


    def form_invalid(self, form):
        logger.error("❌ DEBUG: Register form is invalid!")
        logger.error(f"Form Errors: {form.errors}")  # Log errors in the terminal
        
        messages.error(self.request, "There were errors in your form. Please check below.")
        return render(self.request, self.template_name, {"form": form})

#log in view

class CustomLoginForm(forms.Form):
    identifier = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username or email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password-field", "placeholder": "Enter password"})
    )

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = None  # Disable default form

    def post(self, request, *args, **kwargs):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            # Check if identifier is email or username
            user = None
            if User.objects.filter(email=identifier).exists():
                user = User.objects.get(email=identifier)
            elif User.objects.filter(username=identifier).exists():
                user = User.objects.get(username=identifier)

            # Authenticate user
            if user and authenticate(request, username=user.username, password=password):
                login(request, user)
                return redirect("profile")

        return render(request, self.template_name, {"form": form, "error": "Invalid username/email or password."})



def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        if not request.user.is_authenticated:
            return redirect("login")  # Redirect guests trying to access /profile/
        profile_user = request.user  # Show logged-in user's profile

    favorite_movies = FavoriteMovie.objects.filter(user=profile_user)
    return render(request, "users/profile.html", {
        "profile_user": profile_user,
        "favorite_movies": favorite_movies,
    })

@login_required
def add_favorite_movie(request, movie_id):
    """Add a movie to the user's favorites."""
    if request.method == "POST":
        FavoriteMovie.objects.get_or_create(user=request.user, movie_id=movie_id)
    return redirect('profile')

@login_required
def remove_favorite_movie(request, movie_id):
    """Remove a movie from the user's favorites."""
    if request.method == "POST":
        favorite_movie = get_object_or_404(FavoriteMovie, user=request.user, movie_id=movie_id)
        favorite_movie.delete()
    return redirect('profile')


@login_required
def change_password(request):
    """Allows the user to change their password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in
            messages.success(request, "✅ Your password has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "❌ Error updating password. Please check the form.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})
