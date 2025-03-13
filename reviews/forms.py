from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i}/10") for i in range(0, 11)]  # 0 to 10

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["rating", "review_text"]
