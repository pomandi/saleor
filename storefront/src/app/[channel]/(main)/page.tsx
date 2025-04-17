import React from "react";
import { ImageGallery } from "./ImageGallery";
import { ProductListDocument } from "@/gql/graphql";
import { executeGraphQL } from "@/lib/graphql";
import { ProductList } from "@/ui/components/ProductList";

interface PageProps {
	params: {
		channel: string;
	};
}

const Page: React.FC<PageProps> = async ({ params }) => {
	const data = await executeGraphQL(ProductListDocument, {
		variables: {
			channel: params.channel,
			first: 20, // Fetch first 20 products
		},
		revalidate: 60,
	});

	const products = data.products?.edges || [];

	return (
		<div className="mx-auto max-w-7xl p-8 pb-16">
			<section className="text-center mb-16">
				<h1 className="text-4xl md:text-5xl font-bold mb-6">Premium Men&apos;s Suits</h1>
				<p className="text-xl text-gray-600 max-w-3xl mx-auto">
					Discover our exclusive collection of handcrafted suits, tailored to perfection for the modern gentleman.
					Each piece is a masterwork of style, comfort, and sophistication.
				</p>
			</section>

			<ImageGallery />

			{products.length > 0 ? (
				<section>
					<h2 className="text-3xl font-bold mb-8 text-center">Our Collection</h2>
					<ProductList products={products.map(({ node: product }) => product)} />
				</section>
			) : (
				<section className="text-center py-12">
					<p className="text-xl text-gray-600">No products available at the moment.</p>
				</section>
			)}
		</div>
	);
};

export default Page;
