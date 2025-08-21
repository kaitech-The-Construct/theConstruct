<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { productStore, currentProduct, isLoading } from '$stores/products';
  import { cartStore } from '$stores/cart';
  import { isAuthenticated } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';
  import Input from '$components/ui/Input.svelte';

  let selectedImageIndex = 0;
  let quantity = 1;
  let showSpecifications = true;
  let showReviews = false;

  $: productId = $page.params.id;
  $: product = $currentProduct;
  $: isAvailable = product?.inventory?.available > 0;
  $: maxQuantity = product?.inventory?.available || 1;

  onMount(async () => {
    if (productId) {
      try {
        await productStore.loadProduct(productId);
      } catch (error) {
        console.error('Failed to load product:', error);
        goto('/marketplace');
      }
    }
  });

  function handleAddToCart() {
    if (product) {
      cartStore.addItem(product, quantity);
      // Show success notification
      console.log(`Added ${quantity} ${product.name} to cart`);
    }
  }

  function handleBuyNow() {
    if (product) {
      cartStore.addItem(product, quantity);
      goto('/checkout');
    }
  }

  function selectImage(index: number) {
    selectedImageIndex = index;
  }

  function toggleSpecifications() {
    showSpecifications = !showSpecifications;
  }

  function toggleReviews() {
    showReviews = !showReviews;
  }

  $: formattedPrice = product ? new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(product.price) : '';
</script>

<svelte:head>
  <title>{product?.name || 'Product'} - The Construct</title>
  <meta name="description" content={product?.description || 'Product details'} />
</svelte:head>

{#if $isLoading}
  <!-- Loading State -->
  <div class="product-detail-loading">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="animate-pulse">
        <div class="aspect-square bg-base-300 rounded-lg mb-4"></div>
        <div class="flex gap-2">
          {#each Array(4) as _}
            <div class="w-16 h-16 bg-base-300 rounded"></div>
          {/each}
        </div>
      </div>
      <div class="animate-pulse space-y-4">
        <div class="h-8 bg-base-300 rounded w-3/4"></div>
        <div class="h-4 bg-base-300 rounded w-1/2"></div>
        <div class="h-6 bg-base-300 rounded w-1/4"></div>
        <div class="h-20 bg-base-300 rounded"></div>
        <div class="h-12 bg-base-300 rounded"></div>
      </div>
    </div>
  </div>
{:else if product}
  <div class="product-detail max-w-7xl mx-auto">
    <!-- Breadcrumb -->
    <nav class="breadcrumbs text-sm mb-6">
      <ul>
        <li><a href="/" class="link">Home</a></li>
        <li><a href="/marketplace" class="link">Marketplace</a></li>
        <li><span class="text-base-content/70">{product.category}</span></li>
        <li><span class="text-base-content/70">{product.name}</span></li>
      </ul>
    </nav>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Product Images -->
      <div class="product-images">
        <!-- Main Image -->
        <div class="main-image mb-4">
          <div class="aspect-square bg-base-200 rounded-lg overflow-hidden">
            {#if product.images && product.images.length > 0}
              <img 
                src={product.images[selectedImageIndex]} 
                alt={product.name}
                class="w-full h-full object-cover"
              />
            {:else}
              <div class="w-full h-full flex items-center justify-center">
                <svg class="w-24 h-24 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
            {/if}
          </div>
        </div>

        <!-- Thumbnail Images -->
        {#if product.images && product.images.length > 1}
          <div class="thumbnails flex gap-2 overflow-x-auto">
            {#each product.images as image, index}
              <button
                class="thumbnail w-16 h-16 bg-base-200 rounded border-2 overflow-hidden flex-shrink-0"
                class:border-primary={index === selectedImageIndex}
                class:border-base-300={index !== selectedImageIndex}
                on:click={() => selectImage(index)}
              >
                <img 
                  src={image} 
                  alt="{product.name} - Image {index + 1}"
                  class="w-full h-full object-cover"
                />
              </button>
            {/each}
          </div>
        {/if}
      </div>

      <!-- Product Info -->
      <div class="product-info">
        <!-- Category Badge -->
        <div class="mb-4">
          <span class="badge badge-outline">{product.category}</span>
        </div>

        <!-- Product Name -->
        <h1 class="text-3xl font-bold mb-4">{product.name}</h1>

        <!-- Manufacturer -->
        <div class="mb-4">
          <span class="text-base-content/70">by</span>
          <span class="text-lg font-medium text-primary ml-1">{product.manufacturer}</span>
        </div>

        <!-- Rating -->
        <div class="flex items-center gap-2 mb-6">
          <div class="flex items-center gap-1">
            {#each Array(5) as _, i}
              <svg 
                class="w-5 h-5 {i < Math.floor(product.ratings?.average || 0) ? 'text-warning' : 'text-base-300'}" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            {/each}
          </div>
          <span class="text-lg font-medium">
            {product.ratings?.average?.toFixed(1) || 'N/A'}
          </span>
          <span class="text-base-content/70">
            ({product.ratings?.count || 0} reviews)
          </span>
        </div>

        <!-- Price -->
        <div class="price-section mb-6">
          <div class="flex items-baseline gap-2">
            <span class="text-4xl font-bold text-primary">
              {formattedPrice}
            </span>
            <span class="text-lg text-base-content/70">
              {product.currency}
            </span>
          </div>
          
          <!-- Stock Status -->
          <div class="mt-2">
            {#if isAvailable}
              <span class="text-success font-medium">
                ✓ In Stock ({product.inventory?.available} available)
              </span>
            {:else}
              <span class="text-error font-medium">
                ✗ Out of Stock
              </span>
            {/if}
          </div>
        </div>

        <!-- Description -->
        <div class="description mb-6">
          <h3 class="text-lg font-semibold mb-2">Description</h3>
          <p class="text-base-content/80 leading-relaxed">
            {product.description}
          </p>
        </div>

        <!-- Quantity and Add to Cart -->
        {#if isAvailable}
          <div class="purchase-section mb-6">
            <div class="flex gap-4 items-end mb-4">
              <div class="form-control">
                <label class="label">
                  <span class="label-text">Quantity</span>
                </label>
                <Input
                  type="number"
                  min="1"
                  max={maxQuantity}
                  bind:value={quantity}
                  size="md"
                />
              </div>
            </div>

            <div class="flex gap-3">
              <Button
                variant="outline"
                size="lg"
                fullWidth
                on:click={handleAddToCart}
              >
                Add to Cart
              </Button>
              <Button
                variant="primary"
                size="lg"
                fullWidth
                on:click={handleBuyNow}
              >
                Buy Now
              </Button>
            </div>
          </div>
        {:else}
          <div class="out-of-stock mb-6">
            <Button variant="ghost" size="lg" fullWidth disabled>
              Out of Stock
            </Button>
          </div>
        {/if}

        <!-- Quick Actions -->
        <div class="quick-actions flex gap-2 mb-6">
          <Button variant="ghost" size="sm">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            Add to Wishlist
          </Button>
          <Button variant="ghost" size="sm">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
            Share
          </Button>
          <Button variant="ghost" size="sm">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Compare
          </Button>
        </div>
      </div>
    </div>

    <!-- Product Details Tabs -->
    <div class="product-tabs">
      <div class="tabs tabs-boxed mb-6">
        <button 
          class="tab"
          class:tab-active={showSpecifications}
          on:click={toggleSpecifications}
        >
          Specifications
        </button>
        <button 
          class="tab"
          class:tab-active={showReviews}
          on:click={toggleReviews}
        >
          Reviews ({product.ratings?.count || 0})
        </button>
      </div>

      <!-- Specifications Tab -->
      {#if showSpecifications}
        <Card title="Technical Specifications" class="mb-6">
          {#if product.specifications?.technical}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              {#each Object.entries(product.specifications.technical) as [key, value]}
                <div class="spec-item flex justify-between py-2 border-b border-base-300">
                  <span class="font-medium capitalize">{key.replace(/_/g, ' ')}</span>
                  <span class="text-base-content/70">{value}</span>
                </div>
              {/each}
            </div>
          {:else}
            <p class="text-base-content/70">No specifications available.</p>
          {/if}

          {#if product.specifications?.compatibility && product.specifications.compatibility.length > 0}
            <div class="mt-6">
              <h4 class="font-semibold mb-2">Compatibility</h4>
              <div class="flex flex-wrap gap-2">
                {#each product.specifications.compatibility as item}
                  <span class="badge badge-outline">{item}</span>
                {/each}
              </div>
            </div>
          {/if}
        </Card>
      {/if}

      <!-- Reviews Tab -->
      {#if showReviews}
        <Card title="Customer Reviews" class="mb-6">
          <div class="reviews-section">
            <!-- Review Summary -->
            <div class="review-summary mb-6 p-4 bg-base-200 rounded-lg">
              <div class="flex items-center gap-4">
                <div class="text-center">
                  <div class="text-3xl font-bold text-primary">
                    {product.ratings?.average?.toFixed(1) || 'N/A'}
                  </div>
                  <div class="flex items-center justify-center gap-1 mb-1">
                    {#each Array(5) as _, i}
                      <svg 
                        class="w-4 h-4 {i < Math.floor(product.ratings?.average || 0) ? 'text-warning' : 'text-base-300'}" 
                        fill="currentColor" 
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    {/each}
                  </div>
                  <div class="text-sm text-base-content/70">
                    {product.ratings?.count || 0} reviews
                  </div>
                </div>
                <div class="flex-1">
                  <p class="text-base-content/70">
                    Based on {product.ratings?.count || 0} customer reviews
                  </p>
                </div>
              </div>
            </div>

            <!-- Individual Reviews -->
            <div class="reviews-list">
              <p class="text-center text-base-content/70 py-8">
                Reviews will be loaded from the API in the full implementation.
              </p>
            </div>

            <!-- Write Review -->
            {#if $isAuthenticated}
              <div class="write-review mt-6 p-4 bg-base-200 rounded-lg">
                <h4 class="font-semibold mb-4">Write a Review</h4>
                <Button variant="outline" size="sm">
                  Write Review
                </Button>
              </div>
            {/if}
          </div>
        </Card>
      {/if}
    </div>

    <!-- Related Products -->
    <div class="related-products">
      <h2 class="text-2xl font-bold mb-6">Related Products</h2>
      <p class="text-center text-base-content/70 py-8">
        Related products will be loaded from the API recommendations.
      </p>
    </div>
  </div>
{:else}
  <!-- Product Not Found -->
  <div class="product-not-found text-center py-12">
    <div class="w-24 h-24 bg-base-200 rounded-full flex items-center justify-center mx-auto mb-4">
      <svg class="w-12 h-12 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h2 class="text-2xl font-bold mb-2">Product Not Found</h2>
    <p class="text-base-content/70 mb-6">
      The product you're looking for doesn't exist or has been removed.
    </p>
    <Button href="/marketplace" variant="primary">
      Back to Marketplace
    </Button>
  </div>
{/if}

<style>
  .product-detail {
    @apply animate-fade-in;
  }

  .aspect-square {
    aspect-ratio: 1 / 1;
  }

  .thumbnail {
    @apply transition-all duration-200 hover:border-primary;
  }

  .tabs {
    @apply flex;
  }

  .tab {
    @apply px-4 py-2 rounded-md transition-colors duration-200;
  }

  .tab-active {
    @apply bg-primary text-primary-content;
  }

  .spec-item:last-child {
    @apply border-b-0;
  }

  .breadcrumbs ul {
    @apply flex items-center gap-2;
  }

  .breadcrumbs li:not(:last-child)::after {
    content: '/';
    @apply text-base-content/50 ml-2;
  }

  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: .5;
    }
  }
</style>
