---
tags: [epicura, project-management, epic, android, kotlin, compose]
created: 2026-02-16
aliases: [AND Epic, Android Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 5 stories across Sprints 8–12 |
> | 2026-02-17 | Manas Pradhan | Split BLE.01 (8pts) → BLE.01+BLE.02, COK.01 (8pts) → COK.01+COK.02; now 7 stories |

# Epic: AND — Android App (Kotlin/Compose)

Native Android companion app mirroring iOS functionality: BLE device pairing, WiFi provisioning, recipe browsing, live cooking view, and user profile. Built with Kotlin, Jetpack Compose, MVVM, Hilt DI.

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

### AND-SET.01: Gradle project setup — Compose, Hilt, networking, auth
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-SET.01|BE-SET.01]]
- **Blocks:** [[AND-android#AND-BLE.01|AND-BLE.01]], [[AND-android#AND-RCP.01|AND-RCP.01]]

**Acceptance Criteria:**
- [ ] Android project with Kotlin, Jetpack Compose, minimum SDK 28 (Android 9)
- [ ] MVVM with Hilt DI, Retrofit + OkHttp for networking, Kotlin Serialization
- [ ] JWT token management: encrypted SharedPreferences, auto-refresh interceptor
- [ ] Login/register screens connected to backend auth API
- [ ] Bottom navigation: Recipe, Favourite, Session, Profile
- [ ] ktlint configured; CI pipeline runs lint + build + test

**Tasks:**
- [ ] `AND-SET.01a` — Create Gradle project; configure Compose, Hilt, Retrofit, Navigation Compose
- [ ] `AND-SET.01b` — Create networking layer: Retrofit client, JWT interceptor, token storage (EncryptedSharedPreferences)
- [ ] `AND-SET.01c` — Implement auth flow: login, register, token persistence, auto-login
- [ ] `AND-SET.01d` — Create bottom navigation with NavHost: Recipe, Favourite, Session, Profile tabs
- [ ] `AND-SET.01e` — Configure ktlint; create GitHub Actions CI workflow

---

### AND-BLE.01: BLE pairing — CompanionDeviceManager scanning, WiFi provisioning
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[AND-android#AND-SET.01|AND-SET.01]], [[BE-backend#BE-DEV.01|BE-DEV.01]]
- **Blocks:** [[AND-android#AND-BLE.02|AND-BLE.02]]

**Acceptance Criteria:**
- [ ] CompanionDeviceManager discovers Epicura devices by service UUID
- [ ] Pairing flow UI: scan → select → connect → send WiFi credentials → verify
- [ ] WiFi SSID/password sent via BLE GATT characteristic write
- [ ] Runtime permissions handled: Bluetooth, Location (for BLE scan on older APIs)

**Tasks:**
- [ ] `AND-BLE.01a` — Implement CompanionDeviceManager BLE scanning with service UUID filter
- [ ] `AND-BLE.01b` — Implement BLE pairing flow UI: scan screen, device list, progress indicator
- [ ] `AND-BLE.01c` — Implement WiFi provisioning: GATT write for SSID/password

---

### AND-BLE.02: BLE device management — claim API, home screen status, permissions edge cases
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[AND-android#AND-BLE.01|AND-BLE.01]]
- **Blocks:** [[AND-android#AND-COK.01|AND-COK.01]]

**Acceptance Criteria:**
- [ ] Device claim via API after WiFi connection confirmed
- [ ] Home screen device card with online/offline/cooking status
- [ ] BLE off/location disabled edge cases handled gracefully

**Tasks:**
- [ ] `AND-BLE.02a` — Implement device claim via API after WiFi connection confirmed
- [ ] `AND-BLE.02b` — Implement Home screen with paired device status card
- [ ] `AND-BLE.02c` — Handle runtime permissions and edge cases (BLE off, location disabled)

---

## Phase 3 — Recipe & Cooking (Sprints 9–10)

### AND-RCP.01: Recipe browsing — list, detail, search, favorites
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[AND-android#AND-SET.01|AND-SET.01]], [[BE-backend#BE-RCP.01|BE-RCP.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Recipe list: horizontal card layout with food bowl image on left, name/time/difficulty on right
- [ ] Nutrition per serving on each card: Protein (g), Carbs (g), Fats (g), Calories (kcal)
- [ ] Tag filter chips (horizontally scrollable): All Recipes, Vegan, Healthy, Vegetarian, Protein Rich, Stir Fry, Gluten Free, Quick Recipe
- [ ] Cuisine filter chips (second row): Indian, Italian, American, Chinese, Mexican, Korean, Thai, Asian, Global
- [ ] Recipe detail: full image, ingredient list, step preview, nutrition info
- [ ] Search with debounce
- [ ] Favorites: toggle with local Room DB + cloud sync
- [ ] Pull-to-refresh and pagination
- [ ] "Start Cooking" sends command to device

**Tasks:**
- [ ] `AND-RCP.01a` — Implement recipe list with horizontal card layout (bowl image left, details + nutrition right)
- [ ] `AND-RCP.01b` — Implement tag and cuisine filter chip rows
- [ ] `AND-RCP.01c` — Implement recipe detail screen with expandable sections and nutrition
- [ ] `AND-RCP.01d` — Implement search with debounce
- [ ] `AND-RCP.01e` — Implement favorites with Room persistence and cloud sync
- [ ] `AND-RCP.01f` — Implement "Start Cooking" with device command API

---

### AND-COK.01: Live cooking view — camera stream, status, temperature, timer
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[AND-android#AND-BLE.02|AND-BLE.02]]
- **Blocks:** [[AND-android#AND-COK.02|AND-COK.02]]

**Acceptance Criteria:**
- [ ] Live camera stream via WebSocket rendered in AndroidView or Compose Canvas
- [ ] Cooking status: current state, step, progress bar
- [ ] Temperature gauge: current vs target with animated arc (Canvas animation)
- [ ] Timer: step countdown + total elapsed with foreground service
- [ ] Keep screen on during cooking (FLAG_KEEP_SCREEN_ON)

**Tasks:**
- [ ] `AND-COK.01a` — Implement WebSocket client for camera stream; render frames
- [ ] `AND-COK.01b` — Implement cooking status composable with state and progress
- [ ] `AND-COK.01c` — Implement temperature gauge with Canvas animation
- [ ] `AND-COK.01d` — Implement timer with foreground service for background accuracy

---

### AND-COK.02: Cooking controls and notifications — pause/abort, FCM push, testing
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[AND-android#AND-COK.01|AND-COK.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Controls: Pause/Resume, Abort with AlertDialog confirmation
- [ ] FCM push notifications for cooking events (done, error, attention needed)
- [ ] Tested with live device stream

**Tasks:**
- [ ] `AND-COK.02a` — Implement pause/resume/abort controls
- [ ] `AND-COK.02b` — Implement FCM integration for cooking event notifications
- [ ] `AND-COK.02c` — Test with live device stream

---

## Phase 4 — User Profile (Sprint 11)

### AND-USR.01: User profile — settings, cooking history, preferences
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-USR.01|BE-USR.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Profile: name, email, avatar (photo picker), dietary preferences
- [ ] Cooking history: chronological list with recipe, date, duration, status
- [ ] Preferences: spice level, serving size, cuisines
- [ ] Device management: list, unpair, rename
- [ ] Settings: notifications, units, logout, delete account

**Tasks:**
- [ ] `AND-USR.01a` — Implement profile screen with editable fields and image picker
- [ ] `AND-USR.01b` — Implement cooking history with LazyColumn and recipe navigation
- [ ] `AND-USR.01c` — Implement preferences with DataStore persistence + cloud sync
- [ ] `AND-USR.01d` — Implement device management screen
- [ ] `AND-USR.01e` — Implement settings with notification toggle, units, logout, account deletion

---

### AND-LIVE.01: Glance Widget — Cooking Progress App Widget (Jetpack Glance)
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[AND-android#AND-COK.01|AND-COK.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Glance widget: recipe name, current stage, temperature (current/target), progress bar, time remaining
- [ ] Near real-time updates via WorkManager + foreground service broadcast
- [ ] Pulsing indicator when active; static idle state when no session
- [ ] Widget sizes: small (2x1 — recipe name + time), medium (3x2 — full info)
- [ ] Tapping deep-links to cooking session screen
- [ ] Auto-clears to idle on cooking complete/abort
- [ ] Idle fallback: "No active cooking" with last session summary

**Tasks:**
- [ ] `AND-LIVE.01a` — Create `CookingGlanceWidget` with `GlanceAppWidget` and Compose-style layout
- [ ] `AND-LIVE.01b` — Implement small (2x1) and medium (3x2) widget size variants
- [ ] `AND-LIVE.01c` — Wire `GlanceAppWidgetManager.updateAll()` to cooking foreground service
- [ ] `AND-LIVE.01d` — Implement `GlanceStateDefinition` backed by DataStore for widget state
- [ ] `AND-LIVE.01e` — Implement idle/active/completed widget states

---

## Dependencies

### What AND blocks

None — Android app is a leaf node.

### What blocks AND

| AND Story | Blocked by | Reason |
|-----------|------------|--------|
| AND-SET.01 | BE-SET.01 | Needs backend auth API |
| AND-BLE.01 | AND-SET.01, BE-DEV.01 | Needs networking + device API |
| AND-BLE.02 | AND-BLE.01 | Needs BLE pairing flow |
| AND-RCP.01 | AND-SET.01, BE-RCP.01 | Needs app scaffold + recipe API |
| AND-COK.01 | AND-BLE.02 | Needs paired device |
| AND-COK.02 | AND-COK.01 | Needs live cooking view |
| AND-USR.01 | BE-USR.01 | Needs user API |

---

## References

- [[__Workspaces/Epicura/docs/12-MobileApps/03-Android-App|Android App Details]]
- [[__Workspaces/Epicura/docs/12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]
- [[__Workspaces/Epicura/docs/11-API/04-BLE-Services|BLE Services]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
