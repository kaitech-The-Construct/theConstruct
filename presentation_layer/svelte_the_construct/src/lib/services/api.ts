import axios, { type AxiosInstance, type AxiosResponse } from 'axios';
import type { 
  ApiError, 
  ApiResponse, 
  AuthResponse, 
  LoginCredentials, 
  RegisterData, 
  User, 
  Product, 
  Order, 
  SearchFilters 
} from '$types';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL: string = 'http://localhost:8080') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        const apiError: ApiError = {
          status: error.response?.status || 500,
          message: error.response?.data?.detail || error.message,
          details: error.response?.data,
        };
        return Promise.reject(apiError);
      }
    );
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  loadToken() {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        this.token = token;
      }
    }
  }

  private async request<T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    endpoint: string,
    data?: any
  ): Promise<T> {
    const response: AxiosResponse<T> = await this.client.request({
      method,
      url: endpoint,
      data,
    });
    return response.data;
  }

  // Authentication endpoints
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await this.client.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    return this.request<AuthResponse>('POST', '/auth/register', userData);
  }

  async refreshToken(): Promise<{ access_token: string }> {
    return this.request<{ access_token: string }>('POST', '/auth/refresh');
  }

  async logout(): Promise<{ message: string }> {
    return this.request<{ message: string }>('POST', '/auth/logout');
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('GET', '/auth/profile');
  }

  async updateProfile(profileData: Partial<User>): Promise<User> {
    return this.request<User>('PUT', '/auth/profile', profileData);
  }

  // User endpoints
  async getUser(userId: string): Promise<User> {
    return this.request<User>('GET', `/users/${userId}`);
  }

  async updateUser(userId: string, userData: Partial<User>): Promise<User> {
    return this.request<User>('PUT', `/users/${userId}`, userData);
  }

  async deleteUser(userId: string): Promise<void> {
    return this.request<void>('DELETE', `/users/${userId}`);
  }

  // Product endpoints
  async getProducts(): Promise<Product[]> {
    return this.request<Product[]>('GET', '/robots');
  }

  async getProduct(productId: string): Promise<Product> {
    return this.request<Product>('GET', `/robots/${productId}`);
  }

  async createProduct(productData: Partial<Product>): Promise<Product> {
    return this.request<Product>('POST', '/robots', productData);
  }

  async updateProduct(productId: string, productData: Partial<Product>): Promise<Product> {
    return this.request<Product>('PUT', `/robots/${productId}`, productData);
  }

  async deleteProduct(productId: string): Promise<void> {
    return this.request<void>('DELETE', `/robots/${productId}`);
  }

  async searchProducts(filters: SearchFilters): Promise<Product[]> {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, value.toString());
      }
    });
    return this.request<Product[]>('GET', `/robots/search?${params.toString()}`);
  }

  async getRecommendations(userId: string): Promise<Product[]> {
    return this.request<Product[]>('GET', `/robots/recommendations/${userId}`);
  }

  // Order endpoints
  async createOrder(orderData: Partial<Order>): Promise<Order> {
    return this.request<Order>('POST', '/trades', orderData);
  }

  async getOrders(): Promise<Order[]> {
    return this.request<Order[]>('GET', '/trades');
  }

  async getOrder(orderId: string): Promise<Order> {
    return this.request<Order>('GET', `/trades/${orderId}`);
  }

  async updateOrderStatus(orderId: string, status: string): Promise<Order> {
    return this.request<Order>('PUT', `/trades/${orderId}`, { status });
  }

  async getUserOrders(userId: string): Promise<Order[]> {
    return this.request<Order[]>('GET', `/trades/user/${userId}`);
  }

  // Payment endpoints
  async processPayment(orderId: string, paymentData: any): Promise<any> {
    return this.request<any>('POST', `/trades/${orderId}/payment`, paymentData);
  }

  async trackOrder(orderId: string): Promise<any> {
    return this.request<any>('GET', `/trades/${orderId}/tracking`);
  }

  // Blockchain endpoints
  async connectWallet(walletData: any): Promise<any> {
    return this.request<any>('POST', '/auth/wallet/connect', walletData);
  }

  async getWalletBalance(address: string): Promise<any> {
    return this.request<any>('GET', `/blockchain/xrpl/balance/${address}`);
  }

  async createEscrow(escrowData: any): Promise<any> {
    return this.request<any>('POST', '/trades/escrow/create', escrowData);
  }

  async releaseEscrow(escrowId: string): Promise<any> {
    return this.request<any>('PUT', `/trades/escrow/${escrowId}/release`);
  }

  // Manufacturing endpoints
  async createRFQ(rfqData: any): Promise<any> {
    return this.request<any>('POST', '/manufacturing/rfq', rfqData);
  }

  async getQuotes(rfqId: string): Promise<any> {
    return this.request<any>('GET', `/manufacturing/rfq/${rfqId}/quotes`);
  }

  async createManufacturingOrder(orderData: any): Promise<any> {
    return this.request<any>('POST', '/manufacturing/orders', orderData);
  }

  async getManufacturingOrder(orderId: string): Promise<any> {
    return this.request<any>('GET', `/manufacturing/orders/${orderId}`);
  }
}

// Create and export a singleton instance
export const apiClient = new ApiClient();

// Export the class for testing or custom instances
export { ApiClient };
