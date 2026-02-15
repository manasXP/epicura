---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Android App

## Platform Requirements

| Requirement | Value |
|-------------|-------|
| **Language** | Kotlin 1.9+ |
| **UI Framework** | Jetpack Compose + Material 3 |
| **Min SDK** | API 26 (Android 8.0 Oreo) |
| **Target SDK** | API 35 (Android 15) |
| **Architecture** | MVVM + Kotlin coroutines / Flow |
| **IDE** | Android Studio Ladybug+ |
| **Build System** | Gradle (Kotlin DSL) |

---

## Project Structure

```
app/src/main/java/io/epicura/app/
├── EpicuraApplication.kt                Hilt application class
├── MainActivity.kt                      Single-activity, Compose host
│
├── core/
│   ├── network/
│   │   ├── ApiClient.kt                 Retrofit/Ktor REST client
│   │   ├── ApiEndpoints.kt              Endpoint interface definitions
│   │   ├── AuthInterceptor.kt           OkHttp interceptor: JWT + 401 refresh
│   │   ├── ApiResponse.kt               Sealed class for API responses
│   │   ├── WebSocketManager.kt          OkHttp WebSocket + event parsing
│   │   └── MjpegStreamDecoder.kt        MJPEG frame parser → Bitmap Flow
│   │
│   ├── ble/
│   │   ├── BleManager.kt                CompanionDeviceManager + GATT client
│   │   ├── BleDeviceScanner.kt          Scan + filter Epicura peripherals
│   │   ├── BlePairingService.kt         Pairing flow orchestration
│   │   ├── WifiProvisioningService.kt   Write SSID/password, monitor status
│   │   └── BleConstants.kt              Service/characteristic UUIDs
│   │
│   ├── auth/
│   │   ├── AuthManager.kt              Login, register, token lifecycle
│   │   ├── TokenStorage.kt             EncryptedSharedPreferences for JWT
│   │   └── AuthState.kt                StateFlow-based auth state
│   │
│   └── storage/
│       ├── EpicuraDatabase.kt           Room database definition
│       ├── RecipeDao.kt                 Recipe queries (Room DAO)
│       ├── HistoryDao.kt               Cooking history queries
│       ├── CachedRecipeEntity.kt        Room entity for offline recipes
│       ├── CookingHistoryEntity.kt      Room entity for session history
│       └── ImageCache.kt               Coil disk cache configuration
│
├── features/
│   ├── auth/
│   │   ├── LoginScreen.kt
│   │   ├── RegisterScreen.kt
│   │   └── AuthViewModel.kt
│   │
│   ├── recipes/
│   │   ├── RecipeListScreen.kt          LazyVerticalGrid of recipes + filters
│   │   ├── RecipeDetailScreen.kt        Full recipe with ingredients + stages
│   │   ├── RecipeSearchBar.kt           Search + category filter chips
│   │   └── RecipesViewModel.kt
│   │
│   ├── cooking/
│   │   ├── CookingProgressScreen.kt     Live status, camera, gauges
│   │   ├── CookingControlsBar.kt       Start, pause, stop buttons
│   │   ├── TemperatureGauge.kt          Canvas-drawn circular temp display
│   │   ├── StageProgressIndicator.kt    Stage-by-stage progress
│   │   └── CookingViewModel.kt
│   │
│   ├── pairing/
│   │   ├── PairingFlowScreen.kt         Step-by-step BLE pairing
│   │   ├── DeviceScanScreen.kt          BLE device discovery list
│   │   ├── WifiSetupScreen.kt           SSID/password entry
│   │   ├── PairingCompleteScreen.kt     Success confirmation
│   │   └── PairingViewModel.kt
│   │
│   ├── history/
│   │   ├── HistoryListScreen.kt         Past cooking sessions
│   │   ├── HistoryDetailScreen.kt       Session details + stage log
│   │   └── HistoryViewModel.kt
│   │
│   └── settings/
│       ├── SettingsScreen.kt            Preferences, allergens, devices
│       ├── ApplianceListScreen.kt       Paired devices management
│       ├── ProfileScreen.kt            User profile editing
│       └── SettingsViewModel.kt
│
├── di/
│   ├── NetworkModule.kt                 Hilt: Retrofit, OkHttp, WebSocket
│   ├── DatabaseModule.kt               Hilt: Room database, DAOs
│   ├── BleModule.kt                    Hilt: BLE manager
│   └── AuthModule.kt                   Hilt: Auth manager, token storage
│
├── navigation/
│   ├── NavGraph.kt                      Compose Navigation graph
│   ├── Routes.kt                        Sealed class for navigation routes
│   └── BottomNavBar.kt                 Bottom navigation composable
│
└── ui/
    ├── theme/
    │   ├── Theme.kt                     Material 3 theme (Epicura colors)
    │   ├── Color.kt                     Brand color definitions
    │   ├── Type.kt                      Typography scale
    │   └── Shape.kt                     Corner radius definitions
    │
    └── components/
        ├── RecipeCard.kt                Reusable recipe card composable
        ├── StatusBadge.kt               Device/cooking status badge
        ├── EpicuraButton.kt             Styled button variants
        └── LoadingIndicator.kt          Shimmer + spinner states
```

---

## Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **Hilt** | 2.51+ | Dependency injection |
| **Retrofit** | 2.11+ | Type-safe REST API client |
| **OkHttp** | 4.12+ | HTTP client, WebSocket, interceptors |
| **Moshi** / **Kotlinx Serialization** | Latest | JSON parsing |
| **Room** | 2.6+ | Local SQLite database (recipes, history) |
| **Coil** | 2.7+ | Image loading and caching (Compose integration) |
| **DataStore** | 1.1+ | Preferences storage (user settings) |
| **Compose Navigation** | 2.8+ | Type-safe navigation with arguments |
| **Material 3** | 1.3+ | Design system components |
| **Accompanist** | Latest | Compose utility libraries (permissions, etc.) |
| **Firebase Messaging** | Latest | FCM push notifications |
| **Kotlin Coroutines** | 1.8+ | Async programming, Flow |
| **Timber** | 5.0+ | Logging |
| **LeakCanary** | 2.14+ | Memory leak detection (debug only) |

---

## BLE Implementation Notes

### CompanionDeviceManager Approach

Android 8.0+ provides `CompanionDeviceManager` for BLE pairing, which avoids requiring `ACCESS_FINE_LOCATION` permission:

```kotlin
class BleManager @Inject constructor(
    private val context: Context,
    private val companionDeviceManager: CompanionDeviceManager
) {
    fun startPairing(activity: ComponentActivity) {
        val filter = BluetoothLeDeviceFilter.Builder()
            .setNamePattern(Pattern.compile("Epicura-.*"))
            .setScanFilter(
                ScanFilter.Builder()
                    .setServiceUuid(ParcelUuid(BleConstants.WIFI_PROVISIONING_SERVICE_UUID))
                    .build()
            )
            .build()

        val request = AssociationRequest.Builder()
            .addDeviceFilter(filter)
            .setSingleDevice(false)
            .build()

        companionDeviceManager.associate(
            request,
            object : CompanionDeviceManager.Callback() {
                override fun onDeviceFound(chooserLauncher: IntentSender) {
                    activity.startIntentSenderForResult(chooserLauncher, REQUEST_CODE, null, 0, 0, 0)
                }
                override fun onFailure(error: CharSequence?) {
                    // Handle scan failure
                }
            },
            null
        )
    }
}
```

### Key Considerations

- **Permissions (Android 12+):** Request `BLUETOOTH_CONNECT` and `BLUETOOTH_SCAN` at runtime
- **CompanionDeviceManager:** Preferred for pairing — shows system UI, no location permission needed
- **Fallback:** For Android < 8.0 (API < 26), use `BluetoothLeScanner` directly (min SDK 26 avoids this)
- **MTU Negotiation:** Request 247 MTU after connection for efficient WiFi credential transfer
- **Error Handling:** Handle `BluetoothGatt.GATT_FAILURE`, connection timeout, bond errors
- **Lifecycle:** Disconnect GATT in `onStop()`, reconnect in `onStart()` if pairing incomplete

---

## Foreground Service for Cooking

When the user starts a cook remotely, a foreground service maintains the WebSocket connection and displays a persistent notification with cooking progress:

```kotlin
class CookingForegroundService : Service() {
    private val notificationId = 1001

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = NotificationCompat.Builder(this, COOKING_CHANNEL_ID)
            .setContentTitle("Cooking Dal Tadka")
            .setContentText("Stage 3/6 - Saute Onions (42%)")
            .setSmallIcon(R.drawable.ic_cooking)
            .setOngoing(true)
            .setProgress(100, 42, false)
            .build()

        startForeground(notificationId, notification)
        return START_STICKY
    }
}
```

**Foreground Service Type:** `foregroundServiceType="connectedDevice"` (Android 14+)

---

## WorkManager for Background Sync

Periodic background tasks using WorkManager:

| Worker | Schedule | Task |
|--------|----------|------|
| `RecipeSyncWorker` | Every 6 hours (WiFi only) | Sync new/updated recipes from cloud |
| `HistoryUploadWorker` | Every 1 hour (any network) | Upload unsynced cooking logs |
| `TokenRefreshWorker` | Every 12 hours | Preemptively refresh JWT tokens |
| `PushTokenRefreshWorker` | On app update | Re-register FCM token |

```kotlin
val syncRequest = PeriodicWorkRequestBuilder<RecipeSyncWorker>(6, TimeUnit.HOURS)
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.UNMETERED)
            .build()
    )
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "recipe_sync",
    ExistingPeriodicWorkPolicy.KEEP,
    syncRequest
)
```

---

## Push Notifications (FCM)

### Setup

```kotlin
class EpicuraFirebaseMessagingService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        // Register with backend: POST /push/register { platform: "android", token: token }
        CoroutineScope(Dispatchers.IO).launch {
            apiClient.registerPushToken(platform = "android", token = token)
        }
    }

    override fun onMessageReceived(message: RemoteMessage) {
        // Handle data payload → show notification or update UI
        when (message.data["type"]) {
            "cooking_complete" -> showCookingCompleteNotification(message)
            "cooking_error" -> showCookingErrorNotification(message)
            "firmware_update" -> showFirmwareNotification(message)
        }
    }
}
```

### Notification Channels (Android 8.0+)

| Channel | ID | Importance | Description |
|---------|----|------------|-------------|
| Cooking Alerts | `cooking_alerts` | HIGH | Cooking complete, errors |
| Device Status | `device_status` | DEFAULT | Firmware updates, device alerts |
| General | `general` | LOW | New recipes, announcements |

---

## Testing

### Unit Tests (JUnit 5)

| Test Class | Scope |
|-----------|-------|
| `ApiClientTest` | Request building, interceptors, error parsing |
| `AuthManagerTest` | Login, register, token lifecycle |
| `BleManagerTest` | Mock BLE interactions, state transitions |
| `RecipesViewModelTest` | Recipe list loading, filtering, search |
| `CookingViewModelTest` | WebSocket events, state transitions |
| `PairingViewModelTest` | BLE pairing flow |

### Flow Testing (Turbine)

```kotlin
@Test
fun `recipes load successfully`() = runTest {
    val viewModel = RecipesViewModel(repository)

    viewModel.recipes.test {
        assertEquals(UiState.Loading, awaitItem())
        assertEquals(UiState.Success(mockRecipes), awaitItem())
    }
}
```

### UI Tests (Compose UI Test)

```kotlin
@Test
fun recipeCard_displaysCorrectInfo() {
    composeTestRule.setContent {
        RecipeCard(recipe = testRecipe)
    }

    composeTestRule.onNodeWithText("Dal Tadka").assertIsDisplayed()
    composeTestRule.onNodeWithText("35 min").assertIsDisplayed()
    composeTestRule.onNodeWithText("Easy").assertIsDisplayed()
}
```

### Testing Tools

| Tool | Purpose |
|------|---------|
| JUnit 5 | Unit testing framework |
| Turbine | Testing Kotlin Flow emissions |
| MockK | Kotlin mocking library |
| Compose UI Test | Composable rendering and interaction tests |
| Robolectric | JVM-based Android runtime for unit tests |
| Hilt Testing | DI module replacement in tests |
| LeakCanary | Memory leak detection (debug builds) |

---

## Related Documentation

- [[01-Mobile-Architecture|Mobile Architecture]] - Shared architecture and design system
- [[02-iOS-App|iOS App]] - iOS counterpart
- [[../11-API/01-REST-API-Reference|REST API Reference]] - Backend API
- [[../11-API/02-WebSocket-Events|WebSocket Events]] - Real-time events
- [[../11-API/04-BLE-Services|BLE Services]] - BLE GATT services and pairing flow
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]] - Design language

#epicura #android #kotlin #jetpack-compose #mobile #ble #native-mobile

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
