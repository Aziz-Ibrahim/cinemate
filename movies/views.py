import requests
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from users.models import FavoriteMovie, Profile
from reviews.models import Review
from reviews.forms import ReviewForm

# Constants for TMDB API
TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def get_movie_genres():
    """Fetch the list of movie genres from TMDB API."""
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    return response.json().get("genres", [])


def trending_movies(request):
    """Fetches trending movies from TMDB and renders the trending page."""
    url = (
        f"https://api.themoviedb.org/3/trending/movie/week?"
        f"api_key={TMDB_API_KEY}"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return render(request, "movies/trending.html", {"movies": []})

    movies = response.json().get("results", [])

    return render(request, "movies/trending.html", {"movies": movies})


@login_required
def movie_list(request):
    """
    Fetch and display a list of movies.
    Supports search, sorting, genre filtering, and pagination.
    Includes favorite status for each movie.
    """
    search_query = request.GET.get("search", "").strip()
    sort_by = request.GET.get("sort_by", "popularity.desc")
    genre_id = request.GET.get("genre", "")
    page = int(request.GET.get("page", 1))

    # Fetch movies from TMDb API
    if search_query:
        movies = search_movies(search_query)
        total_pages = 1  # Search results usually return a single page
    else:
        movies, total_pages = get_all_movies(sort_by, genre_id, page)

    # Retrieve user's favorite movie IDs
    favorite_movie_ids = set(
        map(
            int,
            FavoriteMovie.objects.filter(user=request.user).values_list(
                "movie_id", flat=True
            ),
        )
    )

    # Annotate movies with favorite status
    for movie in movies:
        movie["is_favorite"] = movie["id"] in favorite_movie_ids

    # If it's an AJAX request, return JSON response
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"movies": movies, "total_pages": total_pages})

    genres = get_movie_genres()

    return render(
        request,
        "movies/movie_list.html",
        {
            "movies": movies,
            "sort_by": sort_by,
            "genres": genres,
            "selected_genre": int(genre_id) if genre_id else "",
            "search_query": search_query,
        },
    )


def get_all_movies(sort_by="popularity.desc", genre_id="", page=1):
    """Fetches a paginated list of movies from TMDB
    based on sorting and genre."""
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
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
    """Fetches a list of movies based on a search query from TMDB API."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "query": query,
        "page": 1,
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])


def get_movie_details(movie_id):
    """Fetch detailed information about a specific movie from TMDB API."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "append_to_response": "credits,watch/providers,videos,reviews,similar",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return None  # Return None if the movie is not found


@login_required
def movie_detail(request, movie_id):
    """
    Fetch movie details and determine if the movie is in the user's favorites.
    Includes images, reviews, cast, and watch providers.
    """
    try:
        movie_id = int(movie_id)  # Convert to int
    except ValueError:
        return HttpResponseBadRequest("Invalid movie ID")  # Handle error

    # Fetch movie details
    movie = get_movie_details(movie_id)
    if not movie:
        return render(
            request, "movies/movie_not_found.html", {"movie_id": movie_id}
        )

    # Check if the movie is in the user's favorites
    is_favorite = FavoriteMovie.objects.filter(
        user=request.user, movie_id=movie_id
    ).exists()

    # Fetch additional details
    images = get_movie_images(movie_id)
    backdrops = images.get("backdrops", [])[:5]

    # Fetch watch providers
    watch_providers_data = (
            movie.get("watch/providers", {})
            .get("results", {})
            .get("GB", {})
        )

    watch_providers = {
        provider_type: [
            {
                **provider,
                "link": f"https://www.themoviedb.org/movie/{movie_id}/watch",
            }
            for provider in watch_providers_data.get(provider_type, [])
        ]
        for provider_type in ["flatrate", "buy", "rent"]
    }

    # Fetch reviews
    reviews = Review.objects.filter(movie_id=movie_id).order_by("-created_at")
    review_form = ReviewForm()

    # Fetch top 10 cast members
    cast = movie.get("credits", {}).get("cast", [])[:10]

    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie,
            "is_favorite": is_favorite,
            "movie_id": movie_id,
            "reviews": reviews,
            "review_form": review_form,
            "watch_providers": watch_providers,
            "cast": cast,
            "backdrops": backdrops,        },
    )


def get_movie_images(movie_id):
    """Fetch movie images (backdrops) from the TMDB API."""
    api_key = TMDB_API_KEY
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}/images?"
        f"api_key={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {}  # Return an empty dictionary in case of an error


from django.views.decorators.http import require_GET

@require_GET
def movie_detail_api(request, movie_id):
    """
    API endpoint to return trimmed movie details in JSON format.
    """
    movie = get_movie_details(movie_id)
    if not movie:
        return JsonResponse({"error": "Movie not found"}, status=404)

    # Fetch lightweight image data
    images = get_movie_images(movie_id)
    backdrops = images.get("backdrops", [])[:5]  # Limit to 3 images

    # Trim cast to top 10
    cast = movie.get("credits", {}).get("cast", [])[:10]

    # Get only 'GB' watch providers
    providers = (
        movie.get("watch/providers", {})
        .get("results", {})
        .get("GB", {})
    )

    # Build a smaller dict
    trimmed_data = {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "overview": movie.get("overview"),
        "poster_path": movie.get("poster_path"),
        "release_date": movie.get("release_date"),
        "vote_average": movie.get("vote_average"),
        "runtime": movie.get("runtime"),
        "genres": [g["name"] for g in movie.get("genres", [])],

        "cast": [
            {
                "name": c["name"],
                "character": c["character"],
                "profile_path": c["profile_path"],
            }
            for c in cast
        ],

        "backdrops": backdrops[:5],

        "watch_providers": {
            t: providers.get(t, [])
            for t in ["flatrate", "buy", "rent"]
        },

        "similar_movies": [
            {
                "id": sm["id"],
                "title": sm["title"],
                "poster_path": sm["poster_path"],
                "release_date": sm["release_date"],
            }
            for sm in movie.get("similar", {}).get("results", [])[:10]
        ],
    }

    return JsonResponse(trimmed_data)



@login_required
def get_favorite_movies(request):
    """Returns a list of movie IDs (integers) that the user has favorited."""
    user_favorites = FavoriteMovie.objects.filter(
        user=request.user
    ).values_list("movie_id", flat=True)

    # Convert movie_ids to integers
    favorite_movie_ids = list(map(int, user_favorites))

    return JsonResponse({"favorite_movie_ids": favorite_movie_ids})


@login_required
def toggle_favorite(request):
    """Toggles the favorite status of a movie for a user."""
    if request.method == "POST":
        try:
            movie_id = request.POST.get("movie_id")
            title = request.POST.get("title")
            poster_path = request.POST.get("poster_path")
            release_date = request.POST.get("release_date")
            rating = request.POST.get("rating")

            # Normalize poster path to full URL if needed
            if poster_path and not poster_path.startswith("http"):
                poster_path = f"https://image.tmdb.org/t/p/w500{poster_path}"

            # Validate movie_id
            try:
                movie_id = int(movie_id.strip())
            except (ValueError, AttributeError):
                return JsonResponse(
                    {"status": "error", "message": "Invalid movie ID"},
                    status=400,
                )

            # Convert rating to float, if available
            try:
                rating = float(rating) if rating else None
            except ValueError:
                rating = None

            # Get or create the FavoriteMovie object
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
                # Movie was already a favorite, so remove it
                favorite.delete()
                return JsonResponse({"status": "removed"})
            else:
                # Movie was added as a favorite
                return JsonResponse({"status": "added"})

        except Exception:
            return JsonResponse(
                {"status": "error", "message": "Internal server error"},
                status=500,
            )

    else:
        # Handle non-POST requests
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"},
            status=405,
        )
