import React from "react";

const Header: React.FC = () => {
	return (
		<header className="bg-white shadow-md">
			<div className="max-w-7xl mx-auto px-6 py-4">
				<div className="flex items-center justify-between">
					<h1 className="text-3xl font-bold text-primary">
						🎬 Movie Recommendation System
					</h1>
					<nav className="hidden md:flex gap-4">
						<a
							href="#content-based"
							className="text-secondary hover:text-primary transition-colors"
						>
							Content-Based
						</a>
						<a
							href="#popular"
							className="text-secondary hover:text-primary transition-colors"
						>
							Popular Movies
						</a>
					</nav>
				</div>
			</div>
		</header>
	);
};

export default Header;
