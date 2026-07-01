import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NAV = [
  { to: "/", label: "Dashboard", icon: "◈" },
  { to: "/conversation", label: "AI Assistant", icon: "✦" },
  { to: "/orders", label: "Orders", icon: "◎" },
  { to: "/products", label: "Products", icon: "▣" },
  { to: "/inventory", label: "Inventory", icon: "⬡" },
];

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">AI</span>
          <div>
            <strong>Distributor</strong>
            <small>Ordering Platform</small>
          </div>
        </div>
        <nav className="nav">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="user-chip">
            <span className="user-avatar">{user?.subject.slice(0, 2).toUpperCase()}</span>
            <div>
              <div className="user-name">{user?.subject}</div>
              <div className="user-role">{user?.role}</div>
            </div>
          </div>
          <button type="button" className="btn-ghost" onClick={logout}>
            Sign out
          </button>
        </div>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
