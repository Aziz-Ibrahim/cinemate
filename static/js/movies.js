/**
 * Executes initialization functions after the DOM content is fully loaded.
 */
document.addEventListener("DOMContentLoaded", function () {
    initializeMovieDetails();
    initializeReviewForm();
    setupInfiniteScroll();
});

/**
 * Fetches and displays movie details from the server.
 * Parses the movie ID from the URL and updates the DOM with movie information.
 */
function initializeMovieDetails() {
    const path = window.location.pathname;
    const movieIdMatch = path.match(/\/movies\/(\d+)\//);

    if (movieIdMatch && movieIdMatch[1]) {
        const movieId = movieIdMatch[1];

        fetch(`/movies/${movieId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById("movie-title").textContent = data.title;
                document.getElementById("movie-overview").textContent = data.overview;
                document.getElementById("movie-rating").textContent = data.vote_average;
                document.getElementById("movie-poster").src = `https://image.tmdb.org/t/p/w500/${data.poster_path}`;
            })
            .catch(error => console.error("Error fetching movie details:", error));
    }
}

/**
 * Initializes the review form submission handler.
 * Prevents default form submission and sends review data to the server via AJAX.
 */
function initializeReviewForm() {
    const reviewForm = document.getElementById("review-form");
    if (!reviewForm) return;

    reviewForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(reviewForm);
        const movieId = window.location.pathname.split("/")[2];

        fetch(`/movies/${movieId}/submit_review/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") location.reload();
                else alert("Error submitting review. Please try again.");
            })
            .catch(error => console.error("Error submitting review:", error));
    });
}

/**
 * Sets up event delegation for favorite button clicks.
 * Listens for click events on the document and triggers the toggleFavorite function for elements with the 'favorite-btn' class.
 */
document.addEventListener("click", function (event) {
    const target = event.target.closest(".favorite-btn");
    if (!target) return; // Ignore clicks outside favorite buttons
    toggleFavorite.call(target);
});

/**
 * Toggles the favorite status of a movie.
 * Sends an AJAX request to the server to add or remove the movie from the user's favorites.
 */
function toggleFavorite() {
    const movieId = this.dataset.movieId;
    const formData = new URLSearchParams({
        "movie_id": movieId,
        "title": this.dataset.title || "",
        "poster_path": this.dataset.posterpath || "",
        "release_date": this.dataset.releasedate || "",
        "rating": this.dataset.rating || "0"
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
            this.innerHTML = `<i class="fa fa-heart"></i> ${data.status === "added" ? "Remove from favorites" : "Add to favorites"}`;
        })
        .catch(error => console.error("Error toggling favorite:", error));
}

/**
 * Sets up infinite scroll functionality for loading more movies.
 * Loads additional movie data when the user scrolls to the bottom of the page.
 */
function setupInfiniteScroll() {
    let currentPage = 1;
    let totalPages = Infinity;

    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 50 && currentPage < totalPages) {
            loadMoreMovies(currentPage);
        }
    });

    /**
     * Loads more movies from the server and appends them to the DOM.
     * @param {number} page - The page number to load.
     */
    function loadMoreMovies(page) {
        const sortBySelect = document.getElementById("sortSelect");
        if (!sortBySelect) {
            console.error("Sort by select element not found.");
            return;
        }

        fetch(`/movies/?sort_by=${sortBySelect.value}&page=${currentPage + 1}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then(response => response.text())
            .then(text => JSON.parse(text))
            .then(data => {
                if (data.movies.length > 0) {
                    appendMoviesToDOM(data.movies);
                    currentPage++;
                    totalPages = data.total_pages;
                }
            })
            .catch(error => console.error("Error fetching more movies:", error));
    }
}

/**
 * Appends movie cards to the DOM.
 * @param {Array} movies - An array of movie objects to append.
 */
function appendMoviesToDOM(movies) {
    const movieContainer = document.querySelector(".row.mt-4");
    const movieRow = document.createElement("div");
    movieRow.className = "row g-4";

    movies.forEach(movie => {
        const movieCard = document.createElement("div");
        movieCard.className = "col-12 col-md-4 col-lg-3 card-deck d-flex";
        movieCard.innerHTML = `
            <div class="card mb-4 shadow-sm" style="height: 100%;">
                <img src="${movie.poster_path ? `https://image.tmdb.org/t/p/w500/${movie.poster_path}` : '/static/images/movie-card-placeholder-img.png'}"
                    class="card-img-top" alt="${movie.title}" style="object-fit: cover; height: 300px;">
                <div class="card-body d-flex flex-column justify-content-between">
                    <h5 class="card-title">${movie.title}</h5>
                    <p class="card-text">${movie.overview.split(" ").slice(0, 20).join(" ")}...</p>
                    <div class="btn-wrapper text-center d-flex justify-content-between">
                        <a href="/movies/${movie.id}/" class="btn btn-dark card-link">Show More</a>
                        <button class="btn btn-outline-danger card-link favorite-btn" 
                                data-movie-id="${movie.id}" data-title="${movie.title}" 
                                data-posterpath="${movie.poster_path}" 
                                data-releasedate="${movie.release_date}" 
                                data-rating="${movie.vote_average}">
                            <i class="fa fa-heart"></i> Add to List
                        </button>
                    </div>
                </div>
            </div>`;
        movieRow.appendChild(movieCard);
    });

    movieContainer.appendChild(movieRow);
}

/**
 * Adds a "Back to Top" button that appears when the user scrolls down.
 * The button smoothly scrolls the page back to the top when clicked.
 *
 * Behavior:
 * - Listens for the DOM to fully load.
 * - Shows the button when the user scrolls down 300px or more.
 * - Hides the button when the user scrolls above 300px.
 * - Smoothly scrolls to the top when the button is clicked.
 */
document.addEventListener("DOMContentLoaded", function () {
    const backToTopButton = document.getElementById("back-to-top");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 300) {
            backToTopButton.style.display = "flex";
        } else {
            backToTopButton.style.display = "none";
        }
    });

    backToTopButton.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});


/**
 * Retrieves the value of a cookie by name.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} - The cookie value or null if not found.
 */
function getCookie(name) {
    return document.cookie.split("; ").reduce((cookieValue, cookie) => {
        if (cookie.startsWith(name + "=")) return decodeURIComponent(cookie.split("=")[1]);
        return cookieValue;
    }, null);
}