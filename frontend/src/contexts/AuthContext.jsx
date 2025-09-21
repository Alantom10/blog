import { createContext, useContext, useState, useEffect } from "react";
import {
  login as loginApi,
  getCurrentUser,
  logout as logoutApi,
} from "../api/authApi";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on app load
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Try to get user data using cookie
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (error) {
        // No valid session
        setUser(null);
      }

      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (credentials) => {
    try {
      await loginApi(credentials);

      // Get user data
      const userData = await getCurrentUser();
      setUser(userData);
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    await logoutApi(); // This removes tokens from localStorage
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
