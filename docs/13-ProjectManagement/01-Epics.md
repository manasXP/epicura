---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Epics

## Overview

This document defines the major epics for Epicura prototype development. Each epic represents a significant feature area or system component that delivers measurable value.

---

## Epic 1: Foundation Infrastructure

**Epic ID:** EP-001
**Priority:** Critical
**Timeline:** Sprints 1-2 (Weeks 1-4)
**Status:** Not Started

### Description
Establish the core hardware and software infrastructure including CM5 compute module, STM32 controller, inter-processor communication, and power distribution.

### Business Value
Without this foundation, no other subsystems can be developed or integrated. This epic establishes the architectural backbone of the entire system.

### Success Criteria
- [ ] CM5 running Yocto Linux with SSH access
- [ ] STM32 running FreeRTOS with 4+ tasks
- [ ] Bidirectional UART communication <10ms latency
- [ ] Stable power distribution under full load
- [ ] CSI-2 camera interface validated

### Dependencies
- Component procurement (CM5, STM32 Nucleo, power supplies)
- Development tools setup (STM32CubeIDE, Yocto build environment)

### Related Stories
- [[02-Stories#ST-001|ST-001: CM5 Yocto Build]]
- [[02-Stories#ST-002|ST-002: STM32 FreeRTOS Setup]]
- [[02-Stories#ST-003|ST-003: UART Communication Protocol]]
- [[02-Stories#ST-004|ST-004: Power Distribution]]

---

## Epic 2: Thermal Control System

**Epic ID:** EP-002
**Priority:** Critical
**Timeline:** Sprints 3-4 (Weeks 5-7)
**Status:** Not Started

### Description
Integrate commercial microwave induction surface with CAN bus control, implement PID temperature controller, and validate accurate temperature sensing and regulation.

### Business Value
Precise temperature control is fundamental to cooking quality. This epic enables the robot to execute complex cooking techniques requiring specific heat levels (simmering, searing, boiling).

### Success Criteria
- [ ] CAN bus communication with induction module operational
- [ ] PID controller achieving ±10°C accuracy (prototype target)
- [ ] MLX90614 IR sensor calibrated and reading accurately
- [ ] Safety relay and thermal cutoffs functional
- [ ] Water boil test: 1L → 100°C in <8 minutes

### Dependencies
- EP-001 (STM32 platform ready)
- Commercial induction module procurement
- CAN transceiver hardware

### Related Stories
- [[02-Stories#ST-005|ST-005: CAN Bus Integration]]
- [[02-Stories#ST-006|ST-006: PID Controller Implementation]]
- [[02-Stories#ST-007|ST-007: IR Temperature Sensor]]
- [[02-Stories#ST-008|ST-008: Safety Interlocks]]

---

## Epic 3: Robotic Manipulation

**Epic ID:** EP-003
**Priority:** High
**Timeline:** Sprints 4-5 (Weeks 8-10)
**Status:** Not Started

### Description
Build and integrate the servo-driven stirring arm with multiple motion patterns, and implement load cell-based weighing system for ingredient verification.

### Business Value
Automated stirring prevents burning and ensures even cooking. Weight measurement enables precise ingredient dispensing critical for recipe consistency.

### Success Criteria
- [ ] Servo arm mounted and mechanically stable
- [ ] 5 stirring patterns implemented (circular, sweep, scrape, fold, pulse)
- [ ] Load cells calibrated to ±10g accuracy
- [ ] Torque limiting prevents damage from obstructions
- [ ] Stirring effective in water and thick dal consistency

### Dependencies
- EP-001 (STM32 PWM outputs ready)
- Mechanical design and fabrication
- DS3225 servo and load cell procurement

### Related Stories
- [[02-Stories#ST-009|ST-009: Servo Arm Assembly]]
- [[02-Stories#ST-010|ST-010: Stirring Patterns]]
- [[02-Stories#ST-011|ST-011: Load Cell Integration]]
- [[02-Stories#ST-012|ST-012: Weight-Based Dispensing]]

---

## Epic 4: Computer Vision System

**Epic ID:** EP-004
**Priority:** High
**Timeline:** Sprints 6-7 (Weeks 11-14)
**Status:** Not Started

### Description
Implement overhead camera system with controlled illumination, build image preprocessing pipeline, collect training data, and deploy TFLite food stage classification model.

### Business Value
Vision-based cooking stage detection enables autonomous recipe progression without manual intervention. This is a key differentiator from simple timer-based cooking.

### Success Criteria
- [ ] Camera capturing stable overhead images with LED ring lighting
- [ ] Preprocessing pipeline <100ms per frame
- [ ] Training dataset: 2,000+ labeled images across 5-7 stage classes
- [ ] TFLite model deployed with >85% accuracy
- [ ] Inference time <200ms on CM5
- [ ] Rule-based fallback operational

### Dependencies
- EP-001 (CM5 platform, CSI-2 camera interface)
- Training data collection (requires manual cooking sessions)

### Related Stories
- [[02-Stories#ST-013|ST-013: Camera and Lighting Setup]]
- [[02-Stories#ST-014|ST-014: Image Preprocessing Pipeline]]
- [[02-Stories#ST-015|ST-015: Training Data Collection]]
- [[02-Stories#ST-016|ST-016: Model Training and Deployment]]

---

## Epic 5: Recipe Orchestration

**Epic ID:** EP-005
**Priority:** Critical
**Timeline:** Sprints 8-9 (Weeks 15-17)
**Status:** Not Started

### Description
Define recipe YAML format, implement state machine execution engine, build ingredient dispensing subsystems (ASD, CID, SLD), and validate end-to-end cooking of 3-5 Indian recipes.

### Business Value
This epic brings all subsystems together into cohesive autonomous cooking. It validates the core product value proposition: "robot cooks complete meals autonomously."

### Success Criteria
- [ ] Recipe YAML schema defined and validated
- [ ] State machine executes recipes with CV/timeout/weight transitions
- [ ] ASD (3 servo gates), CID (2 linear actuators), SLD (2 pumps + solenoids + load cell) operational
- [ ] Weight-verified dispensing ±10% accuracy
- [ ] 5 recipes successfully cooked: Dal Tadka, Jeera Rice, Tomato Soup, Khichdi, Vegetable Curry

### Dependencies
- EP-002 (thermal control)
- EP-003 (stirring and weighing)
- EP-004 (CV stage detection)
- Mechanical dispensing tray fabrication

### Related Stories
- [[02-Stories#ST-017|ST-017: Recipe YAML Format]]
- [[02-Stories#ST-018|ST-018: State Machine Engine]]
- [[02-Stories#ST-019|ST-019: Dispensing Mechanism]]
- [[02-Stories#ST-020|ST-020: Recipe Testing]]

---

## Epic 6: User Interface

**Epic ID:** EP-006
**Priority:** Medium
**Timeline:** Sprints 9-10 (Weeks 18-20)
**Status:** Not Started

### Description
Build Qt/QML touchscreen UI on CM5, implement REST API for remote control, and develop Flutter companion mobile app for iOS and Android.

### Business Value
User-friendly interfaces (touchscreen + mobile app) make the product accessible to non-technical users. Live camera feed and remote monitoring enhance user experience and trust.

### Success Criteria
- [ ] 5 touchscreen screens: Home, Recipe Detail, Cooking, Settings, History
- [ ] Live camera feed embedded in UI with CV overlays
- [ ] REST API with 5+ endpoints operational
- [ ] Flutter app functional on Android/iOS with recipe browse and live view
- [ ] WiFi AP mode pairing flow working

### Dependencies
- EP-001 (CM5 platform)
- EP-004 (camera feed)
- EP-005 (recipe state machine for API integration)

### Related Stories
- [[02-Stories#ST-021|ST-021: Touchscreen UI Implementation]]
- [[02-Stories#ST-022|ST-022: REST API Development]]
- [[02-Stories#ST-023|ST-023: Flutter Mobile App]]
- [[02-Stories#ST-024|ST-024: WiFi Pairing]]

---

## Epic 7: Integration & Validation

**Epic ID:** EP-007
**Priority:** Critical
**Timeline:** Sprints 11-12 (Weeks 21-24)
**Status:** Not Started

### Description
Complete system integration, perform comprehensive cooking validation, execute safety testing, and conduct reliability assessment through endurance testing.

### Business Value
Validates production readiness, identifies bugs and edge cases, ensures safety compliance, and provides confidence for alpha phase planning.

### Success Criteria
- [ ] All subsystems integrated in single assembly
- [ ] 5 recipes cooked 5+ times each with consistent results
- [ ] All safety interlocks verified (pot detect, overtemp, e-stop, comm loss)
- [ ] 50+ cook cycle endurance test passed
- [ ] 24-hour continuous operation test passed
- [ ] Live demo prepared with 3 recipes
- [ ] Prototype report and lessons learned documented

### Dependencies
- EP-001 through EP-006 (all subsystems completed)
- Full mechanical assembly

### Related Stories
- [[02-Stories#ST-025|ST-025: Full System Integration]]
- [[02-Stories#ST-026|ST-026: Cooking Validation]]
- [[02-Stories#ST-027|ST-027: Safety Testing]]
- [[02-Stories#ST-028|ST-028: Reliability Testing]]
- [[02-Stories#ST-029|ST-029: Demo Preparation]]

---

## Epic Priority Matrix

| Epic | Priority | Business Value | Technical Risk | Timeline |
|------|----------|----------------|----------------|----------|
| EP-001: Foundation Infrastructure | Critical | High | Medium | Sprints 1-2 |
| EP-002: Thermal Control System | Critical | High | High | Sprints 3-4 |
| EP-003: Robotic Manipulation | High | High | Medium | Sprints 4-5 |
| EP-004: Computer Vision System | High | High | High | Sprints 6-7 |
| EP-005: Recipe Orchestration | Critical | Very High | Medium | Sprints 8-9 |
| EP-006: User Interface | Medium | Medium | Low | Sprints 9-10 |
| EP-007: Integration & Validation | Critical | Very High | Medium | Sprints 11-12 |

---

## Epic Dependencies Graph

```
EP-001 (Foundation)
  ├──► EP-002 (Thermal)
  ├──► EP-003 (Robotic)
  ├──► EP-004 (Vision)
  └──► EP-006 (UI)

EP-002 + EP-003 + EP-004
  └──► EP-005 (Recipe Orchestration)

EP-001 + EP-005
  └──► EP-006 (UI - API integration)

EP-001 through EP-006
  └──► EP-007 (Integration & Validation)
```

---

## Related Documentation

- [[02-Stories|User Stories]]
- [[03-Sprints|Sprint Planning]]
- [[../07-Development/01-Prototype-Development-Plan|Prototype Development Plan]]

---

#epicura #epics #projectmanagement #agile
---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |