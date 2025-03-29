from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Review model.

    Provides a customized interface for managing movie reviews in the Django 
    admin panel.
    """
    list_display = ('user', 'movie_id', 'rating', 'created_at')
    search_fields = ('user__username', 'review_text')
    list_filter = ('user', 'rating')