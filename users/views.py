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
from .models import FavoriteMovie



# Create your views here.
def home(request):
    return render(request, "users/home.html")

class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")  # Redirect after successful registration

    def form_valid(self, form):
        user = form.save(commit=False)  # Don't save to DB yet
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.save()  # Now save the user with first & last name
        login(self.request, user)  # Log in the user automatically
        return super().form_valid(form)


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
    