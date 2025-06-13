import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig } from 'axios';
import authService from './auth.service';

class ApiService {
  private static instance: ApiService;
  private api: AxiosInstance;
  private isDevelopment: boolean;

  private constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development';
    const baseURL = this.isDevelopment 
      ? 'http://localhost:8000/api/v1'
      : '/api/v1';

    this.api = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for authentication
    this.api.interceptors.request.use(
      (config) => {
        const token = authService.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        const adminPrefix = this.isDevelopment ? '' : '/admin';
        const isLoginPage = window.location.pathname === `${adminPrefix}/login`;
        
        if (error.response?.status === 401 && !isLoginPage) {
          // Handle unauthorized access
          authService.logout();
          window.location.href = `${adminPrefix}/login`;
        } else if (error.response?.status === 403 && !isLoginPage) {
          // Handle forbidden access (not admin)
          if (!authService.isAdmin()) {
            alert('You are not authorized to access this page');
            authService.logout();
            window.location.href = `${adminPrefix}/login`;
          }
        }
        return Promise.reject(error);
      }
    );
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  public getApi(): AxiosInstance {
    return this.api;
  }

  public getAdminPrefix(): string {
    return this.isDevelopment ? '' : '/admin';
  }

  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.get<T>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.post<T>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.put<T>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.delete<T>(url, config);
    return response.data;
  }
}

export default ApiService.getInstance(); 