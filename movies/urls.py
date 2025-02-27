from django.urls import path
from .views import movie_list
from .views import toggle_favorite

urlpatterns = [
    path("", movie_list, name="movie_list"),
    path("toggle_favorite/", toggle_favorite, name="toggle_favorite"),
]
