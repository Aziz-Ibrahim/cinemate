from django.urls import path
from .views import actor_detail

urlpatterns = [
    path("<int:actor_id>/", actor_detail, name="actor_detail"),
]
