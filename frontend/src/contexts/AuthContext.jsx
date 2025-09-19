import { createContext, useContext, useState, useEffect } from 'react';
import { login as loginApi, getCurrentUser, logout as logoutApi } from '../api/authApi';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on app load
  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('token');
      
      if (token) {
        try {
          const userData = await getCurrentUser(token);
          setUser(userData);
        } catch (error) {
          // Token is invalid, remove it
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      }
      
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (credentials) => {
    try {
      const response = await loginApi(credentials);
      
      // Store token
      localStorage.setItem('token', response.access_token);
      
      // Get user data
      const userData = await getCurrentUser(response.access_token);
      setUser(userData);
      
      return response;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    logoutApi(); // This removes tokens from localStorage
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user
  };
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};