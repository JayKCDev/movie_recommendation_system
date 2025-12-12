import React from "react";

const InfoBanner: React.FC = () => {
	return (
		<div className="bg-indigo-50 border-b border-indigo-100">
			<div className="max-w-7xl mx-auto px-6 py-2">
				<p className="text-sm text-gray-700 text-center">
					This app is deployed on a free-tier environment (
					<span className="font-semibold">512 MB RAM, 0.1 CPU</span>) purely for
					portfolio demonstration purposes. Resource limitations may cause
					occasional slow responses. Thank you for your consideration.
				</p>
			</div>
		</div>
	);
};

export default InfoBanner;
