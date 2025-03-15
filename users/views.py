import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import FavoriteMovie, Profile
from django.contrib import messages



# Create your views here.
def home(request):
    return render(request, "users/home.html")



# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)  # Configure logging
logger = logging.getLogger(__name__)  # Get logger for this module

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

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile")


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

def add_favorite_movie(request, movie_id):
    if request.method == "POST":
        FavoriteMovie.objects.create(user=request.user, movie_id=movie_id)
        return redirect('profile') 
    