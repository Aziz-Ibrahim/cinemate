import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from users.models import FavoriteMovie
from django.db.models import Q
from django.http import JsonResponse

@login_required
def movie_list(request):
    sort_by = request.GET.get("sort_by", "popularity.desc")
    page = int(request.GET.get("page", 1))  # Get current page

    movies, total_pages = get_all_movies(sort_by, page)

    # If it's an AJAX request, return JSON instead of rendering a template
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'movies': movies, 'current_page': page, 'total_pages': total_pages})

    return render(request, "movies/movie_list.html", {"movies": movies, "sort_by": sort_by})

def get_all_movies(sort_by="popularity.desc", page=1):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "sort_by": sort_by,
        "page": page,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("results", []), data.get("total_pages", 1)  # Return movies & total pages





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
    api_key = settings.TMDB_API_KEY
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=videos,reviews,similar,watch/providers"
    country_code = "US"
    movie = get_movie_details(movie_id)

    response = requests.get(url)
    if response.status_code != 200:
        return render(request, "movies/movie_detail.html", {"error": "Movie not found"})

    # Extract watch providers safely
    watch_providers = movie.get("watch/providers", {}).get("results", {}).get(country_code, {})
    cast = movie.get("credits", {}).get("cast", [])[:10]

    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "watch_providers": watch_providers,  # Passing to template separately
        "cast": cast,
    })