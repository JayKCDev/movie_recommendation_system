from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models.popularity import get_popular_movies, get_popularity_stats
from utils.data_loader import data_loader

# Create FastAPI app instance
app = FastAPI(
    title="Movie Recommender API",
    description="Movie recommendation system with popularity-based and content-based filtering",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load data at startup
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("Starting Movie Recommender API...")
    data_loader.load_data()
    print("API ready! 🚀")
    print("=" * 50)


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Movie Recommender API is running",
        "version": "1.0.0",
        "endpoints": {
            "popular": "/api/popular",
            "stats": "/api/stats"
        }
    }


# API 1: Get popular movies
@app.get("/api/popular")
async def get_popular(
        limit: int = Query(10, ge=1, le=100,
                           description="Number of movies to return"),
        percentile: float = Query(0.9, ge=0.5, le=0.99,
                                  description="Vote count percentile threshold")
):
    """
    Get popular movies based on IMDB weighted rating formula

    - **limit**: Number of movies to return (1-100)
    - **percentile**: Minimum vote count percentile (0.5-0.99)
    """
    try:
        popular_movies = get_popular_movies(n=limit,
                                            min_vote_percentile=percentile)

        return {
            "success": True,
            "count": len(popular_movies),
            "movies": popular_movies
        }
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error fetching popular movies: {str(e)}")


# Get popularity calculation stats
@app.get("/api/stats")
async def get_stats():
    """
    Get statistics about the movie database and popularity calculation
    """
    try:
        stats = get_popularity_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error fetching stats: {str(e)}")

# API 2: Content-based recommendation (placeholder - we'll implement next)
# @app.post("/api/recommend")
# async def recommend_movies(request: RecommendationRequest):
#     """Get content-based recommendations for a given movie"""
#     pass