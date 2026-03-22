<script lang="ts">
  import { onMount } from 'svelte';
  import { manufacturingStore } from '$stores/manufacturing';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';
  import Input from '$components/ui/Input.svelte';

  // RFQ State
  let rfqPartName = '';
  let rfqQuantity = 1;
  let rfqSpecs = '';
  let rfqResult: any = null;
  let rfqError: string | null = null;
  let isSubmittingRfq = false;

  // Order Tracking State
  let lookupOrderId = '';
  let walletAddress = '';
  let paymentResult: string | null = null;
  let paymentError: string | null = null;
  let payingMilestoneId: string | null = null;

  async function handleSubmitRfq() {
    isSubmittingRfq = true;
    rfqResult = null;
    rfqError = null;
    
    try {
      const data = await manufacturingStore.submitRFQ({
        part_name: rfqPartName,
        quantity: Number(rfqQuantity),
        specifications: rfqSpecs
      });
      rfqResult = data;
      // Clear form
      rfqPartName = '';
      rfqQuantity = 1;
      rfqSpecs = '';
    } catch (err: any) {
      rfqError = err.message || 'Failed to submit Request for Quote.';
    } finally {
      isSubmittingRfq = false;
    }
  }

  async function handleLoadOrder() {
    if (!lookupOrderId) return;
    paymentResult = null;
    paymentError = null;
    try {
      await manufacturingStore.loadOrder(lookupOrderId);
    } catch (err: any) {
      // Error handled in store
    }
  }

  async function handlePayMilestone(milestoneId: string) {
    if (!walletAddress) {
      paymentError = 'Please provide a wallet address to process payment.';
      return;
    }
    payingMilestoneId = milestoneId;
    paymentResult = null;
    paymentError = null;
    
    try {
      const data = await manufacturingStore.payMilestone(lookupOrderId, milestoneId, walletAddress);
      paymentResult = `Payment successful! Tx Hash: ${data.tx_hash}`;
    } catch (err: any) {
      paymentError = err.message || 'Payment failed.';
    } finally {
      payingMilestoneId = null;
    }
  }
</script>

<svelte:head>
  <title>Manufacturing | The Construct</title>
</svelte:head>

<div class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8 animate-fade-in">
  <div class="flex flex-col gap-2">
    <h1 class="text-3xl font-bold text-base-content">Manufacturing Dashboard</h1>
    <p class="text-base-content/70">Request quotes, manage manufacturing orders, and process on-chain milestone payments.</p>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <!-- Submit RFQ Section -->
    <div class="space-y-6">
      <h2 class="text-2xl font-semibold text-base-content flex items-center gap-2 border-b border-base-300 pb-2">
        <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        Request For Quote (RFQ)
      </h2>
      
      <Card shadow={true}>
        <div class="flex flex-col gap-4">
          <Input 
            label="Part Name / Description" 
            placeholder="e.g. Servo Motor Bracket v2"
            bind:value={rfqPartName}
            fullWidth
          />
          <Input 
            type="number"
            label="Quantity" 
            min={1}
            bind:value={rfqQuantity}
            fullWidth
          />
          <div class="form-control w-full">
            <label class="label" for="specs">
              <span class="label-text font-medium text-base-content">Specifications / Details</span>
            </label>
            <textarea 
              id="specs"
              class="textarea textarea-bordered w-full min-h-[100px]" 
              placeholder="Material requirements, tolerances, etc."
              bind:value={rfqSpecs}
            ></textarea>
          </div>
          
          <Button 
            variant="primary" 
            fullWidth 
            loading={isSubmittingRfq}
            disabled={!rfqPartName || !rfqSpecs || isSubmittingRfq}
            onclick={handleSubmitRfq}
          >
            Submit RFQ
          </Button>
          
          {#if rfqError}
            <div class="text-error text-sm mt-2">{rfqError}</div>
          {/if}
          
          {#if rfqResult}
            <div class="bg-success/10 text-success p-4 rounded-md mt-4 border border-success/20">
              <h4 class="font-bold mb-1">RFQ Submitted Successfully!</h4>
              <p class="text-sm">RFQ ID: <span class="font-mono">{rfqResult.rfq_id}</span></p>
              <p class="text-sm text-success/80">Our manufacturing network is reviewing your request.</p>
            </div>
          {/if}
        </div>
      </Card>
    </div>

    <!-- Order Tracking Section -->
    <div class="space-y-6">
      <h2 class="text-2xl font-semibold text-base-content flex items-center gap-2 border-b border-base-300 pb-2">
        <svg class="w-6 h-6 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Order & Milestones Tracking
      </h2>
      
      <Card shadow={true}>
        <div class="flex gap-2">
          <Input 
            placeholder="Enter Order ID (e.g. MFG123...)"
            bind:value={lookupOrderId}
            fullWidth
          />
          <Button 
            variant="secondary" 
            onclick={handleLoadOrder}
            loading={$manufacturingStore.isLoading && !payingMilestoneId && !isSubmittingRfq}
            disabled={!lookupOrderId}
          >
            Track
          </Button>
        </div>
        
        {#if $manufacturingStore.error && !payingMilestoneId && !isSubmittingRfq}
          <div class="text-error text-sm mt-4">{$manufacturingStore.error}</div>
        {/if}

        {#if $manufacturingStore.activeOrder}
          <div class="mt-8 space-y-4 animate-slide-up">
            <div class="flex justify-between items-center border-b border-base-300 pb-2">
              <h3 class="font-bold text-lg">Order Details</h3>
              <span class="badge badge-primary uppercase">{$manufacturingStore.activeOrder.status}</span>
            </div>
            
            <p class="text-sm">
              <span class="font-medium text-base-content/70">Order ID:</span> 
              <span class="font-mono">{$manufacturingStore.activeOrder.order_id}</span>
            </p>

            <h4 class="font-bold mt-6 mb-2">Production Milestones</h4>
            {#if $manufacturingStore.milestones && $manufacturingStore.milestones.length > 0}
              <div class="space-y-4">
                {#each $manufacturingStore.milestones as milestone}
                  <div class="bg-base-200 rounded-lg p-4 border border-base-300 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div>
                      <p class="font-bold">{milestone.description}</p>
                      <div class="flex items-center gap-2 mt-1">
                        <span class="badge badge-sm" class:badge-success={milestone.status === 'completed'} class:badge-ghost={milestone.status !== 'completed'}>
                          {milestone.status}
                        </span>
                        {#if milestone.paid}
                          <span class="badge badge-sm badge-success badge-outline gap-1">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            Paid
                          </span>
                        {/if}
                      </div>
                      <p class="text-sm font-medium text-primary mt-2">Cost: {milestone.payment_amount} XRP</p>
                    </div>
                    
                    {#if milestone.status === 'completed' && !milestone.paid}
                      <div class="w-full sm:w-auto flex flex-col gap-2">
                        <Input 
                          placeholder="Payer Wallet Address"
                          bind:value={walletAddress}
                          size="sm"
                        />
                        <Button 
                          variant="primary" 
                          size="sm"
                          loading={payingMilestoneId === milestone.id}
                          disabled={payingMilestoneId !== null}
                          onclick={() => handlePayMilestone(milestone.id)}
                        >
                          Pay Milestone On-Chain
                        </Button>
                      </div>
                    {/if}
                  </div>
                {/each}
              </div>
              
              {#if paymentError}
                <div class="text-error text-sm mt-4 p-2 bg-error/10 rounded">{paymentError}</div>
              {/if}
              {#if paymentResult}
                <div class="text-success text-sm mt-4 p-2 bg-success/10 rounded break-all">{paymentResult}</div>
              {/if}
            {:else}
              <p class="text-base-content/50 italic">No milestones defined for this order.</p>
            {/if}
          </div>
        {/if}
      </Card>
    </div>
  </div>
</div>
