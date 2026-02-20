---
tags: [epicura, project-management, epic, actuation, dispensing]
created: 2026-02-16
aliases: [ARM Epic, Actuation Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 5 stories across Sprints 4–6 |
> | 2026-02-17 | Manas Pradhan | Split SRV, ASD, SLD stories (>5pts) — 8 stories across Sprints 4–6 |

# Epic: ARM — Robotic Arm & Dispensing

Servo arm stirring control and all three dispensing subsystems: P-ASD (pneumatic seasoning), CID (coarse ingredients), and SLD (standard liquids). Covers motor drivers, closed-loop feedback, and calibration routines.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SRV — Servo Arm | 2 | 8 | 4 |
| ASD — Pneumatic Seasoning Dispenser | 2 | 8 | 5 |
| CID — Coarse Ingredient Dispenser | 1 | 5 | 5 |
| SLD — Standard Liquid Dispenser | 2 | 8 | 6 |
| CAL — Calibration | 1 | 5 | 6 |
| **Total** | **8** | **~35** | |

---

## Phase 1 — Robotic Arm (Sprint 4)

### ARM-SRV.01: Servo arm control — PWM driver, stirring patterns, smooth motion
- **Sprint:** [[sprint-04|Sprint 4]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#119](https://github.com/manasXP/epicura/issues/119)
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]], [[EMB-embedded#EMB-COM.01|EMB-COM.01]]
- **Blocks:** [[ARM-actuation#ARM-SRV.02|ARM-SRV.02]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]], [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] DS3225 servo controlled via PWM (50 Hz, 500–2500µs pulse width)
- [ ] 4 stirring patterns implemented: circular, figure-eight, scrape-bottom, fold
- [ ] Smooth acceleration/deceleration ramps to prevent food splashing
- [ ] Home position (arm retracted) command for dispensing and idle states

**Tasks:**
- [ ] `ARM-SRV.01a` — Configure TIM1 PWM for servo: 50 Hz, resolution for 500–2500µs range
- [ ] `ARM-SRV.01b` — Implement servo position control with acceleration/deceleration profiles
- [ ] `ARM-SRV.01c` — Implement stirring patterns: circular (continuous sweep), figure-eight, scrape (slow bottom pass), fold (alternating direction)

---

### ARM-SRV.02: Servo arm feedback — stall detection, SPI commands, testing
- **Sprint:** [[sprint-04|Sprint 4]]
- **Priority:** P0
- **Points:** 3
- **GitHub:** [#120](https://github.com/manasXP/epicura/issues/120)
- **Blocked by:** [[ARM-actuation#ARM-SRV.01|ARM-SRV.01]]
- **Blocks:** [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]], [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] Stall detection via current sensing: if servo draws >2A for >500ms, halt and alert
- [ ] SPI commands implemented: SET_ANGLE, SET_PATTERN, HOME, STOP
- [ ] Position commands accepted via SPI from CM5: angle (0–270°), speed (1–10), pattern ID
- [ ] Each pattern tested with a pot of water; no splashing and smooth motion verified

**Tasks:**
- [ ] `ARM-SRV.02a` — Implement stall detection via ADC current sense on servo power line
- [ ] `ARM-SRV.02b` — Implement SPI command handler for servo: SET_ANGLE, SET_PATTERN, HOME, STOP
- [ ] `ARM-SRV.02c` — Test each pattern with a pot of water; verify no splashing and smooth motion

---

## Phase 2 — Dispensing Subsystems (Sprints 5–6)

### ARM-ASD.01: P-ASD hardware control — pump PWM, solenoid GPIO, pressure sensor
- **Sprint:** [[sprint-05|Sprint 5]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#122](https://github.com/manasXP/epicura/issues/122)
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** [[ARM-actuation#ARM-ASD.02|ARM-ASD.02]], [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]], [[ARM-actuation#ARM-CAL.01|ARM-CAL.01]]

**Acceptance Criteria:**
- [ ] Diaphragm pump controlled via PWM (variable pressure 0–30 kPa)
- [ ] 6× NC solenoid valves individually addressable via GPIO; only one open at a time
- [ ] ADS1015 pressure sensor read via I2C at 10 Hz
- [ ] Closed-loop pressure regulation via P-controller

**Tasks:**
- [ ] `ARM-ASD.01a` — Configure pump PWM channel; implement pressure-to-PWM mapping
- [ ] `ARM-ASD.01b` — Configure 6× GPIO outputs for solenoid valves; implement mutex (one valve at a time)
- [ ] `ARM-ASD.01c` — Implement ADS1015 I2C driver; read pressure at 10 Hz
- [ ] `ARM-ASD.01d` — Implement closed-loop pressure control: P-controller, setpoint via SPI command

---

### ARM-ASD.02: P-ASD dispensing sequence — state machine, anti-clog, accuracy testing
- **Sprint:** [[sprint-05|Sprint 5]]
- **Priority:** P0
- **Points:** 3
- **GitHub:** [#123](https://github.com/manasXP/epicura/issues/123)
- **Blocked by:** [[ARM-actuation#ARM-ASD.01|ARM-ASD.01]]
- **Blocks:** [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]], [[ARM-actuation#ARM-CAL.01|ARM-CAL.01]]

**Acceptance Criteria:**
- [ ] Dispensing sequence state machine: IDLE → PRESSURIZE → DISPENSE → PURGE → IDLE
- [ ] Anti-clog: reverse pressure pulse (valve open, pump off, vent) after dispensing
- [ ] Dose accuracy: ±0.5g for 2g target dose (verified via weight measurement, 20 samples per cartridge)

**Tasks:**
- [ ] `ARM-ASD.02a` — Implement dispensing sequence state machine: IDLE → PRESSURIZE → DISPENSE → PURGE → IDLE
- [ ] `ARM-ASD.02b` — Implement anti-clog reverse pulse routine
- [ ] `ARM-ASD.02c` — Test dose accuracy: dispense onto scale, record 20 samples per cartridge position

---

### ARM-CID.01: CID coarse ingredient dispenser — linear actuator control, position sensing
- **Sprint:** [[sprint-05|Sprint 5]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#125](https://github.com/manasXP/epicura/issues/125)
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]], [[ARM-actuation#ARM-CAL.01|ARM-CAL.01]]

**Acceptance Criteria:**
- [ ] 2× linear actuators driven via DRV8876 H-bridge (forward, reverse, brake, coast)
- [ ] Push-plate travel: 0–100mm, controlled via timed drive or limit switches
- [ ] Actuator speed adjustable via PWM duty cycle (30–100%)
- [ ] Stall detection: if current exceeds 3A for >200ms, stop and report jam
- [ ] SPI commands: DISPENSE(tray_id, distance_mm), HOME(tray_id), STATUS

**Tasks:**
- [ ] `ARM-CID.01a` — Configure DRV8876 control GPIO: IN1, IN2, nSLEEP for each actuator
- [ ] `ARM-CID.01b` — Implement linear actuator driver: forward, reverse, brake, coast with PWM speed
- [ ] `ARM-CID.01c` — Implement timed-distance control (calibrated mm/sec at given PWM duty)
- [ ] `ARM-CID.01d` — Implement stall/jam detection via current sense ADC
- [ ] `ARM-CID.01e` — Implement SPI command handler: DISPENSE, HOME, STATUS for each tray
- [ ] `ARM-CID.01f` — Test with loaded trays: verify dispensing accuracy and jam detection

---

### ARM-SLD.01: SLD hardware control — peristaltic pumps, valves, load cells
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P0
- **Points:** 5
- **GitHub:** [#127](https://github.com/manasXP/epicura/issues/127)
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** [[ARM-actuation#ARM-SLD.02|ARM-SLD.02]], [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]], [[ARM-actuation#ARM-CAL.01|ARM-CAL.01]]

**Acceptance Criteria:**
- [ ] 2× peristaltic pumps driven via TB6612FNG: PWM speed control (forward only)
- [ ] 2× NC solenoid valves (one per reservoir) for drip prevention when idle
- [ ] 2× HX711 load cells (one per reservoir) read at 10 Hz for level monitoring
- [ ] Load cell tare and calibrate functions implemented

**Tasks:**
- [ ] `ARM-SLD.01a` — Configure TB6612FNG control: AIN1, AIN2, PWMA for each pump
- [ ] `ARM-SLD.01b` — Implement peristaltic pump driver with PWM speed control
- [ ] `ARM-SLD.01c` — Configure solenoid valve GPIO; implement open/close with pump interlocking
- [ ] `ARM-SLD.01d` — Implement HX711 SPI driver; tare and calibrate load cells

---

### ARM-SLD.02: SLD dispensing and monitoring — closed-loop dispense, level alerts, priming
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P0
- **Points:** 3
- **GitHub:** [#128](https://github.com/manasXP/epicura/issues/128)
- **Blocked by:** [[ARM-actuation#ARM-SLD.01|ARM-SLD.01]]
- **Blocks:** [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]], [[ARM-actuation#ARM-CAL.01|ARM-CAL.01]]

**Acceptance Criteria:**
- [ ] Closed-loop dispensing: pump until load cell detects target weight change (±2g accuracy)
- [ ] Reservoir low-level alert: if load cell reads <100g, warn user via UI
- [ ] SPI commands implemented: DISPENSE(liquid_id, grams), LEVEL(liquid_id), PRIME(liquid_id)
- [ ] Priming routine: run pump for 5 seconds to fill tubing
- [ ] Dispensing accuracy tested: 10ml, 50ml, 100ml targets with actual vs target recorded

**Tasks:**
- [ ] `ARM-SLD.02a` — Implement closed-loop dispensing: start pump → monitor weight delta → stop at target
- [ ] `ARM-SLD.02b` — Implement reservoir level monitoring and low-level alert via MQTT
- [ ] `ARM-SLD.02c` — Implement SPI commands: DISPENSE, LEVEL, PRIME
- [ ] `ARM-SLD.02d` — Implement priming routine (run pump for 5 seconds to fill tubing)
- [ ] `ARM-SLD.02e` — Test dispensing accuracy: 10ml, 50ml, 100ml targets; record actual vs target

---

### ARM-CAL.01: Dispenser calibration — automated routines, persistent storage
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P1
- **Points:** 5
- **GitHub:** [#130](https://github.com/manasXP/epicura/issues/130)
- **Blocked by:** [[ARM-actuation#ARM-ASD.01|ARM-ASD.01]], [[ARM-actuation#ARM-CID.01|ARM-CID.01]], [[ARM-actuation#ARM-SLD.01|ARM-SLD.01]]
- **Blocks:** [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]]

**Acceptance Criteria:**
- [ ] P-ASD calibration: dispense 10 puffs per cartridge; measure average dose weight; store correction factor
- [ ] CID calibration: run actuator full travel; measure actual distance; store mm/sec calibration
- [ ] SLD calibration: dispense 100g water; compare load cell reading; store scale factor and offset
- [ ] Calibration data stored in STM32 flash (non-volatile); survives power cycles and OTA updates
- [ ] Calibration triggered via SPI command or UI maintenance screen
- [ ] Calibration results reported to CM5 and logged to PostgreSQL

**Tasks:**
- [ ] `ARM-CAL.01a` — Design calibration data structure: per-dispenser correction factors, last calibration timestamp
- [ ] `ARM-CAL.01b` — Implement P-ASD calibration routine: multi-puff test, weight measurement, factor calculation
- [ ] `ARM-CAL.01c` — Implement CID calibration routine: full-travel test, timing measurement
- [ ] `ARM-CAL.01d` — Implement SLD calibration routine: known-weight dispensing test
- [ ] `ARM-CAL.01e` — Implement flash storage for calibration data (STM32 flash page with wear leveling)
- [ ] `ARM-CAL.01f` — Implement SPI command: RUN_CALIBRATION(dispenser_id), GET_CALIBRATION(dispenser_id)

---

## Dependencies

### What ARM blocks (downstream consumers)

| ARM Story | Blocks | Reason |
|-----------|--------|--------|
| ARM-SRV.01 | ARM-SRV.02, RCP-FSM.01, INT-SYS.01 | Servo driver needed for feedback, recipe execution, and integration |
| ARM-SRV.02 | RCP-FSM.01, INT-SYS.01 | Stall detection and SPI commands needed for recipe execution |
| ARM-ASD.01 | ARM-ASD.02, RCP-DSP.01, ARM-CAL.01 | P-ASD hardware needed for dispensing sequence and calibration |
| ARM-ASD.02 | RCP-DSP.01, ARM-CAL.01 | Dispensing sequence needed for recipe dispensing and calibration |
| ARM-CID.01 | RCP-DSP.01, ARM-CAL.01 | CID needed for ingredient dispensing |
| ARM-SLD.01 | ARM-SLD.02, RCP-DSP.01, ARM-CAL.01 | SLD hardware needed for dispensing logic and calibration |
| ARM-SLD.02 | RCP-DSP.01, ARM-CAL.01 | Closed-loop dispensing needed for recipe dispensing and calibration |
| ARM-CAL.01 | RCP-DSP.01 | Calibration needed for accurate dispensing |

### What blocks ARM (upstream dependencies)

| ARM Story | Blocked by | Reason |
|-----------|------------|--------|
| ARM-SRV.01 | EMB-SET.01, EMB-COM.01 | Need STM32 HAL + SPI bridge |
| ARM-SRV.02 | ARM-SRV.01 | Need servo driver for feedback and commands |
| ARM-ASD.01 | EMB-SET.01 | Need STM32 GPIO, PWM, I2C, ADC |
| ARM-ASD.02 | ARM-ASD.01 | Need P-ASD hardware for dispensing sequence |
| ARM-CID.01 | EMB-SET.01 | Need STM32 GPIO, PWM, ADC |
| ARM-SLD.01 | EMB-SET.01 | Need STM32 PWM, GPIO, SPI (HX711) |
| ARM-SLD.02 | ARM-SLD.01 | Need SLD hardware for dispensing and monitoring |
| ARM-CAL.01 | ARM-ASD.01, ARM-CID.01, ARM-SLD.01 | Need all dispensers working |

---

## References

- [[__Workspaces/Epicura/docs/05-Subsystems/02-Robotic-Arm|Robotic Arm Subsystem]]
- [[__Workspaces/Epicura/docs/05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing Subsystem]]
- [[__Workspaces/Epicura/docs/08-Components/02-Actuation-Components|Actuation Components BOM]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
