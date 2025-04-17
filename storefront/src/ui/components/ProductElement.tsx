import { LinkWithChannel } from "../atoms/LinkWithChannel";
import { ProductImageWrapper } from "@/ui/atoms/ProductImageWrapper";

import type { ProductListItemFragment } from "@/gql/graphql";
import { formatMoneyRange } from "@/lib/utils";

export function ProductElement({
	product,
	loading,
	priority,
}: {
	product: ProductListItemFragment;
	loading: "eager" | "lazy";
	priority?: boolean;
}) {
	const imageUrl = product?.thumbnail?.url;

	return (
		<li data-testid="ProductElement" className="group relative">
			<LinkWithChannel href={`/products/${product.slug}`} key={product.id}>
				<div className="overflow-hidden rounded-lg border border-neutral-200">
					<div className="aspect-square relative bg-neutral-50">
						{imageUrl && (
							<ProductImageWrapper
								loading={loading}
								src={imageUrl}
								alt={product.thumbnail?.alt ?? product.name}
								width={512}
								height={512}
								quality={90}
								sizes="(min-width: 1024px) 25vw, (min-width: 768px) 33vw, 50vw"
								priority={priority}
								className="object-contain transition-transform duration-300 group-hover:scale-105"
							/>
						)}
					</div>
					<div className="p-4">
						<h3 className="text-sm font-medium text-neutral-900">{product.name}</h3>
						<p className="mt-1 text-sm text-neutral-500" data-testid="ProductElement_Category">
							{product.category?.name}
						</p>
						<p className="mt-1 text-sm font-medium text-neutral-900" data-testid="ProductElement_PriceRange">
							{formatMoneyRange({
								start: product?.pricing?.priceRange?.start?.gross,
								stop: product?.pricing?.priceRange?.stop?.gross,
							})}
						</p>
					</div>
				</div>
			</LinkWithChannel>
		</li>
	);
}
