/**
 * Event listener for removing a movie from favorites.
 * Listens for clicks on elements with the class "remove-favorite-btn"
 * and sends an AJAX request to remove the selected movie.
 */
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-favorite-btn")) {
        console.log("Remove button clicked"); // Debugging

        const movieId = event.target.dataset.movieId;
        console.log("Movie ID:", movieId); // Debugging

        fetch(`/movies/remove_favorite/${movieId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response from server:", data); // Debugging
            if (data.status === "removed") {
                event.target.closest(".col-12").remove(); // Remove the movie card from UI
            }
        })
        .catch(error => console.error("Error removing favorite:", error));
    }
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
