import logging
import os
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from .forms import RegisterForm, ContactForm
from .models import FavoriteMovie, Profile


# Home view.
def home(request):
    """Renders the home page."""
    return render(request, "users/home.html")


# Registration view
class RegisterView(CreateView):
    """
    Handles user registration using Django's built-in CreateView.
    Automatically creates a user profile and logs in the
    user after registration.
    """

    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """Saves the user and profile if the form is valid."""
        user = form.save()

        Profile.objects.get_or_create(user=user)

        login(self.request, user)
        messages.success(self.request, "Registration successful! Please login")

        return redirect(self.success_url)

    def form_invalid(self, form):
        """Renders the form with errors if it's invalid."""
        messages.error(
            self.request, "There were errors in your form. Please check below."
        )
        return render(self.request, self.template_name, {"form": form})


# Log in view
class CustomLoginForm(forms.Form):
    """Custom login form with username or email identifier."""

    identifier = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter username or email",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password-field",
                "placeholder": "Enter password",
            }
        ),
    )


class CustomLoginView(LoginView):
    """Custom login view to handle login with username or email."""

    template_name = "users/login.html"
    authentication_form = None  # Disable default form

    def post(self, request, *args, **kwargs):
        """Handles POST requests for login."""
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]

            # Check if identifier is email or username
            user = None
            if User.objects.filter(email=identifier).exists():
                user = User.objects.get(email=identifier)
            elif User.objects.filter(username=identifier).exists():
                user = User.objects.get(username=identifier)

            # Authenticate user
            if user and authenticate(
                request, username=user.username, password=password
            ):
                login(request, user)
                return redirect("profile")

        return render(
            request,
            self.template_name,
            {"form": form, "error": "Invalid username/email or password."},
        )


def profile_view(request, username=None):
    """Displays the user's profile and favorite movies."""
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        if not request.user.is_authenticated:
            # Redirect guests trying to access /profile/
            return redirect("login")
        profile_user = request.user  # Show logged-in user's profile

    favorite_movies = FavoriteMovie.objects.filter(user=profile_user)
    return render(
        request,
        "users/profile.html",
        {"profile_user": profile_user, "favorite_movies": favorite_movies},
    )


def fetch_movie_details(movie_id):
    """Fetch movie details from TMDB API."""
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}?"
        f"api_key={settings.TMDB_API_KEY}&language=en-US"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def add_favorite_movie(request, movie_id):
    """Add a movie to the user's favorites list."""
    if request.method == "POST":
        # Fetch movie details from TMDb API
        api_url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}?"
            f"api_key={settings.TMDB_API_KEY}"
        )
        response = requests.get(api_url)
        movie_data = response.json()

        # Save movie with full poster URL
        FavoriteMovie.objects.create(
            user=request.user,
            movie_id=movie_id,
            title=movie_data.get("title", "Unknown Movie"),
            poster_path=f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}"  # noqa: E501
            if movie_data.get("poster_path")
            else None,
            release_date=movie_data.get("release_date", ""),
            rating=movie_data.get("vote_average", None),
        )
        return redirect("profile")


def remove_favorite_movie(request, movie_id):
    """
    Handles the removal of a movie from a user's favorites.

    Args:
        request (HttpRequest): The incoming HTTP request
        (must be a POST request).
        movie_id (int):
        The ID of the movie to remove from the user's favorites.

    Returns:
        JsonResponse: A JSON response indicating success ("removed")
        or failure ("error").
    """
    print(f"Request received to remove movie {movie_id}")  # Debugging
    if request.method == "POST":
        favorite_movie = get_object_or_404(
            FavoriteMovie, user=request.user, movie_id=movie_id
        )
        favorite_movie.delete()
        return JsonResponse({"status": "removed"})

    return JsonResponse({"status": "error"}, status=400)


@login_required
def change_password(request):
    """Allows the user to change their password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in
            messages.success(request, " password updated successfully.")
            return redirect("profile")
        else:
            messages.error
            (request, "Error updating password. Please check the form.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})


def contact_view(request):
    """
    Handles the contact form submission and sends an email to the site owner.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            subject = f"New Contact Message from {name}"
            full_message = f"From: {name} ({email})\n\n{message}"

            send_mail(
                subject,
                full_message,
                os.getenv("EMAIL_HOST_USER"),  # Your email
                [os.getenv("EMAIL_HOST_USER")],  # Receiver (yourself)
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent!")
            return redirect("contact")  # Redirect back to the form

    else:
        form = ContactForm()  # Empty form for GET request

    return render(request, "users/contact.html", {"form": form})
