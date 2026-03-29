<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { authStore } from '$stores/auth.svelte';
  import { cartItemCount, cartStore } from '$stores/cart';
  import Button from '$components/ui/Button.svelte';

  export let mobileMenuOpen: boolean;

  const dispatch = createEventDispatcher();

  function handleLogout() {
    authStore.logout();
  }

  function openCart() {
    cartStore.openCart();
  }

  function toggleMobileMenu() {
    dispatch('toggle-mobile');
  }
</script>

<div class="flex items-center gap-2">
  <!-- Cart button -->
  <button
    class="cart-button"
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
      <span class="cart-badge">
        {$cartItemCount}
      </span>
    {/if}
  </button>

  <!-- User menu -->
  {#if authStore.isAuthenticated}
    <div class="dropdown dropdown-end">
      <button class="user-avatar" tabindex="0">
        {authStore.user?.username?.charAt(0).toUpperCase() || 'U'}
      </button>
      <ul class="dropdown-menu menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
        <li class="menu-title">
          <span>Hello, {authStore.user?.username}!</span>
        </li>
        <li><a href="/profile">Profile</a></li>
        <li><a href="/orders">My Orders</a></li>
        <li><a href="/settings">Settings</a></li>
        <li><hr class="dropdown-divider" /></li>
        <li>
          <button on:click={handleLogout} class="text-error dropdown-item">
            Logout
          </button>
        </li>
      </ul>
    </div>
  {:else}
    <div class="hidden md:flex items-center gap-2">
      <Button href="/login" variant="ghost" size="sm">
        Login
      </Button>
      <Button href="/register" variant="primary" size="sm">
        Sign Up
      </Button>
    </div>
  {/if}

  <!-- Mobile menu button -->
  <button
    class="mobile-menu-button"
    class:active={mobileMenuOpen}
    on:click={toggleMobileMenu}
    aria-label="Toggle menu"
    aria-expanded={mobileMenuOpen}
    aria-controls="mobile-menu"
  >
    <div class="hamburger-icon" class:active={mobileMenuOpen}>
      <span></span>
      <span></span>
      <span></span>
    </div>
  </button>
</div>
