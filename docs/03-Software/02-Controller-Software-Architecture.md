---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Controller & Software Architecture

## Architecture Overview

Epicura uses a dual-processor architecture: a Raspberry Pi CM5 running Yocto Linux for AI vision, UI, and cloud connectivity, paired with an STM32G4 microcontroller running FreeRTOS for real-time motor control, PID loops, and safety monitoring.

| Aspect | CM5 (Application) | STM32G4 (Real-Time) |
|--------|-------------------|---------------------|
| **Processor** | Broadcom BCM2712, 4-core Cortex-A76 | STM32G474RE, Cortex-M4F |
| **Clock** | 2.4 GHz | 170 MHz |
| **OS** | Yocto Linux (Kirkstone/Scarthgap) | FreeRTOS 10.x |
| **Role** | AI/Vision, UI, Recipe Engine, Cloud | PID, Motor, Sensors, Safety |
| **Languages** | Python 3.11+, KV | C (MISRA C subset) |
| **Graphics** | Kivy on 10" touchscreen | None |
| **IPC** | SPI (primary) / CAN bus (alternative) | SPI (primary) / CAN bus (alternative) |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Raspberry Pi CM5 (Yocto Linux)                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      Application Layer                              │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌────────┐ ┌──────────────┐    │    │
│  │  │ Recipe Engine │ │ CV Pipeline  │ │   UI   │ │  Cloud Sync  │    │    │
│  │  │ (State Mach.) │ │ (TFLite/OCV) │ │(Kivy) │ │ (MQTT/HTTPS) │    │    │
│  │  └──────────────┘ └──────────────┘ └────────┘ └──────────────┘    │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                      Middleware Layer                                │    │
│  │  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌─────────────┐  │    │
│  │  │  SQLite  │  │  MQTT Client │  │  GStreamer  │  │  SPI/CAN    │  │    │
│  │  │ Database │  │ (Eclipse Paho)│  │  (Camera)  │  │   Driver    │  │    │
│  │  └──────────┘  └──────────────┘  └────────────┘  └──────┬──────┘  │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                      Yocto Linux (systemd)                          │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │           Hardware: BCM2712, 4x Cortex-A76 @ 2.4 GHz               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                              SPI / CAN Bus
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                       STM32G474RE (FreeRTOS)                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      FreeRTOS Tasks                                  │    │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │    │
│  │  │ PID Control │ │ Motor Control│ │Sensor Polling│ │   Safety   │ │    │
│  │  │  (10 Hz)    │ │  (50 Hz)     │ │  (10 Hz)     │ │  Monitor   │ │    │
│  │  └─────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                      HAL / Driver Layer                              │    │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────────┐  │    │
│  │  │ PWM  │  │ ADC  │  │ SPI  │  │ I2C  │  │ GPIO │  │ SPI/CAN  │  │    │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘  └──────────┘  │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │           Hardware: STM32G474RE, Cortex-M4F @ 170 MHz               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Distribution

| Module | Processor | Rationale |
|--------|-----------|-----------|
| Recipe Engine (State Machine) | CM5 | Complex logic, YAML parsing, file I/O |
| Computer Vision Pipeline | CM5 | TFLite inference, camera access, OpenCV |
| Kivy User Interface | CM5 | GPU-accelerated UI, touchscreen driver |
| Cloud Sync (MQTT/HTTPS) | CM5 | Full Linux networking stack |
| SQLite Database | CM5 | Filesystem access, complex queries |
| OTA Firmware Updates | CM5 | Network + flash management |
| PID Temperature Control | STM32 | Hard real-time, deterministic timing |
| Servo Motor Control | STM32 | PWM generation, position feedback |
| Sensor Polling (Temp/Weight) | STM32 | ADC sampling, I2C/SPI peripherals |
| Safety Monitor / Watchdog | STM32 | Independent safety, E-stop authority |
| Ingredient Dispensing | STM32 | Servo actuation, load cell feedback |
| Induction Heater PWM | STM32 | High-frequency PWM, fault detection |

---

## Software Stack

### CM5 Docker-based Stack

```
┌─────────────────────────────────────────────────────────────┐
│                   Yocto Linux (Host OS)                     │
│     Hardware: BCM2712 (4x Cortex-A76 @ 2.4 GHz)            │
│     RAM: 4 GB LPDDR4X  |  Storage: 64 GB eMMC              │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Docker Engine                             │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Kivy Frontend Container (Python)                      │ │
│  │  • Cooking dashboard • Recipe browser • Settings       │ │
│  │  • Camera widget (GStreamer) • Touch input             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Backend API Container (FastAPI + Python)              │ │
│  │  • Recipe Engine (state machine)                       │ │
│  │  • REST endpoints for UI                               │ │
│  │  • Cloud sync service                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  CV Pipeline Container (Python + TFLite)               │ │
│  │  • Camera capture (V4L2/GStreamer)                     │ │
│  │  • OpenCV preprocessing                                │ │
│  │  • MobileNetV2 INT8 inference                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  CM5-STM32 Bridge Container (Python)                   │ │
│  │  • SPI/UART protocol handler                           │ │
│  │  • Message queue (Redis)                               │ │
│  │  • Telemetry buffering                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  PostgreSQL 16 Container                               │ │
│  │  • Recipes, logs, preferences, ingredients             │ │
│  │  • JSONB for flexible recipe data                      │ │
│  │  • Persistent volume: /var/lib/postgresql/data         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  MQTT Broker Container (Mosquitto)                     │ │
│  │  • Local telemetry pub/sub                             │ │
│  │  • Bridge to cloud broker                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Redis Container                                        │ │
│  │  • Message queue for bridge service                    │ │
│  │  • Pub/sub for inter-container communication           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### STM32 FreeRTOS Stack

```
┌─────────────────────────────────────────────────────────┐
│              FreeRTOS Application Tasks                   │
│  • PID Control         • Motor Control                   │
│  • Sensor Polling      • Safety Monitor                  │
│  • Communication       • Dispensing                      │
├─────────────────────────────────────────────────────────┤
│                      FreeRTOS 10.x                       │
│  • Priority-based preemptive scheduling                  │
│  • Queues, Semaphores, Timers, Event Groups              │
│  • Memory management (heap_4)                            │
├─────────────────────────────────────────────────────────┤
│                   HAL / CMSIS Layer                       │
│  • STM32 HAL drivers (PWM, ADC, SPI, I2C, CAN)          │
│  • CMSIS-DSP (PID math, filtering)                       │
│  • CMSIS-RTOS2 abstraction                               │
├─────────────────────────────────────────────────────────┤
│     Hardware: STM32G474RE (Cortex-M4F @ 170 MHz)         │
│     Flash: 512 KB  |  SRAM: 128 KB                       │
└─────────────────────────────────────────────────────────┘
```

---

## Core Modules

### 1. Recipe Engine (CM5)

#### State Machine Design

Each recipe is modeled as a finite state machine. The Recipe Engine loads a YAML recipe definition, then drives the cooking process by transitioning between stages based on CV analysis, temperature readings, and timer events.

> [!tip] Detailed State Machine
> See [[03-Main-Loop-State-Machine|Main Loop State Machine]] for the full state diagram with Mermaid visualizations, state-layer impact matrix, sequence diagrams, and transition trigger tables.

**Recipe States:**

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
                    ▼                                              │
┌──────┐    ┌──────────┐    ┌───────────────┐    ┌──────┐        │
│ IDLE │───►│ PREHEAT  │───►│ADD_INGREDIENT │───►│ COOK │        │
└──────┘    └──────────┘    └───────────────┘    └──┬───┘        │
   ▲                                                │             │
   │        ┌──────────┐    ┌──────────┐            ▼             │
   │        │ COMPLETE │◄───│ MONITOR  │◄───────┌──────┐         │
   │        └──────────┘    └────┬─────┘        │ STIR │         │
   │                             │              └──────┘         │
   │                             ▼                                │
   │                        ┌──────────┐                          │
   │                        │  ADJUST  │──────────────────────────┘
   │                        └──────────┘
   │
   │        ┌──────────┐
   └────────│  ERROR   │◄─── (from any state)
            └──────────┘
```

#### Recipe Format (YAML)

```yaml
recipe:
  name: "Dal Tadka"
  servings: 4
  total_time_minutes: 35
  stages:
    - name: "Heat Oil"
      temp_target: 180
      duration_seconds: 120
      stir: false
      ingredients: [{subsystem: "SLD", channel: "OIL", name: "oil", amount_g: 30}]
      cv_check: "oil_shimmer"
    - name: "Add Spices to Oil"
      temp_target: 160
      ingredients:
        - {subsystem: "ASD", id: 1, name: "turmeric", amount_g: 3}
        - {subsystem: "ASD", id: 2, name: "chili_powder", amount_g: 5}
      cv_check: "spice_bloom"
      stir: true
      stir_pattern: "intermittent"
    - name: "Add Onions & Tomatoes"
      temp_target: 150
      duration_seconds: 300
      ingredients: [{subsystem: "CID", id: 1, name: "onion_tomato", mode: "FULL"}]
      cv_check: "golden_brown"
      stir: true
      stir_pattern: "continuous"
    - name: "Season"
      temp_target: 140
      duration_seconds: 60
      ingredients: [{subsystem: "ASD", id: 3, name: "salt_garam_masala", amount_g: 5}]
      stir: true
      stir_pattern: "fold"
    - name: "Add Dal & Water"
      temp_target: 95
      ingredients:
        - {subsystem: "CID", id: 2, name: "toor_dal", mode: "FULL"}
        - {subsystem: "SLD", channel: "WATER", name: "water", amount_g: 400}
    - name: "Simmer Dal"
      temp_target: 95
      duration_seconds: 900
      cv_check: "thick_consistency"
      stir: true
      stir_pattern: "intermittent"
```

#### Key Functions

```python
class RecipeEngine:
    def load_recipe(self, recipe_path: str) -> Recipe:
        """Parse YAML recipe file and validate against schema."""
        pass

    def execute_stage(self, stage: Stage) -> StageResult:
        """Run a single cooking stage: set temp, dispense, stir, monitor."""
        pass

    def check_transition(self, stage: Stage, cv_result: CVResult,
                         sensor_data: SensorData) -> bool:
        """Evaluate whether current stage is complete and ready to advance."""
        pass

    def handle_error(self, error: CookingError) -> ErrorAction:
        """Determine recovery action: retry, skip, pause, or abort."""
        pass
```

---

### 2. CV Pipeline (CM5)

#### Pipeline Architecture

```
┌────────────┐    ┌────────────────┐    ┌───────────────┐    ┌────────────────┐
│  CSI-2     │    │  Preprocess    │    │   Inference   │    │ Classification │
│  Camera    │───►│  (OpenCV)      │───►│  (TFLite)     │───►│   & Decision   │
│  Capture   │    │  Resize 224x224│    │  MobileNetV2  │    │                │
│            │    │  Normalize     │    │  INT8 Quant.  │    │  Cooking Stage │
└────────────┘    └────────────────┘    └───────────────┘    └────────────────┘
                                                                     │
                                                                     ▼
                                                              ┌──────────────┐
                                                              │  Confidence  │
                                                              │  < 0.6 ?     │
                                                              │              │
                                                              │  YES ► Timer │
                                                              │  + Temp      │
                                                              │  Fallback    │
                                                              └──────────────┘
```

#### Pipeline Implementation

```python
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

class CVPipeline:
    def __init__(self, model_path: str):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.confidence_threshold = 0.6

    def capture_frame(self, camera) -> np.ndarray:
        """Capture frame from CSI-2 camera via GStreamer pipeline."""
        ret, frame = camera.read()
        return frame

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Resize to 224x224, normalize to [0,1], convert to INT8."""
        resized = cv2.resize(frame, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        return np.expand_dims(normalized, axis=0)

    def infer(self, input_tensor: np.ndarray) -> tuple:
        """Run MobileNetV2 INT8 quantized inference. Target: <200ms."""
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        class_id = np.argmax(output)
        confidence = float(output[0][class_id])
        return class_id, confidence

    def classify_stage(self, frame: np.ndarray) -> dict:
        """Full pipeline: capture -> preprocess -> infer -> classify."""
        preprocessed = self.preprocess(frame)
        class_id, confidence = self.infer(preprocessed)
        if confidence < self.confidence_threshold:
            return {"stage": "unknown", "confidence": confidence,
                    "fallback": True}
        return {"stage": STAGE_LABELS[class_id],
                "confidence": confidence, "fallback": False}
```

**Model Specifications:**

| Parameter | Value |
|-----------|-------|
| Architecture | MobileNetV2 |
| Input Size | 224 x 224 x 3 |
| Quantization | INT8 (post-training) |
| Inference Time | < 200 ms on CM5 |
| Classes | ~15 cooking stages |
| Fallback | Timer + temperature thresholds if confidence < 0.6 |

---

### 3. Motor Control (STM32)

#### PID Controller

```c
typedef struct {
    float setpoint;
    float kp, ki, kd;
    float integral;
    float prev_error;
    float output;
    float output_min, output_max;
} pid_controller_t;

void pid_init(pid_controller_t *pid, float kp, float ki, float kd,
              float out_min, float out_max)
{
    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
    pid->output_min = out_min;
    pid->output_max = out_max;
}

float pid_compute(pid_controller_t *pid, float measurement, float dt)
{
    float error = pid->setpoint - measurement;
    pid->integral += error * dt;
    float derivative = (error - pid->prev_error) / dt;

    pid->output = (pid->kp * error)
                + (pid->ki * pid->integral)
                + (pid->kd * derivative);

    /* Clamp output */
    if (pid->output > pid->output_max) pid->output = pid->output_max;
    if (pid->output < pid->output_min) pid->output = pid->output_min;

    /* Anti-windup: clamp integral if output is saturated */
    if (pid->output == pid->output_max || pid->output == pid->output_min) {
        pid->integral -= error * dt;
    }

    pid->prev_error = error;
    return pid->output;
}
```

#### Stirring Patterns

| Pattern | Speed (RPM) | Behavior | Use Case |
|---------|-------------|----------|----------|
| Continuous | 60 | Constant rotation | Gravy, sauce reduction |
| Intermittent | 30 | 5s on / 10s off | Dal simmering, rice |
| Reverse | 45 | Alternating CW/CCW every 8s | Prevent sticking |
| Scrape | 15 | Slow rotation + edge-seeking path | Thick pastes, halwa |
| Fold | 20 | Gentle wide sweep, low torque | Mixing delicate ingredients |

---

### 4. Safety Monitor (STM32)

#### Safety State Machine

```
┌─────────┐   temp > warn_thresh    ┌──────────┐   temp > crit_thresh   ┌───────────┐
│  NORMAL │────────────────────────►│ WARNING  │───────────────────────►│ CRITICAL  │
│         │   OR sensor_degraded    │          │   OR motor_stall       │           │
└─────────┘                         └──────────┘   OR comms_lost > 5s   └─────┬─────┘
     ▲                                   │                                     │
     │       conditions cleared          │                                     │
     └───────────────────────────────────┘                                     │
                                                                               ▼
                                                                         ┌──────────┐
                                                                         │  E_STOP  │
                                                                         │          │
                                                                         │ Cut heat │
                                                                         │ Stop arm │
                                                                         │ Alert UI │
                                                                         └──────────┘
```

**Transition Conditions:**

| From | To | Condition |
|------|----|-----------|
| NORMAL | WARNING | Temperature > warning threshold (e.g., setpoint + 20C) |
| NORMAL | WARNING | Single sensor reading out of range |
| WARNING | CRITICAL | Temperature > critical threshold (e.g., 260C) |
| WARNING | CRITICAL | Motor stall detected (overcurrent) |
| WARNING | CRITICAL | CM5 heartbeat lost for > 5 seconds |
| CRITICAL | E_STOP | Any CRITICAL condition persists > 3 seconds |
| WARNING | NORMAL | All conditions return to safe range |
| E_STOP | NORMAL | Manual user reset only |

**Watchdog Timer:**
- CM5 sends heartbeat every 2 seconds via SPI
- STM32 independent watchdog (IWDG) timeout: 5 seconds
- If heartbeat missed: enter WARNING state
- If heartbeat missed > 5s: enter CRITICAL state, cut induction

**Emergency Actions (E_STOP):**
1. Immediately send CAN off command to microwave surface module + open safety relay
2. Stop servo motor and engage brake
3. Send alert message to CM5 UI (if comms available)
4. Activate buzzer alarm
5. Log event to non-volatile memory
6. Require manual user intervention to reset

---

### 5. Data Management (CM5)

#### PostgreSQL Schema (Docker Container)

The CM5 uses the same PostgreSQL schema as the cloud backend for consistency. See [[../../10-Backend/02-Database-Schema|Database Schema]] for full table definitions.

**Key Tables:**

```sql
-- Recipes (JSONB for flexible recipe data)
CREATE TABLE recipes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(200) NOT NULL,
    category    VARCHAR(50) NOT NULL,
    cuisine     VARCHAR(50) DEFAULT 'indian',
    recipe_data JSONB NOT NULL,      -- Full recipe definition
    tags        TEXT[] DEFAULT '{}',
    difficulty  VARCHAR(10) NOT NULL,
    time_minutes INTEGER NOT NULL,
    image_url   TEXT,
    version     INTEGER NOT NULL DEFAULT 1,
    is_published BOOLEAN NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Cooking logs
CREATE TABLE cooking_sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id   UUID NOT NULL REFERENCES recipes(id),
    started_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    stages_log  JSONB,              -- Array of {stage, duration, result, cv_confidence}
    status      VARCHAR(20) NOT NULL DEFAULT 'started',
    peak_temperature REAL,
    total_duration_s INTEGER,
    user_rating INTEGER CHECK (user_rating BETWEEN 1 AND 5),
    notes       TEXT
);

-- User preferences
CREATE TABLE user_preferences (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language    VARCHAR(10) DEFAULT 'en_IN',
    spice_level INTEGER DEFAULT 3 CHECK (spice_level BETWEEN 1 AND 5),
    default_servings INTEGER DEFAULT 4,
    allergens   TEXT[] DEFAULT '{}',
    theme       VARCHAR(10) DEFAULT 'light',
    last_sync_at TIMESTAMPTZ
);

-- Indexes for performance
CREATE INDEX idx_recipes_category ON recipes(category);
CREATE INDEX idx_recipes_tags ON recipes USING GIN(tags);
CREATE INDEX idx_recipes_data ON recipes USING GIN(recipe_data jsonb_path_ops);
CREATE INDEX idx_sessions_started ON cooking_sessions(started_at DESC);
```

**Docker Volume Persistence:**

```yaml
volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres  # Persistent partition on eMMC
```

---

### 6. Cloud Sync (CM5)

#### PostgreSQL Sync Strategy

The CM5 PostgreSQL database syncs with the cloud PostgreSQL instance using a hybrid approach:

**Sync Methods:**

| Data Type | Sync Method | Direction | Frequency |
|-----------|-------------|-----------|-----------|
| Recipes | REST API + SQL inserts | Cloud → Device | On-demand + daily |
| Cooking Logs | Batch INSERT via REST API | Device → Cloud | After each session |
| User Preferences | REST API PUT/GET | Bidirectional | On change |
| Recipe Images | S3 URL caching | Cloud → Device | Lazy load |

**Sync Service (Docker Container):**

```python
class CloudSyncService:
    """Runs as background service in Docker container"""

    async def sync_recipes(self):
        """Download new/updated recipes from cloud"""
        last_sync = await self.db.get_last_sync_timestamp()
        response = await self.api_client.get(
            f"/recipes/sync?since={last_sync}"
        )
        for recipe in response['recipes']:
            await self.db.upsert_recipe(recipe)
        await self.db.update_last_sync()

    async def upload_cooking_logs(self):
        """Upload completed cooking sessions to cloud"""
        unsynced_logs = await self.db.get_unsynced_sessions()
        for log in unsynced_logs:
            await self.api_client.post("/sessions", data=log)
            await self.db.mark_session_synced(log['id'])
```

#### MQTT Telemetry

- **Local Broker:** Mosquitto container with bridge to cloud
- **Topic structure:** `epicura/{device_id}/telemetry`
- **QoS:** Level 1 (at least once delivery)
- **Publish interval:** Every 10 seconds during cooking
- **Bridge:** Mosquitto bridge forwards to cloud AWS IoT Core

```python
# Telemetry payload example
{
    "device_id": "EPIC-001",
    "timestamp": "2026-02-14T12:30:00Z",
    "state": "COOKING",
    "recipe_id": "uuid-here",
    "stage": "Simmer Dal",
    "temperature": 96.2,
    "stir_active": true,
    "progress_pct": 72
}
```

#### OTA Firmware Updates

| Target | Method | Mechanism |
|--------|--------|-----------|
| CM5 (Linux) | A/B root partition | swupdate with signature verification |
| STM32 (FreeRTOS) | System bootloader | CM5 triggers STM32 bootloader via BOOT0 GPIO, streams .bin over SPI |

**Update Flow:**
1. CM5 checks for updates via HTTPS
2. Downloads and verifies signature (RSA-2048)
3. CM5: writes to inactive partition, reboots, verifies, swaps
4. STM32: CM5 holds STM32 in bootloader mode, streams firmware, verifies CRC, resets

---

## Control Flow

### Cooking Workflow (10-Step Sequence)

```
 1. User selects recipe on touchscreen
                │
                ▼
 2. Recipe Engine loads YAML, validates ingredients
                │
                ▼
 3. UI prompts user to load dispensing subsystems (ASD/CID/SLD) with weight confirmation
                │
                ▼
 4. CM5 sends PREHEAT command to STM32 (target temperature)
                │
                ▼
 5. For each stage:
    ┌───────────────────────────────────────────────────┐
    │  a. Dispense ingredients (DISPENSE_ASD/CID/SLD)   │
    │  b. Set temperature (CM5 → STM32 SET_TEMP)        │
    │  c. Set stir pattern (CM5 → STM32 SET_STIR)       │
    │  d. Monitor via CV pipeline (camera → TFLite)     │
    │  e. Check transition conditions                   │
    │  f. If stage complete → advance to next stage     │
    └───────────────────────────────────────────────────┘
                │
                ▼
 6. CV pipeline confirms final stage complete
                │
                ▼
 7. CM5 sends STOP commands (temp → 0, stir → off)
                │
                ▼
 8. UI displays "Cooking Complete" with summary
                │
                ▼
 9. Log results to SQLite (temps, times, stages, rating)
                │
                ▼
10. Publish summary to cloud via MQTT
```

---

## CM5-STM32 Communication Protocol

### Message Structure

```c
typedef struct {
    uint8_t  msg_id;        /* Sequence number (0-255, wraps) */
    uint8_t  msg_type;      /* Command or response type */
    uint16_t payload_len;   /* Length of payload in bytes */
    uint8_t  payload[64];   /* Variable-length payload data */
    uint16_t crc;           /* CRC-16/CCITT for integrity */
} cmd_msg_t;
```

### Message Types

| Message | Type Code | Direction | Payload |
|---------|-----------|-----------|---------|
| SET_TEMP | 0x01 | CM5 → STM32 | target_temp (float), ramp_rate (float) |
| SET_STIR | 0x02 | CM5 → STM32 | pattern (uint8), speed_rpm (uint16) |
| DISPENSE_ASD | 0x03 | CM5 → STM32 | asd_id (uint8: 1-3), target_g (uint16) |
| DISPENSE_CID | 0x06 | CM5 → STM32 | cid_id (uint8: 1-2), mode (uint8), pos_mm (uint8) |
| DISPENSE_SLD | 0x07 | CM5 → STM32 | channel (uint8: OIL=1, WATER=2), target_g (uint16) |
| E_STOP | 0x04 | CM5 → STM32 | reason_code (uint8) |
| HEARTBEAT | 0x05 | CM5 → STM32 | uptime_ms (uint32) |
| TELEMETRY | 0x10 | STM32 → CM5 | temp, motor_rpm, weight, state |
| SENSOR_DATA | 0x11 | STM32 → CM5 | adc_values[], ir_temp, load_cells[] |
| STATUS | 0x12 | STM32 → CM5 | safety_state, error_code, flags |
| ACK | 0xFF | Bidirectional | ack_msg_id, result_code |

### Protocol Details

- **Clock speed:** 2 MHz (SPI) or 500 kbps (CAN)
- **Framing:** Type byte, MSG_ID, length, payload, CRC-16 (no start/end bytes needed — SPI is clocked)
- **IRQ line:** STM32 asserts PB3 low to signal data-ready to CM5
- **Timeout:** 500 ms for ACK; retry up to 3 times
- **Critical commands (E_STOP):** No ACK required, acted on immediately

---

## Real-Time Requirements

| Task | Frequency | Deadline | Processor | Priority |
|------|-----------|----------|-----------|----------|
| PID temperature loop | 10 Hz | 100 ms | STM32 | High |
| Motor control (PWM) | 50 Hz | 20 ms | STM32 | Highest |
| Sensor polling (ADC/I2C) | 10 Hz | 100 ms | STM32 | High |
| Safety monitor check | 10 Hz | 100 ms | STM32 | Highest |
| Communication handler | 20 Hz | 50 ms | STM32 | Medium |
| CV inference | 2 Hz | 500 ms | CM5 | Medium |
| UI update (Kivy render) | 30 Hz | 33 ms | CM5 | Medium |
| Recipe engine tick | 1 Hz | 1 s | CM5 | Low |
| Cloud sync (MQTT) | 0.1 Hz | 10 s | CM5 | Low |

---

## Error Handling

### Common Errors

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| Sensor failure (temp/weight) | ADC out-of-range or NaN | CRITICAL | Fall back to timer-based cooking, alert user |
| Communication timeout | No ACK within 500 ms x 3 retries | WARNING → CRITICAL | Retry 3x, then pause cooking, alert user |
| Over-temperature | Temp > 260C (absolute max) | CRITICAL → E_STOP | Immediately cut heater, stop motor, alarm |
| Motor stall | Overcurrent on motor driver | WARNING → CRITICAL | Stop motor, alert user, suggest pot check |
| CV failure | Camera disconnect or TFLite error | WARNING | Fall back to timer + temp thresholds |
| Power anomaly | Voltage/current out of range | CRITICAL | Graceful shutdown, save state to flash |
| Recipe parse error | Invalid YAML or missing fields | WARNING | Reject recipe, notify user, suggest re-download |

### Fallback Strategies

1. **CV fallback:** If camera or model fails, every recipe stage includes `duration_seconds` and `temp_target` as backup transition criteria
2. **Communication fallback:** STM32 operates autonomously with last-known setpoints for up to 30 seconds, then enters safe shutdown
3. **Power loss recovery:** Cooking state saved to SQLite every 10 seconds; on restart, offer to resume or discard

---

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[03-Main-Loop-State-Machine|Main Loop State Machine]]
- [[08-Tech-Stack|Tech Stack]]
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]]

#epicura #software-architecture #controller #firmware #recipe-engine #computer-vision #pid-control #safety #stm32 #raspberry-pi

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |