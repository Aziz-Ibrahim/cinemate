from django.urls import path
from .views import RegisterView, CustomLoginView, profile_view, add_favorite_movie, remove_favorite_movie, change_password, contact_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/", profile_view, name="profile"),  # Logged-in user's profile
    path("profile/<str:username>/", profile_view, name="user_profile"),  # Any user's profile
    path('add_favorite/<int:movie_id>/', add_favorite_movie, name='add_favorite'),
    path("remove_favorite/<int:movie_id>/", remove_favorite_movie, name="remove_favorite"),
    path("change-password/", change_password, name="change_password"),
    path("contact/", contact_view, name="contact"),
]
