import apiService from './api.service';

export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  user_type: 'client' | 'broker' | 'admin';
  is_active: boolean;
  created_at: string;
  updated_at: string;
  is_verified: boolean;
  phone_number?: string;
}

export interface UserCreate {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  user_type: 'client' | 'broker' | 'admin';
}

export interface UserUpdate {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone_number?: string;
  user_type?: 'client' | 'broker' | 'admin';
  is_active?: boolean;
}

class UserService {
  // Static mock data for development until backend is ready
  private static mockUsers: User[] = [
    {
      id: '1',
      first_name: 'John',
      last_name: 'Doe',
      email: 'john.doe@example.com',
      user_type: 'admin',
      is_active: true,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-03-15T10:30:00Z',
      is_verified: true
    },
    {
      id: '2',
      first_name: 'Jane',
      last_name: 'Smith',
      email: 'jane.smith@example.com',
      user_type: 'broker',
      is_active: true,
      created_at: '2024-01-15T00:00:00Z',
      updated_at: '2024-03-14T15:45:00Z',
      is_verified: true
    },
    {
      id: '3',
      first_name: 'Mike',
      last_name: 'Johnson',
      email: 'mike.johnson@example.com',
      user_type: 'client',
      is_active: false,
      created_at: '2024-02-01T00:00:00Z',
      updated_at: '2024-03-10T09:20:00Z',
      is_verified: true
    },
    {
      id: '4',
      first_name: 'Sarah',
      last_name: 'Williams',
      email: 'sarah.williams@example.com',
      user_type: 'broker',
      is_active: true,
      created_at: '2024-02-15T00:00:00Z',
      updated_at: '2024-03-15T08:15:00Z',
      is_verified: true
    },
    {
      id: '5',
      first_name: 'David',
      last_name: 'Brown',
      email: 'david.brown@example.com',
      user_type: 'client',
      is_active: true,
      created_at: '2024-03-01T00:00:00Z',
      updated_at: '2024-03-13T14:30:00Z',
      is_verified: true
    }
  ];

  async getUsers(): Promise<User[]> {
    try {
      // Try to fetch from backend first
      const response = await apiService.get<User[]>('/users');
      return response;
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      return Promise.resolve(UserService.mockUsers);
    }
  }

  async createUser(userData: UserCreate): Promise<User> {
    try {
      // Try to create user in backend
      const response = await apiService.post<User>('/users', userData);
      return response;
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      const newUser: User = {
        ...userData,
        id: Math.random().toString(36).substr(2, 9),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_verified: true,
        is_active: true
      };
      return Promise.resolve(newUser);
    }
  }

  async updateUser(id: string, userData: UserUpdate): Promise<User> {
    try {
      // Try to update user in backend
      const response = await apiService.put<User>(`/users/${id}`, userData);
      return response;
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      const user = UserService.mockUsers.find(u => u.id === id);
      if (!user) {
        throw new Error('User not found');
      }
      const updatedUser = { ...user, ...userData };
      return Promise.resolve(updatedUser);
    }
  }

  async deleteUser(id: string): Promise<void> {
    try {
      // Try to delete user in backend
      await apiService.delete(`/users/${id}`);
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      const index = UserService.mockUsers.findIndex(u => u.id === id);
      if (index !== -1) {
        UserService.mockUsers.splice(index, 1);
      }
      return Promise.resolve();
    }
  }

  async toggleUserStatus(id: string): Promise<User> {
    try {
      // Try to update user status in backend
      const user = await this.getUserById(id);
      const response = await apiService.put<User>(`/users/${id}`, {
        is_active: !user.is_active
      });
      return response;
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      const user = UserService.mockUsers.find(u => u.id === id);
      if (!user) {
        throw new Error('User not found');
      }
      const updatedUser = { ...user, is_active: !user.is_active };
      return Promise.resolve(updatedUser);
    }
  }

  async getUserById(id: string): Promise<User> {
    try {
      // Try to get user from backend
      const response = await apiService.get<User>(`/users/${id}`);
      return response;
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      const user = UserService.mockUsers.find(u => u.id === id);
      if (!user) {
        throw new Error('User not found');
      }
      return Promise.resolve(user);
    }
  }

  async searchUsers(query: string, userType?: string): Promise<User[]> {
    try {
      // Try to search users in backend
      const params = new URLSearchParams();
      if (query) params.append('search', query);
      if (userType) params.append('user_type', userType);
      const response = await apiService.get<User[]>(`/users?${params.toString()}`);
      return response;
    } catch (error) {
      console.warn('Backend not available, using mock data:', error);
      // Fallback to mock data if backend is not available
      return Promise.resolve(
        UserService.mockUsers.filter(user => {
          const matchesSearch = 
            user.first_name.toLowerCase().includes(query.toLowerCase()) ||
            user.last_name.toLowerCase().includes(query.toLowerCase()) ||
            user.email.toLowerCase().includes(query.toLowerCase());
          const matchesType = !userType || user.user_type === userType;
          return matchesSearch && matchesType;
        })
      );
    }
  }
}

export default new UserService(); 