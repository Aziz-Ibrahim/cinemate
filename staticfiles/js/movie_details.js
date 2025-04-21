/**
 * Extracts the movie ID from the URL.
 * @returns {number|null} The extracted movie ID or null if not found.
 */
function extractMovieIdFromUrl() {
    const path = window.location.pathname;
    const match = path.match(/\/movies\/(\d+)\/?$/);
    return match ? parseInt(match[1], 10) : null;
}

/**
 * Fetches movie details and updates the DOM.
 * @param {number} movieId - The ID of the movie.
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
        });
}

/**
 * Updates the UI of the favorite button based on favorite status.
 */
function updateFavoriteButtonUI(button, isFavorite) {
    button.innerHTML = `<i class="fa-${isFavorite ? "solid" : "regular"} fa-heart"></i> ${isFavorite ? "Remove" : "Add to Favs"}`;
    button.classList.toggle("btn-danger", isFavorite);
    button.classList.toggle("btn-outline-danger", !isFavorite);
}

/**
 * Toggles the favorite status of a movie and updates the UI.
 */
function toggleFavorite(button, event) {
    if (event) {
        event.stopPropagation();
    }
    button.disabled = true;

    console.log("Toggling favorite for movie:", button.dataset.movieId);

    const movieId = parseInt(button.dataset.movieId, 10);
    const formData = new URLSearchParams({
        "movie_id": movieId,
        "title": button.dataset.title || "",
        "poster_path": button.dataset.posterPath || "",
        "release_date": button.dataset.releasedate || "",
        "rating": button.dataset.rating || "0"
    });

    fetch("/movies/toggle_favorite/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        console.log("Favorite toggle response:", data);
        const isNowFavorite = data.status === "added";
        console.log("UI should reflect favorite:", isNowFavorite);
        updateFavoriteButtonUI(button, isNowFavorite);
    })
    .catch(error => console.error("Error toggling favorite:", error))
    .finally(() => {
        button.disabled = false;
    });
    console.log("Sending poster_path:", button.dataset.posterPath);
}

/**
 * Debounces the favorite button click to prevent multiple requests.
 * @param {Function} func - The function to debounce.
 * @param {number} delay - The delay in milliseconds.
 * @returns {Function} - A debounced version of the function.
 */
function debounce(fn, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}


/**
 * Initializes the favorite button.
 * @param {number} movieId - The ID of the movie.
 */
function initializeFavoriteButtons(movieId) {
    const favButton = document.querySelector(".favorite-btn");
    if (!favButton) return;

    // Fetch user's favorite movies and check if the current movie is a favorite
    fetch("/movies/get_favorite_movies/")
        .then(response => response.json())
        .then(data => {
            const favoriteMovieIds = data.favorite_movie_ids;
            // Initialize main movie button first
            initializeMainMovieFavoriteButton(favButton, movieId, favoriteMovieIds);
            // Then initialize similar movie buttons
            initializeSimilarMoviesFavoriteButtons(favoriteMovieIds);
        })
        .catch(error => console.error("Error fetching favorites:", error));
}

/**
 * Initializes main movie favorite button and its event listener.
 */
function initializeMainMovieFavoriteButton(favButton, movieId, favoriteMovieIds) {
    // REMOVE ANY PREVIOUS EVENT LISTENERS
    favButton.replaceWith(favButton.cloneNode(true));
    const newButton = document.querySelector(".favorite-btn");

    // Check if the main movie is in the user's favorites
    const isFavorite = favoriteMovieIds.includes(movieId);
    updateFavoriteButtonUI(newButton, isFavorite);

    // Create debounced version of toggleFavorite inside here
    const debouncedToggle = debounce((event) => {
        toggleFavorite(newButton, event);
    }, 300);

    newButton.addEventListener("click", debouncedToggle);
}

/**
 * Initializes favorite buttons for similar movies.
 * @param {Array} favoriteMovieIds - Array of favorite movie IDs.
 */
function initializeSimilarMoviesFavoriteButtons(favoriteMovieIds) {
    const similarMovieButtons = document.querySelectorAll(".similar-movie-fav-btn");

    similarMovieButtons.forEach(button => {
        const movieId = parseInt(button.dataset.movieId, 10);

        // Check if this similar movie is in the user's favorites
        const isFavorite = favoriteMovieIds.includes(movieId);
        updateFavoriteButtonUI(button, isFavorite);

        // Create debounced version of toggleFavorite inside here for similar movies
        const debouncedToggle = debounce((event) => {
            toggleFavorite(button, event);
        }, 300);

        button.addEventListener("click", debouncedToggle);
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
 * Handles review submission.
 */
function setupAjaxReviewSubmission() {
    const form = document.getElementById("review-form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest"
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const newReview = `
                <div class="review p-3 mb-3 border rounded" id="review-${data.review_id}">
                    <div class="d-flex align-items-center mb-2">
                        <a href="/profile/${data.username}/" class="fw-bold me-2 link-dark text-decoration-none">
                            ${data.username}
                        </a>
                        <span class="text-muted">Just now</span>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <span class="badge bg-warning text-dark" id="review-rating-${data.review_id}">${data.rating}/5</span>
                    </div>
                    <p id="review-text-${data.review_id}">${data.review_text}</p>
                    <button class="btn btn-sm btn-outline-dark edit-review-btn" data-review-id="${data.review_id}" data-review-text="${data.review_text}" data-review-rating="${data.rating}">
                        Edit
                    </button>
                    <button class="btn btn-sm btn-outline-danger delete-review-btn" data-review-id="${data.review_id}">
                        Delete
                    </button>
                </div>
                `;

                // Clear previous errors
                const errorContainer = document.getElementById("review-errors");
                if (errorContainer) {
                    errorContainer.classList.add("d-none");
                    errorContainer.innerHTML = "";
                }


                // Check if the review already exists in the DOM
                const existingReview = document.getElementById(`review-${data.review_id}`);
                if (existingReview) {
                    existingReview.outerHTML = newReview;
                } else {
                    document.getElementById("reviews").insertAdjacentHTML("afterbegin", newReview);
}

                form.reset(); // Clear the form (including radio stars)

                // Refresh edit/delete handlers
                setupReviewActions();
            } else {
                const errorContainer = document.getElementById("review-errors");
                if (errorContainer) {
                    // Clear previous errors
                    errorContainer.classList.remove("d-none");
                    errorContainer.innerHTML = "";
            
                    // Loop through each field error and show a detailed message
                    let errorMessages = "";
            
                    // Loop through the fields
                    for (const [field, messages] of Object.entries(data.errors)) {
                        let fieldName = field.charAt(0).toUpperCase() + field.slice(1); // Capitalize the field name
            
                        // For example, if the field is 'rating', change the message to 'Rating is required'
                        if (field === "rating") {
                            errorMessages += `<li>Please select a ${fieldName.toLowerCase()}.</li>`;
                        } else if (field === "review_text") {
                            errorMessages += `<li>Please enter a review text.</li>`;
                        } else {
                            errorMessages += `<li>${fieldName} is required.</li>`;
                        }
                    }
            
                    // Display the errors
                    errorContainer.innerHTML = `<ul class="mb-0">${errorMessages}</ul>`;
                }
            }            
        });
    });
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
 * Executes initialization functions after the DOM content is fully loaded.
 */
document.addEventListener("DOMContentLoaded", function () {
    const movieId = extractMovieIdFromUrl();
    if (movieId) {
        fetchMovieDetails(movieId);

        // Initialize both the main movie's and similar movies' favorite buttons
        initializeFavoriteButtons(movieId);

        initializeBackdropCarousel();
        initializeLogoCarousel();
        setupReviewActions();
        setupAjaxReviewSubmission();
    } else {
        console.warn("Movie ID not found in URL. Check if the URL format is correct.");
    }
});
