---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# REST API Reference

## Base URL

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:3000/api/v1` |
| Production | `https://api.epicura.io/api/v1` |

---

## Authentication

All endpoints except `/auth/register` and `/auth/login` require a valid JWT access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Tokens are obtained via the login flow. See [[../10-Backend/01-Backend-Architecture#JWT Authentication Flow|JWT Authentication Flow]] for details.

---

## Common Response Format

### Success

```json
{
  "success": true,
  "data": { ... }
}
```

### Paginated

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 142,
    "total_pages": 8
  }
}
```

### Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {"field": "email", "message": "Must be a valid email address"}
    ]
  }
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request body/params failed validation |
| `INVALID_CREDENTIALS` | 401 | Wrong email or password |
| `TOKEN_EXPIRED` | 401 | Access token has expired |
| `TOKEN_INVALID` | 401 | Malformed or revoked token |
| `FORBIDDEN` | 403 | Insufficient permissions (e.g., non-admin) |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Duplicate resource (e.g., email already registered) |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Rate Limits

| Scope | Limit | Window |
|-------|-------|--------|
| Authentication endpoints | 10 requests | 1 minute |
| General API | 100 requests | 1 minute |
| Recipe sync (CM5) | 30 requests | 1 minute |
| Telemetry ingestion | 600 requests | 1 minute |

---

## Endpoints

### Auth

#### `POST /auth/register`

Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "Manas Pradhan"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "Manas Pradhan",
      "role": "user"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

```bash
curl -X POST https://api.epicura.io/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securePassword123","name":"Manas Pradhan"}'
```

#### `POST /auth/login`

Authenticate and receive tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "Manas Pradhan",
      "role": "user"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

```bash
curl -X POST https://api.epicura.io/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securePassword123"}'
```

#### `POST /auth/refresh`

Refresh an expired access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

#### `POST /auth/logout`

Revoke the current refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "success": true,
  "data": { "message": "Logged out successfully" }
}
```

---

### Recipes

#### `GET /recipes`

List published recipes with optional filtering.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `limit` | integer | 20 | Items per page (max 50) |
| `category` | string | — | Filter by category (`dal`, `curry`, `rice`, etc.) |
| `cuisine` | string | — | Filter by cuisine |
| `difficulty` | string | — | Filter by difficulty (`easy`, `medium`, `hard`) |
| `tags` | string | — | Comma-separated tag filter (`vegetarian,quick`) |
| `search` | string | — | Full-text search query |
| `sort` | string | `name` | Sort field (`name`, `time_minutes`, `created_at`) |
| `order` | string | `asc` | Sort order (`asc`, `desc`) |

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "recipe-uuid-001",
      "name": "Dal Tadka",
      "category": "dal",
      "cuisine": "indian",
      "difficulty": "easy",
      "time_minutes": 35,
      "servings": 4,
      "tags": ["vegetarian", "protein-rich"],
      "image_url": "https://cdn.epicura.io/recipes/dal-tadka.jpg",
      "version": 2
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 142,
    "total_pages": 8
  }
}
```

```bash
curl https://api.epicura.io/api/v1/recipes?category=dal&difficulty=easy \
  -H "Authorization: Bearer <token>"
```

#### `GET /recipes/:id`

Get full recipe details including `recipe_data` (stages, ingredients).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "recipe-uuid-001",
    "name": "Dal Tadka",
    "category": "dal",
    "cuisine": "indian",
    "difficulty": "easy",
    "time_minutes": 35,
    "servings": 4,
    "tags": ["vegetarian", "protein-rich"],
    "image_url": "https://cdn.epicura.io/recipes/dal-tadka.jpg",
    "version": 2,
    "recipe_data": {
      "name": "Dal Tadka",
      "servings": 4,
      "total_time_minutes": 35,
      "stages": [
        {
          "name": "Heat Oil",
          "temp_target": 180,
          "duration_seconds": 120,
          "stir": false,
          "ingredients": [{"subsystem": "SLD", "channel": "OIL", "name": "oil", "amount_g": 30}],
          "cv_check": "oil_shimmer"
        }
      ]
    },
    "created_at": "2026-01-15T10:30:00Z",
    "updated_at": "2026-02-10T14:22:00Z"
  }
}
```

#### `POST /recipes` (Admin only)

Create a new recipe.

**Request:**
```json
{
  "name": "Paneer Butter Masala",
  "category": "curry",
  "cuisine": "indian",
  "difficulty": "medium",
  "time_minutes": 45,
  "servings": 4,
  "tags": ["vegetarian", "rich"],
  "recipe_data": {
    "stages": [ ... ]
  }
}
```

**Response (201):** Returns created recipe.

#### `PUT /recipes/:id` (Admin only)

Update an existing recipe. Increments `version` automatically.

#### `DELETE /recipes/:id` (Admin only)

Soft-delete a recipe (sets `is_published = false`).

#### `GET /recipes/sync`

CM5 recipe sync endpoint. Returns recipes updated since a given timestamp.

**Query Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `since` | ISO 8601 | Yes | Return recipes updated after this timestamp |

**Response (200):**
```json
{
  "success": true,
  "data": {
    "recipes": [
      {
        "id": "recipe-uuid-003",
        "name": "Jeera Rice",
        "recipe_data": { ... },
        "version": 3,
        "updated_at": "2026-02-14T08:00:00Z"
      }
    ],
    "deleted_ids": ["recipe-uuid-old-1"],
    "server_timestamp": "2026-02-14T12:00:00Z"
  }
}
```

```bash
curl "https://api.epicura.io/api/v1/recipes/sync?since=2026-02-01T00:00:00Z" \
  -H "Authorization: Bearer <token>"
```

---

### Appliances

#### `POST /appliances/register`

Register a new appliance (called by CM5 on first boot).

**Request:**
```json
{
  "device_id": "EPIC-001",
  "serial_number": "SN2026020001",
  "firmware_version_cm5": "1.0.0",
  "firmware_version_stm32": "1.0.0",
  "wifi_mac": "AA:BB:CC:DD:EE:FF"
}
```

**Response (201):** Returns appliance record.

#### `POST /appliances/pair`

Pair an appliance with a user account using a pairing code obtained via BLE (see [[04-BLE-Services|BLE Services]]).

**Request:**
```json
{
  "pairing_code": "482917"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "appliance": {
      "id": "appliance-uuid-001",
      "device_id": "EPIC-001",
      "name": "My Epicura",
      "status": "online"
    }
  }
}
```

#### `GET /appliances`

List user's paired appliances.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "appliance-uuid-001",
      "device_id": "EPIC-001",
      "name": "Kitchen Epicura",
      "status": "online",
      "firmware_version_cm5": "1.2.0",
      "firmware_version_stm32": "1.1.0",
      "last_seen_at": "2026-02-14T12:28:00Z"
    }
  ]
}
```

#### `GET /appliances/:id`

Get appliance details.

#### `PUT /appliances/:id`

Update appliance (e.g., rename).

**Request:**
```json
{
  "name": "Kitchen Epicura"
}
```

---

### Cooking Sessions

#### `POST /sessions`

Create a new cooking session (called by CM5 when cooking starts or by mobile app to upload synced logs).

**Request:**
```json
{
  "appliance_id": "appliance-uuid-001",
  "recipe_id": "recipe-uuid-001",
  "customizations": {
    "spice_level": 4,
    "servings": 2
  }
}
```

**Response (201):** Returns session record with `status: "started"`.

#### `PUT /sessions/:id`

Update session status and data (called by CM5 during/after cooking).

**Request (during cooking):**
```json
{
  "status": "cooking",
  "stages_log": [
    {"stage": "Heat Oil", "duration_s": 118, "result": "success", "cv_confidence": 0.87}
  ]
}
```

**Request (on completion):**
```json
{
  "status": "completed",
  "completed_at": "2026-02-14T13:05:22Z",
  "peak_temperature": 182.5,
  "total_duration_s": 2122,
  "stages_log": [ ... ]
}
```

#### `GET /sessions`

List user's cooking sessions (history).

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `limit` | integer | 20 | Items per page |
| `appliance_id` | uuid | — | Filter by appliance |
| `recipe_id` | uuid | — | Filter by recipe |
| `status` | string | — | Filter by status |

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "session-uuid-001",
      "recipe": {"id": "recipe-uuid-001", "name": "Dal Tadka"},
      "appliance": {"id": "appliance-uuid-001", "device_id": "EPIC-001"},
      "status": "completed",
      "started_at": "2026-02-14T12:30:00Z",
      "completed_at": "2026-02-14T13:05:22Z",
      "total_duration_s": 2122,
      "user_rating": 5,
      "notes": "Perfect consistency"
    }
  ],
  "pagination": { ... }
}
```

#### `GET /sessions/:id`

Get full session details including stage log.

#### `PUT /sessions/:id/rate`

Rate a completed cooking session.

**Request:**
```json
{
  "rating": 5,
  "notes": "Perfect consistency, great taste"
}
```

---

### User Preferences

#### `GET /users/me`

Get current user profile and preferences.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user-uuid-001",
      "email": "user@example.com",
      "name": "Manas Pradhan",
      "role": "user",
      "created_at": "2026-01-10T08:00:00Z"
    },
    "preferences": {
      "language": "en_IN",
      "spice_level": 3,
      "default_servings": 4,
      "allergens": ["mustard"],
      "theme": "light",
      "notifications_enabled": true
    }
  }
}
```

#### `PUT /users/me`

Update profile and preferences.

**Request:**
```json
{
  "name": "Manas P.",
  "preferences": {
    "spice_level": 4,
    "allergens": ["mustard", "nuts"],
    "language": "hi_IN"
  }
}
```

---

### Push Notifications

#### `POST /push/register`

Register a device push token.

**Request:**
```json
{
  "platform": "ios",
  "token": "fcm-or-apns-device-token-string"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": { "message": "Push token registered" }
}
```

---

### Firmware

#### `GET /firmware/latest`

Check for firmware updates (called by CM5).

**Query Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `target` | string | Yes | `cm5` or `stm32` |
| `current_version` | string | Yes | Currently installed version |
| `channel` | string | No | `stable` (default), `beta`, `alpha` |

**Response (200) — Update available:**
```json
{
  "success": true,
  "data": {
    "update_available": true,
    "version": "1.2.1",
    "binary_url": "https://cdn.epicura.io/firmware/cm5/1.2.1.img",
    "checksum_sha256": "a1b2c3d4...",
    "file_size_bytes": 209715200,
    "is_mandatory": false,
    "release_notes": "Bug fixes and improved PID tuning"
  }
}
```

**Response (200) — No update:**
```json
{
  "success": true,
  "data": {
    "update_available": false
  }
}
```

```bash
curl "https://api.epicura.io/api/v1/firmware/latest?target=cm5&current_version=1.2.0" \
  -H "Authorization: Bearer <token>"
```

---

## CM5 Local API Cross-Reference

The CM5 also runs a local REST API (Flask/FastAPI) for direct WiFi communication with mobile apps on the same network. See [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]] and [[../07-Development/Prototype-Development-Plan#Phase 6|Prototype Dev Plan - Phase 6]] for local endpoints:

| Local Endpoint | Cloud Equivalent | Notes |
|----------------|------------------|-------|
| `GET /recipes` | `GET /recipes` | Local serves from SQLite; cloud from Postgres |
| `GET /status` | WebSocket events | Local is REST polling; cloud uses WebSocket |
| `POST /cook/start` | `POST /sessions` | Local directly starts; cloud creates session record |
| `POST /cook/stop` | WebSocket `cooking:stop` | Local sends UART E_STOP; cloud relays via MQTT |
| `GET /camera/stream` | MJPEG via WebSocket | Local MJPEG direct; cloud relay not supported |

---

## Pagination

All list endpoints support cursor or offset pagination:

| Param | Type | Default | Max | Description |
|-------|------|---------|-----|-------------|
| `page` | integer | 1 | — | Page number (1-indexed) |
| `limit` | integer | 20 | 50 | Items per page |

---

## Related Documentation

- [[../10-Backend/01-Backend-Architecture|Backend Architecture]] - Server setup and deployment
- [[../10-Backend/02-Database-Schema|Database Schema]] - Tables queried by these endpoints
- [[02-WebSocket-Events|WebSocket Events]] - Real-time cooking events
- [[03-MQTT-Topics|MQTT Topics]] - Device telemetry protocol
- [[04-BLE-Services|BLE Services]] - BLE pairing flow
- [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] - Mobile app networking layer

#epicura #api #rest #endpoints #backend

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
