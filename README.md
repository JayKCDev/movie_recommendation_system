---
title: MovieMind AI
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# MovieMind AI | AI Movie Recommender System

Machine learning-powered movie recommendation API using multiple algorithms.

## Features

- **Popularity-based**: Get trending movies based on vote count and ratings
- **Content-based filtering**: Find similar movies based on plot, genres, and metadata
- **Collaborative filtering**: Personalized recommendations (coming soon)

## Tech Stack

- FastAPI
- Scikit-learn
- Pandas, NumPy
- TF-IDF Vectorization
- Cosine Similarity

## API Documentation

Visit `/docs` for interactive Swagger UI documentation.

## Endpoints

### Get Popular Movies

```bash
GET /api/recommendations/popular?n=10
```

### Get Similar Movies

```bash
GET /api/recommendations/content-based?movie_title=Inception&n=10
```

## Example Usage

```bash
# Get top 10 popular movies
curl "https://jay-kc-dev-ai-movie-recommender-system.hf.space/api/recommendations/popular?n=10"

# Find movies similar to Inception
curl "https://jay-kc-dev-ai-movie-recommender-system.hf.space/api/recommendations/content-based?movie_title=Inception&n=10"
```

## Architecture

- **Backend**: FastAPI
- **ML Models**: Scikit-learn
- **Data Storage**: GitHub (CSV files loaded via github raw URLs)
- **Deployment**: HuggingFace Spaces (Docker)

Built by Jay Karamchandani | [LinkedIn](https://www.linkedin.com/in/jaykcdev/) | [GitHub](https://github.com/JayKCDev)
