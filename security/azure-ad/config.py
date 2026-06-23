"""Azure Active Directory / Entra ID integration."""

AZURE_AD_CONFIG = {
    "tenant_id_env": "AZURE_AD_TENANT_ID",
    "client_id_env": "AZURE_AD_CLIENT_ID",
    "client_secret_env": "AZURE_AD_CLIENT_SECRET",
    "app_role_mapping": {
        "SmartPort.Admin": ["admin", "operator"],
        "SmartPort.Operator": ["operator"],
        "SmartPort.CustomsOfficer": ["customs_officer"],
        "SmartPort.Executive": ["executive"],
        "SmartPort.Maintenance": ["maintenance"],
    },
    "managed_identity_enabled": True,
}
