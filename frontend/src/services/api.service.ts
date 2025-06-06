import axios from 'axios';

interface ApiConfig {
  baseURL: string;
  headers: Record<string, string>;
}

class ApiService {
  private static instance: ApiService;
  private api: ReturnType<typeof axios.create>;

  private constructor() {
    const config: ApiConfig = {
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    };

    this.api = axios.create(config);
    this.setupInterceptors();
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private setupInterceptors(): void {
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/sign-in';
        }
        return Promise.reject(error);
      }
    );
  }

  public async get<T>(url: string, config?: Record<string, unknown>): Promise<T> {
    const response = await this.api.get<T>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: unknown, config?: Record<string, unknown>): Promise<T> {
    const response = await this.api.post<T>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: unknown, config?: Record<string, unknown>): Promise<T> {
    const response = await this.api.put<T>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: Record<string, unknown>): Promise<T> {
    const response = await this.api.delete<T>(url, config);
    return response.data;
  }
}

export default ApiService; 