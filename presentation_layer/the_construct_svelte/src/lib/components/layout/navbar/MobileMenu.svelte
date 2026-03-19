<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  
  export let mobileMenuOpen: boolean;
  export let currentPath: string;
  
  const dispatch = createEventDispatcher();
  
  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/marketplace', label: 'Marketplace' },
    { href: '/manufacturing', label: 'Manufacturing' },
    { href: '/about', label: 'About' }
  ];
  
  function handleClose() {
    dispatch('close');
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      handleClose();
    }
  }
  
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      handleClose();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if mobileMenuOpen}
  <div 
    class="mobile-menu-overlay open"
    transition:fade={{ duration: 300 }}
    on:click={handleBackdropClick}
    role="dialog"
    aria-modal="true"
    aria-label="Mobile navigation menu"
  >
    <div 
      class="mobile-menu-content"
      transition:fly={{ y: 20, duration: 300, delay: 100 }}
    >
      <nav role="navigation" aria-label="Mobile navigation">
        {#each navItems as item}
          <a 
            href={item.href}
            class="mobile-nav-item"
            class:active={currentPath === item.href}
            on:click={handleClose}
            aria-current={currentPath === item.href ? 'page' : undefined}
          >
            {item.label}
          </a>
        {/each}
      </nav>
      
      <button 
        class="mobile-menu-close"
        on:click={handleClose}
        aria-label="Close mobile menu"
      >
        ✕
      </button>
    </div>
  </div>
{/if}

<style>
  .mobile-menu-close {
    position: absolute;
    top: 2rem;
    right: 2rem;
    width: 3rem;
    height: 3rem;
    background: transparent;
    border: 1px solid var(--robotic-border);
    border-radius: 50%;
    color: var(--base-content);
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .mobile-menu-close:hover {
    border-color: var(--robotic-glow);
    color: var(--robotic-glow);
    box-shadow: 0 0 15px var(--robotic-shadow);
  }
</style>
