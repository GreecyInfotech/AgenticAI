import { useState, useCallback } from 'react';
import axios from 'axios';

const TOKEN_KEY = 'smart_port_token';

export function useAuth() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));

  const login = useCallback(async (username: string, password: string) => {
    const { data } = await axios.post('/api/v1/auth/login', { username, password });
    localStorage.setItem(TOKEN_KEY, data.access_token);
    setToken(data.access_token);
    return data;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
  }, []);

  return { token, isAuthenticated: !!token, login, logout };
}
