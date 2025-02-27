import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from users.models import FavoriteMovie
from django.db.models import Q

@login_required
def movie_list(request):
    sort_by = request.GET.get('sort_by', 'popularity')  # Get sorting parameter from request (default is 'popularity')
    search_query = request.GET.get('search', '')  # Get search query from request (default is empty)

    # Log the sort_by value to see if it's being passed correctly
    print(f"Sort By: {sort_by}")
    print(f"Search Query: {search_query}")
    print(f"GET Parameters: {request.GET}")

    if search_query:
        movies = search_movies(search_query)  # Get movies by search query
    else:
        movies = get_all_movies(sort_by)  # Get all movies sorted by the 'sort_by' parameter

    return render(request, "movies/movie_list.html", {
        "movies": movies,
        "sort_by": sort_by,
        "search_query": search_query
    })

def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def get_all_movies(sort_by=' '):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "sort_by": sort_by,  # Use the sort_by parameter here to dynamically change sorting
        "page": 1
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])


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