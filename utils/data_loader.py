import pandas as pd
from pathlib import Path


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
        """Load all datasets once at startup"""
        if self._movies is None:
            data_path = Path(__file__).parent.parent / "data"

            print("Loading datasets...")
            movies_columns_to_import = ["id", "title", "overview", "release_date", "keywords", "genres", "vote_average",
         "vote_count"]
            self._movies = pd.read_csv(data_path / "movies.csv", usecols=movies_columns_to_import, dtype={"vote_count": 'int32', "vote_average": "float32"})
            self._ratings = pd.read_csv(data_path / "ratings.csv")
            print(f"✓ Loaded {len(self._movies)} movies")
            print(f"✓ Loaded {len(self._ratings)} ratings")
            # Commented out for future use/reference
            # self._credits = pd.read_csv(data_path / "credits.csv")
            # print(f"✓ Loaded {len(self._credits)} credits")

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