import requests
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
        movie_id = int(movie_id) #Convert to int
    except ValueError:
        return HttpResponseBadRequest("Invalid movie ID") #Handle error

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
    backdrops = images.get("backdrops", [])
    logos = [
        image for image in images.get("logos", [])
        if image.get("iso_639_1") == "en"
    ]

    # Get the user's country if logged in, otherwise default to "GB"
    user_country = "GB"
    if request.user.is_authenticated:
        try:
            user_country = request.user.profile.country.code or "GB"
        except Profile.DoesNotExist:
            print("WARNING: User has no profile, defaulting to 'GB'")

    # Fetch watch providers
    watch_providers_data = (
        movie.get
        ("watch/providers", {}).get("results", {}).get(user_country, {})
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
            "reviews": reviews,
            "review_form": review_form,
            "watch_providers": watch_providers,
            "cast": cast,
            "backdrops": backdrops,
            "logos": logos,
            "user_country": user_country,
        },
    )

def get_movie_images(movie_id):
    """Fetch movie images (backdrops and logos) from the TMDB API."""
    api_key = TMDB_API_KEY
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {}  # Return an empty dictionary in case of an error


def movie_detail_api(request, movie_id):
    """
    API endpoint to return movie details in JSON format.
    If the movie is not found, return a 404 error.
    """
    movie = get_movie_details(movie_id)
    if not movie:
        return JsonResponse({"error": "Movie not found"}, status=404)

    return JsonResponse(movie)  # Return movie data as JSON


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
    """
    Toggle favorite status for a movie.
    If the movie is already a favorite, remove it. Otherwise, add it.
    """
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")

        # Validate movie_id
        try:
            movie_id = int(movie_id.strip())  # Stripping whitespace if necessary
        except (ValueError, AttributeError):  # Handle cases where movie_id is None or invalid
            return JsonResponse({"status": "error"}, status=400)

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
