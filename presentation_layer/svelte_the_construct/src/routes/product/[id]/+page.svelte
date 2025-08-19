<script>
  import { userStore } from '$lib/stores/userStore';
  import { createEscrow } from '$lib/services/xrplClient';
  import { goto } from '$app/navigation';
  
  /** @type {import('./$types').PageData} */
  export let data;
  const { product } = data;

  let transactionStatus = '';

  async function handleBuy() {
    if (!$userStore.isConnected) {
      alert('Please connect your wallet first.');
      return;
    }
    transactionStatus = 'Submitting...';
    try {
      const newOrder = await createEscrow(product.id, product.price);
      transactionStatus = 'Success! Redirecting to your orders...';
      // In a real app, the new order would be added to a global store
      // or fetched again on the orders page. For now, we just navigate.
      setTimeout(() => {
        goto('/account/orders');
      }, 2000);
    } catch (error) {
      transactionStatus = `Failed: ${error.message}`;
    }
  }
</script>

<div class="product-detail">
  <img src={product.imageUrl} alt={product.name} />
  <div class="info">
    <h1>{product.name}</h1>
    <p class="description">{product.description}</p>
    <p class="price">{product.price} {product.currency}</p>
    <button on:click={handleBuy} disabled={!$userStore.isConnected || transactionStatus === 'Submitting...'}>
      Buy Now
    </button>
    {#if transactionStatus}
      <p class="status">{transactionStatus}</p>
    {/if}
  </div>
</div>

<style>
  .product-detail {
    display: flex;
    gap: 2rem;
    margin-top: 2rem;
  }
  img {
    max-width: 50%;
    border-radius: 8px;
  }
  .info {
    flex-grow: 1;
  }
  .price {
    font-size: 1.5rem;
    font-weight: bold;
    color: #007bff;
  }
  button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .status {
    margin-top: 1rem;
    font-weight: bold;
  }
</style>
