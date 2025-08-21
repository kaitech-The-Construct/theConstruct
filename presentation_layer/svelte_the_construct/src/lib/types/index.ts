// User Types
export interface User {
  id: string;
  email: string;
  username: string;
  profile?: UserProfile;
  wallets?: UserWallets;
  kyc?: KYCStatus;
  is_active: boolean;
  created_at: string;
}

export interface UserProfile {
  first_name?: string;
  last_name?: string;
  avatar?: string;
  bio?: string;
}

export interface UserWallets {
  xrpl?: string;
  solana?: string;
}

export interface KYCStatus {
  status: 'pending' | 'verified' | 'rejected';
  documents?: string[];
  verified_at?: string;
}

// Authentication Types
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Product Types
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  category: string;
  manufacturer: string;
  images: string[];
  specifications: ProductSpecifications;
  ratings: ProductRatings;
  inventory: ProductInventory;
  status: 'active' | 'inactive' | 'sold';
  created_at: string;
}

export interface ProductSpecifications {
  technical: Record<string, any>;
  compatibility: string[];
  dimensions: Record<string, number>;
}

export interface ProductRatings {
  average: number;
  count: number;
  reviews: string[];
}

export interface ProductInventory {
  available: number;
  reserved: number;
  total: number;
}

// Order Types
export interface Order {
  id: string;
  buyer_id: string;
  seller_id: string;
  items: OrderItem[];
  total_price: number;
  currency: string;
  status: OrderStatus;
  created_at: string;
}

export interface OrderItem {
  product_id: string;
  quantity: number;
  unit_price: number;
}

export type OrderStatus = 
  | 'created' 
  | 'paid' 
  | 'processing' 
  | 'shipped' 
  | 'delivered' 
  | 'completed' 
  | 'cancelled';

// Cart Types
export interface CartItem {
  product_id: string;
  product: Product;
  quantity: number;
  price: number;
}

// API Types
export interface ApiError {
  status: number;
  message: string;
  details?: any;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

// Search and Filter Types
export interface SearchFilters {
  query?: string;
  category?: string;
  min_price?: number;
  max_price?: number;
  manufacturer?: string;
  min_rating?: number;
  sort_by?: 'price' | 'rating' | 'date' | 'name';
  sort_order?: 'asc' | 'desc';
}

// Notification Types
export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  created_at: string;
}

// Blockchain Types
export interface WalletConnection {
  type: 'xrpl' | 'solana' | 'ethereum';
  address: string;
  connected: boolean;
}

export interface Transaction {
  id: string;
  hash: string;
  from: string;
  to: string;
  amount: number;
  currency: string;
  status: 'pending' | 'confirmed' | 'failed';
  created_at: string;
}
