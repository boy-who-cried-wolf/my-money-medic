import apiService from './api.service';

export interface CacheSettings {
  enabled: boolean;
  maxSize: number;
  currentSize: number;
  ttl: number;
}

export interface SecuritySettings {
  twoFactorEnabled: boolean;
  sessionTimeout: number;
  maxLoginAttempts: number;
  passwordExpiry: number;
}

export interface ApiSettings {
  rateLimit: number;
  timeout: number;
  maxRetries: number;
  baseUrl: string;
}

export interface NotificationSettings {
  email: boolean;
  sms: boolean;
  push: boolean;
  alertThreshold: number;
}

export interface SystemSettings {
  cache: CacheSettings;
  security: SecuritySettings;
  api: ApiSettings;
  notifications: NotificationSettings;
}

class SettingsService {
  // Mock data for development
  private static mockSettings: SystemSettings = {
    cache: {
      enabled: true,
      maxSize: 1024,
      currentSize: 512,
      ttl: 30
    },
    security: {
      twoFactorEnabled: true,
      sessionTimeout: 60,
      maxLoginAttempts: 5,
      passwordExpiry: 90
    },
    api: {
      rateLimit: 100,
      timeout: 30,
      maxRetries: 3,
      baseUrl: 'http://localhost:8000/api/v1'
    },
    notifications: {
      email: true,
      sms: false,
      push: true,
      alertThreshold: 80
    }
  };

  async getSettings(): Promise<SystemSettings> {
    try {
      // When backend is ready, uncomment this:
      // return await apiService.get<SystemSettings>('/settings');
      
      // For now, return mock data
      return Promise.resolve(SettingsService.mockSettings);
    } catch (error) {
      console.error('Error fetching settings:', error);
      throw error;
    }
  }

  async updateSettings(settings: SystemSettings): Promise<SystemSettings> {
    try {
      // When backend is ready, uncomment this:
      // return await apiService.put<SystemSettings>('/settings', settings);
      
      // For now, update mock data and return
      SettingsService.mockSettings = settings;
      return Promise.resolve(settings);
    } catch (error) {
      console.error('Error updating settings:', error);
      throw error;
    }
  }
}

export default new SettingsService(); 