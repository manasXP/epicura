---
created: 2026-02-15
modified: 2026-02-15
version: 2.0
status: Draft
---

# Ingredient Dispensing System

## Overview

The ingredient dispensing system is divided into three purpose-built subsystems, each optimized for a different ingredient class. Together they surround the cooking pot and are orchestrated by the STM32 controller under commands from the CM5 recipe engine.

| Subsystem | Full Name | Purpose | Actuators | Metering |
|-----------|-----------|---------|-----------|----------|
| **ASD** | Advanced Seasoning Dispenser | Ground/powdered spices (turmeric, chili, salt, cumin powder, garam masala) | 3 Servo Motors (SG90) | Weight-verified via pot load cells |
| **CID** | Coarse Ingredients Dispenser | Pre-cut vegetables, meat, paneer, dal, rice | 2 Linear Actuators (slider mechanism) | Timed/position-based |
| **SLD** | Standard Liquid Dispenser | Oil and water | 2 Peristaltic Pumps + 2 Solenoid Valves + 1 Load Cell (dedicated) | Closed-loop weight feedback |

## Layout

### Top-View Arrangement

```
┌───────────────────────────────────────────────────────┐
│                    REAR OF UNIT                        │
│                                                        │
│       ┌──────────────────────────────────────┐         │
│       │           ASD (Seasonings)           │         │
│       │  ┌────────┐ ┌────────┐ ┌────────┐   │         │
│       │  │ ASD-1  │ │ ASD-2  │ │ ASD-3  │   │         │
│       │  │Turmeric│ │ Chili  │ │ Salt / │   │         │
│       │  │Powder  │ │Powder  │ │ Masala │   │         │
│       │  │(80 mL) │ │(80 mL) │ │(80 mL) │   │         │
│       │  └───┬────┘ └───┬────┘ └───┬────┘   │         │
│       └──────┼──────────┼──────────┼─────────┘         │
│              ▼          ▼          ▼                    │
│  ┌─────┐ ┌──────────────────────────────────┐ ┌─────┐ │
│  │ SLD │ │                                  │ │ SLD │ │
│  │Oil  │ │          COOKING POT             │ │Water│ │
│  │Pump │►│          (Center)                │◄│Pump │ │
│  │     │ │                                  │ │     │ │
│  └─────┘ └──────────────────────────────────┘ └─────┘ │
│              ▲                       ▲                  │
│       ┌──────┴───────────────────────┴─────────┐       │
│       │           CID (Coarse)                 │       │
│       │  ┌──────────────┐  ┌──────────────┐    │       │
│       │  │    CID-1     │  │    CID-2     │    │       │
│       │  │  Vegetables  │  │  Dal / Rice  │    │       │
│       │  │ / Meat (400mL│  │  / Paneer    │    │       │
│       │  │  tray)       │  │  (400mL tray)│    │       │
│       │  └──────────────┘  └──────────────┘    │       │
│       └────────────────────────────────────────┘       │
│                    FRONT OF UNIT                        │
└───────────────────────────────────────────────────────┘
```

### Side-View Cross Sections

**ASD (Servo-Gated Gravity Feed):**

```
       ┌───────────┐
       │ Seasoning  │
       │ (powder,   │
       │  gravity   │
       │  fed)      │
       │     ▼      │
       └─────┬──────┘
             │
       ┌─────┴──────┐
       │ Servo Gate │ ◄── SG90 rotates flap 90°
       └─────┬──────┘
             │
       ┌─────┴──────┐
       │ Chute /    │ ◄── 45° min angle
       │ Funnel     │
       └─────┬──────┘
             ▼
    ┌────────────────────┐
    │    COOKING POT     │
    └────────────────────┘
```

**CID (Linear Actuator Slider):**

```
       ┌──────────────────────────────────────┐
       │          TRAY (removable)            │
       │  ┌──────────────────────────┐        │
       │  │  Pre-cut ingredients     │  PUSH  │
       │  │  (vegetables, dal, etc.) │◄──PLATE│
       │  └──────────────┬───────────┘   │    │
       │                 │               │    │
       │                 ▼             ──┤    │
       │           ┌──────────┐     Linear    │
       │           │  Drop-off│     Actuator  │
       │           │  Edge    │     (12V DC)  │
       │           └─────┬────┘               │
       └─────────────────┼────────────────────┘
                         ▼
                ┌────────────────────┐
                │    COOKING POT     │
                └────────────────────┘
```

**SLD (Peristaltic Pump + Solenoid):**

```
    ┌──────────────┐
    │  Reservoir   │
    │  (Oil/Water) │
    │  500 mL      │
    └──────┬───────┘
           │ Silicone tube (6mm ID)
           ▼
    ┌──────────────┐
    │  Peristaltic │ ◄── 12V DC gear motor, PWM speed control
    │  Pump        │     Flow rate: 5-50 mL/min
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Solenoid    │ ◄── 12V NC solenoid, prevents drip when idle
    │  Valve       │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Nozzle      │ ──► Into cooking pot
    └──────────────┘

    ┌──────────────┐
    │  Load Cell   │ ◄── Dedicated HX711, measures reservoir weight
    │  (under      │     Closed-loop: pump until target Δweight reached
    │   reservoir) │
    └──────────────┘
```

## ASD — Advanced Seasoning Dispenser

### Compartment Specifications

| Parameter | Value |
|-----------|-------|
| Compartments | 3 (ASD-1, ASD-2, ASD-3) |
| Capacity | 80 mL each |
| Material | Food-grade PP (translucent) |
| Removable | Yes (lift-out for cleaning/refill) |
| Lid | Snap-fit with silicone gasket |
| Feed Type | Gravity-fed, tapered hopper with 45° minimum chute angle |
| Gate | SG90 servo rotates flap 90° (closed ↔ open) |

### Actuator: SG90 Micro Servo

| Parameter | Value |
|-----------|-------|
| Model | SG90 (or MG90S metal-gear upgrade) |
| Torque | 1.2 kg·cm @ 4.8V |
| Weight | 9g |
| PWM | 50 Hz, 500–2500 µs pulse |
| Supply | 5V from buck converter rail |
| Cost | ~$2 each |

### Anti-Clog Mechanisms

| Mechanism | Implementation | Trigger |
|-----------|---------------|---------|
| Vibration motors (3x) | Coin-type eccentric motor mounted on each ASD hopper (PC7, PD2, PA3) | 200 ms pulse before every dispense |
| Anti-bridging geometry | Tapered walls, rounded internal corners, 45° min angle | Passive |
| Retry logic | Close-open-close if no weight change after 3s | Auto on stall detection |
| Gate oscillation | Rapidly open/close servo 3× in 1s | After first retry fails |
| Vibration + oscillation | Simultaneous vibration motor pulse and servo oscillation | Final retry before error |

**Vibration Motor Specifications:**
- Type: ERM (Eccentric Rotating Mass), 3V nominal
- Driver: 2N7002 N-MOSFET with 10Ω current limit resistor
- Current: ~80-100 mA typical
- Pulse duration: 200 ms before dispense, 500 ms during retry
- One motor per ASD hopper ensures targeted anti-clog action

### Metering Strategy

ASD uses the **pot load cells** (4× 5 kg Wheatstone bridge under the cooking pot) for weight verification:

1. Tare pot weight → W_initial
2. Open ASD-N servo gate
3. Monitor pot weight at 10 Hz: W_delta = W_current − W_initial
4. Close gate when W_delta ≥ target × 0.90 (early close for in-flight powder)
5. Log actual dispensed weight

Accuracy: ±10% of target weight.

## CID — Coarse Ingredients Dispenser

### Tray Specifications

| Parameter | Value |
|-----------|-------|
| Trays | 2 (CID-1, CID-2) |
| Capacity | 400 mL each (shallow tray, ~200×100×20 mm) |
| Material | Food-grade PP (removable, dishwasher-safe) |
| Removable | Yes (slide-out tray) |
| Ingredient Types | Pre-cut vegetables, meat, paneer, dal, rice |

### Actuator: Linear Actuator (Push-Plate Slider)

| Parameter | Value |
|-----------|-------|
| Type | 12V DC linear actuator, 50 mm stroke |
| Force | 20–50 N (sufficient to push 500g of chopped vegetables) |
| Speed | ~10 mm/s |
| Control | H-bridge motor driver (DRV8876RGTR), EN/PH direction + PWM |
| Position Feedback | Limit switches at home and full-extend positions |
| Supply | 12V from PSU rail |
| Cost | ~$8 each |

### Dispensing Mechanism

The push-plate slides along the tray, sweeping ingredients off the drop-off edge into the pot:

1. CM5 sends CID dispense command with tray ID
2. STM32 drives linear actuator forward at controlled speed
3. Ingredients fall off tray edge into pot
4. Actuator reaches full-extend limit switch → retract to home
5. Dispense confirmed by limit switch + optional pot weight check

### Metering Strategy

CID uses **position-based / timed dispensing**:

- Full push = entire tray contents dumped at once (typical usage)
- Partial push = actuator extends to a specified position (for partial dispense)
- No closed-loop weight verification (coarse items are pre-measured by user when loading tray)

## SLD — Standard Liquid Dispenser

### Channel Specifications

| Parameter | Oil Channel (SLD-OIL) | Water Channel (SLD-WATER) |
|-----------|----------------------|--------------------------|
| Reservoir | 200 mL food-grade PP bottle | 500 mL food-grade PP bottle |
| Tube | 6 mm ID food-grade silicone | 6 mm ID food-grade silicone |
| Pump | 12V DC peristaltic, 5–50 mL/min | 12V DC peristaltic, 5–50 mL/min |
| Valve | 12V NC solenoid (drip prevention) | 12V NC solenoid (drip prevention) |
| Nozzle | Directed into pot center | Directed into pot center |

### Actuators

**Peristaltic Pump (×2):**

| Parameter | Value |
|-----------|-------|
| Type | Peristaltic roller pump, 12V DC gear motor |
| Tube | Food-grade silicone, 6 mm ID |
| Flow Rate | 5–50 mL/min (adjustable via PWM motor speed) |
| Accuracy | ±2% volumetric (further refined by load cell) |
| Advantage | Self-priming, no contamination (fluid only touches tube), reversible |
| Cost | ~$10 each |

**Solenoid Valve (×2):**

| Parameter | Value |
|-----------|-------|
| Type | 12V DC, normally closed, spring return |
| Response | <50 ms open/close |
| Purpose | Prevent dripping when pump is off |
| Power | ~5W when energized |
| Driver | N-channel MOSFET (IRLZ44N) with flyback diode |
| Cost | ~$4 each |

### Dedicated Load Cell

| Parameter | Value |
|-----------|-------|
| Type | Single 1 kg strain gauge under SLD reservoir platform |
| ADC | Dedicated HX711 (separate from pot load cells) |
| Purpose | Measure liquid dispensed by tracking reservoir weight decrease |
| Accuracy | ±1 g (24-bit HX711 with averaging) |
| Sampling | 10 Hz |
| Cost | ~$5 (load cell) + ~$3 (HX711) |

### Metering Strategy (Closed-Loop)

SLD uses a **dedicated load cell** under the reservoir platform for closed-loop dispensing:

```
┌───────────────┐
│ 1. Tare       │
│ reservoir     │──► W_initial = sld_load_cell.read()
│ weight        │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 2. Open       │
│ solenoid +    │──► solenoid[channel].open()
│ start pump    │    pump[channel].start(speed)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 3. Monitor    │
│ reservoir     │──► W_dispensed = W_initial - sld_load_cell.read()
│ weight loss   │    (sampled at 10 Hz)
│ in real-time  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 4. Stop pump  │
│ + close       │──► IF W_dispensed >= target_g * 0.95:
│ solenoid when │        pump[channel].stop()
│ target reached│        solenoid[channel].close()
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 5. Verify     │
│ final weight  │──► W_actual = W_initial - sld_load_cell.read()
│ and log       │    log(channel, target_g, W_actual)
└───────────────┘
```

Accuracy: ±5% of target weight (significantly better than ASD due to dedicated load cell and controllable flow rate).

## STM32 Control Interface

### GPIO and PWM Assignments

| Subsystem | Actuator | STM32 Pin | Interface | Notes |
|-----------|----------|-----------|-----------|-------|
| **ASD** | Servo ASD-1 | PA0 (TIM2_CH1) | PWM 50 Hz | SG90, 500–2500 µs pulse |
| **ASD** | Servo ASD-2 | PA1 (TIM2_CH2) | PWM 50 Hz | SG90, 500–2500 µs pulse |
| **ASD** | Servo ASD-3 | PA2 (TIM2_CH3) | PWM 50 Hz | SG90, 500–2500 µs pulse |
| **ASD** | Vibration Motor 1 | PC7 (GPIO) | Digital output via MOSFET | 5V ERM motor, hopper 1 anti-clog |
| **ASD** | Vibration Motor 2 | PD2 (GPIO) | Digital output via MOSFET | 5V ERM motor, hopper 2 anti-clog |
| **ASD** | Vibration Motor 3 | PA3 (GPIO) | Digital output via MOSFET | 5V ERM motor, hopper 3 anti-clog |
| **CID** | Linear Actuator CID-1 EN | PA10 (TIM1_CH3/GPIO) | PWM/GPIO | DRV8876 #1 enable/speed |
| **CID** | Linear Actuator CID-1 PH | PB4 (GPIO) | Digital output | DRV8876 #1 phase/direction |
| **CID** | Linear Actuator CID-2 EN | PB5 (GPIO) | PWM/GPIO | DRV8876 #2 enable/speed |
| **CID** | Linear Actuator CID-2 PH | PC2 (GPIO) | Digital output | DRV8876 #2 phase/direction |
| **SLD** | Pump Motor SLD-OIL (PWM) | PC3 (GPIO) | PWM (motor speed) | TB6612 PWMA via MOSFET |
| **SLD** | Pump Motor SLD-OIL (DIR) | PC4 (GPIO) | Digital output | TB6612 AIN1 direction |
| **SLD** | Pump Motor SLD-WATER (PWM) | PC5 (GPIO) | PWM (motor speed) | TB6612 PWMB via MOSFET |
| **SLD** | Pump Motor SLD-WATER (DIR) | PC6 (GPIO) | Digital output | TB6612 BIN1 direction |
| **SLD** | Solenoid SLD-OIL | PA7 (GPIO) | Digital output via MOSFET | 12V NC solenoid, flyback diode |
| **SLD** | Solenoid SLD-WATER | PA9 (GPIO) | Digital output via MOSFET | 12V NC solenoid, flyback diode |
| **SLD** | HX711 SCK (dedicated) | PC11 (GPIO) | Clock out | SLD reservoir load cell (not implemented in current design) |
| **SLD** | HX711 DOUT (dedicated) | PC12 (GPIO) | Data in | SLD reservoir load cell (not implemented in current design) |

> **Note:** Pot load cells remain on PC0/PC1 (existing allocation). Pin assignments match [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]] document. Vibration motors are part of the ASD anti-clog mechanism — one motor per hopper vibrates powder before dispensing.

### Dispensing Command Protocol (CM5 → STM32)

| Command | Code | Parameters | Response | Description |
|---------|------|------------|----------|-------------|
| DISPENSE_ASD | 0x30 | asd_id (1 byte: 1–3), target_weight_g (2 bytes) | ACK + actual_weight_g | Dispense seasoning via servo gate, weight-verified by pot load cells |
| DISPENSE_CID | 0x31 | cid_id (1 byte: 1–2), mode (1 byte: FULL/PARTIAL), position_mm (1 byte) | ACK + status | Push tray contents into pot via linear actuator |
| DISPENSE_SLD | 0x32 | channel (1 byte: OIL=1, WATER=2), target_weight_g (2 bytes) | ACK + actual_weight_g | Pump liquid, closed-loop via dedicated load cell |
| OPEN_GATE | 0x33 | subsystem (1 byte: ASD=1), gate_id (1 byte), duration_ms (2 bytes) | ACK | Timed gate open (manual override, ASD only) |
| CLOSE_GATE | 0x34 | subsystem (1 byte), gate_id (1 byte) | ACK | Force close gate/stop actuator |
| QUERY_WEIGHT | 0x35 | source (1 byte: POT=0, SLD=1) | weight_g (4 bytes) | Read weight from pot or SLD load cells |
| PREFLIGHT | 0x36 | subsystem_mask (1 byte) | status per subsystem | Check if required subsystems are loaded/ready |
| TARE | 0x37 | source (1 byte: POT=0, SLD=1) | ACK | Zero the specified load cell readings |

## Clog Prevention (ASD)

### Clog Detection and Recovery Flow

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Open Servo   │────►│ Wait 3s,      │────►│ Pot Weight   │
│ Gate         │     │ Monitor Weight │     │ Changed?     │
└──────────────┘     └───────────────┘     └──────┬───────┘
                                                   │
                                          Yes ◄────┴────► No
                                           │              │
                                           ▼              ▼
                                    ┌──────────┐   ┌──────────────┐
                                    │ Continue │   │ Retry #1:    │
                                    │ Normally │   │ Close + Open │
                                    └──────────┘   └──────┬───────┘
                                                          │
                                                          ▼
                                                   ┌──────────────┐
                                                   │ Pot Weight   │
                                                   │ Changed?     │
                                                   └──────┬───────┘
                                                          │
                                                 Yes ◄────┴────► No
                                                  │              │
                                                  ▼              ▼
                                           ┌──────────┐   ┌──────────────┐
                                           │ Continue │   │ Retry #2:    │
                                           │ Normally │   │ Vibrate +    │
                                           └──────────┘   │ Oscillate    │
                                                          └──────┬───────┘
                                                                 │
                                                                 ▼
                                                          ┌──────────────┐
                                                          │ Pot Weight   │
                                                          │ Changed?     │
                                                          └──────┬───────┘
                                                                 │
                                                        Yes ◄────┴────► No
                                                         │              │
                                                         ▼              ▼
                                                  ┌──────────┐   ┌──────────┐
                                                  │ Continue │   │ CLOG     │
                                                  │ Normally │   │ ERROR    │
                                                  └──────────┘   │ Alert    │
                                                                 │ User     │
                                                                 └──────────┘
```

## Metering Accuracy Summary

| Factor | ASD Impact | CID Impact | SLD Impact | Mitigation |
|--------|-----------|-----------|-----------|------------|
| In-flight material | Powder still falling when gate closes | N/A (push mechanism) | Fluid in tube after pump stops | ASD: close at 90% target. SLD: close at 95% target |
| Load cell noise | ±3 g at 10 Hz (pot cells) | N/A | ±1 g (dedicated cell) | Moving average filter (3 samples) |
| Vibration | Arm motor affects pot weight | N/A | Dedicated cell isolated from pot | Pause arm during ASD dispensing |
| Sticky ingredients | Powder adheres to gate | Pieces stick to tray | Oil residue in tube | ASD: vibration + anti-stick coating. CID: angled tray. SLD: tube replacement |
| Fill level variance | Gravity rate varies with hopper level | N/A | Pump rate independent of level | ASD: tapered hopper geometry |

## Recipe Integration

### Dispensing Sequence Example (Dal Tadka)

```
Step 1:  DISPENSE_SLD(OIL, 30g)                ──► Oil into hot pot
Step 2:  Wait for sear temp (200°C)             ──► IR sensor confirms
Step 3:  DISPENSE_ASD(ASD-1, 3g)               ──► Turmeric powder
Step 4:  DISPENSE_ASD(ASD-2, 5g)               ──► Chili powder
Step 5:  Stir briefly                           ──► Arm mixes spices into oil
Step 6:  DISPENSE_CID(CID-1, FULL)             ──► Chopped onions, tomatoes
Step 7:  Wait for browning (CV detection)       ──► Camera detects golden color
Step 8:  DISPENSE_ASD(ASD-3, 5g)               ──► Salt + garam masala
Step 9:  DISPENSE_CID(CID-2, FULL)             ──► Toor dal (200g, pre-measured)
Step 10: DISPENSE_SLD(WATER, 400g)              ──► Water
Step 11: Simmer until done (CV + timer)         ──► Camera detects thickening
```

### Ingredient Loading Configuration

Users configure subsystem contents when loading ingredients before cooking:

| Field | Example Value | Source |
|-------|---------------|--------|
| Subsystem | ASD-2 | Fixed by hardware position |
| Ingredient Name | "Chili Powder" | From recipe ingredient list |
| Target Weight (g) | 5 | From recipe (adjusted for servings) |
| Pre-loaded | Yes/No | User confirms via touchscreen or app |

### Pre-Flight Check

Before starting a recipe, the system verifies all required subsystems:

1. **ASD:** Check pot weight change when each hopper is tapped (vibration motor pulse) — confirms powder present
2. **CID:** User confirms tray loaded via touchscreen (no automatic check — visual confirmation)
3. **SLD:** Read dedicated load cell — compare reservoir weight to minimum required for recipe
4. Display subsystem status on UI: loaded / insufficient / empty
5. Block recipe start if any required subsystem is insufficient

## Food Safety

### Temperature and Hold Time

| Consideration | Guideline | Implementation |
|--------------|-----------|----------------|
| Compartment Temperature | Ambient (no active heating or cooling) | Passive, ingredients at room temperature |
| Maximum Hold Time | 2 hours recommended for perishables | Timer starts when user loads, alert at 90 min |
| Allergen Cross-Contamination | Dedicated subsystems per ingredient type | ASD: dry spices only. CID: separate trays. SLD: separate tubes per liquid |
| Raw Meat Handling | CID-1 designated for raw protein | Tray labeled, separate drop zone, cleaning reminder after use |

### Contamination Prevention

- ASD: each hopper has a dedicated chute/funnel (no shared paths)
- CID: each tray drops into a distinct zone of the pot (no shared surfaces)
- SLD: fluid only contacts silicone tubing (per-channel, no shared path)
- All removable parts are smooth, non-porous food-grade PP
- Silicone pump tubing is replaceable (recommended every 3 months or 200 cycles)

## Cleaning Design

### Removable Components

| Component | Removal Method | Dishwasher Safe | Cleaning Frequency |
|-----------|----------------|-----------------|-------------------|
| ASD Hoppers (×3) | Lift out from top | Yes | After every use |
| ASD Hopper Lids (×3) | Snap-off | Yes | After every use |
| ASD Chute/Funnel Inserts (×3) | Pull out from below | Yes | After every use |
| CID Trays (×2) | Slide out from front | Yes | After every use |
| SLD Reservoirs (×2) | Lift out | Yes | After every use |
| SLD Silicone Tubing (×2) | Disconnect at quick-fit couplings | Hand wash (boil sterilize) | Weekly; replace every 3 months |
| SLD Nozzles (×2) | Unscrew | Yes | After every use |
| Servo Flap Assembly (ASD) | Not user-removable | No | Wipe-down weekly |
| Linear Actuator / Push-Plate (CID) | Not user-removable | No | Wipe-down weekly |
| Solenoid Valve Assembly (SLD) | Not user-removable | No | Wipe-down weekly |

### Auto-Rinse Cycle

For quick cleaning of SLD channels between recipes:

1. User fills SLD-WATER reservoir with warm water
2. Select "Rinse" mode on touchscreen
3. System runs pump through each SLD channel sequentially (water + oil lines)
4. Water flushes through tubing and nozzle into pot
5. User discards pot contents; repeat if needed

## Testing and Validation

### Test Procedures

| Test | Subsystem | Method | Pass Criteria |
|------|-----------|--------|---------------|
| Seasoning Accuracy | ASD | 10 trials per hopper, weigh dispensed amount vs. target | Within ±10% of target weight |
| Liquid Accuracy | SLD | 10 trials per channel, compare load cell reading to scale | Within ±5% of target weight |
| Coarse Dispense | CID | 10 trials, verify full tray contents dumped into pot | All contents reach pot, no spillage |
| Clog Recovery (ASD) | ASD | Pack powder tightly, run dispense cycle | Cleared within 2 retries, or clean error reported |
| Drip Prevention (SLD) | SLD | After pump stop, observe nozzle for 60s | No drip (solenoid sealed) |
| Cross-Contamination | All | Dispense colored liquid (SLD), colored powder (ASD), inspect adjacent paths | No visible contamination |
| Food Safety Hold Time | All | Load perishable ingredient, monitor temperature over 2 hours | Temperature remains within safe zone (ambient <25°C) |
| Cleaning Verification | All | ATP swab test after cleaning on all removable parts | ATP reading <100 RLU |
| ASD Servo Endurance | ASD | 10,000 open/close cycles per servo | No binding, position accuracy maintained |
| SLD Pump Endurance | SLD | 10,000 pump cycles (1-minute runs) | Consistent flow rate, no tube degradation |
| CID Actuator Endurance | CID | 5,000 extend/retract cycles | Limit switches reliable, no mechanical play |
| SLD Solenoid Endurance | SLD | 10,000 open/close cycles | No leaking when closed, consistent response |
| Tubing Replacement | SLD | Replace tubing, verify flow rate matches spec | Flow rate within ±10% of calibrated value |

### Prototype Validation Checklist

- [ ] All 3 ASD hoppers seat securely and lift out easily
- [ ] ASD servo flaps close fully (no gap visible)
- [ ] ASD weight-verified dispensing achieves ±10% accuracy
- [ ] ASD clog detection fires within 3s of blocked flow
- [ ] ASD vibration motor successfully loosens settled ground spices
- [ ] Both CID trays slide in/out smoothly
- [ ] CID linear actuators push full tray contents into pot reliably
- [ ] CID limit switches trigger at correct positions
- [ ] SLD peristaltic pumps deliver consistent flow at calibrated speed
- [ ] SLD solenoid valves seal completely when de-energized (no drips)
- [ ] SLD dedicated load cell reads within ±1g of calibration weight
- [ ] SLD closed-loop dispensing achieves ±5% accuracy
- [ ] Pre-flight check correctly identifies empty/insufficient subsystems
- [ ] All chutes/nozzles direct ingredients into pot center (no spillage)
- [ ] Auto-rinse cycle clears visible residue from SLD tubing

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../02-Hardware/01-Epicura-Architecture|Hardware Architecture]]
- [[09-Induction-Heating|Induction Heating System]]
- [[10-Robotic-Arm|Robotic Arm System]]
- [[12-Vision-System|Vision System]]
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]]

#epicura #ingredient-dispensing #subsystem #asd #cid #sld

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-15 | Manas Pradhan | Rewrite: replaced 6-compartment C1-C6 system with 3 subsystems (ASD, CID, SLD) |
