---
tags: [epicura, project-management, epic, ios, swiftui]
created: 2026-02-16
aliases: [IOS Epic, iOS Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 5 stories across Sprints 8–12 |
> | 2026-02-17 | Manas Pradhan | Split BLE.01 (8pts) → BLE.01+BLE.02, COK.01 (8pts) → COK.01+COK.02; now 7 stories |

# Epic: IOS — iOS App (SwiftUI)

Native iOS companion app for Epicura: BLE device pairing, WiFi provisioning, recipe browsing, live cooking view with camera stream, and user profile. Built with SwiftUI, MVVM, async/await.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SET — Project Setup | 1 | 5 | 8 |
| BLE — BLE Pairing | 2 | 8 | 8 |
| RCP — Recipe Browsing | 1 | 5 | 9 |
| COK — Live Cooking | 2 | 8 | 10 |
| USR — User Profile | 1 | 5 | 11 |
| **Total** | **7** | **~30** | |

---

## Phase 3 — Mobile Foundation (Sprint 8)

### IOS-SET.01: Xcode project setup — SwiftUI, MVVM, networking, auth
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-SET.01|BE-SET.01]]
- **Blocks:** [[IOS-ios#IOS-BLE.01|IOS-BLE.01]], [[IOS-ios#IOS-RCP.01|IOS-RCP.01]]

**Acceptance Criteria:**
- [ ] Xcode project created with SwiftUI, minimum iOS 17
- [ ] MVVM architecture with @Observable view models
- [ ] Networking layer: async/await HTTP client, JWT token management, auto-refresh
- [ ] Login/register screens connected to backend auth API
- [ ] Tab bar navigation: Recipe, Favourite, Session, Profile
- [ ] SwiftLint configured; CI pipeline runs lint + build + test

**Tasks:**
- [ ] `IOS-SET.01a` — Create Xcode project; configure SwiftUI App lifecycle, deployment target iOS 17
- [ ] `IOS-SET.01b` — Create networking layer: URLSession wrapper, JWT storage (Keychain), token refresh
- [ ] `IOS-SET.01c` — Implement auth flow: login, register, token persistence, auto-login
- [ ] `IOS-SET.01d` — Create tab bar navigation with Recipe, Favourite, Session, Profile tabs
- [ ] `IOS-SET.01e` — Configure SwiftLint; create GitHub Actions CI workflow

---

### IOS-BLE.01: BLE pairing — CoreBluetooth scanning, WiFi provisioning
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[IOS-ios#IOS-SET.01|IOS-SET.01]], [[BE-backend#BE-DEV.01|BE-DEV.01]]
- **Blocks:** [[IOS-ios#IOS-BLE.02|IOS-BLE.02]]

**Acceptance Criteria:**
- [ ] BLE scan discovers Epicura devices advertising service UUID
- [ ] Pairing flow: scan → select device → connect → exchange WiFi credentials → verify connection
- [ ] WiFi SSID and password sent to device via BLE characteristic write
- [ ] Device confirms WiFi connection and registers with cloud API

**Tasks:**
- [ ] `IOS-BLE.01a` — Implement CoreBluetooth manager: scan, connect, discover services
- [ ] `IOS-BLE.01b` — Implement BLE pairing flow UI: scan screen, device list, pairing progress
- [ ] `IOS-BLE.01c` — Implement WiFi provisioning: write SSID/password to BLE characteristic

---

### IOS-BLE.02: BLE device management — claim API, home screen status, end-to-end test
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[IOS-ios#IOS-BLE.01|IOS-BLE.01]]
- **Blocks:** [[IOS-ios#IOS-COK.01|IOS-COK.01]]

**Acceptance Criteria:**
- [ ] App claims device via POST `/api/devices/:id/claim`
- [ ] Paired device shown on Home screen with status (online/offline/cooking)
- [ ] End-to-end BLE test with Epicura device (or BLE simulator)

**Tasks:**
- [ ] `IOS-BLE.02a` — Implement device claim API call after successful WiFi connection
- [ ] `IOS-BLE.02b` — Implement Home screen with paired device card and status indicator
- [ ] `IOS-BLE.02c` — Test BLE flow end-to-end with Epicura device (or BLE simulator)

---

## Phase 3 — Recipe & Cooking (Sprints 9–10)

### IOS-RCP.01: Recipe browsing — list, detail, search, favorites
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[IOS-ios#IOS-SET.01|IOS-SET.01]], [[BE-backend#BE-RCP.01|BE-RCP.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Recipe list: horizontal card layout with food bowl image on left, name/time/difficulty on right
- [ ] Nutrition per serving on each card: Protein (g), Carbs (g), Fats (g), Calories (kcal)
- [ ] Tag filter chips (horizontally scrollable): All Recipes, Vegan, Healthy, Vegetarian, Protein Rich, Stir Fry, Gluten Free, Quick Recipe
- [ ] Cuisine filter chips (second row): Indian, Italian, American, Chinese, Mexican, Korean, Thai, Asian, Global
- [ ] Recipe detail: full image, ingredient list, step preview, nutrition info
- [ ] Search: text search with debounce
- [ ] Favorites: heart toggle, persisted locally and synced to cloud
- [ ] Pull-to-refresh and infinite scroll pagination
- [ ] "Start Cooking" button sends command to device via API

**Tasks:**
- [ ] `IOS-RCP.01a` — Implement recipe list with horizontal card layout (bowl image left, details + nutrition right)
- [ ] `IOS-RCP.01b` — Implement tag and cuisine filter chip rows
- [ ] `IOS-RCP.01c` — Implement recipe detail view with ingredient, step, and nutrition sections
- [ ] `IOS-RCP.01d` — Implement search with debounce
- [ ] `IOS-RCP.01e` — Implement favorites with local persistence (SwiftData) and cloud sync
- [ ] `IOS-RCP.01f` — Implement "Start Cooking" button with device command API call

---

### IOS-COK.01: Live cooking view — camera stream, status, temperature, timer
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[IOS-ios#IOS-BLE.02|IOS-BLE.02]]
- **Blocks:** [[IOS-ios#IOS-COK.02|IOS-COK.02]]

**Acceptance Criteria:**
- [ ] Live camera stream from device via WebSocket (MJPEG or H.264)
- [ ] Cooking status overlay: current state, step name, progress bar
- [ ] Temperature display: current vs target with animated gauge
- [ ] Timer: step countdown and total elapsed

**Tasks:**
- [ ] `IOS-COK.01a` — Implement WebSocket client for camera stream; render in AVPlayerLayer or UIImage
- [ ] `IOS-COK.01b` — Implement cooking status view: state, step, progress from MQTT via API polling
- [ ] `IOS-COK.01c` — Implement temperature gauge with SwiftUI animation
- [ ] `IOS-COK.01d` — Implement timer with background countdown

---

### IOS-COK.02: Cooking controls and notifications — pause/abort, push notifications, background alerts
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[IOS-ios#IOS-COK.01|IOS-COK.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Controls: Pause/Resume, Abort (with confirmation alert)
- [ ] Push notifications (APNs) for cooking events: done, error, attention needed
- [ ] Background audio alert when cooking requires user intervention
- [ ] Tested with live device: verify stream quality and control responsiveness

**Tasks:**
- [ ] `IOS-COK.02a` — Implement pause/resume and abort controls via device command API
- [ ] `IOS-COK.02b` — Implement push notifications (APNs) for cooking events
- [ ] `IOS-COK.02c` — Test with live device: verify stream quality and control responsiveness

---

## Phase 4 — User Profile (Sprint 11)

### IOS-USR.01: User profile — settings, cooking history, preferences
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-USR.01|BE-USR.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Profile screen: name, email, avatar (photo picker), dietary preferences
- [ ] Cooking history: chronological list with recipe name, date, duration, status
- [ ] Preferences: spice level slider, serving size picker, favorite cuisines
- [ ] Device management: list paired devices, unpair option
- [ ] Settings: notifications toggle, units (metric/imperial), logout, delete account

**Tasks:**
- [ ] `IOS-USR.01a` — Implement profile view with editable fields and avatar picker
- [ ] `IOS-USR.01b` — Implement cooking history list with recipe detail navigation
- [ ] `IOS-USR.01c` — Implement preferences screen with local + cloud sync
- [ ] `IOS-USR.01d` — Implement device management: list, unpair, rename
- [ ] `IOS-USR.01e` — Implement settings: notifications, units, logout, account deletion

---

### IOS-LIVE.01: Live Activity — Cooking Progress on Lock Screen & Dynamic Island
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[IOS-ios#IOS-COK.01|IOS-COK.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Live Activity starts when cooking session begins (WebSocket event or local push)
- [ ] Lock Screen: recipe name, current stage, temperature (current/target), progress bar, time remaining
- [ ] Dynamic Island compact: recipe name + time remaining
- [ ] Dynamic Island expanded: recipe name, stage, temperature gauge, progress bar, time remaining
- [ ] Real-time updates via ActivityKit push token notifications
- [ ] Live Activity ends on cooking complete/fail/abort with final status
- [ ] Tapping deep-links to cooking session screen
- [ ] Stale activity alert if no update in 60s

**Tasks:**
- [ ] `IOS-LIVE.01a` — Define `CookingActivityAttributes` (static: recipe name/image; dynamic: stage, temp, progress, timeRemaining)
- [ ] `IOS-LIVE.01b` — Implement Lock Screen Live Activity layout
- [ ] `IOS-LIVE.01c` — Implement Dynamic Island compact and expanded views
- [ ] `IOS-LIVE.01d` — Wire ActivityKit start/update/end to cooking WebSocket events
- [ ] `IOS-LIVE.01e` — Implement APNs push token updates for background refresh

---

## Dependencies

### What IOS blocks

| IOS Story | Blocks | Reason |
|-----------|--------|--------|
| None | — | iOS app is a leaf node; no other epics depend on it |

### What blocks IOS

| IOS Story | Blocked by | Reason |
|-----------|------------|--------|
| IOS-SET.01 | BE-SET.01 | Needs backend auth API |
| IOS-BLE.01 | IOS-SET.01, BE-DEV.01 | Needs networking layer + device API |
| IOS-BLE.02 | IOS-BLE.01 | Needs BLE pairing flow |
| IOS-RCP.01 | IOS-SET.01, BE-RCP.01 | Needs app scaffold + recipe API |
| IOS-COK.01 | IOS-BLE.02 | Needs paired device for streaming |
| IOS-COK.02 | IOS-COK.01 | Needs live cooking view |
| IOS-USR.01 | BE-USR.01 | Needs user API |

---

## References

- [[__Workspaces/Epicura/docs/12-MobileApps/02-iOS-App|iOS App Details]]
- [[__Workspaces/Epicura/docs/12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]
- [[__Workspaces/Epicura/docs/11-API/04-BLE-Services|BLE Services]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
