import pandas as pd

# credits_csv_raw_url = "https://media.githubusercontent.com/media/JayKCDev/movie_recommendation_system/refs/heads/main/data/credits.csv"
movies_csv_raw_url = "https://media.githubusercontent.com/media/JayKCDev/movie_recommendation_system/refs/heads/main/data/movies.csv"
ratings_csv_raw_url = "https://media.githubusercontent.com/media/JayKCDev/movie_recommendation_system/refs/heads/main/data/ratings.csv"


class DataLoader:
    """Singleton class to load datasets once at startup"""
    _instance = None
    _movies = None
    _ratings = None
    _credits = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_data(self):
        if self._movies is None:
            print("Loading datasets from GitHub...")

            # Movies - only load needed columns with optimized dtypes
            movies_columns_to_import = [
                "id", "title", "overview", "release_date",
                "keywords", "genres", "vote_average", "vote_count"
            ]
            self._movies = pd.read_csv(
                movies_csv_raw_url,
                usecols=movies_columns_to_import,
                dtype={
                    "id": "int32",
                    "vote_count": "int32",
                    "vote_average": "float32"
                }
            )
            print(f"✓ Loaded {len(self._movies)} movies")

            # Ratings - with optimized dtypes
            self._ratings = pd.read_csv(
                ratings_csv_raw_url,
                dtype={
                    "userId": "int32",
                    "movieId": "int32",
                    "rating": "float32"
                }
            )
            print(f"✓ Loaded {len(self._ratings)} ratings")

    @property
    def movies(self):
        if self._movies is None:
            self.load_data()
        return self._movies

    @property
    def ratings(self):
        if self._ratings is None:
            self.load_data()
        return self._ratings

    @property
    def credits(self):
        if self._credits is None:
            self.load_data()
        return self._credits


# Singleton instance
data_loader = DataLoader()