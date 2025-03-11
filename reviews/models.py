from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    RATING_CHOICES = [
        (0.5, '★☆☆☆☆ (0.5)'),
        (1, '★☆☆☆☆ (1)'),
        (1.5, '★★☆☆☆ (1.5)'),
        (2, '★★☆☆☆ (2)'),
        (2.5, '★★★☆☆ (2.5)'),
        (3, '★★★☆☆ (3)'),
        (3.5, '★★★★☆ (3.5)'),
        (4, '★★★★☆ (4)'),
        (4.5, '★★★★★ (4.5)'),
        (5, '★★★★★ (5)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # TMDB movie ID
    review_text = models.TextField()
    rating = models.FloatField(choices=RATING_CHOICES)  # Store user's rating locally
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.movie_id}"
