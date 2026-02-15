---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
tags: [epicura, state-machine, software-architecture, recipe-engine]
---

# Main Loop State Machine

This document describes the main cooking loop state machine and how each state drives behavior across the three system layers: **UI** (Kivy touchscreen), **Controller** (Recipe Engine on CM5), and **Driver** (STM32 FreeRTOS).

> [!note] Related
> See [[02-Controller-Software-Architecture|Controller Software Architecture]] for the overall dual-processor design, recipe YAML format, and CV pipeline details.

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> LOADING : User selects recipe
    LOADING --> AWAITING_LOAD : Recipe validated
    LOADING --> ERROR : Parse/validation failure

    AWAITING_LOAD --> PREHEATING : All dispensers loaded (weight confirmed)
    AWAITING_LOAD --> IDLE : User cancels

    PREHEATING --> DISPENSING : Target temp reached
    PREHEATING --> ERROR : Thermal fault / timeout

    DISPENSING --> COOKING : Dispense complete (weight verified)
    DISPENSING --> ERROR : Dispenser jam / weight mismatch

    COOKING --> MONITORING : Cook timer elapsed or CV trigger
    COOKING --> PAUSED : User pause or safety warning

    MONITORING --> TRANSITIONING : Stage complete (CV pass or timer fallback)
    MONITORING --> COOKING : Not ready, continue cooking
    MONITORING --> ERROR : CV anomaly detected

    TRANSITIONING --> PREHEATING : Next stage needs different temp
    TRANSITIONING --> DISPENSING : Next stage needs new ingredients
    TRANSITIONING --> COMPLETING : Final stage done

    COMPLETING --> IDLE : Session logged, user dismissed

    PAUSED --> COOKING : User resumes
    PAUSED --> IDLE : User cancels cook
    PAUSED --> ERROR : Timeout in paused state (>30 min)

    ERROR --> IDLE : User aborts
    ERROR --> COOKING : User retries (recoverable)
    ERROR --> E_STOP : Critical fault escalation

    E_STOP --> IDLE : Manual hardware reset

    note right of E_STOP : Hardware relay cut.\nRequires physical reset.
```

---

## State-Layer Impact Table

| State | UI (Kivy) | Controller (CM5 Recipe Engine) | Driver (STM32) |
|-------|-----------|-------------------------------|----------------|
| **IDLE** | Recipe browser, cook history, settings | Waiting for recipe selection | Sensors polling at 1 Hz, heartbeat to CM5, safety idle checks |
| **LOADING** | "Validating recipe..." spinner | Parse YAML, resolve ingredient list, check dispenser mapping | No change from IDLE |
| **AWAITING_LOAD** | Checklist UI: "Load onions in CID-1 ✓", live weight readout per slot | Monitor load cell readings via bridge service, compare against recipe requirements | Report load cell weights on poll request |
| **PREHEATING** | Progress bar (current temp → target), ETA countdown | Send `SET_TEMP(target, ramp_rate)` via bridge, poll telemetry at 2 Hz | PID ramp-up, CAN `SET_POWER` command to induction surface, report temp |
| **DISPENSING** | "Dispensing oil (30 g)..." with live weight bar | Send `DISPENSE_SLD(channel, target_g)` or `DISPENSE_CID(tray)`, verify ACK, monitor weight convergence | Actuate pumps/servos/actuators, stream load cell delta, report completion ACK |
| **COOKING** | Timer countdown, live temp graph, stir pattern indicator | Send `SET_STIR(pattern, speed)`, maintain temp setpoint, trigger CV capture at 2 Hz | PID hold temperature, PWM servo pattern execution, report telemetry |
| **MONITORING** | CV confidence overlay on camera feed, "Analyzing..." indicator | Run TFLite inference on latest frame, evaluate `cv_check` condition, apply timer fallback | Continue current PID + stir setpoints unchanged |
| **TRANSITIONING** | "Stage 3/6 complete — next: Add Dal", brief animation | Compute next stage parameters from YAML, send new `SET_TEMP` / `DISPENSE` commands | Ramp temp to new target, stop or change stir pattern |
| **COMPLETING** | "Cooking Complete!" summary card, rating prompt, share option | Log session to PostgreSQL, publish MQTT `cook/complete`, compute nutrition estimate | Heater OFF (CAN `SET_POWER(0)`), stir OFF, exhaust fan cooldown ramp |
| **PAUSED** | "Paused" overlay with resume / cancel buttons, elapsed pause timer | Suspend stage timer, hold current setpoints, log pause event | Hold current temp at reduced power (50%), stir OFF |
| **ERROR** | Error description banner, retry / skip stage / abort buttons | Classify error (recoverable vs critical), determine recovery options, log to DB | Depends on error: reduce power, stop dispensing, or hold safe state |
| **E_STOP** | Full-screen red alert: "Emergency Stop — Reset Required" | Log event with full telemetry snapshot, await manual reset GPIO signal | Cut heater relay (hardware), brake servo, activate buzzer, all outputs safe |

---

## Sequence Diagram: Single Cooking Stage

The following shows message flow for a typical "Add Spices" stage from the Dal Tadka recipe (stage 3: add cumin seeds to hot oil).

```mermaid
sequenceDiagram
    participant UI as UI (Kivy)
    participant RE as Recipe Engine
    participant BR as CM5-STM32 Bridge
    participant MC as STM32 (FreeRTOS)

    RE->>RE: Load stage 3 from YAML
    RE->>UI: state=DISPENSING, msg="Dispensing cumin (5g)"

    RE->>BR: DISPENSE_ASD(hopper=1, grams=5)
    BR->>MC: SPI frame [CMD=0x30, hopper=1, target=5g]
    MC->>MC: Open servo gate, monitor load cell
    MC-->>BR: SPI frame [ACK, weight=4.8g]
    BR-->>RE: dispense_ack(weight=4.8g)

    RE->>RE: Weight within ±10% tolerance → OK
    RE->>UI: state=COOKING, msg="Cooking 45s at 180°C"

    RE->>BR: SET_TEMP(180), SET_STIR(pattern=CIRCULAR, speed=40)
    BR->>MC: SPI frame [CMD=0x10, temp=180]
    BR->>MC: SPI frame [CMD=0x20, pattern=CIRCULAR, speed=40]
    MC->>MC: PID loop active, servo PWM running

    loop Every 500ms
        MC-->>BR: SPI telemetry [temp=178, stir_ok, weight=stable]
        BR-->>RE: telemetry(temp=178)
        RE->>UI: update temp graph
    end

    RE->>RE: Timer=45s elapsed
    RE->>UI: state=MONITORING, msg="Analyzing..."

    RE->>RE: Capture frame, run TFLite inference
    RE->>RE: cv_result=cumin_toasted (confidence=0.87)

    RE->>UI: state=TRANSITIONING, msg="Stage 3/6 done — next: Add onions"
    RE->>BR: SET_TEMP(160)
    BR->>MC: SPI frame [CMD=0x10, temp=160]
```

---

## Transition Trigger Table

| From | To | Trigger | Details |
|------|----|---------|---------|
| IDLE | LOADING | User action | User taps recipe and confirms "Start Cook" |
| LOADING | AWAITING_LOAD | Validation pass | YAML parsed, all ingredients mapped to dispensers |
| LOADING | ERROR | Validation fail | Missing ingredient, unsupported dispenser, corrupt YAML |
| AWAITING_LOAD | PREHEATING | Weight confirmed | All required dispenser slots report weight ≥ recipe minimum |
| AWAITING_LOAD | IDLE | User cancel | User taps "Cancel" before loading |
| PREHEATING | DISPENSING | Temp threshold | IR sensor reads within ±5°C of stage target for 3 consecutive readings |
| PREHEATING | ERROR | Timeout / fault | Temp not reached within `preheat_timeout` (default 300 s) or NTC over-temp |
| DISPENSING | COOKING | Weight converged | Load cell delta matches target ±10%, or fixed dispense time elapsed |
| DISPENSING | ERROR | Jam / mismatch | No weight change after actuation, or weight exceeds 150% of target |
| COOKING | MONITORING | Timer / CV | `duration_seconds` elapsed, or periodic CV check interval reached |
| COOKING | PAUSED | User / safety | User taps pause, or non-critical safety warning (e.g., lid open) |
| MONITORING | TRANSITIONING | Stage complete | `cv_check` condition met (confidence ≥ threshold) or timer fallback expired |
| MONITORING | COOKING | Not ready | CV confidence below threshold, resume cooking with same setpoints |
| MONITORING | ERROR | CV anomaly | Anomaly detected (e.g., smoke, empty vessel, unexpected color) |
| TRANSITIONING | PREHEATING | Temp change needed | Next stage `temp_target` differs by >10°C from current |
| TRANSITIONING | DISPENSING | New ingredients | Next stage has `ingredients` list to dispense |
| TRANSITIONING | COMPLETING | Last stage | No more stages in recipe YAML |
| COMPLETING | IDLE | Session end | Log written, user dismisses summary or 5 min auto-return |
| PAUSED | COOKING | User resume | User taps "Resume" |
| PAUSED | IDLE | User cancel | User taps "Cancel Cook" during pause |
| PAUSED | ERROR | Pause timeout | Paused longer than 30 min without action |
| ERROR | IDLE | User abort | User taps "Abort" — session logged as incomplete |
| ERROR | COOKING | User retry | Recoverable error — user taps "Retry", controller re-sends last command |
| ERROR | E_STOP | Critical fault | Thermal runaway, CAN bus failure, or repeated unrecoverable error |
| E_STOP | IDLE | Hardware reset | Physical reset button pressed, watchdog confirms safe state |

---

## Related Documentation

- [[02-Controller-Software-Architecture|Controller Software Architecture]] — Recipe YAML format, CV pipeline, PID tuning
- [[08-Tech-Stack|Tech Stack]] — Yocto, Kivy, FreeRTOS, Docker stack
- [[../../04-UserInterface/03-UI-UX-Design|UI/UX Design]] — Touchscreen wireframes and screen flows
- [[../../05-Subsystems/09-Induction-Heating|Induction Heating]] — PID control and CAN bus protocol
- [[../../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing]] — ASD/CID/SLD subsystem details

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
