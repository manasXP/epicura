---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Backend Architecture

## 1. System Overview

Epicura's cloud backend provides centralized services for recipe management, appliance registration, user accounts, cooking telemetry, OTA firmware updates, and push notifications. The backend serves both the native mobile apps (iOS/Android) and the admin portal, while also receiving telemetry from Epicura devices via MQTT.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         Epicura Cloud Architecture                         │
│                                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  iOS App     │  │ Android App  │  │ Admin Portal │  │ Epicura CM5  │    │
│  │  (SwiftUI)   │  │ (Compose)    │  │ (Next.js)    │  │ (Yocto)      │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │ HTTPS           │ HTTPS           │ HTTPS           │ MQTT/HTTPS │
│         └────────┬────────┘                 │                 │            │
│                  │                          │                 │            │
│         ┌────────▼──────────────────────────▼──────┐   ┌──────▼───────┐    │
│         │              Fastify API Server          │   │ MQTT Broker  │    │
│         │              (Node.js / TypeScript)      │◄──┤ (Mosquitto / │    │ 
│         │                                          │   │  AWS IoT)    │    │
│         │  ┌──────────────────────────────────┐    │   └──────────────┘    │
│         │  │ Service Modules:                 │    │                       │
│         │  │  Auth  │ Recipes  │ Appliances   │    │                       │
│         │  │  Sessions │ Telemetry │ Notifications │                       │
│         │  │  OTA   │ Admin                   │    │                       │
│         │  └──────────────────────────────────┘    │                       │
│         └──────────┬──────────────┬────────────────┘                       │
│                    │              │                                        │
│           ┌────────▼───┐  ┌───────▼─────┐                                  │
│           │ PostgreSQL │  │    Redis    │                                  │
│           │ (Primary)  │  │  (Cache +   │                                  │
│           │            │  │   Sessions) │                                  │
│           └────────────┘  └─────────────┘                                  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Runtime** | Node.js 20 LTS | Server runtime |
| **Framework** | Fastify 5.x | HTTP framework (high performance, schema validation) |
| **Language** | TypeScript 5.x | Type safety across the entire backend |
| **Database** | PostgreSQL 16 | Primary data store (JSONB, full-text search, partitioning) |
| **ORM** | Drizzle ORM | Type-safe schema, migrations, query builder |
| **Cache** | Redis 7.x | Session store, rate limiting, pub/sub for WebSocket |
| **MQTT Broker** | Mosquitto (dev) / AWS IoT Core (prod) | Device telemetry ingestion |
| **Auth** | JWT (access + refresh tokens) | Stateless authentication |
| **Validation** | Zod | Runtime request/response validation |
| **API Docs** | Swagger / OpenAPI 3.1 | Auto-generated from Fastify schemas |
| **Task Queue** | BullMQ (Redis-backed) | Background jobs (push notifications, telemetry aggregation) |
| **File Storage** | S3 / Cloudflare R2 | Recipe images, firmware binaries |
| **Logging** | Pino (Fastify default) | Structured JSON logging |
| **Testing** | Vitest + Supertest | Unit and integration tests |

---

## 3. Service Modules

### 3.1 Module Overview

| Module | Responsibility | Key Endpoints |
|--------|---------------|---------------|
| **Auth** | Registration, login, JWT lifecycle, password reset | `/auth/*` |
| **Recipes** | CRUD, versioning, search, CM5 sync | `/recipes/*` |
| **Appliances** | Registration, pairing, status tracking | `/appliances/*` |
| **Sessions** | Cooking session lifecycle, history | `/sessions/*` |
| **Telemetry** | Ingest MQTT data, store time-series, analytics | `/telemetry/*` |
| **Notifications** | Push notifications via FCM/APNs | `/push/*` |
| **OTA** | Firmware release management, update checks | `/firmware/*` |
| **Admin** | Admin-only endpoints for portal | `/admin/*` |

### 3.2 Module Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Fastify Server                        │
│                                                              │
│  ┌─────────────┐  ┌──────────────────────────────────────┐   │
│  │   Plugins   │  │            Route Modules             │   │
│  │  ┌────────┐ │  │  ┌──────┐ ┌────────┐ ┌───────────┐   │   │
│  │  │  Auth  │ │  │  │ Auth │ │Recipes │ │Appliances │   │   │
│  │  │ (JWT)  │ │  │  └──┬───┘ └───┬────┘ └──────┬────┘   │   │
│  │  ├────────┤ │  │     │         │             │        │   │
│  │  │  CORS  │ │  │  ┌──▼─────────▼─────────────▼──────┐ │   │
│  │  ├────────┤ │  │  │         Service Layer           │ │   │
│  │  │  Rate  │ │  │  │  (Business logic, validation)   │ │   │
│  │  │ Limit  │ │  │  └──┬─────────┬─────────────┬──────┘ │   │
│  │  └────────┘ │  │     │         │             │        │   │
│  └─────────────┘  │  ┌──▼─────────▼─────────────▼──────┐ │   │
│                   │  │       Repository Layer          │ │   │
│                   │  │  (Drizzle ORM queries)          │ │   │
│                   │  └──┬─────────┬─────────────┬──────┘ │   │
│                   │     │         │             │        │   │
│                   └─────┼─────────┼─────────────┼────────┘   │
│                         │         │             │            │
│                  ┌──────▼──┐  ┌───▼────┐  ┌─────▼───┐        │
│                  │PostgreSQL  │ Redis  │  │   S3    │        │
│                  └─────────┘  └────────┘  └─────────┘        │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. JWT Authentication Flow

```
┌──────────┐                          ┌──────────┐                ┌──────────┐
│  Client  │                          │   API    │                │   DB     │
└────┬─────┘                          └────┬─────┘                └────┬─────┘
     │  POST /auth/login                   │                           │
     │  {email, password}                  │                           │
     │────────────────────────────────────►│                           │
     │                                     │  Verify credentials       │
     │                                     │──────────────────────────►│
     │                                     │◄──────────────────────────│
     │                                     │                           │
     │  {access_token (15m),               │                           │
     │   refresh_token (30d)}              │                           │
     │◄────────────────────────────────────│                           │
     │                                     │                           │
     │  GET /recipes                       │                           │
     │  Authorization: Bearer <access>     │                           │
     │────────────────────────────────────►│                           │
     │                                     │  Verify JWT, extract user │
     │  {recipes: [...]}                   │                           │
     │◄────────────────────────────────────│                           │
     │                                     │                           │
     │  POST /auth/refresh                 │                           │
     │  {refresh_token}                    │                           │
     │────────────────────────────────────►│                           │
     │                                     │  Verify + rotate          │
     │  {new access_token,                 │                           │
     │   new refresh_token}                │                           │
     │◄────────────────────────────────────│                           │
```

**Token Details:**

| Token | Lifetime | Storage (Mobile) | Contains |
|-------|----------|------------------|----------|
| Access Token | 15 minutes | Memory | `user_id`, `email`, `role` |
| Refresh Token | 30 days | Secure Keychain / EncryptedSharedPreferences | `user_id`, `token_family` |

**Roles:**

| Role | Access |
|------|--------|
| `user` | Own data, recipes, sessions, appliances |
| `admin` | All data, recipe CRUD, appliance management, analytics |

---

## 5. Monorepo Structure

```
epicura-cloud/
├── apps/
│   ├── api/                          Fastify API server
│   │   ├── src/
│   │   │   ├── plugins/              Fastify plugins (auth, cors, rate-limit)
│   │   │   ├── modules/
│   │   │   │   ├── auth/             Routes, service, schemas
│   │   │   │   ├── recipes/
│   │   │   │   ├── appliances/
│   │   │   │   ├── sessions/
│   │   │   │   ├── telemetry/
│   │   │   │   ├── notifications/
│   │   │   │   ├── ota/
│   │   │   │   └── admin/
│   │   │   ├── mqtt/                 MQTT subscriber and handlers
│   │   │   ├── ws/                   WebSocket event handlers
│   │   │   └── server.ts             Fastify app bootstrap
│   │   ├── test/
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   └── admin/                        Next.js admin portal
│       ├── src/
│       │   ├── app/                  App Router pages
│       │   ├── components/
│       │   ├── hooks/
│       │   └── lib/
│       ├── Dockerfile
│       └── package.json
│
├── packages/
│   ├── db/                           Drizzle schema + migrations
│   │   ├── schema/
│   │   ├── migrations/
│   │   └── drizzle.config.ts
│   │
│   └── shared/                       Shared types, constants, utils
│       ├── types/
│       ├── constants/
│       └── validators/
│
├── docker-compose.yml                Dev environment (Postgres, Redis, Mosquitto)
├── turbo.json                        Turborepo config
├── package.json                      Root workspace
└── tsconfig.base.json                Shared TypeScript config
```

---

## 6. Environment Configuration

| Variable | Dev Default | Description |
|----------|-------------|-------------|
| `DATABASE_URL` | `postgres://epicura:epicura@localhost:5432/epicura` | PostgreSQL connection |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection |
| `MQTT_BROKER_URL` | `mqtt://localhost:1883` | MQTT broker |
| `JWT_SECRET` | (generated) | JWT signing secret |
| `JWT_REFRESH_SECRET` | (generated) | Refresh token signing secret |
| `S3_BUCKET` | `epicura-dev` | Object storage bucket |
| `S3_ENDPOINT` | (local MinIO URL) | S3-compatible endpoint |
| `FCM_SERVICE_ACCOUNT` | (path to JSON) | Firebase Cloud Messaging credentials |
| `APNS_KEY_ID` | (Apple key ID) | APNs authentication key |
| `PORT` | `3000` | API server port |
| `NODE_ENV` | `development` | Environment flag |

---

## 7. Deployment

### 7.1 Development (Docker Compose)

```yaml
# docker-compose.yml (simplified)
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: epicura
      POSTGRES_USER: epicura
      POSTGRES_PASSWORD: epicura
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  mosquitto:
    image: eclipse-mosquitto:2
    ports: ["1883:1883", "9001:9001"]
    volumes: [./mosquitto.conf:/mosquitto/config/mosquitto.conf]

  api:
    build: ./apps/api
    ports: ["3000:3000"]
    depends_on: [postgres, redis, mosquitto]
    env_file: .env

  admin:
    build: ./apps/admin
    ports: ["3001:3001"]
    depends_on: [api]
```

### 7.2 Production

| Service | Platform | Notes |
|---------|----------|-------|
| API Server | Fly.io / AWS ECS | Auto-scaling, health checks |
| Admin Portal | Vercel | Static + SSR, edge functions |
| PostgreSQL | AWS RDS / Neon | Managed, automated backups |
| Redis | Upstash / ElastiCache | Serverless or managed |
| MQTT | AWS IoT Core | Managed, device certificates, rules engine |
| Object Storage | Cloudflare R2 / S3 | Recipe images, firmware binaries |
| CDN | Cloudflare | Recipe image delivery |

---

## 8. MQTT Bridge (Device to Backend)

The backend subscribes to device MQTT topics and bridges telemetry data to WebSocket clients (mobile apps) and to PostgreSQL for persistence.

```
┌──────────┐     MQTT      ┌──────────────┐     Internal    ┌───────────┐
│ Epicura  │──────────────►│  MQTT Broker │────────────────►│ API Server│
│ CM5      │               │  (Mosquitto /│                 │ (Fastify) │
│          │               │   AWS IoT)   │                 │           │
└──────────┘               └──────────────┘                 └─────┬─────┘
                                                                   │
                                                          ┌────────┼────────┐
                                                          │        │        │
                                                    ┌─────▼──┐ ┌──▼────┐ ┌▼────────┐
                                                    │WebSocket│ │Postgres│ │BullMQ   │
                                                    │→ Mobile │ │(store) │ │(push    │
                                                    │  Apps   │ │        │ │ notify) │
                                                    └────────┘ └────────┘ └─────────┘
```

---

## 9. Design Decisions

| Decision | Chosen | Alternative | Rationale |
|----------|--------|-------------|-----------|
| API Framework | Fastify | Express, NestJS | Fastest Node.js framework, built-in schema validation, plugin system, TypeScript-first |
| Language | TypeScript | JavaScript, Go | Type safety, shared types between API and admin portal, large ecosystem |
| Database | PostgreSQL | MongoDB, MySQL | JSONB for flexible recipe data, full-text search, table partitioning for telemetry, mature ecosystem |
| ORM | Drizzle | Prisma, TypeORM | Lightweight, type-safe, SQL-like API, better performance than Prisma for complex queries |
| Cache | Redis | Memcached | Pub/sub for WebSocket fan-out, BullMQ job queues, session store, sorted sets for rate limiting |
| Auth | JWT | Session cookies | Stateless, works across mobile apps and web, refresh token rotation for security |
| Monorepo | Turborepo | Nx, Lerna | Simple config, fast builds, good Vercel integration for admin portal |
| Admin Portal | Next.js | Remix, Vite SPA | SSR for SEO-less admin is fine, but App Router + Server Actions simplify data fetching; shared Turborepo |
| Task Queue | BullMQ | Agenda, custom | Redis-backed, reliable, retries, dashboard (Bull Board), TypeScript types |

---

## 10. Unified Deployment Model (Cloud + CM5)

The same Fastify codebase deploys to both the cloud and each CM5 device. This eliminates API drift and reduces maintenance to a single implementation.

| Aspect | Cloud | CM5 (On-Device) |
|--------|-------|-----------------|
| **Runtime** | Node.js 20 LTS (cloud VM / container) | Node.js 20 LTS (Docker on Yocto) |
| **Database** | PostgreSQL 16 (RDS/Neon) | PostgreSQL 16 (Docker container) |
| **Schema** | Identical | Identical |
| **Modules Enabled** | All (Auth, Recipes, Appliances, Sessions, Telemetry, Notifications, OTA, **Admin**) | All except **Admin** (`DISABLE_ADMIN=true`) |
| **Port** | 3000 | 3000 |
| **Access** | Public internet (HTTPS) | Local network only (HTTP via mDNS) |

**How it works:**
- The `epicura-api` monorepo builds a single Docker image
- An environment variable (`DISABLE_ADMIN=true`) excludes the admin module on CM5
- Kivy UI calls `http://api:3000/api/v1/...` endpoints via Python `requests` — the interface is identical regardless of whether Fastify or any other framework serves it
- Recipe engine, CV pipeline, and bridge services also call Fastify endpoints over HTTP rather than touching PostgreSQL directly
- Camera MJPEG streaming (port 8080) is bundled inside the cv-pipeline container

---

## 11. Related Documentation

- [[02-Database-Schema|Database Schema]] - Full table definitions and ER diagram
- [[03-Admin-Portal|Admin Portal]] - Next.js admin interface
- [[01-REST-API-Reference|REST API Reference]] - Complete endpoint documentation
- [[02-WebSocket-Events|WebSocket Events]] - Real-time event protocol
- [[03-MQTT-Topics|MQTT Topics]] - Device telemetry topic hierarchy
- [[../03-Software/02-Controller-Software-Architecture|Controller & Software Architecture]] - CM5 PostgreSQL schema and cloud sync
- [[../03-Software/01-Tech-Stack|Tech Stack]] - Overall technology choices

#epicura #backend #fastify #typescript #postgresql #redis #mqtt #architecture

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
