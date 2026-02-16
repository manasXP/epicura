---
tags: [epicura, testing, android, kotlin, compose]
created: 2026-02-16
aliases: [Android Test Strategy]
---

# Android Test Strategy — epicura-android

## Scope

Testing strategy for the Android companion app: authentication, BLE pairing/WiFi provisioning, recipe browsing, live cooking view, and user profile.

---

## Test Levels

### 1. Unit Tests

**Framework:** JUnit 5 + Mockk + Turbine (for Flow testing)
**Runs on:** JVM (no emulator required)

| Module | Key Test Cases |
|--------|---------------|
| `api/` (Retrofit) | Request construction, response deserialization, error mapping (4xx/5xx), JWT interceptor attaches token, 401 triggers refresh |
| `repository/` | Repository methods call correct API + cache to Room, offline fallback returns cached data, sync conflict resolution |
| `local/` (Room) | DAO queries return correct results, migration tests for schema changes, data integrity after insert/update/delete |
| **Auth ViewModels** | Login validation, register validation, error/loading state emissions via StateFlow, navigation events |
| **Recipe ViewModels** | List filtering, search debounce (Turbine), favorite toggle with optimistic update, pagination via Paging 3 |
| **Cooking ViewModel** | State transitions, timer countdown, temperature formatting, WebSocket event handling |
| **BLE ViewModel** | Scan state machine, CompanionDeviceManager flow, WiFi provisioning protocol, timeout handling |
| `di/` (Hilt) | Hilt modules provide correct dependencies (compile-time verified) |

**Approach:**
- ViewModels tested with `TestDispatcher` for coroutine control
- Flows tested with Turbine for emission assertions
- Retrofit tested with MockWebServer (OkHttp)
- Room tested with in-memory database (`Room.inMemoryDatabaseBuilder`)
- All external dependencies injected via Hilt, replaced with fakes in tests

### 2. Integration Tests

**Framework:** JUnit 5 + Hilt testing + MockWebServer
**Runs on:** JVM or emulator

| Test Area | Setup | Verification |
|-----------|-------|-------------|
| Auth flow | MockWebServer with auth responses | Register → login → token stored → refresh → logout → token cleared |
| Recipe data layer | MockWebServer + in-memory Room | API fetch → Room cache → offline read returns cached |
| Cooking flow | MockWebServer + mock WebSocket | Start cook → receive updates → ViewModel emits correct states |
| Network error handling | MockWebServer returns 500/timeout | UI shows error state, retry works |

### 3. UI Tests

**Framework:** Compose UI Test (AndroidX)
**Runs on:** Emulator (CI via Gradle managed devices)

| Test | Steps | Verification |
|------|-------|-------------|
| Login flow | Launch → enter credentials → tap login | Home screen composable displayed |
| Recipe browse | Navigate to recipes → scroll LazyColumn → tap recipe | Detail screen shows correct data, back navigation works |
| BLE pairing (mock) | Navigate to device setup → tap scan | Scanning UI appears, CompanionDeviceManager dialog shown |
| Settings | Navigate to profile → toggle preference → restart | Preference persists (DataStore) |
| Accessibility | TalkBack pass, `assertHasContentDescription` | All interactive elements have content descriptions |

### 4. Performance Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| App startup | Macrobenchmark `StartupBenchmark` | Cold start < 1.5s on Pixel 7 |
| Recipe list scroll | Macrobenchmark `ScrollBenchmark` | p95 frame time < 16ms (60 FPS) |
| Memory usage | Android Profiler during cooking view | < 200 MB RSS |
| APK size | `bundletool size` | < 15 MB download size |
| Battery impact | Battery Historian during 30-min cook | No excessive wakelocks |

### 5. Security Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Token storage | Inspect EncryptedSharedPreferences | Tokens encrypted at rest via AndroidKeyStore |
| Certificate pinning | Proxy with self-signed cert | OkHttp `CertificatePinner` rejects connection |
| Root detection | Test on rooted emulator | Warning displayed, sensitive features restricted |
| ProGuard/R8 | Decompile release APK | No plain-text API keys or tokens visible |
| Exported components | `aapt dump` manifest analysis | No unintentionally exported activities/receivers |

---

## CI Pipeline

```yaml
# .github/workflows/ci.yml
trigger: PR to develop or main

steps:
  1. Checkout
  2. Set up JDK 17 + Gradle cache
  3. Run ktlint
  4. Build debug APK (./gradlew assembleDebug)
  5. Run unit tests (./gradlew testDebugUnitTest)
  6. Run Compose UI tests (Gradle managed device, API 34)
  7. Report coverage (JaCoCo)
```

**Gate criteria:** ktlint clean, build succeeds, all unit + UI tests pass, coverage ≥ 70%.

---

## Test Fixtures

- **MockWebServer responses:** JSON files for all API endpoints
- **Room test database:** Pre-populated with recipes, user data for DAO tests
- **Compose test tags:** All interactive composables tagged with `testTag` for UI test targeting
- **BLE mock:** Fake `CompanionDeviceManager` responses for pairing flow
- **Sample images:** Drawable resources for recipe thumbnail rendering tests

---

## References

- [[__Workspaces/Epicura/docs/07-Development/02-Repository-Plan|Repository Plan]]
- [[__Workspaces/Epicura/docs/12-MobileApps/03-Android-App|Android App]]
- [[__Workspaces/Epicura/docs/12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]
- [[__Workspaces/Epicura/docs/11-API/04-BLE-Services|BLE Services]]
