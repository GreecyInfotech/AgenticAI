import { useCallback, useEffect, useState } from 'react';

const SESSION_KEY = 'bfsi.sessionId';
const CUSTOMER_KEY = 'bfsi.customerId';

const defaultCustomerId =
  import.meta.env.VITE_DEFAULT_CUSTOMER_ID ?? 'CUST-12345';

export function useSession() {
  const [sessionId, setSessionId] = useState(() => {
    const stored = sessionStorage.getItem(SESSION_KEY);
    if (stored) return stored;
    const id = crypto.randomUUID();
    sessionStorage.setItem(SESSION_KEY, id);
    return id;
  });

  const [customerId, setCustomerId] = useState(
    () => sessionStorage.getItem(CUSTOMER_KEY) ?? defaultCustomerId,
  );

  useEffect(() => {
    sessionStorage.setItem(SESSION_KEY, sessionId);
  }, [sessionId]);

  useEffect(() => {
    sessionStorage.setItem(CUSTOMER_KEY, customerId);
  }, [customerId]);

  const resetSession = useCallback(() => {
    const id = crypto.randomUUID();
    setSessionId(id);
    sessionStorage.setItem(SESSION_KEY, id);
  }, []);

  return { sessionId, customerId, setCustomerId, resetSession };
}
