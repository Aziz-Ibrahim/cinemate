from django.contrib import admin
from .models import Actor


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Actor model.

    Provides a customized interface for managing actor information in the
    Django admin panel.
    """
    list_display = ('name', 'tmdb_id', 'date_of_birth')
    search_fields = ('name',)
    list_filter = ('date_of_birth',)
