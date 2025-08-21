<script lang="ts">
  export let title: string = '';
  export let subtitle: string = '';
  export let compact: boolean = false;
  export let bordered: boolean = true;
  export let shadow: boolean = true;
  export let clickable: boolean = false;
</script>

<div 
  class="card"
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
  .card {
    @apply bg-base-100 rounded-lg transition-all duration-200 ease-in-out;
  }

  .card-compact .card-body {
    @apply p-4;
  }

  .card-body {
    @apply p-6;
  }

  .card-bordered {
    @apply border border-base-300;
  }

  .card-header {
    @apply mb-4;
  }

  .card-title {
    @apply text-xl font-semibold text-base-content mb-1;
  }

  .card-subtitle {
    @apply text-sm text-base-content/70;
  }

  .card-content {
    @apply flex-1;
  }

  .card-actions {
    @apply flex gap-2 mt-4;
  }

  .cursor-pointer:hover {
    @apply transform scale-[1.02];
  }
</style>
