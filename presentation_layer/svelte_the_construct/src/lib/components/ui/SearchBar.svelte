<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import Button from './Button.svelte';

  export let value: string = '';
  export let placeholder: string = 'Search products...';
  export let loading: boolean = false;
  export let showFilters: boolean = false;

  const dispatch = createEventDispatcher();

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
    dispatch('input', { value });
  }

  function handleSearch() {
    dispatch('search', { value });
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }

  function toggleFilters() {
    showFilters = !showFilters;
    dispatch('toggle-filters', { showFilters });
  }
</script>

<div class="search-bar">
  <div class="flex gap-2">
    <div class="relative flex-1">
      <input
        type="search"
        {placeholder}
        bind:value
        on:input={handleInput}
        on:keydown={handleKeydown}
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
      on:click={handleSearch}
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
      on:click={toggleFilters}
      class="btn-square"
      aria-label="Toggle filters"
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
  .search-bar {
    @apply w-full;
  }

  .input {
    @apply transition-all duration-200 ease-in-out;
  }

  .input:focus {
    @apply ring-2 ring-primary ring-offset-2;
  }
</style>
