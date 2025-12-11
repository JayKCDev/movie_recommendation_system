# Algorithm Overview:
# 1. Feature Extraction: Combines movie overview, keywords, genres, and title into a weighted text representation
# 2. Vectorization: Uses TF-IDF to convert text content into numerical vectors
# 3. Similarity Calculation: Computes cosine similarity between all movie pairs
# 4. Recommendation: Returns movies with highest similarity scores
#
# Key Features:
# - Uses weighted concatenation to prioritize certain features (keywords, genres)
# - Supports exact and partial movie title matching
# - Returns similarity scores for observation/transparency and accuracy check

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.data_loader import data_loader

# Global variables - only store the vectorizer and matrix (not full similarity matrix)
_tfidf_vectorizer = None
_tfidf_matrix = None


def initialize_content_model():
    """
    Initialize TF-IDF model (without pre-computing similarity matrix)
    """
    global _tfidf_vectorizer, _tfidf_matrix

    if _tfidf_matrix is not None:
        return  # Already initialized

    print("Initializing content-based recommendation model")

    movies = data_loader.movies.copy()

    # Create TF-IDF vectorizer with English stop words removed
    # Stop words (the, a, an, etc.) are filtered to focus on meaningful content
    _tfidf_vectorizer = TfidfVectorizer(
        stop_words="english",
        # max_features=5000,  # Reduced from 10000 to save more memory
        # max_df=0.8,         # Ignore terms that appear in >80% of documents
        # min_df=2            # Ignore terms that appear in <2 documents
    )

    # Weighted concatenation (same as before)
    content = (
        (movies["overview"].fillna("") + " ") * 2 +  # Reduced weight
        (movies["keywords"].fillna("") + " ") * 2 +
        (movies["genres"].fillna("") + " ") * 2 +
        (movies["title"].fillna(""))
    )

    # Only store TF-IDF matrix, NOT similarity matrix
    _tfidf_matrix = _tfidf_vectorizer.fit_transform(content)

    print(f"✓ Content model initialized with {len(movies)} movies")
    print(f"✓ TF-IDF matrix shape: {_tfidf_matrix.shape}")


def get_similar_movies(movie_title, num_recommendations=5):
    """
    Get similar movies by computing similarities on-demand
    """
    if _tfidf_matrix is None:
        initialize_content_model()

    movies = data_loader.movies

    # Find the movie
    movie_matches = movies[movies["title"].str.lower() == movie_title.lower()]

    if movie_matches.empty:
        movie_matches = movies[
            movies["title"].str.contains(movie_title, case=False, na=False)
        ]
        if movie_matches.empty:
            raise ValueError(f"Movie '{movie_title}' not found in dataset")

    movie_index = movie_matches.index[0]
    actual_title = movie_matches.iloc[0]["title"]

    movie_vector = _tfidf_matrix[movie_index]
    similarities = cosine_similarity(movie_vector, _tfidf_matrix).flatten()

    # Get top N similar movies (same logic as before)
    scores = list(enumerate(similarities))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    similar_movie_indices = [score_tuple[0] for score_tuple in
                             scores[1:num_recommendations + 1]]

    similar_movies = movies.loc[
        similar_movie_indices,
        ["id", "title", "overview", "release_date", "vote_average", "vote_count"]
    ]

    similarity_scores = [scores[i + 1][1] for i in range(num_recommendations)]

    # Format response
    result = []
    for idx, (_, movie) in enumerate(similar_movies.iterrows()):
        result.append({
            "id": int(movie["id"]),
            "title": movie["title"],
            "overview": movie["overview"] if pd.notna(movie["overview"]) else "",
            "release_date": movie["release_date"] if pd.notna(movie["release_date"]) else "",
            "vote_average": float(movie["vote_average"]) if pd.notna(movie["vote_average"]) else 0.0,
            "vote_count": int(movie["vote_count"]) if pd.notna(movie["vote_count"]) else 0,
            "similarity_score": round(float(similarity_scores[idx]), 4)
        })

    return {
        "query_movie": actual_title,  # Return normalized title for display
        "recommendations": result
    }


def search_movies(query, limit=10):
    """Search for movies by title"""
    movies = data_loader.movies
    matches = movies[movies["title"].str.contains(query, case=False, na=False)]
    matches = matches.head(limit)

    return [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "release_date": row["release_date"] if pd.notna(
                row["release_date"]) else ""  # Return empty string for missing dates
        }
        for _, row in matches.iterrows()
    ]