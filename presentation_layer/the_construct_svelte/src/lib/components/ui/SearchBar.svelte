<script lang="ts">
  import Button from './Button.svelte';

  let {
    value = $bindable(''),
    placeholder = 'Search products...',
    loading = false,
    showFilters = $bindable(false),
    oninput,
    onsearch,
    ontogglefilters
  }: {
    value?: string;
    placeholder?: string;
    loading?: boolean;
    showFilters?: boolean;
    oninput?: (event: { value: string }) => void;
    onsearch?: (event: { value: string }) => void;
    ontogglefilters?: (event: { showFilters: boolean }) => void;
  } = $props();

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
    if (oninput) oninput({ value });
  }

  function handleSearch() {
    if (onsearch) onsearch({ value });
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }

  function toggleFilters() {
    showFilters = !showFilters;
    if (ontogglefilters) ontogglefilters({ showFilters });
  }
</script>

<div class="search-bar">
  <div class="flex gap-2">
    <div class="relative flex-1">
      <input
        aria-label="Search Input"
        type="search"
        {placeholder}
        bind:value
        oninput={handleInput}
        onkeydown={handleKeydown}
        class="input input-bordered w-full pl-10 pr-4"
        disabled={loading}
      />
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg
          class="h-5 w-5 text-base-content/50"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
    </div>
    
    <Button
      variant="primary"
      onclick={handleSearch}
      {loading}
      disabled={loading}
    >
      {#if loading}
        <span class="loading loading-spinner loading-sm"></span>
      {:else}
        Search
      {/if}
    </Button>
    
    <Button
      variant="outline"
      onclick={toggleFilters}
      class="btn-square"
      ariaLabel="Toggle filters"
    >
      <svg
        class="h-5 w-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.121A1 1 0 013 6.414V4z"
        />
      </svg>
    </Button>
  </div>
</div>

<style>
  /* svelte-ignore css_unknown_at_rule */
  @reference "../../../app.css";
  .search-bar {
    width: 100%;
  }

  .input {
    transition: all 0.2s ease-in-out;
  }

  .input:focus {
    box-shadow: 0 0 0 2px var(--primary), 0 0 0 4px var(--base-100);
  }
</style>