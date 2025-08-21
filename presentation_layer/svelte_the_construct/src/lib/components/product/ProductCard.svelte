<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Product } from '$types';
  import { cartStore } from '$stores/cart';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';

  export let product: Product;
  export let showAddToCart: boolean = true;
  export let compact: boolean = false;

  const dispatch = createEventDispatcher();

  function handleAddToCart() {
    cartStore.addItem(product, 1);
    dispatch('add-to-cart', { product });
  }

  function handleViewDetails() {
    dispatch('view-details', { product });
  }

  function handleCompare() {
    dispatch('compare', { product });
  }

  function handleWishlist() {
    dispatch('wishlist', { product });
  }

  $: formattedPrice = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(product.price);

  $: isAvailable = product.inventory?.available > 0;
</script>

<Card 
  clickable={true} 
  shadow={true} 
  {compact}
  on:click={handleViewDetails}
  class="product-card h-full"
>
  <!-- Product Image -->
  <div class="aspect-video bg-base-200 rounded-lg mb-4 overflow-hidden relative group">
    {#if product.images && product.images.length > 0}
      <img 
        src={product.images[0]} 
        alt={product.name}
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        loading="lazy"
      />
    {:else}
      <div class="w-full h-full flex items-center justify-center">
        <svg class="w-16 h-16 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
    {/if}
    
    <!-- Status Badge -->
    {#if !isAvailable}
      <div class="absolute top-2 left-2">
        <span class="badge badge-error">Out of Stock</span>
      </div>
    {:else if product.inventory?.available < 10}
      <div class="absolute top-2 left-2">
        <span class="badge badge-warning">Low Stock</span>
      </div>
    {/if}

    <!-- Quick Actions -->
    <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div class="flex flex-col gap-1">
        <button
          class="btn btn-circle btn-sm bg-base-100/80 hover:bg-base-100"
          on:click|stopPropagation={handleWishlist}
          aria-label="Add to wishlist"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
        <button
          class="btn btn-circle btn-sm bg-base-100/80 hover:bg-base-100"
          on:click|stopPropagation={handleCompare}
          aria-label="Compare product"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
  
  <!-- Product Info -->
  <div class="flex-1 flex flex-col">
    <!-- Category -->
    <div class="mb-2">
      <span class="badge badge-outline badge-sm">{product.category}</span>
    </div>

    <!-- Product Name -->
    <h3 class="font-semibold text-lg mb-2 line-clamp-2 flex-shrink-0">
      {product.name}
    </h3>
    
    <!-- Description -->
    <p class="text-base-content/70 text-sm mb-4 line-clamp-3 flex-1">
      {product.description}
    </p>
    
    <!-- Manufacturer -->
    <div class="mb-3">
      <span class="text-xs text-base-content/60">by</span>
      <span class="text-sm font-medium text-primary">{product.manufacturer}</span>
    </div>

    <!-- Rating and Reviews -->
    <div class="flex items-center gap-2 mb-4">
      <div class="flex items-center gap-1">
        {#each Array(5) as _, i}
          <svg 
            class="w-4 h-4 {i < Math.floor(product.ratings?.average || 0) ? 'text-warning' : 'text-base-300'}" 
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        {/each}
      </div>
      <span class="text-sm text-base-content/70">
        {product.ratings?.average?.toFixed(1) || 'N/A'}
      </span>
      <span class="text-xs text-base-content/50">
        ({product.ratings?.count || 0} reviews)
      </span>
    </div>
    
    <!-- Price and Stock -->
    <div class="flex justify-between items-center mb-4">
      <div>
        <span class="text-2xl font-bold text-primary">
          {formattedPrice}
        </span>
        <span class="text-sm text-base-content/70 ml-1">
          {product.currency}
        </span>
      </div>
      <div class="text-right">
        <div class="text-sm text-base-content/70">
          {product.inventory?.available || 0} in stock
        </div>
      </div>
    </div>
  </div>
  
  <!-- Actions -->
  <div slot="actions" class="flex gap-2">
    <Button 
      variant="outline" 
      size="sm" 
      fullWidth
      on:click|stopPropagation={handleViewDetails}
    >
      View Details
    </Button>
    {#if showAddToCart && isAvailable}
      <Button 
        variant="primary" 
        size="sm" 
        fullWidth
        on:click|stopPropagation={handleAddToCart}
      >
        Add to Cart
      </Button>
    {:else if !isAvailable}
      <Button 
        variant="ghost" 
        size="sm" 
        fullWidth
        disabled
      >
        Out of Stock
      </Button>
    {/if}
  </div>
</Card>

<style>
  .product-card {
    @apply transition-all duration-300 hover:shadow-xl;
  }

  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .aspect-video {
    aspect-ratio: 16 / 9;
  }

  .badge {
    @apply text-xs font-medium;
  }

  .badge-outline {
    @apply border border-base-300 text-base-content/70;
  }

  .badge-error {
    @apply bg-error text-error-content;
  }

  .badge-warning {
    @apply bg-warning text-warning-content;
  }
</style>
