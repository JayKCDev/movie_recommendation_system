import React, { useState } from "react";

const Header: React.FC = () => {
	const [isMenuOpen, setIsMenuOpen] = useState(false);

	return (
		<header className="bg-white shadow-md">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 sm:py-4">
				<div className="flex items-center justify-between">
					<h1 className="text-xl sm:text-2xl md:text-3xl font-bold text-primary">
						MovieMind AI
					</h1>
					{/* Desktop Navigation */}
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
					{/* Mobile Menu Button */}
					<button
						onClick={() => setIsMenuOpen(!isMenuOpen)}
						className="md:hidden p-2 text-gray-600 hover:text-primary focus:outline-none focus:ring-2 focus:ring-primary rounded-md transition-colors"
						aria-label="Toggle menu"
					>
						<svg
							className="w-6 h-6"
							fill="none"
							strokeLinecap="round"
							strokeLinejoin="round"
							strokeWidth="2"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							{isMenuOpen ? (
								<path d="M6 18L18 6M6 6l12 12" />
							) : (
								<path d="M4 6h16M4 12h16M4 18h16" />
							)}
						</svg>
					</button>
				</div>
				{/* Mobile Navigation */}
				{isMenuOpen && (
					<nav className="md:hidden mt-4 pb-2 border-t border-gray-200 pt-4">
						<div className="flex flex-col gap-3">
							<a
								href="#content-based"
								onClick={() => setIsMenuOpen(false)}
								className="text-secondary hover:text-primary transition-colors py-2 px-2 rounded-md hover:bg-gray-50"
							>
								Content-Based
							</a>
							<a
								href="#popular"
								onClick={() => setIsMenuOpen(false)}
								className="text-secondary hover:text-primary transition-colors py-2 px-2 rounded-md hover:bg-gray-50"
							>
								Popular Movies
							</a>
						</div>
					</nav>
				)}
			</div>
		</header>
	);
};

export default Header;
