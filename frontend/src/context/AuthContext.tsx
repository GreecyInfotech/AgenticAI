import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api, clearToken, setToken } from "../api/client";

interface AuthState {
  subject: string;
  role: string;
  token: string;
}

interface AuthContextValue {
  user: AuthState | null;
  loading: boolean;
  login: (subject: string, role: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthState | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const subject = localStorage.getItem("user_subject");
    const role = localStorage.getItem("user_role");
    if (token && subject && role) {
      setUser({ token, subject, role });
    }
    setLoading(false);
  }, []);

  const login = useCallback(async (subject: string, role: string) => {
    const res = await api.login(subject, role);
    setToken(res.access_token);
    localStorage.setItem("user_subject", subject);
    localStorage.setItem("user_role", role);
    setUser({ token: res.access_token, subject, role });
  }, []);

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const value = useMemo(() => ({ user, loading, login, logout }), [user, loading, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
