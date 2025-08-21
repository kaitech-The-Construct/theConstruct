import { writable, derived } from 'svelte/store';
import type { CartItem, Product } from '$types';

// Cart state
export const cartItems = writable<CartItem[]>([]);
export const isCartOpen = writable(false);

// Derived stores
export const cartTotal = derived(cartItems, ($cartItems) =>
  $cartItems.reduce((total, item) => total + (item.price * item.quantity), 0)
);

export const cartItemCount = derived(cartItems, ($cartItems) =>
  $cartItems.reduce((count, item) => count + item.quantity, 0)
);

// Cart actions
export const cartStore = {
  // Initialize cart from localStorage
  init: () => {
    if (typeof window !== 'undefined') {
      const savedCart = localStorage.getItem('cart');
      if (savedCart) {
        try {
          cartItems.set(JSON.parse(savedCart));
        } catch (e) {
          console.error('Failed to parse saved cart:', e);
          localStorage.removeItem('cart');
        }
      }
    }
  },

  // Add item to cart
  addItem: (product: Product, quantity: number = 1) => {
    cartItems.update(items => {
      const existingItem = items.find(item => item.product_id === product.id);
      
      if (existingItem) {
        existingItem.quantity += quantity;
        return items;
      } else {
        const newItem: CartItem = {
          product_id: product.id,
          product,
          quantity,
          price: product.price
        };
        return [...items, newItem];
      }
    });
    
    cartStore.saveToStorage();
  },

  // Remove item from cart
  removeItem: (productId: string) => {
    cartItems.update(items => items.filter(item => item.product_id !== productId));
    cartStore.saveToStorage();
  },

  // Update item quantity
  updateQuantity: (productId: string, quantity: number) => {
    if (quantity <= 0) {
      cartStore.removeItem(productId);
      return;
    }

    cartItems.update(items => {
      const item = items.find(item => item.product_id === productId);
      if (item) {
        item.quantity = quantity;
      }
      return items;
    });
    
    cartStore.saveToStorage();
  },

  // Clear cart
  clearCart: () => {
    cartItems.set([]);
    cartStore.saveToStorage();
  },

  // Toggle cart visibility
  toggleCart: () => {
    isCartOpen.update(open => !open);
  },

  // Open cart
  openCart: () => {
    isCartOpen.set(true);
  },

  // Close cart
  closeCart: () => {
    isCartOpen.set(false);
  },

  // Save cart to localStorage
  saveToStorage: () => {
    if (typeof window !== 'undefined') {
      cartItems.subscribe(items => {
        localStorage.setItem('cart', JSON.stringify(items));
      })();
    }
  }
};
