import { userStore } from '$lib/stores/userStore';

// Mock functions for wallet interaction
export function connectWallet() {
  // In a real app, this would use a library like Xumm or gemwallet
  console.log('Simulating wallet connection...');
  userStore.update(state => ({
    ...state,
    isConnected: true,
    address: 'rPsmM6C6G8c6JMA4p6pG24a42d2C4A4d2C', // Example address
    balance: 1000, // Example balance
  }));
  console.log('Wallet connected.');
}

export function disconnectWallet() {
  console.log('Simulating wallet disconnection...');
  userStore.set({
    isConnected: false,
    address: null,
    balance: 0,
  });
  console.log('Wallet disconnected.');
}

export async function createEscrow(productId, amount) {
  return new Promise((resolve) => {
    console.log(`Simulating EscrowCreate transaction for product ${productId} with amount ${amount}...`);
    setTimeout(() => {
      console.log('Escrow created successfully.');
      // In a real app, you'd get a new order ID from the transaction result
      const newOrder = { id: Date.now(), productId, status: 'In Escrow', date: new Date().toISOString() };
      // For the mock, we'll just resolve it. The page will handle adding it to a local store.
      resolve(newOrder);
    }, 1500);
  });
}

export async function finishEscrow(orderId) {
  return new Promise((resolve) => {
    console.log(`Simulating EscrowFinish transaction for order ${orderId}...`);
    setTimeout(() => {
      console.log('Escrow finished successfully.');
      resolve({ success: true });
    }, 1000);
  });
}

export async function cancelEscrow(orderId) {
  return new Promise((resolve) => {
    console.log(`Simulating EscrowCancel transaction for order ${orderId}...`);
    setTimeout(() => {
      console.log('Escrow canceled successfully.');
      resolve({ success: true });
    }, 1000);
  });
}
