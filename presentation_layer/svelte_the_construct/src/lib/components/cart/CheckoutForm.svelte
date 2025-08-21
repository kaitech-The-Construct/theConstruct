<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { cartItems, cartTotal } from '$stores/cart';
  import { user } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Input from '$components/ui/Input.svelte';
  import Card from '$components/ui/Card.svelte';

  const dispatch = createEventDispatcher();

  let shippingInfo = {
    fullName: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    country: '',
  };

  let billingInfo = {
    sameAsShipping: true,
    fullName: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    country: '',
  };

  let paymentMethod = 'crypto';
  let loading = false;
  let errors: Record<string, string> = {};

  function validateForm() {
    errors = {};
    if (!shippingInfo.fullName) errors.shippingFullName = 'Full name is required';
    if (!shippingInfo.address) errors.shippingAddress = 'Address is required';
    if (!shippingInfo.city) errors.shippingCity = 'City is required';
    if (!shippingInfo.zip) errors.shippingZip = 'ZIP code is required';
    if (!shippingInfo.country) errors.shippingCountry = 'Country is required';

    if (!billingInfo.sameAsShipping) {
      if (!billingInfo.fullName) errors.billingFullName = 'Full name is required';
      if (!billingInfo.address) errors.billingAddress = 'Address is required';
      if (!billingInfo.city) errors.billingCity = 'City is required';
      if (!billingInfo.zip) errors.billingZip = 'ZIP code is required';
      if (!billingInfo.country) errors.billingCountry = 'Country is required';
    }

    return Object.keys(errors).length === 0;
  }

  async function handleSubmit() {
    if (!validateForm()) {
      return;
    }

    loading = true;
    try {
      const orderData = {
        shipping: shippingInfo,
        billing: billingInfo.sameAsShipping ? shippingInfo : billingInfo,
        payment: {
          method: paymentMethod,
        },
        items: $cartItems,
        total: $cartTotal,
        user: $user,
      };
      
      dispatch('submit', orderData);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // On success, dispatch a success event
      dispatch('success', { orderId: `ORD-${Math.random().toString(36).substr(2, 9).toUpperCase()}` });
      
    } catch (error) {
      console.error('Checkout failed:', error);
      dispatch('error', { message: 'Checkout failed. Please try again.' });
    } finally {
      loading = false;
    }
  }

  $: if (billingInfo.sameAsShipping) {
    billingInfo = { ...billingInfo, ...shippingInfo };
  }
</script>

<div class="checkout-form">
  <form on:submit|preventDefault={handleSubmit}>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Shipping and Payment -->
      <div>
        <!-- Shipping Information -->
        <Card title="Shipping Information" class="mb-6">
          <div class="space-y-4">
            <Input
              label="Full Name"
              bind:value={shippingInfo.fullName}
              error={errors.shippingFullName}
              required
            />
            <Input
              label="Address"
              bind:value={shippingInfo.address}
              error={errors.shippingAddress}
              required
            />
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="City"
                bind:value={shippingInfo.city}
                error={errors.shippingCity}
                required
              />
              <Input
                label="State / Province"
                bind:value={shippingInfo.state}
              />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="ZIP / Postal Code"
                bind:value={shippingInfo.zip}
                error={errors.shippingZip}
                required
              />
              <Input
                label="Country"
                bind:value={shippingInfo.country}
                error={errors.shippingCountry}
                required
              />
            </div>
          </div>
        </Card>

        <!-- Billing Information -->
        <Card title="Billing Information" class="mb-6">
          <div class="form-control">
            <label class="label cursor-pointer">
              <span class="label-text">Same as shipping address</span>
              <input
                type="checkbox"
                class="checkbox checkbox-primary"
                bind:checked={billingInfo.sameAsShipping}
              />
            </label>
          </div>

          {#if !billingInfo.sameAsShipping}
            <div class="space-y-4 mt-4">
              <Input
                label="Full Name"
                bind:value={billingInfo.fullName}
                error={errors.billingFullName}
                required
              />
              <Input
                label="Address"
                bind:value={billingInfo.address}
                error={errors.billingAddress}
                required
              />
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="City"
                  bind:value={billingInfo.city}
                  error={errors.billingCity}
                  required
                />
                <Input
                  label="State / Province"
                  bind:value={billingInfo.state}
                />
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="ZIP / Postal Code"
                  bind:value={billingInfo.zip}
                  error={errors.billingZip}
                  required
                />
                <Input
                  label="Country"
                  bind:value={billingInfo.country}
                  error={errors.billingCountry}
                  required
                />
              </div>
            </div>
          {/if}
        </Card>

        <!-- Payment Method -->
        <Card title="Payment Method">
          <div class="space-y-4">
            <div 
              class="payment-option"
              class:active={paymentMethod === 'crypto'}
              on:click={() => paymentMethod = 'crypto'}
            >
              <input type="radio" name="paymentMethod" value="crypto" bind:group={paymentMethod} class="radio radio-primary" />
              <div class="flex-1">
                <div class="font-medium">Cryptocurrency</div>
                <div class="text-sm text-base-content/70">Pay with XRPL, Solana, or other supported cryptocurrencies.</div>
              </div>
            </div>
            <div 
              class="payment-option"
              class:active={paymentMethod === 'card'}
              on:click={() => paymentMethod = 'card'}
            >
              <input type="radio" name="paymentMethod" value="card" bind:group={paymentMethod} class="radio radio-primary" />
              <div class="flex-1">
                <div class="font-medium">Credit Card</div>
                <div class="text-sm text-base-content/70">Secure payment with Stripe.</div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Order Summary -->
      <div>
        <Card title="Order Summary">
          <div class="space-y-4">
            {#each $cartItems as item}
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 bg-base-200 rounded-lg overflow-hidden">
                    <img src={item.product.images[0]} alt={item.product.name} class="w-full h-full object-cover" />
                  </div>
                  <div>
                    <div class="font-medium">{item.product.name}</div>
                    <div class="text-sm text-base-content/70">
                      Qty: {item.quantity}
                    </div>
                  </div>
                </div>
                <div class="font-medium">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            {/each}
          </div>

          <div class="divider"></div>

          <div class="space-y-2">
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span>${$cartTotal.toFixed(2)}</span>
            </div>
            <div class="flex justify-between">
              <span>Shipping</span>
              <span>Free</span>
            </div>
            <div class="flex justify-between">
              <span>Taxes</span>
              <span>Calculated at next step</span>
            </div>
          </div>

          <div class="divider"></div>

          <div class="flex justify-between font-bold text-lg">
            <span>Total</span>
            <span>${$cartTotal.toFixed(2)}</span>
          </div>

          <div class="mt-6">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              {loading}
            >
              {#if loading}
                Processing...
              {:else}
                Place Order
              {/if}
            </Button>
          </div>
        </Card>
      </div>
    </div>
  </form>
</div>

<style>
  .payment-option {
    @apply flex items-center gap-4 p-4 border border-base-300 rounded-lg cursor-pointer
           transition-all duration-200;
  }

  .payment-option.active {
    @apply border-primary ring-2 ring-primary;
  }

  .payment-option:hover {
    @apply border-primary/50;
  }

  .divider {
    @apply my-4 border-t border-base-300;
  }
</style>
