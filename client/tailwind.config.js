/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				primary: "#6366f1",
				secondary: "#6b7280",
				accent: "#fbbf24",
			},
		},
	},
	plugins: [],
};
