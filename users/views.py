from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def home(request):
    return render(request, "users/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect("home")  # Redirect to homepage
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

