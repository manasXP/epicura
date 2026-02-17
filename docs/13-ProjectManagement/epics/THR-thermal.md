---
tags: [epicura, project-management, epic, thermal, induction, pid]
created: 2026-02-16
aliases: [THR Epic, Thermal Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 4 stories across Sprints 3–4 |
> | 2026-02-17 | Manas Pradhan | Split CAN and PID stories (>5pts) — 6 stories across Sprints 3–4 |

# Epic: THR — Thermal & Induction Control

CAN bus interface to the commercial microwave induction surface, closed-loop PID temperature control using IR and NTC feedback, thermal safety interlocks, and PWM exhaust fan control. Owned by **Embedded Engineer**.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| CAN — Induction CAN Interface | 2 | 8 | 3 |
| PID — Temperature Control | 2 | 8 | 3–4 |
| SAF — Thermal Safety | 1 | 5 | 4 |
| EXH — Exhaust Fan Control | 1 | 5 | 4 |
| **Total** | **6** | **~28** | |

---

## Phase 1 — Thermal Control (Sprints 3–4)

### THR-CAN.01: CAN bus driver — FDCAN1 init, TX power command, RX status parsing
- **Sprint:** [[sprint-03|Sprint 3]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** [[THR-thermal#THR-CAN.02|THR-CAN.02]], [[THR-thermal#THR-PID.01|THR-PID.01]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]

**Acceptance Criteria:**
- [ ] FDCAN1 initialized at 500 kbps with correct bit timing for STM32G474
- [ ] CAN TX: power level command (0–100%) sent to induction module at 10 Hz
- [ ] CAN RX: module status (power, fault codes, coil temperature) parsed correctly

**Tasks:**
- [ ] `THR-CAN.01a` — Configure FDCAN1 peripheral: 500 kbps, 11-bit standard ID, FIFO0 for RX
- [ ] `THR-CAN.01b` — Implement CAN TX function: pack power level into CAN frame; send at 10 Hz
- [ ] `THR-CAN.01c` — Implement CAN RX callback: parse status frames, update shared telemetry struct

---

### THR-CAN.02: CAN bus error handling and induction commands — bus-off recovery, power ramp, e-stop
- **Sprint:** [[sprint-03|Sprint 3]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[THR-thermal#THR-CAN.01|THR-CAN.01]]
- **Blocks:** [[THR-thermal#THR-PID.01|THR-PID.01]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]

**Acceptance Criteria:**
- [ ] CAN error handling: bus-off auto-recovery, error frame counting, fault reporting
- [ ] Power ramp: smooth 0→100% ramp in 5 seconds without CAN bus errors
- [ ] Module emergency stop via CAN command verified
- [ ] Full command set implemented: SET_POWER, GET_STATUS, EMERGENCY_STOP

**Tasks:**
- [ ] `THR-CAN.02a` — Implement CAN error handler: bus-off auto-recovery, error counter monitoring
- [ ] `THR-CAN.02b` — Implement induction module command set: SET_POWER, GET_STATUS, EMERGENCY_STOP
- [ ] `THR-CAN.02c` — Test with induction module: power ramp, status read, e-stop command

---

### THR-PID.01: PID controller — sensor drivers, closed-loop temperature control
- **Sprint:** [[sprint-03|Sprint 3]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-COM.01|EMB-COM.01]], [[THR-thermal#THR-CAN.01|THR-CAN.01]]
- **Blocks:** [[THR-thermal#THR-PID.02|THR-PID.02]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]], [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] MLX90614 IR thermometer read via I2C at 10 Hz; value fed to PID as process variable
- [ ] NTC thermistors (coil + ambient) read via ADC at 10 Hz with Steinhart-Hart conversion
- [ ] PID loop runs at 100 Hz in dedicated FreeRTOS task (highest priority); default gains Kp=2.0, Ki=0.5, Kd=0.1
- [ ] Anti-windup: integral term clamped when output saturated
- [ ] PID output (0–100%) maps to CAN power command with rate limiting (max 10%/sec change)

**Tasks:**
- [ ] `THR-PID.01a` — Implement MLX90614 I2C driver: object temperature read, emissivity config
- [ ] `THR-PID.01b` — Implement NTC ADC reading with Steinhart-Hart equation for temperature conversion
- [ ] `THR-PID.01c` — Implement PID controller: proportional, integral (with anti-windup), derivative (with low-pass filter)
- [ ] `THR-PID.01d` — Map PID output to CAN power command; implement output rate limiting (max 10%/sec change)

---

### THR-PID.02: PID tuning and telemetry — gain storage, SPI reporting, performance validation
- **Sprint:** [[sprint-03|Sprint 3]] → [[sprint-04|Sprint 4]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[THR-thermal#THR-PID.01|THR-PID.01]]
- **Blocks:** [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]], [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] PID gains stored in STM32 flash; adjustable via SPI command from CM5
- [ ] PID telemetry (setpoint, PV, output, error) published to CM5 at 1 Hz via SPI
- [ ] Steady-state error ≤ ±5°C at target temperatures (80°C, 120°C, 180°C)

**Tasks:**
- [ ] `THR-PID.02a` — Store PID gains in STM32 flash; implement SPI command to read/write gains
- [ ] `THR-PID.02b` — Implement telemetry struct: setpoint, PV (IR), PV (NTC), output, error, integral; send via SPI at 1 Hz
- [ ] `THR-PID.02c` — Test PID performance: step response to 80°C, 120°C, 180°C; measure overshoot and settling time

---

### THR-SAF.01: Thermal safety interlocks — runaway detection, coil overtemp, pan detection
- **Sprint:** [[sprint-04|Sprint 4]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SAF.01|EMB-SAF.01]], [[THR-thermal#THR-PID.01|THR-PID.01]]
- **Blocks:** [[INT-integration#INT-SAF.01|INT-SAF.01]]

**Acceptance Criteria:**
- [ ] Thermal runaway detection: if temperature rises >20°C/min above setpoint, trigger ALERT
- [ ] Coil overtemperature: if NTC reads >150°C, immediately cut induction power
- [ ] Pan detection: if IR reads <30°C after 30 seconds at >50% power, assume no pan → shutdown
- [ ] All thermal faults logged with timestamp, readings, and action taken
- [ ] Recovery from ALERT requires temperature to return to setpoint ±10°C for 30 seconds
- [ ] Safety interlocks cannot be bypassed via software command

**Tasks:**
- [ ] `THR-SAF.01a` — Implement thermal runaway detector: rolling 60-second temperature gradient calculation
- [ ] `THR-SAF.01b` — Implement coil overtemperature check in Sensor task; direct GPIO to safety relay
- [ ] `THR-SAF.01c` — Implement pan detection logic: timeout-based IR temperature check
- [ ] `THR-SAF.01d` — Implement fault logging: circular buffer in SRAM, dump via UART on request
- [ ] `THR-SAF.01e` — Test all thermal safety paths with simulated sensor values

---

### THR-EXH.01: PWM exhaust fan control — temperature-proportional speed, grease filter monitor
- **Sprint:** [[sprint-04|Sprint 4]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Exhaust fan speed proportional to cooking temperature (0% at <60°C, 100% at >180°C)
- [ ] Fan startup ramp: 0→target speed over 2 seconds to avoid inrush current
- [ ] Fan continues running 60 seconds after cooking ends (cool-down period)
- [ ] Fan RPM feedback via tachometer input (if available) or open-loop PWM
- [ ] Fan failure alert: if expected airflow not detected, warn user via UI

**Tasks:**
- [ ] `THR-EXH.01a` — Configure TIM PWM channel for fan motor; set 25 kHz PWM frequency
- [ ] `THR-EXH.01b` — Implement temperature-to-speed mapping curve (piecewise linear)
- [ ] `THR-EXH.01c` — Implement startup ramp and cool-down timer logic
- [ ] `THR-EXH.01d` — Implement fan failure detection (tachometer or current sensing)
- [ ] `THR-EXH.01e` — Test fan control across temperature range; verify noise levels acceptable

---

## Dependencies

### What THR blocks (downstream consumers)

| THR Story | Blocks | Reason |
|-----------|--------|--------|
| THR-CAN.01 | THR-CAN.02, THR-PID.01, RCP-FSM.01 | CAN driver needed for error handling, PID output, and recipe engine |
| THR-CAN.02 | THR-PID.01, RCP-FSM.01 | CAN commands needed for PID output and recipe engine |
| THR-PID.01 | THR-PID.02, RCP-FSM.01, INT-SYS.01 | Core PID needed for tuning, cooking, and integration |
| THR-PID.02 | RCP-FSM.01, INT-SYS.01 | Tuned PID with telemetry needed for cooking and integration |
| THR-SAF.01 | INT-SAF.01 | Thermal safety needed for certification |

### What blocks THR (upstream dependencies)

| THR Story | Blocked by | Reason |
|-----------|------------|--------|
| THR-CAN.01 | EMB-SET.01 | Need STM32 HAL and FDCAN peripheral |
| THR-CAN.02 | THR-CAN.01 | Need CAN driver for error handling and commands |
| THR-PID.01 | EMB-COM.01, THR-CAN.01 | Need bridge for telemetry + CAN for power output |
| THR-PID.02 | THR-PID.01 | Need core PID running for tuning and telemetry |
| THR-SAF.01 | EMB-SAF.01, THR-PID.01 | Need safety framework + PID running |
| THR-EXH.01 | EMB-SET.01 | Need STM32 PWM timer |

---

## References

- [[__Workspaces/Epicura/docs/05-Subsystems/01-Induction-Heating|Induction Heating Subsystem]]
- [[__Workspaces/Epicura/docs/05-Subsystems/05-Exhaust-Fume-Management|Exhaust & Fume Management]]
- [[__Workspaces/Epicura/docs/02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
