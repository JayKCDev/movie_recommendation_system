import React from "react";
import Header from "./components/Header";
import InfoBanner from "./components/InfoBanner";
import PopularMovies from "./components/PopularMovies";
import ContentBased from "./components/ContentBased";
import "./App.css";

const App: React.FC = () => {
	return (
		<div className="min-h-screen bg-gray-50">
			<InfoBanner />
			<Header />
			<main>
				<ContentBased />
				<PopularMovies />
			</main>
			<footer className="bg-white border-t border-gray-200 py-4 sm:py-6 mt-8 sm:mt-12">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 text-center text-secondary">
					<p className="text-xs sm:text-sm">
						MovieMind AI | <a href="https://www.linkedin.com/in/jaykcdev/" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">Jay Karamchandani</a> | Portfolio Project &copy; {new Date().getFullYear()}
					</p>
				</div>
			</footer>
		</div>
	);
};

export default App;
