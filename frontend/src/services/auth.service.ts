import ApiService from './api.service';

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

  private constructor() {
    this.apiService = ApiService.getInstance();
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async login(data: LoginData): Promise<LoginResponse> {
    const response = await this.apiService.post<LoginResponse>('/auth/login', data);
    if (response.access_token) {
      localStorage.setItem('token', response.access_token);
    }
    return response;
  }

  public async register(data: RegisterData): Promise<RegisterResponse> {
    return await this.apiService.post<RegisterResponse>('/auth/register', data);
  }

  public logout(): void {
    localStorage.removeItem('token');
    window.location.href = '/sign-in';
  }

  public isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  public getToken(): string | null {
    return localStorage.getItem('token');
  }
}

export default AuthService; 