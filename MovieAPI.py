from flask import Flask, jsonify, request, send_from_directory
from cache_config import cache
from recommendation import get_movie_recommendations, get_genres, get_movies_by_genre
from routes_chat import register_chat_routes
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
cache.init_app(app)

register_chat_routes(app)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/recommend-ai', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def recommend():
    movie_title = (request.args.get("title") or "").strip()
    if not movie_title:
        return jsonify({"error": "title parameter missing"}), 400
    recommendations = get_movie_recommendations(movie_title)
    return jsonify({"input_movie": movie_title, "recommended_movies": recommendations})

@app.route('/genres', methods=['GET'])
def genres():
    genres_list = get_genres()
    return jsonify({"genres": genres_list})

@app.route('/movies-by-genre', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def movies_by_genre():
    genre_id = (request.args.get("genre_id") or "").strip()
    if not genre_id:
        return jsonify({"error": "genre_id parameter missing"}), 400
    try:
        genre_id = int(genre_id)
    except ValueError:
        return jsonify({"error": "genre_id must be an integer"}), 400
    movies = get_movies_by_genre(genre_id)
    return jsonify({"genre_id": genre_id, "movies": movies})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
