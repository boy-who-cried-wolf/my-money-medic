import React, { createContext, useContext, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth.service';

export interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  phone?: string;
}

export interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    phone?: string;
  }) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const navigate = useNavigate();
  const [state, setState] = useState({
    isAuthenticated: AuthService.getInstance().getUser() !== null,
    user: AuthService.getInstance().getUser(),
    isLoading: false,
    error: null as string | null,
  });

  const login = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      await AuthService.getInstance().login(email, password);
      setState(prev => ({
        ...prev,
        isAuthenticated: true,
        user: AuthService.getInstance().getUser(),
        isLoading: false
      }));
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An error occurred during login'
      }));
      throw error;
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
      await AuthService.getInstance().register(data);
      setState(prev => ({
        ...prev,
        isAuthenticated: true,
        user: AuthService.getInstance().getUser(),
        isLoading: false
      }));
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration failed:', error);
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An error occurred during registration'
      }));
      throw error;
    }
  }, [navigate]);

  const logout = useCallback(() => {
    AuthService.getInstance().logout();
    setState(prev => ({
      ...prev,
      isAuthenticated: false,
      user: null
    }));
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, logout, register }}>
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