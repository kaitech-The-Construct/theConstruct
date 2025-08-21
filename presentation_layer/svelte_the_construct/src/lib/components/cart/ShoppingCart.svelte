<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { cartItems, cartTotal, isCartOpen, cartStore } from '$stores/cart';
  import Button from '$components/ui/Button.svelte';
  import Input from '$components/ui/Input.svelte';

  const dispatch = createEventDispatcher();

  function handleUpdateQuantity(productId: string, quantity: number) {
    cartStore.updateQuantity(productId, quantity);
  }

  function handleRemoveItem(productId: string) {
    cartStore.removeItem(productId);
  }

  function handleClearCart() {
    cartStore.clearCart();
  }

  function handleCheckout() {
    dispatch('checkout');
    cartStore.closeCart();
  }

  function handleClose() {
    cartStore.closeCart();
  }

  function handleContinueShopping() {
    cartStore.closeCart();
    dispatch('continue-shopping');
  }

  $: formattedTotal = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format($cartTotal);
</script>

<!-- Cart Drawer/Modal -->
{#if $isCartOpen}
  <div class="cart-overlay fixed inset-0 z-50 flex">
    <!-- Backdrop -->
    <div 
      class="fixed inset-0 bg-black/50 transition-opacity"
      on:click={handleClose}
      on:keydown={(e) => e.key === 'Escape' && handleClose()}
    ></div>
    
    <!-- Cart Panel -->
    <div class="cart-panel ml-auto bg-base-100 w-full max-w-md h-full shadow-xl flex flex-col animate-slide-in-right">
      <!-- Header -->
      <div class="cart-header flex justify-between items-center p-6 border-b border-base-300">
        <h2 class="text-xl font-semibold">Shopping Cart</h2>
        <button 
          class="btn btn-ghost btn-circle btn-sm"
          on:click={handleClose}
          aria-label="Close cart"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Cart Items -->
      <div class="cart-items flex-1 overflow-y-auto p-6">
        {#if $cartItems.length === 0}
          <!-- Empty Cart -->
          <div class="empty-cart text-center py-12">
            <div class="w-16 h-16 bg-base-200 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.8-1.8M7 13l-1.8 1.8M17 21a2 2 0 100-4 2 2 0 000 4zM9 21a2 2 0 100-4 2 2 0 000 4z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold mb-2">Your cart is empty</h3>
            <p class="text-base-content/70 mb-6">
              Add some products to get started!
            </p>
            <Button variant="primary" on:click={handleContinueShopping}>
              Continue Shopping
            </Button>
          </div>
        {:else}
          <!-- Cart Items List -->
          <div class="space-y-4">
            {#each $cartItems as item (item.product_id)}
              <div class="cart-item flex gap-4 p-4 bg-base-200 rounded-lg">
                <!-- Product Image -->
                <div class="w-16 h-16 bg-base-300 rounded-lg flex-shrink-0 overflow-hidden">
                  {#if item.product.images && item.product.images.length > 0}
                    <img 
                      src={item.product.images[0]} 
                      alt={item.product.name}
                      class="w-full h-full object-cover"
                    />
                  {:else}
                    <div class="w-full h-full flex items-center justify-center">
                      <svg class="w-6 h-6 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                    </div>
                  {/if}
                </div>

                <!-- Product Info -->
                <div class="flex-1 min-w-0">
                  <h4 class="font-medium text-sm mb-1 truncate">
                    {item.product.name}
                  </h4>
                  <p class="text-xs text-base-content/70 mb-2">
                    by {item.product.manufacturer}
                  </p>
                  
                  <!-- Quantity Controls -->
                  <div class="flex items-center gap-2">
                    <button
                      class="btn btn-circle btn-xs"
                      on:click={() => handleUpdateQuantity(item.product_id, item.quantity - 1)}
                      disabled={item.quantity <= 1}
                    >
                      -
                    </button>
                    <span class="text-sm font-medium min-w-[2rem] text-center">
                      {item.quantity}
                    </span>
                    <button
                      class="btn btn-circle btn-xs"
                      on:click={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}
                    >
                      +
                    </button>
                  </div>
                </div>

                <!-- Price and Remove -->
                <div class="flex flex-col items-end justify-between">
                  <button
                    class="btn btn-ghost btn-xs text-error"
                    on:click={() => handleRemoveItem(item.product_id)}
                    aria-label="Remove item"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                  <div class="text-right">
                    <div class="text-sm font-semibold">
                      ${(item.price * item.quantity).toFixed(2)}
                    </div>
                    <div class="text-xs text-base-content/70">
                      ${item.price.toFixed(2)} each
                    </div>
                  </div>
                </div>
              </div>
            {/each}
          </div>

          <!-- Clear Cart Button -->
          {#if $cartItems.length > 0}
            <div class="mt-6 text-center">
              <Button variant="ghost" size="sm" on:click={handleClearCart}>
                Clear Cart
              </Button>
            </div>
          {/if}
        {/if}
      </div>

      <!-- Cart Footer -->
      {#if $cartItems.length > 0}
        <div class="cart-footer border-t border-base-300 p-6">
          <!-- Total -->
          <div class="flex justify-between items-center mb-4">
            <span class="text-lg font-semibold">Total:</span>
            <span class="text-2xl font-bold text-primary">
              {formattedTotal}
            </span>
          </div>

          <!-- Actions -->
          <div class="space-y-3">
            <Button 
              variant="primary" 
              size="lg" 
              fullWidth
              on:click={handleCheckout}
            >
              Proceed to Checkout
            </Button>
            <Button 
              variant="outline" 
              size="md" 
              fullWidth
              on:click={handleContinueShopping}
            >
              Continue Shopping
            </Button>
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .cart-overlay {
    @apply backdrop-blur-sm;
  }

  .cart-panel {
    @apply transform transition-transform duration-300 ease-in-out;
  }

  .animate-slide-in-right {
    animation: slideInRight 0.3s ease-out;
  }

  @keyframes slideInRight {
    from {
      transform: translateX(100%);
    }
    to {
      transform: translateX(0);
    }
  }

  .cart-item {
    @apply transition-all duration-200 hover:bg-base-300/50;
  }

  .empty-cart {
    @apply flex flex-col items-center justify-center h-full;
  }

  .btn-xs {
    @apply w-6 h-6 min-h-0 text-xs;
  }

  .truncate {
    @apply overflow-hidden text-ellipsis whitespace-nowrap;
  }
</style>
