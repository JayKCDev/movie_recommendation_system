import React, { useState, useEffect } from "react";
import { getSimilarMovies, searchMovies } from "../services/api";
import MovieCard from "./MovieCard";
import type {
	MovieWithSimilarity,
	SearchMovieResult,
	ApiError,
} from "../types";

const ContentBased: React.FC = () => {
	const [query, setQuery] = useState<string>("");
	const [searchResults, setSearchResults] = useState<SearchMovieResult[]>([]);
	const [recommendations, setRecommendations] = useState<MovieWithSimilarity[]>(
		[]
	);
	const [matchedMovie, setMatchedMovie] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(false);
	const [searching, setSearching] = useState<boolean>(false);
	const [error, setError] = useState<string | null>(null);
	const [numRecommendations, setNumRecommendations] = useState<number>(10);
	const [showSearchResults, setShowSearchResults] = useState<boolean>(false);

	useEffect(() => {
		const timer = setTimeout(() => {
			if (query.length >= 2) {
				handleSearch();
			} else {
				setSearchResults([]);
				setShowSearchResults(false);
			}
		}, 300);

		return () => clearTimeout(timer);
	}, [query]);

	const handleSearch = async (): Promise<void> => {
		if (query.length < 2) return;

		try {
			setSearching(true);
			const data = await searchMovies(query, 10);
			setSearchResults(data.results || []);
			setShowSearchResults(true);
		} catch (err) {
			console.error("Search error:", err);
			setSearchResults([]);
		} finally {
			setSearching(false);
		}
	};

	const handleGetRecommendations = async (
		movieTitle: string
	): Promise<void> => {
		if (!movieTitle) return;

		try {
			setLoading(true);
			setError(null);
			setShowSearchResults(false);
			const data = await getSimilarMovies(movieTitle, numRecommendations);
			setRecommendations(data.recommendations || []);
			setMatchedMovie(data.matched_movie);
			setQuery(movieTitle);
		} catch (err) {
			const apiError = err as ApiError;
			if (apiError.response?.status === 404) {
				setError(apiError.response.data?.detail || "Movie not found");
			} else {
				setError(
					"Failed to get recommendations. Make sure the backend is running."
				);
			}
			setRecommendations([]);
			setMatchedMovie(null);
		} finally {
			setLoading(false);
		}
	};

	const handleSearchResultClick = (movieTitle: string): void => {
		setQuery(movieTitle);
		handleGetRecommendations(movieTitle);
	};

	const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
		e.preventDefault();
		if (query.trim()) {
			handleGetRecommendations(query.trim());
		}
	};

	return (
		<section id="content-based" className="py-8 bg-white">
			<div className="max-w-7xl mx-auto px-6">
				<div className="mb-8">
					<h2 className="text-4xl font-bold text-gray-800 mb-2">
						Content-Based Recommendations
					</h2>
					<p className="text-lg text-secondary">
						Find movies similar to your favorite based on movie title and
						description
					</p>
				</div>

				<div className="mb-8">
					<form onSubmit={handleSubmit} className="relative">
						<div className="flex flex-col sm:flex-row gap-4">
							<div className="flex-1 relative">
								<input
									type="text"
									value={query}
									onChange={(e) => setQuery(e.target.value)}
									placeholder="Search for a movie (e.g., 'The Dark Knight')..."
									className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-lg"
								/>
								{searching && (
									<div className="absolute right-3 top-1/2 transform -translate-y-1/2">
										<div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary"></div>
									</div>
								)}
								{showSearchResults && searchResults.length > 0 && (
									<div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
										{searchResults.map((movie) => (
											<button
												key={movie.id}
												type="button"
												onClick={() => handleSearchResultClick(movie.title)}
												className="w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors border-b border-gray-100 last:border-b-0"
											>
												<div className="font-medium text-gray-800">
													{movie.title}
												</div>
												{movie.release_date && (
													<div className="text-sm text-secondary">
														{new Date(movie.release_date).getFullYear()}
													</div>
												)}
											</button>
										))}
									</div>
								)}
							</div>
							<div className="flex items-center gap-2">
								<label
									htmlFor="numRecs"
									className="text-sm font-medium text-gray-700 whitespace-nowrap"
								>
									Results:
								</label>
								<input
									id="numRecs"
									type="number"
									min="1"
									max="50"
									value={numRecommendations}
									onChange={(e) =>
										setNumRecommendations(parseInt(e.target.value) || 10)
									}
									className="w-20 px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
								/>
							</div>
							<button
								type="submit"
								disabled={loading || !query.trim()}
								className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
							>
								{loading ? "Loading..." : "Get Recommendations"}
							</button>
						</div>
					</form>
				</div>

				{error && (
					<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
						{error}
					</div>
				)}

				{matchedMovie && (
					<div className="mb-6 p-4 bg-primary/10 border border-primary/20 rounded-lg">
						<p className="text-sm text-secondary mb-1">
							Showing recommendations for:
						</p>
						<p className="text-xl font-bold text-primary">{matchedMovie}</p>
					</div>
				)}

				{loading && (
					<div className="text-center py-12">
						<div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
						<p className="mt-4 text-secondary">Finding similar movies...</p>
					</div>
				)}

				{!loading && recommendations.length > 0 && (
					<>
						<div className="mb-4">
							<h3 className="text-2xl font-bold text-gray-800">
								Similar Movies ({recommendations.length})
							</h3>
						</div>
						<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
							{recommendations.map((movie) => (
								<MovieCard key={movie.id} movie={movie} showSimilarity={true} />
							))}
						</div>
					</>
				)}

				{!loading && !error && recommendations.length === 0 && query && (
					<div className="text-center py-12 text-secondary">
						Enter a movie title above to get recommendations
					</div>
				)}
			</div>
		</section>
	);
};

export default ContentBased;
