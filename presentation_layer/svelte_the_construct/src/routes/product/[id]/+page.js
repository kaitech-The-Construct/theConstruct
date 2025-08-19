import products from '$lib/data/products.json';

/** @type {import('./$types').PageLoad} */
export function load({ params }) {
  const product = products.find((p) => p.id === parseInt(params.id));
  if (product) {
    return { product };
  } else {
    return { status: 404, error: new Error('Product not found') };
  }
}
