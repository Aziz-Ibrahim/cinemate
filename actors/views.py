import requests
from django.shortcuts import render
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY


def actor_detail(request, actor_id):
    """Fetches and displays details for a specific actor."""
    actor_url = (
        f"https://api.themoviedb.org/3/person/{actor_id}"
        f"?api_key={TMDB_API_KEY}"
        f"&append_to_response=movie_credits,external_ids"
    )
    response = requests.get(actor_url)

    if response.status_code != 200:
        return render(
            request, "actors/actor_not_found.html", {"actor_id": actor_id}
        )

    actor = response.json()

    similar_actors = get_similar_actors_by_genre(
        actor.get("movie_credits", {})
    )

    # Extract social media links
    external_ids = actor.get('external_ids', {})
    social_links = {
        "imdb": f"https://www.imdb.com/name/{external_ids.get('imdb_id')}"
        if external_ids.get('imdb_id') else None,
        "twitter": f"https://twitter.com/{external_ids.get('twitter_id')}"
        if external_ids.get('twitter_id') else None,
        "instagram": (
            f"https://instagram.com/{external_ids.get('instagram_id')}"
            if external_ids.get('instagram_id') else None
        ),
        "facebook": f"https://facebook.com/{external_ids.get('facebook_id')}"
        if external_ids.get('facebook_id') else None,
    }

    return render(
        request,
        "actors/actor_detail.html",
        {
            "actor": actor,
            "movies": actor.get("movie_credits", {}).get("cast", []),
            "social_links": social_links,
            "similar_actors": similar_actors,
        },
    )


def get_similar_actors_by_genre(movie_credits):
    """Fetches actors based on shared movie genres."""
    genre_count = {}

    for movie in movie_credits.get("cast", []):
        for genre in movie.get("genre_ids", []):
            genre_count[genre] = genre_count.get(genre, 0) + 1

    # Get the top 2 genres
    top_genres = sorted(genre_count, key=genre_count.get, reverse=True)[:2]

    if not top_genres:
        return []

    genre_query = "|".join(map(str, top_genres))  # Format for API query
    url = (
        f"https://api.themoviedb.org/3/discover/movie?"
        f"api_key={TMDB_API_KEY}&with_genres={genre_query}"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return []

    movies = response.json().get("results", [])

    # Extract unique actors from those movies
    similar_actors = []
    seen_actor_ids = set()

    for movie in movies[:5]:  # Limit the number of movies checked
        movie_details_url = (
            f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?"
            f"api_key={TMDB_API_KEY}"
        )
        movie_response = requests.get(movie_details_url)

        if movie_response.status_code == 200:
            # Limit actors per movie
            cast = movie_response.json().get("cast", [])[:5]
            for actor in cast:
                if actor["id"] not in seen_actor_ids:
                    similar_actors.append(
                        {
                            "id": actor["id"],
                            "name": actor["name"],
                            "profile_path": actor.get("profile_path"),
                        }
                    )
                    seen_actor_ids.add(actor["id"])

    return similar_actors[:10]  # Limit results
