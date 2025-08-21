<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { SearchFilters } from '$types';
  import Button from './Button.svelte';
  import Input from './Input.svelte';

  export let filters: SearchFilters = {};
  export let categories: string[] = ['Robots', 'Components', 'Software', 'Tools'];
  export let manufacturers: string[] = [];
  export let visible: boolean = false;

  const dispatch = createEventDispatcher();

  let localFilters: SearchFilters = { ...filters };

  function applyFilters() {
    dispatch('apply', localFilters);
  }

  function clearFilters() {
    localFilters = {};
    dispatch('clear');
  }

  function handleCategoryChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    localFilters.category = target.value || undefined;
  }

  function handleManufacturerChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    localFilters.manufacturer = target.value || undefined;
  }

  function handleSortChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const [sortBy, sortOrder] = target.value.split('-');
    localFilters.sort_by = sortBy as any;
    localFilters.sort_order = sortOrder as 'asc' | 'desc';
  }

  $: if (visible) {
    localFilters = { ...filters };
  }
</script>

{#if visible}
  <div class="product-filters bg-base-100 border border-base-300 rounded-lg p-4 mb-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">Filters</h3>
      <Button variant="ghost" size="sm" on:click={clearFilters}>
        Clear All
      </Button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Price Range -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Price Range</span>
        </label>
        <div class="flex gap-2">
          <Input
            type="number"
            placeholder="Min"
            size="sm"
            bind:value={localFilters.min_price}
          />
          <Input
            type="number"
            placeholder="Max"
            size="sm"
            bind:value={localFilters.max_price}
          />
        </div>
      </div>

      <!-- Category -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Category</span>
        </label>
        <select
          class="select select-bordered select-sm"
          on:change={handleCategoryChange}
          value={localFilters.category || ''}
        >
          <option value="">All Categories</option>
          {#each categories as category}
            <option value={category}>{category}</option>
          {/each}
        </select>
      </div>

      <!-- Manufacturer -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Manufacturer</span>
        </label>
        <select
          class="select select-bordered select-sm"
          on:change={handleManufacturerChange}
          value={localFilters.manufacturer || ''}
        >
          <option value="">All Manufacturers</option>
          {#each manufacturers as manufacturer}
            <option value={manufacturer}>{manufacturer}</option>
          {/each}
        </select>
      </div>

      <!-- Sort By -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Sort By</span>
        </label>
        <select
          class="select select-bordered select-sm"
          on:change={handleSortChange}
          value={`${localFilters.sort_by || 'name'}-${localFilters.sort_order || 'asc'}`}
        >
          <option value="name-asc">Name (A-Z)</option>
          <option value="name-desc">Name (Z-A)</option>
          <option value="price-asc">Price (Low to High)</option>
          <option value="price-desc">Price (High to Low)</option>
          <option value="rating-desc">Rating (High to Low)</option>
          <option value="date-desc">Newest First</option>
          <option value="date-asc">Oldest First</option>
        </select>
      </div>
    </div>

    <!-- Rating Filter -->
    <div class="form-control mt-4">
      <label class="label">
        <span class="label-text">Minimum Rating</span>
      </label>
      <div class="flex gap-2 items-center">
        <input
          type="range"
          min="0"
          max="5"
          step="0.5"
          class="range range-primary range-sm"
          bind:value={localFilters.min_rating}
        />
        <span class="text-sm font-medium min-w-[3rem]">
          {localFilters.min_rating || 0}★
        </span>
      </div>
    </div>

    <!-- Apply Filters Button -->
    <div class="flex justify-end mt-6">
      <Button variant="primary" on:click={applyFilters}>
        Apply Filters
      </Button>
    </div>
  </div>
{/if}

<style>
  .product-filters {
    @apply animate-slide-up;
  }

  .select {
    @apply w-full;
  }

  .range {
    @apply flex-1;
  }

  .form-control {
    @apply w-full;
  }

  .label {
    @apply mb-1;
  }

  .label-text {
    @apply text-sm font-medium text-base-content;
  }
</style>
