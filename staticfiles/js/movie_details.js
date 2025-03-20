/**
 * Executes initialization functions after the DOM content is fully loaded.
 * Extracts the movie ID from the URL and fetches movie details.
 */
document.addEventListener("DOMContentLoaded", function () {
    const path = window.location.pathname;
    console.log("Current URL Path:", path); // Log the full path

    const movieIdMatch = path.match(/\/movies\/(\d+)\/?$/);
    if (movieIdMatch) {
        const movieId = movieIdMatch[1];
        console.log("Extracted Movie ID:", movieId);
        fetchMovieDetails(movieId);
    } else {
        console.warn("Movie ID not found in URL. Check if the URL format is correct.");
    }
});

/**
 * Fetches movie details from the API and updates the DOM with the retrieved data.
 * @param {string} movieId - The ID of the movie to fetch.
 */
function fetchMovieDetails(movieId) {
    fetch(`/movies/api/details/${movieId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("movie-poster").src = `https://image.tmdb.org/t/p/w500/${data.poster_path}`;
            document.getElementById("movie-title").textContent = data.title;
            document.getElementById("release-date").textContent = data.release_date;
            document.getElementById("rating").textContent = data.vote_average;
            document.getElementById("overview").textContent = data.overview;

            displayWatchProviders(data.watch_providers);
            displayVideos(data.videos.results);   // Fix
            displayReviews(data.reviews.results); // Fix
            displaySimilarMovies(data.similar.results); // Fix
        })
        .catch(error => console.error("Error fetching movie details:", error));
}


document.addEventListener('DOMContentLoaded', function() {
    const backdrops = document.querySelectorAll('.backdrop-image');
    let index = 0;

    function showNextBackdrop() {
        backdrops.forEach(backdrop => backdrop.style.opacity = 0); // Hide all
        backdrops[index].style.opacity = 1; // Show current
        index = (index + 1) % backdrops.length; // Loop through images
    }

    if(backdrops.length > 0){
      showNextBackdrop(); // Show initial image
      setInterval(showNextBackdrop, 5000); // Change image every 5 seconds
    }

    const logos = document.querySelectorAll('.logo-image');
    let logoIndex = 0;

    function showNextLogo() {
        logos.forEach(logo => logo.style.opacity = 0); // Hide all
        logos[logoIndex].style.opacity = 1; // Show current
        logoIndex = (logoIndex + 1) % logos.length; // Loop through images
    }

    if(logos.length > 0){
      showNextLogo(); // Show initial image
      setInterval(showNextLogo, 3000); // Change image every 3 seconds
    }
});

/**
 * Toggle Favorite Movie
 * @param {string} movieId - The ID of the movie to toggle favorite status.
 * @param {string} title - The title of the movie.
 * @param {string} posterPath - The poster path of the movie.
 * @param {string} releaseDate - The release date of the movie.
 * @param {string} rating - The rating of the movie.
 */
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".favorite-btn").forEach(button => {
        button.addEventListener("click", function () {
            let movieId = this.dataset.movieId;
            let title = this.dataset.title;
            let posterPath = this.dataset.posterPath;
            let releaseDate = this.dataset.releaseDate;
            let rating = this.dataset.rating;

            fetch("{% url 'toggle_favorite' %}", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    movie_id: movieId,
                    title: title,
                    poster_path: posterPath,
                    release_date: releaseDate,
                    rating: rating
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "added") {
                    this.innerHTML = '<i class="fa-solid fa-heart"></i> Favorited';
                    this.classList.remove("btn-outline-danger");
                    this.classList.add("btn-danger");
                } else if (data.status === "removed") {
                    this.innerHTML = '<i class="fa-regular fa-heart"></i> Add to Favorites';
                    this.classList.remove("btn-danger");
                    this.classList.add("btn-outline-danger");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});

/**
 * Function to get CSRF token
 */ 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            let trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}


/**
 * Displays watch providers in the designated container.
 * @param {Array} providers - An array of watch provider objects.
 */
function displayWatchProviders(providers) {
    const container = document.getElementById("watch-providers");
    container.innerHTML = providers.length
        ? providers.map(p => `<li>${p.provider_name}</li>`).join('')
        : "<p>No providers available.</p>";
}

/**
 * Displays videos (e.g., trailers) in the designated container.
 * @param {Array} videos - An array of video objects.
 */
function displayVideos(videos) {
    const container = document.getElementById("videos");
    container.innerHTML = videos.length
        ? videos.map(v => `<iframe width="250" height="150" src="https://www.youtube.com/embed/$${v.key}" frameborder="0" allowfullscreen></iframe>`).join('')
        : "<p>No videos available.</p>";
}

/**
 * Displays reviews in the designated container.
 * @param {Array} reviews - An array of review objects.
 */
function displayReviews(reviews) {
    const container = document.getElementById("reviews");
    container.innerHTML = reviews.length
        ? reviews.map(r => `<div class='mb-3'><strong>${r.author}</strong><p>${r.content}</p></div>`).join('')
        : "<p>No reviews available.</p>";
}

document.addEventListener("DOMContentLoaded", function () {
    // Open Edit Modal with existing review data
    document.querySelectorAll(".edit-review-btn").forEach(button => {
        button.addEventListener("click", function () {
            const reviewId = this.getAttribute("data-review-id");
            const reviewText = this.getAttribute("data-review-text");
            const reviewRating = this.getAttribute("data-review-rating");

            document.getElementById("edit-review-id").value = reviewId;
            document.getElementById("edit-review-text").value = reviewText;
            document.getElementById("edit-review-rating").value = reviewRating;

            let modal = new bootstrap.Modal(document.getElementById("editReviewModal"));
            modal.show();
        });
    });

    // Handle Review Update AJAX
    document.getElementById("editReviewForm").addEventListener("submit", function (e) {
        e.preventDefault();

        const reviewId = document.getElementById("edit-review-id").value;
        const reviewText = document.getElementById("edit-review-text").value;
        const reviewRating = document.getElementById("edit-review-rating").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch(`/reviews/update/${reviewId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ review_text: reviewText, rating: reviewRating })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`review-text-${reviewId}`).textContent = reviewText;
                let modal = bootstrap.Modal.getInstance(document.getElementById("editReviewModal"));
                modal.hide();
            } else {
                alert("Error updating review.");
            }
        });
    });

    // Handle Review Delete AJAX
    document.querySelectorAll(".delete-review-btn").forEach(button => {
        button.addEventListener("click", function () {
            const reviewId = this.getAttribute("data-review-id");
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            if (confirm("Are you sure you want to delete this review?")) {
                fetch(`/reviews/delete/${reviewId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(`review-${reviewId}`).remove();
                    } else {
                        alert("Error deleting review.");
                    }
                });
            }
        });
    });
});


/**
 * Displays similar movies in the designated container.
 * @param {Array} movies - An array of similar movie objects.
 */
function displaySimilarMovies(movies) {
    const container = document.getElementById("similar-movies");
    container.innerHTML = movies.length
        ? movies.map(m => `<div class="card" style="width: 10rem;"><img class="card-img-top" src="https://image.tmdb.org/t/p/w200/${m.poster_path}" alt="${m.title}"><div class="card-body"><p class="card-text">${m.title}</p></div></div>`).join('')
        : "<p>No similar movies found.</p>";
}