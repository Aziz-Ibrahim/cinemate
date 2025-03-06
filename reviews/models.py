from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆ (1)'),
        (2, '★★☆☆☆ (2)'),
        (3, '★★★☆☆ (3)'),
        (4, '★★★★☆ (4)'),
        (5, '★★★★★ (5)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # Foreign key to TMDB movie ID
    review_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.movie_id}"
