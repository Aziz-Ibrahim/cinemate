/**
 * Event listener for removing a movie from favorites.
 * Listens for clicks on elements with the class "remove-favorite-btn"
 * and sends an AJAX request to remove the selected movie.
 */
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-favorite-btn").forEach(button => {
        button.addEventListener("click", function () {
            const movieId = this.dataset.movieId;
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            if (confirm("Are you sure you want to remove this movie from favorites?")) {
                fetch(`/users/remove_favorite/${movieId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/json"
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "removed") {
                        this.closest(".col-12").remove(); // Remove the movie card from the UI
                        updateNoFavoritesMessage(); // Update the message if no favorites are left
                    } else {
                        alert("Failed to remove the movie. Please try again.");
                    }
                })
                .catch(error => console.error("Error removing favorite:", error));
            }
        });
    });
});

/**
 * Updates the "No favorite movies yet" message if there are no movies left.
 */
function updateNoFavoritesMessage() {
    const favoriteMoviesContainer = document.getElementById("user-favorites").querySelector(".row");
    if (!favoriteMoviesContainer.querySelector(".col-12")) {
        favoriteMoviesContainer.innerHTML = "<p>No favorite movies yet.</p>";
    }
}

/**
 * Retrieves the CSRF token from cookies.
 * Required for making POST requests in Django.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} - The CSRF token if found, otherwise null.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Fetches and displays the user's favorite movies.
 */
function fetchFavoriteMovies() {
    fetch("/users/get_favorite_movies/") // Replace with your actual endpoint
        .then(response => response.json())
        .then(data => {
            if (data && data.movies) {
                displayFavoriteMovies(data.movies);
            } else {
                document.getElementById("favorite-movies-container").innerHTML = "<p>No favorite movies found.</p>";
            }
        })
        .catch(error => console.error("Error fetching favorite movies:", error));
}

/**
 * Displays the favorite movies in the UI.
 * @param {Array} movies - An array of movie objects.
 */
function displayFavoriteMovies(movies) {
    const container = document.getElementById("favorite-movies-container");
    container.innerHTML = ""; // Clear existing content

    movies.forEach(movie => {
        const movieCard = document.createElement("div");
        movieCard.className = "col-12 mb-4"; // Bootstrap column class
        movieCard.innerHTML = `
            <div class="card">
                <div class="row no-gutters">
                    <div class="col-md-4">
                        <img src="https://image.tmdb.org/t/p/w500/${movie.poster_path}" class="card-img" alt="${movie.title}">
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                            <h5 class="card-title">${movie.title}</h5>
                            <p class="card-text">Release Date: ${movie.release_date}</p>
                            <p class="card-text">Rating: ${movie.rating}</p>
                            <button class="btn btn-danger remove-favorite-btn" data-movie-id="${movie.movie_id}">Remove from Favorites</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(movieCard);
    });
}