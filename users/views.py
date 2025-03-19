import logging
from django.conf import settings
import requests
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

def fetch_movie_details(movie_id):
    """Fetch movie details from TMDB API"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def add_favorite_movie(request, movie_id):
    if request.method == "POST":
        # Fetch movie details from TMDb API
        api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}"
        response = requests.get(api_url)
        movie_data = response.json()

        # Save movie with full poster URL
        FavoriteMovie.objects.create(
            user=request.user,
            movie_id=movie_id,
            title=movie_data.get("title", "Unknown Movie"),
            poster_path=f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}" if movie_data.get("poster_path") else None,
            release_date=movie_data.get("release_date", ""),
            rating=movie_data.get("vote_average", None),
        )
        return redirect("profile")

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
