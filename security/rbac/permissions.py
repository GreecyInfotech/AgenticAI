"""Role-Based Access Control definitions."""

from enum import Enum


class Permission(str, Enum):
    VESSEL_READ = "vessel:read"
    VESSEL_WRITE = "vessel:write"
    CONTAINER_READ = "container:read"
    CONTAINER_WRITE = "container:write"
    CUSTOMS_READ = "customs:read"
    CUSTOMS_WRITE = "customs:write"
    CUSTOMS_APPROVE = "customs:approve"
    BILLING_READ = "billing:read"
    BILLING_WRITE = "billing:write"
    AGENT_INVOKE = "agent:invoke"
    ML_PREDICT = "ml:predict"
    ADMIN_ALL = "admin:*"
    EXECUTIVE_READ = "executive:read"
    MAINTENANCE_READ = "maintenance:read"
    MAINTENANCE_WRITE = "maintenance:write"


ROLE_PERMISSIONS: dict[str, list[Permission]] = {
    "admin": list(Permission),
    "operator": [
        Permission.VESSEL_READ, Permission.VESSEL_WRITE,
        Permission.CONTAINER_READ, Permission.CONTAINER_WRITE,
        Permission.AGENT_INVOKE, Permission.ML_PREDICT,
    ],
    "customs_officer": [
        Permission.CUSTOMS_READ, Permission.CUSTOMS_WRITE, Permission.CUSTOMS_APPROVE,
        Permission.VESSEL_READ, Permission.AGENT_INVOKE,
    ],
    "executive": [
        Permission.EXECUTIVE_READ, Permission.VESSEL_READ,
        Permission.BILLING_READ, Permission.AGENT_INVOKE,
    ],
    "maintenance": [
        Permission.MAINTENANCE_READ, Permission.MAINTENANCE_WRITE,
        Permission.AGENT_INVOKE, Permission.ML_PREDICT,
    ],
}


def has_permission(roles: list[str], required: Permission) -> bool:
    for role in roles:
        permissions = ROLE_PERMISSIONS.get(role, [])
        if Permission.ADMIN_ALL in permissions or required in permissions:
            return True
    return False
