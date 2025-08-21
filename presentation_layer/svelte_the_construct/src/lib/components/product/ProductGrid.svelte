<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Product } from '$types';
  import ProductCard from './ProductCard.svelte';

  export let products: Product[] = [];
  export let loading: boolean = false;
  export let emptyMessage: string = 'No products found';
  export let columns: number = 3;

  const dispatch = createEventDispatcher();

  function handleAddToCart(event: CustomEvent) {
    dispatch('add-to-cart', event.detail);
  }

  function handleViewDetails(event: CustomEvent) {
    dispatch('view-details', event.detail);
  }

  function handleCompare(event: CustomEvent) {
    dispatch('compare', event.detail);
  }

  function handleWishlist(event: CustomEvent) {
    dispatch('wishlist', event.detail);
  }

  $: gridClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4',
    5: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5',
    6: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6'
  }[columns] || 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3';
</script>

<div class="product-grid">
  {#if loading}
    <!-- Loading Skeleton -->
    <div class="grid {gridClasses} gap-6">
      {#each Array(6) as _}
        <div class="card bg-base-100 shadow-md animate-pulse">
          <div class="card-body">
            <div class="aspect-video bg-base-300 rounded-lg mb-4"></div>
            <div class="h-4 bg-base-300 rounded mb-2"></div>
            <div class="h-3 bg-base-300 rounded mb-2 w-3/4"></div>
            <div class="h-3 bg-base-300 rounded mb-4 w-1/2"></div>
            <div class="flex justify-between items-center">
              <div class="h-6 bg-base-300 rounded w-20"></div>
              <div class="h-4 bg-base-300 rounded w-16"></div>
            </div>
            <div class="flex gap-2 mt-4">
              <div class="h-8 bg-base-300 rounded flex-1"></div>
              <div class="h-8 bg-base-300 rounded flex-1"></div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {:else if products.length === 0}
    <!-- Empty State -->
    <div class="empty-state text-center py-12">
      <div class="w-24 h-24 bg-base-200 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-12 h-12 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold mb-2 text-base-content/70">
        {emptyMessage}
      </h3>
      <p class="text-base-content/50 mb-6">
        Try adjusting your search criteria or browse our categories.
      </p>
      <slot name="empty-actions" />
    </div>
  {:else}
    <!-- Product Grid -->
    <div class="grid {gridClasses} gap-6">
      {#each products as product (product.id)}
        <div class="animate-fade-in">
          <ProductCard
            {product}
            on:add-to-cart={handleAddToCart}
            on:view-details={handleViewDetails}
            on:compare={handleCompare}
            on:wishlist={handleWishlist}
          />
        </div>
      {/each}
    </div>
  {/if}

  <!-- Results Summary -->
  {#if !loading && products.length > 0}
    <div class="results-summary mt-8 text-center">
      <p class="text-base-content/70">
        Showing {products.length} product{products.length !== 1 ? 's' : ''}
      </p>
    </div>
  {/if}
</div>

<style>
  .product-grid {
    @apply w-full;
  }

  .empty-state {
    @apply max-w-md mx-auto;
  }

  .results-summary {
    @apply border-t border-base-300 pt-4;
  }

  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: .5;
    }
  }

  .animate-fade-in {
    animation: fadeIn 0.5s ease-in-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
