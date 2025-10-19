import { writable, derived } from 'svelte/store';
import type { User, LoginCredentials, RegisterData } from '$types';
import { apiClient } from '$services/api';

// Auth state
export const user = writable<User | null>(null);
export const isAuthenticated = derived(user, ($user) => !!$user);
export const isLoading = writable(false);
export const authError = writable<string | null>(null);

// Auth actions
export const authStore = {
  // Initialize auth state from localStorage
  init: () => {
    if (typeof window !== 'undefined') {
      apiClient.loadToken();
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        try {
          user.set(JSON.parse(savedUser));
        } catch (e) {
          console.error('Failed to parse saved user:', e);
          localStorage.removeItem('user');
        }
      }
    }
  },

  // Login user
  login: async (credentials: LoginCredentials) => {
    isLoading.set(true);
    authError.set(null);
    
    try {
      const response = await apiClient.login(credentials);
      apiClient.setToken(response.access_token);
      user.set(response.user);
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.user));
      }
      
      return response;
    } catch (error: any) {
      authError.set(error.message || 'Login failed');
      throw error;
    } finally {
      isLoading.set(false);
    }
  },

  // Register user
  register: async (userData: RegisterData) => {
    isLoading.set(true);
    authError.set(null);
    
    try {
      const response = await apiClient.register(userData);
      apiClient.setToken(response.access_token);
      user.set(response.user);
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.user));
      }
      
      return response;
    } catch (error: any) {
      authError.set(error.message || 'Registration failed');
      throw error;
    } finally {
      isLoading.set(false);
    }
  },

  // Logout user
  logout: async () => {
    isLoading.set(true);
    
    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      apiClient.clearToken();
      user.set(null);
      authError.set(null);
      
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
      }
      
      isLoading.set(false);
    }
  },

  // Update user profile
  updateProfile: async (profileData: Partial<User>) => {
    isLoading.set(true);
    authError.set(null);
    
    try {
      const updatedUser = await apiClient.updateProfile(profileData);
      user.set(updatedUser);
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
      
      return updatedUser;
    } catch (error: any) {
      authError.set(error.message || 'Profile update failed');
      throw error;
    } finally {
      isLoading.set(false);
    }
  },

  // Refresh token
  refreshToken: async () => {
    try {
      const response = await apiClient.refreshToken();
      apiClient.setToken(response.access_token);
      return response;
    } catch (error) {
      // If refresh fails, logout user
      authStore.logout();
      throw error;
    }
  },

  // Clear auth error
  clearError: () => {
    authError.set(null);
  }
};
