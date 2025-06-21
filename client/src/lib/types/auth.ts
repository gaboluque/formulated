export interface User {
  id: number;
  username: string;
  email: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  username?: string;
}

export interface AuthResponse {
  message: string;
  user: User;
}

export interface AuthError {
  error: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// Form validation types
export interface AuthFormErrors {
  email?: string;
  password?: string;
  username?: string;
  general?: string;
}

export interface PasswordResetData {
  email: string;
}

export interface PasswordResetConfirmData {
  token: string;
  password: string;
  confirmPassword: string;
} 