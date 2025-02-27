from django.urls import path
from .views import movie_detail, movie_list, toggle_favorite

urlpatterns = [
    path("", movie_list, name="movie_list"),
    path("toggle_favorite/", toggle_favorite, name="toggle_favorite"),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),
]
