---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Sprint Planning

## Overview

This document outlines the sprint plan for the Epicura prototype development. The project spans **6 weeks of pre-sprint PCB development** plus **12 two-week sprints (24 weeks)** for a total of **30 weeks**.

**CRITICAL UPDATE:** A Pre-Sprint Phase for custom PCB design and fabrication has been added. This phase is **essential** and must complete before Sprint 1 to avoid blocking the entire project.

**Target Velocity:** 20-25 story points per sprint (1-2 developers)
**Sprint Duration:** 2 weeks (10 working days)
**Total Sprints:** 3 pre-sprint stories + 12 regular sprints
**Total Story Points:** 34 (pre-sprint) + 246 (sprints) = **280 points**

---

## Pre-Sprint Phase: PCB Development (Weeks -6 to 0)

### Overview

**Duration:** 6 weeks (Weeks -6 to 0, before Sprint 1)
**Epic:** EP-000 (Hardware Foundation - NEW)
**Total Story Points:** 34
**Goal:** Design, fabricate, and validate 3 custom PCBs required for all subsequent sprints

**Critical Path Impact:** Without these PCBs, Sprint 2+ will be blocked. The NUCLEO-G474RE dev board can support Sprint 1 only.

---

### Story PCB-001: Controller PCB Design

**Story Type:** Technical
**Story Points:** 13
**Priority:** P0 (Critical)
**Duration:** Weeks -6 to -4 (3 weeks)

#### Description
As a hardware engineer, I need to design the Controller PCB hosting the STM32G474RE and all sensor interfaces so that the embedded software can run on custom hardware instead of a development board.

#### Acceptance Criteria
- [ ] Schematic complete in KiCad with all components from [[../09-PCB/01-Controller-PCB-Design|Controller PCB Design]] spec:
  - STM32G474RE LQFP-64 with all peripherals (SPI2, I2C1, ADC, PWM, CAN)
  - 3.3V LDO (AMS1117) with proper decoupling
  - 8 MHz HSE and 32.768 kHz LSE crystals
  - All sensor connectors (MLX90614, HX711, NTC, safety I/O)
  - SPI interface to CM5
  - SWD debug header
- [ ] PCB layout complete (4-layer, 160x90mm, ENIG finish):
  - GND plane continuous under STM32
  - SPI traces matched length (±2mm)
  - ADC traces routed over solid GND
  - Thermal vias under STM32 exposed pad (9+ vias)
  - All connectors accessible from board edges
- [ ] DRC (Design Rule Check) passes with zero errors
- [ ] ERC (Electrical Rule Check) passes with zero errors
- [ ] BOM exported with Mouser/Digikey part numbers
- [ ] Gerber files generated for JLCPCB submission
- [ ] Design review completed by embedded developer and power engineer

#### Technical Notes
- Use 4-layer stackup: Signal (2oz Cu) / GND / 3.3V / Signal (2oz Cu)
- Follow IPC-2221 class 2 design rules
- Reference design: ST NUCLEO-G474RE schematic

#### Dependencies
- STM32G474RE datasheet and pin allocation decisions
- Sensor interface specifications from [[../02-Hardware/03-Sensors-Acquisition|Sensors & Acquisition]]

**Estimated Effort:** 120 hours (3 weeks × 40 hrs)

---

### Story PCB-002: Driver PCB Design

**Story Type:** Technical
**Story Points:** 13
**Priority:** P0 (Critical)
**Duration:** Weeks -5 to -3 (3 weeks, overlaps with PCB-001 layout)

#### Description
As a hardware engineer, I need to design the Driver PCB with power conversion and actuator drivers so that all servos, solenoids, and motors can be powered and controlled from the STM32.

#### Acceptance Criteria
- [ ] Schematic complete in KiCad per [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]] spec:
  - 3x MP1584EN buck converters (24V → 12V, 6.5V, 5V)
  - 2x DRV8876 H-bridge ICs for linear actuators
  - 1x TB6612FNG dual H-bridge for peristaltic pumps
  - 3x IRLML6344 MOSFETs for solenoids and fan
  - INA219 current monitor on 24V input
  - Input protection (polyfuse, reverse polarity Schottky, TVS)
  - All actuator output connectors
- [ ] PCB layout complete (4-layer, 160x90mm, 2oz outer copper):
  - GND plane continuous under all switching converters
  - Buck converter input/output cap loops minimized (<10mm)
  - Power traces sized for current (≥2mm for 24V input, ≥1mm for rails)
  - Thermal vias under DRV8876 exposed pads (6+ vias each)
  - Creepage ≥2mm between 24V and logic signals
- [ ] Thermal analysis completed (component junction temps <125°C)
- [ ] DRC and ERC pass with zero errors
- [ ] BOM exported with Mouser/Digikey part numbers
- [ ] Gerber files ready for JLCPCB
- [ ] Design review by power electronics engineer

#### Technical Notes
- 2oz outer copper required for high-current traces
- Use large copper pours (≥400mm²) around MP1584EN for heat dissipation
- All MOSFET gates have 10kΩ pull-downs (safe default state)

#### Dependencies
- Power budget calculations from [[../08-Components/04-Total-Component-Cost|Component Cost]]
- Actuator current specifications

**Estimated Effort:** 120 hours (3 weeks × 40 hrs)

---

### Story PCB-003: PCB Fabrication and Assembly

**Story Type:** Technical
**Story Points:** 8
**Priority:** P0 (Critical)
**Duration:** Weeks -3 to 0 (4 weeks: 3 weeks fab + 1 week testing)

#### Description
As a hardware engineer, I need to fabricate and assemble the Controller and Driver PCBs so that embedded software development can begin on custom hardware.

#### Acceptance Criteria
- [ ] PCB orders placed with JLCPCB (or equivalent):
  - Controller PCB: 10 pcs, 4-layer, 160x90mm, ENIG, 1.6mm thick
  - Driver PCB: 10 pcs, 4-layer, 160x90mm, ENIG, 2oz outer Cu
  - CM5IO Board: 5 pcs, 4-layer, 160x90mm, ENIG (CM5 carrier)
- [ ] All components procured and received:
  - Controller PCB BOM (~$115 for 10 boards with spares)
  - Driver PCB BOM (~$180 for 10 boards with spares)
  - CM5IO BOM (~$155 for 5 boards)
- [ ] PCBs received and visually inspected (no defects)
- [ ] Assembly completed (SMT reflow + through-hole):
  - Controller PCB: 3 boards fully assembled
  - Driver PCB: 3 boards fully assembled
  - CM5IO Board: 2 boards fully assembled
- [ ] Power-on testing passed for all assembled boards:
  - 3.3V rail measures 3.3V ±3% under 100mA load
  - 12V, 6.5V, 5V rails measure correctly ±3% (Driver PCB)
  - STM32 responds to ST-Link probe (reads device ID)
  - No shorts detected between power rails
- [ ] Continuity testing complete (all connectors, signals)
- [ ] Basic I/O validated:
  - STM32 GPIO toggle (blink LED) on Controller PCB
  - CM5 boots to Linux prompt on CM5IO
  - Buck converters regulate properly under 500mA dummy load (Driver PCB)

#### Technical Notes
- JLCPCB lead time: 24h review + 3-4 days production + 5-7 days DHL shipping = 10-14 days total
- Consider JLCPCB SMT assembly service (+$150-300) to save 2-3 days
- Order components 1 week before PCB arrival to minimize wait time

#### Procurement Dependencies
- Week -8: Order long-lead ICs (STM32, DRV8876, TB6612FNG, MP1584EN)
- Week -7: Order passives, connectors, inductors
- Week -6: Submit Gerber files to JLCPCB
- Week -3: PCBs ship from China
- Week -2: PCBs arrive, begin assembly

#### Risks & Mitigation
- **Risk:** PCB fabrication defects
  - **Mitigation:** Order 10 boards (need 3, have 7 spares)
- **Risk:** Component out of stock
  - **Mitigation:** Order 2x critical ICs, identify drop-in replacements
- **Risk:** Assembly errors (bridged pins, cold solder joints)
  - **Mitigation:** Visual inspection under magnifier, continuity testing before power-on

#### Definition of Done
- [ ] 3x Controller PCBs powered and responding to SWD debugger
- [ ] 3x Driver PCBs powered with all rails within spec
- [ ] 2x CM5IO boards booting CM5 to Linux
- [ ] All test results documented in git repository
- [ ] Known issues list created (minor rework if needed)

**Estimated Effort:** 80 hours (40 hrs procurement/tracking + 40 hrs assembly/testing)

---

### Pre-Sprint Phase Deliverables

By Week 0 (Sprint 1 start), the following must be complete:

- [ ] **Hardware:**
  - 3 functional Controller PCBs (STM32 programmed, basic I/O verified)
  - 3 functional Driver PCBs (power rails stable, actuators connectable)
  - 2 functional CM5IO boards (CM5 booting Linux)
  - Stacking connector tested (all 3 boards mate correctly)

- [ ] **Documentation:**
  - Complete KiCad project files in git repo (`hardware/pcb/controller`, `hardware/pcb/driver`, `hardware/pcb/cmio`)
  - BOM with Mouser/Digikey links (CSV + markdown)
  - Assembly instructions with photos
  - Power-on test procedure documented
  - Known issues tracker

- [ ] **Procurement:**
  - All Sprint 1 components ordered (CM5, sensors, cables)
  - All Sprint 2-3 long-lead components ordered (induction surface, MLX90614, load cells)

---

### Pre-Sprint Risks & Critical Path

**Critical Path Items:**
1. ❗ **PCB design must complete by Week -6** to submit to JLCPCB on time
2. ❗ **Long-lead ICs must be ordered by Week -8** (STM32G474, DRV8876, TB6612FNG: 2-3 week lead time)
3. ❗ **Raspberry Pi CM5 must be ordered by Week -4** (3-4 week lead time)

**Blocking Dependencies:**
- Sprint 1 can proceed with NUCLEO-G474RE dev board if custom PCBs delayed (fallback)
- Sprint 2+ **BLOCKED** without custom PCBs (no CAN bus, no actuator drivers, no power rails)

**Mitigation Strategy:**
- Start PCB design immediately (Week -8)
- Order all long-lead components before PCB submission (Week -8)
- Use Nucleo + breadboard for Sprint 1 if PCBs delayed >2 weeks

---

## Sprint 1: Foundation - Compute Platforms

**Duration:** Weeks 1-2
**Epic:** EP-001 (Foundation Infrastructure)
**Total Story Points:** 21
**Goal:** Establish CM5 and STM32 platforms with basic I/O validation

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-001 | CM5 Yocto Build and Setup | 8 | Not Started |
| ST-002 | STM32 FreeRTOS Setup | 5 | Not Started |
| ST-003 | UART Communication Protocol | 8 | Not Started |

### Sprint Deliverables
- CM5 booting Yocto Linux with SSH access
- STM32 running FreeRTOS with 4 tasks
- Bidirectional UART messaging functional (<10ms latency)

### Risks & Mitigation
- **Risk:** Yocto build complexity
  - **Mitigation:** Fallback to Raspberry Pi OS if needed
- **Risk:** UART reliability issues
  - **Mitigation:** Add hardware flow control (RTS/CTS)

### Definition of Done
- [ ] All acceptance criteria met for all stories
- [ ] Code reviewed and committed
- [ ] Basic integration test passed
- [ ] Documentation updated

---

## Sprint 2: Foundation - Power & Thermal Setup

**Duration:** Weeks 3-4
**Epic:** EP-001 (Foundation), EP-002 (Thermal Control)
**Total Story Points:** 18
**Goal:** Complete power distribution and begin thermal subsystem integration

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-004 | Power Distribution | 5 | Not Started |
| ST-005 | CAN Bus Integration with Induction Module | 8 | Not Started |
| ST-007 | IR Temperature Sensor Integration | 5 | Not Started |

### Sprint Deliverables
- Stable power to all subsystems (1-hour stress test passed)
- CAN bus communication with induction module
- MLX90614 temperature readings validated

### Risks & Mitigation
- **Risk:** Induction module CAN protocol undocumented
  - **Mitigation:** Reverse-engineer protocol or contact manufacturer
- **Risk:** Power brownouts under load
  - **Mitigation:** Add decoupling capacitors, separate power rails

### Definition of Done
- [ ] All acceptance criteria met
- [ ] Power consumption measured and within budget
- [ ] CAN protocol documented
- [ ] Temperature sensor calibrated

---

## Sprint 3: Thermal Control - PID & Safety

**Duration:** Weeks 5-6
**Epic:** EP-002 (Thermal Control)
**Total Story Points:** 21
**Goal:** Complete thermal control subsystem with PID and safety interlocks

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-006 | PID Controller Implementation | 8 | Not Started |
| ST-008 | Safety Interlocks | 5 | Not Started |

### Carryover Capacity
- **8 points** available for polish, documentation, or addressing technical debt

### Sprint Deliverables
- PID controller achieving ±10°C accuracy
- All safety interlocks functional and tested
- Water boil test: 1L → 100°C in <8 minutes

### Risks & Mitigation
- **Risk:** PID tuning difficult
  - **Mitigation:** Use auto-tuning methods (Ziegler-Nichols)
- **Risk:** False triggers on safety interlocks
  - **Mitigation:** Add hysteresis and debouncing

### Definition of Done
- [ ] Step response test passed
- [ ] All safety interlocks verified individually
- [ ] PID gains documented
- [ ] Thermal subsystem integrated and tested

---

## Sprint 4: Robotic Manipulation - Arm & Patterns

**Duration:** Weeks 7-8
**Epic:** EP-003 (Robotic Manipulation)
**Total Story Points:** 21
**Goal:** Build servo arm and implement stirring patterns

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-009 | Servo Arm Assembly | 5 | Not Started |
| ST-010 | Stirring Pattern Implementation | 8 | Not Started |

### Carryover Capacity
- **8 points** available for mechanical iterations or additional patterns

### Sprint Deliverables
- Servo arm mechanically stable and mounted
- 5 stirring patterns functional
- Patterns tested in water and thick dal

### Risks & Mitigation
- **Risk:** Mechanical design iterations needed
  - **Mitigation:** Rapid prototyping with 3D printer
- **Risk:** Servo torque insufficient
  - **Mitigation:** Verify DS3225 specs, upgrade if needed

### Definition of Done
- [ ] All stirring patterns functional
- [ ] Mechanical stability verified (no wobble)
- [ ] Torque limiting working
- [ ] Speed control validated (10-60 RPM)

---

## Sprint 5: Robotic Manipulation - Weighing

**Duration:** Weeks 9-10
**Epic:** EP-003 (Robotic Manipulation)
**Total Story Points:** 19
**Goal:** Complete weight measurement system for dispensing verification

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-011 | Load Cell Integration | 8 | Not Started |
| ST-012 | Weight-Based Dispensing Preparation | 3 | Not Started |

### Carryover Capacity
- **8 points** available for calibration refinement or buffer

### Sprint Deliverables
- Load cells calibrated to ±10g accuracy
- Weight-based dispensing control logic ready
- Platform mechanically stable

### Risks & Mitigation
- **Risk:** Vibration noise in weight readings
  - **Mitigation:** Mechanical isolation, median filtering

### Definition of Done
- [ ] Calibration completed with reference weights
- [ ] Accuracy verified across full range (0-5kg)
- [ ] Weight monitoring functional
- [ ] Integration test with simulated dispensing

---

## Sprint 6: Computer Vision - Camera & Preprocessing

**Duration:** Weeks 11-12
**Epic:** EP-004 (Computer Vision)
**Total Story Points:** 21
**Goal:** Set up camera system and build preprocessing pipeline

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-013 | Camera and Lighting Setup | 5 | Not Started |
| ST-014 | Image Preprocessing Pipeline | 8 | Not Started |

### Carryover Capacity
- **8 points** available for pipeline optimization

### Sprint Deliverables
- Camera capturing stable 1080p @ 30fps
- LED ring providing consistent illumination
- Preprocessing pipeline <100ms per frame

### Risks & Mitigation
- **Risk:** Camera performance bottleneck
  - **Mitigation:** Optimize with OpenCV, consider GPU acceleration

### Definition of Done
- [ ] Camera feed stable and consistent
- [ ] All preprocessing steps functional
- [ ] Benchmark target achieved (<100ms)
- [ ] Test images captured across cooking stages

---

## Sprint 7: Computer Vision - Training & Deployment

**Duration:** Weeks 13-14
**Epic:** EP-004 (Computer Vision)
**Total Story Points:** 26
**Goal:** Collect training data, train model, and deploy to CM5

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-015 | Training Data Collection | 13 | Not Started |
| ST-016 | Model Training and Deployment | 13 | Not Started |

### Sprint Deliverables
- 2,000+ labeled images across 5-7 cooking stages
- TFLite model deployed with >85% accuracy
- Inference <200ms per frame on CM5

### Risks & Mitigation
- **Risk:** Insufficient model accuracy
  - **Mitigation:** Collect more data, ensemble methods, rule-based fallback
- **Risk:** Training time exceeds sprint
  - **Mitigation:** Use pre-trained models, cloud GPU resources

### Definition of Done
- [ ] Dataset complete and augmented
- [ ] Model accuracy >85% on test set
- [ ] TFLite conversion successful
- [ ] Deployed model meets performance targets
- [ ] Rule-based fallback implemented

---

## Sprint 8: Recipe Orchestration - State Machine

**Duration:** Weeks 15-16
**Epic:** EP-005 (Recipe Orchestration)
**Total Story Points:** 24
**Goal:** Define recipe format and implement state machine engine

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-017 | Recipe YAML Format | 5 | Not Started |
| ST-018 | State Machine Engine | 13 | Not Started |

### Carryover Capacity
- **6 points** available for state machine testing

### Sprint Deliverables
- Recipe YAML schema defined with 5 recipe files
- State machine executing recipes end-to-end
- Transitions working: CV, timeout, weight-based

### Risks & Mitigation
- **Risk:** State machine complexity
  - **Mitigation:** Start simple, iterate with test recipes
- **Risk:** Integration bugs across subsystems
  - **Mitigation:** Unit test each subsystem interface

### Definition of Done
- [ ] 5 recipe files validated against schema
- [ ] State machine executes 2-stage test recipe successfully
- [ ] All transition types functional
- [ ] Error handling and logging implemented

---

## Sprint 9: Recipe Orchestration - Dispensing & Testing

**Duration:** Weeks 17-18
**Epic:** EP-005 (Recipe Orchestration), EP-006 (User Interface)
**Total Story Points:** 34 (high - consider overflow to Sprint 10)
**Goal:** Build dispensing mechanism, validate recipes, and start UI work

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-019 | Dispensing Mechanism | 8 | Not Started |
| ST-020 | Recipe Testing and Validation | 13 | Not Started |
| ST-021 | Touchscreen UI Implementation | 13 | Not Started |

### Sprint Strategy
- Prioritize ST-019 and ST-020 (critical path)
- Start ST-021 if capacity allows, otherwise defer to Sprint 10

### Sprint Deliverables
- ASD/CID/SLD dispensing subsystems functional
- 3-5 recipes validated (minimum 3 for MVP)
- UI development started (if time permits)

### Risks & Mitigation
- **Risk:** Sprint overload
  - **Mitigation:** Defer UI polish to Sprint 10
- **Risk:** Recipe failures due to integration issues
  - **Mitigation:** Debug systematically, prioritize 3 recipes for MVP

### Definition of Done
- [ ] Dispensing working for all 3 subsystems (ASD, CID, SLD)
- [ ] Minimum 3 recipes producing edible output
- [ ] Results logged and analyzed
- [ ] UI framework set up (if started)

---

## Sprint 10: User Interface - Touchscreen & API

**Duration:** Weeks 19-20
**Epic:** EP-006 (User Interface)
**Total Story Points:** 34 (high - balanced with Sprint 9)
**Goal:** Complete touchscreen UI and implement REST API

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-021 | Touchscreen UI Implementation (carryover if needed) | 13 | Not Started |
| ST-022 | REST API Development | 8 | Not Started |
| ST-023 | Flutter Mobile App | 13 | Not Started |

### Sprint Strategy
- Complete ST-021 from Sprint 9 if needed
- Prioritize ST-022 for mobile app integration
- Start ST-023, defer polish to Sprint 11 if needed

### Sprint Deliverables
- 5 touchscreen screens functional
- REST API with all endpoints working
- Flutter app basic functionality (browse, live view)

### Risks & Mitigation
- **Risk:** UI/UX iterations take longer than expected
  - **Mitigation:** Focus on functionality over polish for prototype

### Definition of Done
- [ ] All 5 UI screens implemented and navigable
- [ ] API tested with curl and Postman
- [ ] Mobile app functional on Android device
- [ ] Camera stream rendering in both UIs

---

## Sprint 11: Integration & Validation - Part 1

**Duration:** Weeks 21-22
**Epic:** EP-007 (Integration & Validation), EP-006 (User Interface - polish)
**Total Story Points:** 29
**Goal:** Full system integration, cooking validation, and UI polish

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-024 | WiFi Pairing Flow | 8 | Not Started |
| ST-025 | Full System Integration | 8 | Not Started |
| ST-026 | Cooking Validation | 13 | Not Started |

### Sprint Deliverables
- All subsystems integrated in single assembly
- WiFi pairing working end-to-end
- 5 recipes each cooked 5+ times with logged results

### Risks & Mitigation
- **Risk:** Integration issues surface
  - **Mitigation:** Systematic debugging, isolate subsystems

### Definition of Done
- [ ] End-to-end system test passed
- [ ] Cooking success rate >80%
- [ ] Results analyzed and documented
- [ ] WiFi pairing tested

---

## Sprint 12: Integration & Validation - Part 2

**Duration:** Weeks 23-24
**Epic:** EP-007 (Integration & Validation)
**Total Story Points:** 29
**Goal:** Safety testing, reliability assessment, and demo preparation

### Stories

| ID | Story | Points | Status |
|----|-------|--------|--------|
| ST-027 | Safety Testing | 8 | Not Started |
| ST-028 | Reliability Testing | 13 | Not Started |
| ST-029 | Demo Preparation and Documentation | 8 | Not Started |

### Sprint Deliverables
- All safety interlocks validated
- 50+ cook cycle endurance test completed
- Live demo ready with 3 recipes
- Prototype report written

### Risks & Mitigation
- **Risk:** Reliability test failures
  - **Mitigation:** Document issues, prioritize critical fixes

### Definition of Done
- [ ] Safety test report completed
- [ ] Reliability metrics calculated
- [ ] Demo successfully rehearsed
- [ ] All documentation complete
- [ ] Known issues documented

---

## Sprint Capacity Planning

| Sprint | Weeks | Story Points | Stories | Epic Focus |
|--------|-------|--------------|---------|------------|
| **Pre-Sprint** | **-6 to 0** | **34** | **3** | **EP-000: PCB Development** |
| Sprint 1 | 1-2 | 21 | 3 | EP-001: Foundation |
| Sprint 2 | 3-4 | 18 | 3 | EP-001, EP-002: Power & Thermal Setup |
| Sprint 3 | 5-6 | 21 | 2 | EP-002: Thermal Control |
| Sprint 4 | 7-8 | 21 | 2 | EP-003: Robotic Arm |
| Sprint 5 | 9-10 | 19 | 2 | EP-003: Weighing |
| Sprint 6 | 11-12 | 21 | 2 | EP-004: CV Setup |
| Sprint 7 | 13-14 | 26 | 2 | EP-004: CV Training |
| Sprint 8 | 15-16 | 24 | 2 | EP-005: Recipe Engine |
| Sprint 9 | 17-18 | 34 | 3 | EP-005, EP-006: Dispensing & UI |
| Sprint 10 | 19-20 | 34 | 3 | EP-006: UI & API |
| Sprint 11 | 21-22 | 29 | 3 | EP-007, EP-006: Integration Part 1 |
| Sprint 12 | 23-24 | 29 | 3 | EP-007: Integration Part 2 |
| **Total** | **30 weeks** | **331** | **33** | **All Epics** |

**Notes:**
- Total points: 34 (pre-sprint) + 297 (sprints with carryover) = **331 points**
- Core stories only: 34 (pre-sprint) + 246 (sprints) = **280 points**
- **Pre-Sprint Phase is CRITICAL PATH** - must complete before Sprint 1 to avoid project delays

---

## Velocity Tracking

### Target Velocity
- **Pre-Sprint Phase:** 11-12 points/week (PCB engineer + embedded dev, 6 weeks)
- **Conservative:** 18-20 points/sprint (solo developer, 2-week sprints)
- **Moderate:** 20-25 points/sprint (1-2 developers, 2-week sprints)
- **Aggressive:** 25-30 points/sprint (2-3 developers, experienced team, 2-week sprints)

### Actual Velocity
Track actual velocity after each sprint to adjust future sprint planning.

| Sprint | Planned | Completed | Variance | Notes |
|--------|---------|-----------|----------|-------|
| **Pre-Sprint** | **34 (over 6 weeks)** | **-** | **-** | **PCB-001, PCB-002, PCB-003** |
| Sprint 1 | 21 | - | - | |
| Sprint 2 | 18 | - | - | |
| Sprint 3 | 21 | - | - | |
| Sprint 4 | 21 | - | - | |
| Sprint 5 | 19 | - | - | |
| Sprint 6 | 21 | - | - | |
| Sprint 7 | 26 | - | - | |
| Sprint 8 | 24 | - | - | |
| Sprint 9 | 34 | - | - | |
| Sprint 10 | 34 | - | - | |
| Sprint 11 | 29 | - | - | |
| Sprint 12 | 29 | - | - | |

**Pre-Sprint Velocity Note:** 34 points over 6 weeks = 5.7 points/week average. This is lower velocity due to external dependencies (JLCPCB fabrication time).

---

## Sprint Ceremonies

### Sprint Planning (2 hours, start of sprint)
- Review sprint goal
- Review and estimate stories
- Commit to sprint backlog
- Identify dependencies and risks

### Daily Standup (15 minutes, daily)
- What did I complete yesterday?
- What will I work on today?
- Are there any blockers?

### Sprint Review (1 hour, end of sprint)
- Demo completed stories
- Review sprint goal achievement
- Gather stakeholder feedback

### Sprint Retrospective (1 hour, end of sprint)
- What went well?
- What could be improved?
- Action items for next sprint

---

## Critical Path Analysis

### Updated Dependencies (Including Pre-Sprint Phase)

```
Week -8: Start PCB Design (PCB-001, PCB-002)
   ↓ (3 weeks design)
Week -6: Submit PCBs to JLCPCB
   ↓ (3 weeks fabrication)
Week -3: PCBs Ship from China
   ↓ (1 week delivery)
Week -2: PCBs Arrive → Begin Assembly (PCB-003)
   ↓ (2 weeks assembly + testing)
Week 0: Sprint 1 Starts (ST-001, ST-002, ST-003)
   ↓ (2 weeks)
Week 2: Sprint 2 (Power + CAN) ← **BLOCKED without custom PCBs**
   ↓ (2 weeks)
Week 4: Sprint 3 (PID + Safety)
   ↓ (2 weeks)
Week 6: Sprint 4-5 (Robotic Arm + Load Cells) ← Can parallelize
   ↓ (4 weeks)
Week 10: Sprint 6-7 (CV Setup + Training) ← Can parallelize
   ↓ (4 weeks)
Week 14: Sprint 8 (Recipe Engine) ← Blocked until CV deployed
   ↓ (2 weeks)
Week 16: Sprint 9 (Dispensing + Recipe Testing)
   ↓ (2 weeks)
Week 18: Sprint 10 (UI + API)
   ↓ (2 weeks)
Week 20: Sprint 11 (Integration Part 1)
   ↓ (2 weeks)
Week 22: Sprint 12 (Integration Part 2 + Validation)
   ↓ (2 weeks)
Week 24: Project Complete
```

### Parallel Tracks

**Pre-Sprint Phase (Weeks -6 to 0):**
- Week -6 to -4: Controller + Driver PCB design (serial, PCB engineer)
- Week -4: CM5IO PCB design (can overlap with layout work)
- Week -3 to 0: Fabrication (JLCPCB) + procurement (parallel)

**Sprint Phase (Weeks 7-18):**
- **Thermal subsystem** (complete by Sprint 3) can run in parallel with:
  - **Robotic subsystem** (Sprints 4-5)
  - **CV subsystem** (Sprints 6-7)

This parallelization assumes multiple team members or ability to context-switch.

### Critical Path Items (Cannot Compress)

| Item | Duration | Why Critical | Earliest Start | Latest Finish |
|------|----------|--------------|----------------|---------------|
| PCB Fabrication (JLCPCB) | 3 weeks | External vendor lead time | Week -6 | Week -3 |
| CM5 Procurement | 3-4 weeks | Raspberry Pi supply chain | Week -4 | Week 0 |
| Induction Surface Procurement | 3-4 weeks | China shipping (AliExpress) | Week -2 | Week 2 |
| CV Model Training (Sprint 7) | 2 weeks | Data collection + labeling time | Week 13 | Week 14 |
| Recipe Testing (Sprint 9) | 2 weeks | Cook time + iterations (25 sessions) | Week 17 | Week 18 |

**Total Critical Path Duration:** 30 weeks (6 pre-sprint + 24 sprints)

---

## Risk Register by Sprint

| Sprint | Risk | Impact | Mitigation |
|--------|------|--------|------------|
| **Pre-Sprint** | **PCB design errors (schematic/layout)** | **Critical** | **Design reviews, DRC/ERC checks, order 10 boards for spares** |
| **Pre-Sprint** | **Component shortages (STM32, DRV8876, CM5)** | **Critical** | **Order 2x critical parts by Week -8, identify drop-in replacements** |
| **Pre-Sprint** | **PCB fabrication defects** | **High** | **Order 10 boards (need 3), visual inspection before assembly** |
| **Pre-Sprint** | **Assembly errors (bridged pins, cold solder)** | **High** | **Magnifier inspection, continuity testing, power-on procedure** |
| 1 | Yocto build fails | High | Fallback to Raspberry Pi OS |
| 2 | CAN protocol undocumented | Medium | Reverse-engineer or contact manufacturer |
| 2 | **No custom PCBs (blocked by Pre-Sprint delay)** | **Critical** | **Use Nucleo + breadboard for Sprint 2 (degraded functionality), extend timeline +4 weeks** |
| 3 | PID tuning difficult | Medium | Use auto-tuning methods |
| 4 | Mechanical iterations needed | Medium | Rapid 3D printing |
| 7 | CV model accuracy low | High | Collect more data, use fallback |
| 9 | Recipe failures | High | Focus on 3 MVP recipes |
| 11 | Integration issues | Medium | Systematic debugging |
| 12 | Reliability test failures | Medium | Document and prioritize fixes |

### Pre-Sprint Phase Risk Mitigation Plan

**Highest Impact Risks:**
1. **PCB Design Errors** → Multi-stage review process:
   - Week -6: Self-review (designer)
   - Week -5: Peer review (embedded developer validates pin assignments)
   - Week -4: Power engineer review (thermal, current capacity)
   - Week -3: Final DRC/ERC before submission

2. **Component Shortages** → Procurement strategy:
   - Week -8: Order ALL long-lead ICs (STM32G474, DRV8876, TB6612FNG, MP1584EN, INA219)
   - Order 2x critical single-point-of-failure parts (STM32, CM5)
   - Document drop-in replacements in BOM notes
   - Monitor Mouser/Digikey stock levels weekly

3. **PCB Fabrication Delays** → Backup plan:
   - Primary: JLCPCB (3-4 week lead time)
   - Backup: PCBWay (5-6 week lead time, submit in parallel if budget allows)
   - Fallback: Nucleo-G474RE + breadboard for Sprint 1-2 (degrades functionality, adds 4 weeks)

**Monitoring Plan:**
- Week -8: PCB design kickoff meeting
- Week -6: PCB design 80% checkpoint
- Week -5: Submit PCBs to JLCPCB
- Week -4: Track PCB production status (JLCPCB dashboard)
- Week -3: Confirm DHL tracking number
- Week -2: PCBs arrive → begin assembly
- Week -1: Power-on testing checkpoint
- Week 0: Sprint 1 starts with validated PCBs

---

## Definition of Done (Project-Wide)

For a story to be considered "Done":
- [ ] All acceptance criteria met
- [ ] Code reviewed (if applicable)
- [ ] Unit tests written and passing (if applicable)
- [ ] Integration test passed
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Stakeholder demo completed (if user-facing)

For a sprint to be considered "Done":
- [ ] All committed stories completed
- [ ] Sprint goal achieved
- [ ] Sprint review conducted
- [ ] Sprint retrospective completed
- [ ] Next sprint planned

---

## Burndown Chart Template

Track story points remaining over sprint days (10 working days per sprint).

**Example:**
```
Story Points
25 |●
20 |  ●
15 |    ●
10 |      ●
 5 |        ●
 0 |__________●
   Day 1 3 5 7 9

● = Actual
/ = Ideal (linear)
```

---

## Related Documentation

### Project Management
- [[01-Epics|Epics]] — High-level project epics and themes
- [[02-Stories|User Stories]] — Detailed story definitions with acceptance criteria
- [[04-Procurement-Schedule|Procurement Schedule]] — ⭐ **NEW** Detailed component ordering timeline with part numbers and suppliers
- [[05-Resource-Allocation|Resource Allocation]] — ⭐ **NEW** Personnel assignments, Gantt chart, labor cost estimates
- [[../../__todo|Project Todo List]] — Current task tracking

### Hardware Design
- [[../09-PCB/01-Controller-PCB-Design|Controller PCB Design]] — STM32G474RE board schematic and layout
- [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]] — Power conversion and actuator drivers
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]] — Full BOM and cost analysis

### Development Planning
- [[../07-Development/01-Prototype-Development-Plan|Prototype Development Plan]] — Overall prototype roadmap

---

## Action Items (Start Immediately)

### Week -8 (NOW)
- [ ] Hire PCB design engineer or assign internal resource
- [ ] Order long-lead components (CM5, STM32G474, DRV8876, TB6612FNG, MP1584EN)
- [ ] Set up KiCad project repository
- [ ] Review [[../09-PCB/01-Controller-PCB-Design|Controller PCB Design]] and [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]] specifications

### Week -7
- [ ] Controller PCB schematic 80% complete
- [ ] Order passive components and connectors (see [[04-Procurement-Schedule|Procurement Schedule]])
- [ ] Begin Driver PCB schematic

### Week -6
- [ ] Complete all PCB layouts (Controller, Driver, CM5IO)
- [ ] Submit Gerber files to JLCPCB
- [ ] Confirm component orders placed

### Week -3
- [ ] Track PCB shipment from JLCPCB
- [ ] Prepare assembly workspace (soldering station, magnifier, multimeter)

### Week 0
- [ ] Complete PCB power-on testing
- [ ] Begin Sprint 1

---

#epicura #sprints #projectmanagement #agile #scrum #pcb-development
---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |