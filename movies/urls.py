from django.urls import path
from . import views
from .views import movie_detail, movie_list, toggle_favorite


app_name = "movies" # This is the namespace for the movies app

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
]
