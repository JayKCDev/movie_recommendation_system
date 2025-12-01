import React, { useState, useEffect } from "react";
import { getPopularMovies, getPopularityStats } from "../services/api";
import MovieCard from "./MovieCard";
import type { Movie, PopularityStats } from "../types";

const PopularMovies: React.FC = () => {
	const [movies, setMovies] = useState<Movie[]>([]);
	const [stats, setStats] = useState<PopularityStats | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);
	const [limit, setLimit] = useState<number>(10);
	const [percentile, setPercentile] = useState<number>(0.9);

	useEffect(() => {
		fetchPopularMovies();
		fetchStats();
	}, [limit, percentile]);

	const fetchPopularMovies = async (): Promise<void> => {
		try {
			setLoading(true);
			setError(null);
			const data = await getPopularMovies(limit, percentile);
			setMovies(data.movies || []);
		} catch (err) {
			setError(
				"Failed to load popular movies. Make sure the backend is running."
			);
			console.error(err);
		} finally {
			setLoading(false);
		}
	};

	const fetchStats = async (): Promise<void> => {
		try {
			const data = await getPopularityStats();
			setStats(data.stats);
		} catch (err) {
			console.error("Failed to load stats:", err);
		}
	};

	return (
		<section id="popular" className="py-8 bg-gray-50">
			<div className="max-w-7xl mx-auto px-6">
				<div className="mb-8">
					<h2 className="text-4xl font-bold text-gray-800 mb-2">
						Popular Movies
					</h2>
					<p className="text-lg text-secondary">
						Top-rated movies based on IMDB weighted rating formula
					</p>
				</div>

				{stats && (
					<div className="mb-6 p-4 bg-white rounded-lg shadow-sm">
						<div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
							<div>
								<p className="text-2xl font-bold text-primary">
									{stats.total_movies}
								</p>
								<p className="text-sm text-secondary">Total Movies</p>
							</div>
							<div>
								<p className="text-2xl font-bold text-primary">
									{stats.qualified_movies}
								</p>
								<p className="text-sm text-secondary">Qualified Movies</p>
							</div>
							<div>
								<p className="text-2xl font-bold text-primary">
									{stats.min_vote_threshold}
								</p>
								<p className="text-sm text-secondary">Min Vote Threshold</p>
							</div>
							<div>
								<p className="text-2xl font-bold text-primary">
									{stats.mean_vote_average.toFixed(2)}
								</p>
								<p className="text-sm text-secondary">Mean Vote Average</p>
							</div>
						</div>
					</div>
				)}

				<div className="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center">
					<div className="flex items-center gap-2">
						<label
							htmlFor="limit"
							className="text-sm font-medium text-gray-700"
						>
							Number of movies:
						</label>
						<input
							id="limit"
							type="number"
							min="1"
							max="100"
							value={limit}
							onChange={(e) => setLimit(parseInt(e.target.value) || 10)}
							className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
						/>
					</div>
					<div className="flex items-center gap-2">
						<label
							htmlFor="percentile"
							className="text-sm font-medium text-gray-700"
						>
							Percentile threshold:
						</label>
						<input
							id="percentile"
							type="number"
							min="0.5"
							max="0.99"
							step="0.01"
							value={percentile}
							onChange={(e) => setPercentile(parseFloat(e.target.value) || 0.9)}
							className="w-24 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
						/>
					</div>
				</div>

				{loading && (
					<div className="text-center py-12">
						<div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
						<p className="mt-4 text-secondary">Loading popular movies...</p>
					</div>
				)}

				{error && (
					<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
						{error}
					</div>
				)}

				{!loading && !error && movies.length > 0 && (
					<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
						{movies.map((movie) => (
							<MovieCard key={movie.id} movie={movie} />
						))}
					</div>
				)}

				{!loading && !error && movies.length === 0 && (
					<div className="text-center py-12 text-secondary">
						No movies found. Try adjusting the filters.
					</div>
				)}
			</div>
		</section>
	);
};

export default PopularMovies;
