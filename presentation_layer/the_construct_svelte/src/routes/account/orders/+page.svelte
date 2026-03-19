<script>
  import { onMount } from 'svelte';
  import { finishEscrow, cancelEscrow } from '$lib/services/xrplClient';
  import allOrders from '$lib/data/orders.json';
  import products from '$lib/data/products.json';

  let orders = [];

  onMount(() => {
    // In a real app, you'd fetch orders for the logged-in user
    orders = allOrders.map(order => {
      const product = products.find(p => p.id === order.productId);
      return { ...order, productName: product ? product.name : 'Unknown Product' };
    });
  });

  async function handleFinish(orderId) {
    await finishEscrow(orderId);
    orders = orders.map(o => o.id === orderId ? { ...o, status: 'Completed' } : o);
  }

  async function handleCancel(orderId) {
    await cancelEscrow(orderId);
    orders = orders.map(o => o.id === orderId ? { ...o, status: 'Canceled' } : o);
  }
</script>

<h1>My Orders</h1>

<div class="order-list">
  {#each orders as order (order.id)}
    <div class="order-item">
      <div class="order-details">
        <h3>{order.productName}</h3>
        <p>Order ID: {order.id}</p>
        <p>Status: <span class="status-{order.status.toLowerCase()}">{order.status}</span></p>
        <p>Date: {new Date(order.date).toLocaleDateString()}</p>
      </div>
      <div class="order-actions">
        {#if order.status === 'In Escrow'}
          <button class="confirm" on:click={() => handleFinish(order.id)}>Confirm Receipt</button>
          <button class="cancel" on:click={() => handleCancel(order.id)}>Cancel Order</button>
        {/if}
      </div>
    </div>
  {/each}
</div>

<style>
  .order-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  .order-item {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .status-in-escrow { color: #ffc107; }
  .status-completed { color: #28a745; }
  .status-canceled { color: #dc3545; }
  .order-actions {
    display: flex;
    gap: 1rem;
  }
  button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    color: white;
  }
  .confirm { background-color: #28a745; }
  .cancel { background-color: #dc3545; }
</style>
