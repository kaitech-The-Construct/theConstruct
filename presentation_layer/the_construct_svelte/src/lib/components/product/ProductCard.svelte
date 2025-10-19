<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Product, RobotProduct, SoftwareProduct } from '$types';
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

  // Type guards
  function isRobotProduct(product: Product): product is RobotProduct {
    return product.product_type === 'robot';
  }

  function isSoftwareProduct(product: Product): product is SoftwareProduct {
    return product.product_type === 'software';
  }

  // Price formatting for different product types
  $: formattedPrice = (() => {
    if (isRobotProduct(product) && product.price_details) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(product.price_details.listing_price || product.price);
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(product.price);
  })();

  $: subscriptionPrice = (() => {
    if (isRobotProduct(product) && product.price_details) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(product.price_details.subscription_price);
    }
    return null;
  })();

  $: isAvailable = product.inventory?.available > 0;

  // Get product type badge class
  $: productTypeBadge = (() => {
    switch (product.product_type) {
      case 'robot':
        return 'badge-robot';
      case 'software':
        return 'badge-software';
      case 'hardware':
        return 'badge-hardware';
      default:
        return 'badge-outline';
    }
  })();

  // Get product type icon
  $: productTypeIcon = (() => {
    switch (product.product_type) {
      case 'robot':
        return 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z';
      case 'software':
        return 'M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0L19.2 12l-4.6-4.6L16 6l6 6-6 6-1.4-1.4z';
      case 'hardware':
        return 'M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z';
      default:
        return '';
    }
  })();
</script>

<div class="robotic-card product-card h-full animate-fade-in">
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
      <div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-base-200 to-base-300">
        <div class="hexagon-small opacity-30"></div>
      </div>
    {/if}
    
    <!-- Robotic overlay effect -->
    <div class="absolute inset-0 bg-gradient-to-t from-base-100/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    
    <!-- Status Badge -->
    {#if !isAvailable}
      <div class="absolute top-2 left-2">
        <span class="badge badge-error animate-pulse-border">Out of Stock</span>
      </div>
    {:else if product.inventory?.available < 10}
      <div class="absolute top-2 left-2">
        <span class="badge badge-warning animate-pulse-border">Low Stock</span>
      </div>
    {/if}

    <!-- Product Type Badge -->
    <div class="absolute top-2 right-2">
      <span class="badge {productTypeBadge} text-xs font-mono uppercase">
        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 24 24">
          <path d={productTypeIcon} />
        </svg>
        {product.product_type}
      </span>
    </div>

    <!-- Quick Actions -->
    <div class="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div class="flex gap-1">
        <button
          class="robotic-button btn btn-circle btn-sm"
          on:click|stopPropagation={handleWishlist}
          aria-label="Add to wishlist"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
        <button
          class="robotic-button btn btn-circle btn-sm"
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
  <div class="flex-1 flex flex-col p-4">
    <!-- Category -->
    <div class="mb-2">
      <span class="badge badge-outline badge-sm font-mono text-xs">{product.category}</span>
    </div>

    <!-- Product Name -->
    <h3 class="font-display text-lg mb-2 line-clamp-2 flex-shrink-0 text-glow">
      {product.name}
    </h3>
    
    <!-- Product-specific info -->
    {#if isRobotProduct(product)}
      <div class="mb-2 text-xs font-mono text-base-content/70">
        <div>Model: <span class="text-primary">{product.model}</span></div>
        <div>ID: <span class="text-secondary">{product.model_id}</span></div>
      </div>
    {:else if isSoftwareProduct(product)}
      <div class="mb-2 text-xs font-mono text-base-content/70">
        <div>Version: <span class="text-accent">{product.version}</span></div>
        <div>Author: <span class="text-secondary">{product.author}</span></div>
        <div>License: <span class="text-warning">{product.license}</span></div>
      </div>
    {/if}
    
    <!-- Description -->
    <p class="text-base-content/70 text-sm mb-4 line-clamp-3 flex-1 font-mono">
      {product.description}
    </p>
    
    <!-- Manufacturer -->
    <div class="mb-3">
      <span class="text-xs text-base-content/60 font-mono">by</span>
      <span class="text-sm font-mono font-medium text-primary">{product.manufacturer}</span>
    </div>

    <!-- Compatibility Tags -->
    {#if product.specifications?.compatibility && product.specifications.compatibility.length > 0}
      <div class="mb-3">
        <div class="text-xs text-base-content/60 font-mono mb-1">Compatible with:</div>
        <div class="flex flex-wrap gap-1">
          {#each product.specifications.compatibility.slice(0, 3) as compat}
            <span class="badge badge-outline badge-xs font-mono">{compat}</span>
          {/each}
          {#if product.specifications.compatibility.length > 3}
            <span class="badge badge-outline badge-xs font-mono">+{product.specifications.compatibility.length - 3}</span>
          {/if}
        </div>
      </div>
    {/if}

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
      <span class="text-sm text-base-content/70 font-mono">
        {product.ratings?.average?.toFixed(1) || 'N/A'}
      </span>
      <span class="text-xs text-base-content/50 font-mono">
        ({product.ratings?.count || 0})
      </span>
    </div>
    
    <!-- Price and Stock -->
    <div class="flex justify-between items-center mb-4">
      <div>
        {#if subscriptionPrice}
          <div class="text-sm text-base-content/70 font-mono">Subscription</div>
          <span class="text-lg font-bold text-accent font-mono">
            {subscriptionPrice}/mo
          </span>
          <div class="text-xs text-base-content/50 font-mono">
            or {formattedPrice} one-time
          </div>
        {:else}
          <span class="text-2xl font-bold text-primary font-mono">
            {formattedPrice}
          </span>
        {/if}
      </div>
      <div class="text-right">
        <div class="text-sm text-base-content/70 font-mono">
          {product.inventory?.available || 0} units
        </div>
        <div class="text-xs text-base-content/50 font-mono">
          in stock
        </div>
      </div>
    </div>
  </div>
  
  <!-- Actions -->
  <div class="p-4 pt-0 flex gap-2">
    <button
      class="robotic-button flex-1 py-2 px-4 text-sm font-mono uppercase tracking-wide"
      on:click|stopPropagation={handleViewDetails}
    >
      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      </svg>
      Analyze
    </button>
    {#if showAddToCart && isAvailable}
      <button
        class="robotic-button flex-1 py-2 px-4 text-sm font-mono uppercase tracking-wide bg-primary/20 border-primary text-primary"
        on:click|stopPropagation={handleAddToCart}
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
        </svg>
        Acquire
      </button>
    {:else if !isAvailable}
      <button
        class="robotic-button flex-1 py-2 px-4 text-sm font-mono uppercase tracking-wide opacity-50 cursor-not-allowed"
        disabled
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18.364 5.636M5.636 18.364l12.728-12.728" />
        </svg>
        Unavailable
      </button>
    {/if}
  </div>
</div>

<style>
  .product-card {
    transition: all 0.3s;
    cursor: pointer;
  }

  .product-card:hover {
    transform: translateY(-4px);
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
    font-size: 0.75rem;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
  }

  .badge-outline {
    border: 1px solid var(--robotic-border);
    color: #e0e0e0b3;
  }

  .badge-error {
    background-color: var(--error);
    color: var(--error-content);
  }

  .badge-warning {
    background-color: var(--warning);
    color: var(--warning-content);
  }

  /* Custom robotic button styling */
  .robotic-button {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, var(--base-200), var(--base-300));
    border: 1px solid var(--robotic-border);
    color: var(--base-content);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.3s ease;
  }

  .robotic-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 225, 0.2), transparent);
    transition: left 0.5s ease;
  }

  .robotic-button:hover::before {
    left: 100%;
  }

  .robotic-button:hover {
    border-color: var(--robotic-glow);
    color: var(--robotic-glow);
    box-shadow: 0 0 10px var(--robotic-shadow);
    transform: translateY(-1px);
  }

  .robotic-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .robotic-button:disabled:hover {
    transform: none;
    box-shadow: none;
    border-color: var(--robotic-border);
    color: var(--base-content);
  }
</style>
