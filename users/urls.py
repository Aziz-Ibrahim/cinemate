from django.urls import path
from .views import RegisterView, CustomLoginView, profile_view, add_favorite_movie
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/", profile_view, name="profile"),
    path('add_favorite/<int:movie_id>/', add_favorite_movie, name='add_favorite'),
]
