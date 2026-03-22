<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    title = '',
    subtitle = '',
    class: className = '',
    compact = false,
    bordered = true,
    shadow = true,
    clickable = false,
    children,
    actions,
    onclick,
    onkeydown
  }: {
    title?: string;
    subtitle?: string;
    class?: string;
    compact?: boolean;
    bordered?: boolean;
    shadow?: boolean;
    clickable?: boolean;
    children?: Snippet;
    actions?: Snippet;
    onclick?: (e: MouseEvent) => void;
    onkeydown?: (e: KeyboardEvent) => void;
  } = $props();
</script>

{#snippet cardInner()}
  <div class="card-body">
    {#if title || subtitle}
      <div class="card-header">
        {#if title}
          <h2 class="card-title">{title}</h2>
        {/if}
        {#if subtitle}
          <p class="card-subtitle">{subtitle}</p>
        {/if}
      </div>
    {/if}
    
    <div class="card-content">
      {@render children?.()}
    </div>
    
    {#if actions}
      <div class="card-actions justify-end">
        {@render actions()}
      </div>
    {/if}
  </div>
{/snippet}

{#if clickable}
<button
  class="card {className} text-left w-full"
  class:card-compact={compact}
  class:card-bordered={bordered}
  class:shadow-lg={shadow}
  class:cursor-pointer={clickable}
  class:hover:shadow-xl={clickable}
  {onclick}
  {onkeydown}
  type="button"
>
  {@render cardInner()}
</button>
{:else}
<div 
  class="card {className}"
  class:card-compact={compact}
  class:card-bordered={bordered}
  class:shadow-lg={shadow}
>
  {@render cardInner()}
</div>
{/if}

<style>
  /* svelte-ignore css_unknown_at_rule */
  @reference "../../../app.css";
  .card {
    background-color: var(--base-100);
    border-radius: 0.5rem;
    transition: all 0.2s ease-in-out;
    border: none;
  }

  .card-compact .card-body {
    padding: 1rem;
  }

  .card-body {
    padding: 1.5rem;
  }

  .card-bordered {
    border: 1px solid var(--base-300);
  }

  .card-header {
    margin-bottom: 1rem;
  }

  .card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--base-content);
    margin-bottom: 0.25rem;
  }

  .card-subtitle {
    font-size: 0.875rem;
    color: rgba(var(--base-content), 0.7);
  }

  .card-content {
    flex: 1;
  }

  .card-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .cursor-pointer:hover {
    transform: scale(1.02);
  }
</style>