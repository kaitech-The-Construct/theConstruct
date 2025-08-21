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
    productStore.setSearchQuery('');
    productStore.setSearchFilters({});
    productStore.loadProducts();
    showFilters = false;
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

  // Get unique categories and manufacturers for filters
  $: categories = [...new Set($filteredProducts.map(p => p.category))];
  $: manufacturers = [...new Set($filteredProducts.map(p => p.manufacturer))];
</script>

<svelte:head>
  <title>Marketplace - The Construct</title>
  <meta name="description" content="Browse our extensive marketplace of robotics, components, and automation solutions." />
</svelte:head>

<div class="marketplace-page">
  <!-- Page Header -->
  <div class="mb-8">
    <h1 class="text-4xl font-bold mb-4">Marketplace</h1>
    <p class="text-lg text-base-content/70 mb-6">
      Discover cutting-edge robotics and automation solutions from verified manufacturers worldwide.
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
  {#if Object.keys(currentFilters).length > 0}
    <div class="active-filters mb-6">
      <div class="flex flex-wrap gap-2 items-center">
        <span class="text-sm font-medium">Active filters:</span>
        
        {#if currentFilters.category}
          <span class="badge badge-primary gap-1">
            Category: {currentFilters.category}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => {
                currentFilters.category = undefined;
                handleApplyFilters({ detail: currentFilters });
              }}
            >
              ×
            </button>
          </span>
        {/if}
        
        {#if currentFilters.manufacturer}
          <span class="badge badge-primary gap-1">
            Manufacturer: {currentFilters.manufacturer}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => {
                currentFilters.manufacturer = undefined;
                handleApplyFilters({ detail: currentFilters });
              }}
            >
              ×
            </button>
          </span>
        {/if}
        
        {#if currentFilters.min_price || currentFilters.max_price}
          <span class="badge badge-primary gap-1">
            Price: ${currentFilters.min_price || 0} - ${currentFilters.max_price || '∞'}
            <button 
              class="btn btn-circle btn-xs"
              on:click={() => {
                currentFilters.min_price = undefined;
                currentFilters.max_price = undefined;
                handleApplyFilters({ detail: currentFilters });
              }}
            >
              ×
            </button>
          </span>
        {/if}
        
        <Button variant="ghost" size="sm" on:click={handleClearFilters}>
          Clear All
        </Button>
      </div>
    </div>
  {/if}

  <!-- Results Header -->
  {#if !$isLoading && $filteredProducts.length > 0}
    <div class="results-header mb-6 flex justify-between items-center">
      <div>
        <h2 class="text-xl font-semibold">
          {$filteredProducts.length} Product{$filteredProducts.length !== 1 ? 's' : ''} Found
        </h2>
        {#if searchQuery}
          <p class="text-base-content/70">
            Results for "{searchQuery}"
          </p>
        {/if}
      </div>
      
      <!-- View Toggle -->
      <div class="flex gap-2">
        <button class="btn btn-square btn-sm btn-active">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
        </button>
        <button class="btn btn-square btn-sm">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>
  {/if}

  <!-- Product Grid -->
  <ProductGrid
    products={$filteredProducts}
    loading={$isLoading}
    emptyMessage="No products match your search criteria"
    on:add-to-cart={handleAddToCart}
    on:view-details={handleViewDetails}
    on:compare={handleCompare}
    on:wishlist={handleWishlist}
  >
    <div slot="empty-actions" class="flex gap-4 justify-center">
      <Button variant="primary" on:click={handleClearFilters}>
        Clear Filters
      </Button>
      <Button variant="outline" href="/">
        Back to Home
      </Button>
    </div>
  </ProductGrid>

  <!-- Load More Button (for pagination) -->
  {#if !$isLoading && $filteredProducts.length > 0 && $filteredProducts.length % 12 === 0}
    <div class="text-center mt-8">
      <Button variant="outline" size="lg">
        Load More Products
      </Button>
    </div>
  {/if}
</div>

<style>
  .marketplace-page {
    @apply max-w-7xl mx-auto;
  }

  .active-filters {
    @apply bg-base-100 border border-base-300 rounded-lg p-4;
  }

  .results-header {
    @apply border-b border-base-300 pb-4;
  }

  .badge {
    @apply inline-flex items-center;
  }

  .btn-xs {
    @apply w-4 h-4 min-h-0 p-0;
  }
</style>
