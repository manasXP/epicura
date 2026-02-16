---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# User Stories & Technical Stories

## Overview

This document contains all user stories and technical stories organized by epic. Stories follow standard Agile format with acceptance criteria, story points, and dependencies.

**Story Point Scale:** Fibonacci (1, 2, 3, 5, 8, 13)
- 1 point = ~4 hours
- 2 points = ~1 day
- 3 points = ~1.5 days
- 5 points = ~2-3 days
- 8 points = ~4-5 days
- 13 points = ~1 week (consider splitting)

---

## Epic 1: Foundation Infrastructure (EP-001)

### ST-001: CM5 Yocto Build and Setup

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 1

#### Description
As a developer, I need to build and deploy a Yocto Linux image on the Raspberry Pi CM5 so that we have a stable, customized OS foundation for the Epicura software stack.

#### Acceptance Criteria
- [ ] Yocto build environment configured on development machine
- [ ] Minimal Yocto image built with Python 3.11+, OpenCV 4.8+, libcamera
- [ ] Image flashed to microSD card
- [ ] CM5 boots in <30 seconds
- [ ] SSH access established over Ethernet or WiFi
- [ ] GPIO, I2C, SPI, UART accessible from userspace
- [ ] CSI-2 camera interface verified with test capture

#### Technical Notes
- Use Kirkstone or Scarthgap Yocto release
- Create custom BSP layer for CM5
- Include Python, OpenCV, libcamera, GStreamer in image recipe

#### Dependencies
- CM5 module + CM5IO carrier board procured
- Development workstation with 100GB+ free space

---

### ST-002: STM32 FreeRTOS Setup

**Story Type:** Technical
**Story Points:** 5
**Priority:** P0 (Critical)
**Sprint:** Sprint 1

#### Description
As a developer, I need to set up the STM32G474RE with FreeRTOS and basic task structure so that we have a real-time control foundation for sensors and actuators.

#### Acceptance Criteria
- [ ] STM32CubeIDE and STM32CubeMX installed
- [ ] FreeRTOS project created with 4 tasks: PID (100Hz), Servo (50Hz), Sensor (10Hz), Comms (20Hz)
- [ ] LED blink test successful (GPIO output)
- [ ] UART echo test successful (serial terminal)
- [ ] ADC reading test successful (NTC thermistor voltage)
- [ ] PWM output test successful (servo signal generation)
- [ ] Task scheduling verified with logic analyzer

#### Technical Notes
- Use STM32 HAL drivers
- Configure system clock for 170MHz
- Allocate heap for FreeRTOS tasks

#### Dependencies
- NUCLEO-G474RE development board procured
- ST-Link debugger functional

---

### ST-003: UART Communication Protocol

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 1

#### Description
As a developer, I need to implement a reliable UART protocol between CM5 and STM32 so that the recipe engine can command the controller and receive sensor data.

#### Acceptance Criteria
- [ ] Protocol specification documented (header, command ID, payload length, CRC16)
- [ ] STM32 C implementation: interrupt-driven UART RX/TX
- [ ] CM5 Python implementation using pyserial
- [ ] Bidirectional echo test: CM5 sends command, STM32 responds with ACK
- [ ] Round-trip latency measured at <10ms
- [ ] Error handling: timeouts, CRC failures, retries
- [ ] At least 10 command types defined (heat, stir, dispense, query, etc.)

#### Technical Notes
```
Message Format:
[SYNC:2][CMD:1][LEN:2][PAYLOAD:0-255][CRC16:2]
SYNC = 0xAA55
```

#### Dependencies
- ST-001 (CM5 setup)
- ST-002 (STM32 setup)
- UART wiring between CM5 and STM32

---

### ST-004: Power Distribution

**Story Type:** Technical
**Story Points:** 5
**Priority:** P0 (Critical)
**Sprint:** Sprint 2

#### Description
As a developer, I need to design and implement a stable power distribution system so that all subsystems receive clean, regulated power under load.

#### Acceptance Criteria
- [ ] Power requirements calculated for all subsystems
- [ ] Bench PSU configuration documented (5V/3A for CM5, 6V for servos, 3.3V for STM32)
- [ ] Power distribution wiring diagram created
- [ ] All subsystems powered simultaneously
- [ ] Power consumption measured under load
- [ ] Stress test: 1-hour continuous operation with no brownouts
- [ ] Voltage ripple <100mV on all rails

#### Technical Notes
- Initial: bench PSU with multiple outputs
- Later: Mean Well LRS-75-24 with buck converters

#### Dependencies
- All major components procured

---

## Epic 2: Thermal Control System (EP-002)

### ST-005: CAN Bus Integration with Induction Module

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 2

#### Description
As a developer, I need to integrate the commercial microwave induction surface via CAN bus so that the STM32 can programmatically control heating power.

#### Acceptance Criteria
- [ ] CAN bus wiring: module ↔ STM32 FDCAN1 (PB8/PB9) with transceiver and 120Ω termination
- [ ] CAN protocol documentation reviewed and understood
- [ ] STM32 FDCAN driver configured and tested
- [ ] Successfully send HEAT_QUERY command and receive HEAT_STATUS response
- [ ] Power level control: 0-100% in 10% increments
- [ ] Safety relay wired to AC mains (STM32 GPIO control)
- [ ] Emergency off command functional

#### Technical Notes
- CAN bus speed: 500 kbps
- Use TJA1050 or similar CAN transceiver

#### Dependencies
- ST-002 (STM32 platform)
- Commercial microwave induction module procured

---

### ST-006: PID Controller Implementation

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 3

#### Description
As a developer, I need to implement a PID temperature controller on STM32 so that the system can accurately maintain target cooking temperatures.

#### Acceptance Criteria
- [ ] PID algorithm implemented in FreeRTOS task (10Hz loop)
- [ ] Configurable gains: Kp, Ki, Kd (defaults: 2.0, 0.5, 0.1)
- [ ] Anti-windup mechanism for integral term
- [ ] Output mapped to CAN power level (0-100%)
- [ ] Step response test: ambient → 100°C
- [ ] Setpoint tracking test: 100°C → 85°C simmer
- [ ] Target accuracy achieved: ±10°C (prototype), goal ±5°C
- [ ] Tuning documentation created

#### Technical Notes
```c
output = Kp * error + Ki * integral + Kd * derivative
integral += error * dt (with anti-windup)
derivative = (error - prev_error) / dt
```

#### Dependencies
- ST-005 (CAN control)
- ST-007 (temperature sensor)

---

### ST-007: IR Temperature Sensor Integration

**Story Type:** Technical
**Story Points:** 5
**Priority:** P0 (Critical)
**Sprint:** Sprint 3

#### Description
As a developer, I need to integrate the MLX90614 IR thermometer so that the system can measure pot surface temperature for PID control.

#### Acceptance Criteria
- [ ] MLX90614 wired to STM32 I2C bus
- [ ] I2C driver configured and tested
- [ ] Temperature reading function implemented
- [ ] Calibration performed against reference thermometer (0-250°C range)
- [ ] Accuracy verified: ±5°C of reference across operating range
- [ ] NTC thermistor wired to ADC for coil temperature monitoring
- [ ] Both sensors logged simultaneously at 10Hz

#### Technical Notes
- MLX90614 I2C address: 0x5A (default)
- Emissivity correction may be needed for different pot materials

#### Dependencies
- ST-002 (STM32 I2C interface)
- MLX90614 and NTC thermistor procured

---

### ST-008: Safety Interlocks

**Story Type:** Technical
**Story Points:** 5
**Priority:** P0 (Critical)
**Sprint:** Sprint 3

#### Description
As a user, I want the system to automatically shut off heating in unsafe conditions so that I am protected from burns, fire, or equipment damage.

#### Acceptance Criteria
- [ ] Overtemperature cutoff: induction off at 200°C coil temp
- [ ] Thermal fuse installed (240°C)
- [ ] Safety relay on AC mains controlled by STM32 GPIO
- [ ] Emergency stop button wired and functional
- [ ] Watchdog timer configured on STM32
- [ ] Communication loss detection: safe stop after 30s
- [ ] All interlocks tested individually

#### Technical Notes
- Use fail-safe relay design (relay must be energized to enable heating)

#### Dependencies
- ST-005 (CAN control)
- ST-007 (temperature sensing)

---

## Epic 3: Robotic Manipulation (EP-003)

### ST-009: Servo Arm Assembly

**Story Type:** Technical
**Story Points:** 5
**Priority:** P1 (High)
**Sprint:** Sprint 4

#### Description
As a developer, I need to build and mount the servo stirring arm so that the system can automatically stir food during cooking.

#### Acceptance Criteria
- [ ] DS3225 servo motor acquired (25 kg·cm, metal gear)
- [ ] Mounting bracket designed and 3D printed (PETG) or machined (aluminum)
- [ ] Stainless steel shaft fabricated (8mm diameter, 250mm length)
- [ ] Food-grade silicone paddle attached to shaft end
- [ ] Servo + shaft assembly mounted above pot center
- [ ] Servo wired to STM32 PWM output (TIM1 or TIM2)
- [ ] Mechanical stability verified: no wobble during operation
- [ ] Paddle reaches pot bottom when lowered

#### Technical Notes
- Shaft must be food-grade stainless steel (SS304 or SS316)
- Mounting must withstand repeated stirring torque

#### Dependencies
- Mechanical design files
- 3D printer or machine shop access

---

### ST-010: Stirring Pattern Implementation

**Story Type:** Technical
**Story Points:** 8
**Priority:** P1 (High)
**Sprint:** Sprint 4

#### Description
As a user, I want the robot to use different stirring patterns so that food is mixed properly without burning or sticking.

#### Acceptance Criteria
- [ ] 5 stirring patterns implemented on STM32:
  - Circular: continuous rotation, adjustable speed (10-60 RPM)
  - Back-and-forth: 180° sweep
  - Scraping: edge-following pattern
  - Folding: slow, deep strokes for delicate mixing
  - Pulse: intermittent stir (e.g., 5s on / 30s off)
- [ ] Speed control: 10-60 RPM range
- [ ] Torque monitoring via servo current sensing
- [ ] Obstruction detection: stall detection and safe stop
- [ ] All patterns tested with water
- [ ] All patterns tested with thick dal consistency

#### Technical Notes
- Use servo position feedback where available
- Monitor current draw to detect stalling

#### Dependencies
- ST-009 (servo arm mounted)

---

### ST-011: Load Cell Integration

**Story Type:** Technical
**Story Points:** 8
**Priority:** P1 (High)
**Sprint:** Sprint 5

#### Description
As a developer, I need to integrate load cells for weight measurement so that ingredient dispensing can be verified.

#### Acceptance Criteria
- [ ] 4x CZL635 load cells installed in platform (Wheatstone bridge)
- [ ] HX711 24-bit ADC module wired to STM32 SPI/GPIO
- [ ] Load cell reading function implemented
- [ ] Calibration performed with reference weights: 0g, 500g, 1000g, 2000g, 3000g
- [ ] Accuracy measured: ±5g at 500g, ±10g at 3000g
- [ ] Tare function implemented
- [ ] Weight-change detection for dispensing feedback
- [ ] Data logged at 10Hz

#### Technical Notes
- Platform must be mechanically stable to avoid vibration noise
- Use median filter to reduce noise

#### Dependencies
- Load cells and HX711 procured
- Mechanical platform fabricated

---

### ST-012: Weight-Based Dispensing Preparation

**Story Type:** Technical
**Story Points:** 3
**Priority:** P1 (High)
**Sprint:** Sprint 5

#### Description
As a developer, I need to prepare weight-based dispensing control logic so that ingredients can be metered accurately in the recipe engine.

#### Acceptance Criteria
- [ ] Weight monitoring algorithm implemented
- [ ] Dispensing state machine defined: idle → opening → dispensing → closing → verify
- [ ] Target weight comparison logic
- [ ] Timeout handling if weight doesn't change
- [ ] Integration test: simulate dispensing with manual weight addition
- [ ] Accuracy target: ±10% on dispensed weight

#### Technical Notes
- Will be fully integrated with dispensing mechanism in EP-005

#### Dependencies
- ST-011 (load cells functional)

---

## Epic 4: Computer Vision System (EP-004)

### ST-013: Camera and Lighting Setup

**Story Type:** Technical
**Story Points:** 5
**Priority:** P1 (High)
**Sprint:** Sprint 6

#### Description
As a developer, I need to set up the overhead camera with controlled illumination so that CV can analyze food consistently.

#### Acceptance Criteria
- [ ] IMX219 camera module mounted above pot (overhead view)
- [ ] LED ring installed around camera (WS2812B, 12-LED NeoPixel)
- [ ] libcamera configured on CM5 for 1080p @ 30fps capture
- [ ] White balance and exposure control implemented
- [ ] Image quality verified under LED illumination (consistent lighting)
- [ ] Test images captured at various cooking stages
- [ ] CSI-2 ribbon cable length verified (<150mm for signal integrity)

#### Technical Notes
- Use diffuser on LED ring to eliminate hot spots
- Fixed exposure settings for consistency

#### Dependencies
- ST-001 (CM5 platform with libcamera)
- Camera and LED components procured

---

### ST-014: Image Preprocessing Pipeline

**Story Type:** Technical
**Story Points:** 8
**Priority:** P1 (High)
**Sprint:** Sprint 6

#### Description
As a developer, I need to build an image preprocessing pipeline so that raw camera images are converted into features suitable for ML inference.

#### Acceptance Criteria
- [ ] OpenCV pipeline implemented in Python on CM5:
  - Color space conversion (BGR → HSV, LAB)
  - ROI extraction (pot area only)
  - Noise reduction (Gaussian blur, bilateral filter)
  - Color histogram extraction
  - Texture analysis (LBP or Gabor features)
  - Steam/bubble detection (motion analysis)
- [ ] Pipeline benchmarked: <100ms per frame on CM5
- [ ] Output data structure defined for model input
- [ ] Unit tests for each preprocessing step

#### Technical Notes
- Use OpenCV with NumPy for efficiency
- Consider GPU acceleration if available

#### Dependencies
- ST-013 (camera functional)

---

### ST-015: Training Data Collection

**Story Type:** Technical
**Story Points:** 13
**Priority:** P1 (High)
**Sprint:** Sprint 7

#### Description
As a developer, I need to collect and label a comprehensive dataset of cooking images so that the CV model can learn to recognize cooking stages.

#### Acceptance Criteria
- [ ] 20+ dishes cooked manually
- [ ] Images captured every 10 seconds during cooking
- [ ] All images labeled by cooking stage:
  - Raw ingredients
  - Oil heating / tempering
  - Sauteing (browning)
  - Liquid added (boiling)
  - Simmering
  - Thickening
  - Done / ready to serve
- [ ] Dataset augmented: rotation, brightness, contrast variations
- [ ] Target achieved: 2,000+ labeled images across 5-7 stage classes
- [ ] Dataset split: 70% train, 15% validation, 15% test
- [ ] Data stored in organized directory structure

#### Technical Notes
- Use LabelImg or similar tool for labeling
- Document lighting conditions and camera settings

#### Dependencies
- ST-013 (camera setup)
- Ingredients for 20+ cook sessions

---

### ST-016: Model Training and Deployment

**Story Type:** Technical
**Story Points:** 13
**Priority:** P1 (High)
**Sprint:** Sprint 7

#### Description
As a developer, I need to train and deploy a food stage classification model so that the system can autonomously detect cooking progress.

#### Acceptance Criteria
- [ ] Transfer learning setup: MobileNetV2 pretrained on ImageNet
- [ ] Model fine-tuned on cooking stage dataset (TensorFlow/Keras)
- [ ] Training metrics logged: accuracy, loss, confusion matrix
- [ ] Model converted to TFLite with INT8 quantization
- [ ] TFLite model deployed on CM5
- [ ] Inference time measured: <200ms per frame
- [ ] Validation accuracy achieved: >85% on test set
- [ ] Rule-based fallback implemented (color thresholds + temperature)
- [ ] Confidence threshold tuning (min 70% for CV-based transitions)

#### Technical Notes
- Use TensorFlow Lite converter with representative dataset for quantization
- Monitor for overfitting during training

#### Dependencies
- ST-015 (training dataset)
- GPU workstation for training (optional but recommended)

---

## Epic 5: Recipe Orchestration (EP-005)

### ST-017: Recipe YAML Format

**Story Type:** Technical
**Story Points:** 5
**Priority:** P0 (Critical)
**Sprint:** Sprint 8

#### Description
As a developer, I need to define a structured recipe YAML format so that recipes can be easily authored and parsed by the state machine.

#### Acceptance Criteria
- [ ] YAML schema documented with examples
- [ ] Schema includes: name, servings, total_time, stages, actions, detection methods
- [ ] 5 recipe files created: Dal Tadka, Jeera Rice, Tomato Soup, Khichdi, Vegetable Curry
- [ ] YAML parser implemented in Python
- [ ] Validation logic for required fields
- [ ] Unit tests for parser

#### Example Schema
```yaml
name: "Dal Tadka"
servings: 2
total_time_min: 25
stages:
  - name: "Heat Oil"
    actions:
      - type: heat
        target: 180
        mode: sear
    detect:
      method: cv
      class: oil_shimmer
    timeout_sec: 180
  - name: "Add Tempering"
    actions:
      - type: dispense
        subsystem: "ASD"
        id: 1
        weight_g: 5
    detect:
      method: weight
      min_change_g: 10
    timeout_sec: 30
```

#### Dependencies
- None (foundational)

---

### ST-018: State Machine Engine

**Story Type:** Technical
**Story Points:** 13
**Priority:** P0 (Critical)
**Sprint:** Sprint 8

#### Description
As a developer, I need to implement a recipe state machine engine so that recipes execute autonomously with proper stage transitions.

#### Acceptance Criteria
- [ ] State machine implemented in Python on CM5
- [ ] Load recipe YAML and parse into stages
- [ ] Execute stages sequentially
- [ ] Transition logic: CV detection OR timeout OR weight confirmation
- [ ] Send commands to STM32 via UART (heat, stir, dispense)
- [ ] Receive sensor data from STM32 (temperature, weight)
- [ ] Logging of all state transitions and actions
- [ ] Error handling and recovery
- [ ] Manual override capability via UI
- [ ] End-to-end test with simple 2-stage recipe

#### Technical Notes
- Use asyncio for concurrent sensor monitoring and state execution

#### Dependencies
- ST-003 (UART protocol)
- ST-017 (recipe format)

---

### ST-019: Dispensing Mechanism

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 9

#### Description
As a user, I want the robot to automatically dispense ingredients in precise amounts so that recipes are cooked consistently.

#### Acceptance Criteria
- [ ] ASD: 3 seasoning hoppers built (80 mL each, 3D printed PETG) with SG90 servo gates
- [ ] CID: 2 slide-out trays built (400 mL each) with 12V linear actuators + limit switches
- [ ] SLD: 2 liquid channels built (peristaltic pumps + solenoid valves + silicone tubing)
- [ ] SLD: dedicated load cell + HX711 installed under reservoir platform
- [ ] All actuators wired to STM32 (PWM + GPIO)
- [ ] ASD calibration: open gate → monitor pot weight → close at target ±10%
- [ ] SLD calibration: start pump → monitor reservoir weight loss → stop at target ±5%
- [ ] All subsystems tested individually
- [ ] Integration test: dispense from ASD, CID, and SLD sequentially

#### Technical Notes
- Gate design must prevent ingredient bridging or jamming

#### Dependencies
- ST-011 (load cells)
- ST-012 (weight-based control logic)
- 3D printer access

---

### ST-020: Recipe Testing and Validation

**Story Type:** Technical
**Story Points:** 13
**Priority:** P0 (Critical)
**Sprint:** Sprint 9

#### Description
As a product owner, I want to validate that 5 recipes cook successfully end-to-end so that we confirm the core product value proposition.

#### Acceptance Criteria
- [ ] Recipe 1 tested: Dal Tadka (lentil curry with tempering)
- [ ] Recipe 2 tested: Jeera Rice (cumin rice)
- [ ] Recipe 3 tested: Tomato Soup (simple, CV-friendly color transitions)
- [ ] Recipe 4 tested: Khichdi (rice + lentil, one-pot)
- [ ] Recipe 5 tested: Vegetable Curry (mixed vegetables in gravy)
- [ ] All recipes produce edible output
- [ ] Timing accuracy within ±10% of expected
- [ ] Temperature control within ±10°C
- [ ] CV stage transitions occur correctly
- [ ] Results logged: timing, temperature, CV detections, taste evaluation
- [ ] PID gains, stirring patterns, dispensing calibration iterated based on results

#### Technical Notes
- Conduct taste tests with at least 2 people
- Document failure modes

#### Dependencies
- ST-018 (state machine)
- ST-019 (dispensing)
- All subsystems operational

---

## Epic 6: User Interface (EP-006)

### ST-021: Touchscreen UI Implementation

**Story Type:** User Story
**Story Points:** 13
**Priority:** P1 (High)
**Sprint:** Sprint 9-10

#### Description
As a user, I want a touchscreen interface so that I can select recipes, monitor cooking, and adjust settings without using a mobile app.

#### Acceptance Criteria
- [ ] Kivy framework set up on CM5
- [ ] 5 core screens implemented:
  1. **Home:** Recipe selection grid with images
  2. **Recipe Detail:** Ingredients, servings, estimated time, start button
  3. **Cooking:** Live camera feed, current stage, progress bar, temperature
  4. **Settings:** WiFi, language, spice level, allergen preferences
  5. **History:** Past cook logs with timestamps and results
- [ ] UI events wired to recipe state machine
- [ ] Real-time sensor data displayed (temperature, weight, arm status)
- [ ] Touch responsiveness <100ms
- [ ] Visual design polished (fonts, colors, icons)

#### Technical Notes
- Use Kivy for Python-native widgets and camera integration

#### Dependencies
- ST-001 (CM5 platform)
- 10" touchscreen display procured
- ST-018 (state machine for integration)

---

### ST-022: REST API Development

**Story Type:** Technical
**Story Points:** 8
**Priority:** P1 (High)
**Sprint:** Sprint 10

#### Description
As a mobile app developer, I need a REST API so that the Flutter app can communicate with the Epicura device.

#### Acceptance Criteria
- [ ] Flask or FastAPI server implemented on CM5
- [ ] API endpoints functional:
  - `GET /recipes` - List available recipes
  - `GET /status` - Current cooking state, temperature, stage
  - `POST /cook/start` - Start cooking a recipe
  - `POST /cook/stop` - Emergency stop
  - `GET /camera/stream` - MJPEG camera stream
  - `GET /history` - Past cook logs
  - `POST /settings` - Update preferences
- [ ] API response time <500ms
- [ ] Error handling and status codes
- [ ] API tested with curl and Postman
- [ ] API documentation generated (Swagger/OpenAPI)

#### Technical Notes
- Use CORS headers for web access
- Consider authentication for production

#### Dependencies
- ST-001 (CM5 platform)
- ST-018 (state machine)

---

### ST-023: Flutter Mobile App

**Story Type:** User Story
**Story Points:** 13
**Priority:** P2 (Medium)
**Sprint:** Sprint 10

#### Description
As a user, I want a mobile app so that I can browse recipes and monitor cooking remotely from my phone.

#### Acceptance Criteria
- [ ] Flutter project created (Android + iOS support)
- [ ] 4 screens implemented:
  1. **Discovery:** Find Epicura on local network (mDNS)
  2. **Recipe Browse:** List and detail view from API
  3. **Live Cook:** Camera feed + status from API
  4. **Controls:** Start/stop, spice level adjustment
- [ ] API integration functional (HTTP client)
- [ ] MJPEG camera stream rendering
- [ ] Real-time status updates (polling or WebSocket)
- [ ] App tested on Android physical device
- [ ] Basic error handling and offline states

#### Technical Notes
- Use http or dio package for API calls
- Consider flutter_webrtc for camera streaming (future)

#### Dependencies
- ST-022 (REST API)
- Flutter development environment

---

### ST-024: WiFi Pairing Flow

**Story Type:** User Story
**Story Points:** 8
**Priority:** P2 (Medium)
**Sprint:** Sprint 10

#### Description
As a user, I want to easily connect Epicura to my home WiFi so that I can use the mobile app.

#### Acceptance Criteria
- [ ] CM5 creates WiFi AP mode on first boot (SSID: "Epicura-XXXX")
- [ ] Mobile app detects AP and prompts user to connect
- [ ] App presents WiFi configuration screen
- [ ] User enters home WiFi credentials
- [ ] Credentials sent to CM5 via REST API
- [ ] CM5 connects to home WiFi and disables AP mode
- [ ] App discovers device on home network via mDNS
- [ ] Pairing flow tested end-to-end

#### Technical Notes
- Use NetworkManager on CM5 for WiFi control
- Store credentials securely

#### Dependencies
- ST-022 (REST API)
- ST-023 (Flutter app)

---

## Epic 7: Integration & Validation (EP-007)

### ST-025: Full System Integration

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 11

#### Description
As a developer, I need to integrate all subsystems into a single assembly so that the prototype operates as a cohesive unit.

#### Acceptance Criteria
- [ ] All subsystems connected in single enclosure/frame
- [ ] Wiring verified: power, UART, I2C, SPI, PWM, servo, relay
- [ ] System self-test sequence implemented (each subsystem checks in)
- [ ] End-to-end smoke test: select recipe on UI → cook → complete notification
- [ ] All sensors reporting data correctly
- [ ] No mechanical interference between components
- [ ] Cable management organized and secure

#### Technical Notes
- Create wiring diagram for assembly documentation

#### Dependencies
- All previous epics (EP-001 through EP-006)
- Mechanical enclosure/frame fabricated

---

### ST-026: Cooking Validation

**Story Type:** Technical
**Story Points:** 13
**Priority:** P0 (Critical)
**Sprint:** Sprint 11

#### Description
As a product owner, I need comprehensive cooking validation so that we can verify recipe quality and consistency.

#### Acceptance Criteria
- [ ] Each of 5 recipes cooked 5+ times
- [ ] Results logged for every cook: timing, temperature profile, CV transitions, weight measurements
- [ ] Taste evaluation performed (2+ tasters per recipe)
- [ ] Texture and consistency evaluated
- [ ] Failure modes documented
- [ ] Edge cases identified (e.g., different pot sizes, ingredient variations)
- [ ] PID tuning adjusted based on results
- [ ] CV thresholds optimized
- [ ] Dispensing calibration refined
- [ ] Success rate: >80% of cooks produce acceptable results

#### Technical Notes
- Use 2L, 3L, 4L pot sizes for variety testing

#### Dependencies
- ST-025 (integrated system)
- Ingredients for 25+ cook sessions

---

### ST-027: Safety Testing

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Sprint:** Sprint 12

#### Description
As a product owner, I need comprehensive safety testing so that we can ensure the prototype meets safety requirements before alpha phase.

#### Acceptance Criteria
- [ ] All interlocks tested:
  - Pot removed during cooking → induction off immediately
  - Lid opened → arm stops immediately
  - Overtemperature (200°C coil) → auto shutoff
  - Emergency stop button → all actuators off immediately
  - Communication loss (CM5-STM32) → safe stop after 30s
- [ ] External surface temperatures measured during cooking (<60°C on accessible surfaces)
- [ ] Thermal fuse activation tested (controlled over-temp scenario)
- [ ] STM32 watchdog timer recovery tested
- [ ] All tests passed without failures
- [ ] Safety test report documented

#### Technical Notes
- Use thermal camera for surface temperature mapping

#### Dependencies
- ST-025 (integrated system)

---

### ST-028: Reliability Testing

**Story Type:** Technical
**Story Points:** 13
**Priority:** P0 (Critical)
**Sprint:** Sprint 12

#### Description
As a product owner, I need reliability testing so that we can assess MTBF (Mean Time Between Failures) and identify weak points.

#### Acceptance Criteria
- [ ] 24-hour continuous operation test completed (cycle through recipes)
- [ ] 50+ cook cycle endurance test completed
- [ ] Memory leak testing on CM5 (Python processes monitored)
- [ ] Power consumption profiled (average and peak) across all recipes
- [ ] No critical failures during testing
- [ ] Any non-critical failures documented with root cause analysis
- [ ] MTBF estimate calculated
- [ ] Component wear assessment (servo, relay, load cells)

#### Technical Notes
- Use system monitoring tools (htop, free, iotop) on CM5
- Log power consumption with power meter

#### Dependencies
- ST-025 (integrated system)

---

### ST-029: Demo Preparation and Documentation

**Story Type:** Technical
**Story Points:** 8
**Priority:** P1 (High)
**Sprint:** Sprint 12

#### Description
As a product owner, I need a polished demo and comprehensive documentation so that we can present the prototype to stakeholders and prepare for alpha phase.

#### Acceptance Criteria
- [ ] Live demo script prepared: cook 3 recipes sequentially
- [ ] Demo includes: touchscreen UI, camera feed, mobile app, all subsystems
- [ ] Video recording of full cook cycle for each demo recipe
- [ ] Prototype report written covering:
  - System architecture
  - Subsystem performance metrics
  - Cooking validation results
  - Safety test results
  - Reliability assessment
  - Lessons learned
  - Recommendations for alpha phase
- [ ] BOM with actual costs
- [ ] Assembly documentation with photos
- [ ] Known issues and limitations documented

#### Technical Notes
- Prepare backup plan for demo (pre-recorded video if live fails)

#### Dependencies
- ST-026 (cooking validation)
- ST-027 (safety testing)
- ST-028 (reliability testing)

---

## Story Summary by Epic

| Epic | Total Stories | Total Story Points | Avg Points/Story |
|------|---------------|-------------------|------------------|
| EP-001: Foundation | 4 | 26 | 6.5 |
| EP-002: Thermal Control | 4 | 26 | 6.5 |
| EP-003: Robotic Manipulation | 4 | 24 | 6.0 |
| EP-004: Computer Vision | 4 | 39 | 9.8 |
| EP-005: Recipe Orchestration | 4 | 39 | 9.8 |
| EP-006: User Interface | 4 | 42 | 10.5 |
| EP-007: Integration & Validation | 5 | 50 | 10.0 |
| **Total** | **29** | **246** | **8.5** |

---

## Priority Distribution

| Priority | Count | Percentage |
|----------|-------|------------|
| P0 (Critical) | 14 | 48% |
| P1 (High) | 12 | 41% |
| P2 (Medium) | 3 | 11% |

---

## Related Documentation

- [[01-Epics|Epics]]
- [[03-Sprints|Sprint Planning]]
- [[../07-Development/01-Prototype-Development-Plan|Prototype Development Plan]]

---

#epicura #userstories #projectmanagement #agile
---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |