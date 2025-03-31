
/**
 * Adds a "Back to Top" button that appears when the user scrolls down.
 */
function initializeBackToTopButton() {
    const backToTopButton = document.getElementById("back-to-top");
    if (!backToTopButton) return;

    window.addEventListener("scroll", function () {
        backToTopButton.style.display = window.scrollY > 300 ? "flex" : "none";
    });

    backToTopButton.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

/**
 * Initializes favorite buttons, ensuring favorite status persists.
 */
function initializeFavoriteButtons() {
    document.querySelectorAll(".favorite-btn").forEach(button => {
        const isFavorite = button.dataset.isFavorite === "true";
        updateFavoriteButtonUI(button, isFavorite);

        button.addEventListener("click", function () {
            toggleFavorite(this);
        });
    });
}

/**
 * Toggles the favorite status of a movie and updates the UI.
 */
function toggleFavorite(button) {
    const movieId = button.dataset.movieId;
    const formData = new URLSearchParams({
        "movie_id": movieId,
        "title": button.dataset.title || "",
        "poster_path": button.dataset.posterpath || "",
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
        const isNowFavorite = data.status === "added";
        updateFavoriteButtonUI(button, isNowFavorite);
    })
    .catch(error => console.error("Error toggling favorite:", error));
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
 * Fetches and displays movie details from the server.
 */
function initializeMovieDetails() {
    const movieIdMatch = window.location.pathname.match(/\/movies\/(\d+)\//);
    if (!movieIdMatch) return;

    fetch(`/movies/${movieIdMatch[1]}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("movie-title").textContent = data.title;
            document.getElementById("movie-overview").textContent = data.overview;
            document.getElementById("movie-rating").textContent = data.vote_average;
            document.getElementById("movie-poster").src = `https://image.tmdb.org/t/p/w500/${data.poster_path}`;
        })
        .catch(error => console.error("Error fetching movie details:", error));
}

/**
 * Handles review form submission via AJAX.
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

let currentPage = 0;
let totalPages = Infinity;
let isFetching = false;
const fetchedPages = new Set();

/**
 * Debounces a function to limit its execution until a certain time has passed
 * after the last call. Prevents excessive function calls from rapid events.
 *
 * @param {Function} func - The function to debounce.
 * @param {number} delay - The delay in milliseconds.
 * @returns {Function} - A debounced version of the function.
 */
function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func(...args), delay);
    };
}

/**
 * Fetches and appends the next page of movies to the DOM.
 * Ensures that movies are not duplicated and updates the current page and total pages.
 */
function loadMoreMovies() {
    if (isFetching || currentPage >= totalPages || fetchedPages.has(currentPage + 1)) {
        return;
    }

    isFetching = true;
    let nextPage = currentPage + 1;
    fetchedPages.add(nextPage);

    const sortBySelect = document.getElementById("sortSelect");
    let sortByValue = "popularity.desc";
    if (sortBySelect) {
        sortByValue = sortBySelect.value;
    }

    fetch(`/movies/?sort_by=${sortByValue}&page=${nextPage}`, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.movies.length > 0) {
            appendMoviesToDOM(data.movies);
            currentPage = nextPage;
            totalPages = data.total_pages;
        } else {
            console.warn(`No movies found for page ${nextPage}`);
        }
    })
    .catch(error => {
        console.error("Error fetching more movies:", error);
    })
    .finally(() => {
        isFetching = false;
    });
}

/**
 * Appends movie cards to the DOM, creating HTML elements based on the movie data.
 *
 * @param {Array} movies - An array of movie objects to append to the DOM.
 */
function appendMoviesToDOM(movies) {
    const movieContainer = document.querySelector(".row.mt-4");
    if (!movieContainer) return;

    const movieRow = document.createElement("div");
    movieRow.className = "row g-4";

    movies.forEach(movie => {
        const isFavorite = movie.is_favorite;
        const movieCard = document.createElement("div");
        movieCard.className = "col-12 col-md-4 col-lg-3 card-deck d-flex";

    // Reinitialize favorite buttons for dynamically loaded movies
    initializeFavoriteButtons();

        movieCard.innerHTML = `
            <div class="card mb-4 shadow-sm" style="height: 100%;">
                <img src="${movie.poster_path ? `https://image.tmdb.org/t/p/w500/${movie.poster_path}` : '/static/images/movie-card-placeholder-img.png'}"
                    class="card-img-top" alt="${movie.title}" style="object-fit: cover; height: 300px;">
                <div class="card-body d-flex flex-column justify-content-between">
                    <h5 class="card-title">${movie.title}</h5>
                    <p class="card-text">${movie.overview.split(" ").slice(0, 20).join(" ")}...</p>
                    <div class="btn-wrapper text-center d-flex justify-content-between">
                        <a href="/movies/${movie.id}/" class="btn btn-dark card-link">Show More</a>
                        <button class="btn ${isFavorite ? 'btn-danger' : 'btn-outline-danger'} card-link favorite-btn btn-sm" 
                                data-movie-id="${movie.id}" data-title="${movie.title}" 
                                data-posterpath="${movie.poster_path || ''}" 
                                data-releasedate="${movie.release_date || ''}" 
                                data-rating="${movie.vote_average || '0'}"
                                data-is-favorite="${isFavorite}">
                            <i class="fa ${isFavorite ? 'fa-solid' : 'fa-regular'} fa-heart"></i> 
                            ${isFavorite ? "Remove" : "Add to Favs"}
                        </button>
                    </div>
                </div>
            </div>
        `;

        movieRow.appendChild(movieCard);
    });

    movieContainer.appendChild(movieRow);
    initializeFavoriteButtons();
}

/**
 * Sets up infinite scrolling by adding a debounced scroll event listener.
 * Loads the first page of movies immediately.
 */
function setupInfiniteScroll() {

    window.addEventListener("scroll", debounce(() => {
        const scrollThreshold = document.body.offsetHeight - 200;
        const scrollPosition = window.innerHeight + window.scrollY;

        if (scrollPosition >= scrollThreshold && currentPage < totalPages && !isFetching) {
            loadMoreMovies();
        }
    }, 250));
    loadMoreMovies();
}

/**
 * Retrieves the value of a cookie by name.
 */
function getCookie(name) {
    return document.cookie.split("; ").reduce((cookieValue, cookie) => {
        if (cookie.startsWith(name + "=")) return decodeURIComponent(cookie.split("=")[1]);
        return cookieValue;
    }, null);
}


/**
 * Initializes various functionalities after the DOM content is fully loaded.
 */
document.addEventListener("DOMContentLoaded", function () {
    initializeBackToTopButton();
    initializeMovieDetails();
    initializeReviewForm();
    setupInfiniteScroll();
    initializeFavoriteButtons();
    fetch("/movies/get_favorite_movies/")
    .then(response => response.json())
    .then(data => {

        document.querySelectorAll(".favorite-btn").forEach(button => {
            const movieId = parseInt(button.dataset.movieId);
            
            if (isNaN(movieId)) {
                console.error("Invalid movie ID:", button);
                return;
            }

            const isFavorite = data.favorite_movie_ids.includes(movieId);
            
            updateFavoriteButtonUI(button, isFavorite);
            
            // Ensure data-is-favorite attribute is updated
            button.dataset.isFavorite = isFavorite.toString();
        });
    })
    .catch(error => console.error("Error fetching favorites:", error));
});