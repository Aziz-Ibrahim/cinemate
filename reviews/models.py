from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    """
    Represents a movie review submitted by a user.

    Attributes:
        user (User): The user who wrote the review.
        movie_id (int): The TMDB movie ID for the reviewed movie.
        review_text (str): The text content of the review.
        rating (Decimal): The user's rating for the movie (0.0 to 5.0).
        created_at (datetime): The date and time when the review was created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # TMDB movie ID
    review_text = models.TextField()
    # Store user's rating locally, Scale: 0.0-5.0
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the review.

        Returns:
            str: A string indicating the reviewer and the movie ID.
        """
        return f"Review by {self.user.username} for Movie ID {self.movie_id}"