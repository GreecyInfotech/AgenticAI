import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { HomePage } from '@/pages/HomePage';
import { CustomerPortal } from '@/pages/CustomerPortal';
import { EmployeePortal } from '@/pages/EmployeePortal';
import { AdminPortal } from '@/pages/AdminPortal';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/customer" element={<CustomerPortal />} />
        <Route path="/employee" element={<EmployeePortal />} />
        <Route path="/admin" element={<AdminPortal />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
