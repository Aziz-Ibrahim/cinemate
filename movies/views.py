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

def movie_detail(request, movie_id):
    movie = get_object_or_404(FavoriteMovie, id=movie_id)  # Adjust the model if you're using a different one
    return render(request, "movies/movie_detail.html", {"movie": movie})