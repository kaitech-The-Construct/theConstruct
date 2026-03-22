<script lang="ts">
  import { onMount } from 'svelte';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';
  import Input from '$components/ui/Input.svelte';

  // State for MCP tools
  let address = '';
  let balanceResult = '';
  let checkingBalance = false;

  let robotId = '';
  let nftStatusResult = '';
  let checkingNft = false;

  // State for Manufacturing
  let orderId = 'MFG123456';
  let milestoneId = 'milestone-1';
  let wallet = 'wallet-addr-123';
  let paymentResult = '';
  let processingPayment = false;

  const API_URL = 'http://localhost:8000'; // Adjust as needed based on FastAPI setup

  async function checkBalance() {
    checkingBalance = true;
    balanceResult = '';
    try {
      const response = await fetch(`${API_URL}/mcp/tools/get_balance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address })
      });
      const data = await response.json();
      balanceResult = JSON.stringify(data, null, 2);
    } catch (err: any) {
      balanceResult = `Error: ${err.message}`;
    }
    checkingBalance = false;
  }

  async function checkNftStatus() {
    checkingNft = true;
    nftStatusResult = '';
    try {
      const response = await fetch(`${API_URL}/mcp/tools/check_nft_status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ robot_id: robotId })
      });
      const data = await response.json();
      nftStatusResult = JSON.stringify(data, null, 2);
    } catch (err: any) {
      nftStatusResult = `Error: ${err.message}`;
    }
    checkingNft = false;
  }

  async function payMilestone() {
    processingPayment = true;
    paymentResult = '';
    try {
      const response = await fetch(`${API_URL}/manufacturing/orders/${orderId}/milestones/${milestoneId}/pay`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet })
      });
      const data = await response.json();
      paymentResult = JSON.stringify(data, null, 2);
    } catch (err: any) {
      paymentResult = `Error: ${err.message}`;
    }
    processingPayment = false;
  }
</script>

<svelte:head>
  <title>Tools | The Construct</title>
</svelte:head>

<div class="max-w-6xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8 animate-fade-in">
  <div class="flex flex-col gap-2">
    <h1 class="text-3xl font-bold text-base-content">Blockchain & Manufacturing Tools</h1>
    <p class="text-base-content/70">Manage on-chain assets, query ledgers, and process manufacturing milestone payments.</p>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
    <!-- MCP Tools Section -->
    <div class="space-y-6">
      <h2 class="text-xl font-semibold text-base-content flex items-center gap-2 border-b border-base-300 pb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
        </svg>
        MCP Blockchain Tools
      </h2>
      
      <!-- Balance Check -->
      <Card title="Check XRPL Balance" subtitle="Retrieve the balance of an XRPL wallet address">
        <div class="flex flex-col gap-4 mt-4">
          <Input 
            bind:value={address} 
            placeholder="e.g. rK...1E..." 
            label="Wallet Address"
            fullWidth
          />
          <Button 
            variant="primary" 
            onclick={checkBalance} 
            disabled={checkingBalance || !address}
            loading={checkingBalance}
            fullWidth
          >
            Get Balance
          </Button>
          {#if balanceResult}
            <div class="bg-base-200 text-success p-3 rounded-md text-sm overflow-x-auto mt-2 border border-base-300">
              <pre class="font-mono">{balanceResult}</pre>
            </div>
          {/if}
        </div>
      </Card>

      <!-- NFT Status Check -->
      <Card title="Check Robot NFT Status" subtitle="Verify if a robot design has been minted on-chain">
        <div class="flex flex-col gap-4 mt-4">
          <Input 
            bind:value={robotId} 
            placeholder="e.g. ROBOT-99X" 
            label="Robot ID"
            fullWidth
          />
          <Button 
            variant="primary" 
            onclick={checkNftStatus} 
            disabled={checkingNft || !robotId}
            loading={checkingNft}
            fullWidth
          >
            Check Status
          </Button>
          {#if nftStatusResult}
            <div class="bg-base-200 text-success p-3 rounded-md text-sm overflow-x-auto mt-2 border border-base-300">
              <pre class="font-mono">{nftStatusResult}</pre>
            </div>
          {/if}
        </div>
      </Card>
    </div>

    <!-- Manufacturing Section -->
    <div class="space-y-6">
      <h2 class="text-xl font-semibold text-base-content flex items-center gap-2 border-b border-base-300 pb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Manufacturing Logistics
      </h2>
      
      <Card title="Process Milestone Payment" subtitle="Execute on-chain payment for a completed milestone">
        <div class="flex flex-col gap-4 mt-4">
          <Input 
            bind:value={orderId} 
            label="Manufacturing Order ID"
            placeholder="e.g. MFG123456"
            fullWidth
          />
          <Input 
            bind:value={milestoneId} 
            label="Milestone ID"
            placeholder="e.g. milestone-1"
            fullWidth
          />
          <Input 
            bind:value={wallet} 
            label="Payer Wallet Address"
            placeholder="e.g. rP...9Q..."
            fullWidth
          />
          
          <div class="pt-4 mt-2 border-t border-base-200">
            <Button 
              variant="secondary" 
              onclick={payMilestone} 
              disabled={processingPayment || !orderId || !milestoneId || !wallet}
              loading={processingPayment}
              fullWidth
            >
              Execute Payment
            </Button>
          </div>

          {#if paymentResult}
            <div class="bg-base-200 text-success p-3 rounded-md text-sm mt-2 overflow-x-auto border border-base-300">
              <pre class="font-mono">{paymentResult}</pre>
            </div>
          {/if}
        </div>
      </Card>
    </div>
  </div>
</div>
