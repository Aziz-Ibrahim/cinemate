from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    RegisterView,
    CustomLoginView,
    profile_view,
    add_favorite_movie,
    remove_favorite_movie,
    change_password,
    contact_view,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/", profile_view, name="profile"),  # Logged-in user's profile
    path("profile/<str:username>/", profile_view, name="user_profile"),
    path("add_favorite/<int:movie_id>/", add_favorite_movie, name="add_favorite"),  # noqa: E501
    path(
        "remove_favorite/<int:movie_id>/", remove_favorite_movie, name="remove_favorite"  # noqa: E501
    ),
    path("change-password/", change_password, name="change_password"),
    path("contact/", contact_view, name="contact"),
]
