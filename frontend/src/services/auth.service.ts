import ApiService from './api.service';
import { User } from '../context/AuthContext';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface RegisterResponse {
  message: string;
  user: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    phone: string;
  };
}

interface LoginData {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
}

class AuthService {
  private static instance: AuthService;
  private apiService: ApiService;
  private user: User | null = null;

  private constructor() {
    this.apiService = ApiService.getInstance();
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public getUser(): User | null {
    return this.user;
  }

  public async login(email: string, password: string): Promise<void> {
    // TODO: Implement actual login logic
    this.user = {
      id: '1',
      email,
      firstName: 'John',
      lastName: 'Doe'
    };
  }

  public async register(data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    phone?: string;
  }): Promise<void> {
    // TODO: Implement actual registration logic
    this.user = {
      id: '1',
      email: data.email,
      firstName: data.firstName,
      lastName: data.lastName,
      phone: data.phone
    };
  }

  public logout(): void {
    this.user = null;
  }

  public isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  public getToken(): string | null {
    return localStorage.getItem('token');
  }
}

export default AuthService; 