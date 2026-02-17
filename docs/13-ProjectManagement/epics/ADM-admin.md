---
tags: [epicura, project-management, epic, admin, nextjs]
created: 2026-02-16
aliases: [ADM Epic, Admin Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 4 stories across Sprints 10–12 |
> | 2026-02-17 | Manas Pradhan | Split RCP.01 (8pts) → RCP.01+RCP.02; now 5 stories |

# Epic: ADM — Admin Portal (Next.js)

Web-based admin dashboard for recipe management, device monitoring, and user administration. Built with Next.js App Router, shadcn/ui, TanStack Table.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SET — Project Setup | 1 | 5 | 10 |
| RCP — Recipe Management | 2 | 8 | 10 |
| DEV — Device Monitoring | 1 | 5 | 11 |
| USR — User Administration | 1 | 5 | 12 |
| **Total** | **5** | **~22** | |

---

## Phase 4 — Admin Portal (Sprints 10–12)

### ADM-SET.01: Next.js project setup — App Router, shadcn/ui, auth, layout
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-SET.01|BE-SET.01]]
- **Blocks:** [[ADM-admin#ADM-RCP.01|ADM-RCP.01]], [[ADM-admin#ADM-DEV.01|ADM-DEV.01]], [[ADM-admin#ADM-USR.01|ADM-USR.01]]

**Acceptance Criteria:**
- [ ] Next.js 14+ with App Router, TypeScript, Tailwind CSS
- [ ] shadcn/ui components installed: Button, Table, Dialog, Form, Card, Tabs
- [ ] Admin auth: login page, JWT session, protected routes middleware
- [ ] Dashboard layout: sidebar navigation, header with user menu, main content area
- [ ] Admin-only access: reject non-admin users at middleware level

**Tasks:**
- [ ] `ADM-SET.01a` — Create Next.js project with App Router, TypeScript, Tailwind CSS
- [ ] `ADM-SET.01b` — Install and configure shadcn/ui; create theme with Epicura brand colors
- [ ] `ADM-SET.01c` — Implement admin auth: login, session management, route protection
- [ ] `ADM-SET.01d` — Create dashboard layout: sidebar nav (Recipes, Devices, Users), header, content
- [ ] `ADM-SET.01e` — Deploy to Vercel; configure preview deployments for PRs

---

### ADM-RCP.01: Recipe management — list, create/edit form, YAML editor
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[ADM-admin#ADM-SET.01|ADM-SET.01]], [[BE-backend#BE-RCP.01|BE-RCP.01]]
- **Blocks:** [[ADM-admin#ADM-RCP.02|ADM-RCP.02]]

**Acceptance Criteria:**
- [ ] Recipe list: TanStack Table with sort, search, pagination
- [ ] Recipe create/edit form: name, cuisine, servings, time, difficulty
- [ ] YAML editor: Monaco editor for ingredients and steps with syntax highlighting

**Tasks:**
- [ ] `ADM-RCP.01a` — Implement recipe list page with TanStack Table, server-side pagination
- [ ] `ADM-RCP.01b` — Implement recipe form with shadcn/ui Form and Zod validation
- [ ] `ADM-RCP.01c` — Integrate Monaco editor for YAML ingredient/step editing

---

### ADM-RCP.02: Recipe management — image upload, preview, delete
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[ADM-admin#ADM-RCP.01|ADM-RCP.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Image upload with drag-and-drop and presigned URL; preview before save
- [ ] Recipe preview: rendered view of YAML steps as timeline
- [ ] Delete with confirmation dialog; soft delete with undo

**Tasks:**
- [ ] `ADM-RCP.02a` — Implement image upload with drag-and-drop and presigned URL
- [ ] `ADM-RCP.02b` — Implement recipe preview renderer for YAML steps
- [ ] `ADM-RCP.02c` — Implement delete with confirmation and soft-delete/undo

---

### ADM-DEV.01: Device monitoring — list, status, telemetry, commands
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[ADM-admin#ADM-SET.01|ADM-SET.01]], [[BE-backend#BE-DEV.01|BE-DEV.01]], [[BE-backend#BE-MQT.01|BE-MQT.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Device list: table with device UUID, owner, status (online/offline/cooking), firmware version
- [ ] Device detail: real-time telemetry (temperature, sensor readings) with time-series chart
- [ ] Command panel: send commands to device (start cook, abort, request update)
- [ ] Cooking session history for each device
- [ ] Firmware version overview: count of devices per version for update tracking

**Tasks:**
- [ ] `ADM-DEV.01a` — Implement device list page with status indicators and filtering
- [ ] `ADM-DEV.01b` — Implement device detail with telemetry charts (Recharts or Chart.js)
- [ ] `ADM-DEV.01c` — Implement command panel with confirmation dialogs
- [ ] `ADM-DEV.01d` — Implement cooking session history table per device
- [ ] `ADM-DEV.01e` — Implement firmware version overview dashboard card

---

### ADM-USR.01: User administration — list, detail, roles
- **Sprint:** [[sprint-12|Sprint 12]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[ADM-admin#ADM-SET.01|ADM-SET.01]], [[BE-backend#BE-USR.01|BE-USR.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] User list: table with name, email, devices count, last active, role
- [ ] User detail: profile info, claimed devices, cooking history summary
- [ ] Role management: assign/revoke admin role
- [ ] User search and filter by role, active status
- [ ] Account actions: disable, enable, delete (with confirmation)

**Tasks:**
- [ ] `ADM-USR.01a` — Implement user list with TanStack Table, search, and role filter
- [ ] `ADM-USR.01b` — Implement user detail page with device and history sections
- [ ] `ADM-USR.01c` — Implement role management with role select dropdown
- [ ] `ADM-USR.01d` — Implement account actions: disable/enable toggle, delete with confirmation

---

## Dependencies

### What ADM blocks

None — Admin portal is a leaf node.

### What blocks ADM

| ADM Story | Blocked by | Reason |
|-----------|------------|--------|
| ADM-SET.01 | BE-SET.01 | Needs backend auth API |
| ADM-RCP.01 | ADM-SET.01, BE-RCP.01 | Needs portal scaffold + recipe API |
| ADM-RCP.02 | ADM-RCP.01 | Needs recipe list and form |
| ADM-DEV.01 | ADM-SET.01, BE-DEV.01, BE-MQT.01 | Needs portal + device API + MQTT |
| ADM-USR.01 | ADM-SET.01, BE-USR.01 | Needs portal + user API |

---

## References

- [[__Workspaces/Epicura/docs/10-Backend/03-Admin-Portal|Admin Portal Design]]
- [[__Workspaces/Epicura/docs/11-API/01-REST-API-Reference|REST API Reference]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
