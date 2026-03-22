<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    class: className = '',
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    type = 'button',
    href = undefined,
    fullWidth = false,
    ariaLabel = undefined,
    children,
    onclick
  }: {
    class?: string;
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    loading?: boolean;
    type?: 'button' | 'submit' | 'reset';
    href?: string;
    fullWidth?: boolean;
    ariaLabel?: string;
    children?: Snippet;
    onclick?: (event: MouseEvent) => void;
  } = $props();

  function handleClick(event: MouseEvent) {
    if (!disabled && !loading && onclick) {
      onclick(event);
    }
  }

  let classes = $derived([
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
  ].filter(Boolean).join(' '));
</script>

{#if href}
  <a 
    {href}
    class={classes}
    class:btn-disabled={disabled}
    {onclick}
    role="button"
    tabindex={disabled ? -1 : 0}
    aria-label={ariaLabel}
  >
    {#if loading}
      <span class="loading loading-spinner loading-sm"></span>
    {/if}
    {@render children?.()}
  </a>
{:else}
  <button
    {type}
    {disabled}
    class={classes}
    {onclick}
    aria-label={ariaLabel}
  >
    {#if loading}
      <span class="loading loading-spinner loading-sm"></span>
    {/if}
    {@render children?.()}
  </button>
{/if}

<style>
  /* svelte-ignore css_unknown_at_rule */
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
    background-color: var(--error);
    color: var(--error-content);
  }

  .btn-error:hover:not(:disabled) {
    background-color: var(--error-focus);
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