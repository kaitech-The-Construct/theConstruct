<script>
  import ProductCard from './ProductCard.svelte';
  import products from '$lib/data/products.json';
</script>

<div class="grid">
  {#each products as product}
    <ProductCard {product} />
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
</style>
