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