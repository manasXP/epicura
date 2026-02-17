---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Mobile Architecture

## Native vs Cross-Platform Decision

Epicura uses native mobile development (Swift/SwiftUI for iOS, Kotlin/Jetpack Compose for Android) instead of the originally considered Flutter approach.

| Criteria | Native (Swift + Kotlin) | Flutter | Decision Factor |
|----------|------------------------|---------|-----------------|
| **BLE Performance** | Direct platform APIs (Core Bluetooth, CompanionDeviceManager) | Plugin-based (`flutter_blue_plus`), limited control | BLE pairing and WiFi provisioning are critical setup flow |
| **Camera Streaming** | Native AVFoundation / CameraX for MJPEG | Plugin-based, frame decoding overhead | Live cooking camera feed requires low-latency rendering |
| **Platform Feel** | 100% native UI, gestures, animations | Custom Skia rendering, approximates native | Indian users expect platform-consistent experience |
| **Background Processing** | Full OS-level support (BGTasks, WorkManager) | Limited plugin support | Cooking notifications must arrive reliably in background |
| **Push Notifications** | Native APNs/FCM integration | Plugin-based | Critical for cooking alerts |
| **App Size** | ~15-25 MB per platform | ~25-40 MB (Dart runtime + Skia engine) | Smaller app size preferred for Indian market (data constraints) |
| **Maintenance** | Two codebases, platform expertise needed | Single codebase, Dart expertise | Acceptable trade-off for better BLE and camera support |
| **Long-term** | Apple/Google invest directly in platform SDKs | Flutter updates may lag platform features | Guaranteed compatibility with new OS versions |

**Decision:** Native development provides superior BLE integration, camera streaming performance, and platform-native user experience — all critical for Epicura's core flows.

---

## MVVM Architecture

Both iOS and Android apps use the MVVM (Model-View-ViewModel) pattern with a shared architectural philosophy:

```
┌───────────────────────────────────────────────────────────────────┐
│                        Mobile App                                 │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                      View Layer                            │   │
│  │  SwiftUI Views (iOS) / Composable Functions (Android)      │   │
│  │  Observes ViewModel state, dispatches user actions         │   │
│  └────────────────────────────┬───────────────────────────────┘   │
│                               │                                   │
│  ┌────────────────────────────▼───────────────────────────────┐   │
│  │                    ViewModel Layer                         │   │
│  │  Holds UI state, processes user actions                    │   │
│  │  Transforms data models into display models                │   │
│  │  iOS: @Observable classes + Combine                        │   │
│  │  Android: ViewModel + StateFlow + Kotlin coroutines        │   │
│  └────────────────────────────┬───────────────────────────────┘   │
│                               │                                   │
│  ┌────────────────────────────▼───────────────────────────────┐   │
│  │                    Repository Layer                        │   │
│  │  Coordinates data sources, caching strategy                │   │
│  │  Single source of truth for each data type                 │   │
│  └──────────┬───────────────────────────┬─────────────────────┘   │
│             │                           │                         │
│  ┌──────────▼──────────┐    ┌───────────▼────────────┐            │
│  │   Remote Sources    │    │    Local Sources       │            │
│  │  ┌───────────────┐  │    │  ┌─────────────────┐   │            │
│  │  │ API Client    │  │    │  │ SwiftData/Room  │   │            │
│  │  │ (REST + JWT)  │  │    │  │ (local cache)   │   │            │
│  │  ├───────────────┤  │    │  ├─────────────────┤   │            │
│  │  │ WebSocket     │  │    │  │ Keychain /      │   │            │
│  │  │ (real-time)   │  │    │  │ DataStore       │   │            │
│  │  ├───────────────┤  │    │  │ (secure store)  │   │            │
│  │  │ BLE Manager   │  │    │  └─────────────────┘   │            │
│  │  │ (pairing)     │  │    │                        │            │
│  │  └───────────────┘  │    └────────────────────────┘            │
│  └─────────────────────┘                                          │
└───────────────────────────────────────────────────────────────────┘
```

---

## Feature Priority Matrix

| Priority | Feature | iOS | Android |
|----------|---------|-----|---------|
| **P0** | BLE pairing + WiFi provisioning | Core Bluetooth | CompanionDeviceManager |
| **P0** | User auth (phone+OTP primary, email fallback) | URLSession | Retrofit/OkHttp |
| **P0** | Recipe browsing + detail view | SwiftUI List/Grid | LazyColumn/LazyGrid |
| **P0** | Live cooking progress (WebSocket) | URLSessionWebSocketTask | OkHttp WebSocket |
| **P0** | Push notifications | APNs | FCM |
| **P1** | MJPEG camera stream | AVFoundation | MediaCodec |
| **P1** | Cooking history + ratings | SwiftData | Room |
| **P1** | User preferences + allergen profile | SwiftData | DataStore + Room |
| **P1** | Offline recipe cache | SwiftData | Room |
| **P1** | Appliance management (rename, status) | REST API | REST API |
| **P2** | Recipe search (full-text) | REST API | REST API |
| **P2** | Grocery list generation | Computed from recipes | Computed from recipes |
| **P2** | Meal planning / scheduling | REST API + local | REST API + local |
| **P2** | Dark mode | System setting | Material 3 dynamic |
| **P2** | Multi-language (Hindi, Tamil, etc.) | String Catalogs | string resources |

---

## Networking Layer

### API Client

Both platforms implement a type-safe API client wrapping the [[../11-API/01-REST-API-Reference|REST API]]:

```
┌─────────────────────────────────────────────────────┐
│                  API Client                         │
│                                                     │
│  Base URL: https://api.epicura.io/api/v1            │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  Request Pipeline:                           │   │
│  │  1. Build request (URL, method, body)        │   │
│  │  2. Attach JWT access token                  │   │
│  │  3. Send request                             │   │
│  │  4. If 401 → refresh token → retry           │   │
│  │  5. Decode response (JSON → model)           │   │
│  │  6. Return Result<T, APIError>               │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │  Token Management:                            │  │
│  │  - Store access + refresh tokens securely     │  │
│  │  - Auto-refresh on 401 response               │  │
│  │  - Refresh token rotation                     │  │
│  │  - Queue concurrent requests during refresh   │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### WebSocket Client

Real-time cooking updates via WebSocket (see [[../11-API/02-WebSocket-Events|WebSocket Events]]):

```
┌─────────────────────────────────────────────────────┐
│              WebSocket Manager                      │
│                                                     │
│  States:                                            │
│  ┌──────────┐  connect  ┌────────────┐              │
│  │Disconnect│──────────►│ Connecting │              │
│  │   ed     │           └─────┬──────┘              │
│  └────▲─────┘                 │                     │
│       │              success  │  failure            │
│       │           ┌───────────┘  │                  │
│       │           ▼              ▼                  │
│       │    ┌────────────┐  ┌──────────┐             │
│       │    │ Connected  │  │ Retrying │             │
│       │    │            │  │ (backoff)│             │
│       │    └─────┬──────┘  └────┬─────┘             │
│       │          │              │                   │
│       │     disconnect    retry │                   │
│       └──────────┘              │                   │
│       └─────────────────────────┘                   │
│                                                     │
│  Features:                                          │
│  - Auto-reconnect with exponential backoff          │
│  - Re-subscribe to appliances on reconnect          │
│  - Ping/pong heartbeat (30s interval)               │
│  - Parse events → dispatch to ViewModel observers   │
└─────────────────────────────────────────────────────┘
```

### BLE Manager

BLE state machine for device pairing (see [[../11-API/04-BLE-Services|BLE Services]]):

```
┌─────────────────────────────────────────────────────┐
│                BLE Manager                          │
│                                                     │
│  ┌──────┐  scan   ┌──────────┐  found  ┌────────┐   │
│  │ Idle │────────►│ Scanning │────────►│Connect-│   │
│  │      │         │          │         │  ing   │   │
│  └──▲───┘         └──────────┘         └────┬───┘   │
│     │                                       │       │
│     │              ┌─────────┐    connected │       │
│     │  disconnect  │Discover-│◄─────────────┘       │
│     │◄─────────────│  ing    │                      │
│     │              │Services │                      │
│     │              └────┬────┘                      │
│     │                   │ services discovered       │
│     │              ┌────▼────┐                      │
│     │              │ Ready   │                      │
│     │              │ (read/  │                      │
│     │              │  write) │                      │
│     │              └────┬────┘                      │
│     │                   │ provisioning complete     │
│     │              ┌────▼────┐                      │
│     └──────────────│  Done   │                      │
│                    └─────────┘                      │
└─────────────────────────────────────────────────────┘
```

---

## MJPEG Camera Streaming

The CM5 serves a live MJPEG stream during cooking at `http://<device-ip>:8080/camera/stream`. The mobile app renders this as a live video feed.

**Implementation Approach:**

| Platform | Method | Notes |
|----------|--------|-------|
| iOS | `URLSession` data task → parse JPEG boundaries → display in `Image` | Use `AsyncStream` to yield frames |
| Android | `OkHttp` streaming response → parse JPEG boundaries → display in `Composable Image` | Use `Flow<Bitmap>` to emit frames |

**MJPEG Frame Parsing:**

```
Content-Type: multipart/x-mixed-replace; boundary=frame

--frame
Content-Type: image/jpeg
Content-Length: 12345

<JPEG bytes>
--frame
Content-Type: image/jpeg
...
```

Target: 10-15 fps at 640x480 resolution.

---

## Offline Strategy

| Data | Cache Strategy | Sync Direction |
|------|---------------|----------------|
| **Recipes** | Cache all published recipes in local DB | Cloud → Device |
| **Cooking History** | Store locally, upload to cloud | Device → Cloud |
| **User Preferences** | Store locally, sync on change | Bidirectional |
| **Recipe Images** | Disk cache with LRU eviction | Cloud → Device |
| **Push Tokens** | Register/refresh on app launch | Device → Cloud |

**Offline Behavior:**

- User can browse cached recipes without internet
- Cannot start remote cooking (requires cloud relay)
- Can start cooking via direct WiFi connection to Epicura device
- Cooking history queued for upload when connection restored
- Preference changes queued and synced on reconnect

---

## Design System

### Epicura Color Palette

| Color | Name | Hex | Usage |
|-------|------|-----|-------|
| Primary | Warm Orange | `#E65100` | CTAs, navigation highlights |
| Primary Variant | Deep Orange | `#BF360C` | Status bar, pressed states |
| Secondary | Forest Green | `#2E7D32` | Success states, positive indicators |
| Background | Cream White | `#FFF8E1` | Main background |
| Surface | White | `#FFFFFF` | Cards, sheets, dialogs |
| Text Primary | Dark Brown | `#3E2723` | Body text, headings |
| Text Secondary | Medium Brown | `#6D4C41` | Captions, labels |
| Emergency | Bright Red | `#D50000` | Emergency stop, critical errors |
| Success | Green | `#43A047` | Cooking complete, success states |
| Warning | Amber | `#FFB300` | Warnings, caution states |

This palette matches the Kivy touchscreen UI colors defined in [[../04-UserInterface/03-UI-UX-Design#Styling|UI/UX Design - Styling]].

### Platform-Native Patterns

| Pattern | iOS (SwiftUI) | Android (Compose) |
|---------|--------------|-------------------|
| Navigation | `NavigationStack` + `NavigationLink` | `NavHost` + `NavController` |
| Tab Bar | `TabView` (Recipe, Favourite, Session, Profile) | `NavigationBar` (Material 3) (Recipe, Favourite, Session, Profile) |
| Pull to Refresh | `.refreshable` modifier | `PullToRefreshBox` |
| Haptics | `UIImpactFeedbackGenerator` | `HapticFeedback` compose |
| System Theme | `@Environment(\.colorScheme)` | `isSystemInDarkTheme()` |
| Typography | SF Pro (system) | Roboto / Material 3 type scale |

---

## Related Documentation

- [[02-iOS-App|iOS App]] - SwiftUI implementation details
- [[03-Android-App|Android App]] - Jetpack Compose implementation details
- [[../11-API/01-REST-API-Reference|REST API Reference]] - Backend endpoints
- [[../11-API/02-WebSocket-Events|WebSocket Events]] - Real-time event protocol
- [[../11-API/04-BLE-Services|BLE Services]] - BLE pairing services
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]] - Design language and color palette
- [[../03-Software/08-Tech-Stack|Tech Stack]] - Overall technology choices

#epicura #mobile #architecture #mvvm #ios #android #swift #kotlin #native-mobile

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
