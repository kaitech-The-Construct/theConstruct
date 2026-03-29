<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$stores/auth.svelte';
  import { cartStore } from '$stores/cart';
  import { notificationStore } from '$stores/notifications.svelte';
  import Header from '$components/layout/Header.svelte';
  import ShoppingCart from '$components/cart/ShoppingCart.svelte';
  import '../app.css';

  // Initialize stores on app load
  onMount(() => {
    authStore.init();
    cartStore.init();
    notificationStore.init();
  });

  function handleCheckout() {
    goto('/checkout');
  }

  function handleContinueShopping() {
    goto('/marketplace');
  }
</script>

<div class="min-h-screen bg-base-200">
  <Header />
  
  <main class="container mx-auto px-4 py-8">
    <slot />
  </main>
  
  <footer class="footer footer-center p-10 bg-base-300 text-base-content">
    <div>
      <div class="grid grid-flow-col gap-4">
        <a href="/about" class="link link-hover">About</a>
        <a href="/contact" class="link link-hover">Contact</a>
        <a href="/privacy" class="link link-hover">Privacy</a>
        <a href="/terms" class="link link-hover">Terms</a>
      </div>
      <div>
        <p class="font-bold">
          <span class="text-primary">The</span>
          <span class="text-secondary">Construct</span>
        </p>
        <p>Decentralized Robotics Exchange Platform</p>
      </div>
      <div>
        <p>Copyright © 2025 - All rights reserved</p>
      </div>
    </div>
  </footer>
</div>

<!-- Shopping Cart Component -->
<ShoppingCart 
  on:checkout={handleCheckout}
  on:continue-shopping={handleContinueShopping}
/>

<style>
  @reference "../app.css";
  :global(html) {
    scroll-behavior: smooth;
  }

  :global(body) {
    font-family: system-ui, -apple-system, sans-serif;
  }

  .container {
    max-width: 80rem;
  }

  .footer {
    margin-top: auto;
  }
</style>
