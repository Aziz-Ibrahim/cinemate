document.addEventListener("DOMContentLoaded", function () {
    initializeMovieDetails();
    initializeReviewForm();
    setupInfiniteScroll();
});

/** Fetch and display movie details */
function initializeMovieDetails() {
    const path = window.location.pathname;
    const movieIdMatch = path.match(/\/movies\/(\d+)\//);

    if (movieIdMatch && movieIdMatch[1]) {
        const movieId = movieIdMatch[1];

        fetch(`/movie_detail_api/${movieId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("movie-title").textContent = data.title;
                document.getElementById("movie-overview").textContent = data.overview;
                document.getElementById("movie-rating").textContent = data.vote_average;
                document.getElementById("movie-poster").src = `https://image.tmdb.org/t/p/w500/${data.poster_path}`;
            })
            .catch(error => console.error("Error fetching movie details:", error));
    }
}

/** Handles review form submission */
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

/** Event delegation for favorite button clicks */
document.addEventListener("click", function (event) {
    const target = event.target.closest(".favorite-btn");
    if (!target) return; // Ignore clicks outside favorite buttons
    toggleFavorite.call(target);
});

/** Handles adding/removing favorite movies */
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
        this.innerHTML = `<i class="fa fa-heart"></i> ${data.status === "added" ? "Remove from List" : "Add to List"}`;
    })
    .catch(error => console.error("Error toggling favorite:", error));
}

/** Infinite Scroll Setup */
function setupInfiniteScroll() {
    let currentPage = 1;
    let totalPages = Infinity;

    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 50 && currentPage < totalPages) {
            loadMoreMovies(currentPage);
        }
    });

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

/** Appends new movies to the DOM */
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

/** Helper function to get CSRF token */
function getCookie(name) {
    return document.cookie.split("; ").reduce((cookieValue, cookie) => {
        if (cookie.startsWith(name + "=")) return decodeURIComponent(cookie.split("=")[1]);
        return cookieValue;
    }, null);
}
