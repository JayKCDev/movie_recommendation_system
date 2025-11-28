import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from utils.data_loader import data_loader

# Global variables to store computed data (computed once at startup)
_tfidf_vectorizer = None
_tfidf_matrix = None
_similarity_matrix = None


def initialize_content_model():
    """
    Initialize the content-based model by computing TF-IDF and similarity matrix.
    This should be called once at startup to precompute expensive operations.
    """
    global _tfidf_vectorizer, _tfidf_matrix, _similarity_matrix

    if _similarity_matrix is not None:
        return  # Already initialized

    print("Initializing content-based recommendation model...")

    movies = data_loader.movies.copy()

    # Fill missing overviews with empty string
    movies["overview"] = movies["overview"].fillna("")

    # Create TF-IDF vectorizer
    _tfidf_vectorizer = TfidfVectorizer(stop_words="english")

    # Fit and transform movie overviews
    _tfidf_matrix = _tfidf_vectorizer.fit_transform(movies["overview"])

    # Compute similarity matrix using linear kernel (same as cosine similarity)
    _similarity_matrix = linear_kernel(_tfidf_matrix, _tfidf_matrix)

    print(f"✓ Content model initialized with {len(movies)} movies")
    print(f"✓ TF-IDF matrix shape: {_tfidf_matrix.shape}")
    print(f"✓ Similarity matrix shape: {_similarity_matrix.shape}")


def get_similar_movies(movie_title, num_recommendations=5):
    """
    Get similar movies based on content (movie overview/description)

    Args:
        movie_title: Title of the movie to find similar movies for
        num_recommendations: Number of similar movies to return

    Returns:
        List of similar movies with details
    """
    if _similarity_matrix is None:
        initialize_content_model()

    movies = data_loader.movies

    # Find the movie index
    movie_matches = movies[movies["title"].str.lower() == movie_title.lower()]

    if movie_matches.empty:
        # Try partial match
        movie_matches = movies[
            movies["title"].str.contains(movie_title, case=False, na=False)]

        if movie_matches.empty:
            raise ValueError(f"Movie '{movie_title}' not found in database")

    # Get the first match
    movie_index = movie_matches.index[0]
    actual_title = movie_matches.iloc[0]["title"]

    # Get similarity scores for this movie
    scores = list(enumerate(_similarity_matrix[movie_index]))

    # Sort by similarity score (descending)
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Get top N similar movies (excluding the movie itself at index 0)
    similar_movie_indices = [score_tuple[0] for score_tuple in
                             scores[1:num_recommendations + 1]]

    # Get movie details
    similar_movies = movies.loc[
        similar_movie_indices,
        ["id", "title", "overview", "release_date", "vote_average",
         "vote_count"]
    ]

    # Add similarity scores
    similarity_scores = [scores[i + 1][1] for i in range(num_recommendations)]

    # Format response
    result = []
    for idx, (_, movie) in enumerate(similar_movies.iterrows()):
        result.append({
            "id": int(movie["id"]),
            "title": movie["title"],
            "overview": movie["overview"] if pd.notna(
                movie["overview"]) else "",
            "release_date": movie["release_date"] if pd.notna(
                movie["release_date"]) else "",
            "vote_average": float(movie["vote_average"]) if pd.notna(
                movie["vote_average"]) else 0.0,
            "vote_count": int(movie["vote_count"]) if pd.notna(
                movie["vote_count"]) else 0,
            "similarity_score": round(float(similarity_scores[idx]), 4)
        })

    return {
        "query_movie": actual_title,
        "recommendations": result
    }


def search_movies(query, limit=10):
    """
    Search for movies by title (helper function for frontend autocomplete)

    Args:
        query: Search query string
        limit: Maximum number of results

    Returns:
        List of matching movie titles
    """
    movies = data_loader.movies

    # Case-insensitive partial match
    matches = movies[movies["title"].str.contains(query, case=False, na=False)]

    # Limit results
    matches = matches.head(limit)

    return [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "release_date": row["release_date"] if pd.notna(
                row["release_date"]) else ""
        }
        for _, row in matches.iterrows()
    ]