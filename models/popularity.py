import pandas as pd
from utils.data_loader import data_loader


def weighted_rating(df, m, C):
    """
    Calculate IMDB weighted rating formula
    WR = (v/(v+m)) * R + (m/(v+m)) * C

    Args:
        df: DataFrame row with vote_average and vote_count
        m: Minimum votes required
        C: Mean vote average across all movies

    Returns:
        Weighted rating score
    """
    R = df["vote_average"]
    v = df["vote_count"]
    wr = (v / (v + m)) * R + (m / (v + m)) * C
    return wr


def get_popular_movies(n=10, min_vote_percentile=0.9):
    """
    Get top N popular movies based on weighted rating

    Args:
        n: Number of movies to return
        min_vote_percentile: Percentile threshold for vote_count filter (0.9 = top 10%)

    Returns:
        List of dictionaries with movie details
    """
    movies = data_loader.movies.copy()

    # Calculate threshold values
    m = movies["vote_count"].quantile(min_vote_percentile)
    C = movies["vote_average"].mean()

    # Filter movies with sufficient votes
    movies_filtered = movies.loc[movies["vote_count"] >= m].copy()

    # Calculate weighted rating
    movies_filtered["weighted_rating"] = movies_filtered.apply(
        lambda x: weighted_rating(x, m, C),
        axis=1
    )

    # Sort by weighted rating and get top N
    top_movies = movies_filtered.sort_values(
        "weighted_rating",
        ascending=False
    ).head(n)

    # Format response
    result = []
    for _, movie in top_movies.iterrows():
        result.append({
            "id": int(movie["id"]),
            "title": movie["title"],
            "weighted_rating": round(float(movie["weighted_rating"]), 2),
            "vote_average": float(movie["vote_average"]),
            "vote_count": int(movie["vote_count"]),
            "release_date": movie["release_date"],
            "overview": movie["overview"]
        })

    return result


def get_popularity_stats():
    """
    Get statistics about the popularity calculation

    Returns:
        Dictionary with stats
    """
    movies = data_loader.movies

    m = movies["vote_count"].quantile(0.9)
    C = movies["vote_average"].mean()
    qualified_count = len(movies[movies["vote_count"] >= m])

    return {
        "total_movies": len(movies),
        "qualified_movies": qualified_count,
        "min_vote_threshold": round(m, 2),
        "mean_vote_average": round(C, 2)
    }