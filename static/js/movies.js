document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    const movieIdMatch = path.match(/\/movies\/(\d+)\//);

    if (movieIdMatch && movieIdMatch[1]) {
        const movieId = movieIdMatch[1];

        // Fetch movie details from your Django API
        fetch(`/movie_detail_api/${movieId}/`)
            .then(response => response.json())
            .then(data => {
                // Display movie details on the page
                console.log(data); // Log the movie data
                // Update the DOM with the movie details
                document.getElementById("movie-title").textContent = data.title;
                document.getElementById("movie-overview").textContent = data.overview;
                document.getElementById("movie-rating").textContent = data.vote_average;
                document.getElementById("movie-poster").src = `https://image.tmdb.org/t/p/w500/${data.poster_path}`;

            })
            .catch(error => {
                console.error("Error fetching movie details:", error);
            });
    } else {
        console.error("Movie ID not found in URL");
    }


    function attachFavoriteButtonListeners() {
        document.querySelectorAll(".favorite-btn").forEach(button => {
            button.removeEventListener("click", toggleFavorite);
            button.addEventListener("click", toggleFavorite);
        });
    }

    function toggleFavorite() {
        let movieId = this.dataset.movieId;
        let title = this.dataset.title;
        let posterPath = this.dataset.posterpath;  // Fixed dataset case
        let releaseDate = this.dataset.releasedate;  // Fixed dataset case
        let rating = this.dataset.rating;

        console.log("Movie ID sent:", movieId);  // Debugging log
        console.log("Title:", title);
        console.log("Poster Path:", posterPath);
        console.log("Release Date:", releaseDate);
        console.log("Rating:", rating);

        const formData = new URLSearchParams();
        formData.append("movie_id", movieId);
        formData.append("title", title || "");
        formData.append("poster_path", posterPath || "");
        formData.append("release_date", releaseDate || "");
        formData.append("rating", rating || "0");

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
            if (data.status === "added") {
                this.innerHTML = '<i class="fa fa-heart"></i> Remove from List';
            } else if (data.status === "removed") {
                this.innerHTML = '<i class="fa fa-heart"></i> Add to List';
            }
        })
        .catch(error => console.error("Error:", error));
    }

    attachFavoriteButtonListeners();



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

    let currentPage = 1;
    let totalPages = Infinity;

    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 50 && currentPage < totalPages) {
            loadMoreMovies();
        }
    });

    function loadMoreMovies() {
        let sortBySelect = document.getElementById("sort_by");
        if (!sortBySelect) {
            console.error("Sort by select element not found.");
            return;
        }

        let sortBy = sortBySelect.value;

        fetch(`/movies/?sort_by=${sortBy}&page=${currentPage + 1}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.movies.length > 0) {
                let movieContainer = document.querySelector(".row.mt-4");
                let movieRow = document.createElement("div");
                movieRow.className = "row g-4";

                data.movies.forEach(movie => {
                    let movieCard = document.createElement("div");
                    movieCard.className = "col-12 col-md-4 col-lg-3 card-deck d-flex";
                    movieCard.innerHTML = `
                        <div class="card mb-4 shadow-sm" style="height: 100%;">
                            <img src="${movie.poster_path ? `https://image.tmdb.org/t/p/w500/${movie.poster_path}` : '/static/images/movie-card-placeholder-img.png'}" class="card-img-top" alt="${movie.title}" style="object-fit: cover; height: 300px;">
                            <div class="card-body d-flex flex-column justify-content-between">
                                <h5 class="card-title">${movie.title}</h5>
                                <p class="card-text">${movie.overview.split(" ").slice(0, 20).join(" ")}...</p>
                                <div class="btn-wrapper text-center d-flex justify-content-between">
                                    <a href="/movies/${movie.id}/" class="btn btn-dark card-link">Show More</a>
                                    <button class="btn btn-outline-danger card-link favorite-btn" data-movie-id="${movie.id}" data-title="${movie.title}" data-posterpath="${movie.poster_path}" data-releasedate="${movie.release_date}" data-rating="${movie.vote_average}">
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

                attachFavoriteButtonListeners();
            }
        })
        .catch(error => console.error("Error fetching movies:", error));
    }
});
