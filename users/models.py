from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


class Profile(models.Model):
    """Represents a user profile."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self):
        return self.user.username


class FavoriteMovie(models.Model):
    """Represents a movie favorited by a user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255, default="Unknown Movie")
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.CharField(max_length=10, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        # Ensures no duplicate movies per user.
        unique_together = ("user", "movie_id")
