---
tags: [epicura, project-management, epic, ui, kivy, touchscreen]
created: 2026-02-16
aliases: [UI Epic, Touchscreen Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 4 stories across Sprints 9–10 |
> | 2026-02-17 | Manas Pradhan | Split UI-COK.01 (8pts) into UI-COK.01 (5pts) + UI-COK.02 (3pts) |

# Epic: UI — Touchscreen UI (Kivy)

10" capacitive touchscreen interface built with Kivy, running as a Docker container on CM5. Provides recipe browsing, live cooking status with camera feed, and settings/diagnostics screens.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SET — App Scaffold | 1 | 5 | 9 |
| RCP — Recipe Browser | 1 | 5 | 9 |
| COK — Cooking Screen | 2 | 8 | 10 |
| MNT — Settings & Maintenance | 1 | 5 | 10 |
| **Total** | **5** | **~24** | |

---

## Phase 3 — UI Development (Sprints 9–10)

### UI-SET.01: Kivy app scaffold — screen manager, theme, navigation, GPU acceleration
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#138](https://github.com/manasXP/epicura/issues/138)
- **Blocked by:** [[EMB-embedded#EMB-SET.02|EMB-SET.02]], [[EMB-embedded#EMB-SET.03|EMB-SET.03]]
- **Blocks:** [[UI-touchscreen#UI-RCP.01|UI-RCP.01]], [[UI-touchscreen#UI-COK.01|UI-COK.01]], [[UI-touchscreen#UI-MNT.01|UI-MNT.01]]

**Acceptance Criteria:**
- [ ] Kivy app launches on 10" DSI display at 1280×800 resolution
- [ ] GPU acceleration enabled (EGL/DRM) with smooth 60fps transitions
- [ ] Screen manager with slide transitions: Home, Recipe List, Recipe Detail, Cooking, Settings
- [ ] Touch input working on capacitive touchscreen; multi-touch for pinch-zoom on recipe images
- [ ] Custom theme: dark mode with high-contrast food imagery, large touch targets (min 48×48dp)
- [ ] MQTT client connected for real-time status updates from recipe engine

**Tasks:**
- [ ] `UI-SET.01a` — Create Kivy project structure: main.py, screens/, widgets/, assets/
- [ ] `UI-SET.01b` — Configure Kivy for DSI display: resolution, DPI, touch input device
- [ ] `UI-SET.01c` — Implement ScreenManager with all screen stubs and slide transitions
- [ ] `UI-SET.01d` — Create custom theme: colors, fonts, button styles, card layouts
- [ ] `UI-SET.01e` — Implement MQTT client integration: subscribe to cook status, sensor data, alerts
- [ ] `UI-SET.01f` — Test on 10" display: verify touch, transitions, and rendering performance

---

### UI-RCP.01: Recipe browser — grid view, detail view, search, favorites
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#141](https://github.com/manasXP/epicura/issues/141)
- **Blocked by:** [[UI-touchscreen#UI-SET.01|UI-SET.01]], [[RCP-recipe#RCP-FMT.01|RCP-FMT.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Recipe list displayed as scrollable grid (2 columns) with thumbnail, name, time, servings
- [ ] Recipe detail screen: full image, ingredient list, step-by-step preview, estimated time
- [ ] Search bar with text input; filters recipes by name, cuisine, ingredient
- [ ] Favorites: heart icon toggle; favorites stored in local PostgreSQL
- [ ] Recipes loaded from local PostgreSQL cache (offline-first)
- [ ] "Start Cooking" button on detail screen navigates to cooking screen

**Tasks:**
- [ ] `UI-RCP.01a` — Implement RecipeListScreen: grid layout with RecycleView for performance
- [ ] `UI-RCP.01b` — Implement recipe card widget: thumbnail, title, metadata badges
- [ ] `UI-RCP.01c` — Implement RecipeDetailScreen: scrollable layout with ingredient table and step list
- [ ] `UI-RCP.01d` — Implement search functionality with real-time filtering
- [ ] `UI-RCP.01e` — Implement favorites toggle with PostgreSQL persistence
- [ ] `UI-RCP.01f` — Test with 20+ recipes: verify scroll performance and image loading

---

### UI-COK.01: Live cooking screen — camera feed, status, temperature, timer
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#143](https://github.com/manasXP/epicura/issues/143)
- **Blocked by:** [[UI-touchscreen#UI-SET.01|UI-SET.01]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]
- **Blocks:** [[UI-touchscreen#UI-COK.02|UI-COK.02]]

**Acceptance Criteria:**
- [ ] Live camera feed (720p) displayed in main area with CV stage overlay
- [ ] Current cooking state and step shown with progress bar
- [ ] Temperature display: current (IR) vs target, with visual gauge
- [ ] Timer: countdown for current step; total elapsed time
- [ ] Screen stays awake during cooking (no screen timeout)

**Tasks:**
- [ ] `UI-COK.01a` — Implement camera feed widget using picamera2 preview or MJPEG stream
- [ ] `UI-COK.01b` — Implement status panel: state label, step name, progress bar
- [ ] `UI-COK.01c` — Implement temperature gauge widget: current vs target, color-coded
- [ ] `UI-COK.01d` — Implement timer widget: step countdown + total elapsed

---

### UI-COK.02: Cooking screen controls and alerts — pause/resume, abort, alert banners
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 3
- **GitHub:** [#144](https://github.com/manasXP/epicura/issues/144)
- **Blocked by:** [[UI-touchscreen#UI-COK.01|UI-COK.01]]
- **Blocks:** [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] Control buttons: Pause/Resume, Abort (with confirmation dialog)
- [ ] Dispensing status: current ingredient being dispensed, progress
- [ ] Alert banners: thermal warning (yellow), safety shutdown (red), dispense error (orange)
- [ ] All real-time widgets tested during simulated cook

**Tasks:**
- [ ] `UI-COK.02a` — Implement control buttons: pause/resume (MQTT publish), abort with confirmation
- [ ] `UI-COK.02b` — Implement alert banner system: subscribe to MQTT alerts, display with severity colors
- [ ] `UI-COK.02c` — Test during simulated cook: verify all widgets update in real-time

---

### UI-MNT.01: Settings & maintenance — WiFi, calibration, diagnostics, about
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P1
- **Points:** 5
- **GitHub:** [#145](https://github.com/manasXP/epicura/issues/145)
- **Blocked by:** [[UI-touchscreen#UI-SET.01|UI-SET.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] WiFi settings: scan, connect, forget networks; show signal strength
- [ ] Calibration screen: trigger dispenser calibration, view results, last calibration date
- [ ] Diagnostics screen: sensor readings (IR temp, CAN coil temp, load cells), actuator status, CAN bus status
- [ ] System info: firmware version, device UUID, storage usage, uptime
- [ ] Factory reset option (with double-confirmation)
- [ ] OTA update check and install progress display

**Tasks:**
- [ ] `UI-MNT.01a` — Implement WiFi settings screen using nmcli or NetworkManager D-Bus API
- [ ] `UI-MNT.01b` — Implement calibration screen: trigger via MQTT command, display results
- [ ] `UI-MNT.01c` — Implement diagnostics screen: live sensor readings via MQTT subscription
- [ ] `UI-MNT.01d` — Implement system info screen: read firmware version, disk usage, uptime
- [ ] `UI-MNT.01e` — Implement factory reset with double confirmation dialog
- [ ] `UI-MNT.01f` — Implement OTA update screen: check for updates, download progress, install status

---

## Dependencies

### What UI blocks (downstream consumers)

| UI Story | Blocks | Reason |
|----------|--------|--------|
| UI-COK.02 | INT-SYS.01 | Cooking UI needed for end-to-end integration test |

### What blocks UI (upstream dependencies)

| UI Story | Blocked by | Reason |
|----------|------------|--------|
| UI-SET.01 | EMB-SET.02, EMB-SET.03 | Need CM5 Docker + Kivy container |
| UI-RCP.01 | UI-SET.01, RCP-FMT.01 | Need app scaffold and recipe format |
| UI-COK.01 | UI-SET.01, RCP-FSM.01 | Need app scaffold and state machine |
| UI-COK.02 | UI-COK.01 | Need cooking screen base layout |
| UI-MNT.01 | UI-SET.01 | Need app scaffold |

---

## References

- [[__Workspaces/Epicura/docs/04-UserInterface/01-UI-UX-Design|UI/UX Design]]
- [[__Workspaces/Epicura/docs/03-Software/01-Tech-Stack|Tech Stack]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
