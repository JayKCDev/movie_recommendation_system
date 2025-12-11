# MovieMind AI

A movie recommendation system built with Python, FastAPI, and machine learning libraries. This portfolio project demonstrates skills in Python, FastAPI, and AI/ML libraries including scikit-learn.

## Description

MovieMind AI is an intelligent movie recommendation system that provides personalized movie suggestions using two main approaches:

1. **Content-Based Filtering**: Uses TF-IDF vectorization and cosine similarity to recommend movies based on their content (overview, keywords, genres, and title). The system analyzes movie features to find similar films.

2. **Popularity-Based Recommendations**: Implements the IMDB weighted rating formula to identify and rank popular movies based on vote counts and ratings.

The system features a modern React frontend with a FastAPI backend, providing a seamless user experience for discovering new movies.

## Tech Stack

### Backend

- **Python 3.13**
- **FastAPI** - Modern, fast web framework for building APIs
- **scikit-learn** - Machine learning library (TF-IDF vectorization, cosine similarity)
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **uvicorn** - ASGI server for FastAPI
- **python-dotenv** - Environment variable management

### Frontend

- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests

### Deployment

- **Docker** - Containerization support
- **Vercel** - Frontend deployment configuration

## Environment Variables

### Frontend

- `VITE_API_URL` (Optional) - Backend API URL. Defaults to `http://localhost:8000` if not set.

### Backend

- `ALLOWED_ORIGINS` (Required) - Comma-separated list of allowed CORS origins. Example: `http://localhost:3000,http://localhost:5173,https://yourdomain.com`

**Setup Instructions:**

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Update the `ALLOWED_ORIGINS` variable in `.env` with your frontend URL(s).

The application loads environment variables from `.env` and optionally from `.env.local` (if present) for local overrides. Movie data is loaded from GitHub repositories at startup.

## Project Structure

```
movie_recommendation_system/
├── main.py                 # FastAPI application entry point
├── models/                 # ML recommendation models
│   ├── content_based_recommendation.py
│   ├── popularity.py
│   └── collaborative_based_filtering.py
├── utils/                  # Utility functions
│   └── data_loader.py      # Data loading and management
├── client/                 # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   └── types.ts        # TypeScript type definitions
│   └── package.json
├── data/                   # Movie datasets (CSV files)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example           # Environment variables template
└── README.md
```

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `GET /api/popular` - Get popular movies (query params: `limit`, `percentile`)
- `GET /api/stats` - Get popularity calculation statistics
- `POST /api/similar/movies` - Get content-based recommendations
- `GET /api/search` - Search movies by title (query params: `query`, `limit`)

## Features

- **Content-Based Recommendations**: Find similar movies based on content analysis
- **Popular Movies**: Discover trending and highly-rated films
- **Movie Search**: Autocomplete search functionality
- **Modern UI**: Responsive design with Tailwind CSS
- **RESTful API**: Well-documented FastAPI endpoints
- **CORS Enabled**: Cross-origin resource sharing configured

## Note

This is a **portfolio project** designed to demonstrate skills in:

- Python programming
- FastAPI framework
- AI/ML libraries (scikit-learn)
- React and TypeScript
- Full-stack development

---

## Author

**Jay Karamchandani**

- Email: jay.kc.fullstackdeveloper@gmail.com
- LinkedIn: [@jaykcdev](https://www.linkedin.com/in/jaykcdev/)
- GitHub: [@JayKCDev](https://github.com/JayKCDev)
