<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  let className = '';
  export { className as class };
  export let variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let disabled: boolean = false;
  export let loading: boolean = false;
  export let type: 'button' | 'submit' | 'reset' = 'button';
  export let href: string | undefined = undefined;
  export let fullWidth: boolean = false;
  export let ariaLabel: string | undefined = undefined;

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
    'transition-all duration-200 ease-in-out',
    className
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
    aria-label={ariaLabel}
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
    aria-label={ariaLabel}
  >
    {#if loading}
      <span class="loading loading-spinner loading-sm"></span>
    {/if}
    <slot />
  </button>
{/if}

<style>
  @reference "../../../app.css";
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    border-radius: 0.375rem;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
    border: none;
    cursor: pointer;
  }

  .btn:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--primary);
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }

  .btn-md {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }

  .btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
  }

  .btn-primary {
<<<<<<< HEAD:presentation_layer/svelte_the_construct/src/lib/components/ui/Button.svelte
    @apply bg-primary text-primary-content hover:bg-primary 
           focus:ring-primary;
  }

  .btn-secondary {
    @apply bg-secondary text-secondary-content hover:bg-secondary 
           focus:ring-secondary;
=======
    background-color: var(--primary);
    color: var(--primary-content);
  }

  .btn-primary:hover:not(:disabled) {
    background-color: var(--primary-focus);
  }

  .btn-secondary {
    background-color: var(--secondary);
    color: var(--secondary-content);
  }

  .btn-secondary:hover:not(:disabled) {
    background-color: var(--secondary-focus);
>>>>>>> f7d49693536da70b91928faf93cf1c603f102fd0:presentation_layer/the_construct_svelte/src/lib/components/ui/Button.svelte
  }

  .btn-outline {
    border: 2px solid var(--primary);
    color: var(--primary);
    background-color: transparent;
  }

  .btn-outline:hover:not(:disabled) {
    background-color: var(--primary);
    color: var(--primary-content);
  }

  .btn-ghost {
    color: var(--primary);
    background-color: transparent;
  }

  .btn-ghost:hover:not(:disabled) {
    background-color: rgba(59, 130, 246, 0.1);
  }

  .btn-error {
<<<<<<< HEAD:presentation_layer/svelte_the_construct/src/lib/components/ui/Button.svelte
    @apply bg-error text-error-content hover:bg-error 
           focus:ring-error;
=======
    background-color: var(--error);
    color: var(--error-content);
  }

  .btn-error:hover:not(:disabled) {
    background-color: var(--error-focus);
>>>>>>> f7d49693536da70b91928faf93cf1c603f102fd0:presentation_layer/the_construct_svelte/src/lib/components/ui/Button.svelte
  }

  .btn-block {
    width: 100%;
  }

  .btn-disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }
</style>
