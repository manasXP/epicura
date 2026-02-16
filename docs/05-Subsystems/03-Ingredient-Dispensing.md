---
created: 2026-02-15
modified: 2026-02-15
version: 3.0
status: Draft
---

# Ingredient Dispensing System

## Overview

The ingredient dispensing system is divided into three purpose-built subsystems, each optimized for a different ingredient class. Together they surround the cooking pot and are orchestrated by the STM32 controller under commands from the CM5 recipe engine.

| Subsystem | Full Name | Purpose | Actuators | Metering |
|-----------|-----------|---------|-----------|----------|
| **P-ASD** | Pneumatic Advanced Seasoning Dispenser | Ground/powdered spices (turmeric, chili, cumin, salt, garam masala, coriander) | 6 Solenoid Valves + Micro Diaphragm Pump | Weight-verified via pot load cells |
| **CID** | Coarse Ingredients Dispenser | Pre-cut vegetables, meat, paneer, dal, rice | 2 Linear Actuators (slider mechanism) | Timed/position-based |
| **SLD** | Standard Liquid Dispenser | Oil and water | 2 Peristaltic Pumps + 2 Solenoid Valves + 1 Load Cell (dedicated) | Closed-loop weight feedback |

## Layout

### Top-View Arrangement

```
┌───────────────────────────────────────────────────────┐
│                    REAR OF UNIT                        │
│                                                        │
│       ┌──────────────────────────────────────────┐     │
│       │        P-ASD (Pneumatic Seasonings)       │     │
│       │  ┌────────┐ ┌────────┐ ┌────────┐        │     │
│       │  │P-ASD-1 │ │P-ASD-2 │ │P-ASD-3 │ Row A  │     │
│       │  │Turmeric│ │ Chili  │ │ Cumin  │ (rear) │     │
│       │  │(60 mL) │ │(60 mL) │ │(60 mL) │        │     │
│       │  └───┬────┘ └───┬────┘ └───┬────┘        │     │
│       │  ┌───┴────┐ ┌───┴────┐ ┌───┴────┐        │     │
│       │  │P-ASD-4 │ │P-ASD-5 │ │P-ASD-6 │ Row B  │     │
│       │  │  Salt  │ │ Garam  │ │Coriand.│ (front)│     │
│       │  │(60 mL) │ │ Masala │ │(60 mL) │        │     │
│       │  └───┬────┘ └───┬────┘ └───┬────┘        │     │
│       └──────┼──────────┼──────────┼──────────────┘     │
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

**P-ASD (Pneumatic Puff-Dosing):**

```
              ┌──── Threaded cap + silicone O-ring seal
              │     ┌── Desiccant pocket (1g silica gel)
              ▼     ▼
       ┌───────────────────┐
       │  ╔═══════════════╗│
       │  ║               ║│  45 mm dia × 50 mm tall
       │  ║   SPICE       ║│  60 mL capacity
       │  ║   POWDER      ║│  Food-grade PP, translucent
       │  ║               ║│
       │  ╚═══╤═══════╤═══╝│
       │      │  AIR ► │    │ ◄── Air inlet barb (4mm, side wall)
       │      └───┬───┘    │
       │     ┌────▼────┐   │
       │     │ 5mm     │   │ ◄── Discharge orifice + 200-mesh SS screen
       │     │ orifice │   │
       │     └────┬────┘   │
       └──────────┼────────┘
                  │
           ┌──────▼──────┐
           │  Bayonet    │ ◄── Quarter-turn lock into docking station
           │  collar     │
           └──────┬──────┘
                  │
           ┌──────▼──────┐
           │ Chute /     │ ◄── Shared collection funnel
           │ Funnel      │
           └──────┬──────┘
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

## P-ASD — Pneumatic Advanced Seasoning Dispenser

### Mechanism Overview

The P-ASD uses **puff-dosing** — a micro diaphragm pump pressurizes a small accumulator to ~1.0 bar. Individual solenoid valves open briefly (100–400 ms), delivering calibrated air bursts into sealed cartridges. The pressure forces powder through a 5 mm bottom orifice into a shared funnel chute leading to the pot. This eliminates all moving parts from the powder path, dramatically improving reliability with sticky Indian spices like turmeric and chili.

### Cartridge Specifications

| Parameter | Value |
|-----------|-------|
| Cartridges | 6 (P-ASD-1 through P-ASD-6) |
| Capacity | 60 mL each |
| Dimensions | 45 mm diameter × 50 mm tall (cylindrical) |
| Material | Food-grade polypropylene (PP), translucent |
| Removable | Yes (quarter-turn bayonet lock for quick swap) |
| Lid | Threaded screw-cap with silicone O-ring seal, desiccant pocket |
| Orifice | 5 mm diameter bottom opening with 200-mesh SS anti-clog screen |
| Air Inlet | 4 mm barb on side wall (above powder line), self-sealing push-fit |
| Weight (empty) | ~25 g |

### Default Cartridge Assignment

| Cartridge | Position | Default Spice |
|-----------|----------|---------------|
| P-ASD-1 | Row A, Left | Turmeric powder |
| P-ASD-2 | Row A, Center | Chili powder |
| P-ASD-3 | Row A, Right | Cumin powder |
| P-ASD-4 | Row B, Left | Salt (fine) |
| P-ASD-5 | Row B, Center | Garam masala |
| P-ASD-6 | Row B, Right | Coriander powder |

### Pneumatic System

#### Air Source

| Parameter | Value |
|-----------|-------|
| Type | 12V micro diaphragm pump (e.g., SC3701PM or equivalent) |
| Max Pressure | 2.0 bar (200 kPa) |
| Free Flow | 3–4 L/min |
| Voltage | 12V DC |
| Current | 0.5–0.8 A |
| Noise | <45 dB |
| Size | 65 × 40 × 40 mm |

#### Accumulator & Regulation

| Component | Specification |
|-----------|---------------|
| Accumulator | 100 mL sealed aluminum cylinder, 1.5 bar max |
| Pressure Regulator | Miniature inline, adjustable 0.3–2.0 bar |
| Pressure Sensor | ADS1015 (I2C) + MPXV5100GP analog, on I2C1 bus (address 0x48) |
| Relief Valve | 2.0 bar pop-off safety valve on accumulator |
| Operating Pressure | 0.8–1.2 bar nominal |

#### Solenoid Valves (×6)

| Parameter | Value |
|-----------|-------|
| Type | 2-way normally-closed, direct-acting, 12V DC |
| Response Time | <20 ms open, <30 ms close |
| Orifice | 2–3 mm (sufficient for air burst) |
| Power | ~4W when energized (one at a time) |
| Driver | IRLML6344 N-MOSFET (SOT-23) with flyback diode on Driver PCB |
| Cost | ~$3.50 each |

#### Pneumatic Circuit

```
12V ───► Micro Diaphragm Pump (3-4 L/min, <45 dB)
              │
              ▼
         Accumulator (100 mL, 1.5 bar max)
              │
              ▼
         Pressure Regulator (set 1.0 bar) + Relief Valve (2.0 bar)
              │
              ▼
         Pressure Sensor ──► STM32 via I2C1 (ADS1015 @ 0x48)
              │
              ▼
         ┌─── 6-Way Manifold (3D-printed nylon PA12) ───┐
         │                                               │
    ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
    │V1│ │V2│ │V3│ │V4│ │V5│ │V6│   6× 12V NC solenoid valves
    └┬─┘ └┬─┘ └┬─┘ └┬─┘ └┬─┘ └┬─┘
     ▼    ▼    ▼    ▼    ▼    ▼
   C-1  C-2  C-3  C-4  C-5  C-6     Cartridges
```

### Anti-Clog Design

Pneumatic dispensing inherently prevents clogging — the primary failure mode of gravity-fed systems:

| Advantage | Mechanism |
|-----------|-----------|
| Bridge breaking | Pressurized air shatters powder arches over the orifice |
| Humidity tolerance | Forced airflow pushes damp/sticky powder through |
| No residue buildup | No gate in powder path; orifice air-cleared after every dispense |
| Self-clearing nozzle | Post-dispense purge (200 ms at 1.2 bar) cleans orifice |
| 200-mesh SS screen | Prevents large clumps from blocking the 5 mm orifice |
| 60° cone angle | Internal cartridge geometry prevents dead zones |

**Clog Recovery (if no weight change after 3 pulses):** Rapid 50 ms on/off oscillating air pulses to vibrate powder loose — pneumatic equivalent of vibration motors, but with no additional hardware.

### Metering Strategy

P-ASD uses **calibrated puff-dosing with weight feedback** (dual-loop):

**Primary control:** Timed air pulses calibrated per spice type:

| Spice | Bulk Density (g/mL) | Pulse Duration for ~1g (ms) | Pressure (bar) |
|-------|--------------------|-----------------------------|-----------------|
| Turmeric powder | 0.55 | 200–300 | 1.0 |
| Chili powder | 0.45 | 250–350 | 1.0 |
| Cumin powder | 0.40 | 300–400 | 1.0 |
| Salt (fine) | 1.20 | 100–150 | 0.8 |
| Garam masala | 0.50 | 200–300 | 1.0 |
| Coriander powder | 0.35 | 300–400 | 1.0 |

**Secondary control (closed-loop):** Pot load cells provide weight feedback at 10 Hz:

1. Tare pot weight → W_initial
2. Pre-purge: 100 ms pulse at 0.3 bar (loosen packed powder)
3. Main dispense: open solenoid for calibrated duration
4. Monitor pot weight at 10 Hz: W_delta = W_current − W_initial
5. If W_delta < target × 0.85 → additional 50 ms pulses until target reached
6. Close solenoid when W_delta ≥ target × 0.90 (in-flight compensation)
7. Post-dispense purge: 200 ms at 1.2 bar (clear orifice)
8. Log actual dispensed weight

Accuracy: ±10% of target weight (with weight feedback).

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
| **P-ASD** | Diaphragm Pump Motor | PA0 (TIM2_CH1) | PWM | 12V pump speed control via MOSFET |
| **P-ASD** | Solenoid Valve V1 | PA1 (GPIO) | Digital output via MOSFET | 12V NC solenoid, cartridge 1 |
| **P-ASD** | Solenoid Valve V2 | PA2 (GPIO) | Digital output via MOSFET | 12V NC solenoid, cartridge 2 |
| **P-ASD** | Solenoid Valve V3 | PC7 (GPIO) | Digital output via MOSFET | 12V NC solenoid, cartridge 3 |
| **P-ASD** | Solenoid Valve V4 | PD2 (GPIO) | Digital output via MOSFET | 12V NC solenoid, cartridge 4 |
| **P-ASD** | Solenoid Valve V5 | PA3 (GPIO) | Digital output via MOSFET | 12V NC solenoid, cartridge 5 |
| **P-ASD** | Solenoid Valve V6 | PB11 (GPIO) | Digital output via MOSFET | 12V NC solenoid, cartridge 6 |
| **P-ASD** | Pressure Sensor | I2C1 (PB6/PB7) | I2C via ADS1015 | Accumulator pressure, addr 0x48 |
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

> **Note:** Pot load cells remain on PC0/PC1 (existing allocation). Pin assignments match [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]] document. P-ASD solenoid valves are driven by IRLML6344 MOSFETs on the Driver PCB. Pressure sensor shares I2C1 bus with MLX90614 (0x5A) and INA219 (0x40) — ADS1015 at address 0x48.

### Dispensing Command Protocol (CM5 → STM32)

| Command | Code | Parameters | Response | Description |
|---------|------|------------|----------|-------------|
| DISPENSE_PASD | 0x30 | cartridge_id (1 byte: 1–6), target_weight_g (2 bytes) | ACK + actual_weight_g | Dispense seasoning via pneumatic puff-dose, weight-verified by pot load cells |
| DISPENSE_CID | 0x31 | cid_id (1 byte: 1–2), mode (1 byte: FULL/PARTIAL), position_mm (1 byte) | ACK + status | Push tray contents into pot via linear actuator |
| DISPENSE_SLD | 0x32 | channel (1 byte: OIL=1, WATER=2), target_weight_g (2 bytes) | ACK + actual_weight_g | Pump liquid, closed-loop via dedicated load cell |
| PURGE_PASD | 0x38 | cartridge_id (1 byte: 1–6, or 0xFF=all) | ACK | Post-dispense air purge to clear orifice |
| PRESSURE_STATUS | 0x39 | — | pressure_bar (2 bytes, fixed-point) | Read accumulator pressure |
| QUERY_WEIGHT | 0x35 | source (1 byte: POT=0, SLD=1) | weight_g (4 bytes) | Read weight from pot or SLD load cells |
| PREFLIGHT | 0x36 | subsystem_mask (1 byte) | status per subsystem | Check if required subsystems are loaded/ready |
| TARE | 0x37 | source (1 byte: POT=0, SLD=1) | ACK | Zero the specified load cell readings |

## Clog Prevention (P-ASD)

### Clog Detection and Recovery Flow

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Pre-purge    │────►│ Main dispense │────►│ Pot Weight   │
│ (100ms,0.3bar│     │ pulse         │     │ Changed?     │
└──────────────┘     └───────────────┘     └──────┬───────┘
                                                   │
                                          Yes ◄────┴────► No
                                           │              │
                                           ▼              ▼
                                    ┌──────────┐   ┌──────────────┐
                                    │ Continue │   │ Retry #1:    │
                                    │ Normally │   │ Increase     │
                                    └──────────┘   │ pressure to  │
                                                   │ 1.2 bar,     │
                                                   │ repeat pulse │
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
                                           ┌──────────┐   ┌──────────────┐
                                           │ Continue │   │ Retry #2:    │
                                           │ Normally │   │ Rapid 50ms   │
                                           └──────────┘   │ on/off pulses│
                                                          │ (5 cycles)   │
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

| Factor | P-ASD Impact | CID Impact | SLD Impact | Mitigation |
|--------|-------------|-----------|-----------|------------|
| In-flight material | Powder still in chute after solenoid closes | N/A (push mechanism) | Fluid in tube after pump stops | P-ASD: close at 90% target. SLD: close at 95% target |
| Load cell noise | ±3 g at 10 Hz (pot cells) | N/A | ±1 g (dedicated cell) | Moving average filter (3 samples) |
| Vibration | Arm motor affects pot weight | N/A | Dedicated cell isolated from pot | Pause arm during P-ASD dispensing |
| Sticky ingredients | Pressurized air forces through orifice | Pieces stick to tray | Oil residue in tube | P-ASD: post-dispense purge. CID: angled tray. SLD: tube replacement |
| Fill level variance | Air pressure compensates (consistent regardless of fill) | N/A | Pump rate independent of level | P-ASD: pressure regulation maintains consistent force |

## Recipe Integration

### Dispensing Sequence Example (Dal Tadka)

```
Step 1:  DISPENSE_SLD(OIL, 30g)                ──► Oil into hot pot
Step 2:  Wait for sear temp (200°C)             ──► IR sensor confirms
Step 3:  DISPENSE_PASD(P-ASD-1, 3g)             ──► Turmeric powder
Step 4:  DISPENSE_PASD(P-ASD-2, 5g)             ──► Chili powder
Step 5:  Stir briefly                           ──► Arm mixes spices into oil
Step 6:  DISPENSE_CID(CID-1, FULL)             ──► Chopped onions, tomatoes
Step 7:  Wait for browning (CV detection)       ──► Camera detects golden color
Step 8:  DISPENSE_PASD(P-ASD-4, 5g)             ──► Salt
Step 8b: DISPENSE_PASD(P-ASD-5, 3g)             ──► Garam masala
Step 9:  DISPENSE_CID(CID-2, FULL)             ──► Toor dal (200g, pre-measured)
Step 10: DISPENSE_SLD(WATER, 400g)              ──► Water
Step 11: Simmer until done (CV + timer)         ──► Camera detects thickening
```

### Ingredient Loading Configuration

Users configure subsystem contents when loading ingredients before cooking:

| Field | Example Value | Source |
|-------|---------------|--------|
| Subsystem | P-ASD-2 | Fixed by hardware position |
| Ingredient Name | "Chili Powder" | From recipe ingredient list |
| Target Weight (g) | 5 | From recipe (adjusted for servings) |
| Pre-loaded | Yes/No | User confirms via touchscreen or app |

### Pre-Flight Check

Before starting a recipe, the system verifies all required subsystems:

1. **P-ASD:** Short air pulse into each cartridge, monitor pot weight change — confirms powder present and orifice clear
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

- P-ASD: each cartridge has a dedicated discharge path; shared funnel is air-purged between dispenses
- CID: each tray drops into a distinct zone of the pot (no shared surfaces)
- SLD: fluid only contacts silicone tubing (per-channel, no shared path)
- All removable parts are smooth, non-porous food-grade PP
- Silicone pump tubing is replaceable (recommended every 3 months or 200 cycles)

## Cleaning Design

### Removable Components

| Component | Removal Method | Dishwasher Safe | Cleaning Frequency |
|-----------|----------------|-----------------|-------------------|
| P-ASD Cartridges (×6) | Quarter-turn bayonet, lift out | Yes | After every use |
| P-ASD Cartridge Caps (×6) | Unscrew threaded cap | Yes | After every use |
| P-ASD Orifice Screens (×6) | Press-fit removal from cartridge base | Yes | Weekly deep clean |
| P-ASD Docking Funnels (×6) | Pull out from below | Yes | After every use |
| CID Trays (×2) | Slide out from front | Yes | After every use |
| SLD Reservoirs (×2) | Lift out | Yes | After every use |
| SLD Silicone Tubing (×2) | Disconnect at quick-fit couplings | Hand wash (boil sterilize) | Weekly; replace every 3 months |
| SLD Nozzles (×2) | Unscrew | Yes | After every use |
| P-ASD Pneumatic Tubing | Not user-removable | No | Air purge self-cleans; inspect monthly |
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
| Seasoning Accuracy | P-ASD | 10 trials per cartridge, weigh dispensed amount vs. target | Within ±10% of target weight |
| Liquid Accuracy | SLD | 10 trials per channel, compare load cell reading to scale | Within ±5% of target weight |
| Coarse Dispense | CID | 10 trials, verify full tray contents dumped into pot | All contents reach pot, no spillage |
| Clog Recovery (P-ASD) | P-ASD | Pack powder tightly, run dispense cycle | Cleared within 2 retries, or clean error reported |
| Drip Prevention (SLD) | SLD | After pump stop, observe nozzle for 60s | No drip (solenoid sealed) |
| Cross-Contamination | All | Dispense colored liquid (SLD), colored powder (ASD), inspect adjacent paths | No visible contamination |
| Food Safety Hold Time | All | Load perishable ingredient, monitor temperature over 2 hours | Temperature remains within safe zone (ambient <25°C) |
| Cleaning Verification | All | ATP swab test after cleaning on all removable parts | ATP reading <100 RLU |
| P-ASD Solenoid Endurance | P-ASD | 10,000 open/close cycles per valve | Consistent response time, no leaking |
| P-ASD Pump Endurance | P-ASD | 10,000 pump cycles | Consistent pressure, no membrane degradation |
| SLD Pump Endurance | SLD | 10,000 pump cycles (1-minute runs) | Consistent flow rate, no tube degradation |
| CID Actuator Endurance | CID | 5,000 extend/retract cycles | Limit switches reliable, no mechanical play |
| SLD Solenoid Endurance | SLD | 10,000 open/close cycles | No leaking when closed, consistent response |
| Tubing Replacement | SLD | Replace tubing, verify flow rate matches spec | Flow rate within ±10% of calibrated value |

### Prototype Validation Checklist

- [ ] All 6 P-ASD cartridges dock securely via bayonet lock and release easily
- [ ] P-ASD air seals are airtight (no pressure loss when cartridge docked)
- [ ] P-ASD weight-verified dispensing achieves ±10% accuracy for all 6 spices
- [ ] P-ASD clog detection fires within 3 pulse cycles of blocked flow
- [ ] P-ASD post-dispense purge clears orifice (no residual powder visible)
- [ ] P-ASD pump recharges accumulator to 1.0 bar within 5 seconds
- [ ] P-ASD pressure sensor reads within ±0.05 bar of reference gauge
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

#epicura #ingredient-dispensing #subsystem #p-asd #pneumatic #cid #sld

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-15 | Manas Pradhan | Rewrite: replaced 6-compartment C1-C6 system with 3 subsystems (ASD, CID, SLD) |
| 3.0 | 2026-02-16 | Manas Pradhan | Replaced ASD (servo-gated gravity-fed, 3 hoppers) with P-ASD (pneumatic puff-dosing, 6 cartridges) |
