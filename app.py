import pandas as pd
import random
from flask.helpers import send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify

load_dotenv()

data = pd.read_csv('main_data.csv')
cv = CountVectorizer()
countMatrix = cv.fit_transform(data['comb'])
similarity = cosine_similarity(countMatrix)

app = Flask(__name__, static_folder='movie-recommender-app/build',
            static_url_path='/')
CORS(app)

def createSimilarity():
    
    data = pd.read_csv('main_data.csv') # reading the dataset
    cv = CountVectorizer()
    countMatrix = cv.fit_transform(data['comb'])
    similarity = cosine_similarity(countMatrix) # creating the similarity matrix
    return (data, similarity)


def getAllMovies():
    return list(data['movie_title'].str.capitalize())

def Recommend(movie):
    movie = movie.lower()
    if movie not in data['movie_title'].unique():
        return 'Sorry! The movie you requested is not present in our database.'
    else:
        movieIndex = data.loc[data['movie_title'] == movie].index[0]
        lst = list(enumerate(similarity[movieIndex]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:20]  # excluding first item since it is the requested movie itself and taking the top 20 movies
        movieList = [data['movie_title'][i[0]] for i in lst]
        return movieList

def getRandomMovies():
    random_movies = random.sample(list(data['movie_title']), 10)  # Select 10 random movies
    return random_movies


@app.route('/api/movies', methods=['GET'])
@cross_origin()
def movies():
    # returns all the movies in the dataset
    movies = getAllMovies()
    result = {'arr': movies}
    return jsonify(result)

@app.route('/api/random', methods=['GET'])
@cross_origin()
def random_movies():
    movies = getRandomMovies()
    result = {'arr': movies}
    return jsonify(result)


@app.route('/')
@cross_origin()
def serve():
    return "Welcome to Recommendation App!"


@app.route('/api/similarity/<name>')
@cross_origin()
def similarity_endpoint(name):
    recommendations = Recommend(name)
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
