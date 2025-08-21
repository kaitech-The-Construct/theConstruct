<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Product } from '$types';
  import { cartStore } from '$stores/cart';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';

  export let products: Product[] = [];
  export let maxProducts: number = 4;

  const dispatch = createEventDispatcher();

  $: comparisonData = products.slice(0, maxProducts);

  function handleRemoveProduct(productId: string) {
    dispatch('remove-product', { productId });
  }

  function handleAddToCart(product: Product) {
    cartStore.addItem(product, 1);
    dispatch('add-to-cart', { product });
  }

  function handleViewDetails(product: Product) {
    dispatch('view-details', { product });
  }

  function handleClearComparison() {
    dispatch('clear-comparison');
  }

  function formatPrice(price: number, currency: string = 'USD') {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency
    }).format(price);
  }

  function getSpecificationValue(product: Product, key: string): string {
    return product.specifications?.technical?.[key] || 'N/A';
  }

  // Get all unique specification keys across all products
  $: allSpecKeys = Array.from(
    new Set(
      comparisonData.flatMap(product => 
        Object.keys(product.specifications?.technical || {})
      )
    )
  ).sort();
</script>

<div class="product-comparison">
  {#if comparisonData.length === 0}
    <!-- Empty State -->
    <Card title="Product Comparison">
      <div class="text-center py-12">
        <div class="w-24 h-24 bg-base-200 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-12 h-12 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold mb-2">No Products to Compare</h3>
        <p class="text-base-content/70 mb-6">
          Add products from the marketplace to compare their features and specifications.
        </p>
        <Button variant="primary" href="/marketplace">
          Browse Marketplace
        </Button>
      </div>
    </Card>
  {:else}
    <!-- Comparison Table -->
    <div class="comparison-header mb-6 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">Product Comparison</h1>
        <p class="text-base-content/70">
          Comparing {comparisonData.length} product{comparisonData.length !== 1 ? 's' : ''}
        </p>
      </div>
      <Button variant="outline" on:click={handleClearComparison}>
        Clear All
      </Button>
    </div>

    <div class="comparison-table overflow-x-auto">
      <table class="table table-zebra w-full">
        <thead>
          <tr>
            <th class="sticky left-0 bg-base-100 z-10 min-w-[200px]">Feature</th>
            {#each comparisonData as product}
              <th class="min-w-[250px] text-center">
                <div class="product-header p-4">
                  <!-- Product Image -->
                  <div class="w-20 h-20 bg-base-200 rounded-lg overflow-hidden mx-auto mb-3">
                    {#if product.images && product.images.length > 0}
                      <img 
                        src={product.images[0]} 
                        alt={product.name}
                        class="w-full h-full object-cover"
                      />
                    {:else}
                      <div class="w-full h-full flex items-center justify-center">
                        <svg class="w-8 h-8 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                      </div>
                    {/if}
                  </div>
                  
                  <!-- Product Name -->
                  <h3 class="font-semibold text-sm mb-1 line-clamp-2">
                    {product.name}
                  </h3>
                  
                  <!-- Manufacturer -->
                  <p class="text-xs text-base-content/70 mb-2">
                    by {product.manufacturer}
                  </p>
                  
                  <!-- Remove Button -->
                  <button
                    class="btn btn-circle btn-xs btn-error"
                    on:click={() => handleRemoveProduct(product.id)}
                    aria-label="Remove from comparison"
                  >
                    ×
                  </button>
                </div>
              </th>
            {/each}
          </tr>
        </thead>
        <tbody>
          <!-- Basic Information -->
          <tr class="bg-base-200">
            <td class="sticky left-0 bg-base-200 font-semibold">Basic Information</td>
            {#each comparisonData as _}
              <td></td>
            {/each}
          </tr>
          
          <tr>
            <td class="sticky left-0 bg-base-100 font-medium">Price</td>
            {#each comparisonData as product}
              <td class="text-center">
                <span class="text-lg font-bold text-primary">
                  {formatPrice(product.price, product.currency)}
                </span>
              </td>
            {/each}
          </tr>

          <tr>
            <td class="sticky left-0 bg-base-100 font-medium">Category</td>
            {#each comparisonData as product}
              <td class="text-center">
                <span class="badge badge-outline">{product.category}</span>
              </td>
            {/each}
          </tr>

          <tr>
            <td class="sticky left-0 bg-base-100 font-medium">Rating</td>
            {#each comparisonData as product}
              <td class="text-center">
                <div class="flex items-center justify-center gap-1">
                  <span class="font-medium">
                    {product.ratings?.average?.toFixed(1) || 'N/A'}
                  </span>
                  <div class="flex">
                    {#each Array(5) as _, i}
                      <svg 
                        class="w-3 h-3 {i < Math.floor(product.ratings?.average || 0) ? 'text-warning' : 'text-base-300'}" 
                        fill="currentColor" 
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    {/each}
                  </div>
                </div>
                <div class="text-xs text-base-content/70">
                  ({product.ratings?.count || 0} reviews)
                </div>
              </td>
            {/each}
          </tr>

          <tr>
            <td class="sticky left-0 bg-base-100 font-medium">Availability</td>
            {#each comparisonData as product}
              <td class="text-center">
                {#if product.inventory?.available > 0}
                  <span class="badge badge-success">In Stock</span>
                  <div class="text-xs text-base-content/70 mt-1">
                    {product.inventory.available} available
                  </div>
                {:else}
                  <span class="badge badge-error">Out of Stock</span>
                {/if}
              </td>
            {/each}
          </tr>

          <!-- Technical Specifications -->
          {#if allSpecKeys.length > 0}
            <tr class="bg-base-200">
              <td class="sticky left-0 bg-base-200 font-semibold">Technical Specifications</td>
              {#each comparisonData as _}
                <td></td>
              {/each}
            </tr>

            {#each allSpecKeys as specKey}
              <tr>
                <td class="sticky left-0 bg-base-100 font-medium capitalize">
                  {specKey.replace(/_/g, ' ')}
                </td>
                {#each comparisonData as product}
                  <td class="text-center">
                    {getSpecificationValue(product, specKey)}
                  </td>
                {/each}
              </tr>
            {/each}
          {/if}

          <!-- Compatibility -->
          <tr class="bg-base-200">
            <td class="sticky left-0 bg-base-200 font-semibold">Compatibility</td>
            {#each comparisonData as _}
              <td></td>
            {/each}
          </tr>

          <tr>
            <td class="sticky left-0 bg-base-100 font-medium">Compatible Systems</td>
            {#each comparisonData as product}
              <td class="text-center">
                {#if product.specifications?.compatibility && product.specifications.compatibility.length > 0}
                  <div class="flex flex-wrap gap-1 justify-center">
                    {#each product.specifications.compatibility.slice(0, 3) as item}
                      <span class="badge badge-outline badge-xs">{item}</span>
                    {/each}
                    {#if product.specifications.compatibility.length > 3}
                      <span class="text-xs text-base-content/70">
                        +{product.specifications.compatibility.length - 3} more
                      </span>
                    {/if}
                  </div>
                {:else}
                  <span class="text-base-content/70">N/A</span>
                {/if}
              </td>
            {/each}
          </tr>

          <!-- Actions -->
          <tr class="bg-base-200">
            <td class="sticky left-0 bg-base-200 font-semibold">Actions</td>
            {#each comparisonData as _}
              <td></td>
            {/each}
          </tr>

          <tr>
            <td class="sticky left-0 bg-base-100 font-medium">Purchase</td>
            {#each comparisonData as product}
              <td class="text-center p-4">
                <div class="space-y-2">
                  {#if product.inventory?.available > 0}
                    <Button
                      variant="primary"
                      size="sm"
                      fullWidth
                      on:click={() => handleAddToCart(product)}
                    >
                      Add to Cart
                    </Button>
                  {:else}
                    <Button variant="ghost" size="sm" fullWidth disabled>
                      Out of Stock
                    </Button>
                  {/if}
                  <Button
                    variant="outline"
                    size="sm"
                    fullWidth
                    on:click={() => handleViewDetails(product)}
                  >
                    View Details
                  </Button>
                </div>
              </td>
            {/each}
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Comparison Summary -->
    <div class="comparison-summary mt-8">
      <Card title="Comparison Summary">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Best Value -->
          <div class="summary-item">
            <h4 class="font-semibold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
              Best Value
            </h4>
            {#if comparisonData.length > 0}
              {@const bestValue = comparisonData.reduce((best, current) => 
                current.price < best.price ? current : best
              )}
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-base-200 rounded overflow-hidden">
                  <img 
                    src={bestValue.images?.[0] || ''} 
                    alt={bestValue.name}
                    class="w-full h-full object-cover"
                  />
                </div>
                <div>
                  <div class="font-medium text-sm">{bestValue.name}</div>
                  <div class="text-primary font-bold">
                    {formatPrice(bestValue.price, bestValue.currency)}
                  </div>
                </div>
              </div>
            {/if}
          </div>

          <!-- Highest Rated -->
          <div class="summary-item">
            <h4 class="font-semibold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5 text-warning" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              Highest Rated
            </h4>
            {#if comparisonData.length > 0}
              {@const highestRated = comparisonData.reduce((best, current) => 
                (current.ratings?.average || 0) > (best.ratings?.average || 0) ? current : best
              )}
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-base-200 rounded overflow-hidden">
                  <img 
                    src={highestRated.images?.[0] || ''} 
                    alt={highestRated.name}
                    class="w-full h-full object-cover"
                  />
                </div>
                <div>
                  <div class="font-medium text-sm">{highestRated.name}</div>
                  <div class="flex items-center gap-1">
                    <span class="font-bold text-warning">
                      {highestRated.ratings?.average?.toFixed(1) || 'N/A'}
                    </span>
                    <svg class="w-4 h-4 text-warning" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  </div>
                </div>
              </div>
            {/if}
          </div>

          <!-- Most Popular -->
          <div class="summary-item">
            <h4 class="font-semibold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5 text-info" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              Most Popular
            </h4>
            {#if comparisonData.length > 0}
              {@const mostPopular = comparisonData.reduce((best, current) => 
                (current.ratings?.count || 0) > (best.ratings?.count || 0) ? current : best
              )}
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-base-200 rounded overflow-hidden">
                  <img 
                    src={mostPopular.images?.[0] || ''} 
                    alt={mostPopular.name}
                    class="w-full h-full object-cover"
                  />
                </div>
                <div>
                  <div class="font-medium text-sm">{mostPopular.name}</div>
                  <div class="text-info font-bold">
                    {mostPopular.ratings?.count || 0} reviews
                  </div>
                </div>
              </div>
            {/if}
          </div>
        </div>
      </Card>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions mt-6 text-center">
      <div class="flex gap-4 justify-center">
        <Button variant="primary" size="lg">
          Add All to Cart
        </Button>
        <Button variant="outline" href="/marketplace">
          Continue Shopping
        </Button>
      </div>
    </div>
  {/if}
</div>

<style>
  .comparison-table {
    @apply border border-base-300 rounded-lg;
  }

  .table {
    @apply mb-0;
  }

  .table th {
    @apply bg-base-200 font-semibold text-base-content;
  }

  .table td {
    @apply border-r border-base-300 last:border-r-0;
  }

  .product-header {
    @apply border-b border-base-300;
  }

  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .summary-item {
    @apply p-4 bg-base-200 rounded-lg;
  }

  .sticky {
    position: sticky;
  }

  /* Responsive table scrolling */
  .comparison-table {
    scrollbar-width: thin;
    scrollbar-color: theme('colors.base-300') transparent;
  }

  .comparison-table::-webkit-scrollbar {
    height: 8px;
  }

  .comparison-table::-webkit-scrollbar-track {
    background: transparent;
  }

  .comparison-table::-webkit-scrollbar-thumb {
    background-color: theme('colors.base-300');
    border-radius: 4px;
  }

  .comparison-table::-webkit-scrollbar-thumb:hover {
    background-color: theme('colors.base-400');
  }
</style>
