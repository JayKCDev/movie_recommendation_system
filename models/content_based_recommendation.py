"""
Content-Based Movie Recommendation System

This module implements a content-based filtering recommendation system using
TF-IDF (Term Frequency-Inverse Document Frequency) vectorization and cosine similarity.

Algorithm Overview:
------------------
1. Feature Extraction: Combines movie overview, keywords, genres, and title into
   a weighted text representation
2. Vectorization: Uses TF-IDF to convert text content into numerical vectors
3. Similarity Calculation: Computes cosine similarity between all movie pairs
4. Recommendation: Returns movies with highest similarity scores

Key Features:
- Pre-computes similarity matrix at startup for fast recommendations
- Uses weighted concatenation to prioritize certain features (keywords, genres)
- Supports exact and partial movie title matching
- Returns similarity scores for transparency

Performance:
- Initialization: O(n²) where n = number of movies (done once at startup)
- Recommendation: O(1) lookup from pre-computed similarity matrix
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from utils.data_loader import data_loader

# Global variables to store computed data (computed once at startup)
# These are cached to avoid recomputing expensive operations on every request
_tfidf_vectorizer = None  # TF-IDF vectorizer fitted on movie content
_tfidf_matrix = None      # TF-IDF vectorized representation of all movies
_similarity_matrix = None # Pre-computed similarity matrix (n x n) for all movies


def initialize_content_model():
    """
    Initialize the content-based model by computing TF-IDF and similarity matrix.
    This should be called once at startup to precompute expensive operations.

    Process:
    1. Combines movie features (overview, keywords, genres, title) with weights
    2. Applies TF-IDF vectorization to convert text to numerical features
    3. Computes pairwise cosine similarity for all movies
    4. Stores results in global variables for fast lookup

    Weighted Feature Strategy:
    - Overview: Weight 3x (base content)
    - Keywords: Weight 3x (high importance for matching themes)
    - Genres: Weight 3x (high importance for genre-based recommendations)
    - Title: Weight 1x (supplementary information)

    Time Complexity: O(n² * m) where n = movies, m = average features per movie
    Space Complexity: O(n²) for similarity matrix storage

    Note: This function is idempotent - calling it multiple times has no effect
    after the first successful initialization.
    """
    global _tfidf_vectorizer, _tfidf_matrix, _similarity_matrix

    if _similarity_matrix is not None:
        return  # Already initialized - skip expensive recomputation

    print("Initializing content-based recommendation model...")

    movies = data_loader.movies.copy()

    # Create TF-IDF vectorizer with English stop words removed
    # Stop words (the, a, an, etc.) are filtered to focus on meaningful content
    _tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)

    # Weighted Concatenation Strategy:
    # Combines multiple features with different weights to create a unified text representation
    # - Keywords and genres are weighted 3x to emphasize thematic similarity
    # - Overview provides detailed context (1x weight)
    # - Title helps with exact matches and series recognition (1x weight)
    # The multiplication by 3 effectively repeats the text 3 times in the concatenation,
    # giving those features more influence in the TF-IDF calculation
    content = (
            (movies["overview"].fillna("") + " ") * 3 +  # Movie description (weight: 1x)
            (movies["keywords"].fillna("") + " ") * 3 +  # Keywords (weight: 3x)
            (movies["genres"].fillna("") + " ") * 3 +  # Genres (weight: 3x)
            (movies["title"].fillna("") + " ")  # Title (weight: 1x)
    )

    # Fit and transform: Learn vocabulary from all movies, then vectorize
    # Returns a sparse matrix where each row is a movie, each column is a word/term
    # Values represent TF-IDF scores (higher = more important/unique term)
    _tfidf_matrix = _tfidf_vectorizer.fit_transform(content)

    # Compute similarity matrix using linear kernel
    # Linear kernel on normalized TF-IDF vectors = Cosine Similarity
    # Result: n x n matrix where [i, j] = similarity between movie i and movie j
    # Values range from 0 (no similarity) to 1 (identical content)
    _similarity_matrix = linear_kernel(_tfidf_matrix, _tfidf_matrix)

    print(f"✓ Content model initialized with {len(movies)} movies")
    print(f"✓ TF-IDF matrix shape: {_tfidf_matrix.shape}")
    print(f"✓ Similarity matrix shape: {_similarity_matrix.shape}")


def get_similar_movies(movie_title, num_recommendations=5):
    """
    Get similar movies based on content similarity using pre-computed similarity matrix.

    This function performs a fast O(1) lookup from the pre-computed similarity matrix
    to find movies with the highest content similarity to the query movie.

    Args:
        movie_title (str): Title of the movie to find similar movies for.
                          Supports exact and partial matching (case-insensitive).
        num_recommendations (int, optional): Number of similar movies to return.
                                            Defaults to 5. Range: 1-50.

    Returns:
        dict: Dictionary containing:
            - query_movie (str): The actual matched movie title (normalized)
            - recommendations (list): List of dictionaries, each containing:
                - id (int): Movie ID
                - title (str): Movie title
                - overview (str): Movie description
                - release_date (str): Release date
                - vote_average (float): Average user rating
                - vote_count (int): Number of votes
                - similarity_score (float): Similarity score (0-1, higher = more similar)

    Raises:
        ValueError: If the movie title is not found in the dataset (after trying
                   both exact and partial matching).

    Algorithm:
        1. Find the query movie in the dataset (exact match first, then partial)
        2. Extract similarity scores for that movie from pre-computed matrix
        3. Sort movies by similarity score (descending)
        4. Return top N movies (excluding the query movie itself)

    Time Complexity: O(n log n) for sorting, but n is typically small (< 50)
    Space Complexity: O(k) where k = num_recommendations

    Example:
        >>> result = get_similar_movies("The Dark Knight", num_recommendations=5)
        >>> print(result["query_movie"])
        "The Dark Knight"
        >>> print(len(result["recommendations"]))
        5
    """
    # Ensure model is initialized (lazy initialization if not done at startup)
    if _similarity_matrix is None:
        initialize_content_model()

    movies = data_loader.movies

    # Step 1: Find the movie in the dataset
    # Try exact match first (case-insensitive for better user experience)
    movie_matches = movies[movies["title"].str.lower() == movie_title.lower()]

    if movie_matches.empty:
        # Fallback to partial match if exact match fails
        # This handles cases like "Dark Knight" matching "The Dark Knight"
        movie_matches = movies[
            movies["title"].str.contains(movie_title, case=False, na=False)]

        if movie_matches.empty:
            raise ValueError(f"Movie '{movie_title}' not found in dataset")

    # Get the first match (in case multiple movies match, use the first one)
    # Note: movie_index is the DataFrame index, which corresponds to the row
    # position in the original  and similarity matrix
    movie_index = movie_matches.index[0]
    actual_title = movie_matches.iloc[0]["title"]

    # Step 2: Extract similarity scores for this movie
    # _similarity_matrix[movie_index] returns a 1D array of similarity scores
    # between the query movie and all other movies
    # enumerate() creates (index, score) tuples for sorting
    scores = list(enumerate(_similarity_matrix[movie_index]))

    # Step 3: Sort by similarity score (descending order)
    # Highest similarity scores first
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Step 4: Get top N similar movies
    # Skip index 0 (the movie itself, which has similarity = 1.0)
    # Take next num_recommendations movies
    similar_movie_indices = [score_tuple[0] for score_tuple in
                             scores[1:num_recommendations + 1]]

    # Step 5: Retrieve movie details for recommended movies
    similar_movies = movies.loc[
        similar_movie_indices,
        ["id", "title", "overview", "release_date", "vote_average",
         "vote_count"]
    ]

    # Extract corresponding similarity scores
    # scores[0] is the query movie itself, so we start from scores[1]
    similarity_scores = [scores[i + 1][1] for i in range(num_recommendations)]

    # Step 6: Format response with proper data types and null handling
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
            "similarity_score": round(float(similarity_scores[idx]), 4)  # Round to 4 decimal places
        })

    return {
        "query_movie": actual_title,  # Return normalized title for display
        "recommendations": result
    }


def search_movies(query, limit=10):
    """
    Search for movies by title (helper function for frontend autocomplete).

    This function provides fast text-based search for movie titles, enabling
    autocomplete functionality in the frontend. It performs case-insensitive
    partial matching on movie titles.

    Args:
        query (str): Search query string. Can be a partial title match.
                    Minimum length should be enforced by the caller.
        limit (int, optional): Maximum number of results to return.
                              Defaults to 10. Range: 1-50.

    Returns:
        list: List of dictionaries, each containing:
            - id (int): Movie ID
            - title (str): Full movie title
            - release_date (str): Release date (empty string if not available)

    Algorithm:
        1. Perform case-insensitive substring search on movie titles
        2. Filter out movies with null/NaN titles
        3. Return top N results (ordered by original  order)

    Time Complexity: O(n) where n = number of movies (linear scan)
    Space Complexity: O(k) where k = limit

    Note: This is a simple text search. For more advanced search capabilities,
          consider implementing full-text search with ranking/scoring.

    Example:
        >>> results = search_movies("dark", limit=5)
        >>> print(results[0]["title"])
        "The Dark Knight"
    """
    movies = data_loader.movies

    # Case-insensitive partial match
    # str.contains() with case=False performs case-insensitive substring matching
    # na=False ensures movies with null titles are excluded from results
    matches = movies[movies["title"].str.contains(query, case=False, na=False)]

    # Limit results to prevent returning too many matches
    # head() takes the first N results (maintains original order)
    matches = matches.head(limit)

    # Format results with proper data type handling
    return [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "release_date": row["release_date"] if pd.notna(
                row["release_date"]) else ""  # Return empty string for missing dates
        }
        for _, row in matches.iterrows()
    ]