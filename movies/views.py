from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def movie_list(request):
    return render(request, "movies/movie_list.html")
