<script lang="ts">
  import { onMount } from 'svelte';
  import { productStore, filteredProducts, isLoading } from '$stores/products';
  import { isAuthenticated } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';

  let featuredProducts: any[] = [];

  onMount(async () => {
    // Load some featured products for the homepage
    try {
      await productStore.loadProducts();
      // Take first 6 products as featured
      featuredProducts = $filteredProducts.slice(0, 6);
    } catch (error) {
      console.error('Failed to load featured products:', error);
    }
  });
</script>

<svelte:head>
  <title>The Construct - Decentralized Robotics Exchange</title>
  <meta name="description" content="The premier decentralized marketplace for robotics, manufacturing, and automation solutions." />
</svelte:head>

<!-- Hero Section -->
<section class="hero min-h-[60vh] bg-gradient-to-br from-primary/10 to-secondary/10 rounded-lg mb-12">
  <div class="hero-content text-center">
    <div class="max-w-4xl">
      <h1 class="text-5xl font-bold mb-6 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
        Welcome to The Construct
      </h1>
      <p class="text-xl mb-8 text-base-content/80">
        The premier decentralized marketplace for robotics, manufacturing, and automation solutions.
        Connect with manufacturers, discover cutting-edge robotics, and build the future.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <Button href="/marketplace" variant="primary" size="lg">
          Explore Marketplace
        </Button>
        <Button href="/manufacturing" variant="outline" size="lg">
          Start Manufacturing
        </Button>
      </div>
    </div>
  </div>
</section>

<!-- Features Section -->
<section class="mb-12">
  <div class="text-center mb-8">
    <h2 class="text-3xl font-bold mb-4">Why Choose The Construct?</h2>
    <p class="text-lg text-base-content/70">
      Revolutionizing robotics commerce through blockchain technology
    </p>
  </div>
  
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <Card title="Decentralized Marketplace" shadow={true}>
      <div class="text-center">
        <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <p class="text-base-content/70">
          Trade robotics and components on a secure, decentralized platform powered by blockchain technology.
        </p>
      </div>
    </Card>

    <Card title="Smart Manufacturing" shadow={true}>
      <div class="text-center">
        <div class="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <p class="text-base-content/70">
          Connect with verified manufacturers for custom robotics solutions with milestone-based payments.
        </p>
      </div>
    </Card>

    <Card title="Blockchain Security" shadow={true}>
      <div class="text-center">
        <div class="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <p class="text-base-content/70">
          Secure transactions with smart contracts, escrow services, and multi-chain support.
        </p>
      </div>
    </Card>
  </div>
</section>

<!-- Featured Products Section -->
{#if featuredProducts.length > 0}
  <section class="mb-12">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h2 class="text-3xl font-bold mb-2">Featured Products</h2>
        <p class="text-base-content/70">Discover the latest in robotics and automation</p>
      </div>
      <Button href="/marketplace" variant="outline">
        View All Products
      </Button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {#each featuredProducts as product}
        <Card clickable={true} shadow={true}>
          <div class="aspect-video bg-base-200 rounded-lg mb-4 flex items-center justify-center">
            {#if product.images && product.images.length > 0}
              <img 
                src={product.images[0]} 
                alt={product.name}
                class="w-full h-full object-cover rounded-lg"
              />
            {:else}
              <svg class="w-16 h-16 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            {/if}
          </div>
          
          <h3 class="font-semibold text-lg mb-2">{product.name}</h3>
          <p class="text-base-content/70 text-sm mb-4 line-clamp-2">
            {product.description}
          </p>
          
          <div class="flex justify-between items-center">
            <div>
              <span class="text-2xl font-bold text-primary">
                ${product.price.toLocaleString()}
              </span>
              <span class="text-sm text-base-content/70 ml-1">
                {product.currency}
              </span>
            </div>
            <div class="flex items-center gap-1">
              <svg class="w-4 h-4 text-warning" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span class="text-sm text-base-content/70">
                {product.ratings?.average?.toFixed(1) || 'N/A'}
              </span>
            </div>
          </div>
          
          <div slot="actions">
            <Button href="/product/{product.id}" variant="primary" size="sm" fullWidth>
              View Details
            </Button>
          </div>
        </Card>
      {/each}
    </div>
  </section>
{/if}

<!-- CTA Section -->
<section class="bg-gradient-to-r from-primary to-secondary rounded-lg p-8 text-center text-primary-content">
  <h2 class="text-3xl font-bold mb-4">Ready to Get Started?</h2>
  <p class="text-lg mb-6 opacity-90">
    Join thousands of robotics enthusiasts, manufacturers, and innovators building the future.
  </p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    {#if $isAuthenticated}
      <Button href="/marketplace" variant="outline" size="lg" class="text-white border-white hover:bg-white hover:text-primary">
        Start Shopping
      </Button>
      <Button href="/profile" variant="ghost" size="lg" class="text-white hover:bg-white/10">
        View Profile
      </Button>
    {:else}
      <Button href="/register" variant="outline" size="lg" class="text-white border-white hover:bg-white hover:text-primary">
        Create Account
      </Button>
      <Button href="/login" variant="ghost" size="lg" class="text-white hover:bg-white/10">
        Sign In
      </Button>
    {/if}
  </div>
</section>

<style>
  .hero {
    @apply flex items-center justify-center;
  }

  .hero-content {
    @apply max-w-4xl mx-auto px-4;
  }

  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .aspect-video {
    aspect-ratio: 16 / 9;
  }
</style>
