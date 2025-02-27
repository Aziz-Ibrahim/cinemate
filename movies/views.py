import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from users.models import FavoriteMovie

@login_required
def movie_list(request):
    movies = get_popular_movies()
    return render(request, "movies/movie_list.html", {"movies": movies})

def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    return response.json().get("results", [])


@login_required
def toggle_favorite(request):
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        title = request.POST.get("title")
        poster_path = request.POST.get("poster_path")
        release_date = request.POST.get("release_date")
        rating = request.POST.get("rating")

        favorite, created = FavoriteMovie.objects.get_or_create(
            user=request.user,
            movie_id=movie_id,
            defaults={
                "title": title,
                "poster_path": poster_path,
                "release_date": release_date,
                "rating": rating,
            },
        )

        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})

        return JsonResponse({"status": "added"})

    return JsonResponse({"status": "error"}, status=400)
