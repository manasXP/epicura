---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Actuation Components

## Overview

This document details the actuation subsystem components for the Epicura kitchen robot prototype, including the induction heating element, servo stirring arm, and ingredient dispensing mechanisms.

## Actuation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Actuation Subsystem                          │
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │  STM32G474RE │─── PWM ►│  DS3225      │                     │
│  │  (Controller)│         │  Servo Arm   │                     │
│  │              │         └──────────────┘                     │
│  │              │                                               │
│  │              │─── PWM ►┌──────────────┐                     │
│  │              │         │  ASD: SG90 x3│                     │
│  │              │         │  (Seasonings)│                     │
│  │              │         └──────────────┘                     │
│  │              │                                               │
│  │              │── GPIO ►┌──────────────┐                     │
│  │              │  + PWM  │  CID: LinAct │                     │
│  │              │         │  x2 (Coarse) │                     │
│  │              │         └──────────────┘                     │
│  │              │                                               │
│  │              │── PWM  ►┌──────────────┐                     │
│  │              │  +GPIO  │  SLD: Pump x2│                     │
│  │              │         │  + Solenoid x2│                    │
│  │              │         └──────────────┘                     │
│  │              │                                               │
│  │              │── GPIO ►┌──────────────┐    ┌────────────┐   │
│  │              │         │  Relay x2    │───►│ Induction  │   │
│  │              │         │  (10A)       │    │ Hob 1800W  │   │
│  └──────────────┘         └──────────────┘    └────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component List

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| Microwave Induction Surface (1800W, CAN) | Commercial module | 1 | $60.00 | $60.00 | Supplier TBD | Self-contained module with CAN bus port; no teardown needed |
| DS3225 Servo Motor (25 kg.cm) | DS3225 | 1 | $15.00 | $15.00 | Amazon / AliExpress | Main stirring arm; metal gear, waterproof rated |
| SG90 Micro Servo (9g) — ASD | SG90 | 3 | $2.00 | $6.00 | Amazon / AliExpress | ASD seasoning gate actuators |
| 12V DC Linear Actuator (50mm) — CID | Generic 12V, 50mm stroke | 2 | $8.00 | $16.00 | Amazon / AliExpress | CID push-plate slider for coarse ingredients |
| 12V Peristaltic Pump — SLD | Generic 12V DC gear motor | 2 | $10.00 | $20.00 | Amazon / AliExpress | SLD liquid dispensing (oil + water) |
| 12V NC Solenoid Valve — SLD | Generic 12V, normally closed | 2 | $4.00 | $8.00 | Amazon / AliExpress | SLD drip prevention |
| 1 kg Load Cell + HX711 — SLD | Generic strain gauge + HX711 | 1 | $8.00 | $8.00 | Amazon | SLD dedicated closed-loop metering |
| H-Bridge Motor Driver — CID | DRV8876RGTR (x2) | 2 | $2.50 | $5.00 | Mouser | CID linear actuator EN/PH direction + speed |
| Limit Switches (micro) — CID | Generic micro switch | 4 | $0.50 | $2.00 | Amazon | CID home/extend position detection |
| CAN Transceiver (for FDCAN1) | SN65HVD230 or MCP2551 | 1 | $3.00 | $3.00 | Mouser / DigiKey | CAN bus interface to microwave surface module |
| Relay Module (5V, 10A) | SRD-05VDC-SL-C | 2 | $3.00 | $6.00 | Amazon | Induction on/off and power cycling control (prototype) |
| Motor Driver Board | L298N or custom | 1 | $8.00 | $8.00 | Amazon | Servo power distribution and level shifting |
| Power Connectors (XT60) | XT60 male+female | 4 | $1.00 | $4.00 | Amazon | High-current connections for induction and servo power |
| Wiring Harness (18AWG silicone) | 18AWG, 5m assorted | 1 lot | $10.00 | $10.00 | Amazon | Internal wiring; silicone insulation for heat resistance |
| Servo Extension Cables (300mm) | 300mm JR/Futaba | 3 | $1.00 | $3.00 | Amazon | ASD servo wiring to STM32 PWM headers |
| Exhaust Fan (60mm, PWM) | Noctua NF-A6x25 or generic | 1 | $8.00 | $8.00 | Amazon | 4-pin PWM, 12V, fume extraction |
| Grease Mesh + Carbon Filter | 304 SS mesh + coconut carbon | 1 set | $8.00 | $8.00 | Amazon / AliExpress | Dual-stage filtration cartridge |
| Filter Housing + Duct | 3D printed ABS + sheet metal | 1 | $6.00 | $6.00 | Self-fabricated | Slide-out cartridge + 60mm duct |
| Fan MOSFET (PWM driver) | IRLZ44N | 1 | $0.50 | $0.50 | LCSC | Logic-level gate for STM32 PWM |
| Piezo Buzzer (5V, PWM) | MLT-5030 or generic | 1 | $0.80 | $0.80 | Amazon / Mouser | Audio feedback for alerts, errors, task completion |
| Buzzer MOSFET | 2N7002 (SOT-23) | 1 | $0.05 | $0.05 | LCSC | Logic-level gate for buzzer PWM |

---

## Cost Summary

| Item | Cost |
|------|------|
| Microwave Induction Surface (CAN) | $60.00 |
| DS3225 Servo (main arm) | $15.00 |
| SG90 Micro Servos — ASD (3x) | $6.00 |
| Linear Actuators — CID (2x) | $16.00 |
| Peristaltic Pumps — SLD (2x) | $20.00 |
| Solenoid Valves — SLD (2x) | $8.00 |
| Load Cell + HX711 — SLD | $8.00 |
| H-Bridge Driver — CID | $5.00 |
| Limit Switches — CID (4x) | $2.00 |
| CAN Transceiver | $3.00 |
| Relay Module (safety, 2x) | $6.00 |
| Motor Driver Board | $8.00 |
| Connectors + Wiring | $17.00 |
| Exhaust Fan + Filtration | $22.50 |
| Piezo Buzzer + MOSFET | $0.85 |
| **Category Subtotal** | **$197.35** |

---

## Design Notes

### Microwave Induction Surface Strategy
- **Both Prototype and Production:** Commercial microwave induction surface with CAN bus port
  - Self-contained module: internal coil, driver, safety circuits
  - STM32 controls power level (0-100%) via CAN 2.0B at 500 kbps
  - No custom IGBT driver design needed
  - Safety relay on AC mains provides system-level hard disconnect
  - Module-internal pot detection and thermal cutoff

### DS3225 Servo Selection
- **25 kg.cm torque** at 6V provides sufficient force for thick curries and dals
- **Metal gears** for durability (plastic gears strip under load)
- **IP66 waterproof** rated (important for kitchen environment)
- PWM control: 500-2500 us pulse, 50 Hz frequency
- Continuous rotation not needed; 270° range sufficient for stirring patterns

### ASD Gate Servos (SG90 ×3)
- 9g weight, minimal space requirement per seasoning hopper gate
- 1.2 kg.cm torque sufficient for gate open/close
- 3 units for 3 seasoning hoppers (ASD-1, ASD-2, ASD-3)
- Consider upgrading to MG90S (metal gear) if reliability issues arise

### CID Linear Actuators (×2)
- 12V DC, 50 mm stroke push-plate sliders for coarse ingredients
- 20–50 N force sufficient for pushing up to 500g of chopped vegetables
- H-bridge driver (DRV8876RGTR) for EN/PH direction and speed control
- Limit switches at home/extend positions for position feedback

### SLD Peristaltic Pumps (×2) + Solenoid Valves (×2)
- Peristaltic: fluid only touches food-grade silicone tubing (no contamination)
- Flow rate 5–50 mL/min, adjustable via PWM motor speed
- Solenoid valves (12V NC) prevent dripping when pumps are off
- Dedicated 1 kg load cell + HX711 for closed-loop liquid metering (±5%)

### Production Cost Reduction

| Item | Prototype | Production (1000 qty) | Savings |
|------|-----------|----------------------|---------|
| Microwave surface | $60 | $40 (bulk) | 33% |
| DS3225 | $15 | $8 (bulk) | 47% |
| SG90 x3 (ASD) | $6 | $3 (bulk) | 50% |
| Linear actuators x2 (CID) | $16 | $8 (bulk) | 50% |
| Peristaltic pumps x2 (SLD) | $20 | $10 (bulk) | 50% |
| Solenoid valves x2 (SLD) | $8 | $4 (bulk) | 50% |
| CAN transceiver | $3 | $1 (bulk) | 67% |
| Wiring | $20 | $8 (harness) | 60% |

---

## Related Documentation

- [[01-Compute-Module-Components|Compute Module Components]]
- [[03-Sensor-Components|Sensor Components]]
- [[04-Total-Component-Cost|Total Component Cost]]
- [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]

---

#epicura #components #actuation #bom

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
