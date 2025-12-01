from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from models.popularity import get_popular_movies, get_popularity_stats
from models.content_based_recommendation import get_similar_movies, search_movies, \
    initialize_content_model
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

    # Initialize content-based model (precompute similarity matrix)
    initialize_content_model()

    print("API ready! 🚀")
    print("=" * 50)


# Pydantic models for request/response
class RecommendationRequest(BaseModel):
    movie_title: str
    num_recommendations: int = 10


class MovieSearchQuery(BaseModel):
    query: str
    limit: int = 10


@app.get("/")
async def root():
    return {
        "message": "Movie Recommender API is running",
        "version": "1.0.0",
        "endpoints": {
            "popular": "/api/popular",
            "similar": "/api/similar_movies",
            "search": "/api/search",
            "stats": "/api/stats"
        }
    }

# API 1: Get popular movies
@app.get("/api/popular")
async def get_popular(
        limit: int = Query(10, ge=1, le=20,
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


# Pydantic model for request body
class RecommendationRequest(BaseModel):
    movie_title: str
    num_recommendations: int = 10


# API 2: Content-based recommendation
@app.post("/api/similar/movies")
async def similar_movies(request: RecommendationRequest):
    """
    Get content-based movie recommendations

    - **movie_title**: Title of the movie (case-insensitive, partial match supported)
    - **num_recommendations**: Number of recommendations to return (1-50)
    """
    # Validate num_recommendations
    if request.num_recommendations < 1 or request.num_recommendations > 50:
        raise HTTPException(
            status_code=400,
            detail="num_recommendations must be between 1 and 50"
        )

    try:
        result = get_similar_movies(
            movie_title=request.movie_title,
            num_recommendations=request.num_recommendations
        )

        return {
            "success": True,
            "query": request.movie_title,
            "matched_movie": result["query_movie"],
            "count": len(result["recommendations"]),
            "recommendations": result["recommendations"]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error fetching similar movies: {str(e)}")


# API 3: Search movies (for autocomplete)
@app.get("/api/search")
async def search_movies_endpoint(
        query: str = Query(..., min_length=1, description="Search query"),
        limit: int = Query(10, ge=1, le=50, description="Maximum results")
):
    """
    Search for movies by title (for autocomplete/search functionality)

    - **query**: Search string (case-insensitive)
    - **limit**: Maximum number of results (1-50)
    """
    try:
        results = search_movies(query=query, limit=limit)

        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error searching movies: {str(e)}")