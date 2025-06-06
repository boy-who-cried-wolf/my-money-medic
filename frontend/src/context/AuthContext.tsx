import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth.service';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    phone?: string;
  }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const navigate = useNavigate();
  const [state, setState] = useState({
    isAuthenticated: AuthService.getInstance().isAuthenticated(),
    isLoading: false,
    error: null as string | null,
  });

  const login = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      await AuthService.getInstance().login({ email, password });
      setState(prev => ({ ...prev, isAuthenticated: true, isLoading: false }));
      navigate('/dashboard');
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An error occurred during login',
      }));
    }
  }, [navigate]);

  const register = useCallback(async (data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    phone?: string;
  }) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      await AuthService.getInstance().register({
        email: data.email,
        password: data.password,
        first_name: data.firstName,
        last_name: data.lastName,
        phone: data.phone,
      });
      // After successful registration, log the user in
      await login(data.email, data.password);
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error.response?.data?.detail || error.message || 'An error occurred during registration',
      }));
    }
  }, [login]);

  const logout = useCallback(() => {
    AuthService.getInstance().logout();
    setState(prev => ({ ...prev, isAuthenticated: false }));
  }, []);

  const value = {
    ...state,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}; 