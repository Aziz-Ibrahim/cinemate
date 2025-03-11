from django import forms
from .models import Review
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review_text", "rating"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-select"}),
            "review_text": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Write your review here"}),
        }
