from django.contrib import admin
from .models import Profile, FavoriteMovie


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.

    Provides a customized interface for managing user profiles in the
    Django admin panel.
    """
    list_display = ('user',)
    search_fields = ('user__username', 'country__name')


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    """
    Admin configuration for the FavoriteMovie model.

    Provides a customized interface for managing user's favorite movies in the
    Django admin panel.
    """
    list_display = ('user', 'title', 'movie_id', 'rating')
    search_fields = ('user__username', 'title')
    list_filter = ('user',)
