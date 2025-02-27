from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from .models import FavoriteMovie



# Create your views here.
def home(request):
    return render(request, "users/home.html")

class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")  # Redirect after successful registration

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user automatically
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile")


@login_required
def profile_view(request):
    favorite_movies = FavoriteMovie.objects.filter(user=request.user)
    return render(request, "users/profile.html", {"favorite_movies": favorite_movies})

def add_favorite_movie(request, movie_id):
    if request.method == "POST":
        FavoriteMovie.objects.create(user=request.user, movie_id=movie_id)
        return redirect('profile') 
    