from django.urls import path, include
from .views import (
    movie_detail,
    movie_list,
    toggle_favorite,
    movie_detail_api,
    trending_movies,
    get_favorite_movies
)

app_name = "movies"

urlpatterns = [
    path("", movie_list, name="movie_list"),
    path("<int:movie_id>/", movie_detail, name="movie_detail"),
    path("toggle_favorite/", toggle_favorite, name="toggle_favorite"),
    path(
        "get_favorite_movies/", get_favorite_movies, name="get_favorite_movies"
    ),
    path(
        "api/details/<int:movie_id>/",
        movie_detail_api,
        name="movie_detail_api",
    ),
    path("trending/", trending_movies, name="trending"),
    path("reviews/", include("reviews.urls")),
]
