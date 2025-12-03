// API Response Types
export interface PopularMoviesResponse {
	success: boolean;
	count: number;
	movies: Movie[];
}

export interface PopularityStatsResponse {
	success: boolean;
	stats: PopularityStats;
}

export interface SimilarMoviesResponse {
	success: boolean;
	query: string;
	matched_movie: string;
	count: number;
	recommendations: MovieWithSimilarity[];
}

export interface SearchMoviesResponse {
	success: boolean;
	query: string;
	count: number;
	results: SearchMovieResult[];
}

// Movie Types
export interface Movie {
	id: number;
	title: string;
	overview: string;
	release_date: string;
	vote_average: number;
	vote_count: number;
	weighted_rating?: number;
}

export interface MovieWithSimilarity extends Movie {
	similarity_score: number;
}

export interface SearchMovieResult {
	id: number;
	title: string;
	release_date: string;
}

// Statistics Types
export interface PopularityStats {
	total_movies: number;
	qualified_movies: number;
	min_vote_threshold: number;
	mean_vote_average: number;
}

// Component Props Types
export interface MovieCardProps {
	movie: Movie | MovieWithSimilarity;
	showSimilarity?: boolean;
}

// API Error Types
export interface ApiError {
	response?: {
		status?: number;
		data?: {
			detail?: string;
		};
	};
	message?: string;
}
