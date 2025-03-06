from django.urls import path
from .views import submit_review

app_name = "reviews"

urlpatterns = [
    path("submit/<int:movie_id>/", submit_review, name="submit_review"),
]
