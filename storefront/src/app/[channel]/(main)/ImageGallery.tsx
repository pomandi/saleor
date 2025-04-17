'use client';

import Image from "next/image";
import React, { useState, useEffect } from "react";

export const ImageGallery = () => {
	const [currentIndex, setCurrentIndex] = useState(0);
	const [imageError, setImageError] = useState<Record<string, boolean>>({});

	const images = [
		"/1.png", "/2.png", "/3.png", "/4.png", "/5.png", "/6.png", "/7.png",
		"/8.png", "/9.png", "/10.png", "/11.png", "/12.png", "/13.png",
		"/14.png", "/15.png", "/16.png", "/17.png", "/18.png", "/19.png",
		"/20.png", "/21.png", "/22.png", "/23.png", "/24.png", "/25.png",
		"/26.png", "/27.png", "/28.png", "/29.png", "/30.png", "/31.png",
		"/32.png", "/33.png"
	].filter(image => !imageError[image]);

	useEffect(() => {
		const timer = setInterval(() => {
			if (images.length > 0) {
				setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
			}
		}, 5000);

		return () => clearInterval(timer);
	}, [images.length]);

	const goToSlide = (index: number) => {
		setCurrentIndex(index);
	};

	const goToNextSlide = () => {
		setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
	};

	const goToPrevSlide = () => {
		setCurrentIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
	};

	const handleImageError = (imagePath: string) => {
		setImageError(prev => ({
			...prev,
			[imagePath]: true
		}));
	};

	if (images.length === 0) {
		return null;
	}

	return (
		<div className="w-full max-w-screen-xl mx-auto px-4 py-8">
			<div className="relative aspect-[16/9]">
				{images.map((image, index) => (
					<div
						key={index}
						className={`absolute w-full h-full transition-opacity duration-500 ${
							index === currentIndex ? "opacity-100" : "opacity-0"
						}`}
					>
						<Image
							src={image}
							alt={`Premium Men's Suit ${index + 1}`}
							fill
							className="object-contain rounded-lg"
							priority={index === 0}
							onError={() => handleImageError(image)}
							sizes="(max-width: 1280px) 100vw, 1280px"
						/>
					</div>
				))}
				{images.length > 1 && (
					<>
						<button
							onClick={goToPrevSlide}
							className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors"
							aria-label="Previous slide"
						>
							←
						</button>
						<button
							onClick={goToNextSlide}
							className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors"
							aria-label="Next slide"
						>
							→
						</button>
						<div className="absolute bottom-4 left-0 right-0 flex justify-center gap-1 flex-wrap px-4">
							{images.map((_, index) => (
								<button
									key={index}
									onClick={() => goToSlide(index)}
									className={`w-2 h-2 rounded-full transition-colors ${
										index === currentIndex ? "bg-white" : "bg-white/50"
									}`}
									aria-label={`Go to slide ${index + 1}`}
								/>
							))}
						</div>
					</>
				)}
			</div>
		</div>
	);
}; 