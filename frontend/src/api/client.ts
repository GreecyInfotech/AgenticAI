const API_BASE = import.meta.env.VITE_API_URL || "";

export interface ApiError {
  title: string;
  detail: string;
  status: number;
}

export class ApiClientError extends Error {
  constructor(
    message: string,
    public status: number,
    public body?: ApiError,
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

function getToken(): string | null {
  return localStorage.getItem("access_token");
}

export function setToken(token: string): void {
  localStorage.setItem("access_token", token);
}

export function clearToken(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_subject");
  localStorage.removeItem("user_role");
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  auth = true,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (auth) {
    const token = getToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (!response.ok) {
    let body: ApiError | undefined;
    try {
      body = await response.json();
    } catch {
      /* empty */
    }
    throw new ApiClientError(
      body?.detail || body?.title || response.statusText,
      response.status,
      body,
    );
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in_minutes: number;
}

export interface UserProfile {
  subject: string;
  role: string;
}

export interface ConversationResponse {
  session_id: string;
  reply: string | null;
  target_agent: string | null;
  agent_results: Record<string, unknown>[];
  requires_escalation: boolean;
}

export interface OrderItem {
  sku: string;
  quantity: number;
  unit_price?: number;
  line_total?: number;
}

export interface Order {
  order_id: string;
  customer_id: string;
  status: string;
  total: number;
  items: OrderItem[];
}

export interface Paginated<T> {
  items: T[];
  next_cursor: string | null;
  total: number | null;
}

export interface Product {
  sku: string;
  name: string;
  price: number;
  category?: string;
}

export interface InventoryItem {
  sku: string;
  available: number;
  warehouse: string;
}

export interface Customer {
  customer_id: string;
  name: string;
  tier: string;
  credit_limit?: number;
}

export const api = {
  login: (subject: string, role: string) =>
    request<TokenResponse>("/api/v1/auth/token", {
      method: "POST",
      body: JSON.stringify({ subject, role }),
    }, false),

  getMe: () => request<UserProfile>("/api/v1/auth/me"),

  health: () =>
    request<{ status: string; service: string }>("/api/v1/health", {}, false),

  converse: (sessionId: string, customerId: string, message: string) =>
    request<ConversationResponse>("/api/v1/conversation", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, customer_id: customerId, message }),
    }),

  listProducts: (cursor?: string) => {
    const q = cursor ? `?cursor=${cursor}` : "";
    return request<Paginated<Product>>(`/api/v1/products${q}`);
  },

  getInventory: (sku: string) => request<InventoryItem>(`/api/v1/inventory/${sku}`),

  listOrders: (cursor?: string) => {
    const q = cursor ? `?cursor=${cursor}` : "";
    return request<Paginated<Order>>(`/api/v1/orders${q}`);
  },

  createOrder: (customerId: string, items: { sku: string; quantity: number }[], idempotencyKey?: string) =>
    request<Order>("/api/v1/orders", {
      method: "POST",
      headers: idempotencyKey ? { "Idempotency-Key": idempotencyKey } : {},
      body: JSON.stringify({ customer_id: customerId, items }),
    }),

  getCustomer: (customerId: string) => request<Customer>(`/api/v1/customers/${customerId}`),
};
