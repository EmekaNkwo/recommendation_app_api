# Movie Recommendation System API

=====================================

## Table of Contents

1. [Overview](#overview)
2. [Endpoints](#endpoints)
3. [Usage](#usage)
4. [Recommendation System](#recommendation-system)

## Overview

This API provides a movie recommendation system that suggests movies based on their similarity. The system uses a TF-IDF vectorizer to calculate the similarity between movie descriptions.

## Endpoints

### 1. Get All Movies

- **URL:** `/api/movies`
- **Method:** `GET`
- **Response:** A JSON object containing an array of all movie titles.

### 2. Get Random Movies

- **URL:** `/api/random`
- **Method:** `GET`
- **Response:** A JSON object containing an array of 10 random movie titles.

### 3. Get Similar Movies

- **URL:** `/api/similarity/<name>`
- **Method:** `GET`
- **Response:** A JSON object containing an array of movie titles similar to the input movie.

### 4. Serve

- **URL:** `/`
- **Method:** `GET`
- **Response:** A welcome message.

## Usage

To use the API, simply send a GET request to the desired endpoint. For example, to get all movies, send a GET request to `/api/movies`.

## Recommendation System

The recommendation system uses a TF-IDF vectorizer to calculate the similarity between movie descriptions. The system is trained on a dataset of movie descriptions, and can recommend movies based on their similarity to a given input movie.

The system consists of the following components:

- **Data Loader:** Loads the movie dataset into memory.
- **TF-IDF Vectorizer:** Calculates the TF-IDF vectors for each movie description.
- **Similarity Calculator:** Calculates the similarity between movie descriptions using the TF-IDF vectors.
- **Recommendation Generator:** Generates a list of recommended movies based on the similarity scores.

The system is implemented using the following algorithms:

- **TF-IDF Vectorizer:** Uses the scikit-learn library to calculate the TF-IDF vectors.
- **Similarity Calculator:** Uses the cosine similarity metric to calculate the similarity between movie descriptions.
- **Recommendation Generator:** Uses a simple ranking algorithm to generate the list of recommended movies.
