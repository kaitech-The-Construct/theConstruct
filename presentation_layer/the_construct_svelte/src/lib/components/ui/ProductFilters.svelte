<script lang="ts">
  import type { SearchFilters } from '$types';
  import Button from './Button.svelte';
  import Input from './Input.svelte';

  let {
    filters = {},
    categories = ['Robots', 'Components', 'Software', 'Tools'],
    manufacturers = [],
    visible = false,
    onapply,
    onclear
  }: {
    filters?: SearchFilters;
    categories?: string[];
    manufacturers?: string[];
    visible?: boolean;
    onapply?: (filters: SearchFilters) => void;
    onclear?: () => void;
  } = $props();

  let localFilters = $state<SearchFilters>({ ...filters });

  function applyFilters() {
    if (onapply) onapply(localFilters);
  }

  function clearFilters() {
    localFilters = {};
    if (onclear) onclear();
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

  $effect(() => {
    if (visible) {
      localFilters = { ...filters };
    }
  });
</script>

{#if visible}
  <div class="product-filters bg-base-100 border border-base-300 rounded-lg p-4 mb-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">Filters</h3>
      <Button variant="ghost" size="sm" onclick={clearFilters}>
        Clear All
      </Button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Price Range -->
      <div class="form-control">
        <label class="label" for="min-price">
          <span class="label-text">Price Range</span>
        </label>
        <div class="flex gap-2">
          <Input
            id="min-price"
            type="number"
            placeholder="Min"
            size="sm"
            bind:value={localFilters.min_price}
          />
          <Input
            id="max-price"
            type="number"
            placeholder="Max"
            size="sm"
            bind:value={localFilters.max_price}
          />
        </div>
      </div>

      <!-- Category -->
      <div class="form-control">
        <label class="label" for="category-select">
          <span class="label-text">Category</span>
        </label>
        <select
          id="category-select"
          class="select select-bordered select-sm"
          onchange={handleCategoryChange}
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
        <label class="label" for="manufacturer-select">
          <span class="label-text">Manufacturer</span>
        </label>
        <select
          id="manufacturer-select"
          class="select select-bordered select-sm"
          onchange={handleManufacturerChange}
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
        <label class="label" for="sort-select">
          <span class="label-text">Sort By</span>
        </label>
        <select
          id="sort-select"
          class="select select-bordered select-sm"
          onchange={handleSortChange}
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
      <label class="label" for="min-rating">
        <span class="label-text">Minimum Rating</span>
      </label>
      <div class="flex gap-2 items-center">
        <input
          id="min-rating"
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
      <Button variant="primary" onclick={applyFilters}>
        Apply Filters
      </Button>
    </div>
  </div>
{/if}

<style>
  /* svelte-ignore css_unknown_at_rule */
  @reference "../../../app.css";
  .product-filters {
    animation: slideUp 0.3s ease-out;
  }

  .select {
    width: 100%;
  }

  .range {
    flex: 1 1 0%;
  }

  .form-control {
    width: 100%;
  }

  .label {
    margin-bottom: 0.25rem;
  }

  .label-text {
    font-size: 0.875rem;
    line-height: 1.25rem;
    font-weight: 500;
    color: var(--base-content);
  }
</style>