import pandas as pd
import random
from flask.helpers import send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify

load_dotenv()

# Use memory-efficient TfidfVectorizer and sparse matrices
class RecommendationSystem:
    def __init__(self, csv_file):
        # Initialize and load data in chunks
        self.csv_file = csv_file
        self.data = self._load_data()
        self.similarity = self._calculate_similarity()

    def _load_data(self):
        # Read the CSV file in chunks to avoid memory issues
        chunks = pd.read_csv(self.csv_file, chunksize=10000)
        data = pd.concat(chunks)
        return data

    def _calculate_similarity(self):
        # Calculate the similarity matrix using TfidfVectorizer
        tfidf = TfidfVectorizer()
        count_matrix = tfidf.fit_transform(self.data['comb'])  # Sparse matrix
        similarity = cosine_similarity(count_matrix, dense_output=False)  # Sparse similarity matrix
        return similarity

    def get_all_movies(self):
        return list(self.data['movie_title'].str.capitalize())

    def recommend(self, movie):
        movie = movie.lower()
        if movie not in self.data['movie_title'].unique():
            return 'Sorry! The movie you requested is not present in our database.'
        else:
            movie_index = self.data.loc[self.data['movie_title'] == movie].index[0]
            lst = list(enumerate(self.similarity[movie_index].toarray().flatten()))
            lst = sorted(lst, key=lambda x: x[1], reverse=True)
            lst = lst[1:20]  # Exclude the first item since it is the requested movie itself and take the top 20 movies
            movie_list = [self.data['movie_title'][i[0]] for i in lst]
            return movie_list

    def get_random_movies(self):
        random_movies = random.sample(list(self.data['movie_title']), 10)  # Select 10 random movies
        return random_movies

# Initialize recommendation system
rec_system = RecommendationSystem('main_data.csv')

app = Flask(__name__, static_folder='movie-recommender-app/build', static_url_path='/')
CORS(app)

@app.route('/api/movies', methods=['GET'])
@cross_origin()
def movies():
    # Returns all the movies in the dataset
    movies = rec_system.get_all_movies()
    result = {'arr': movies}
    return jsonify(result)

@app.route('/api/random', methods=['GET'])
@cross_origin()
def random_movies():
    movies = rec_system.get_random_movies()
    result = {'arr': movies}
    return jsonify(result)

@app.route('/')
@cross_origin()
def serve():
    return "Welcome to Recommendation App!"

@app.route('/api/similarity/<name>')
@cross_origin()
def similarity_endpoint(name):
    recommendations = rec_system.recommend(name)
    if isinstance(recommendations, str):
        # If it's an error message (string), split by '---'
        resultArray = recommendations.split('---')
    else:
        # If it's a list of movie names
        movieString = '---'.join(recommendations)
        resultArray = movieString.split('---')
    
    apiResult = {'movies': resultArray}
    return jsonify(apiResult)

@app.errorhandler(404)
def not_found(e):
    return "Sorry! Not Found. Please check your URL."

if __name__ == '__main__':
    app.run(debug=True)
