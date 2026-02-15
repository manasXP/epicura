---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# iOS App

## Platform Requirements

| Requirement | Value |
|-------------|-------|
| **Language** | Swift 5.9+ |
| **UI Framework** | SwiftUI |
| **Minimum iOS** | iOS 17.0 |
| **Architecture** | MVVM + Combine / async-await |
| **IDE** | Xcode 16+ |
| **Package Manager** | Swift Package Manager (SPM) |

---

## Project Structure

```
EpicuraApp/
├── App/
│   ├── EpicuraApp.swift                 @main entry point
│   ├── AppDelegate.swift                Push notification setup
│   └── ContentView.swift                Root TabView
│
├── Core/
│   ├── Network/
│   │   ├── APIClient.swift              Fastify REST API client (URLSession)
│   │   ├── APIEndpoints.swift           Endpoint definitions
│   │   ├── APIError.swift               Error types and handling
│   │   ├── AuthInterceptor.swift        JWT attach + 401 refresh logic
│   │   ├── WebSocketManager.swift       WebSocket connection + event parsing
│   │   └── MJPEGStreamView.swift        MJPEG frame parser + SwiftUI view
│   │
│   ├── BLE/
│   │   ├── BLEManager.swift             Core Bluetooth central manager
│   │   ├── BLEDeviceScanner.swift       Scan + filter Epicura peripherals
│   │   ├── BLEPairingService.swift      Pairing flow orchestration
│   │   ├── WiFiProvisioningService.swift Write SSID/password, monitor status
│   │   └── BLEConstants.swift           Service/characteristic UUIDs
│   │
│   ├── Auth/
│   │   ├── AuthManager.swift            Login, register, token lifecycle
│   │   ├── KeychainService.swift        Secure token storage
│   │   └── AuthState.swift              Observable auth state
│   │
│   └── Storage/
│       ├── PersistenceController.swift  SwiftData container setup
│       ├── CachedRecipe.swift           SwiftData model for offline recipes
│       ├── CookingHistoryItem.swift     SwiftData model for session history
│       └── ImageCache.swift             Disk-based recipe image cache
│
├── Features/
│   ├── Auth/
│   │   ├── LoginView.swift
│   │   ├── RegisterView.swift
│   │   └── AuthViewModel.swift
│   │
│   ├── Recipes/
│   │   ├── RecipeListView.swift         Grid/list of recipes with filters
│   │   ├── RecipeDetailView.swift       Full recipe with ingredients + stages
│   │   ├── RecipeSearchBar.swift        Search + category filter chips
│   │   └── RecipesViewModel.swift
│   │
│   ├── Cooking/
│   │   ├── CookingProgressView.swift    Live status, camera, gauges
│   │   ├── CookingControlsView.swift    Start, pause, stop buttons
│   │   ├── TemperatureGauge.swift       Circular temp display
│   │   ├── StageProgressBar.swift       Stage-by-stage progress
│   │   └── CookingViewModel.swift
│   │
│   ├── Pairing/
│   │   ├── PairingFlowView.swift        Step-by-step BLE pairing
│   │   ├── DeviceScanView.swift         BLE device discovery list
│   │   ├── WiFiSetupView.swift          SSID/password entry
│   │   ├── PairingCompleteView.swift    Success confirmation
│   │   └── PairingViewModel.swift
│   │
│   ├── History/
│   │   ├── HistoryListView.swift        Past cooking sessions
│   │   ├── HistoryDetailView.swift      Session details + stage log
│   │   └── HistoryViewModel.swift
│   │
│   └── Settings/
│       ├── SettingsView.swift           Preferences, allergens, devices
│       ├── ApplianceListView.swift      Paired devices management
│       ├── ProfileView.swift            User profile editing
│       └── SettingsViewModel.swift
│
├── DesignSystem/
│   ├── EpicuraTheme.swift               Colors, typography, spacing
│   ├── EpicuraColors.swift              Brand color definitions
│   ├── Components/
│   │   ├── RecipeCard.swift             Reusable recipe card component
│   │   ├── StatusBadge.swift            Device/cooking status badge
│   │   ├── EpicuraButton.swift          Styled button variants
│   │   └── LoadingView.swift            Skeleton + spinner states
│   └── Modifiers/
│       └── CardStyle.swift              Card shadow + corner radius
│
├── Resources/
│   ├── Assets.xcassets                  App icon, images, colors
│   ├── Localizable.xcstrings            String catalogs (en, hi, ta, te)
│   └── Info.plist
│
└── Tests/
    ├── UnitTests/
    │   ├── APIClientTests.swift
    │   ├── AuthManagerTests.swift
    │   ├── BLEManagerTests.swift
    │   └── RecipesViewModelTests.swift
    └── UITests/
        ├── PairingFlowUITests.swift
        └── RecipeBrowsingUITests.swift
```

---

## Frameworks & Libraries

| Framework / Library | Source | Purpose |
|--------------------|--------|---------|
| **SwiftUI** | Apple | Declarative UI framework |
| **Combine** | Apple | Reactive streams, publisher/subscriber |
| **Core Bluetooth** | Apple | BLE scanning, connection, GATT operations |
| **AVFoundation** | Apple | MJPEG camera stream decoding |
| **SwiftData** | Apple | Local persistence (recipes, history, preferences) |
| **Network** (NWBrowser) | Apple | mDNS/Bonjour discovery of Epicura device on LAN |
| **UserNotifications** | Apple | Local + remote push notification handling |
| **Security** (Keychain) | Apple | Secure JWT token storage |
| **CryptoKit** | Apple | AES-128 encryption for BLE WiFi password |
| **Swift Concurrency** | Apple | async/await, Task, AsyncStream |
| **Nuke** | SPM | Efficient image loading and caching (recipe photos) |

---

## BLE Implementation Notes

### Core Bluetooth Setup

```swift
class BLEManager: NSObject, ObservableObject, CBCentralManagerDelegate {
    @Published var state: BLEState = .idle
    @Published var discoveredDevices: [EpicuraDevice] = []

    private var centralManager: CBCentralManager!

    override init() {
        super.init()
        centralManager = CBCentralManager(delegate: self, queue: .main)
    }

    func startScanning() {
        guard centralManager.state == .poweredOn else { return }
        centralManager.scanForPeripherals(
            withServices: [BLEConstants.wifiProvisioningServiceUUID],
            options: [CBCentralManagerScanOptionAllowDuplicatesKey: false]
        )
        state = .scanning
    }
}
```

### Key Considerations

- **State Restoration:** Implement `willRestoreState` for background BLE sessions during pairing
- **Permission Flow:** Request Bluetooth permission on pairing screen, not on app launch
- **Error Handling:** Handle `CBManagerState.unauthorized`, `.poweredOff`, `.unsupported` gracefully
- **Timeout:** Set 30-second scan timeout, 10-second connection timeout
- **Cleanup:** Disconnect peripheral and stop scanning when pairing view disappears

---

## Push Notifications (APNs)

### Setup

```swift
// AppDelegate.swift
func application(_ application: UIApplication,
                 didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    // Register with backend: POST /push/register { platform: "ios", token: token }
    Task {
        try await apiClient.registerPushToken(platform: "ios", token: token)
    }
}
```

### Notification Types

| Notification | Trigger | Action |
|-------------|---------|--------|
| Cooking Complete | `cooking:complete` event | Deep link to session detail |
| Cooking Error | `cooking:error` event | Deep link to appliance status |
| Firmware Update | New firmware release | Deep link to settings |
| New Recipes | Admin broadcast | Deep link to recipe list |

---

## Accessibility

### VoiceOver

- All interactive elements have `.accessibilityLabel` and `.accessibilityHint`
- Recipe cards: `"Dal Tadka. Easy difficulty. 35 minutes. Double-tap to view recipe."`
- Temperature gauge: `"Temperature 148 degrees Celsius. Target 150 degrees."`
- Cooking progress: `"Stage 3 of 6. Saute Onions. 42 percent complete."`
- Emergency stop button: `.accessibilityLabel("Emergency stop")` with `.accessibilityAddTraits(.isButton)`

### Dynamic Type

- All text uses SwiftUI semantic font styles (`.title`, `.body`, `.caption`)
- Custom font sizes defined relative to Dynamic Type categories
- Layouts tested from `xSmall` to `AX5` (accessibility extra-extra-extra-extra-extra-large)
- Temperature and time displays use `.font(.system(size: 36, design: .rounded))` with `@ScaledMetric`

---

## Testing

### Unit Tests (XCTest)

| Test Suite | Scope |
|-----------|-------|
| `APIClientTests` | Request building, JWT attachment, error parsing, token refresh |
| `AuthManagerTests` | Login, register, token storage, logout |
| `BLEManagerTests` | Mock CBCentralManager, scanning, connection state machine |
| `RecipesViewModelTests` | Recipe list loading, filtering, search, offline cache |
| `CookingViewModelTests` | WebSocket event handling, state transitions |
| `PairingViewModelTests` | BLE pairing flow, WiFi provisioning |

### UI Tests (XCUITest)

| Test | Flow |
|------|------|
| `PairingFlowUITests` | Launch → Pairing → Scan → Connect → WiFi → Done |
| `RecipeBrowsingUITests` | Tab → Browse → Filter → Detail → Start Cook |
| `CookingProgressUITests` | Start cook → Progress updates → Complete → Rate |
| `SettingsUITests` | Settings → Change preferences → Save → Verify |

### Testing Tools

| Tool | Purpose |
|------|---------|
| XCTest | Unit and integration testing |
| XCUITest | UI automation testing |
| Swift Testing | Modern test framework (Swift 5.9+) |
| Preview Providers | SwiftUI preview testing during development |

---

## Related Documentation

- [[01-Mobile-Architecture|Mobile Architecture]] - Shared architecture and design system
- [[03-Android-App|Android App]] - Android counterpart
- [[../11-API/01-REST-API-Reference|REST API Reference]] - Backend API
- [[../11-API/02-WebSocket-Events|WebSocket Events]] - Real-time events
- [[../11-API/04-BLE-Services|BLE Services]] - BLE GATT services and pairing flow
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]] - Design language

#epicura #ios #swift #swiftui #mobile #core-bluetooth #native-mobile

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
