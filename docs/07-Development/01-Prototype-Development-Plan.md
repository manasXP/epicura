---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Prototype Development Plan

## Overview

This document outlines the comprehensive plan for building a functional Epicura prototype capable of cooking 3-5 Indian recipes autonomously. The prototype will validate core subsystems: induction heating, robotic stirring, computer vision, and recipe state machine execution.

**Target Timeline:** 20-24 weeks
**Goal:** Working prototype demonstrating autonomous one-pot cooking with CV-guided stage detection
**Budget:** $1,500-2,500 (including components, tools, and miscellaneous)

## Project Links

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../03-Software/03-Software-Architecture|Software Architecture]]
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]]

---

## Development Phases

### Phase 1: Hardware Setup & Bring-up (Weeks 1-4)

#### Objectives
- Set up Raspberry Pi CM5 with Yocto Linux image
- Set up STM32G474RE with FreeRTOS
- Establish CM5-to-STM32 communication link
- Validate basic I/O and power supply

#### Tasks

**Week 1: CM5 Bring-up**
- [ ] Acquire CM5 module + IO carrier board
- [ ] Build Yocto image for CM5 (minimal + Python + OpenCV)
- [ ] Flash image to microSD, verify boot
- [ ] Establish SSH access over Ethernet/WiFi
- [ ] Test GPIO, I2C, SPI, UART from Linux userspace
- [ ] Install libcamera and verify CSI-2 camera interface

**Week 2: STM32 Bring-up**
- [ ] Acquire NUCLEO-G474RE development board
- [ ] Install STM32CubeIDE and STM32CubeMX
- [ ] Create FreeRTOS project with basic task structure
- [ ] Test GPIO output (LED blink)
- [ ] Test UART communication (serial terminal echo)
- [ ] Test ADC input (read NTC thermistor voltage)
- [ ] Test PWM output (servo signal generation)

**Week 3: Inter-Processor Communication**
- [ ] Wire UART between CM5 (UART TX/RX) and STM32 (USART2)
- [ ] Define message protocol (header, command ID, payload, CRC)
- [ ] Implement protocol on STM32 (C, interrupt-driven UART)
- [ ] Implement protocol on CM5 (Python, pyserial)
- [ ] Test bidirectional echo: CM5 sends command, STM32 responds
- [ ] Measure round-trip latency (target: < 10 ms)

**Week 4: Power Supply & Integration**
- [ ] Use bench PSU initially (5V/3A for CM5, 6V for servos, 3.3V for STM32)
- [ ] Design power distribution board (or use prototype PSU module)
- [ ] Wire all subsystems to common power rail
- [ ] Verify power consumption under load
- [ ] Stress test: run CM5 + STM32 + servo simultaneously for 1 hour

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| CM5 running Yocto Linux | Boot < 30s, SSH accessible, camera streaming |
| STM32 running FreeRTOS | 4+ tasks running, UART responsive |
| CM5-STM32 link | Bidirectional messaging, < 10 ms round-trip |
| Power distribution | All subsystems powered, no brownouts under load |

**Risks:**
- CM5 Yocto build complexity → Fallback: use Raspberry Pi OS (Debian)
- UART reliability → Fallback: add hardware flow control (RTS/CTS)

---

### Phase 2: Induction Integration (Weeks 5-7)

#### Objectives
- Integrate and control a commercial induction hob
- Implement PID temperature controller on STM32
- Validate temperature accuracy and step response

#### Tasks

**Week 5: Microwave Surface Module Setup**
- [ ] Acquire commercial microwave induction surface with CAN bus port
- [ ] Review module CAN protocol documentation
- [ ] Wire CAN bus: module CAN port ↔ STM32 FDCAN1 (PB8/PB9) + transceiver + 120Ω termination
- [ ] Verify CAN communication: send HEAT_QUERY, receive HEAT_STATUS
- [ ] Wire safety relay on AC mains to module (STM32 GPIO control)

**Week 6: CAN Power Control Integration**
- [ ] Implement CAN power level commands (0-100%) from STM32
- [ ] Verify all power levels (warm, simmer, medium, boil, sear)
- [ ] Measure power delivery at different CAN power levels (25%, 50%, 75%, 100%)
- [ ] Log temperature ramp rates for water (1L, 2L, 3L)
- [ ] Test safety relay disconnect and CAN off command

**Week 7: PID Controller & Sensors**
- [ ] Wire MLX90614 IR thermometer to STM32 I2C bus
- [ ] Wire NTC thermistor (100k) to STM32 ADC via voltage divider
- [ ] Calibrate MLX90614 against reference thermometer (0-250°C range)
- [ ] Implement PID controller on STM32 (FreeRTOS task, 10 Hz loop)
- [ ] Tune PID gains: step response test (ambient → 100°C, 100°C → simmer at 85°C)
- [ ] Validate accuracy: ±10°C at target (prototype), ±5°C goal (optimized)

```
┌─────────────────────────────────────────────────────────┐
│              Induction Control Loop                     │
│                                                         │
│  Target Temp ──► PID ──► Duty Cycle ──► Relay/PWM       │
│       │          ▲                         │            │
│       │          │                         ▼            │
│       │     Error Calc              Induction Coil      │
│       │          │                         │            │
│       │          │                         ▼            │
│       │     ┌────────────┐            ┌────────┐        │
│       │     │ MLX90614   │◄───────────│  Pot   │        │
│       └────►│ IR Sensor  │  (infrared)│        │        │
│             └────────────┘            └────────┘        │
│                                            │            │
│             ┌────────────┐                 │            │
│             │ NTC (coil) │◄────────────────┘            │
│             │ (safety)   │  (conduction)                │
│             └────────────┘                              │
└─────────────────────────────────────────────────────────┘
```

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| Induction control | STM32 can set power 0-100% in 10% steps |
| Temperature sensing | MLX90614 reads pot surface ±5°C of reference |
| PID controller | Reach 100°C in < 8 min (1L water), hold ±10°C |
| Safety cutoff | Auto-off at 200°C coil temp or 240°C thermal fuse |

---

### Phase 3: Arm & Sensors (Weeks 8-10)

#### Objectives
- Build and mount the servo stirring arm
- Integrate load cells for weight measurement
- Implement stirring patterns and weight-verified dispensing preparation

#### Tasks

**Week 8: Servo Arm Assembly**
- [ ] Acquire DS3225 servo motor (25 kg.cm, metal gear)
- [ ] Design mounting bracket (3D print, PETG or aluminum)
- [ ] Fabricate stainless steel shaft (8mm diameter, 250mm length)
- [ ] Attach food-grade silicone paddle to shaft end
- [ ] Mount servo + shaft assembly above pot center
- [ ] Wire servo to STM32 PWM output (TIM1 or TIM2)

**Week 9: Stirring Patterns**
- [ ] Implement 5 stirring patterns on STM32:
  - Circular (continuous rotation, adjustable speed)
  - Back-and-forth (180° sweep)
  - Scraping (edge-following pattern)
  - Folding (slow, deep strokes for delicate mixing)
  - Pulse (intermittent stir, e.g., 5s on / 30s off)
- [ ] Add speed control: 10-60 RPM range
- [ ] Add torque monitoring: detect obstruction via servo current
- [ ] Test all patterns with water, then with thick dal consistency

**Week 10: Load Cells**
- [ ] Install 4x CZL635 load cells in platform (Wheatstone bridge configuration)
- [ ] Wire to HX711 24-bit ADC module
- [ ] Connect HX711 to STM32 SPI/GPIO
- [ ] Calibrate: tare, 500g, 1000g, 2000g, 3000g reference weights
- [ ] Measure accuracy: target ±5g at 500g, ±10g at 3000g
- [ ] Implement weight-change detection for ingredient dispensing feedback

```
┌──────────────────────────────────────────┐
│          Arm & Sensor Assembly           │
│                                          │
│         ┌──────┐                         │
│         │Servo │ DS3225                  │
│         │Motor │ (25 kg.cm)              │
│         └──┬───┘                         │
│            │ Shaft (SS, 8mm)             │
│            │                             │
│            ▼                             │
│     ┌──────────────┐                     │
│     │   Paddle     │ (Silicone)          │
│     └──────────────┘                     │
│            │                             │
│     ┌──────────────┐   ┌─────────────┐   │
│     │     Pot      │   │ MLX90614    │   │
│     │  (3-4L SS)   │   │ IR Sensor   │   │
│     └──────┬───────┘   └─────────────┘   │
│            │                             │
│  ┌─────┐┌─────┐┌─────┐┌─────┐            │
│  │LC 1 ││LC 2 ││LC 3 ││LC 4 │            │
│  └──┬──┘└──┬──┘└──┬──┘└──┬──┘            │
│     └───┬──┘      └───┬──┘               │
│         └──────┬──────┘                  │
│                ▼                         │
│          ┌──────────┐                    │
│          │  HX711   │ 24-bit ADC         │
│          └──────────┘                    │
└──────────────────────────────────────────┘
```

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| Servo arm mounted | Stable mounting, paddle reaches pot bottom |
| 5 stirring patterns | All patterns functional, speed adjustable |
| Load cells calibrated | ±10g accuracy at full range (0-5 kg) |
| Torque limiting | Servo stalls safely at obstruction |

---

### Phase 4: Vision & Computer Vision (Weeks 11-14)

#### Objectives
- Set up overhead camera with controlled illumination
- Build image preprocessing pipeline
- Train and deploy food stage classification model

#### Tasks

**Week 11: Camera Setup**
- [ ] Mount IMX219 camera module above pot (overhead view)
- [ ] Install LED ring (WS2812B, 12-LED NeoPixel) around camera
- [ ] Configure libcamera on CM5 for 1080p @ 30fps capture
- [ ] Implement white balance and exposure control
- [ ] Test image quality under LED illumination (consistent lighting)
- [ ] Capture test images at various cooking stages

**Week 12: Image Preprocessing**
- [ ] Build OpenCV pipeline on CM5 (Python):
  - Color space conversion (BGR → HSV, LAB)
  - Region of interest (ROI) extraction (pot area only)
  - Noise reduction (Gaussian blur, bilateral filter)
  - Color histogram extraction
  - Texture analysis (LBP or Gabor features)
  - Steam/bubble detection (motion analysis)
- [ ] Benchmark pipeline: target < 100 ms per frame on CM5

**Week 13: Training Data Collection**
- [ ] Cook 20+ dishes manually, capturing images every 10 seconds
- [ ] Label images by cooking stage:
  - Raw ingredients
  - Oil heating / tempering
  - Sauteing (browning)
  - Liquid added (boiling)
  - Simmering
  - Thickening
  - Done / ready to serve
- [ ] Augment dataset: rotation, brightness, contrast variations
- [ ] Target: 2,000+ labeled images across 5-7 stage classes

**Week 14: Model Training & Deployment**
- [ ] Transfer learning: MobileNetV2 pretrained on ImageNet
- [ ] Fine-tune on cooking stage dataset (TensorFlow/Keras)
- [ ] Convert to TFLite (quantized INT8 for CM5)
- [ ] Deploy on CM5: inference time target < 200 ms per frame
- [ ] Validate accuracy: target > 85% on held-out test set
- [ ] Implement rule-based fallback (color thresholds + temperature)

```
┌─────────────────────────────────────────────────────┐
│              Vision Pipeline                        │
│                                                     │
│  Camera ──► Preprocess ──► Model ──► Stage Label    │
│  (30fps)    (OpenCV)       (TFLite)   (7 classes)   │
│                │                          │         │
│                ▼                          ▼         │
│         Color Histogram          Recipe State       │
│         Texture Features         Machine Input      │
│         Motion (steam)                              │
│                │                                    │
│                ▼                                    │
│         Rule-Based Fallback                         │
│         (if model confidence < 70%)                 │
└─────────────────────────────────────────────────────┘
```

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| Camera + LED ring | Consistent overhead imaging, no shadows |
| Preprocessing pipeline | < 100 ms/frame, robust ROI extraction |
| Training dataset | 2,000+ labeled images, 5-7 stage classes |
| Deployed TFLite model | > 85% accuracy, < 200 ms inference on CM5 |
| Rule-based fallback | Works when model confidence is low |

---

### Phase 5: Recipe Engine & Dispensing (Weeks 15-17)

#### Objectives
- Define recipe YAML format and implement state machine
- Build ingredient dispensing subsystems (ASD, CID, SLD)
- Validate end-to-end cooking of 3-5 Indian recipes

#### Tasks

**Week 15: Recipe Format & State Machine**
- [ ] Define recipe YAML schema:
  ```yaml
  name: "Dal Tadka"
  servings: 2
  total_time_min: 25
  stages:
    - name: "Heat Oil"
      actions: [heat: {target: 180, mode: sear}]
      detect: {method: cv, class: oil_shimmer}
      timeout_sec: 180
    - name: "Add Tempering"
      actions: [dispense: {subsystem: "ASD", id: 1, weight_g: 5}]
      ...
  ```
- [ ] Implement state machine on CM5 (Python):
  - Load recipe YAML
  - Execute stages sequentially
  - Transition on CV detection OR timeout OR weight confirmation
  - Send commands to STM32 via UART protocol
- [ ] Create recipe files for 5 target dishes

**Week 16: Dispensing Mechanism**
- [ ] Build ASD: 3 seasoning hoppers (3D printed PETG, 80 mL each) with SG90 servo gates
- [ ] Build CID: 2 slide-out trays (400 mL each) with 12V linear actuators and limit switches
- [ ] Build SLD: 2 liquid channels (peristaltic pumps + solenoid valves + silicone tubing)
- [ ] Install SLD dedicated load cell + HX711 under reservoir platform
- [ ] Wire all dispensing actuators to STM32 (PWM + GPIO)
- [ ] Calibrate ASD dispensing: open gate, monitor pot weight, close at target
- [ ] Calibrate SLD dispensing: start pump, monitor reservoir weight loss, stop at target

```
┌──────────────────────────────────────────────────┐
│           Dispensing Subsystem Layout             │
│                                                  │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│   │  ASD-1  │  │  ASD-2  │  │  ASD-3  │         │
│   │(turmeric│  │ (chili  │  │ (salt/  │         │
│   │ powder) │  │ powder) │  │ masala) │         │
│   └────┬────┘  └────┬────┘  └────┬────┘         │
│        │SG90        │SG90        │SG90           │
│        ▼            ▼            ▼               │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─          │
│                                                  │
│   SLD-OIL ═══╗           ╔═══ SLD-WATER          │
│   [Pump]─[Sol]╚══►Pot◄══╝[Sol]─[Pump]           │
│                                                  │
│   ┌──────────────┐  ┌──────────────┐             │
│   │    CID-1     │  │    CID-2     │             │
│   │ (vegetables) │  │  (dal/rice)  │             │
│   │ [LinActuator]│  │ [LinActuator]│             │
│   └──────┬───────┘  └──────┬───────┘             │
│          ▼                 ▼                     │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─          │
│                  Pot Below                       │
└──────────────────────────────────────────────────┘
```

**Week 17: End-to-End Recipe Testing**
- [ ] Test Recipe 1: **Dal Tadka** (lentil curry with tempering)
- [ ] Test Recipe 2: **Jeera Rice** (cumin rice)
- [ ] Test Recipe 3: **Tomato Soup** (simple, CV-friendly color transitions)
- [ ] Test Recipe 4: **Khichdi** (rice + lentil, one-pot)
- [ ] Test Recipe 5: **Vegetable Curry** (mixed vegetables in gravy)
- [ ] Log results: timing, temperature accuracy, CV detections, taste evaluation
- [ ] Iterate on PID gains, stirring patterns, and dispensing calibration

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| Recipe YAML format | 5 recipes defined, schema validated |
| State machine | Executes recipes end-to-end, handles timeouts |
| ASD/CID/SLD subsystems | All actuators functional, no jamming |
| Weight-verified dispensing | ±10% accuracy on dispensed weight |
| 3-5 cooked recipes | Edible output, correct stage transitions |

---

### Phase 6: UI & Companion App (Weeks 18-20)

#### Objectives
- Build touchscreen UI on CM5 with 5 core screens
- Build basic native companion mobile apps (iOS + Android)
- Connect app to CM5 via REST API

#### Tasks

**Week 18: Touchscreen UI**
- [ ] Set up Kivy framework on CM5
- [ ] Implement 5 core screens:
  1. **Home:** Recipe selection grid with images
  2. **Recipe Detail:** Ingredients, servings, estimated time, start button
  3. **Cooking:** Live camera feed, current stage, progress bar, temperature
  4. **Settings:** WiFi, language, spice level, allergen preferences
  5. **History:** Past cook logs with timestamps and results
- [ ] Wire UI events to recipe state machine
- [ ] Display real-time sensor data (temperature, weight, arm status)

**Week 19: Camera Feed & REST API**
- [ ] Embed live camera feed in Cooking screen (MJPEG or V4L2 widget)
- [ ] Overlay CV annotations (stage label, confidence, temperature)
- [ ] Implement REST API on CM5 (Flask or FastAPI):
  - `GET /recipes` - List available recipes
  - `GET /status` - Current cooking state, temperature, stage
  - `POST /cook/start` - Start cooking a recipe
  - `POST /cook/stop` - Emergency stop
  - `GET /camera/stream` - MJPEG camera stream
- [ ] Test API with curl and Postman

**Week 20: Native Companion Mobile Apps**
- [ ] Create native app projects (Swift/SwiftUI for iOS, Kotlin/Compose for Android)
- [ ] Implement 4 screens:
  1. **Discovery:** Find Epicura on local network (mDNS)
  2. **Recipe Browse:** List and detail view from API
  3. **Live Cook:** Camera feed + status from API
  4. **Controls:** Start/stop, spice level adjustment
- [ ] WiFi AP mode pairing flow: CM5 creates AP, app connects, configures home WiFi
- [ ] Test on Android device (physical)

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| Touchscreen UI | 5 screens, responsive touch, camera feed |
| REST API | All endpoints functional, < 500 ms response |
| Native mobile apps | Recipe browse, live camera, start/stop cooking |
| WiFi pairing | AP mode → home WiFi configuration works |

---

### Phase 7: Integration & Testing (Weeks 21-24)

#### Objectives
- Full system integration of all subsystems
- End-to-end cooking validation
- Safety testing and reliability assessment

#### Tasks

**Week 21: Full System Integration**
- [ ] Connect all subsystems into single enclosure/frame
- [ ] Verify wiring: power, UART, I2C, SPI, PWM, servo, relay
- [ ] Run system self-test sequence (each subsystem checks in)
- [ ] End-to-end test: select recipe on UI → cook → complete notification

**Week 22: Cooking Validation**
- [ ] Cook each recipe 5+ times, log all parameters
- [ ] Evaluate results: taste, texture, consistency, timing
- [ ] Identify failure modes and edge cases
- [ ] Tune PID, CV thresholds, and dispensing calibration
- [ ] Test with different pot sizes (2L, 3L, 4L)

**Week 23: Safety Validation**
- [ ] Test all interlocks:
  - Pot removed during cooking → induction off
  - Lid opened → arm stops
  - Overtemperature → auto shutoff
  - Emergency stop button → all off
  - Communication loss → safe stop after 30s
- [ ] Measure external surface temperatures during cooking
- [ ] Test thermal fuse activation (controlled over-temp)
- [ ] Verify watchdog timer recovery on STM32

**Week 24: Reliability & Documentation**
- [ ] 24-hour continuous operation test (cycle through recipes)
- [ ] 50+ cook cycle endurance test
- [ ] Memory leak testing on CM5 (Python processes)
- [ ] Power consumption profiling (average and peak)
- [ ] Bug fixing and optimization
- [ ] Prepare demo: 3 recipes cooked live, camera + UI + app shown
- [ ] Write prototype report and lessons learned

**Deliverables:**

| Deliverable | Success Criteria |
|-------------|-----------------|
| Integrated system | All subsystems in single assembly, working |
| Cooking validation | 5 recipes, 5+ cooks each, consistent results |
| Safety validation | All interlocks verified, no unsafe states |
| Reliability test | 50+ cook cycles without failure |
| Demo & documentation | Live demo ready, prototype report written |

---

## Resource Requirements

| Category | Items | Estimated Cost |
|----------|-------|----------------|
| Compute | CM5 + carrier board + STM32 Nucleo dev board | $200-300 |
| Actuation | DS3225 servo + ASD servos + CID actuators + SLD pumps/solenoids + induction hob | $200-300 |
| Sensors | IMX219 camera + MLX90614 + 4x load cells + NTC + HX711 | $80-120 |
| Mechanical | 3D printing (PETG filament) + stainless steel shaft + fasteners + brackets | $100-200 |
| Display | 10.1" IPS touchscreen (HDMI + I2C touch) | $80-120 |
| Power | Bench PSU + prototype PSU board + cables + connectors | $50-80 |
| Tools | Soldering station + multimeter + oscilloscope + 3D printer access | $100-200 |
| Consumables | Ingredients (20+ cook sessions) + thermal paper + misc | $50-100 |
| Miscellaneous | PCBs (JLCPCB) + shipping + contingency | $200-400 |
| **Total** | | **$1,010-1,770** |

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Induction control difficulty | Medium | High | Start with relay on/off, upgrade to PWM injection; worst case: use commercial hob with manual power setting |
| CV accuracy insufficient | Medium | Medium | Rule-based fallback (color + temperature thresholds); collect more training data; use ensemble of simple classifiers |
| Mechanical assembly issues | Low | Medium | Iterate 3D prints rapidly; consult maker community; use off-the-shelf brackets where possible |
| CM5 performance bottleneck | Low | Medium | Optimize TFLite inference (INT8 quantization); offload preprocessing to GPU; consider Jetson Nano as backup |
| Integration complexity | High | High | Test each subsystem independently before integrating; define clear interfaces (UART protocol, API); CI/CD for CM5 software |
| Servo arm reliability | Medium | Medium | Use metal-gear servo (DS3225); add mechanical end-stops; monitor servo current for early failure detection |
| Recipe state machine bugs | Medium | Medium | Extensive unit testing; timeout fallbacks on every state; manual override via UI |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Component delivery delays | Medium | High | Order early (Week 0); identify backup suppliers; use dev boards initially |
| Yocto build issues | Medium | Medium | Fallback to Raspberry Pi OS; pre-built Yocto images for CM5 may be available |
| Scope creep | Medium | Medium | Strict MVP definition; defer nice-to-haves to post-prototype |
| Testing takes longer than planned | High | Medium | Start testing during development (not only at end); automate where possible |

---

## Success Criteria

### Minimum Viable Prototype (MVP)
- [ ] Cook 3 recipes end-to-end autonomously
- [ ] Temperature control within ±10°C of target
- [ ] Basic touchscreen UI: recipe select, cooking screen, camera feed
- [ ] Safety interlocks functional (pot detect, overtemp shutoff)
- [ ] Dispensing works for all 3 subsystems (ASD, CID, SLD)

### Should-Have
- [ ] 5 recipes validated with consistent results
- [ ] CV-guided cooking stage detection (> 80% accuracy)
- [ ] Mobile app with basic functionality (browse, live view, start/stop)
- [ ] Temperature accuracy ±5°C
- [ ] Weight-verified dispensing (±10% accuracy)

### Nice-to-Have
- [ ] 10+ recipes in library
- [ ] Cloud sync for recipe updates
- [ ] Multi-language UI (English + Hindi)
- [ ] Auto-rinse cycle between recipes
- [ ] Voice notifications during cooking

---

## Budget Summary

| Category | Estimated Cost |
|----------|---------------|
| Electronic Components (BOM) | $614 |
| Tools & Equipment | $100-200 |
| 3D Printing & Mechanical | $100-200 |
| Consumables (ingredients, filament) | $50-100 |
| PCB Fabrication | $40-80 |
| Shipping & Miscellaneous | $100-200 |
| Contingency (+20%) | $200-400 |
| **Total Project Budget** | **$1,500-2,500** |

---

## Next Steps After Prototype

### Alpha Phase Preparation
- Identify improvements from prototype testing
- Design custom carrier PCB (combine CM5 + STM32 + power on single board)
- Plan injection-molded enclosure design
- Begin BIS certification process (India)

### Production Planning
- Finalize component selection for long-term availability
- Design custom induction driver board (replace teardown hob)
- Establish supplier relationships (volume pricing)
- Target production unit cost: $200-250

---

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../03-Software/03-Software-Architecture|Software Architecture]]
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]]
- [[../08-Components/01-Compute-Module-Components|Compute Module Components]]
- [[../08-Components/02-Actuation-Components|Actuation Components]]
- [[../08-Components/03-Sensor-Components|Sensor Components]]
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]]

---

#epicura #development #prototype #roadmap

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
