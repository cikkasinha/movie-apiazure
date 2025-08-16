markdown
# 🎬 Movie Recommendation API

A Flask-based web API that provides movie recommendations using data from [The Movie Database (TMDb)](https://www.themoviedb.org/). It supports genre-based browsing, AI-powered recommendations, and caching for performance.

---

## 🚀 Features

- 🔍 **Search-based Recommendations**: Get similar movies based on a title.
- 🎭 **Genre Explorer**: Browse movies by genre.
- ⚡ **Caching**: Speeds up repeated requests using Flask-Caching.
- 🌐 **Static Frontend**: Serves a simple HTML interface from the `/static` folder.

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Flask**
- **Flask-Caching**
- **TMDb API**
- **Requests**

---

## 📦 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/<your-username>/movie-api.git
   cd movie-api
Create a virtual environment

bash
python -m venv movie_api_env
.\movie_api_env\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set your TMDb API key Replace "TMDB_API_KEY" in recommendation.py with your actual API key.

1.Create a TMDb account at themoviedb.org

2.Log in and go to your account settings.

3.Navigate to the API section.

4.Fill out a brief form describing your intended use.

5.Agree to the terms and generate your key.

Once you have it, replace "TMDB_API_KEY" in your code with the actual key string.

🧪 Running the App
bash
python MovieAPI.py
Visit http://localhost:5000 in your browser.

📁 API Endpoints
Endpoint	Method	Description
/	GET	Serves the static homepage
/recommend-ai	GET	Returns recommended movies for a title
/genres	GET	Lists available movie genres
/movies-by-genre	GET	Returns movies for a given genre ID
🧼 To Do
[ ] Add unit tests

[ ] Improve error handling

[ ] Add support for multiple regions

[ ] Dockerize the app

📜 License
MIT License. See LICENSE for details.


---

Let me know if you'd like to include screenshots, deployment instructions, or a sample response from the API. I can also help you write a `LICENSE` file or a `.env` setup for your API key.
