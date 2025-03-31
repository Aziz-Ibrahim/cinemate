import requests
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

TMDB_API_KEY = settings.TMDB_API_KEY

@login_required
def submit_review(request, movie_id):
    """
    Handles the submission of movie reviews and ratings.

    Allows logged-in users to submit or update reviews for a specific movie.
    The review and rating are stored locally and sent to TMDB API.

    Args:
        request (HttpRequest): The incoming HTTP request.
        movie_id (int): The TMDB movie ID for the movie being reviewed.

    Returns:
        HttpResponse: Renders the movie detail page with the review form or 
        redirects to the movie detail page after successful submission.
    """

    # Check if user already has a review for this movie
    existing_review = Review.objects.filter(movie_id=movie_id, user=request.user).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review) # Prefill if exists
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie_id = movie_id  # Store movie ID from TMDB
            review.save()

            # Convert rating to TMDB’s scale (0-5 → 0-10), or more accurately, (0-5 --> 0-10)
            user_rating = float(form.cleaned_data["rating"]) * 2

            # Send rating to TMDB
            tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}/rating"
            headers = {
                "Authorization": f"Bearer {settings.TMDB_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"value": user_rating}
            response = requests.post(tmdb_url, json=payload, headers=headers)

            if response.status_code == 201:
                print("Rating successfully submitted to TMDB!")
            else:
                print(f"Error submitting rating: {response.json()}")

            return redirect("movies:movie_detail", movie_id=movie_id)
    else:
        form = ReviewForm(instance=existing_review)  # Prefill form with existing review

    return render(request, "movies/movie_detail.html", {"form": form, "movie_id": movie_id})


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.body)
        review.review_text = data.get("review_text", review.review_text)
        review.rating = data.get("rating", review.rating)
        review.save()

        return JsonResponse({"success": True, "review_text": review.review_text})

    return JsonResponse({"success": False})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})