<script lang="ts">
  import { page } from '$app/stores';
  import { user, isAuthenticated, authStore } from '$stores/auth';
  import { cartItemCount, cartStore } from '$stores/cart';
  import Button from '$components/ui/Button.svelte';

  let mobileMenuOpen = false;

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }

  function handleLogout() {
    authStore.logout();
  }

  function openCart() {
    cartStore.openCart();
  }

  $: currentPath = $page.url.pathname;
</script>

<header class="navbar bg-base-100 shadow-lg sticky top-0 z-50">
  <div class="navbar-start">
    <!-- Mobile menu button -->
    <div class="dropdown lg:hidden">
      <button
        class="btn btn-square btn-ghost"
        on:click={toggleMobileMenu}
        aria-label="Toggle menu"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          class="inline-block w-5 h-5 stroke-current"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
      
      {#if mobileMenuOpen}
        <ul class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
          <li><a href="/marketplace" class:active={currentPath === '/marketplace'}>Marketplace</a></li>
          <li><a href="/manufacturing" class:active={currentPath === '/manufacturing'}>Manufacturing</a></li>
          <li><a href="/about" class:active={currentPath === '/about'}>About</a></li>
        </ul>
      {/if}
    </div>

    <!-- Logo -->
    <a href="/" class="btn btn-ghost text-xl font-bold">
      <span class="text-primary">The</span>
      <span class="text-secondary">Construct</span>
    </a>
  </div>

  <!-- Desktop navigation -->
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal px-1">
      <li>
        <a 
          href="/marketplace" 
          class="btn btn-ghost"
          class:btn-active={currentPath === '/marketplace'}
        >
          Marketplace
        </a>
      </li>
      <li>
        <a 
          href="/manufacturing" 
          class="btn btn-ghost"
          class:btn-active={currentPath === '/manufacturing'}
        >
          Manufacturing
        </a>
      </li>
      <li>
        <a 
          href="/about" 
          class="btn btn-ghost"
          class:btn-active={currentPath === '/about'}
        >
          About
        </a>
      </li>
    </ul>
  </div>

  <div class="navbar-end gap-2">
    <!-- Cart button -->
    <button
      class="btn btn-ghost btn-circle relative"
      on:click={openCart}
      aria-label="Shopping cart"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.8-1.8M7 13l-1.8 1.8M17 21a2 2 0 100-4 2 2 0 000 4zM9 21a2 2 0 100-4 2 2 0 000 4z"
        />
      </svg>
      {#if $cartItemCount > 0}
        <span class="badge badge-sm badge-primary absolute -top-2 -right-2">
          {$cartItemCount}
        </span>
      {/if}
    </button>

    <!-- User menu -->
    {#if $isAuthenticated}
      <div class="dropdown dropdown-end">
        <button class="btn btn-ghost btn-circle avatar" tabindex="0">
          <div class="w-8 rounded-full bg-primary text-primary-content flex items-center justify-center">
            {$user?.username?.charAt(0).toUpperCase() || 'U'}
          </div>
        </button>
        <ul class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
          <li class="menu-title">
            <span>Hello, {$user?.username}!</span>
          </li>
          <li><a href="/profile">Profile</a></li>
          <li><a href="/orders">My Orders</a></li>
          <li><a href="/settings">Settings</a></li>
          <li><hr class="my-2" /></li>
          <li>
            <button on:click={handleLogout} class="text-error">
              Logout
            </button>
          </li>
        </ul>
      </div>
    {:else}
      <div class="flex gap-2">
        <Button href="/login" variant="ghost" size="sm">
          Login
        </Button>
        <Button href="/register" variant="primary" size="sm">
          Sign Up
        </Button>
      </div>
    {/if}
  </div>
</header>

<style>
  .navbar {
    @apply px-4 lg:px-8;
  }

  .menu li > a.active,
  .btn-active {
    @apply bg-primary text-primary-content;
  }

  .avatar {
    @apply w-8 h-8;
  }

  .badge {
    @apply text-xs font-bold;
  }

  .menu-title {
    @apply text-xs font-semibold text-base-content/70 uppercase tracking-wider;
  }
</style>
