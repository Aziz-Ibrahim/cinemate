from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm

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
    template_name = "users/login.html"
