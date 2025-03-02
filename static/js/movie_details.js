document.addEventListener("DOMContentLoaded", function () {
    const movieId = new URLSearchParams(window.location.search).get("id");
    if (!movieId) {
        console.error("Movie ID not found in URL");
        return;
    }

    fetchMovieDetails(movieId);
});

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
            displayVideos(data.videos);
            displayReviews(data.reviews);
            displaySimilarMovies(data.similar_movies);
        })
        .catch(error => console.error("Error fetching movie details:", error));
}

function displayWatchProviders(providers) {
    const container = document.getElementById("watch-providers");
    container.innerHTML = providers.length ? providers.map(p => `<li>${p.provider_name}</li>`).join('') : "<p>No providers available.</p>";
}

function displayVideos(videos) {
    const container = document.getElementById("videos");
    container.innerHTML = videos.length ? videos.map(v => `<iframe width="250" height="150" src="https://www.youtube.com/embed/${v.key}" frameborder="0" allowfullscreen></iframe>`).join('') : "<p>No videos available.</p>";
}

function displayReviews(reviews) {
    const container = document.getElementById("reviews");
    container.innerHTML = reviews.length ? reviews.map(r => `<div class='mb-3'><strong>${r.author}</strong><p>${r.content}</p></div>`).join('') : "<p>No reviews available.</p>";
}

function displaySimilarMovies(movies) {
    const container = document.getElementById("similar-movies");
    container.innerHTML = movies.length ? movies.map(m => `<div class="card" style="width: 10rem;"><img class="card-img-top" src="https://image.tmdb.org/t/p/w200/${m.poster_path}" alt="${m.title}"><div class="card-body"><p class="card-text">${m.title}</p></div></div>`).join('') : "<p>No similar movies found.</p>";
}
