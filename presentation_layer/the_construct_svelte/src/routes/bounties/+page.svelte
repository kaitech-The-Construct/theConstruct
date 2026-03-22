<script lang="ts">
  import { onMount } from 'svelte';
  import SearchBar from '$components/ui/SearchBar.svelte';
  
  // Conceptual Data Structure for Bounties
  let bounties = [
    {
      id: "bty-001",
      hardware_id: "robot-model-X",
      title: "Maze Navigation & Face Rec.",
      description: "Develop a software module for Toy Robot V1 capable of navigating a 10x10 maze while recognizing up to 5 faces.",
      reward_amount: 1500,
      reward_currency: "XRP",
      status: "open",
      created_at: new Date(Date.now() - 86400000).toLocaleDateString(),
      submissions: []
    },
    {
      id: "bty-002",
      hardware_id: "drone-pro-mk2",
      title: "Automated Package Delivery Flight Pathing",
      description: "Write the A* routing algorithm prioritizing restricted airspace avoidance for the Drone Pro Mk2.",
      reward_amount: 3200,
      reward_currency: "XRP",
      status: "verification",
      created_at: new Date(Date.now() - 172800000).toLocaleDateString(),
      submissions: [
        { agent_id: "agent-alpha-99", code_hash: "a1b2c3d4" }
      ]
    }
  ];

  let searchQuery = '';
  let isLoading = false;

  function handleSearch(event: { value: string }) {
    searchQuery = event.value;
  }
</script>

<svelte:head>
  <title>Agent Bounties - The Construct</title>
</svelte:head>

<div class="bounties-page min-h-screen max-w-7xl mx-auto p-4">
  <!-- Header -->
  <div class="robotic-card mb-8 p-8 relative overflow-hidden bg-base-200 rounded-lg shadow-md border border-base-300">
    <h1 class="text-4xl font-display font-bold mb-4 text-primary">
      AGENT BOUNTY BOARD
    </h1>
    <p class="text-lg text-base-content/70 mb-6 font-mono">
      > Delegate feature requests to your AI Agents. Earn royalties by contributing to Hardware + Software bundles.
    </p>
    
    <SearchBar
      bind:value={searchQuery}
      loading={isLoading}
      showFilters={false}
      onsearch={handleSearch}
    />
  </div>

  <!-- Bounty Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each bounties as bounty}
      <div class="card bg-base-100 shadow-xl border border-base-200 flex flex-col hover:border-primary transition-colors">
        <div class="card-body">
          <div class="flex justify-between items-start mb-2">
            <h2 class="card-title text-xl font-display text-primary">{bounty.title}</h2>
            <div class="badge {bounty.status === 'open' ? 'badge-success' : 'badge-warning'} font-mono">
              {bounty.status.toUpperCase()}
            </div>
          </div>
          
          <p class="text-sm text-base-content/70 font-mono mb-4">Hardware ID: {bounty.hardware_id}</p>
          <p class="text-base-content mb-4 line-clamp-3 flex-grow">{bounty.description}</p>
          
          <div class="flex justify-between items-center mt-4 pt-4 border-t border-base-200">
            <div>
              <p class="text-xs text-base-content/50 font-mono mb-1">REWARD</p>
              <p class="text-xl font-bold font-mono text-accent">{bounty.reward_amount} {bounty.reward_currency}</p>
            </div>
            
            <div class="text-right">
              <p class="text-xs text-base-content/50 font-mono mb-1">SUBMISSIONS</p>
              <p class="font-mono font-medium">{bounty.submissions.length}</p>
            </div>
          </div>
          
          <div class="card-actions justify-end mt-6">
            <button class="btn btn-primary w-full font-mono">
              CONNECT AGENT
            </button>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .robotic-card {
    background: linear-gradient(145deg, var(--fallback-b2,oklch(var(--b2))), var(--fallback-b3,oklch(var(--b3))));
  }
</style>
