document.addEventListener("DOMContentLoaded", function () {
    // Function to attach favorite button event listeners
    function attachFavoriteButtonListeners() {
        document.querySelectorAll(".favorite-btn").forEach(button => {
            button.removeEventListener("click", toggleFavorite); // Remove existing listeners to prevent duplicates
            button.addEventListener("click", toggleFavorite);
        });
    }

    // Function to handle favorite button click
    function toggleFavorite() {
        let movieId = this.dataset.movieId;
        let title = this.dataset.title;
        let posterPath = this.dataset.posterPath;
        let releaseDate = this.dataset.releaseDate;
        let rating = this.dataset.rating;

        fetch("/movies/toggle_favorite/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `movie_id=${movieId}&title=${title}&poster_path=${posterPath}&release_date=${releaseDate}&rating=${rating}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "added") {
                    this.textContent = "💔 Remove from Favorites";
                } else if (data.status === "removed") {
                    this.textContent = "❤️ Add to Favorites";
                }
            })
            .catch(error => console.error("Error:", error));
    }

    // Initial event listener setup
    attachFavoriteButtonListeners();

    // CSRF token helper function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Infinite Scroll
    let currentPage = 1;
    let totalPages = Infinity; // Initially large to allow scrolling

    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 50 && currentPage < totalPages) {
            loadMoreMovies();
        }
    });

    function loadMoreMovies() {
        let sortBy = document.getElementById("sort_by").value;

        fetch(`/movies/?sort_by=${sortBy}&page=${currentPage + 1}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then(response => response.json())
            .then(data => {
                if (data.movies.length > 0) {
                    let movieContainer = document.querySelector(".row.mt-4");
                    let movieRow = document.createElement("div");
                    movieRow.className = "row g-4"; // Adds spacing between rows

                    data.movies.forEach(movie => {
                        let movieCard = document.createElement("div");
                        movieCard.className = "col-12 col-md-4 col-lg-3 card-deck d-flex";
                        movieCard.innerHTML = `
        <div class="card mb-4 shadow-sm" style="height: 100%;">
            <img src="${movie.poster_path ? `https://image.tmdb.org/t/p/w500/${movie.poster_path}` : '/static/images/movie-card-placeholder-img.png'}" class="card-img-top" alt="${movie.title}" style="object-fit: cover; height: 300px;">
            <div class="card-body d-flex flex-column justify-content-between">
                <h5 class="card-title">${movie.title}</h5>
                <p class="card-text" style="flex-grow: 1;">${movie.overview.split(" ").slice(0, 20).join(" ")}...</p>
                <div class="btn-wrapper text-center d-flex justify-content-between">
                    <a href="/movies/${movie.id}/" class="btn btn-dark card-link">Show More</a>
                    <button class="btn btn-outline-danger card-link favorite-btn" data-movie-id="${movie.id}" data-title="${movie.title}" data-poster="${movie.poster_path}" data-release="${movie.release_date}" data-rating="${movie.vote_average}">
                        <i class="fa fa-heart"></i> Add to List
                    </button>
                </div>
            </div>
        </div>`;
                        movieRow.appendChild(movieCard);
                    });

                    movieContainer.appendChild(movieRow);


                    currentPage++;
                    totalPages = data.total_pages;

                    // Reapply event listeners to new buttons
                    attachFavoriteEventListeners();
                }
            })
            .catch(error => console.error("Error fetching movies:", error));
    }

    // Function to reapply event listeners
    function attachFavoriteEventListeners() {
        document.querySelectorAll(".favorite-btn").forEach(button => {
            button.addEventListener("click", function () {
                let movieId = this.dataset.movieId;
                let title = this.dataset.title;
                let posterPath = this.dataset.poster;
                let releaseDate = this.dataset.release;
                let rating = this.dataset.rating;

                fetch("/movies/toggle_favorite/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: `movie_id=${movieId}&title=${title}&poster_path=${posterPath}&release_date=${releaseDate}&rating=${rating}`
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === "added") {
                            this.innerHTML = `<i class="fa fa-heart"></i> Remove from List`;
                        } else if (data.status === "removed") {
                            this.innerHTML = `<i class="fa fa-heart"></i> Add to List`;
                        }
                    })
                    .catch(error => console.error("Error:", error));
            });
        });
    }
});
