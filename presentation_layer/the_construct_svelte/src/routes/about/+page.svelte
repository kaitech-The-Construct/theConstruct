<script lang="ts">
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';
</script>

<svelte:head>
  <title>About - The Construct</title>
  <meta name="description" content="Learn about The Construct - the premier decentralized marketplace for robotics, manufacturing, and automation solutions." />
</svelte:head>

<!-- Hero Section -->
<section class="hero min-h-[40vh] bg-gradient-to-br from-primary/5 to-secondary/5 rounded-lg mb-12">
  <div class="hero-content text-center">
    <div class="max-w-4xl">
      <h1 class="text-4xl font-bold mb-4 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
        About The Construct
      </h1>
      <p class="text-lg text-base-content/80 mb-6">
        Building the future of robotics commerce through decentralized technology
      </p>
    </div>
  </div>
</section>

<!-- Mission Section -->
<section class="mb-16">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-3xl font-bold text-center mb-8">Our Mission</h2>
    <div class="prose prose-lg max-w-none text-center">
      <p class="text-xl leading-relaxed text-base-content/80">
        The Construct is revolutionizing how the world buys, sells, and manufactures robotics solutions. 
        We're creating a decentralized ecosystem where innovation meets accessibility, connecting robotics enthusiasts, 
        manufacturers, and businesses in a secure, transparent, and efficient marketplace.
      </p>
    </div>
  </div>
</section>

<!-- What We Do Section -->
<section class="mb-16">
  <h2 class="text-3xl font-bold text-center mb-12">What We Do</h2>
  
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
    <Card title="Decentralized Marketplace" shadow={true}>
      <div class="space-y-4">
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <p class="text-base-content/70">
          We operate a secure, blockchain-powered marketplace where buyers and sellers can trade robotics products, 
          software, and components without traditional intermediaries. Every transaction is secured by smart contracts, 
          ensuring trust and transparency.
        </p>
        <ul class="text-sm text-base-content/60 space-y-1">
          <li>• Industrial robots and robotic arms</li>
          <li>• Autonomous mobile robots (AMRs)</li>
          <li>• AI software and motion planning tools</li>
          <li>• Sensors, actuators, and components</li>
        </ul>
      </div>
    </Card>

    <Card title="Smart Manufacturing Network" shadow={true}>
      <div class="space-y-4">
        <div class="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          </svg>
        </div>
        <p class="text-base-content/70">
          We connect businesses needing custom robotics solutions with verified manufacturers and engineers. 
          Our platform facilitates milestone-based project management with secure escrow payments, 
          ensuring quality deliverables and fair compensation.
        </p>
        <ul class="text-sm text-base-content/60 space-y-1">
          <li>• Custom robot design and manufacturing</li>
          <li>• Milestone-based project tracking</li>
          <li>• Verified manufacturer network</li>
          <li>• Secure escrow payment system</li>
        </ul>
      </div>
    </Card>
  </div>
</section>

<!-- Why Blockchain Section -->
<section class="mb-16">
  <h2 class="text-3xl font-bold text-center mb-8">Why Blockchain Technology?</h2>
  
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <Card title="Trust & Transparency" shadow={true}>
      <div class="text-center">
        <div class="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <p class="text-sm text-base-content/70">
          Every transaction is recorded on the blockchain, creating an immutable history that builds trust between buyers and sellers.
        </p>
      </div>
    </Card>

    <Card title="Secure Payments" shadow={true}>
      <div class="text-center">
        <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <p class="text-sm text-base-content/70">
          Smart contracts automatically execute payments when conditions are met, protecting both parties in every transaction.
        </p>
      </div>
    </Card>

    <Card title="Global Access" shadow={true}>
      <div class="text-center">
        <div class="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-sm text-base-content/70">
          Decentralized technology eliminates geographical barriers, enabling global commerce without traditional banking limitations.
        </p>
      </div>
    </Card>
  </div>
</section>

<!-- Technology Stack Section -->
<section class="mb-16">
  <h2 class="text-3xl font-bold text-center mb-8">Built on Modern Technology</h2>
  
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <Card title="Blockchain Infrastructure" shadow={true}>
      <div class="space-y-4">
        <p class="text-base-content/70">
          Our platform leverages multiple blockchain networks to provide the best user experience:
        </p>
        <ul class="space-y-2 text-sm text-base-content/60">
          <li class="flex items-center gap-2">
            <div class="w-2 h-2 bg-primary rounded-full"></div>
            <strong>XRPL (XRP Ledger):</strong> For fast, low-cost international payments
          </li>
          <li class="flex items-center gap-2">
            <div class="w-2 h-2 bg-secondary rounded-full"></div>
            <strong>Solana:</strong> For smart contracts and decentralized applications
          </li>
        </ul>
      </div>
    </Card>

    <Card title="Modern Web Platform" shadow={true}>
      <div class="space-y-4">
        <p class="text-base-content/70">
          Built with cutting-edge web technologies for optimal performance and user experience:
        </p>
        <ul class="space-y-2 text-sm text-base-content/60">
          <li class="flex items-center gap-2">
            <div class="w-2 h-2 bg-accent rounded-full"></div>
            <strong>SvelteKit:</strong> Fast, reactive user interface
          </li>
          <li class="flex items-center gap-2">
            <div class="w-2 h-2 bg-primary rounded-full"></div>
            <strong>Real-time Updates:</strong> Live order tracking and notifications
          </li>
        </ul>
      </div>
    </Card>
  </div>
</section>

<!-- Who We Serve Section -->
<section class="mb-16">
  <h2 class="text-3xl font-bold text-center mb-8">Who We Serve</h2>
  
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <Card shadow={true}>
      <div class="text-center">
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <h3 class="font-semibold mb-2">Researchers</h3>
        <p class="text-sm text-base-content/70">
          Universities and research institutions seeking advanced robotics platforms for breakthrough research.
        </p>
      </div>
    </Card>

    <Card shadow={true}>
      <div class="text-center">
        <div class="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 class="font-semibold mb-2">Manufacturers</h3>
        <p class="text-sm text-base-content/70">
          Companies automating production lines with industrial robots and smart manufacturing solutions.
        </p>
      </div>
    </Card>

    <Card shadow={true}>
      <div class="text-center">
        <div class="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h3 class="font-semibold mb-2">Startups</h3>
        <p class="text-sm text-base-content/70">
          Innovative companies building the next generation of robotic products and services.
        </p>
      </div>
    </Card>

    <Card shadow={true}>
      <div class="text-center">
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h3 class="font-semibold mb-2">Enthusiasts</h3>
        <p class="text-sm text-base-content/70">
          Hobbyists and makers exploring robotics as a passion project or learning experience.
        </p>
      </div>
    </Card>
  </div>
</section>

<!-- Future Vision Section -->
<section class="mb-16">
  <div class="bg-gradient-to-r from-primary/5 to-secondary/5 rounded-lg p-8">
    <h2 class="text-3xl font-bold text-center mb-6">Our Vision for the Future</h2>
    <div class="max-w-3xl mx-auto text-center space-y-4">
      <p class="text-lg text-base-content/80">
        We envision a world where advanced robotics technology is accessible to everyone, 
        from small startups to large enterprises. Through decentralized commerce, we're removing 
        barriers that have historically limited access to cutting-edge robotics solutions.
      </p>
      <p class="text-base-content/70">
        Our goal is to accelerate robotics adoption across industries, foster innovation through 
        global collaboration, and create economic opportunities for manufacturers and developers worldwide.
      </p>
    </div>
  </div>
</section>

<!-- Call to Action -->
<section class="text-center">
  <h2 class="text-3xl font-bold mb-4">Ready to Join The Revolution?</h2>
  <p class="text-lg text-base-content/70 mb-8 max-w-2xl mx-auto">
    Whether you're looking to buy robotics solutions, sell your products, or collaborate on manufacturing projects, 
    The Construct provides the platform and tools you need to succeed.
  </p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <Button href="/marketplace" variant="primary" size="lg">
      Explore Marketplace
    </Button>
    <Button href="/register" variant="outline" size="lg">
      Create Account
    </Button>
  </div>
</section>

<style>
  .hero {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .hero-content {
    max-width: 56rem;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .prose {
    color: inherit;
  }

  .prose p {
    margin-bottom: 1.25em;
  }
</style>
