/** @type {import('next').NextConfig} */
const config = {
	images: {
		remotePatterns: [
			{
				protocol: "http",
				hostname: "127.0.0.1",
				port: "8000",
				pathname: "/**",
			},
		],
		unoptimized: true,
	},
	experimental: {
		serverActions: true,
	},
	webpack: (config) => {
		config.module.rules.push({
			test: /\.css$/,
			use: ['style-loader', 'css-loader'],
		});
		return config;
	},
	// used in the Dockerfile
	output:
		process.env.NEXT_OUTPUT === "standalone"
			? "standalone"
			: process.env.NEXT_OUTPUT === "export"
			  ? "export"
			  : undefined,
};

export default config;
