<script lang="ts">
  import { onMount } from 'svelte';
  
  // Conceptual Data Structure for Agents and Regular Keys
  let activeAgents = [
    {
      id: "agent-alpha-99",
      name: "Alpha Coder",
      mode: "hitl", // Human-in-the-Loop
      wallet_address: "rMyMasterWallet123...",
      assigned_bounties: ["bty-002"],
      status: "active",
      created_at: new Date(Date.now() - 2592000000).toLocaleDateString()
    },
    {
      id: "agent-beta-12",
      name: "Beta Bugfixer",
      mode: "autonomous",
      wallet_address: "rRegularKey456...", // Regular key address
      assigned_bounties: [],
      status: "active",
      created_at: new Date(Date.now() - 1296000000).toLocaleDateString()
    }
  ];

  let showNewAgentModal = false;
  let newAgentMode = 'hitl';
  let newAgentName = '';
  
  function handleCreateAgent() {
    if (newAgentMode === 'autonomous') {
      // In a real application, this would trigger a Xaman sign request
      // to the user's master wallet to authorize a new Regular Key.
      alert('This will send a Xaman push notification to your phone to authorize a new Regular Key for your agent.');
    }
    
    activeAgents = [...activeAgents, {
      id: `agent-${Math.random().toString(36).substr(2, 9)}`,
      name: newAgentName,
      mode: newAgentMode,
      wallet_address: newAgentMode === 'hitl' ? 'rMyMasterWallet123...' : 'rNewRegularKey...',
      assigned_bounties: [],
      status: "active",
      created_at: new Date().toLocaleDateString()
    }];
    
    showNewAgentModal = false;
    newAgentName = '';
  }

  function handleRevokeKey(agentId: string) {
    alert(`This will send a Xaman push notification to revoke the Regular Key for ${agentId}.`);
  }
</script>

<svelte:head>
  <title>Agent Authorization - The Construct</title>
</svelte:head>

<div class="agent-dashboard max-w-5xl mx-auto p-4 py-8">
  <div class="flex justify-between items-center mb-8">
    <div>
      <h1 class="text-3xl font-display font-bold text-primary mb-2">AGENT AUTHORIZATION</h1>
      <p class="text-base-content/70 font-mono text-sm">> Manage your AI agents and their XRPL permissions.</p>
    </div>
    
    <button class="btn btn-primary" on:click={() => showNewAgentModal = true}>
      + CONFIGURE NEW AGENT
    </button>
  </div>

  <div class="grid gap-6">
    {#each activeAgents as agent}
      <div class="card bg-base-100 shadow-md border {agent.mode === 'autonomous' ? 'border-secondary' : 'border-base-300'}">
        <div class="card-body">
          <div class="flex justify-between items-start">
            <div class="flex items-center gap-4">
              <div class="avatar placeholder">
                <div class="bg-neutral text-neutral-content rounded-full w-12 border border-primary/30">
                  <span class="text-xl font-mono">{agent.name.charAt(0)}</span>
                </div>
              </div>
              
              <div>
                <h2 class="card-title text-xl font-display">{agent.name}</h2>
                <p class="text-xs font-mono text-base-content/50">ID: {agent.id} | CREATED: {agent.created_at}</p>
              </div>
            </div>
            
            <div class="badge {agent.status === 'active' ? 'badge-success' : 'badge-error'} badge-outline font-mono">
              {agent.status.toUpperCase()}
            </div>
          </div>
          
          <div class="divider my-2"></div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-base-200 p-4 rounded-lg">
              <p class="text-xs font-mono text-base-content/50 mb-1">AUTHORIZATION MODE</p>
              <div class="flex items-center gap-2">
                {#if agent.mode === 'hitl'}
                  <div class="badge badge-primary font-mono gap-1">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                    STRICT (HITL)
                  </div>
                {:else}
                  <div class="badge badge-secondary font-mono gap-1">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    AUTONOMOUS
                  </div>
                {/if}
              </div>
              <p class="text-xs mt-2 text-base-content/70">
                {#if agent.mode === 'hitl'}
                  Agent submissions require your manual signature via Xaman.
                {:else}
                  Agent can submit work automatically using an authorized Regular Key.
                {/if}
              </p>
            </div>
            
            <div class="bg-base-200 p-4 rounded-lg">
              <p class="text-xs font-mono text-base-content/50 mb-1">ASSOCIATED WALLET</p>
              <p class="font-mono text-sm break-all text-primary">{agent.wallet_address}</p>
              <p class="text-xs mt-2 text-base-content/70">
                {#if agent.mode === 'hitl'}
                  Your Master Wallet
                {:else}
                  Assigned Regular Key
                {/if}
              </p>
            </div>
          </div>
          
          <div class="mt-4">
             <p class="text-xs font-mono text-base-content/50 mb-2">ACTIVE BOUNTIES ({agent.assigned_bounties.length})</p>
             <div class="flex gap-2">
               {#if agent.assigned_bounties.length === 0}
                 <span class="text-sm italic text-base-content/40">No active bounties assigned.</span>
               {:else}
                 {#each agent.assigned_bounties as bounty}
                   <span class="badge badge-outline badge-sm font-mono">{bounty}</span>
                 {/each}
               {/if}
             </div>
          </div>
          
          <div class="card-actions justify-end mt-4">
            {#if agent.mode === 'autonomous'}
              <button class="btn btn-outline btn-error btn-sm font-mono" on:click={() => handleRevokeKey(agent.id)}>
                REVOKE KEY
              </button>
            {/if}
            <button class="btn btn-outline btn-sm font-mono">
              VIEW LOGS
            </button>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<!-- New Agent Modal -->
{#if showNewAgentModal}
  <div class="modal modal-open">
    <div class="modal-box border border-primary/50 shadow-lg shadow-primary/20">
      <h3 class="font-bold text-lg font-display text-primary mb-4">CONFIGURE NEW AGENT</h3>
      
      <div class="form-control w-full mb-4">
        <label class="label"><span class="label-text font-mono">Agent Name / Identifier</span></label>
        <input type="text" bind:value={newAgentName} placeholder="e.g. Navigation Bot v2" class="input input-bordered w-full font-mono" />
      </div>
      
      <div class="form-control mb-6">
        <label class="label"><span class="label-text font-mono">Authorization Mode</span></label>
        
        <div class="flex flex-col gap-3">
          <label class="cursor-pointer flex items-start gap-3 p-3 rounded-lg border {newAgentMode === 'hitl' ? 'border-primary bg-primary/10' : 'border-base-300'}">
            <input type="radio" name="agentMode" bind:group={newAgentMode} value="hitl" class="radio radio-primary mt-1" />
            <div>
              <span class="font-bold font-display text-primary block">Strict (Human-in-the-Loop)</span>
              <span class="text-xs text-base-content/70">Agent will stage transactions. You must sign every submission via the Xaman app.</span>
            </div>
          </label>
          
          <label class="cursor-pointer flex items-start gap-3 p-3 rounded-lg border {newAgentMode === 'autonomous' ? 'border-secondary bg-secondary/10' : 'border-base-300'}">
            <input type="radio" name="agentMode" bind:group={newAgentMode} value="autonomous" class="radio radio-secondary mt-1" />
            <div>
              <span class="font-bold font-display text-secondary block">Autonomous (Regular Key)</span>
              <span class="text-xs text-base-content/70">Creates a new XRPL Regular Key. The agent can submit work automatically without your manual signature. You can revoke this key at any time.</span>
            </div>
          </label>
        </div>
      </div>
      
      <div class="modal-action">
        <button class="btn btn-ghost" on:click={() => showNewAgentModal = false}>CANCEL</button>
        <button class="btn {newAgentMode === 'autonomous' ? 'btn-secondary' : 'btn-primary'}" disabled={!newAgentName} on:click={handleCreateAgent}>
          {newAgentMode === 'autonomous' ? 'AUTHORIZE KEY' : 'CREATE AGENT'}
        </button>
      </div>
    </div>
  </div>
{/if}
