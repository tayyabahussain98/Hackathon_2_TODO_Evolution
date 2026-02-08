'use client';

/**
 * Auth Context Provider
 *
 * Implements Better Auth-based authentication system with JWT tokens.
 */

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  display_name?: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  session: { user: User } | null;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string, displayName: string) => Promise<void>;
  loading: boolean;
  updateUserFromToken: (token: string) => void;
  setTokenAndUser: (token: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on component mount
    const token = localStorage.getItem('token');
    if (token && token !== 'undefined' && token !== 'null') {
      try {
        // Decode JWT token to get user info (simplified)
        const tokenPayload = token.split('.')[1];
        if (tokenPayload) {
          const decoded = JSON.parse(atob(tokenPayload));
          setUser({
            id: decoded.sub || 'mock-user-id',
            email: decoded.email || 'mock@example.com',
            display_name: decoded.display_name || decoded.email || 'Mock User',
            name: decoded.name || decoded.email || 'Mock User'
          });
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  }, []);

  // Listen for storage changes to update auth state when token is set from other tabs/pages
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'token') {
        if (e.newValue && e.newValue !== 'undefined' && e.newValue !== 'null') {
          try {
            const tokenPayload = e.newValue.split('.')[1];
            if (tokenPayload) {
              const decoded = JSON.parse(atob(tokenPayload));
              setUser({
                id: decoded.sub || 'mock-user-id',
                email: decoded.email || 'mock@example.com',
                name: decoded.name || decoded.email || 'Mock User'
              });
            }
          } catch (error) {
            console.error('Error decoding token from storage change:', error);
            setUser(null);
          }
        } else {
          setUser(null);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  // Function to update auth state immediately when token is set programmatically
  const setTokenAndUser = (token: string) => {
    localStorage.setItem('token', token);

    // Trigger storage event to notify other components of the token change
    window.dispatchEvent(new StorageEvent('storage', {
      key: 'token',
      oldValue: null,
      newValue: token,
      url: window.location.href,
      storageArea: localStorage,
    }));

    // Update user state immediately
    try {
      const tokenPayload = token.split('.')[1];
      if (tokenPayload) {
        const decoded = JSON.parse(atob(tokenPayload));
        const userData = {
          id: decoded.sub || 'mock-user-id',
          email: decoded.email || 'mock@example.com',
          display_name: decoded.display_name || decoded.name || decoded.email || 'Mock User',
          name: decoded.name || decoded.display_name || decoded.email || 'Mock User'
        };
        setUser(userData);
        return userData;
      }
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      const { access_token } = data;

      if (!access_token) {
        throw new Error('No token received from server');
      }

      // Store token in localStorage
      localStorage.setItem('token', access_token);

      // Decode JWT to get user info and update user state immediately
      const tokenPayload = access_token.split('.')[1];
      if (tokenPayload) {
        const decoded = JSON.parse(atob(tokenPayload));
        const userData = {
          id: decoded.sub || 'mock-user-id',
          email: decoded.email || email,
          display_name: decoded.display_name || decoded.name || email,
          name: decoded.name || decoded.display_name || email
        };
        setUser(userData);
      } else {
        // Fallback: create a basic user object
        setUser({
          id: 'mock-user-id',
          email: email,
          display_name: email,
          name: email
        });
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };


  const signUp = async (email: string, password: string, displayName: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, display_name: displayName }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Registration failed');
      }

      const data = await response.json();
      const { access_token } = data;

      if (!access_token) {
        throw new Error('No token received from server');
      }

      // Store token in localStorage
      localStorage.setItem('token', access_token);

      // Decode JWT to get user info and update user state immediately
      const tokenPayload = access_token.split('.')[1];
      if (tokenPayload) {
        const decoded = JSON.parse(atob(tokenPayload));
        const userData = {
          id: decoded.sub || 'mock-user-id',
          email: decoded.email || email,
          display_name: decoded.display_name || displayName,
          name: decoded.name || decoded.display_name || displayName
        };
        setUser(userData);
      } else {
        // Fallback: create a basic user object
        setUser({
          id: 'mock-user-id',
          email: email,
          display_name: displayName,
          name: displayName
        });
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = async () => {
    try {
      // Get the token before removing it for the API call
      const token = localStorage.getItem('token');

      // Call backend logout endpoint
      if (token) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }).catch(() => {}); // Ignore errors during logout
      }

      // Remove token from localStorage
      const oldToken = localStorage.getItem('token');
      localStorage.removeItem('token');

      // Trigger storage event to notify other components of the token change
      window.dispatchEvent(new StorageEvent('storage', {
        key: 'token',
        oldValue: oldToken,
        newValue: null,
        url: window.location.href,
        storageArea: localStorage,
      }));

      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  // Function to manually update user from token
  const updateUserFromToken = (token: string) => {
    try {
      const tokenPayload = token.split('.')[1];
      if (tokenPayload) {
        const decoded = JSON.parse(atob(tokenPayload));
        const userData = {
          id: decoded.sub || 'mock-user-id',
          email: decoded.email || 'user@example.com',
          display_name: decoded.display_name || decoded.name || decoded.email || 'Mock User',
          name: decoded.name || decoded.display_name || decoded.email || 'Mock User'
        };
        setUser(userData);
        return userData;
      }
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };

  const value = {
    user,
    session: user ? { user } : null,
    signIn,
    signOut,
    signUp,
    loading,
    updateUserFromToken,
    setTokenAndUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
