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
