---
created: 2026-02-15
modified: 2026-02-20
version: 6.0
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
│  │  STM32G474RE │── PWM+EN►│  24V BLDC    │                     │
│  │  (Controller)│         │  Motor       │                     │
│  │              │         └──────────────┘                     │
│  │              │                                               │
│  │              │── PWM  ►┌──────────────┐                     │
│  │              │  +GPIO  │  P-ASD: Pump │                     │
│  │              │         │  + Sol. x6   │                     │
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
| 24V BLDC Motor w/ Integrated ESC | TBD (24V, 30-50 kg-cm) | 1 | $25.00 | $25.00 | AliExpress | Main stirring arm; brushless, continuous rotation, integrated driver |
| 12V Micro Diaphragm Pump — P-ASD | SC3701PM or equiv. | 1 | $15.00 | $15.00 | AliExpress | P-ASD air source, 3-4 L/min, <45 dB |
| 12V NC Solenoid Valve (mini) — P-ASD | Generic 12V, 2-3mm orifice | 6 | $3.50 | $21.00 | AliExpress | P-ASD cartridge air valves, <20 ms response |
| Accumulator (100mL aluminum) — P-ASD | Custom/generic | 1 | $8.00 | $8.00 | AliExpress | P-ASD pressure reservoir, 1.5 bar max |
| Pressure Regulator (inline) — P-ASD | Miniature, 0.3-2.0 bar | 1 | $5.00 | $5.00 | AliExpress | P-ASD operating pressure set to 1.0 bar |
| ADS1015 ADC (pressure sensor) — P-ASD | ADS1015 breakout | 1 | $3.00 | $3.00 | Mouser | I2C pressure reading, addr 0x48 |
| MPXV5100GP Pressure Sensor — P-ASD | MPXV5100GP | 1 | $8.00 | $8.00 | Mouser | Analog pressure sensor for accumulator |
| Pneumatic Tubing + Fittings — P-ASD | 4mm OD silicone + barb fittings | 1 lot | $10.00 | $10.00 | AliExpress | Pump-to-manifold-to-cartridges |
| Spice Cartridges (6x, PP) — P-ASD | Custom 60mL, food-grade PP | 6 | $3.00 | $18.00 | Custom/3D print | Bayonet-lock, 5mm orifice + 200-mesh screen |
| Relief Valve (2.0 bar) — P-ASD | Pop-off safety valve | 1 | $2.00 | $2.00 | AliExpress | Overpressure protection on accumulator |
| 12V DC Linear Actuator (50mm) — CID | Generic 12V, 50mm stroke | 2 | $8.00 | $16.00 | Amazon / AliExpress | CID push-plate slider for coarse ingredients |
| 12V Peristaltic Pump — SLD | Generic 12V DC gear motor | 2 | $10.00 | $20.00 | Amazon / AliExpress | SLD liquid dispensing (oil + water) |
| 12V NC Solenoid Valve — SLD | Generic 12V, normally closed | 2 | $4.00 | $8.00 | Amazon / AliExpress | SLD drip prevention |
| 2 kg Load Cell + HX711 — SLD (oil) | Generic 2 kg strain gauge + HX711 | 1 | $8.00 | $8.00 | Amazon | SLD oil reservoir closed-loop metering + level alert |
| 2 kg Load Cell + HX711 — SLD (water) | Generic 2 kg strain gauge + HX711 | 1 | $8.00 | $8.00 | Amazon | SLD water reservoir closed-loop metering + level alert |
| H-Bridge Motor Driver — CID | DRV8876RGTR (x2) | 2 | $2.50 | $5.00 | Mouser | CID linear actuator EN/PH direction + speed |
| Limit Switches (micro) — CID | Generic micro switch | 4 | $0.50 | $2.00 | Amazon | CID home/extend position detection |
| PCF8574 I2C GPIO Expander — P-ASD | PCF8574 (SOIC-16) | 1 | $0.50 | $0.50 | LCSC / Mouser | P-ASD solenoid V1-V6 gate driver (I2C1, addr 0x20) |
| ISO1050DUB (isolated CAN transceiver) | ISO1050DUBR | 1 | $3.50 | $3.50 | TI / Mouser | 5 kV RMS galvanic isolation, SOIC-8; on Driver PCB, CAN bus to induction module |
| CAN Termination + Decoupling | 120Ω + MLCC caps | 1 lot | $0.13 | $0.13 | LCSC | CAN bus passives on Driver PCB |
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
| 24V BLDC Motor (main arm) | $25.00 |
| P-ASD Pneumatic System (pump, valves, accumulator, regulator, sensor, tubing, cartridges, relief valve) | $90.00 |
| Linear Actuators — CID (2x) | $16.00 |
| Peristaltic Pumps — SLD (2x) | $20.00 |
| Solenoid Valves — SLD (2x) | $8.00 |
| Load Cells + HX711 — SLD (2×) | $16.00 |
| H-Bridge Driver — CID | $5.00 |
| Limit Switches — CID (4x) | $2.00 |
| PCF8574 I2C GPIO Expander (P-ASD) | $0.50 |
| ISO1050DUB (isolated CAN transceiver) | $3.50 |
| CAN Termination + Decoupling | $0.13 |
| Relay Module (safety, 2x) | $6.00 |
| Motor Driver Board | $8.00 |
| Connectors + Wiring | $17.00 |
| Exhaust Fan + Filtration | $22.50 |
| Piezo Buzzer + MOSFET | $0.85 |
| **Category Subtotal** | **$300.48** |

---

## Design Notes

### Microwave Induction Surface Strategy
- **Both Prototype and Production:** Commercial microwave induction surface with CAN bus port
  - Self-contained module: internal coil, driver, safety circuits
  - STM32 controls power level (0-100%) via CAN 2.0B at 500 kbps
  - No custom IGBT driver design needed
  - Safety relay on AC mains provides system-level hard disconnect
  - Module-internal pot detection and thermal cutoff

### 24V BLDC Motor Selection
- **30-50 kg-cm torque** provides ample margin for thick curries and dals
- **Brushless design** eliminates brush wear, better thermal handling for sustained operation
- **True continuous rotation** — no servo modification needed
- **Integrated ESC** — no external H-bridge or buck converter required
- **Direct 24V operation** — powered from main PSU rail; 6.5V buck converter (MP1584EN #2) retained for future use
- Control: 10 kHz PWM (speed) + EN (enable) + DIR (direction) from STM32
- **Specific model TBD** — document generically as "24V BLDC, 30-50 kg-cm, integrated ESC"

### P-ASD Pneumatic System
- **Puff-dosing mechanism**: pressurized air bursts through sealed cartridges
- **6 cartridges** (60 mL each) with quarter-turn bayonet docking
- **12V diaphragm pump** (3-4 L/min) + 100 mL accumulator at ~1.0 bar
- **6× 12V NC solenoid valves** (<20 ms response) for individual cartridge control
- **Weight-verified** via existing pot load cells (±10% accuracy)
- **Anti-clog**: inherent (pressurized air breaks powder bridges), no moving parts in powder path
- **BOM cost**: ~$90 (vs ~$6 for old 3× SG90 servos) — 15× cost for 2× capacity + dramatically improved reliability with sticky Indian spices

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
| 24V BLDC motor | $25 | $15 (bulk) | 40% |
| P-ASD system (pump+valves+cartridges) | $90 | $50 (bulk) | 44% |
| Linear actuators x2 (CID) | $16 | $8 (bulk) | 50% |
| Peristaltic pumps x2 (SLD) | $20 | $10 (bulk) | 50% |
| Solenoid valves x2 (SLD) | $8 | $4 (bulk) | 50% |
| CAN transceiver (ISO1050DUB) | $3.50 (on Driver PCB) | $2.50 (bulk) | 29% |
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
| 2.0 | 2026-02-16 | Manas Pradhan | Replace ASD (3× SG90 servo hoppers) with P-ASD pneumatic puff-dosing system (pump + 6× solenoid valves + sealed cartridges) |
| 3.0 | 2026-02-16 | Manas Pradhan | Added PCF8574 I2C GPIO expander ($0.50) for P-ASD solenoid control |
| 4.0 | 2026-02-20 | Manas Pradhan | Moved CAN transceiver (now ISO1050DUB) to Compute Modules; replaced with CAN termination + decoupling passives ($0.13); subtotal $289.85 → $286.98 |
| 5.0 | 2026-02-20 | Manas Pradhan | Moved ISO1050DUB ($3.50) back from Compute Modules to Actuation (now on Driver PCB); subtotal $286.98 → $290.48 |
| 6.0 | 2026-02-20 | Manas Pradhan | Replaced DS3225 servo ($15) with 24V BLDC motor w/ integrated ESC ($25); net +$10; subtotal $290.48→$300.48 |
