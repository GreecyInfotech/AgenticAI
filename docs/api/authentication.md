# Authentication & Authorization

## Overview

The platform uses **JWT (JSON Web Token)** authentication with **role-based access control (RBAC)**.

- Algorithm: `HS256`
- Token lifetime: configurable via `JWT_EXPIRE_MINUTES` (default 60)
- Secret: `JWT_SECRET` environment variable

## Obtaining a Token

```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "subject": "CUST-001",
  "role": "distributor"
}
```

### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in_minutes": 60
}
```

> **Production note:** Replace `/auth/token` with OAuth 2.0 / Okta integration. The current endpoint is for development only.

## Using the Token

Include in all protected requests:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Verify Current User

```http
GET /api/v1/auth/me
Authorization: Bearer {token}
```

```json
{"subject": "CUST-001", "role": "distributor"}
```

## Roles

| Role | Description |
|------|-------------|
| `admin` | Full access to all resources |
| `sales_rep` | Orders, inventory, customers, conversation |
| `distributor` | Own orders, inventory read, conversation |
| `viewer` | Read-only access to orders, inventory, customers |

## Permissions

| Permission | admin | sales_rep | distributor | viewer |
|------------|-------|-----------|-------------|--------|
| `orders:read` | ✓ | ✓ | ✓ | ✓ |
| `orders:write` | ✓ | ✓ | ✓ | |
| `inventory:read` | ✓ | ✓ | ✓ | ✓ |
| `customers:read` | ✓ | ✓ | ✓ | ✓ |
| `customers:write` | ✓ | | | |
| `conversation:write` | ✓ | ✓ | ✓ | |
| `analytics:read` | ✓ | | | |

Defined in `shared/security/jwt.py` → `ROLE_PERMISSIONS`.

## Gateway Authentication

The API Gateway validates JWT on all requests except:

- `/health`, `/ready`, `/metrics`
- `/api/v1/health`
- `/api/v1/auth/token`

Invalid tokens return `401 Unauthorized` with RFC 7807 Problem Details.

## Frontend Integration

The React frontend stores the token in `localStorage`:

```typescript
// Login
const res = await api.login("CUST-001", "distributor");
localStorage.setItem("access_token", res.access_token);

// All subsequent requests include:
headers: { Authorization: `Bearer ${token}` }
```

## Security Configuration

```env
JWT_SECRET=change-me-in-production-use-64-char-random-string
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

**Production requirements:**
- Use a cryptographically random secret (64+ characters)
- Rotate secrets periodically
- Consider RS256 with public/private key pair for multi-service validation
- Enable OAuth 2.0 / Okta (`security/oauth.py`, `security/okta.py`)

## Prompt Injection Protection

The `/conversation` endpoint checks for prompt injection patterns before processing:

```
ignore previous, system prompt, you are now, disregard, jailbreak, override instructions
```

Detected injections return `422 Validation Error`.

## PII Masking

Logs automatically mask:
- Email addresses → `[EMAIL]`
- Phone numbers → `[PHONE]`
- SSN patterns → `[SSN]`
- Credit card numbers → `[CARD]`

Implemented in `shared/security/pii.py`.
