<script>
  import { userStore } from '$lib/stores/userStore';
  import { connectWallet, disconnectWallet } from '$lib/services/xrplClient';

  let showDropdown = false;

  function toggleDropdown() {
    showDropdown = !showDropdown;
  }

  function truncateAddress(address) {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  }
</script>

<header>
  <nav>
    <a href="/" class="logo">The Construct</a>
    <ul>
      <li><a href="/marketplace">Marketplace</a></li>
      {#if $userStore.isConnected}
        <li><a href="/account/orders">My Orders</a></li>
      {/if}
    </ul>
  </nav>
  <div class="wallet-section">
    {#if $userStore.isConnected}
      <div class="wallet-info" on:click={toggleDropdown}>
        <span>{truncateAddress($userStore.address)}</span>
        {#if showDropdown}
          <div class="dropdown">
            <button on:click={disconnectWallet}>Disconnect</button>
          </div>
        {/if}
      </div>
    {:else}
      <button on:click={connectWallet}>Connect Wallet</button>
    {/if}
  </div>
</header>

<style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
  }
  nav {
    display: flex;
    align-items: center;
  }
  .logo {
    font-weight: bold;
    font-size: 1.5rem;
    text-decoration: none;
    color: #333;
  }
  ul {
    list-style: none;
    display: flex;
    margin: 0 0 0 2rem;
    padding: 0;
  }
  li {
    margin-right: 1.5rem;
  }
  a {
    text-decoration: none;
    color: #555;
    font-weight: 500;
  }
  .wallet-section {
    position: relative;
  }
  .wallet-info {
    cursor: pointer;
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  .dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background: white;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-top: 0.5rem;
    z-index: 10;
  }
  button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
  }
</style>
