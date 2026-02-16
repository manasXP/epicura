---
tags: [epicura, mpu, cm5, functional-spec, software]
created: 2026-02-16
aliases: [CM5 Spec, MPU Spec]
---

# MPU Functional Specification — Raspberry Pi CM5

> **Document ID:** EPIC-SW-MPU-001
> **Processor:** BCM2712, Quad-core Cortex-A76 @ 2.4 GHz
> **RAM / Storage:** 4 GB LPDDR4X / 64 GB eMMC
> **Carrier Board:** Raspberry Pi CM5IO (official IO board)
> **Related:** [[05-MCU-Functional-Specification]], [[02-Controller-Software-Architecture]], [[01-Tech-Stack]]

---

## 1 Overview

The CM5 is the main application processor for Epicura. It runs Yocto Linux with Docker Compose orchestrating all high-level services: recipe engine, computer vision, touchscreen UI, database, MQTT broker, and cloud sync. It communicates with the STM32 MCU over SPI for real-time actuator commands and telemetry.

### 1.1 Hardware Summary

| Parameter | Value |
|-----------|-------|
| SoC | BCM2712 (Cortex-A76 quad-core @ 2.4 GHz) |
| GPU | VideoCore VII (OpenGL ES 3.1, Vulkan 1.2) |
| RAM | 4 GB LPDDR4X |
| Storage | 64 GB eMMC (A/B partitioned) |
| Camera | MIPI CSI-2 2-lane (IMX219 8 MP or IMX477 12.3 MP) |
| Display | DSI/HDMI — 10" 1280×800 capacitive touch |
| Networking | Wi-Fi 5, BLE 5.0 (on-module) |
| Power | 5 V via CM5IO, ~15 W typical (CM5 + display) |

---

## 2 Functional Requirements

### 2.1 Recipe Engine

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-001 | Parse and validate YAML recipe files | Must | Recipe loads in <2 s; schema errors reported to UI |
| FR-MPU-002 | Execute recipe state machine (IDLE → LOADING → AWAITING_LOAD → PREHEATING → DISPENSING → COOKING → MONITORING → TRANSITIONING → COMPLETING) | Must | All state transitions match [[03-Main-Loop-State-Machine]] trigger table |
| FR-MPU-003 | Support PAUSED state with resume/cancel | Must | Timer suspended, STM32 holds temp at 50% power |
| FR-MPU-004 | Support ERROR state with retry/skip/abort | Must | Error classification determines recovery path |
| FR-MPU-005 | Log cooking session to PostgreSQL on completion | Must | Session record includes timestamps, temps, weights, CV results |
| FR-MPU-006 | Publish session telemetry over MQTT | Should | Topic: `epicura/{device_id}/telemetry`, QoS 1 |

### 2.2 Computer Vision

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-010 | Capture camera frames at 2 Hz during COOKING/MONITORING | Must | Frames 640×480 minimum, consistent interval ±50 ms |
| FR-MPU-011 | Run TFLite MobileNetV2 INT8 inference | Must | Latency <500 ms per frame on CM5 CPU |
| FR-MPU-012 | Classify food stage (raw, browning, cooked, overcooked, anomaly) | Must | Confidence ≥ threshold triggers state transition |
| FR-MPU-013 | Detect anomalies (smoke, dry pot, overflow) | Should | Alert within 1 s of anomaly frame |
| FR-MPU-014 | LED ring illumination (WS2812B) at 5000–6000 K neutral white | Must | Consistent lighting for CV; controlled via GPIO18 |

### 2.3 User Interface

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-020 | Touchscreen UI via Kivy (Python, GPU-accelerated) | Must | Render at 30+ fps on VideoCore VII |
| FR-MPU-021 | Touch-to-visual response <200 ms | Must | Measured from touch event to screen update |
| FR-MPU-022 | Display state-appropriate screens per state machine | Must | Each state maps to a UI view (see §2.3.1) |
| FR-MPU-023 | Live camera feed widget during COOKING/MONITORING | Should | Camera preview with CV confidence overlay |
| FR-MPU-024 | Recipe browser with search and filtering | Must | Full-text search via PostgreSQL |

#### 2.3.1 UI State Mapping

| State | UI View |
|-------|---------|
| IDLE | Recipe browser |
| LOADING | "Validating…" spinner |
| AWAITING_LOAD | Ingredient checklist, live weight readout |
| PREHEATING | Progress bar, ETA countdown |
| DISPENSING | Ingredient name + weight bar (e.g. "Dispensing oil — 30 g") |
| COOKING | Timer, temperature graph, stir indicator |
| MONITORING | CV confidence overlay, "Analyzing…" |
| TRANSITIONING | "Stage 3/6 complete — next: Add Dal" |
| COMPLETING | "Cooking Complete!" summary, user rating prompt |
| PAUSED | "Paused" overlay with Resume / Cancel buttons |
| ERROR | Error description, Retry / Skip / Abort options |
| E_STOP | Full-screen red alert |

### 2.4 Database & Cloud Sync

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-030 | Run PostgreSQL 16 in Docker container | Must | Same schema as cloud backend |
| FR-MPU-031 | Store recipes, sessions, user preferences locally | Must | Full offline operation |
| FR-MPU-032 | Bidirectional sync with cloud PostgreSQL when Wi-Fi available | Should | Conflict resolution: last-write-wins with device priority |
| FR-MPU-033 | Cache recipe images locally for offline use | Should | LRU cache, configurable max size |

### 2.5 MQTT Broker

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-040 | Run Mosquitto broker in Docker container | Must | Accepts local and cloud-bridge connections |
| FR-MPU-041 | Bridge to cloud MQTT when online | Should | Automatic reconnect with exponential backoff |
| FR-MPU-042 | Publish telemetry, session events, errors | Must | QoS 1 for events, QoS 0 for telemetry |

### 2.6 CM5–STM32 Bridge

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-050 | Python bridge service for SPI communication to STM32 | Must | Handles message queuing, CRC validation, retries |
| FR-MPU-051 | Send heartbeat to STM32 every 2 s | Must | Missed heartbeat → STM32 watchdog triggers safe state |
| FR-MPU-052 | UART fallback if SPI fails | Should | Auto-detect and switch, log event |
| FR-MPU-053 | Parse telemetry packets at 10 Hz | Must | Temp, motor RPM, weight, safety state available to all services |

### 2.7 OTA Updates

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MPU-060 | A/B partition updates via swupdate | Must | Rollback on boot failure |
| FR-MPU-061 | RSA-2048 signature verification on update images | Must | Reject unsigned or tampered images |
| FR-MPU-062 | STM32 firmware update via SPI (CM5 streams .bin) | Should | CRC-32 verification before commit |

---

## 3 Hardware Interfaces

### 3.1 GPIO Allocation (via CM5IO 40-pin header)

| GPIO | Function | Direction | Notes |
|------|----------|-----------|-------|
| GPIO8 | SPI0_CE0 | Output | STM32 chip select |
| GPIO9 | SPI0_MISO | Input | STM32 → CM5 data |
| GPIO10 | SPI0_MOSI | Output | CM5 → STM32 data |
| GPIO11 | SPI0_SCLK | Output | SPI clock |
| GPIO4 | IRQ_STM32 | Input | Active-low, data-ready from STM32 |
| GPIO2 | I2C1_SDA | Bidir | Touch panel |
| GPIO3 | I2C1_SCL | Output | Touch panel |
| GPIO18 | WS2812B_DATA | Output | LED ring (12–16 LEDs) |

### 3.2 Camera (CSI-2)

- Connector: 15-pin FFC on CM5IO
- Interface: MIPI CSI-2, 2-lane
- Cable length: ≤150 mm (signal integrity)
- Sensor: IMX219 (prototype) or IMX477 (production option)

### 3.3 Display (DSI/HDMI)

- 10" 1280×800 capacitive touchscreen
- Touch controller on I2C1 (GPIO2/3)
- GPU-accelerated rendering via VideoCore VII

### 3.4 Power

- Input: 5 V from CM5IO 40-pin header (sourced from 24 V → 5 V buck on Driver PCB)
- Typical draw: ~15 W (CM5 + display combined)
- No separate power connector; all power via CM5IO carrier

---

## 4 Software Architecture

### 4.1 Operating System

- **Yocto Linux** (Kirkstone or Scarthgap release)
- Custom BSP with Docker support, CSI-2 camera drivers, GPU acceleration
- A/B root partitions for OTA rollback

### 4.2 Docker Compose Services

| Service | Image Base | Port(s) | Resource Limits |
|---------|-----------|---------|----------------|
| `recipe-engine` | Python 3.11-slim | — | 256 MB RAM |
| `cv-pipeline` | Python 3.11 + OpenCV | — | 512 MB RAM |
| `kivy-ui` | Python 3.11 + Kivy | framebuffer | 512 MB RAM, GPU access |
| `cm5-stm32-bridge` | Python 3.11-slim | — | 128 MB RAM, SPI device |
| `postgresql` | postgres:16-alpine | 5432 | 512 MB RAM |
| `mosquitto` | eclipse-mosquitto:2 | 1883, 8883 | 64 MB RAM |
| `fastapi-backend` | Python 3.11-slim | 8000 | 256 MB RAM |
| `cloud-sync` | Python 3.11-slim | — | 128 MB RAM |

### 4.3 Boot Sequence

1. **U-Boot** → select active A/B partition
2. **Yocto kernel** → hardware init, CSI-2/GPU/SPI drivers
3. **systemd** → mount eMMC, start Docker daemon
4. **Docker Compose up** → PostgreSQL → Mosquitto → bridge → recipe-engine → cv-pipeline → UI → backend → sync
5. **Bridge service** → establish SPI link, send first heartbeat
6. **UI** → display IDLE / recipe browser (target: <30 s from power-on)

### 4.4 Inter-Service Communication

- Services communicate via MQTT topics (local Mosquitto)
- Bridge service publishes STM32 telemetry to `epicura/local/telemetry`
- Recipe engine publishes commands to `epicura/local/commands`
- Bridge subscribes to commands, forwards over SPI to STM32

---

## 5 Communication Protocols

### 5.1 SPI Protocol (CM5 → STM32)

- **Mode:** CM5 = master, STM32 = slave
- **Clock:** SPI0, configurable up to 10 MHz
- **Chip select:** GPIO8 (CE0)
- **IRQ:** GPIO4 (STM32 asserts low when data ready)

**Message Frame:**

```c
typedef struct {
    uint8_t  msg_id;       // Sequence number 0–255
    uint8_t  msg_type;     // Command/response type
    uint16_t payload_len;  // 0–64 bytes
    uint8_t  payload[64];  // Variable-length data
    uint16_t crc;          // CRC-16/CCITT
} cmd_msg_t;               // Max 70 bytes
```

**Key Command Types (CM5 → STM32):**

| Type | Name | Payload | Description |
|------|------|---------|-------------|
| 0x01 | SET_TEMP | target_temp (°C), ramp_rate | Set induction target temperature |
| 0x02 | SET_STIR | pattern, speed_rpm | Set servo stir pattern and speed |
| 0x03 | DISPENSE_ASD | asd_id, target_g | Dispense seasoning from ASD hopper |
| 0x04 | E_STOP | — | Emergency stop all actuators |
| 0x30 | DISPENSE_ASD | id, target_g | Seasoning dispense |
| 0x31 | DISPENSE_CID | id, mode, position | Coarse ingredient dispense |
| 0x32 | DISPENSE_SLD | channel, target_g | Liquid dispense |
| 0x35 | QUERY_WEIGHT | source (POT=0, SLD=1) | Read load cell |
| 0x37 | TARE | source | Zero load cell |

**Key Response Types (STM32 → CM5):**

| Type | Name | Payload | Description |
|------|------|---------|-------------|
| 0x10 | TELEMETRY | temp, motor_rpm, weight, state | Periodic status (10 Hz) |
| 0x12 | STATUS | safety_state, error_code, flags | Safety/error report |

### 5.2 MQTT Topics

| Topic | Publisher | QoS | Description |
|-------|-----------|-----|-------------|
| `epicura/local/telemetry` | bridge | 0 | STM32 sensor data (10 Hz) |
| `epicura/local/commands` | recipe-engine | 1 | Commands for STM32 |
| `epicura/local/cv/result` | cv-pipeline | 1 | CV inference results |
| `epicura/local/session` | recipe-engine | 1 | Session lifecycle events |
| `epicura/{device_id}/telemetry` | cloud-sync | 0 | Cloud-bridged telemetry |

---

## 6 Power Management

### 6.1 Power States

| State | Description | Typical Draw |
|-------|-------------|-------------|
| Active Cooking | All services running, camera capturing, display on | ~15 W |
| Idle | Display on, services running, camera off | ~10 W |
| Standby | Display dimmed/off, reduced polling | ~5 W |
| Off | Powered down (relay-switched) | 0 W |

### 6.2 Power Budget

- CM5 module: 5–8 W (CPU dependent on load)
- Display (10" LCD + backlight): 3–5 W
- LED ring (16× WS2812B): ~1 W
- Total CM5 subsystem: ≤15 W from 5 V rail

---

## 7 Safety & Fault Handling

### 7.1 CM5 Safety Responsibilities

The CM5 is **not** the primary safety controller — the STM32 owns all safety-critical paths. The CM5's safety role is supervisory:

| Responsibility | Action |
|----------------|--------|
| Heartbeat | Send 2 s heartbeat over SPI; if CM5 crashes, STM32 watchdog triggers safe state |
| Error classification | Analyze STM32 error codes, determine user-facing recovery options |
| Logging | Record all safety events to PostgreSQL with timestamps |
| User notification | Display error/E_STOP screens, guide user through recovery |
| CV anomaly detection | Flag smoke/overflow/dry pot, send E_STOP if critical |

### 7.2 Fault Table (CM5-Detected)

| Fault | Detection | Severity | Action |
|-------|-----------|----------|--------|
| SPI link loss | No response for 3 consecutive polls | Critical | Switch to UART fallback; if fails, alert user |
| CV anomaly (smoke/overflow) | Inference confidence ≥ threshold | Critical | Send E_STOP (0x04) to STM32 |
| PostgreSQL crash | Docker health check | Warning | Auto-restart container; queue data in memory |
| OTA update failure | swupdate exit code | Warning | Rollback to B partition |
| Wi-Fi disconnect | Network monitor | Info | Continue offline, queue sync |
| Display freeze | Watchdog timer in UI service | Warning | Restart Kivy container |

### 7.3 Recovery Sequence (E_STOP)

1. CM5 sends E_STOP (0x04) to STM32 (or STM32 initiates independently)
2. STM32 cuts heater relay, brakes servo, activates buzzer
3. CM5 displays full-screen red alert
4. CM5 logs event to PostgreSQL + publishes to MQTT
5. System remains in E_STOP until manual hardware reset (E-stop button released)
6. After reset: STM32 → NORMAL safety state, CM5 → IDLE

---

## 8 Performance Requirements

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Boot time (power-on → recipe browser) | <30 s | Stopwatch from 5 V applied |
| CV inference latency | <500 ms | Timestamp delta (capture → result) |
| UI touch-to-visual response | <200 ms | Touch event → screen update |
| SPI command round-trip | <10 ms | msg_id sent → ACK received |
| Recipe parse + validate | <2 s | YAML load → state machine ready |
| MQTT publish latency (local) | <50 ms | Publish → subscriber callback |
| Database query (recipe list) | <100 ms | SQL execute → result set |
| Camera capture interval | 500 ms ± 50 ms | Frame timestamp jitter |

---

## 9 Dependencies & Constraints

### 9.1 Hardware Dependencies

- CM5IO carrier board provides 5 V power, CSI-2, DSI, SPI, I2C, GPIO breakout
- Controller PCB (STM32) connects via SPI (PB12–15 on STM32 side)
- Driver PCB provides 5 V buck converter feeding CM5IO
- Camera FFC cable ≤150 mm

### 9.2 Software Dependencies

- Yocto BSP must include: Docker CE, CSI-2 camera driver, SPI kernel module, GPU (Mesa/VC4)
- Python 3.11+ for all application services
- TFLite runtime (CPU, INT8 quantized)
- OpenCV 4.x (headless build for CV service)
- Kivy 2.x with SDL2 backend for UI

### 9.3 Cross-References

| Topic | Document |
|-------|----------|
| STM32 MCU spec | [[05-MCU-Functional-Specification]] |
| State machine details | [[03-Main-Loop-State-Machine]] |
| Software architecture | [[02-Controller-Software-Architecture]] |
| Tech stack decisions | [[01-Tech-Stack]] |
| Hardware architecture | [[01-Epicura-Architecture]] |
| Controller PCB | [[01-Controller-PCB-Design]] |
| Driver PCB | [[02-Driver-PCB-Design]] |
| Dispensing subsystems | [[03-Ingredient-Dispensing]] |
