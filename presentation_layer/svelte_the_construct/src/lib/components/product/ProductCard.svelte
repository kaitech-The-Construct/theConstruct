<script>
  export let product;
</script>

<a href="/product/{product.id}" class="card">
  <img src={product.imageUrl} alt={product.name} />
  <div class="card-content">
    <h2>{product.name}</h2>
    <p>{product.price} {product.currency}</p>
  </div>
</a>

<style>
  .card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    transition: box-shadow 0.3s;
  }
  .card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
  .card-content {
    padding: 16px;
  }
</style>
