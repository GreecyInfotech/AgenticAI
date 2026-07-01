from __future__ import annotations

PERMISSIONS = {
    "admin": ["*"],
    "distributor": ["order:create", "order:read", "inventory:read"],
    "sales_rep": ["order:read", "customer:read"],
    "viewer": ["order:read"],
}
