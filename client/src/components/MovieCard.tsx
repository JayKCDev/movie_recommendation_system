import React from "react";
import type { MovieCardProps } from "../types";

const MovieCard: React.FC<MovieCardProps> = ({
	movie,
	showSimilarity = false,
}) => {
	const formatDate = (dateString: string | null | undefined): string => {
		if (!dateString) return "N/A";
		try {
			const date = new Date(dateString);
			return date.getFullYear().toString();
		} catch {
			return dateString;
		}
	};

	const renderRating = (): JSX.Element | null => {
		if ("weighted_rating" in movie && movie.weighted_rating !== undefined) {
			return (
				<div className="flex flex-col sm:flex-row items-start sm:items-center gap-1 sm:gap-2">
					<span className="text-accent text-base sm:text-lg font-semibold">
						⭐ {movie.weighted_rating.toFixed(1)}
					</span>
					<span className="text-xs sm:text-sm text-secondary">
						({movie.vote_count} votes)
					</span>
				</div>
			);
		} else if (movie.vote_average !== undefined) {
			return (
				<div className="flex flex-col sm:flex-row items-start sm:items-center gap-1 sm:gap-2">
					<span className="text-accent text-base sm:text-lg font-semibold">
						⭐ {movie.vote_average.toFixed(1)}
					</span>
					<span className="text-xs sm:text-sm text-secondary">
						({movie.vote_count || 0} votes)
					</span>
				</div>
			);
		}
		return null;
	};

	return (
		<div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden h-full flex flex-col">
			<div className="p-4 sm:p-5 md:p-6 flex-1 flex flex-col">
				<div className="mb-3">
					<h3 className="text-lg sm:text-xl font-bold text-gray-800 mb-1 line-clamp-2">
						{movie.title}
					</h3>
					{movie.release_date && (
						<p className="text-xs sm:text-sm text-secondary">
							{formatDate(movie.release_date)}
						</p>
					)}
				</div>

				{movie.overview && (
					<p className="text-xs sm:text-sm text-gray-600 mb-4 line-clamp-4 sm:line-clamp-6 flex-1">
						{movie.overview}
					</p>
				)}
				<div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 sm:gap-0 mt-auto">
					{renderRating()}
					{showSimilarity &&
						"similarity_score" in movie &&
						movie.similarity_score !== undefined && (
							<span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded whitespace-nowrap">
								{Math.round(movie.similarity_score * 100)}% match
							</span>
						)}
				</div>
			</div>
		</div>
	);
};

export default MovieCard;
