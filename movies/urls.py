from django.urls import path, include
from .views import movie_detail, movie_list, toggle_favorite

app_name = "movies"

urlpatterns = [
    path("", movie_list, name="movie_list"),
    path("<int:movie_id>/", movie_detail, name="movie_detail"),
    path("toggle_favorite/", toggle_favorite, name="toggle_favorite"),
    path("reviews/", include("reviews.urls")),  # Include reviews URLs
]
