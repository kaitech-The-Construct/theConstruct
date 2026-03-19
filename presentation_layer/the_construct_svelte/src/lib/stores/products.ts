import { writable, derived } from 'svelte/store';
import type { Product, SearchFilters } from '$types';
import { apiClient } from '$services/api';

// Product state
export const products = writable<Product[]>([]);
export const currentProduct = writable<Product | null>(null);
export const searchQuery = writable<string>('');
export const searchFilters = writable<SearchFilters>({});
export const isLoading = writable(false);
export const error = writable<string | null>(null);

// Derived stores
export const filteredProducts = derived(
  [products, searchQuery, searchFilters],
  ([$products, $searchQuery, $searchFilters]) => {
    let filtered = $products;

    // Apply text search
    if ($searchQuery) {
      const query = $searchQuery.toLowerCase();
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(query) ||
        product.description.toLowerCase().includes(query) ||
        product.manufacturer.toLowerCase().includes(query)
      );
    }

    // Apply filters
    if ($searchFilters.category) {
      filtered = filtered.filter(product => product.category === $searchFilters.category);
    }

    if ($searchFilters.min_price !== undefined) {
      filtered = filtered.filter(product => product.price >= $searchFilters.min_price!);
    }

    if ($searchFilters.max_price !== undefined) {
      filtered = filtered.filter(product => product.price <= $searchFilters.max_price!);
    }

    if ($searchFilters.manufacturer) {
      filtered = filtered.filter(product => product.manufacturer === $searchFilters.manufacturer);
    }

    if ($searchFilters.min_rating !== undefined) {
      filtered = filtered.filter(product => product.ratings.average >= $searchFilters.min_rating!);
    }

    // Apply sorting
    if ($searchFilters.sort_by) {
      filtered.sort((a, b) => {
        let aValue: any, bValue: any;
        
        switch ($searchFilters.sort_by) {
          case 'price':
            aValue = a.price;
            bValue = b.price;
            break;
          case 'rating':
            aValue = a.ratings.average;
            bValue = b.ratings.average;
            break;
          case 'date':
            aValue = new Date(a.created_at);
            bValue = new Date(b.created_at);
            break;
          case 'name':
            aValue = a.name.toLowerCase();
            bValue = b.name.toLowerCase();
            break;
          default:
            return 0;
        }

        if ($searchFilters.sort_order === 'desc') {
          return bValue > aValue ? 1 : bValue < aValue ? -1 : 0;
        } else {
          return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
        }
      });
    }

    return filtered;
  }
);

// Product actions
export const productStore = {
  // Load all products
  loadProducts: async () => {
    isLoading.set(true);
    error.set(null);
    
    try {
      const productList = await apiClient.getProducts();
      products.set(productList);
    } catch (err: any) {
      error.set(err.message || 'Failed to load products');
      console.error('Failed to load products:', err);
    } finally {
      isLoading.set(false);
    }
  },

  // Load single product
  loadProduct: async (productId: string) => {
    isLoading.set(true);
    error.set(null);
    
    try {
      const product = await apiClient.getProduct(productId);
      currentProduct.set(product);
      return product;
    } catch (err: any) {
      error.set(err.message || 'Failed to load product');
      console.error('Failed to load product:', err);
      throw err;
    } finally {
      isLoading.set(false);
    }
  },

  // Search products
  searchProducts: async (filters: SearchFilters) => {
    isLoading.set(true);
    error.set(null);
    
    try {
      const results = await apiClient.searchProducts(filters);
      products.set(results);
      searchFilters.set(filters);
    } catch (err: any) {
      error.set(err.message || 'Search failed');
      console.error('Search failed:', err);
    } finally {
      isLoading.set(false);
    }
  },

  // Get recommendations
  getRecommendations: async (userId: string) => {
    try {
      const recommendations = await apiClient.getRecommendations(userId);
      return recommendations;
    } catch (err: any) {
      console.error('Failed to get recommendations:', err);
      return [];
    }
  },

  // Update search query
  setSearchQuery: (query: string) => {
    searchQuery.set(query);
  },

  // Update search filters
  setSearchFilters: (filters: SearchFilters) => {
    searchFilters.set(filters);
  },

  // Clear current product
  clearCurrentProduct: () => {
    currentProduct.set(null);
  },

  // Clear error
  clearError: () => {
    error.set(null);
  }
};
