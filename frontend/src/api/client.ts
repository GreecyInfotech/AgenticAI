export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly body?: unknown,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '';

function requestId(): string {
  return crypto.randomUUID();
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  if (!headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json');
  }
  if (!headers.has('X-Request-Id')) {
    headers.set('X-Request-Id', requestId());
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let body: unknown;
    try {
      body = await response.json();
    } catch {
      body = await response.text();
    }
    const message =
      typeof body === 'object' && body !== null && 'message' in body
        ? String((body as { message: string }).message)
        : `Request failed (${response.status})`;
    throw new ApiError(message, response.status, body);
  }

  const contentType = response.headers.get('content-type');
  if (contentType?.includes('application/json')) {
    return response.json() as Promise<T>;
  }
  return (await response.text()) as T;
}
