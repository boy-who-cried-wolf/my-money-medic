import apiService from './api.service';

export interface Broker {
  id: string;
  user_id: string;
  license_number: string;
  license_status: 'active' | 'pending' | 'revoked' | 'expired';
  company_name?: string;
  years_of_experience: number;
  experience_level: string;
  office_address?: string;
  service_areas?: string[];
  bio?: string;
  profile_image?: string;
  website?: string;
  average_rating: number;
  success_rate: number;
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  specializations: Array<{
    id: string;
    name: string;
    created_at: string;
  }>;
}

export interface BrokerCreate {
  user_id: string;
  license_number: string;
  company_name?: string;
  years_of_experience: number;
  experience_level: string;
  office_address?: string;
  service_areas?: string[];
  bio?: string;
  profile_image?: string;
  website?: string;
  specialization_ids?: string[];
}

export interface BrokerUpdate {
  license_status?: 'active' | 'pending' | 'revoked' | 'expired';
  company_name?: string;
  years_of_experience?: number;
  experience_level?: string;
  office_address?: string;
  service_areas?: string[];
  bio?: string;
  profile_image?: string;
  website?: string;
  is_verified?: boolean;
}

class BrokerService {
  private readonly BASE_URL = '/brokers';

  async getBrokers(): Promise<Broker[]> {
    return apiService.get<Broker[]>(this.BASE_URL);
  }

  async getBroker(id: string): Promise<Broker> {
    return apiService.get<Broker>(`${this.BASE_URL}/${id}`);
  }

  async createBroker(broker: BrokerCreate): Promise<Broker> {
    return apiService.post<Broker>(this.BASE_URL, broker);
  }

  async updateBroker(id: string, broker: BrokerUpdate): Promise<Broker> {
    return apiService.put<Broker>(`${this.BASE_URL}/${id}`, broker);
  }

  async deleteBroker(id: string): Promise<void> {
    return apiService.delete(`${this.BASE_URL}/${id}`);
  }

  async toggleVerification(id: string): Promise<Broker> {
    return apiService.put<Broker>(`${this.BASE_URL}/${id}`, {
      is_verified: true,
    });
  }

  async searchBrokers(query: string): Promise<Broker[]> {
    return apiService.post<Broker[]>(`${this.BASE_URL}/search`, { query });
  }
}

export default new BrokerService(); 