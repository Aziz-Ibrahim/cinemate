from django import forms
from .models import Review
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0.5, "★☆☆☆☆ (0.5)"),
        (1, "★☆☆☆☆ (1)"),
        (1.5, "★☆☆☆☆ (1.5)"),
        (2, "★★☆☆☆ (2)"),
        (2.5, "★★☆☆☆ (2.5)"),
        (3, "★★★☆☆ (3)"),
        (3.5, "★★★☆☆ (3.5)"),
        (4, "★★★★☆ (4)"),
        (4.5, "★★★★☆ (4.5)"),
        (5, "★★★★★ (5)"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Your Rating (1-5)"
    )

    class Meta:
        model = Review
        fields = ["review_text", "rating"]
