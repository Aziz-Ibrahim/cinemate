import requests
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from users.models import FavoriteMovie
from reviews.models import Review
from reviews.forms import ReviewForm

def get_movie_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    return response.json().get("genres", [])

@login_required
def movie_list(request):
    sort_by = request.GET.get("sort_by", "popularity.desc")
    genre_id = request.GET.get("genre", "")
    page = int(request.GET.get("page", 1))

    movies, total_pages = get_all_movies(sort_by, genre_id, page)
    
    genres = get_movie_genres()

    return render(request, "movies/movie_list.html", {
        "movies": movies,
        "sort_by": sort_by,
        "genres": genres,
        "selected_genre": int(genre_id) if genre_id else "",
    })



def get_all_movies(sort_by="popularity.desc", genre_id="", page=1):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "sort_by": sort_by,
        "page": page,
    }
    if genre_id:
        params["with_genres"] = genre_id

    response = requests.get(url, params=params)
    data = response.json()
    return data.get("results", []), data.get("total_pages", 1)


def search_movies(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "query": query,
        "page": 1
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "append_to_response": "credits,watch/providers,similar,videos,reviews"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {}

def movie_detail(request, movie_id):
    """Fetch movie details, user reviews, and display movie info."""
    movie = get_movie_details(movie_id)  # Fetch movie details via API
    reviews = Review.objects.filter(movie_id=movie_id).order_by("-created_at")  # Get reviews
    review_form = ReviewForm()

    # Extract additional movie data
    watch_providers = movie.get("watch/providers", {}).get("results", {}).get("US", {})
    cast = movie.get("credits", {}).get("cast", [])[:10]

    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "reviews": reviews,
        "review_form": review_form,
        "watch_providers": watch_providers,
        "cast": cast,
    })

@login_required
def toggle_favorite(request):
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        try:
            movie_id = int(movie_id)  # Convert to int.
        except ValueError:
            print("Error: movie_id is not a valid integer.")
            return JsonResponse({"status": "error"}, status=400)

        title = request.POST.get("title")
        poster_path = request.POST.get("poster_path")
        release_date = request.POST.get("release_date")
        rating = request.POST.get("rating")

        print(f"Movie ID before save: {movie_id}")  # Debugging

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
