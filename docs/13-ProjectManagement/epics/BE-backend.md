---
tags: [epicura, project-management, epic, backend, fastify]
created: 2026-02-16
aliases: [BE Epic, Backend Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 6 stories across Sprints 5–10 |
> | 2026-02-17 | Manas Pradhan | Split BE-SET.01, BE-RCP.01, BE-DEV.01 (8pts each) into pairs of 5+3pts |

# Epic: BE — Cloud Backend (Fastify)

Fastify API server with PostgreSQL, MQTT cloud bridge, recipe management, device management, user accounts, and telemetry. TypeScript throughout. Serves mobile apps and admin portal.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SET — Project Setup | 2 | 8 | 5 |
| RCP — Recipe API | 2 | 8 | 6 |
| DEV — Device Management | 2 | 8 | 7 |
| MQT — MQTT Cloud Bridge | 1 | 5 | 7 |
| USR — User Management | 1 | 5 | 8 |
| LCH — Launch | 1 | 5 | 10 |
| **Total** | **9** | **~38** | |

---

## Phase 2 — Backend Foundation (Sprints 5–6)

### BE-SET.01: Fastify project setup — TypeScript, Drizzle ORM, PostgreSQL schema, auth
- **Sprint:** [[sprint-05|Sprint 5]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** None
- **Blocks:** [[BE-backend#BE-SET.02|BE-SET.02]], All subsequent BE stories

**Acceptance Criteria:**
- [ ] Fastify app bootstraps with TypeScript; health-check returns 200
- [ ] PostgreSQL connection via Drizzle ORM; migrations run without errors
- [ ] Database schema: users, devices, recipes, cook_sessions, telemetry tables
- [ ] JWT authentication: register, login, refresh token endpoints

**Tasks:**
- [ ] `BE-SET.01a` — Initialize Fastify project with TypeScript, fastify-swagger, fastify-jwt
- [ ] `BE-SET.01b` — Configure Drizzle ORM with PostgreSQL; create initial migration with core tables
- [ ] `BE-SET.01c` — Implement auth module: register (email/password), login, JWT refresh, logout

---

### BE-SET.02: Backend dev environment — Docker Compose, Swagger, CI pipeline
- **Sprint:** [[sprint-05|Sprint 5]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[BE-backend#BE-SET.01|BE-SET.01]]
- **Blocks:** [[BE-backend#BE-RCP.01|BE-RCP.01]], [[BE-backend#BE-DEV.01|BE-DEV.01]]

**Acceptance Criteria:**
- [ ] Docker Compose for local development (PostgreSQL + Redis + API)
- [ ] Swagger UI accessible at `/docs` with auto-generated OpenAPI spec
- [ ] ESLint + Prettier configured; CI pipeline runs lint + type-check + test

**Tasks:**
- [ ] `BE-SET.02a` — Set up Docker Compose for local dev: PostgreSQL 16, Redis
- [ ] `BE-SET.02b` — Configure Swagger with JWT bearer auth; verify spec generation
- [ ] `BE-SET.02c` — Set up ESLint, Prettier, Vitest; create CI GitHub Actions workflow

---

### BE-RCP.01: Recipe CRUD API — endpoints, schema, versioning
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-SET.02|BE-SET.02]]
- **Blocks:** [[BE-backend#BE-RCP.02|BE-RCP.02]]

**Acceptance Criteria:**
- [ ] CRUD endpoints for recipes at `/api/recipes` with pagination and search
- [ ] Recipe schema: name, cuisine, servings, cook_time, difficulty, ingredients (JSONB), steps (JSONB), image_url, nutrition (calories, protein_g, carbs_g, fats_g)
- [ ] Recipe versioning: version number incremented on update; sync endpoint with `since_version` param
- [ ] Admin-only create/update/delete; public read access with auth

**Tasks:**
- [ ] `BE-RCP.01a` — Create recipes table migration with JSONB columns for ingredients and steps
- [ ] `BE-RCP.01b` — Implement recipe CRUD endpoints with Drizzle ORM
- [ ] `BE-RCP.01c` — Implement recipe versioning: auto-increment on update, sync endpoint with `since_version` param

---

### BE-RCP.02: Recipe API — image upload, bulk export, testing
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[BE-backend#BE-RCP.01|BE-RCP.01]]
- **Blocks:** [[RCP-recipe#RCP-SYN.01|RCP-SYN.01]], [[IOS-ios#IOS-RCP.01|IOS-RCP.01]], [[AND-android#AND-RCP.01|AND-RCP.01]], [[ADM-admin#ADM-RCP.01|ADM-RCP.01]]

**Acceptance Criteria:**
- [ ] Image upload via presigned S3/R2 URL; CDN delivery
- [ ] Pagination, search (full-text on name + cuisine), and filtering
- [ ] Bulk export endpoint: GET `/api/recipes/export` returns all recipes as JSON
- [ ] API tests for all recipe endpoints

**Tasks:**
- [ ] `BE-RCP.02a` — Implement image upload: presigned URL generation, CDN URL storage
- [ ] `BE-RCP.02b` — Implement pagination, search (full-text on name + cuisine), and filtering
- [ ] `BE-RCP.02c` — Implement bulk export endpoint; write API tests for all recipe endpoints

---

## Phase 2–3 — Device & MQTT (Sprints 7–8)

### BE-DEV.01: Device management API — registration, telemetry, status
- **Sprint:** [[sprint-07|Sprint 7]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-SET.02|BE-SET.02]]
- **Blocks:** [[BE-backend#BE-DEV.02|BE-DEV.02]]

**Acceptance Criteria:**
- [ ] Device registration: POST `/api/devices/register` with device UUID, firmware version, returns device token
- [ ] Device telemetry storage: POST `/api/devices/:id/telemetry` stores sensor readings (time-series)
- [ ] Device status: GET `/api/devices/:id` returns last seen, firmware version, cooking status

**Tasks:**
- [ ] `BE-DEV.01a` — Create devices, device_telemetry, device_commands tables
- [ ] `BE-DEV.01b` — Implement device registration with UUID validation and token generation
- [ ] `BE-DEV.01c` — Implement telemetry ingestion endpoint with time-series storage

---

### BE-DEV.02: Device API — commands, user claiming, testing
- **Sprint:** [[sprint-07|Sprint 7]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[BE-backend#BE-DEV.01|BE-DEV.01]]
- **Blocks:** [[IOS-ios#IOS-BLE.01|IOS-BLE.01]], [[AND-android#AND-BLE.01|AND-BLE.01]], [[ADM-admin#ADM-DEV.01|ADM-DEV.01]]

**Acceptance Criteria:**
- [ ] Device commands: POST `/api/devices/:id/commands` queues command (start_cook, abort, update)
- [ ] User-device linking: POST `/api/devices/:id/claim` associates device with user account; unclaim endpoint
- [ ] Device list for user: GET `/api/devices` returns all claimed devices
- [ ] Integration tests for device lifecycle

**Tasks:**
- [ ] `BE-DEV.02a` — Implement device status and command queue endpoints
- [ ] `BE-DEV.02b` — Implement user-device claim/unclaim flow
- [ ] `BE-DEV.02c` — Write integration tests for device lifecycle

---

### BE-MQT.01: MQTT cloud bridge — telemetry ingestion, command dispatch
- **Sprint:** [[sprint-07|Sprint 7]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-DEV.01|BE-DEV.01]]
- **Blocks:** [[ADM-admin#ADM-DEV.01|ADM-DEV.01]]

**Acceptance Criteria:**
- [ ] Mosquitto cloud broker deployed (Docker or managed service)
- [ ] Bridge service subscribes to device telemetry topics: `epicura/{device_id}/telemetry/#`
- [ ] Telemetry messages parsed and stored in PostgreSQL via device telemetry API
- [ ] Command dispatch: publish to `epicura/{device_id}/commands` when command queued via API
- [ ] Device online/offline detection via MQTT last-will message
- [ ] TLS encryption on all MQTT connections; device authentication via token

**Tasks:**
- [ ] `BE-MQT.01a` — Deploy Mosquitto broker with TLS; configure device auth plugin
- [ ] `BE-MQT.01b` — Implement bridge service: subscribe to telemetry, store in PostgreSQL
- [ ] `BE-MQT.01c` — Implement command dispatch: poll command queue, publish to device topic
- [ ] `BE-MQT.01d` — Implement online/offline tracking via last-will messages
- [ ] `BE-MQT.01e` — Test end-to-end: device publishes telemetry → bridge stores → API returns data

---

### BE-USR.01: User management — profiles, cooking history, preferences
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-SET.01|BE-SET.01]]
- **Blocks:** [[IOS-ios#IOS-USR.01|IOS-USR.01]], [[AND-android#AND-USR.01|AND-USR.01]], [[ADM-admin#ADM-USR.01|ADM-USR.01]]

**Acceptance Criteria:**
- [ ] User profile: GET/PATCH `/api/users/me` with name, email, avatar, dietary preferences
- [ ] Cooking history: GET `/api/users/me/cook-sessions` with pagination, recipe link, status, duration
- [ ] User preferences: spice level, serving size, favorite cuisines (JSONB)
- [ ] Account deletion: DELETE `/api/users/me` soft-deletes with 30-day grace period
- [ ] Admin user list: GET `/api/admin/users` with search and pagination

**Tasks:**
- [ ] `BE-USR.01a` — Extend users table: add profile fields, preferences JSONB, deleted_at
- [ ] `BE-USR.01b` — Implement profile GET/PATCH endpoints
- [ ] `BE-USR.01c` — Implement cooking history endpoint with recipe join and filtering
- [ ] `BE-USR.01d` — Implement soft delete with grace period and data cleanup cron
- [ ] `BE-USR.01e` — Implement admin user list with search

---

### BE-LCH.01: Production deployment — hosting, monitoring, security hardening
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-USR.01|BE-USR.01]]
- **Blocks:** [[INT-integration#INT-LCH.01|INT-LCH.01]]

**Acceptance Criteria:**
- [ ] API deployed to production (Railway/Render/VPS) with HTTPS
- [ ] PostgreSQL production database configured (Neon or managed PostgreSQL)
- [ ] Rate limiting on all endpoints; CORS configured for mobile and admin origins
- [ ] Sentry error tracking integrated; structured logging with Pino
- [ ] Health check endpoint monitored with uptime service
- [ ] Database backup schedule: daily automated backups with 30-day retention

**Tasks:**
- [ ] `BE-LCH.01a` — Deploy Fastify API to production host; configure environment variables
- [ ] `BE-LCH.01b` — Provision production PostgreSQL; run migrations; seed initial data
- [ ] `BE-LCH.01c` — Configure rate limiting (fastify-rate-limit), CORS, helmet security headers
- [ ] `BE-LCH.01d` — Integrate Sentry; configure Pino structured logging
- [ ] `BE-LCH.01e` — Set up uptime monitoring and database backup schedule

---

## Dependencies

### What BE blocks

| BE Story | Blocks | Reason |
|----------|--------|--------|
| BE-SET.01 | BE-SET.02, All subsequent BE stories | Foundation for all backend work |
| BE-SET.02 | BE-RCP.01, BE-DEV.01 | Dev environment for API development |
| BE-RCP.01 | BE-RCP.02 | Recipe CRUD needed for image upload and testing |
| BE-RCP.02 | RCP-SYN.01, IOS-RCP.01, AND-RCP.01, ADM-RCP.01 | Recipe API consumed by device sync, mobile, and admin |
| BE-DEV.01 | BE-DEV.02, BE-MQT.01 | Device registration needed for commands and MQTT |
| BE-DEV.02 | IOS-BLE.01, AND-BLE.01, ADM-DEV.01 | Device API for pairing and monitoring |
| BE-MQT.01 | ADM-DEV.01 | MQTT bridge for real-time device data |
| BE-USR.01 | IOS-USR.01, AND-USR.01, ADM-USR.01 | User API for profiles and history |
| BE-LCH.01 | INT-LCH.01 | Production backend for launch |

### What blocks BE

| BE Story | Blocked by | Reason |
|----------|------------|--------|
| BE-SET.01 | None | Independent |
| BE-SET.02 | BE-SET.01 | Needs Fastify + DB setup |
| BE-RCP.01 | BE-SET.02 | Needs dev environment |
| BE-RCP.02 | BE-RCP.01 | Needs recipe CRUD endpoints |
| BE-DEV.01 | BE-SET.02 | Needs dev environment |
| BE-DEV.02 | BE-DEV.01 | Needs device tables and registration |
| BE-MQT.01 | BE-DEV.01 | Needs device table and API |
| BE-USR.01 | BE-SET.01 | Needs auth module |
| BE-LCH.01 | BE-USR.01 | Needs all features complete |

---

## References

- [[__Workspaces/Epicura/docs/10-Backend/01-Backend-Architecture|Backend Architecture]]
- [[__Workspaces/Epicura/docs/10-Backend/02-Database-Schema|Database Schema]]
- [[__Workspaces/Epicura/docs/11-API/01-REST-API-Reference|REST API Reference]]
- [[__Workspaces/Epicura/docs/11-API/03-MQTT-Topics|MQTT Topics]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
