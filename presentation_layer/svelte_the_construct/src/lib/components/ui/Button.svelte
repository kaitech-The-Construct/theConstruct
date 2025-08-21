<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let disabled: boolean = false;
  export let loading: boolean = false;
  export let type: 'button' | 'submit' | 'reset' = 'button';
  export let href: string | undefined = undefined;
  export let fullWidth: boolean = false;

  const dispatch = createEventDispatcher();

  function handleClick(event: MouseEvent) {
    if (!disabled && !loading) {
      dispatch('click', event);
    }
  }

  $: classes = [
    'btn',
    `btn-${size}`,
    variant === 'primary' && 'btn-primary',
    variant === 'secondary' && 'btn-secondary',
    variant === 'outline' && 'btn-outline',
    variant === 'ghost' && 'btn-ghost',
    variant === 'danger' && 'btn-error',
    fullWidth && 'btn-block',
    loading && 'loading',
    'transition-all duration-200 ease-in-out'
  ].filter(Boolean).join(' ');
</script>

{#if href}
  <a 
    {href}
    class={classes}
    class:btn-disabled={disabled}
    on:click={handleClick}
    role="button"
    tabindex={disabled ? -1 : 0}
  >
    {#if loading}
      <span class="loading loading-spinner loading-sm"></span>
    {/if}
    <slot />
  </a>
{:else}
  <button
    {type}
    {disabled}
    class={classes}
    on:click={handleClick}
  >
    {#if loading}
      <span class="loading loading-spinner loading-sm"></span>
    {/if}
    <slot />
  </button>
{/if}

<style>
  .btn {
    @apply inline-flex items-center justify-center gap-2 rounded-md font-medium 
           focus:outline-none focus:ring-2 focus:ring-offset-2 
           disabled:opacity-50 disabled:cursor-not-allowed;
  }

  .btn-sm {
    @apply px-3 py-1.5 text-sm;
  }

  .btn-md {
    @apply px-4 py-2 text-base;
  }

  .btn-lg {
    @apply px-6 py-3 text-lg;
  }

  .btn-primary {
    @apply bg-primary text-primary-content hover:bg-primary-focus 
           focus:ring-primary;
  }

  .btn-secondary {
    @apply bg-secondary text-secondary-content hover:bg-secondary-focus 
           focus:ring-secondary;
  }

  .btn-outline {
    @apply border-2 border-primary text-primary bg-transparent 
           hover:bg-primary hover:text-primary-content 
           focus:ring-primary;
  }

  .btn-ghost {
    @apply text-primary bg-transparent hover:bg-primary/10 
           focus:ring-primary;
  }

  .btn-error {
    @apply bg-error text-error-content hover:bg-error-focus 
           focus:ring-error;
  }

  .btn-block {
    @apply w-full;
  }

  .btn-disabled {
    @apply opacity-50 cursor-not-allowed pointer-events-none;
  }
</style>
