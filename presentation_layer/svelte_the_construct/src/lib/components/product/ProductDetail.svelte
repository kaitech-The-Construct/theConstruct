<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Product } from '$types';
  import { cartStore } from '$stores/cart';
  import { isAuthenticated, user } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';
  import Input from '$components/ui/Input.svelte';

  export let product: Product;
  export let recommendations: Product[] = [];
  export let reviews: any[] = [];

  const dispatch = createEventDispatcher();

  let selectedImageIndex = 0;
  let quantity = 1;
  let activeTab = 'specifications';
  let newReview = {
    rating: 5,
    title: '',
    comment: ''
  };
  let showWriteReview = false;

  $: isAvailable = product?.inventory?.available > 0;
  $: maxQuantity = product?.inventory?.available || 1;
  $: formattedPrice = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(product.price);

  function handleAddToCart() {
    cartStore.addItem(product, quantity);
    dispatch('add-to-cart', { product, quantity });
  }

  function handleBuyNow() {
    cartStore.addItem(product, quantity);
    dispatch('buy-now', { product, quantity });
  }

  function handleAddToWishlist() {
    dispatch('add-to-wishlist', { product });
  }

  function handleShare() {
    if (navigator.share) {
      navigator.share({
        title: product.name,
        text: product.description,
        url: window.location.href
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      dispatch('share', { product, method: 'clipboard' });
    }
  }

  function handleCompare() {
    dispatch('compare', { product });
  }

  function selectImage(index: number) {
    selectedImageIndex = index;
  }

  function setActiveTab(tab: string) {
    activeTab = tab;
  }

  function handleSubmitReview() {
    if (!$isAuthenticated) {
      dispatch('login-required');
      return;
    }

    const reviewData = {
      ...newReview,
      product_id: product.id,
      user_id: $user?.id
    };

    dispatch('submit-review', reviewData);
    
    // Reset form
    newReview = { rating: 5, title: '', comment: '' };
    showWriteReview = false;
  }

  function handleRecommendationClick(recommendedProduct: Product) {
    dispatch('view-recommendation', { product: recommendedProduct });
  }
</script>

<div class="product-detail">
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
        <div class="aspect-square bg-base-200 rounded-lg overflow-hidden relative group">
          {#if product.images && product.images.length > 0}
            <img 
              src={product.images[selectedImageIndex]} 
              alt={product.name}
              class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
            
            <!-- Image Navigation -->
            {#if product.images.length > 1}
              <button
                class="absolute left-2 top-1/2 transform -translate-y-1/2 btn btn-circle btn-sm bg-base-100/80 hover:bg-base-100"
                on:click={() => selectImage(selectedImageIndex > 0 ? selectedImageIndex - 1 : product.images.length - 1)}
              >
                ←
              </button>
              <button
                class="absolute right-2 top-1/2 transform -translate-y-1/2 btn btn-circle btn-sm bg-base-100/80 hover:bg-base-100"
                on:click={() => selectImage(selectedImageIndex < product.images.length - 1 ? selectedImageIndex + 1 : 0)}
              >
                →
              </button>
            {/if}
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
              class="thumbnail w-16 h-16 bg-base-200 rounded border-2 overflow-hidden flex-shrink-0 transition-all duration-200"
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
        <span class="badge badge-outline badge-lg">{product.category}</span>
      </div>

      <!-- Product Name -->
      <h1 class="text-3xl font-bold mb-4">{product.name}</h1>

      <!-- Manufacturer -->
      <div class="mb-4">
        <span class="text-base-content/70">by</span>
        <a href="/manufacturer/{product.manufacturer}" class="text-lg font-medium text-primary ml-1 link">
          {product.manufacturer}
        </a>
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
        <a href="#reviews" class="text-base-content/70 link">
          ({product.ratings?.count || 0} reviews)
        </a>
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
            <span class="text-success font-medium flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              In Stock ({product.inventory?.available} available)
            </span>
          {:else}
            <span class="text-error font-medium flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Out of Stock
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

      <!-- Quantity and Purchase Actions -->
      {#if isAvailable}
        <div class="purchase-section mb-6">
          <div class="flex gap-4 items-end mb-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">Quantity</span>
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

          <div class="flex gap-3 mb-4">
            <Button
              variant="outline"
              size="lg"
              fullWidth
              on:click={handleAddToCart}
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.8-1.8M7 13l-1.8 1.8M17 21a2 2 0 100-4 2 2 0 000 4zM9 21a2 2 0 100-4 2 2 0 000 4z" />
              </svg>
              Add to Cart
            </Button>
            <Button
              variant="primary"
              size="lg"
              fullWidth
              on:click={handleBuyNow}
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Buy Now
            </Button>
          </div>
        </div>
      {:else}
        <div class="out-of-stock mb-6">
          <Button variant="ghost" size="lg" fullWidth disabled>
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Out of Stock
          </Button>
          <p class="text-center text-sm text-base-content/70 mt-2">
            Get notified when this item is back in stock
          </p>
          <Button variant="outline" size="sm" fullWidth>
            Notify Me
          </Button>
        </div>
      {/if}

      <!-- Quick Actions -->
      <div class="quick-actions flex gap-2">
        <Button variant="ghost" size="sm" on:click={handleAddToWishlist}>
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          Wishlist
        </Button>
        <Button variant="ghost" size="sm" on:click={handleShare}>
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
          </svg>
          Share
        </Button>
        <Button variant="ghost" size="sm" on:click={handleCompare}>
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Compare
        </Button>
      </div>
    </div>
  </div>

  <!-- Product Details Tabs -->
  <div class="product-tabs mb-8">
    <div class="tabs tabs-boxed mb-6">
      <button 
        class="tab"
        class:tab-active={activeTab === 'specifications'}
        on:click={() => setActiveTab('specifications')}
      >
        Specifications
      </button>
      <button 
        class="tab"
        class:tab-active={activeTab === 'reviews'}
        on:click={() => setActiveTab('reviews')}
      >
        Reviews ({product.ratings?.count || 0})
      </button>
      <button 
        class="tab"
        class:tab-active={activeTab === 'shipping'}
        on:click={() => setActiveTab('shipping')}
      >
        Shipping & Returns
      </button>
    </div>

    <!-- Specifications Tab -->
    {#if activeTab === 'specifications'}
      <Card title="Technical Specifications">
        {#if product.specifications?.technical}
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {#each Object.entries(product.specifications.technical) as [key, value]}
              <div class="spec-item flex justify-between py-3 border-b border-base-300 last:border-b-0">
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
            <h4 class="font-semibold mb-3">Compatibility</h4>
            <div class="flex flex-wrap gap-2">
              {#each product.specifications.compatibility as item}
                <span class="badge badge-outline">{item}</span>
              {/each}
            </div>
          </div>
        {/if}

        {#if product.specifications?.dimensions}
          <div class="mt-6">
            <h4 class="font-semibold mb-3">Dimensions</h4>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              {#each Object.entries(product.specifications.dimensions) as [key, value]}
                <div class="text-center p-3 bg-base-200 rounded-lg">
                  <div class="font-medium capitalize">{key}</div>
                  <div class="text-sm text-base-content/70">{value}</div>
                </div>
              {/each}
            </div>
          </div>
        {/if}
      </Card>
    {/if}

    <!-- Reviews Tab -->
    {#if activeTab === 'reviews'}
      <div id="reviews">
        <Card title="Customer Reviews">
          <!-- Review Summary -->
          <div class="review-summary mb-6 p-4 bg-base-200 rounded-lg">
            <div class="flex items-center gap-6">
              <div class="text-center">
                <div class="text-4xl font-bold text-primary">
                  {product.ratings?.average?.toFixed(1) || 'N/A'}
                </div>
                <div class="flex items-center justify-center gap-1 mb-1">
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
                <div class="text-sm text-base-content/70">
                  {product.ratings?.count || 0} reviews
                </div>
              </div>
              
              <!-- Rating Breakdown -->
              <div class="flex-1">
                <h4 class="font-semibold mb-3">Rating Breakdown</h4>
                {#each [5, 4, 3, 2, 1] as rating}
                  <div class="flex items-center gap-2 mb-1">
                    <span class="text-sm w-8">{rating}★</span>
                    <div class="flex-1 bg-base-300 rounded-full h-2">
                      <div 
                        class="bg-warning h-2 rounded-full transition-all duration-300"
                        style="width: {Math.random() * 100}%"
                      ></div>
                    </div>
                    <span class="text-sm text-base-content/70 w-8">
                      {Math.floor(Math.random() * 50)}
                    </span>
                  </div>
                {/each}
              </div>
            </div>
          </div>

          <!-- Write Review Section -->
          {#if $isAuthenticated}
            <div class="write-review mb-6">
              {#if !showWriteReview}
                <Button variant="outline" on:click={() => showWriteReview = true}>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  Write a Review
                </Button>
              {:else}
                <div class="bg-base-200 p-4 rounded-lg">
                  <h4 class="font-semibold mb-4">Write Your Review</h4>
                  
                  <!-- Rating Input -->
                  <div class="mb-4">
                    <label class="label">
                      <span class="label-text">Rating</span>
                    </label>
                    <div class="flex gap-1">
                      {#each Array(5) as _, i}
                        <button
                          type="button"
                          class="text-2xl transition-colors duration-200 {i < newReview.rating ? 'text-warning' : 'text-base-300'}"
                          on:click={() => newReview = { ...newReview, rating: i + 1 }}
                        >
                          ★
                        </button>
                      {/each}
                    </div>
                  </div>

                  <!-- Review Title -->
                  <div class="mb-4">
                    <Input
                      label="Review Title"
                      bind:value={newReview.title}
                      placeholder="Summarize your experience"
                    />
                  </div>

                  <!-- Review Comment -->
                  <div class="mb-4">
                    <label class="label">
                      <span class="label-text">Your Review</span>
                    </label>
                    <textarea
                      class="textarea textarea-bordered w-full h-24"
                      bind:value={newReview.comment}
                      placeholder="Share your thoughts about this product..."
                    ></textarea>
                  </div>

                  <!-- Actions -->
                  <div class="flex gap-2">
                    <Button variant="primary" on:click={handleSubmitReview}>
                      Submit Review
                    </Button>
                    <Button variant="ghost" on:click={() => showWriteReview = false}>
                      Cancel
                    </Button>
                  </div>
                </div>
              {/if}
            </div>
          {:else}
            <div class="text-center p-4 bg-base-200 rounded-lg mb-6">
              <p class="text-base-content/70 mb-2">Sign in to write a review</p>
              <Button variant="outline" size="sm" href="/login">
                Sign In
              </Button>
            </div>
          {/if}

          <!-- Reviews List -->
          <div class="reviews-list space-y-4">
            {#if reviews.length > 0}
              {#each reviews as review}
                <div class="review-item p-4 border border-base-300 rounded-lg">
                  <div class="flex justify-between items-start mb-2">
                    <div>
                      <div class="font-medium">{review.user_name}</div>
                      <div class="flex items-center gap-1">
                        {#each Array(5) as _, i}
                          <svg 
                            class="w-4 h-4 {i < review.rating ? 'text-warning' : 'text-base-300'}" 
                            fill="currentColor" 
                            viewBox="0 0 20 20"
                          >
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                        {/each}
                      </div>
                    </div>
                    <div class="text-sm text-base-content/70">
                      {new Date(review.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <h4 class="font-medium mb-2">{review.title}</h4>
                  <p class="text-base-content/80">{review.comment}</p>
                </div>
              {/each}
            {:else}
              <div class="text-center py-8">
                <svg class="w-16 h-16 text-base-content/30 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <p class="text-base-content/70">No reviews yet</p>
                <p class="text-sm text-base-content/50">Be the first to review this product!</p>
              </div>
            {/if}
          </div>
        </Card>
      </div>
    {/if}

    <!-- Shipping & Returns Tab -->
    {#if activeTab === 'shipping'}
      <Card title="Shipping & Returns">
        <div class="space-y-6">
          <!-- Shipping Information -->
          <div>
            <h4 class="font-semibold mb-3 flex items-center gap-2">
              <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
              Shipping Options
            </h4>
            <div class="space-y-3">
              <div class="flex justify-between items-center p-3 bg-base-200 rounded-lg">
                <div>
                  <div class="font-medium">Standard Shipping</div>
                  <div class="text-sm text-base-content/70">5-7 business days</div>
                </div>
                <div class="font-medium text-success">Free</div>
              </div>
              <div class="flex justify-between items-center p-3 bg-base-200 rounded-lg">
                <div>
                  <div class="font-medium">Express Shipping</div>
                  <div class="text-sm text-base-content/70">2-3 business days</div>
                </div>
                <div class="font-medium">$29.99</div>
              </div>
                <div class="flex justify-between items-center p-3 bg-base-200 rounded-lg">
                <div>
                  <div class="font-medium">Overnight Shipping</div>
                  <div class="text-sm text-base-content/70">Next business day</div>
                </div>
                <div class="font-medium">$59.99</div>
              </div>
            </div>
          </div>

          <!-- Returns Information -->
          <div>
            <h4 class="font-semibold mb-3 flex items-center gap-2">
              <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
              </svg>
              Returns & Exchanges
            </h4>
            <div class="space-y-3">
              <div class="p-3 bg-base-200 rounded-lg">
                <div class="font-medium mb-1">30-Day Return Policy</div>
                <div class="text-sm text-base-content/70">
                  Return unused items in original packaging within 30 days for a full refund.
                </div>
              </div>
              <div class="p-3 bg-base-200 rounded-lg">
                <div class="font-medium mb-1">Free Return Shipping</div>
                <div class="text-sm text-base-content/70">
                  We'll provide a prepaid return label for your convenience.
                </div>
              </div>
              <div class="p-3 bg-base-200 rounded-lg">
                <div class="font-medium mb-1">Exchange Policy</div>
                <div class="text-sm text-base-content/70">
                  Exchange for different size or model within 30 days.
                </div>
              </div>
            </div>
          </div>

          <!-- Warranty Information -->
          <div>
            <h4 class="font-semibold mb-3 flex items-center gap-2">
              <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Warranty
            </h4>
            <div class="p-3 bg-base-200 rounded-lg">
              <div class="font-medium mb-1">1-Year Manufacturer Warranty</div>
              <div class="text-sm text-base-content/70">
                Covers defects in materials and workmanship. Extended warranty options available.
              </div>
            </div>
          </div>
        </div>
      </Card>
    {/if}
  </div>

  <!-- Related Products -->
  {#if recommendations.length > 0}
    <div class="related-products">
      <h2 class="text-2xl font-bold mb-6">You Might Also Like</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each recommendations.slice(0, 4) as recommendedProduct}
          <div class="recommendation-card">
            <button
              class="w-full text-left transition-transform duration-200 hover:scale-105"
              on:click={() => handleRecommendationClick(recommendedProduct)}
            >
              <div class="aspect-square bg-base-200 rounded-lg overflow-hidden mb-3">
                {#if recommendedProduct.images && recommendedProduct.images.length > 0}
                  <img 
                    src={recommendedProduct.images[0]} 
                    alt={recommendedProduct.name}
                    class="w-full h-full object-cover"
                  />
                {:else}
                  <div class="w-full h-full flex items-center justify-center">
                    <svg class="w-12 h-12 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                {/if}
              </div>
              <h3 class="font-medium mb-1 line-clamp-2">{recommendedProduct.name}</h3>
              <p class="text-sm text-base-content/70 mb-2">by {recommendedProduct.manufacturer}</p>
              <div class="font-bold text-primary">
                {new Intl.NumberFormat('en-US', {
                  style: 'currency',
                  currency: 'USD'
                }).format(recommendedProduct.price)}
              </div>
            </button>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .product-detail {
    @apply max-w-7xl mx-auto;
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

  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .recommendation-card {
    @apply bg-base-100 border border-base-300 rounded-lg p-4 hover:shadow-lg transition-shadow duration-200;
  }
</style>
