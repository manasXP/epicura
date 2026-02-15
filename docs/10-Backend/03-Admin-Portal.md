---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Admin Portal

## Overview

The Epicura Admin Portal is a web application for internal team use, providing recipe management (CRUD with stage editor), appliance registration and monitoring, user management, firmware release publishing, analytics dashboards, and push notification broadcasting.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Next.js 15 (App Router) | SSR, Server Actions, file-based routing |
| **UI Library** | shadcn/ui + Radix UI | Accessible, composable component primitives |
| **Styling** | Tailwind CSS 4 | Utility-first styling |
| **State / Data** | TanStack Query v5 | Server state management, caching, pagination |
| **Forms** | React Hook Form + Zod | Performant forms with schema validation |
| **Charts** | Recharts | Analytics dashboards and telemetry visualization |
| **Tables** | TanStack Table v8 | Sortable, filterable, paginated data tables |
| **Auth** | JWT (same API as mobile apps) | Admin role required for all routes |
| **Notifications** | Sonner | Toast notifications |

---

## Page Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Overview metrics, recent activity, system health |
| `/login` | Login | Admin authentication |
| `/recipes` | Recipe List | Searchable, filterable recipe table |
| `/recipes/new` | Create Recipe | Recipe editor with stage builder |
| `/recipes/[id]` | Edit Recipe | Edit existing recipe |
| `/recipes/[id]/preview` | Recipe Preview | Preview recipe as it appears on device |
| `/appliances` | Appliance List | Registered devices with status |
| `/appliances/[id]` | Appliance Detail | Device info, recent sessions, telemetry |
| `/users` | User List | User accounts management |
| `/users/[id]` | User Detail | User profile, preferences, linked appliances |
| `/firmware` | Firmware Releases | Manage firmware versions |
| `/firmware/new` | Create Release | Upload firmware binary, set channel |
| `/analytics` | Analytics | Cooking stats, popular recipes, device health |
| `/notifications` | Push Notifications | Broadcast push to all or filtered users |

---

## Dashboard

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Epicura Admin                                        [Admin Name] [▼]  │
├────────┬─────────────────────────────────────────────────────────────────┤
│        │                                                                 │
│  Nav   │   Dashboard                                                     │
│        │                                                                 │
│  ○ Dash│   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐│
│  ○ Rec │   │ Total Users│  │  Appliances│  │  Sessions  │  │ Recipes  ││
│  ○ App │   │   1,247    │  │    312     │  │   8,432    │  │   142    ││
│  ○ User│   │  +23 today │  │  286 online│  │  +156 today│  │ 12 draft ││
│  ○ FW  │   └────────────┘  └────────────┘  └────────────┘  └──────────┘│
│  ○ Ana │                                                                 │
│  ○ Push│   ┌──────────────────────────────────────────────────────────┐  │
│        │   │  Cooking Sessions (Last 30 Days)           [Line Chart] │  │
│        │   │                                                          │  │
│        │   │  ████                                                    │  │
│        │   │  ██████                                                  │  │
│        │   │  ████████                                                │  │
│        │   │  ██████████████                                          │  │
│        │   └──────────────────────────────────────────────────────────┘  │
│        │                                                                 │
│        │   Recent Activity                                               │
│        │   ┌──────────────────────────────────────────────────────────┐  │
│        │   │ EPIC-312  Completed "Dal Tadka"       ★★★★★   2 min ago │  │
│        │   │ EPIC-045  Started "Paneer Butter"              5 min ago │  │
│        │   │ EPIC-189  Firmware updated to v1.2.1          12 min ago │  │
│        │   │ User #423 Registered new appliance            28 min ago │  │
│        │   └──────────────────────────────────────────────────────────┘  │
│        │                                                                 │
└────────┴─────────────────────────────────────────────────────────────────┘
```

---

## Recipe Editor

The recipe editor is the most complex page, featuring a stage-by-stage builder that matches the YAML recipe format used by the CM5.

### Recipe Editor Wireframe

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Epicura Admin  >  Recipes  >  Edit: Dal Tadka                          │
├────────┬─────────────────────────────────────────────────────────────────┤
│        │                                                                 │
│  Nav   │   Recipe Details                    [Save Draft] [Publish]      │
│        │                                                                 │
│        │   Name:     [Dal Tadka                              ]          │
│        │   Category: [Dal           ▼]   Cuisine: [Indian       ▼]     │
│        │   Difficulty:[Easy         ▼]   Time:    [35    ] min          │
│        │   Servings:  [4            ]    Tags:    [vegetarian, quick]   │
│        │                                                                 │
│        │   Image: [recipe-dal-tadka.jpg]  [Upload New]                  │
│        │                                                                 │
│        │   ──── Cooking Stages ────                                      │
│        │                                                                 │
│        │   ┌─ Stage 1: Heat Oil ──────────────────────── [✎] [✕] [↕]┐  │
│        │   │  Temp Target: [180]°C    Duration: [120] sec            │  │
│        │   │  Stir: [Off]             CV Check: [oil_shimmer    ▼]   │  │
│        │   │  Ingredients:                                            │  │
│        │   │    Comp 1: oil — 30 ml                    [+ Add]       │  │
│        │   └─────────────────────────────────────────────────────────┘  │
│        │                                                                 │
│        │   ┌─ Stage 2: Add Tempering ─────────────────── [✎] [✕] [↕]┐  │
│        │   │  Temp Target: [160]°C    Duration: [  ] sec             │  │
│        │   │  Stir: [Intermittent]    CV Check: [spice_crackle  ▼]   │  │
│        │   │  Ingredients:                                            │  │
│        │   │    Comp 2: cumin_mustard — 5 g             [+ Add]      │  │
│        │   └─────────────────────────────────────────────────────────┘  │
│        │                                                                 │
│        │   ┌─ Stage 3: Saute Onions ──────────────────── [✎] [✕] [↕]┐  │
│        │   │  ...                                                     │  │
│        │   └─────────────────────────────────────────────────────────┘  │
│        │                                                                 │
│        │   [+ Add Stage]                                                 │
│        │                                                                 │
│        │   ──── JSON Preview ────                                        │
│        │   ┌─────────────────────────────────────────────────────────┐  │
│        │   │ {"name":"Dal Tadka","servings":4,"stages":[...]}        │  │
│        │   └─────────────────────────────────────────────────────────┘  │
│        │                                                                 │
└────────┴─────────────────────────────────────────────────────────────────┘
```

### Stage Editor Features

- Drag-and-drop stage reordering (via `[↕]` handle)
- Each stage has: name, temperature target, duration, stir pattern, CV check class, and ingredients
- Ingredients include subsystem (ASD/CID/SLD), ID/channel, name, and amount (g)
- JSON preview panel shows the `recipe_data` JSONB that will be stored
- Schema validation via Zod before save (matches CM5 recipe format)
- "Preview" button renders the recipe as it would appear on the touchscreen UI

---

## Appliance Management

| Column | Description |
|--------|-------------|
| Device ID | Hardware identifier (e.g., `EPIC-001`) |
| Serial | Manufacturing serial number |
| Owner | Linked user email |
| Status | Online / Offline / Cooking / Error (color-coded) |
| FW (CM5) | Current CM5 firmware version |
| FW (STM32) | Current STM32 firmware version |
| Last Seen | Time since last heartbeat |
| Sessions | Total cooking sessions count |

**Detail View:** Shows device telemetry history, recent cooking sessions, firmware update history, and option to remotely trigger OTA update.

---

## User Management

| Column | Description |
|--------|-------------|
| Name | User display name |
| Email | Login email |
| Role | `user` or `admin` |
| Appliances | Number of paired appliances |
| Sessions | Total cooking sessions |
| Joined | Registration date |
| Status | Active / Inactive |

**Actions:** View profile, reset password, toggle active status, promote to admin.

---

## Firmware Release Management

| Field | Description |
|-------|-------------|
| Target | CM5 or STM32 |
| Version | Semantic version string |
| Channel | `stable`, `beta`, `alpha` |
| Binary | Upload firmware file (.img for CM5, .bin for STM32) |
| Checksum | Auto-computed SHA-256 on upload |
| Release Notes | Markdown text field |
| Mandatory | Toggle: force-update all devices |
| Min Version | Minimum required current version to apply |

**Workflow:** Upload binary → auto-compute checksum → write release notes → select channel → publish. Devices check for updates via `GET /firmware/latest`.

---

## Analytics Charts

| Chart | Type | Data Source |
|-------|------|-------------|
| Sessions per Day | Line chart | `cooking_sessions.started_at` |
| Popular Recipes | Horizontal bar | `cooking_sessions` grouped by `recipe_id` |
| Average Rating | Bar chart | `cooking_sessions.user_rating` by recipe |
| Active Devices | Area chart | `appliances.last_seen_at` by day |
| New Users | Line chart | `users.created_at` by day |
| Session Outcomes | Donut chart | `cooking_sessions.status` distribution |
| Avg Cook Duration | Bar chart | `cooking_sessions.total_duration_s` by recipe |
| Firmware Versions | Pie chart | `appliances.firmware_version_cm5` distribution |

---

## Push Notification Broadcast

Admin can send push notifications to:
- **All users** — Announcements, new recipe collections
- **Filtered users** — By appliance firmware version, last active date, or custom criteria
- **Individual user** — Support or troubleshooting

| Field | Description |
|-------|-------------|
| Title | Notification title (max 50 chars) |
| Body | Notification body (max 200 chars) |
| Target | All / Filtered / Specific user |
| Platform | Both / iOS only / Android only |
| Schedule | Send now / Schedule for later |
| Deep Link | Optional: route to specific recipe or screen |

---

## Related Documentation

- [[01-Backend-Architecture|Backend Architecture]] - Monorepo structure, API server
- [[02-Database-Schema|Database Schema]] - Tables and indexes
- [[../11-API/01-REST-API-Reference|REST API Reference]] - API endpoints consumed by admin portal
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]] - Device touchscreen design reference

#epicura #admin #nextjs #dashboard #recipe-editor #backend

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
