import requests
from cache_config import cache

TMDB_API_KEY = "e4b6991b8c2421b74595cb1d30f34061"  # Replace with your actual TMDb API key

@cache.memoize(timeout=600)
def get_genres():
    """
    Retrieve the list of movie genres from TMDb.
    This result is cached for 10 minutes.
    """
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(genre_url).json()
    genres = response.get("genres", [])
    return genres

@cache.memoize(timeout=300)
def get_movies_by_genre(genre_id):
    """
    Use the Discover endpoint to fetch movies by a given genre.
    This result is cached for 5 minutes.
    """
    discover_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
    discover_response = requests.get(discover_url).json()

    image_base_url = "https://image.tmdb.org/t/p/w500"
    movies = []
    for movie in discover_response.get("results", [])[:25]:
        title = movie.get("title", "N/A")
        poster_path = movie.get("poster_path")
        poster_url = image_base_url + poster_path if poster_path else None
        movie_id = movie.get("id")

        # Get OTT info for "IN" region (you can change as needed).
        ott_info = None
        if movie_id:
            provider_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
            provider_response = requests.get(provider_url).json()
            if provider_response.get("results", {}).get("IN"):
                ott_info = provider_response["results"]["IN"]

        # Fetch extra details (like rating, credits for actors & director).
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
        details_response = requests.get(details_url).json()
        rating = details_response.get("vote_average", "N/A")
        credits = details_response.get("credits", {})
        cast = credits.get("cast", [])
        actors = [member.get("name") for member in cast[:3]] if cast else []
        crew = credits.get("crew", [])
        director = next((member.get("name") for member in crew if member.get("job") == "Director"), None)

        movies.append({
            "title": title,
            "poster": poster_url,
            "ott_info": ott_info,
            "rating": rating,
            "actors": actors,
            "director": director
        })
    return movies

def get_movie_recommendations(movie_title):
    """
    Searches for the given movie title and then fetches up to 25 recommended movies.
    For each movie, it retrieves details (rating, credits) and OTT provider info.
    """
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(search_url).json()
    
    if response.get("results"):
        base_movie_id = response["results"][0]["id"]
        rec_url = f"https://api.themoviedb.org/3/movie/{base_movie_id}/recommendations?api_key={TMDB_API_KEY}"
        rec_response = requests.get(rec_url).json()

        image_base_url = "https://image.tmdb.org/t/p/w500"
        recommendations = []
        for movie in rec_response.get("results", [])[:25]:
            title = movie.get("title", "N/A")
            poster_path = movie.get("poster_path")
            poster_url = image_base_url + poster_path if poster_path else None
            movie_id = movie.get("id")

            # Get OTT info for "IN" region
            ott_info = None
            if movie_id:
                provider_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
                provider_response = requests.get(provider_url).json()
                if provider_response.get("results", {}).get("IN"):
                    ott_info = provider_response["results"]["IN"]

            # Extra details: rating and credits
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
            details_response = requests.get(details_url).json()
            rating = details_response.get("vote_average", "N/A")
            credits = details_response.get("credits", {})
            cast = credits.get("cast", [])
            actors = [member.get("name") for member in cast[:3]] if cast else []
            crew = credits.get("crew", [])
            director = next((member.get("name") for member in crew if member.get("job") == "Director"), None)

            recommendations.append({
                "title": title,
                "poster": poster_url,
                "ott_info": ott_info,
                "rating": rating,
                "actors": actors,
                "director": director
            })
        return recommendations if recommendations else ["No recommendations found."]
    return ["Movie not found."]
