---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Tech Stack

## Architecture Overview

Epicura uses a dual-processor architecture with clearly separated responsibilities. The CM5 handles high-level application logic and AI, while the STM32G4 manages real-time control and safety-critical operations.

| Layer | CM5 (Application) | STM32G4 (Real-Time) |
|-------|-------------------|---------------------|
| **Hardware** | BCM2712, 4x Cortex-A76 @ 2.4 GHz, 4/8 GB RAM | STM32G474RE, Cortex-M4F @ 170 MHz, 512 KB Flash, 128 KB SRAM |
| **OS** | Yocto Linux (Kirkstone/Scarthgap), systemd | FreeRTOS 10.x |
| **UI Framework** | Kivy (Python) on 10" touchscreen | None |
| **AI/ML** | TensorFlow Lite, OpenCV 4.x | None |
| **Application** | Python 3.11+ (Recipe Engine, CV, UI) | C (MISRA C subset) |
| **Communication** | SPI/CAN driver, MQTT, HTTPS | SPI/CAN driver |
| **Storage** | PostgreSQL 16 (Docker), ext4 filesystem | Non-volatile flash (settings, logs) |
| **Development** | Yocto/bitbake, VS Code + Kivy Designer | STM32CubeIDE, STM32CubeMX |

---

## CM5 Software Stack

### Hardware Platform

**Raspberry Pi Compute Module 5:**

| Specification | Value |
|--------------|-------|
| SoC | Broadcom BCM2712 |
| CPU | 4-core Cortex-A76 @ 2.4 GHz |
| GPU | VideoCore VII (OpenGL ES 3.1, Vulkan 1.2) |
| RAM | 4 GB LPDDR4X |
| Storage | 64 GB eMMC (onboard) |
| Camera | MIPI CSI-2 (2-lane or 4-lane) |
| Display | MIPI DSI (for touchscreen) or HDMI |
| Connectivity | WiFi 802.11ac, Bluetooth 5.0, GbE |
| GPIO | 28x GPIO, UART, SPI, I2C |
| Carrier Board | CM5IO (Raspberry Pi Compute Module IO Board) |

### Operating System & Container Architecture

**Yocto Linux (Kirkstone or Scarthgap LTS):**
- Custom BSP built with bitbake for CM5
- Minimal image (~500 MB): kernel + systemd + Docker daemon
- Device tree overlays for CSI-2 camera and touchscreen
- Read-only rootfs with overlay for data partition
- A/B root partition layout for OTA updates (swupdate)

**Docker Container Architecture:**

All application services run as Docker containers on the CM5:

```
┌─────────────────────────────────────────────────────────────┐
│                  Yocto Linux (Host OS)                      │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Docker Engine                             │  │
│  │                                                        │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │  │
│  │  │ PostgreSQL   │ │ MQTT Broker  │ │ Backend API  │  │  │
│  │  │ Container    │ │ (Mosquitto)  │ │ (FastAPI)    │  │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘  │  │
│  │                                                        │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │  │
│  │  │ Frontend UI  │ │ Recipe Engine│ │ CM5-STM32    │  │  │
│  │  │ (Kivy)       │ │ (Python)     │ │ Bridge       │  │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘  │  │
│  │                                                        │  │
│  │  ┌──────────────┐ ┌──────────────┐                   │  │
│  │  │ CV Pipeline  │ │ Cloud Sync   │                   │  │
│  │  │ (TFLite/OCV) │ │ Service      │                   │  │
│  │  └──────────────┘ └──────────────┘                   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Container Orchestration:**
- Docker Compose for service management
- Persistent volumes for PostgreSQL data and recipe cache
- Inter-container networking via Docker bridge network
- Host network mode for MQTT and API services

### UI Framework

#### Comparison

| Criteria | Kivy (Chosen) | Qt6/QML | LVGL |
|----------|--------------|---------|------|
| Language | Python (pure) | C++ backend, QML frontend | C (pure) |
| Rendering | GPU-accelerated (OpenGL ES) | GPU-accelerated (OpenGL ES) | Software or basic GPU |
| Widgets | Rich set: buttons, sliders, lists, carousel, video | Rich set: buttons, sliders, lists, charts | Lightweight widget set |
| Camera Integration | Kivy Camera widget + GStreamer | Qt Multimedia + GStreamer | Manual framebuffer |
| Touch Support | Native multi-touch, gestures | Native multi-touch, gestures | Basic touch events |
| Python Integration | Native (100% Python) | PySide6 bindings required | ctypes bindings |
| Development Speed | Fast (Python ecosystem) | Moderate (C++ + QML) | Slow (C only) |
| Resource Usage | ~40-60 MB RAM | ~60-100 MB RAM | ~2-10 MB RAM |
| Complexity | Low (single language) | High (C++ + QML + bindings) | Medium (C only) |
| **Recommendation** | **Primary choice** | **Overkill for this use case** | **Too limited** |

**Decision Rationale**: Kivy allows Python developers to build the entire UI without learning QML or managing C++ bindings. Qt6/QML is designed for medical-grade UX and automotive HMIs—overkill for a kitchen appliance. Kivy provides sufficient touch support, GPU acceleration, and camera integration while keeping development simple and aligned with the Python-based backend services.

#### Kivy Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Kivy Application (Python)                   │
│  • HomePage (recipe browser, quick start)               │
│  • CookingPage (live camera, temp/time, progress)       │
│  • SettingsPage (preferences, pairing, about)           │
│                                                          │
│  Kivy Widgets:                                           │
│  • ScreenManager (page navigation)                       │
│  • Camera widget (live CSI-2 feed)                       │
│  • Video widget (recorded sessions playback)            │
│  • GridLayout, BoxLayout (responsive layouts)           │
│  • Button, Slider, Label, TextInput (controls)          │
├─────────────────────────────────────────────────────────┤
│                    Kivy Framework                        │
│  • Core: Window, Clock, Logger                           │
│  • Graphics: OpenGL ES rendering                         │
│  • Input: Touch events, multi-touch gestures            │
│  • Network: URLRequest (async HTTP)                      │
├─────────────────────────────────────────────────────────┤
│                   Backend Integration                    │
│  • REST API client (requests library)                    │
│  • Redis pub/sub for real-time updates                   │
│  • PostgreSQL client (psycopg2) for local queries        │
├─────────────────────────────────────────────────────────┤
│                   Yocto Linux                            │
└─────────────────────────────────────────────────────────┘
```

### AI/ML Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Image Capture | GStreamer + V4L2 | CSI-2 camera frame acquisition |
| Preprocessing | OpenCV 4.x | Resize, normalize, color conversion |
| Inference | TensorFlow Lite 2.x | MobileNetV2 INT8 model execution |
| Training | Python/Keras (off-device) | Model training on cloud/desktop GPU |
| Labeling | LabelImg / Roboflow | Cooking stage image annotation |

### Recipe Engine

- **Language:** Python 3.11+
- **Container:** Dedicated Docker container with Python runtime
- **Libraries:** PyYAML (recipe parsing), jsonschema (validation), transitions (state machine), psycopg2 (PostgreSQL driver)
- **Interface:** REST API endpoints consumed by Kivy frontend
- **Communication:**
  - PostgreSQL for recipe data
  - Redis pub/sub for real-time state updates
  - gRPC or HTTP API for Kivy frontend integration

### Cloud & Networking

| Service | Library / Protocol | Purpose |
|---------|--------------------|---------|
| Telemetry | Mosquitto MQTT (Docker container) | Local broker + cloud bridge for cooking data |
| Recipe Sync | PostgreSQL replication / REST API | Bidirectional sync with cloud database |
| OTA Updates | swupdate | A/B partition firmware updates |
| Backend API | FastAPI (Python, Docker container) | REST API for UI and mobile app |
| Live Camera | MJPEG over HTTP or WebSocket | Stream cooking video to mobile app |
| CM5-STM32 Bridge | Python service (Docker container) | SPI/UART protocol handler, message queuing |

### Storage

**PostgreSQL 16:**
- Primary database running in Docker container on CM5
- Same schema as cloud backend for consistency
- Recipes, cooking logs, user preferences, ingredient library, images
- JSONB for flexible recipe data
- Full-text search for recipe discovery
- Persistent Docker volume for data partition
- Automated backup to cloud via pg_dump
- Bi-directional sync with cloud PostgreSQL instance

**Database Architecture:**

| Aspect | Local (CM5) | Cloud |
|--------|-------------|-------|
| Engine | PostgreSQL 16 (Docker) | PostgreSQL 16 (RDS/Neon) |
| Schema | Identical | Identical |
| Purpose | Local cache, offline operation | Centralized data, multi-device sync |
| Sync Direction | Bidirectional | Bidirectional |
| Recipes | Downloaded from cloud + local edits | Master repository |
| Cooking Logs | Created locally, synced to cloud | Aggregated from all devices |
| Images | Cached locally (S3 refs) | Stored in S3/R2 |

### CM5 Development Tools

| Tool | Purpose |
|------|---------|
| Yocto / bitbake | Build custom Linux image with Docker support |
| Docker Compose | Container orchestration for local development |
| VS Code + Kivy Designer | Kivy application development |
| VS Code + Remote SSH | Python development on target |
| GDB (remote) | C++ debugging via SSH |
| perf / htop | Performance profiling on target |
| pytest | Python unit and integration testing |
| pytest | Kivy UI unit testing |
| docker logs / docker stats | Container debugging and monitoring |

---

## CM5-STM32 Bridge Service

The bridge service runs as a Python Docker container and handles all communication between the CM5 application layer and the STM32 real-time controller.

### Bridge Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CM5 Application Layer                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ Recipe Engine│ │  Kivy UI     │ │  Backend API │        │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘        │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                  REST API / Redis Pub/Sub                   │
│                          │                                  │
│         ┌────────────────▼────────────────┐                 │
│         │   CM5-STM32 Bridge Service      │                 │
│         │   (Python Docker Container)     │                 │
│         │                                 │                 │
│         │  • SPI/UART protocol handler   │                 │
│         │  • Message queue (Redis)       │                 │
│         │  • Command serialization       │                 │
│         │  • Telemetry buffering         │                 │
│         │  • Watchdog heartbeat          │                 │
│         └────────────┬────────────────────┘                 │
│                      │                                      │
│                  SPI / UART                                 │
│                      │                                      │
└──────────────────────┼──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   STM32G474RE                               │
│               (FreeRTOS Controller)                         │
└─────────────────────────────────────────────────────────────┘
```

### Bridge Service Features

| Feature | Implementation |
|---------|----------------|
| **Protocol** | Binary message framing (TYPE, MSG_ID, LENGTH, PAYLOAD, CRC) |
| **Transport** | SPI (primary, 2 MHz) or UART (fallback, 115200 baud) |
| **Message Queue** | Redis for async command dispatch |
| **Telemetry Buffer** | PostgreSQL write batching (10s interval) |
| **Health Monitoring** | Heartbeat every 2s, alerts if STM32 unresponsive |
| **API** | REST endpoints: `/bridge/command`, `/bridge/telemetry`, `/bridge/status` |
| **Logging** | Structured JSON logs to Docker stdout |

### Bridge Service Stack

```python
# Python dependencies
├── pyserial (UART fallback)
├── spidev (SPI communication)
├── redis (message queue)
├── psycopg2 (PostgreSQL for telemetry storage)
├── fastapi (REST API endpoints)
├── pydantic (message validation)
└── asyncio (async I/O)

---

## STM32 Software Stack

### Hardware Platform

#### Primary Choice: STM32G474RE

| Specification | Value |
|--------------|-------|
| Core | ARM Cortex-M4F @ 170 MHz |
| Flash | 512 KB |
| SRAM | 128 KB |
| FPU | Single-precision hardware FPU |
| ADC | 5x 12-bit ADC (up to 4 Msps) |
| Timers | Advanced PWM timers (HRTIM for induction) |
| Comm | 3x UART, 3x SPI, 4x I2C, FDCAN |
| Package | LQFP-64 or LQFP-100 |

#### Alternative: STM32F446RE

| Specification | Value |
|--------------|-------|
| Core | ARM Cortex-M4F @ 180 MHz |
| Flash | 512 KB |
| SRAM | 128 KB |
| FPU | Single-precision hardware FPU |
| ADC | 3x 12-bit ADC |
| Timers | Standard PWM timers |
| Comm | 4x UART, 4x SPI, 3x I2C, 2x CAN |
| Package | LQFP-64 |

**Recommendation:** STM32G474RE preferred for its FDCAN peripheral (required for CAN bus communication with the microwave induction surface module) and HRTIM for precise servo PWM control.

### RTOS

**FreeRTOS 10.x:**
- 4-5 concurrent tasks (PID, Motor, Sensor, Safety, Communication)
- Priority-based preemptive scheduling
- Memory: heap_4 allocator (128 KB SRAM budget)
- Tick rate: 1 kHz (1 ms resolution)
- Stack monitoring enabled for overflow detection

### Language & Standards

- **Language:** C11 (MISRA C:2012 subset for safety-critical paths)
- **Math:** CMSIS-DSP library for PID computation and signal filtering
- **Coding standard:** MISRA C mandatory for safety monitor and motor control tasks

### HAL & Drivers

| Peripheral | Driver | Usage |
|------------|--------|-------|
| PWM (TIM/HRTIM) | STM32 HAL TIM | Motor control (BLDC, SG90 servos) |
| ADC | STM32 HAL ADC + DMA | Temperature sensors, current sensing |
| SPI | STM32 HAL SPI | Thermocouple interface (MAX31855) |
| I2C | STM32 HAL I2C | Load cells (HX711), IR thermometer |
| SPI | STM32 HAL SPI + DMA | Communication with CM5 (SPI2, slave mode) |
| FDCAN | STM32 HAL FDCAN | CAN bus to microwave induction surface (primary heater control) |
| GPIO | STM32 HAL GPIO | Limit switches, ASD servos, CID actuators, SLD solenoids, buzzer |
| IWDG | STM32 HAL IWDG | Independent watchdog (safety) |

### STM32 Development Tools

| Tool | Purpose |
|------|---------|
| STM32CubeIDE | Integrated C development, debugging |
| STM32CubeMX | Peripheral configuration, code generation |
| ST-Link V3 | On-chip debugging and programming |
| openocd | Alternative debug interface |
| STM32CubeProgrammer | Flash programming and option bytes |
| Logic Analyzer | UART/SPI/I2C protocol debugging |

---

## Companion Mobile Apps

### Framework Comparison

| Criteria | Native (Swift + Kotlin) (Chosen) | Flutter (Previously Considered) |
|----------|----------------------------------|--------------------------------|
| Language | Swift 5.9+ (iOS), Kotlin 1.9+ (Android) | Dart |
| UI Framework | SwiftUI / Jetpack Compose | Custom Skia engine |
| BLE Support | Core Bluetooth / CompanionDeviceManager (direct platform APIs) | flutter_blue_plus (plugin-based, limited control) |
| Camera Streaming | AVFoundation / CameraX (native MJPEG decoding) | Plugin-based, frame decoding overhead |
| Platform Feel | 100% native UI, gestures, animations | Approximates native via Skia |
| Background Processing | Full OS-level support (BGTasks / WorkManager) | Limited plugin support |
| App Size | ~15-25 MB per platform | ~25-40 MB (Dart runtime + Skia) |
| Push Notifications | Native APNs / FCM integration | Plugin-based |
| **Recommendation** | **Primary choice** | **Not selected** |

**Decision:** Native development provides superior BLE integration, camera streaming performance, and platform-native UX — all critical for Epicura's pairing and live cooking flows. See [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] for full rationale.

### Communication

| Channel | Protocol | Purpose |
|---------|----------|---------|
| WiFi (Direct) | mDNS discovery + REST | Recipe browsing, settings, history |
| WiFi (Direct) | WebSocket / MJPEG | Live camera feed during cooking |
| Cloud | HTTPS REST API | Remote monitoring, recipe store |
| Cloud | WebSocket (cloud relay) | Real-time cooking progress via backend |
| Cloud | Push notifications (FCM/APNs) | Cooking complete, error alerts |
| BLE | GATT services | Device pairing, WiFi provisioning |

### Key Screens

1. **Recipe Browse** - Grid of recipes with filters (category, time, difficulty)
2. **Recipe Detail** - Ingredients, steps, customization (spice level, allergens)
3. **Cooking Progress** - Live camera feed, temperature gauge, stage progress
4. **History** - Past cooks with ratings, time logs, notes
5. **Settings** - Device pairing, spice preferences, allergen profiles, language
6. **Remote Start** - Select recipe and start cooking remotely
7. **Device Pairing** - BLE scan, WiFi provisioning, cloud account linking

---

## Testing & Validation

### CM5 Testing

| Framework | Language | Scope |
|-----------|----------|-------|
| pytest | Python | Recipe engine, CV pipeline, cloud sync |
| pytest-cov | Python | Code coverage reporting |
| pytest | Python | Kivy UI components and screens |
| Google Test | C++ | Shared C++ libraries |

### STM32 Testing

| Framework | Language | Scope |
|-----------|----------|-------|
| Unity test framework | C | PID controller, protocol parser, safety logic |
| CMock | C | Mock HAL functions for unit testing |
| Ceedling | C | Build system for Unity + CMock |

### Integration & System Testing

| Method | Purpose |
|--------|---------|
| Hardware-in-Loop (HIL) | STM32 + real sensors, CM5 + camera, end-to-end |
| SPI loopback | Protocol testing without full hardware |
| Static analysis (cppcheck) | C/C++ code quality on both platforms |
| PC-lint (MISRA) | MISRA C compliance on STM32 safety code |
| Valgrind | Memory leak detection on CM5 |
| Kivy Inspector | UI rendering performance on CM5 |

---

## Firmware Update Strategy

### CM5 (Yocto Linux)

```
┌───────────────────────────────────────────────┐
│              eMMC Partition Layout              │
├──────────┬──────────┬──────────┬──────────────┤
│ Boot     │ RootFS A │ RootFS B │ Data         │
│ (FAT32)  │ (ext4)   │ (ext4)   │ (ext4)       │
│ 256 MB   │ 2 GB     │ 2 GB     │ Remaining    │
└──────────┴──────────┴──────────┴──────────────┘
```

- **Mechanism:** swupdate with dual A/B root partitions
- **Delivery:** HTTPS download from update server
- **Verification:** RSA-2048 signature on update image
- **Rollback:** If boot fails 3 times, revert to previous partition
- **Data partition:** Preserved across updates (recipes, logs, preferences)

### STM32 (FreeRTOS)

- **Mechanism:** System bootloader (STM32 built-in SPI bootloader)
- **Trigger:** CM5 asserts STM32 BOOT0 pin via GPIO, then resets
- **Delivery:** CM5 downloads .bin, streams to STM32 over SPI
- **Verification:** CRC-32 check after flashing
- **Rollback:** Dual-bank flash (if available) or re-flash previous version

---

## Development Timeline

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| **Environment Setup** | 2 weeks | Yocto BSP for CM5, STM32CubeIDE project, toolchain validation |
| **Hardware Bring-up** | 4 weeks | CM5 boot + display, STM32 peripherals (PWM, ADC, UART), camera test |
| **Core Firmware** | 6 weeks | FreeRTOS tasks, PID controller, motor control, safety monitor, protocol |
| **CV Integration** | 4 weeks | Camera pipeline, model training (collect cooking images), TFLite on CM5 |
| **UI Development** | 4 weeks | Kivy screens (home, cooking, settings), camera widget, recipe browser |
| **App Development** | 3 weeks | Native iOS + Android apps (recipe browse, live view, settings), WiFi communication |
| **System Integration** | 4 weeks | End-to-end cooking tests, timing tuning, error handling, OTA updates |

**Total estimated:** ~27 weeks (approximately 7 months) from environment setup to integration complete.

---

## Design Decisions

| Decision | Chosen | Alternative | Rationale |
|----------|--------|-------------|-----------|
| CM5 OS | Yocto Linux | Raspbian (Raspberry Pi OS) | Yocto provides minimal custom image, A/B OTA, long-term reproducibility; Raspbian is general-purpose and bloated for embedded |
| UI Framework | Kivy | Qt6/QML, LVGL | Kivy provides GPU-accelerated rendering, Python-native development, camera integration, and i18n via gettext; simpler than Qt6, more capable than LVGL |
| Recipe Engine Language | Python 3.11+ | C++ | Python provides rapid development, easy YAML parsing, and rich ecosystem; performance is sufficient on Cortex-A76 |
| Mobile App Framework | Native (Swift + Kotlin) | Flutter | Native platform APIs for BLE (Core Bluetooth, CompanionDeviceManager) and camera streaming; better UX, smaller app size |
| Backend Framework | Fastify (TypeScript) | Express, NestJS | Fastest Node.js framework, built-in schema validation, TypeScript-first, plugin system |
| STM32 RTOS | FreeRTOS | Bare metal | FreeRTOS provides task isolation, priority scheduling, and watchdog integration needed for concurrent PID + safety + comms |
| Inter-Processor Comm | SPI (primary) | CAN bus | SPI high throughput for CM5↔STM32; CAN used for microwave surface control |
| STM32 Variant | STM32G474RE | STM32F446RE | G474 has FDCAN for microwave surface CAN bus and HRTIM; F446 viable but lacks FDCAN |
| CV Model | MobileNetV2 INT8 | Custom CNN | MobileNetV2 is well-supported on TFLite, proven on ARM, and achievable inference time <200 ms |
| Database | PostgreSQL (Docker) | SQLite, MongoDB | PostgreSQL provides schema consistency with cloud, JSONB support, full-text search, and advanced indexing; Docker enables easy deployment and updates |
| Firmware Update | swupdate (A/B) | Manual SD card | A/B partitions enable safe OTA with automatic rollback; SD card update requires physical access |

---

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[04-Controller-Software-Architecture|Controller & Software Architecture]]
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]]
- [[../10-Backend/01-Backend-Architecture|Backend Architecture]]
- [[../11-API/01-REST-API-Reference|REST API Reference]]
- [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]

#epicura #tech-stack #development #raspberry-pi #stm32 #yocto #kivy #freertos #swift #kotlin #native-mobile #tflite

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |