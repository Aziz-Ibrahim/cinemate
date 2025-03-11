import requests
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Review
from .forms import ReviewForm

TMDB_API_KEY = settings.TMDB_API_KEY

def submit_review(request, movie_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie_id = movie_id
            review.save()

            # Convert rating to TMDB’s scale (1-5 → 2-10)
            user_rating = float(form.cleaned_data["rating"]) * 2  

            # Send rating to TMDB
            tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}/rating"
            headers = {
                "Authorization": f"Bearer {TMDB_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"value": user_rating}
            response = requests.post(tmdb_url, json=payload, headers=headers)

            if response.status_code == 201:
                print("Rating successfully submitted to TMDB!")
            else:
                print(f"Error submitting rating: {response.json()}")

            return redirect("movie_detail", movie_id=movie_id)
    else:
        form = ReviewForm()
    
    return render(request, "reviews/submit_review.html", {"form": form})
