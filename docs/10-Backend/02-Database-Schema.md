---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Database Schema

## Overview

Epicura's cloud database uses PostgreSQL 16 with Drizzle ORM. The schema supports user management, recipe storage (with JSONB for flexible recipe data), appliance registration, cooking session tracking, time-series telemetry (partitioned by month), push notification tokens, and firmware release management.

The cloud schema is designed to complement the [[../03-Software/04-Controller-Software-Architecture#5. Data Management (CM5)|CM5 on-device SQLite schema]], with a sync strategy that keeps recipes and user preferences consistent between cloud and device.

---

## ER Diagram

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│      users       │       │  user_preferences │       │   push_tokens    │
│──────────────────│       │──────────────────│       │──────────────────│
│ id (PK)          │──┐    │ id (PK)          │       │ id (PK)          │
│ email            │  │    │ user_id (FK)     │───┐   │ user_id (FK)     │───┐
│ password_hash    │  │    │ language         │   │   │ platform         │   │
│ name             │  │    │ spice_level      │   │   │ token            │   │
│ role             │  │    │ salt_level       │   │   │ created_at       │   │
│ created_at       │  │    │ oil_level        │   │   └──────────────────┘   │
│ updated_at       │  │    │ diet             │   │                          │
└──────────────────┘  │    │ cuisines         │   │                          │
                      │    │ default_servings │   │                          │
                      │    │ allergens        │   │                          │
                      │    │ theme            │   │                          │
                      │    └──────────────────┘   │                          │
                      │                            │                          │
          ┌───────────┴──────────────┐             │                          │
          │                          │             │                          │
          ▼                          ▼             │                          │
┌──────────────────┐       ┌──────────────────┐   │                          │
│   appliances     │       │ cooking_sessions │   │                          │
│──────────────────│       │──────────────────│   │                          │
│ id (PK)          │──┐    │ id (PK)          │   │                          │
│ user_id (FK)     │  │    │ user_id (FK)     │◄──┘                          │
│ device_id        │  │    │ appliance_id (FK)│◄──┐                          │
│ serial_number    │  │    │ recipe_id (FK)   │   │                          │
│ name             │  │    │ status           │   │                          │
│ firmware_version │  │    │ started_at       │   │                          │
│ paired_at        │  │    │ completed_at     │   │                          │
│ last_seen_at     │  │    │ stages_log       │   │                          │
│ status           │  │    │ user_rating      │   │                          │
└──────────────────┘  │    │ notes            │   │                          │
                      │    └──────────────────┘   │                          │
                      │                            │                          │
                      │    ┌──────────────────┐   │                          │
                      │    │telemetry_events  │   │                          │
                      │    │──────────────────│   │                          │
                      └───►│ id (PK)          │   │                          │
                           │ appliance_id (FK)│   │                          │
                           │ session_id (FK)  │───┘                          │
                           │ event_type       │                              │
                           │ payload (JSONB)  │                              │
                           │ recorded_at      │                              │
                           └──────────────────┘                              │
                                                                             │
┌──────────────────┐       ┌──────────────────┐                              │
│     recipes      │       │firmware_releases │                              │
│──────────────────│       │──────────────────│                              │
│ id (PK)          │       │ id (PK)          │                              │
│ name             │       │ target           │                              │
│ category         │       │ version          │                              │
│ cuisine          │       │ channel          │                              │
│ calories         │       │ binary_url       │                              │
│ protein_g        │       │ checksum         │                              │
│ carbs_g          │       │ release_notes    │                              │
│ fats_g           │       │ is_mandatory     │                              │
│ recipe_data (J)  │       │ created_at       │                              │
│ tags             │       └──────────────────┘                              │
│ difficulty       │                                                         │
│ time_minutes     │                                                         │
│ image_url        │                                                         │
│ version          │                                                         │
│ is_published     │                                                         │
│ created_at       │             users.id ◄── user_preferences.user_id       │
│ updated_at       │             users.id ◄── push_tokens.user_id ───────────┘
└──────────────────┘             users.id ◄── appliances.user_id
                                  users.id ◄── cooking_sessions.user_id
```

---

## Table Definitions

### `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Unique user identifier |
| `email` | `varchar(255)` | UNIQUE, NOT NULL | Login email |
| `password_hash` | `varchar(255)` | NOT NULL | bcrypt hashed password |
| `name` | `varchar(100)` | NOT NULL | Display name |
| `role` | `varchar(20)` | NOT NULL, default `'user'` | `user` or `admin` |
| `is_active` | `boolean` | NOT NULL, default `true` | Account active flag |
| `created_at` | `timestamptz` | NOT NULL, default `now()` | Registration timestamp |
| `updated_at` | `timestamptz` | NOT NULL, default `now()` | Last modification |

### `user_preferences`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Row identifier |
| `user_id` | `uuid` | FK → `users.id`, UNIQUE, NOT NULL | One preferences row per user |
| `language` | `varchar(10)` | default `'en_IN'` | UI language code |
| `spice_level` | `integer` | default `3`, CHECK 1-5 | Default spice level |
| `salt_level` | `integer` | default `3`, CHECK 1-5 | Default salt level |
| `oil_level` | `integer` | default `3`, CHECK 1-5 | Default oil level |
| `diet` | `varchar(20)` | default `'no_restrictions'` | `vegetarian`, `vegan`, `pescatarian`, `no_restrictions` |
| `cuisines` | `text[]` | default `'{indian,italian,thai,mexican}'` | Preferred cuisine tags |
| `default_servings` | `integer` | default `2`, CHECK 1-4 | Default serving count |
| `allergens` | `text[]` | default `'{}'` | Array of allergen tags |
| `theme` | `varchar(10)` | default `'light'` | `light` or `dark` |
| `notifications_enabled` | `boolean` | default `true` | Push notification preference |
| `updated_at` | `timestamptz` | NOT NULL, default `now()` | Last update |

### `appliances`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Appliance record ID |
| `user_id` | `uuid` | FK → `users.id`, NOT NULL | Owner |
| `device_id` | `varchar(50)` | UNIQUE, NOT NULL | Hardware device ID (e.g., `EPIC-001`) |
| `serial_number` | `varchar(50)` | UNIQUE, NOT NULL | Manufacturing serial |
| `name` | `varchar(100)` | default `'My Epicura'` | User-assigned name |
| `firmware_version_cm5` | `varchar(20)` | | Current CM5 firmware |
| `firmware_version_stm32` | `varchar(20)` | | Current STM32 firmware |
| `wifi_mac` | `varchar(17)` | | WiFi MAC address |
| `pairing_code` | `varchar(6)` | | BLE pairing code (rotated) |
| `status` | `varchar(20)` | default `'offline'` | `online`, `offline`, `cooking`, `error` |
| `last_seen_at` | `timestamptz` | | Last heartbeat timestamp |
| `paired_at` | `timestamptz` | NOT NULL, default `now()` | Initial pairing time |
| `created_at` | `timestamptz` | NOT NULL, default `now()` | Record creation |

### `recipes`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Recipe identifier |
| `name` | `varchar(200)` | NOT NULL | Recipe display name |
| `category` | `varchar(50)` | NOT NULL | `dal`, `curry`, `rice`, `pasta`, `soup`, etc. |
| `cuisine` | `varchar(50)` | default `'indian'` | Cuisine: `indian`, `italian`, `american`, `chinese`, `mexican`, `korean`, `thai`, `asian`, `global` |
| `recipe_data` | `jsonb` | NOT NULL | Full recipe definition (stages, ingredients, temps) |
| `tags` | `text[]` | default `'{}'` | Filter tags: `vegan`, `healthy`, `vegetarian`, `protein-rich`, `stir-fry`, `gluten-free`, `quick` |
| `difficulty` | `varchar(10)` | NOT NULL | `easy`, `medium`, `hard` |
| `time_minutes` | `integer` | NOT NULL | Total estimated cooking time |
| `servings` | `integer` | NOT NULL, default `4` | Default serving count |
| `calories` | `real` | | Calories per serving (kcal) |
| `protein_g` | `real` | | Protein per serving (g) |
| `carbs_g` | `real` | | Carbohydrates per serving (g) |
| `fats_g` | `real` | | Fats per serving (g) |
| `image_url` | `text` | | Recipe photo URL (S3/R2) — food in bowl, displayed on left of recipe card |
| `version` | `integer` | NOT NULL, default `1` | Recipe version (incremented on edit) |
| `is_published` | `boolean` | NOT NULL, default `false` | Visible to users when true |
| `created_by` | `uuid` | FK → `users.id` | Admin who created the recipe |
| `created_at` | `timestamptz` | NOT NULL, default `now()` | Creation timestamp |
| `updated_at` | `timestamptz` | NOT NULL, default `now()` | Last modification |

**`recipe_data` JSONB Structure:**

The JSONB field stores the full recipe definition, matching the YAML format defined in [[../03-Software/04-Controller-Software-Architecture#Recipe Format (YAML)|Controller Software Architecture]]:

```json
{
  "name": "Dal Tadka",
  "servings": 4,
  "total_time_minutes": 35,
  "stages": [
    {
      "name": "Heat Oil",
      "temp_target": 180,
      "duration_seconds": 120,
      "stir": false,
      "ingredients": [
        {"subsystem": "SLD", "channel": "OIL", "name": "oil", "amount_g": 30}
      ],
      "cv_check": "oil_shimmer"
    },
    {
      "name": "Add Spices",
      "temp_target": 160,
      "ingredients": [
        {"subsystem": "ASD", "id": 1, "name": "turmeric", "amount_g": 3},
        {"subsystem": "ASD", "id": 2, "name": "chili_powder", "amount_g": 5}
      ],
      "cv_check": "spice_crackle",
      "stir": true,
      "stir_pattern": "intermittent"
    }
  ]
}
```

### `cooking_sessions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Session identifier |
| `user_id` | `uuid` | FK → `users.id`, NOT NULL | User who started the cook |
| `appliance_id` | `uuid` | FK → `appliances.id`, NOT NULL | Device used |
| `recipe_id` | `uuid` | FK → `recipes.id`, NOT NULL | Recipe cooked |
| `status` | `varchar(20)` | NOT NULL, default `'started'` | `started`, `cooking`, `paused`, `completed`, `aborted`, `error` |
| `started_at` | `timestamptz` | NOT NULL, default `now()` | Session start |
| `completed_at` | `timestamptz` | | Session end |
| `stages_log` | `jsonb` | | Array of `{stage, duration_s, result, cv_confidence}` |
| `customizations` | `jsonb` | | Spice level, servings, substitutions applied |
| `peak_temperature` | `real` | | Maximum temperature reached |
| `total_duration_s` | `integer` | | Actual cooking duration in seconds |
| `user_rating` | `integer` | CHECK 1-5 | User's star rating |
| `notes` | `text` | | User's notes about the cook |

### `telemetry_events` (Partitioned)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `bigserial` | PK (within partition) | Event sequence ID |
| `appliance_id` | `uuid` | FK → `appliances.id`, NOT NULL | Source device |
| `session_id` | `uuid` | FK → `cooking_sessions.id` | Associated cooking session (nullable for non-cooking events) |
| `event_type` | `varchar(50)` | NOT NULL | `temperature`, `status`, `stage_change`, `alert`, `heartbeat` |
| `payload` | `jsonb` | NOT NULL | Event-specific data |
| `recorded_at` | `timestamptz` | NOT NULL, default `now()` | Event timestamp |

**Partitioning Strategy:**

```sql
CREATE TABLE telemetry_events (
    id          BIGSERIAL,
    appliance_id UUID NOT NULL REFERENCES appliances(id),
    session_id  UUID REFERENCES cooking_sessions(id),
    event_type  VARCHAR(50) NOT NULL,
    payload     JSONB NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, recorded_at)
) PARTITION BY RANGE (recorded_at);

-- Monthly partitions (created automatically or via cron)
CREATE TABLE telemetry_events_2026_01 PARTITION OF telemetry_events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE telemetry_events_2026_02 PARTITION OF telemetry_events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
-- ...
```

### `push_tokens`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Token record ID |
| `user_id` | `uuid` | FK → `users.id`, NOT NULL | Token owner |
| `platform` | `varchar(10)` | NOT NULL | `ios` or `android` |
| `token` | `text` | UNIQUE, NOT NULL | FCM/APNs device token |
| `created_at` | `timestamptz` | NOT NULL, default `now()` | Registration time |
| `updated_at` | `timestamptz` | NOT NULL, default `now()` | Last refresh |

### `firmware_releases`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `uuid` | PK, default `gen_random_uuid()` | Release identifier |
| `target` | `varchar(10)` | NOT NULL | `cm5` or `stm32` |
| `version` | `varchar(20)` | NOT NULL | Semantic version (e.g., `1.2.0`) |
| `channel` | `varchar(20)` | NOT NULL, default `'stable'` | `stable`, `beta`, `alpha` |
| `binary_url` | `text` | NOT NULL | S3/R2 URL to firmware binary |
| `checksum_sha256` | `varchar(64)` | NOT NULL | SHA-256 of binary |
| `file_size_bytes` | `integer` | NOT NULL | Binary file size |
| `release_notes` | `text` | | Markdown release notes |
| `is_mandatory` | `boolean` | NOT NULL, default `false` | Force update if true |
| `min_version` | `varchar(20)` | | Minimum current version required to apply this update |
| `created_at` | `timestamptz` | NOT NULL, default `now()` | Release timestamp |

---

## Indexes

### Primary Indexes

```sql
-- Users
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Recipes
CREATE INDEX idx_recipes_category ON recipes(category);
CREATE INDEX idx_recipes_cuisine ON recipes(cuisine);
CREATE INDEX idx_recipes_published ON recipes(is_published) WHERE is_published = true;

-- Appliances
CREATE UNIQUE INDEX idx_appliances_device_id ON appliances(device_id);
CREATE INDEX idx_appliances_user ON appliances(user_id);

-- Cooking Sessions
CREATE INDEX idx_sessions_user ON cooking_sessions(user_id);
CREATE INDEX idx_sessions_appliance ON cooking_sessions(appliance_id);
CREATE INDEX idx_sessions_started ON cooking_sessions(started_at DESC);

-- Telemetry (per partition)
CREATE INDEX idx_telemetry_appliance_time ON telemetry_events(appliance_id, recorded_at DESC);
CREATE INDEX idx_telemetry_session ON telemetry_events(session_id) WHERE session_id IS NOT NULL;

-- Firmware
CREATE UNIQUE INDEX idx_firmware_target_version ON firmware_releases(target, version);
CREATE INDEX idx_firmware_channel ON firmware_releases(target, channel, created_at DESC);
```

### GIN Indexes (JSONB & Arrays)

```sql
-- Full recipe data search
CREATE INDEX idx_recipes_data ON recipes USING GIN (recipe_data jsonb_path_ops);

-- Recipe tags array search
CREATE INDEX idx_recipes_tags ON recipes USING GIN (tags);

-- Allergen array search
CREATE INDEX idx_prefs_allergens ON user_preferences USING GIN (allergens);

-- Cuisine preferences array search
CREATE INDEX idx_prefs_cuisines ON user_preferences USING GIN (cuisines);

-- Telemetry payload search
CREATE INDEX idx_telemetry_payload ON telemetry_events USING GIN (payload jsonb_path_ops);
```

### Full-Text Search

```sql
-- Recipe search by name and category
ALTER TABLE recipes ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(name, '') || ' ' || coalesce(category, '') || ' ' || coalesce(cuisine, ''))
    ) STORED;

CREATE INDEX idx_recipes_fts ON recipes USING GIN (search_vector);

-- Query example: search for "dal" or "lentil"
-- SELECT * FROM recipes WHERE search_vector @@ to_tsquery('english', 'dal | lentil');
```

---

## CM5 SQLite Sync Strategy

The Epicura CM5 device stores recipes and cooking logs locally in SQLite (see [[../03-Software/04-Controller-Software-Architecture#5. Data Management (CM5)|CM5 Data Management]]). The cloud sync strategy ensures consistency:

### Recipe Sync (Cloud → Device)

```
┌──────────┐     GET /recipes/sync?since=<timestamp>     ┌──────────┐
│  CM5     │ ──────────────────────────────────────────► │  Cloud   │
│  SQLite  │                                             │  Postgres│
│          │ ◄────────────────────────────────────────── │          │
│          │     {recipes: [...], deleted_ids: [...]}     │          │
└──────────┘                                             └──────────┘
```

1. CM5 stores `last_sync_at` timestamp in `user_preferences`
2. On sync, CM5 requests `GET /recipes/sync?since=<last_sync_at>`
3. Backend returns recipes with `updated_at > since` and list of deleted recipe IDs
4. CM5 upserts recipes into local SQLite and removes deleted ones
5. CM5 updates `last_sync_at` to server timestamp

### Cooking Log Sync (Device → Cloud)

1. CM5 stores cooking logs locally in SQLite
2. Logs marked `synced = false` are uploaded via `POST /sessions` on next connection
3. Backend stores in `cooking_sessions` table and marks as synced
4. Device marks local logs as `synced = true`

### Conflict Resolution

- **Recipes:** Cloud is authoritative; device always accepts cloud version
- **Cooking logs:** Device is authoritative; cloud stores whatever device reports
- **User preferences:** Last-write-wins with timestamp comparison

---

## Drizzle Migration Approach

Migrations are managed via Drizzle Kit:

```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push schema directly (dev only)
npx drizzle-kit push
```

Migration files are stored in `packages/db/migrations/` and version-controlled. Production migrations run as part of the deployment pipeline before the API server starts.

---

## Related Documentation

- [[01-Backend-Architecture|Backend Architecture]] - Service architecture and deployment
- [[../11-API/01-REST-API-Reference|REST API Reference]] - Endpoints that query this schema
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]] - CM5 SQLite schema
- [[03-Admin-Portal|Admin Portal]] - Admin interface for managing this data

#epicura #database #postgresql #schema #drizzle #backend

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 1.1 | 2026-02-17 | Manas Pradhan | Added nutrition columns (calories, protein_g, carbs_g, fats_g) to recipes; updated cuisine/tag values |
