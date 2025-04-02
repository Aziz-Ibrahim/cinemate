/**
 * Executes initialization functions after the DOM content is fully loaded.
 */
document.addEventListener("DOMContentLoaded", function () {
    const movieId = extractMovieIdFromUrl();
    if (movieId) {
        fetchMovieDetails(movieId);
        initializeFavoriteButton(movieId);
        initializeBackdropCarousel();
        initializeLogoCarousel();
        setupReviewActions();
    } else {
        console.warn("Movie ID not found in URL. Check if the URL format is correct.");
    }
});

/**
 * Extracts the movie ID from the URL.
 * @returns {string|null} The extracted movie ID or null if not found.
 */
function extractMovieIdFromUrl() {
    const path = window.location.pathname;
    const match = path.match(/\/movies\/(\d+)\/?$/);
    return match ? parseInt(match[1], 10) : null;
}

/**
 * Fetches movie details and updates the DOM.
 * @param {string} movieId - The ID of the movie.
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
            displayVideos(data.videos.results);
            displayReviews(data.reviews.results);
            displaySimilarMovies(data.similar.results);
        })
        .catch(error => console.error("Error fetching movie details:", error));
}

/**
 * Initializes the favorite button.
 * @param {string} movieId - The ID of the movie.
 */
function initializeFavoriteButton(movieId) {
    const favButton = document.querySelector(".favorite-btn");
    if (!favButton) return;

    // Fetch user's favorite movies and update button state
    fetch("/movies/get_favorites/")
        .then(response => response.json())
        .then(data => {
            if (data.favorite_movie_ids.includes(parseInt(movieId))) {
                favButton.innerHTML = '<i class="fa-solid fa-heart"></i> Favorited';
                favButton.classList.replace("btn-outline-danger", "btn-danger");
            }
        });

    favButton.addEventListener("click", function () {
        const { movieId, title, posterPath, releaseDate, rating } = favButton.dataset;
        
        fetch("{% url 'movies:toggle_favorite' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ movieId, title, poster_path: posterPath, release_date: releaseDate, rating })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "added") {
                favButton.innerHTML = '<i class="fa-solid fa-heart"></i> Favorited';
                favButton.classList.replace("btn-outline-danger", "btn-danger");
            } else if (data.status === "removed") {
                favButton.innerHTML = '<i class="fa-regular fa-heart"></i> Add to Favorites';
                favButton.classList.replace("btn-danger", "btn-outline-danger");
            }
        })
        .catch(error => console.error("Error:", error));
    });
}

/**
 * Initializes backdrop image carousel.
 */
function initializeBackdropCarousel() {
    const backdrops = document.querySelectorAll('.backdrop-image');
    if (!backdrops.length) return;

    let index = 0;
    function showNextBackdrop() {
        backdrops.forEach(backdrop => backdrop.style.opacity = 0);
        backdrops[index].style.opacity = 1;
        index = (index + 1) % backdrops.length;
    }

    showNextBackdrop();
    setInterval(showNextBackdrop, 5000);
}

/**
 * Initializes logo image carousel.
 */
function initializeLogoCarousel() {
    const logos = document.querySelectorAll('.logo-image');
    if (!logos.length) return;

    let index = 0;
    function showNextLogo() {
        logos.forEach(logo => logo.style.opacity = 0);
        logos[index].style.opacity = 1;
        index = (index + 1) % logos.length;
    }

    showNextLogo();
    setInterval(showNextLogo, 3000);
}

/**
 * Handles review actions (edit & delete).
 */
function setupReviewActions() {
    document.querySelectorAll(".edit-review-btn").forEach(button => {
        button.addEventListener("click", function () {
            document.getElementById("edit-review-id").value = this.dataset.reviewId;
            document.getElementById("edit-review-text").value = this.dataset.reviewText;
            document.getElementById("edit-review-rating").value = this.dataset.reviewRating;

            new bootstrap.Modal(document.getElementById("editReviewModal")).show();
        });
    });

    document.getElementById("editReviewForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const reviewId = document.getElementById("edit-review-id").value;
        const reviewText = document.getElementById("edit-review-text").value;
        const reviewRating = document.getElementById("edit-review-rating").value;

        fetch(`/reviews/update/${reviewId}/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken"), "Content-Type": "application/json" },
            body: JSON.stringify({ review_text: reviewText, rating: reviewRating })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`review-text-${reviewId}`).textContent = reviewText;
                // Update the rating display
                const ratingElement = document.getElementById(`review-rating-${reviewId}`);
                if (ratingElement) {
                    ratingElement.textContent = `${reviewRating}/5`;
                }
                bootstrap.Modal.getInstance(document.getElementById("editReviewModal")).hide();
            } else {
                alert("Error updating review.");
            }
        });
    });

    document.querySelectorAll(".delete-review-btn").forEach(button => {
        button.addEventListener("click", function () {
            const reviewId = this.dataset.reviewId;
            if (!confirm("Are you sure you want to delete this review?")) return;

            fetch(`/reviews/delete/${reviewId}/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) document.getElementById(`review-${reviewId}`).remove();
                else alert("Error deleting review.");
            });
        });
    });
}

/**
 * Retrieves CSRF token from cookies.
 */
function getCookie(name) {
    return document.cookie.split("; ").reduce((acc, cookie) => {
        const [key, value] = cookie.split("=");
        return key === name ? decodeURIComponent(value) : acc;
    }, null);
}

/**
 * Displays watch providers.
 */
function displayWatchProviders(providers) {
    const container = document.getElementById("watch-providers");
    container.innerHTML = providers.length
        ? providers.map(p => `<li>${p.provider_name}</li>`).join('')
        : "<p>No providers available.</p>";
}

/**
 * Displays videos (trailers).
 */
function displayVideos(videos) {
    const container = document.getElementById("videos");
    container.innerHTML = videos.length
        ? videos.map(v => `<iframe width="250" height="150" src="https://www.youtube.com/embed/${v.key}" frameborder="0" allowfullscreen></iframe>`).join('')
        : "<p>No videos available.</p>";
}

/**
 * Displays movie reviews.
 */
function displayReviews(reviews) {
    const container = document.getElementById("reviews");
    container.innerHTML = reviews.length
        ? reviews.map(r => `<div class='mb-3'><strong>${r.author}</strong><p>${r.content}</p></div>`).join('')
        : "<p>No reviews available.</p>";
}

/**
 * Displays similar movies.
 */
function displaySimilarMovies(movies) {
    const container = document.getElementById("similar-movies");
    container.innerHTML = movies.length
        ? movies.map(m => `<div class="card" style="width: 10rem;"><img class="card-img-top" src="https://image.tmdb.org/t/p/w200/${m.poster_path}" alt="${m.title}"><div class="card-body"><p class="card-text">${m.title}</p></div></div>`).join('')
        : "<p>No similar movies found.</p>";
}
