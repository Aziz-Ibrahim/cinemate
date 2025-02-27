from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from django.shortcuts import render
from django.conf import settings


@login_required
def movie_list(request):
    return render(request, "movies/movie_list.html")


def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def movie_list(request):
    movies = get_popular_movies()
    return render(request, "movies/movie_list.html", {"movies": movies})
