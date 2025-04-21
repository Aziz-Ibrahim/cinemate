import requests
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from movies.views import get_movie_details
from .models import Review
from .forms import ReviewForm

TMDB_API_KEY = settings.TMDB_API_KEY


@login_required
def submit_review(request, movie_id):
    """
    Handles submission of movie reviews and ratings, via AJAX or normal POST.
    """
    is_ajax = request.headers.get("X-Requested-With", "").lower() == \
        "xmlhttprequest"

    existing_review = Review.objects.filter(
        movie_id=movie_id, user=request.user
    ).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie_id = movie_id
            review.save()

            # TMDB rating (0.0–10.0 scale)
            user_rating = float(form.cleaned_data["rating"]) * 2
            tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}/rating"
            headers = {
                "Authorization": f"Bearer {settings.TMDB_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {"value": user_rating}
            response = requests.post(tmdb_url, json=payload, headers=headers)

            if response.status_code != 201:
                print(
                    f"TMDB rating error: {response.status_code} - "
                    f"{response.text}"
                )

            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "username": request.user.username,
                    "review_text": review.review_text,
                    "rating": str(review.rating),
                    "review_id": review.id,
                })

            return redirect("movies:movie_detail", movie_id=movie_id)

        # Invalid form
        if is_ajax:
            return JsonResponse({"success": False, "errors": form.errors})

    # GET request or other
    form = ReviewForm(instance=existing_review)
    movie = get_movie_details(movie_id)
    return render(
        request,
        "movies/movie_detail.html",
        {"form": form, "movie": movie}
    )




@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.body)
        review.review_text = data.get("review_text", review.review_text)
        review.rating = data.get("rating", review.rating)
        review.save()

        return JsonResponse(
            {"success": True, "review_text": review.review_text})

    return JsonResponse({"success": False})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})
