document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".favorite-btn").forEach(button => {
        button.addEventListener("click", function () {
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
        });
    });
});

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