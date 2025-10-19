<script lang="ts">
  import { page } from '$app/stores';
  import NavBrand from './navbar/NavBrand.svelte';
  import NavMenu from './navbar/NavMenu.svelte';
  import NavActions from './navbar/NavActions.svelte';
  import MobileMenu from './navbar/MobileMenu.svelte';

  let mobileMenuOpen = false;
  let isScrolled = false;

  // Enhanced scroll detection for backdrop blur
  function handleScroll() {
    isScrolled = window.scrollY > 10;
  }

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }

  function closeMobileMenu() {
    mobileMenuOpen = false;
  }

  $: currentPath = $page.url.pathname;
</script>

<svelte:window on:scroll={handleScroll} />

<header 
  class="navbar robotic-navbar"
  class:scrolled={isScrolled}
>
  <div class="navbar-container">
    <NavBrand />
    <NavMenu {currentPath} />
    <NavActions 
      {mobileMenuOpen}
      on:toggle-mobile={toggleMobileMenu}
    />
  </div>
</header>

<MobileMenu 
  {mobileMenuOpen} 
  {currentPath}
  on:close={closeMobileMenu}
/>
