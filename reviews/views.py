from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

@login_required
def submit_review(request, movie_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associate review with logged-in user
            review.movie_id = movie_id  # Store the movie ID
            review.save()
            return redirect("movies:movie_detail", movie_id=movie_id)  # Redirect back to movie page

    return redirect("movies:movie_detail", movie_id=movie_id)  # Redirect in case of errors
