from flask import Flask, jsonify, request , send_from_directory
from cache_config import cache
from recommendation import get_movie_recommendations, get_genres, get_movies_by_genre
from routes_chat import register_chat_routes  # 🔌 Add this

app = Flask(__name__, static_url_path='', static_folder='static')
cache.init_app(app)

register_chat_routes(app)  # Hook in conversational endpoints

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Cache this route for 5 minutes. Different query strings get separate cache entries.
@app.route('/recommend-ai', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def recommend():
    movie_title = request.args.get('title')
    recommendations = get_movie_recommendations(movie_title)
    return jsonify({"input_movie": movie_title, "recommended_movies": recommendations})

# Get genres (already cached at the function level using memoize).
@app.route('/genres', methods=['GET'])
def genres():
    genres_list = get_genres()
    return jsonify({"genres": genres_list})

# Get movies based on genre (cached at the function level).
@app.route('/movies-by-genre', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def movies_by_genre():
    genre_id = request.args.get('genre_id')
    if genre_id:
        movies = get_movies_by_genre(genre_id)
        return jsonify({"genre_id": genre_id, "movies": movies})
    return jsonify({"error": "genre_id parameter missing"}), 400

if __name__ == "__main__":
    app.run(debug=True)
