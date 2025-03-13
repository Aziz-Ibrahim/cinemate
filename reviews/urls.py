from django.urls import path
from .views import submit_review, update_review, delete_review

app_name = "reviews"

urlpatterns = [
    path("submit/<int:movie_id>/", submit_review, name="submit_review"),
    path("update/<int:review_id>/", update_review, name="update_review"),
    path("delete/<int:review_id>/", delete_review, name="delete_review"),
]
