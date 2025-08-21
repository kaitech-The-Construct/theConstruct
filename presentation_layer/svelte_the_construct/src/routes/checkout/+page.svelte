<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { cartItems, cartTotal, cartStore } from '$stores/cart';
  import { isAuthenticated, user } from '$stores/auth';
  import CheckoutForm from '$components/cart/CheckoutForm.svelte';
  import Button from '$components/ui/Button.svelte';

  let orderPlaced = false;
  let orderId: string | null = null;

  onMount(() => {
    if (!$isAuthenticated) {
      goto('/login?redirect=/checkout');
    }
    if ($cartItems.length === 0) {
      goto('/marketplace');
    }
  });

  function handleOrderSuccess(event: CustomEvent) {
    orderPlaced = true;
    orderId = event.detail.orderId;
    cartStore.clearCart();
  }

  function handleOrderError(event: CustomEvent) {
    // Show error notification
    console.error('Order failed:', event.detail.message);
  }
</script>

<svelte:head>
  <title>Checkout - The Construct</title>
  <meta name="description" content="Complete your purchase on The Construct." />
</svelte:head>

<div class="checkout-page max-w-5xl mx-auto">
  {#if orderPlaced}
    <!-- Order Confirmation -->
    <div class="order-confirmation text-center py-12">
      <div class="w-24 h-24 bg-success/10 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-12 h-12 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h1 class="text-3xl font-bold mb-4">Thank you for your order!</h1>
      <p class="text-lg text-base-content/70 mb-6">
        Your order has been placed successfully. Your order ID is:
        <span class="font-semibold text-primary">{orderId}</span>
      </p>
      <p class="mb-8">
        You will receive an email confirmation shortly.
      </p>
      <div class="flex gap-4 justify-center">
        <Button href="/marketplace" variant="primary" size="lg">
          Continue Shopping
        </Button>
        <Button href="/orders" variant="outline" size="lg">
          View My Orders
        </Button>
      </div>
    </div>
  {:else}
    <!-- Checkout Form -->
    <div>
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold mb-4">Checkout</h1>
        <p class="text-lg text-base-content/70">
          Please review your order and provide your shipping and payment information.
        </p>
      </div>
      
      <CheckoutForm 
        on:success={handleOrderSuccess}
        on:error={handleOrderError}
      />
    </div>
  {/if}
</div>

<style>
  .checkout-page {
    @apply animate-fade-in;
  }

  .order-confirmation {
    @apply animate-fade-in;
  }
</style>
