---
tags: [epicura, project-management, epic, android, kotlin, compose]
created: 2026-02-16
aliases: [AND Epic, Android Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 5 stories across Sprints 8–12 |

# Epic: AND — Android App (Kotlin/Compose)

Native Android companion app mirroring iOS functionality: BLE device pairing, WiFi provisioning, recipe browsing, live cooking view, and user profile. Built with Kotlin, Jetpack Compose, MVVM, Hilt DI.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SET — Project Setup | 1 | 5 | 8 |
| BLE — BLE Pairing | 1 | 8 | 8 |
| RCP — Recipe Browsing | 1 | 5 | 9 |
| COK — Live Cooking | 1 | 8 | 10 |
| USR — User Profile | 1 | 5 | 11 |
| **Total** | **5** | **~30** | |

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
- [ ] Bottom navigation: Home, Recipes, Cook, Profile
- [ ] ktlint configured; CI pipeline runs lint + build + test

**Tasks:**
- [ ] `AND-SET.01a` — Create Gradle project; configure Compose, Hilt, Retrofit, Navigation Compose
- [ ] `AND-SET.01b` — Create networking layer: Retrofit client, JWT interceptor, token storage (EncryptedSharedPreferences)
- [ ] `AND-SET.01c` — Implement auth flow: login, register, token persistence, auto-login
- [ ] `AND-SET.01d` — Create bottom navigation with NavHost and 4 tabs
- [ ] `AND-SET.01e` — Configure ktlint; create GitHub Actions CI workflow

---

### AND-BLE.01: BLE pairing — CompanionDeviceManager, WiFi provisioning
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 8
- **Blocked by:** [[AND-android#AND-SET.01|AND-SET.01]], [[BE-backend#BE-DEV.01|BE-DEV.01]]
- **Blocks:** [[AND-android#AND-COK.01|AND-COK.01]]

**Acceptance Criteria:**
- [ ] CompanionDeviceManager discovers Epicura devices by service UUID
- [ ] Pairing flow: scan → select → connect → send WiFi credentials → verify
- [ ] WiFi SSID/password sent via BLE GATT characteristic write
- [ ] Device confirms WiFi and registers with cloud; app claims device
- [ ] Paired device shown on Home with online/offline/cooking status
- [ ] Runtime permissions handled: Bluetooth, Location (for BLE scan on older APIs)

**Tasks:**
- [ ] `AND-BLE.01a` — Implement CompanionDeviceManager BLE scanning with service UUID filter
- [ ] `AND-BLE.01b` — Implement BLE pairing flow UI: scan screen, device list, progress indicator
- [ ] `AND-BLE.01c` — Implement WiFi provisioning: GATT write for SSID/password
- [ ] `AND-BLE.01d` — Implement device claim via API after WiFi connection confirmed
- [ ] `AND-BLE.01e` — Implement Home screen with paired device status card
- [ ] `AND-BLE.01f` — Handle runtime permissions and edge cases (BLE off, location disabled)

---

## Phase 3 — Recipe & Cooking (Sprints 9–10)

### AND-RCP.01: Recipe browsing — list, detail, search, favorites
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[AND-android#AND-SET.01|AND-SET.01]], [[BE-backend#BE-RCP.01|BE-RCP.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Recipe list: LazyVerticalGrid with Coil async image, name, time, difficulty
- [ ] Recipe detail: full image, ingredient list, step preview
- [ ] Search with debounce, filter chips (cuisine, difficulty, time range)
- [ ] Favorites: toggle with local Room DB + cloud sync
- [ ] Pull-to-refresh and pagination
- [ ] "Start Cooking" sends command to device

**Tasks:**
- [ ] `AND-RCP.01a` — Implement recipe list with LazyVerticalGrid and Coil image loading
- [ ] `AND-RCP.01b` — Implement recipe detail screen with expandable sections
- [ ] `AND-RCP.01c` — Implement search with debounce and filter composables
- [ ] `AND-RCP.01d` — Implement favorites with Room persistence and cloud sync
- [ ] `AND-RCP.01e` — Implement "Start Cooking" with device command API

---

### AND-COK.01: Live cooking view — camera stream, status, controls
- **Sprint:** [[sprint-10|Sprint 10]]
- **Priority:** P0
- **Points:** 8
- **Blocked by:** [[AND-android#AND-BLE.01|AND-BLE.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Live camera stream via WebSocket rendered in AndroidView or Compose Canvas
- [ ] Cooking status: current state, step, progress bar
- [ ] Temperature gauge: current vs target with animated arc
- [ ] Timer: step countdown + total elapsed
- [ ] Controls: Pause/Resume, Abort with AlertDialog confirmation
- [ ] FCM push notifications for cooking events
- [ ] Keep screen on during cooking (FLAG_KEEP_SCREEN_ON)

**Tasks:**
- [ ] `AND-COK.01a` — Implement WebSocket client for camera stream; render frames
- [ ] `AND-COK.01b` — Implement cooking status composable with state and progress
- [ ] `AND-COK.01c` — Implement temperature gauge with Canvas animation
- [ ] `AND-COK.01d` — Implement timer with foreground service for background accuracy
- [ ] `AND-COK.01e` — Implement pause/resume/abort controls
- [ ] `AND-COK.01f` — Implement FCM integration for cooking event notifications
- [ ] `AND-COK.01g` — Test with live device stream

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

## Dependencies

### What AND blocks

None — Android app is a leaf node.

### What blocks AND

| AND Story | Blocked by | Reason |
|-----------|------------|--------|
| AND-SET.01 | BE-SET.01 | Needs backend auth API |
| AND-BLE.01 | AND-SET.01, BE-DEV.01 | Needs networking + device API |
| AND-RCP.01 | AND-SET.01, BE-RCP.01 | Needs app scaffold + recipe API |
| AND-COK.01 | AND-BLE.01 | Needs paired device |
| AND-USR.01 | BE-USR.01 | Needs user API |

---

## References

- [[__Workspaces/Epicura/docs/12-MobileApps/03-Android-App|Android App Details]]
- [[__Workspaces/Epicura/docs/12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]
- [[__Workspaces/Epicura/docs/11-API/04-BLE-Services|BLE Services]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
