<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { productStore, filteredProducts, isLoading, searchFilters } from '$stores/products';
  import type { SearchFilters } from '$types';
  import SearchBar from '$components/ui/SearchBar.svelte';
  import ProductFilters from '$components/ui/ProductFilters.svelte';
  import ProductGrid from '$components/product/ProductGrid.svelte';
  import Button from '$components/ui/Button.svelte';

  let searchQuery = '';
  let showFilters = false;
  let currentFilters: SearchFilters = {};
  let activeProductType: 'all' | 'robot' | 'software' | 'hardware' = 'all';

  // Load products on mount
  onMount(async () => {
    await productStore.loadProducts();
  });

  function handleSearch(event: CustomEvent) {
    const { value } = event.detail;
    searchQuery = value;
    productStore.setSearchQuery(value);
  }

  function handleToggleFilters(event: CustomEvent) {
    showFilters = event.detail.showFilters;
  }

  function handleApplyFilters(event: CustomEvent) {
    currentFilters = { ...event.detail, query: searchQuery };
    productStore.searchProducts(currentFilters);
    showFilters = false;
  }

  function handleClearFilters() {
    currentFilters = {};
    searchQuery = '';
    activeProductType = 'all';
    productStore.setSearchQuery('');
    productStore.setSearchFilters({});
    productStore.loadProducts();
    showFilters = false;
  }

  function handleProductTypeFilter(type: 'all' | 'robot' | 'software' | 'hardware') {
    activeProductType = type;
    const newFilters = { ...currentFilters };
    
    if (type === 'all') {
      delete newFilters.category;
    } else {
      // Filter by product type
      newFilters.category = type;
    }
    
    currentFilters = newFilters;
    productStore.searchProducts(currentFilters);
  }

  function handleAddToCart(event: CustomEvent) {
    // Show success message or notification
    console.log('Added to cart:', event.detail.product.name);
  }

  function handleViewDetails(event: CustomEvent) {
    const { product } = event.detail;
    goto(`/product/${product.id}`);
  }

  function handleCompare(event: CustomEvent) {
    // Implement product comparison
    console.log('Compare product:', event.detail.product.name);
  }

  function handleWishlist(event: CustomEvent) {
    // Implement wishlist functionality
    console.log('Add to wishlist:', event.detail.product.name);
  }

  // Filter products by type
  $: typeFilteredProducts = (() => {
    if (activeProductType === 'all') {
      return $filteredProducts;
    }
    return $filteredProducts.filter(product => product.product_type === activeProductType);
  })();

  // Get unique categories and manufacturers for filters
  $: categories = [...new Set($filteredProducts.map(p => p.category))];
  $: manufacturers = [...new Set($filteredProducts.map(p => p.manufacturer))];

  // Get product type counts
  $: productTypeCounts = (() => {
    const counts = {
      all: $filteredProducts.length,
      robot: $filteredProducts.filter(p => p.product_type === 'robot').length,
      software: $filteredProducts.filter(p => p.product_type === 'software').length,
      hardware: $filteredProducts.filter(p => p.product_type === 'hardware').length,
    };
    return counts;
  })();
</script>

<svelte:head>
  <title>Marketplace - The Construct</title>
  <meta name="description" content="Browse our extensive marketplace of robotics, components, and automation solutions." />
</svelte:head>

<div class="marketplace-page min-h-screen">
  <!-- Robotic Header -->
  <div class="robotic-card mb-8 p-8 relative overflow-hidden">
    <!-- Background hexagon pattern -->
    <div class="absolute top-4 right-4 opacity-10">
      <div class="hexagon animate-hexagon-rotate"></div>
    </div>
    <div class="absolute bottom-4 left-4 opacity-5">
      <div class="hexagon-small"></div>
    </div>
    
    <h1 class="text-4xl font-display font-bold mb-4 text-glow">
      MARKETPLACE
    </h1>
    <p class="text-lg text-base-content/70 mb-6 font-mono">
      > Discover cutting-edge robotics and automation solutions from verified manufacturers worldwide.
    </p>
    
    <!-- Search Bar -->
    <SearchBar
      bind:value={searchQuery}
      loading={$isLoading}
      {showFilters}
      on:search={handleSearch}
      on:toggle-filters={handleToggleFilters}
    />
  </div>

  <!-- Product Type Filter Tabs -->
  <div class="mb-8">
    <div class="flex flex-wrap gap-2 justify-center">
      <button
        class="robotic-button px-6 py-3 {activeProductType === 'all' ? 'bg-primary/20 border-primary text-primary' : ''}"
        on:click={() => handleProductTypeFilter('all')}
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        ALL SYSTEMS
        <span class="ml-2 badge badge-outline badge-sm">{productTypeCounts.all}</span>
      </button>
      
      <button
        class="robotic-button px-6 py-3 {activeProductType === 'robot' ? 'bg-primary/20 border-primary text-primary' : ''}"
        on:click={() => handleProductTypeFilter('robot')}
      >
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
        </svg>
        ROBOTS
        <span class="ml-2 badge badge-robot badge-sm">{productTypeCounts.robot}</span>
      </button>
      
      <button
        class="robotic-button px-6 py-3 {activeProductType === 'software' ? 'bg-accent/20 border-accent text-accent' : ''}"
        on:click={() => handleProductTypeFilter('software')}
      >
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
          <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0L19.2 12l-4.6-4.6L16 6l6 6-6 6-1.4-1.4z" />
        </svg>
        SOFTWARE
        <span class="ml-2 badge badge-software badge-sm">{productTypeCounts.software}</span>
      </button>
      
      <button
        class="robotic-button px-6 py-3 {activeProductType === 'hardware' ? 'bg-secondary/20 border-secondary text-secondary' : ''}"
        on:click={() => handleProductTypeFilter('hardware')}
      >
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
          <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z" />
        </svg>
        HARDWARE
        <span class="ml-2 badge badge-hardware badge-sm">{productTypeCounts.hardware}</span>
      </button>
    </div>
  </div>

  <!-- Filters -->
  <ProductFilters
    visible={showFilters}
    filters={currentFilters}
    {categories}
    {manufacturers}
    on:apply={handleApplyFilters}
    on:clear={handleClearFilters}
  />

  <!-- Active Filters Display -->
  {#if Object.keys(currentFilters).length > 0 || activeProductType !== 'all'}
    <div class="robotic-card mb-6 p-4">
      <div class="flex flex-wrap gap-2 items-center">
        <span class="text-sm font-mono font-medium text-primary">ACTIVE_FILTERS:</span>
        
        {#if activeProductType !== 'all'}
          <span class="badge badge-primary gap-1 font-mono">
            TYPE: {activeProductType.toUpperCase()}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => handleProductTypeFilter('all')}
            >
              ×
            </button>
          </span>
        {/if}
        
        {#if currentFilters.category && activeProductType === 'all'}
          <span class="badge badge-primary gap-1 font-mono">
            CATEGORY: {currentFilters.category.toUpperCase()}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => {
                currentFilters.category = undefined;
                productStore.searchProducts(currentFilters);
              }}
            >
              ×
            </button>
          </span>
        {/if}
        
        {#if currentFilters.manufacturer}
          <span class="badge badge-secondary gap-1 font-mono">
            MFG: {currentFilters.manufacturer.toUpperCase()}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => {
                currentFilters.manufacturer = undefined;
                productStore.searchProducts(currentFilters);
              }}
            >
              ×
            </button>
          </span>
        {/if}
        
        {#if currentFilters.min_price || currentFilters.max_price}
          <span class="badge badge-accent gap-1 font-mono">
            PRICE: ${currentFilters.min_price || 0} - ${currentFilters.max_price || '∞'}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => {
                currentFilters.min_price = undefined;
                currentFilters.max_price = undefined;
                productStore.searchProducts(currentFilters);
              }}
            >
              ×
            </button>
          </span>
        {/if}
        
        <button class="robotic-button px-3 py-1 text-xs" on:click={handleClearFilters}>
          CLEAR_ALL
        </button>
      </div>
    </div>
  {/if}

  <!-- Results Header -->
  {#if !$isLoading && typeFilteredProducts.length > 0}
    <div class="robotic-card mb-6 p-4">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-xl font-display font-semibold text-glow">
            {typeFilteredProducts.length} UNIT{typeFilteredProducts.length !== 1 ? 'S' : ''} FOUND
          </h2>
          {#if searchQuery}
            <p class="text-base-content/70 font-mono text-sm">
              > SEARCH_QUERY: "{searchQuery}"
            </p>
          {/if}
          {#if activeProductType !== 'all'}
            <p class="text-base-content/70 font-mono text-sm">
              > FILTER_TYPE: {activeProductType.toUpperCase()}
            </p>
          {/if}
        </div>
        
        <!-- View Toggle -->
        <div class="flex gap-2">
          <button class="robotic-button btn btn-square btn-sm bg-primary/20 border-primary text-primary">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </button>
          <button class="robotic-button btn btn-square btn-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  {/if}

  <!-- Product Grid -->
  <ProductGrid
    products={typeFilteredProducts}
    loading={$isLoading}
    emptyMessage="No products match your search criteria"
    on:add-to-cart={handleAddToCart}
    on:view-details={handleViewDetails}
    on:compare={handleCompare}
    on:wishlist={handleWishlist}
  >
    <div slot="empty-actions" class="flex gap-4 justify-center">
      <button class="robotic-button px-6 py-3 bg-primary/20 border-primary text-primary" on:click={handleClearFilters}>
        RESET_FILTERS
      </button>
      <a href="/" class="robotic-button px-6 py-3">
        RETURN_HOME
      </a>
    </div>
  </ProductGrid>

  <!-- Load More Button (for pagination) -->
  {#if !$isLoading && typeFilteredProducts.length > 0 && typeFilteredProducts.length % 12 === 0}
    <div class="text-center mt-8">
      <button class="robotic-button px-8 py-4 text-lg">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        LOAD_MORE_UNITS
      </button>
    </div>
  {/if}
</div>

<style>
  .marketplace-page {
    max-width: 80rem; /* equivalent to max-w-7xl */
    margin-left: auto; /* mx-auto */
    margin-right: auto;
    padding: 1rem; /* p-4 */
  }

  .badge {
    display: inline-flex;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
  }

  .btn-xs {
    width: 1rem;
    height: 1rem;
    min-height: 0;
    padding: 0;
  }

  /* Custom robotic button styling for this page */
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
    border-radius: 0.5rem;
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

  /* Active state styling */
  .robotic-button.bg-primary\/20 {
    background: rgba(0, 255, 225, 0.2);
    border-color: var(--primary);
    color: var(--primary);
  }

  .robotic-button.bg-accent\/20 {
    background: rgba(57, 255, 20, 0.2);
    border-color: var(--accent);
    color: var(--accent);
  }

  .robotic-button.bg-secondary\/20 {
    background: rgba(0, 212, 255, 0.2);
    border-color: var(--secondary);
    color: var(--secondary);
  }
</style>
