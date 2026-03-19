<script lang="ts">
  export let title: string = '';
  export let subtitle: string = '';
  let className = '';
  export { className as class };
  export let compact: boolean = false;
  export let bordered: boolean = true;
  export let shadow: boolean = true;
  export let clickable: boolean = false;
</script>

<div 
  class="card {className}"
  class:card-compact={compact}
  class:card-bordered={bordered}
  class:shadow-lg={shadow}
  class:cursor-pointer={clickable}
  class:hover:shadow-xl={clickable}
  on:click
  on:keydown
  role={clickable ? 'button' : undefined}
  tabindex={clickable ? 0 : undefined}
>
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
      <slot />
    </div>
    
    {#if $$slots.actions}
      <div class="card-actions justify-end">
        <slot name="actions" />
      </div>
    {/if}
  </div>
</div>

<style>
  @reference "../../../app.css";
  .card {
    background-color: var(--base-100);
    border-radius: 0.5rem;
    transition: all 0.2s ease-in-out;
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
