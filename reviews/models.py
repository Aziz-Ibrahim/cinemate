from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # TMDB movie ID
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=0)  # Store user's rating locally, Scale: 0-10
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for Movie ID {self.movie_id}"