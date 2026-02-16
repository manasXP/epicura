---
tags: [epicura, testing, ios, swift, swiftui]
created: 2026-02-16
aliases: [iOS Test Strategy]
---

# iOS Test Strategy — epicura-ios

## Scope

Testing strategy for the iOS companion app: authentication, BLE pairing/WiFi provisioning, recipe browsing, live cooking view, and user profile.

---

## Test Levels

### 1. Unit Tests

**Framework:** XCTest + Swift Testing
**Runs on:** macOS (Xcode, CI-compatible)

| Module | Key Test Cases |
|--------|---------------|
| `APIClient` | JWT attachment on requests, 401 triggers token refresh, network error handling, response decoding for all model types |
| `BLEManager` | State machine transitions (scanning→discovered→connecting→connected→provisioning), timeout handling, disconnect recovery, WiFi credential transfer protocol |
| `WebSocketClient` | Connection lifecycle, frame parsing, reconnect on disconnect, heartbeat timeout |
| `KeychainService` | Store/retrieve/delete tokens, handle Keychain errors gracefully |
| **Auth ViewModels** | Login validation (email format, password length), register field validation, error state handling, loading state management |
| **Recipe ViewModels** | Recipe list filtering/sorting, search debounce, favorite toggle (optimistic update + rollback), pagination |
| **Cooking ViewModel** | Cook state transitions (idle→preheating→cooking→done), timer countdown, temperature display formatting, alert handling |
| **Models** | Codable encode/decode for all API response types, edge cases (null fields, empty arrays) |

**Approach:**
- ViewModels tested in isolation with mock services (protocol-based DI)
- `APIClient` tested with `URLProtocol` mock (no network)
- `BLEManager` tested with `CBCentralManager` mock via protocol abstraction
- All async code tested with `async/await` + `XCTestExpectation` or Swift Testing `#expect`

### 2. Integration Tests

**Framework:** XCTest
**Runs on:** Simulator + local API server

| Test Area | Setup | Verification |
|-----------|-------|-------------|
| Auth flow | Mock API server (Vapor test server or WireMock) | Register → login → token stored → refresh → logout → token cleared |
| Recipe browsing | Mock API with seeded recipes | List loads, search filters, detail view renders, favorite persists |
| Cooking flow | Mock API + mock WebSocket server | Start cook → receive status updates → display progress → complete |
| Offline mode | Disconnect network mid-operation | Cached recipes accessible, queued actions sync on reconnect |

### 3. UI Tests

**Framework:** XCUITest
**Runs on:** iOS Simulator (CI via `xcodebuild test`)

| Test | Steps | Verification |
|------|-------|-------------|
| Login flow | Launch → enter credentials → tap login | Home screen appears, tab bar visible |
| Recipe browse | Navigate to recipes → scroll → tap recipe | Detail view shows correct recipe data |
| BLE pairing (mock) | Navigate to device setup → tap scan | Scanning UI appears, mock device listed |
| Settings | Navigate to profile → change preference → save | Preference persists after app restart |
| Accessibility | VoiceOver pass on all screens | All interactive elements labeled, correct traits |

### 4. Performance Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| App launch time | XCTest `measure` block | Cold launch < 2s on iPhone 13 |
| Recipe list scroll | FPS monitoring during fast scroll | Sustained 60 FPS, no dropped frames |
| Memory usage | Instruments Allocations | < 150 MB during cooking view with camera feed |
| Network payload | Charles Proxy | Recipe list response < 50 KB, images lazy-loaded |
| Battery impact | Instruments Energy Log during 30-min cook | No excessive CPU/network wake-ups |

### 5. Security Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Keychain storage | Inspect Keychain with `security` CLI on debug build | Tokens stored with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` |
| Certificate pinning | Proxy with self-signed cert | API calls fail (pinning enforced) |
| Jailbreak detection | Test on jailbroken simulator config | Warning displayed, sensitive features restricted |
| Data at rest | Inspect app sandbox | No tokens or PII in UserDefaults or plain files |

---

## CI Pipeline

```yaml
# .github/workflows/ci.yml
trigger: PR to develop or main

steps:
  1. Checkout
  2. Select Xcode 16
  3. Run SwiftLint
  4. Build (xcodebuild build, iPhone 16 simulator)
  5. Run unit tests (xcodebuild test)
  6. Run UI tests (xcodebuild test, XCUITest scheme)
  7. Report coverage (xcresult → lcov)
```

**Gate criteria:** SwiftLint clean, build succeeds, all unit + UI tests pass, coverage ≥ 70%.

---

## Test Fixtures

- **Mock API responses:** JSON files for all endpoints (recipes, user, device, auth)
- **Mock BLE peripherals:** `CBPeripheralMock` conforming to protocol, simulates discovery + connection
- **Sample images:** Recipe thumbnails for UI snapshot tests
- **Test accounts:** Predefined users with various roles (admin, standard, new user)

---

## References

- [[__Workspaces/Epicura/docs/07-Development/02-Repository-Plan|Repository Plan]]
- [[__Workspaces/Epicura/docs/12-MobileApps/02-iOS-App|iOS App]]
- [[__Workspaces/Epicura/docs/12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]
- [[__Workspaces/Epicura/docs/11-API/04-BLE-Services|BLE Services]]
