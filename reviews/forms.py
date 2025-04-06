from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for creating and editing movie reviews.

    Allows users to rate a movie on a scale of 0 to 5 stars,
    with half-star increments,
    and provide a textual review.
    """

    # 0 to 5, in 0.5 increments
    RATING_CHOICES = [(i * 0.5, f"{i * 0.5}/5") for i in range(0, 11)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        help_text="Rate the movie from 0 to 5 stars.",
        required=True,
    )

    class Meta:
        """Meta class to define the model and fields used in the form."""

        model = Review
        fields = ["rating", "review_text"]
