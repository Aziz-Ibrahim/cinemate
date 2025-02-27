from django.db import models
from django.conf import settings
# Create your models here.


class FavoriteMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # or use a more complex structure to store movie details

    def __str__(self):
        return f"{self.user.username}'s favorite movie"