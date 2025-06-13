import apiService from './api.service';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phoneNumber: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'admin' | 'broker' | 'client';
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  phone_number?: string;
}

class AuthService {
  private static instance: AuthService;
  private token: string | null = null;
  private user: User | null = null;

  private constructor() {
    // Initialize token from localStorage if available
    this.token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    if (userStr) {
      this.user = JSON.parse(userStr);
    }
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await apiService.post<AuthResponse>('/auth/login', credentials);
      const { access_token, token_type } = response;
      this.setToken(access_token);
      
      // Try to get user info after successful login, but don't fail if it doesn't work
      try {
        await this.getCurrentUser();
      } catch (userError) {
        console.warn('Failed to fetch user info:', userError);
        // Continue with login even if user fetch fails
      }
      
      return { access_token, token_type };
    } catch (error) {
      throw this.handleError(error);
    }
  }

  public async getCurrentUser(): Promise<User> {
    try {
      const response = await apiService.get<User>('/users/me');
      this.user = response;
      localStorage.setItem('user', JSON.stringify(response));
      return response;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  public async register(data: RegisterData): Promise<any> {
    try {
      return await apiService.post('/auth/register', data);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  public logout(): void {
    this.token = null;
    this.user = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  public getToken(): string | null {
    return this.token;
  }

  public getUser(): User | null {
    return this.user;
  }

  public isAdmin(): boolean {
    return this.user?.user_type === 'admin';
  }

  private setToken(token: string): void {
    this.token = token;
    localStorage.setItem('token', token);
  }

  private handleError(error: any): Error {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const errorMessage = error.response.data.detail || 'Authentication failed';
      throw new Error(errorMessage);
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error('No response from server');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new Error('Error setting up request');
    }
  }
}

export default AuthService.getInstance(); 