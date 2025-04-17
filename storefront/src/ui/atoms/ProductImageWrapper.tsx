import NextImage, { type ImageProps } from "next/image";

export const ProductImageWrapper = ({ src, ...props }: ImageProps) => {
	// Convert localhost to 127.0.0.1
	const imageUrl = typeof src === 'string' ? src.replace('localhost', '127.0.0.1') : src;

	return (
		<div className="relative h-full w-full">
			<NextImage
				{...props}
				src={imageUrl}
				className="absolute inset-0 h-full w-full object-contain transition-transform duration-300 group-hover:scale-105"
			/>
		</div>
	);
};
