import type { User, LoginCredentials, RegisterData } from '$types';
import { apiClient } from '$services/api';

/**
 * Svelte 5 AuthState class
 * Replaces Svelte 4 stores with explicit Runes ($state, $derived).
 */
class AuthState {
  user = $state<User | null>(null);
  isLoading = $state(false);
  authError = $state<string | null>(null);
  
  isAuthenticated = $derived(!!this.user);

  constructor() {
    this.init();
  }

  // Initialize auth state from localStorage
  init() {
    if (typeof window !== 'undefined') {
      apiClient.loadToken();
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        try {
          this.user = JSON.parse(savedUser);
        } catch (e) {
          console.error('Failed to parse saved user:', e);
          localStorage.removeItem('user');
        }
      }
    }
  }

  // Login user
  async login(credentials: LoginCredentials) {
    this.isLoading = true;
    this.authError = null;

    try {
      const response = await apiClient.login(credentials);
      apiClient.setToken(response.access_token);
      this.user = response.user;

      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.user));
      }

      return response;
    } catch (error: any) {
      this.authError = error.message || 'Login failed';
      throw error;
    } finally {
      this.isLoading = false;
    }
  }

  // Register user
  async register(userData: RegisterData) {
    this.isLoading = true;
    this.authError = null;

    try {
      const response = await apiClient.register(userData);
      apiClient.setToken(response.access_token);
      this.user = response.user;

      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.user));
      }

      return response;
    } catch (error: any) {
      this.authError = error.message || 'Registration failed';
      throw error;
    } finally {
      this.isLoading = false;
    }
  }

  // Logout user
  async logout() {
    this.isLoading = true;

    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      apiClient.clearToken();
      this.user = null;
      this.authError = null;

      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
      }

      this.isLoading = false;
    }
  }

  // Update user profile
  async updateProfile(profileData: Partial<User>) {
    this.isLoading = true;
    this.authError = null;

    try {
      const updatedUser = await apiClient.updateProfile(profileData);
      this.user = updatedUser;

      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }

      return updatedUser;
    } catch (error: any) {
      this.authError = error.message || 'Profile update failed';
      throw error;
    } finally {
      this.isLoading = false;
    }
  }

  // Refresh token
  async refreshToken() {
    try {
      const response = await apiClient.refreshToken();
      apiClient.setToken(response.access_token);
      return response;
    } catch (error) {
      // If refresh fails, logout user
      this.logout();
      throw error;
    }
  }

  // Clear auth error
  clearError() {
    this.authError = null;
  }
}

// Export a singleton instance
export const authStore = new AuthState();
