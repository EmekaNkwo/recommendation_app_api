# Movie Recommender API

=======================

## Overview

This API provides a movie recommendation system based on cosine similarity. It uses a dataset of movies to generate recommendations for a given movie.

## Endpoints

### GET /api/movies

Returns a list of all movies in the dataset.

- Response: `{"arr": ["Movie1", "Movie2", ...]}`
- Example: `http://localhost:5000/api/movies`

### GET /api/random

Returns a list of 10 random movies from the dataset.

- Response: `{"arr": ["Movie1", "Movie2", ...]}`
- Example: `http://localhost:5000/api/random`

### GET /api/similarity/<name>

Returns a list of movie recommendations for a given movie.

- Response: `{"movies": ["Movie1", "Movie2", ...]}`
- Example: `http://localhost:5000/api/similarity/The%20Shawshank%20Redemption`

### GET /

Serves a welcome text

## Dataset

The API uses a dataset of movies stored in a CSV file named `main_data.csv`. The dataset contains the following columns:

- `movie_title`: The title of the movie.
- `comb`: A combination of the movie's title and other metadata.

## Recommendation Algorithm

The API uses a cosine similarity algorithm to generate recommendations. The algorithm works as follows:

1. Read the dataset into a pandas dataframe.
2. Create a count matrix of the movie titles using a CountVectorizer.
3. Calculate the cosine similarity between the count matrix and itself.
4. For a given movie, find the index of the movie in the dataframe.
5. Get the similarity scores for the given movie and sort them in descending order.
6. Return the top 20 movies with the highest similarity scores.

## Error Handling

The API handles 404 errors by serving a 404 message

## Running the API

To run the API, save this code in a file named `app.py` and run it using `python app.py`. The API will be available at `http://localhost:5000`.
