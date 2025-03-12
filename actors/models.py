from django.db import models

class Actor(models.Model):
    tmdb_id = models.IntegerField(unique=True)  # Link to TMDB ID
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    profile_path = models.CharField(max_length=255, blank=True)  # TMDB image path

    def __str__(self):
        return self.name
