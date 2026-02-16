---
tags: [epicura, testing, api, backend, admin, typescript]
created: 2026-02-16
aliases: [API Test Strategy, Backend Test Strategy]
---

# API & Admin Test Strategy — epicura-api

## Scope

Testing strategy for the TypeScript monorepo: Fastify API server (`apps/api`), Next.js admin portal (`apps/admin`), and shared packages (`@epicura/types`, `@epicura/validators`).

---

## Test Levels

### 1. Unit Tests

**Framework:** Vitest
**Runs on:** Host (CI-compatible)

#### Shared Packages

| Package | Key Test Cases |
|---------|---------------|
| `@epicura/types` | Type exports compile correctly (type-check only, no runtime tests) |
| `@epicura/validators` | Zod schemas: valid input passes, invalid input rejects with correct error path, edge cases (empty strings, null, boundary values) for recipe, device, user, and auth schemas |

#### API Server (`apps/api`)

| Module | Key Test Cases |
|--------|---------------|
| `routes/auth` | Register (valid/duplicate email/weak password), login (correct/wrong credentials), JWT refresh (valid/expired token), logout (token invalidation) |
| `routes/recipes` | CRUD operations, search with filters, versioning (create new version, list versions), authorization (owner vs. other user) |
| `routes/devices` | Register device, claim by user, telemetry ingestion, command dispatch, duplicate claim rejection |
| `routes/users` | Profile read/update, cooking history pagination, preference save/load |
| `services/mqtt-bridge` | Telemetry message parsing, command serialization, disconnect/reconnect handling |
| `services/upload` | Presigned URL generation, file type validation, size limit enforcement |
| `middleware/auth` | Valid JWT passes, expired JWT rejects (401), malformed token rejects, admin guard blocks non-admin |

**Approach:**
- Use Fastify's `inject()` for route testing (no HTTP server needed)
- Mock database with in-memory Drizzle adapter or test PostgreSQL container
- Mock MQTT client for mqtt-bridge tests
- Mock S3/R2 for upload tests

#### Admin Portal (`apps/admin`)

| Module | Key Test Cases |
|--------|---------------|
| `components/recipe-editor` | Monaco editor renders, YAML validation feedback, save triggers API call |
| `components/telemetry-chart` | Chart renders with sample data, handles empty dataset, time range filter works |
| `lib/api` | Fetch wrapper attaches JWT, handles 401 with redirect to login, retries on network error |
| `lib/auth` | Session persistence, logout clears session, expired session redirects |
| Page routes | Dashboard loads, recipe list renders, device detail shows correct data |

**Approach:**
- Use React Testing Library + Vitest for component tests
- Mock API responses with MSW (Mock Service Worker)
- Test page rendering with Next.js test utilities

### 2. Integration Tests

**Framework:** Vitest + Testcontainers (PostgreSQL, Mosquitto, Redis)
**Runs on:** Host with Docker

| Test Area | Setup | Verification |
|-----------|-------|-------------|
| API ↔ PostgreSQL | Testcontainers PostgreSQL, run migrations | Full CRUD lifecycle for all entities |
| API ↔ MQTT | Testcontainers Mosquitto | Telemetry ingestion stores in DB; command publish reaches subscriber |
| Auth flow | Full API server | Register → login → access protected route → refresh token → logout |
| Recipe lifecycle | Full API server + DB | Create recipe → update → publish → search → version → delete |
| Device lifecycle | Full API server + DB + MQTT | Register device → claim → receive telemetry → send command |
| Admin ↔ API | Next.js dev server + API server | Login to admin, CRUD recipe, view device telemetry |

### 3. API Contract Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| OpenAPI spec validation | Generate OpenAPI from routes, compare against `docs/11-API/01-REST-API-Reference` | No unintended breaking changes |
| Request/response schemas | Validate all endpoints against Zod schemas | 100% endpoints covered |
| MQTT topic validation | Verify published topics match `docs/11-API/03-MQTT-Topics` | All topics match spec |
| WebSocket event validation | Verify event shapes match `docs/11-API/02-WebSocket-Events` | All events match spec |

### 4. Performance Tests

| Test | Tool | Pass Criteria |
|------|------|--------------|
| API throughput | k6 or autocannon | ≥ 500 req/s for recipe list endpoint |
| Database query latency | pg_stat_statements | p95 < 100ms for all common queries |
| Auth middleware overhead | Benchmark with/without JWT | < 5ms added latency |
| Admin page load | Lighthouse CI | Performance score ≥ 80 |
| Admin bundle size | `next build` output | Total JS < 500 KB gzipped |

### 5. Security Tests

| Test | Tool | Pass Criteria |
|------|------|--------------|
| SQL injection | sqlmap against test instance | Zero vulnerabilities |
| JWT manipulation | Manual: expired, tampered, missing claims | All rejected with 401 |
| CORS | curl with wrong origin | Rejected per CORS policy |
| Rate limiting | k6 burst test | 429 returned after limit exceeded |
| Input validation | Fuzz recipe/user inputs | All invalid inputs rejected, no crashes |
| Dependency audit | `pnpm audit` | Zero critical/high vulnerabilities |

---

## CI Pipeline

```yaml
# .github/workflows/ci.yml
trigger: PR to main or staging

steps:
  1. Checkout
  2. pnpm install
  3. turbo run lint (ESLint across all packages)
  4. turbo run typecheck (tsc --noEmit)
  5. turbo run test (Vitest unit tests, parallel per package)
  6. turbo run test:integration (Testcontainers-based)
  7. turbo run build (compile all packages)
  8. Report coverage
```

**Gate criteria:** Lint clean, type-check clean, all tests pass, coverage ≥ 80% (API), ≥ 70% (admin), build succeeds.

---

## Test Data

- **Seed database:** 50 recipes, 10 users (various roles), 5 devices, 1000 telemetry records
- **MQTT test messages:** JSON payloads for all telemetry and command topic types
- **Admin test fixtures:** MSW handlers for all API endpoints with realistic response data

---

## References

- [[__Workspaces/Epicura/docs/07-Development/02-Repository-Plan|Repository Plan]]
- [[__Workspaces/Epicura/docs/10-Backend/01-Backend-Architecture|Backend Architecture]]
- [[__Workspaces/Epicura/docs/10-Backend/02-Database-Schema|Database Schema]]
- [[__Workspaces/Epicura/docs/11-API/01-REST-API-Reference|REST API Reference]]
- [[__Workspaces/Epicura/docs/10-Backend/03-Admin-Portal|Admin Portal]]
