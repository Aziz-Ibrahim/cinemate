from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    country = CountryField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.country}"


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255, default="Unknown Movie")
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.CharField(max_length=10, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        unique_together = ('user', 'movie_id') #ensures that a user cannot have duplicate movies.