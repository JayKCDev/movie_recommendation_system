import axios, { AxiosError } from "axios";
import type {
	PopularMoviesResponse,
	PopularityStatsResponse,
	SimilarMoviesResponse,
	SearchMoviesResponse,
	ApiError,
} from "../types";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
	baseURL: API_BASE_URL,
	headers: {
		"Content-Type": "application/json",
	},
});

/**
 * Get popular movies
 * @param limit - Number of movies to return (1-100)
 * @param percentile - Vote count percentile threshold (0.5-0.99)
 * @returns Popular movies data
 */
export const getPopularMovies = async (
	limit: number = 10,
	percentile: number = 0.9
): Promise<PopularMoviesResponse> => {
	try {
		const response = await api.get<PopularMoviesResponse>("/api/popular", {
			params: { limit, percentile },
		});
		return response.data;
	} catch (error) {
		console.error("Error fetching popular movies:", error);
		throw error;
	}
};

/**
 * Get popularity statistics
 * @returns Statistics data
 */
export const getPopularityStats =
	async (): Promise<PopularityStatsResponse> => {
		try {
			const response = await api.get<PopularityStatsResponse>("/api/stats");
			return response.data;
		} catch (error) {
			console.error("Error fetching stats:", error);
			throw error;
		}
	};

/**
 * Get similar movies (content-based recommendation)
 * @param movieTitle - Title of the movie
 * @param numRecommendations - Number of recommendations (1-50)
 * @returns Similar movies data
 */
export const getSimilarMovies = async (
	movieTitle: string,
	numRecommendations: number = 10
): Promise<SimilarMoviesResponse> => {
	try {
		const response = await api.post<SimilarMoviesResponse>(
			"/api/similar/movies",
			{
				movie_title: movieTitle,
				num_recommendations: numRecommendations,
			}
		);
		return response.data;
	} catch (error) {
		console.error("Error fetching similar movies:", error);
		throw error;
	}
};

/**
 * Search movies by title
 * @param query - Search query
 * @param limit - Maximum results (1-50)
 * @returns Search results
 */
export const searchMovies = async (
	query: string,
	limit: number = 10
): Promise<SearchMoviesResponse> => {
	try {
		const response = await api.get<SearchMoviesResponse>("/api/search", {
			params: { query, limit },
		});
		return response.data;
	} catch (error) {
		console.error("Error searching movies:", error);
		throw error;
	}
};

export default api;
