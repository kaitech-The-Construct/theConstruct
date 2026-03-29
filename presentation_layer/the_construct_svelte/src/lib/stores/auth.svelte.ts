import type { User, LoginCredentials, RegisterData } from '$types';
import { apiClient } from '$services/api';
import { auth } from '$services/firebase';
import { 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  type User as FirebaseUser
} from 'firebase/auth';

/**
 * Svelte 5 AuthState class
 * Replaces Svelte 4 stores with explicit Runes ($state, $derived).
 */
class AuthState {
  user = $state<User | null>(null);
  isLoading = $state(true);
  authError = $state<string | null>(null);
  
  isAuthenticated = $derived(!!this.user);

  constructor() {
    this.init();
  }

  // Initialize auth state from Firebase
  init() {
    if (typeof window !== 'undefined') {
      onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
        if (firebaseUser) {
          try {
            const token = await firebaseUser.getIdToken();
            apiClient.setToken(token);
            
            // Try fetching the full user profile from the backend
            try {
              const profile = await apiClient.getCurrentUser();
              this.user = profile;
            } catch (err) {
              console.error("Failed to fetch user profile from backend", err);
              // Fallback user structure based on Firebase metadata if backend fails
              this.user = {
                id: firebaseUser.uid,
                email: firebaseUser.email || '',
                username: firebaseUser.displayName || firebaseUser.email?.split('@')[0] || '',
                is_active: true,
                created_at: firebaseUser.metadata.creationTime || new Date().toISOString()
              };
            }

            localStorage.setItem('user', JSON.stringify(this.user));
          } catch (error) {
            console.error('Error fetching token:', error);
            this.user = null;
            apiClient.clearToken();
            localStorage.removeItem('user');
          }
        } else {
          this.user = null;
          apiClient.clearToken();
          localStorage.removeItem('user');
        }
        
        this.isLoading = false;
      });
    } else {
      this.isLoading = false;
    }
  }

  // Login user using Firebase SDK
  async login(credentials: LoginCredentials) {
    this.isLoading = true;
    this.authError = null;

    try {
      const userCredential = await signInWithEmailAndPassword(
        auth, 
        credentials.username, 
        credentials.password
      );
      
      // onAuthStateChanged will handle the rest (token, fetching profile)
      return userCredential.user;
    } catch (error: any) {
      this.authError = error.message || 'Login failed';
      this.isLoading = false;
      throw error;
    }
  }

  // Register user via Backend (to create Firestore record), then sign in via Firebase SDK
  async register(userData: RegisterData) {
    this.isLoading = true;
    this.authError = null;

    try {
      // Create user via backend to ensure proper Firestore setup
      await apiClient.register(userData);
      
      // If successful, sign in directly with Firebase SDK
      const userCredential = await signInWithEmailAndPassword(
        auth, 
        userData.email, 
        userData.password
      );
      
      return userCredential.user;
    } catch (error: any) {
      this.authError = error.message || 'Registration failed';
      this.isLoading = false;
      throw error;
    }
  }

  // Logout user
  async logout() {
    this.isLoading = true;

    try {
      // Let Firebase handle the sign out process
      await signOut(auth);
      
      // Clear local state
      apiClient.clearToken();
      this.user = null;
      this.authError = null;

      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
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
      if (auth.currentUser) {
        const token = await auth.currentUser.getIdToken(true); // true forces refresh
        apiClient.setToken(token);
        return { access_token: token };
      }
      throw new Error("No current user");
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
