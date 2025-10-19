import { writable } from 'svelte/store';

function createUserStore() {
  const { subscribe, set, update } = writable({
    isConnected: false,
    address: null,
    balance: 0,
  });

  return {
    subscribe,
    set,
    update,
  };
}

export const userStore = createUserStore();
