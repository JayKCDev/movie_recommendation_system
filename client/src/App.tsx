import React from "react";
import Header from "./components/Header";
import PopularMovies from "./components/PopularMovies";
import ContentBased from "./components/ContentBased";
import "./App.css";

const App: React.FC = () => {
	return (
		<div className="min-h-screen bg-gray-50">
			<Header />
			<main>
				<ContentBased />
				<PopularMovies />
			</main>
			<footer className="bg-white border-t border-gray-200 py-6 mt-12">
				<div className="max-w-7xl mx-auto px-6 text-center text-secondary">
					<p>Movie Recommendation System &copy; 2024</p>
				</div>
			</footer>
		</div>
	);
};

export default App;
