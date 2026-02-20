---
created: 2026-02-15
modified: 2026-02-20
version: 4.0
status: Draft
---

# Total Component Cost Summary

## Overview

This document provides a consolidated view of all component costs for the Epicura kitchen robot prototype, including electronic components, mechanical parts, and projected production costs.

---

## Category Summary

| Category | Subtotal | % of Total | Details |
|----------|----------|------------|---------|
| [[01-Compute-Module-Components|Compute Modules]] | $199.50 | 25% | CM5, STM32, display, cables, ISO1050DUB isolated CAN transceiver |
| [[02-Actuation-Components|Actuation]] | $278.85 | 35% | Induction hob, P-ASD pneumatic system + PCF8574 I2C expander, CID linear actuators, SLD pumps/solenoids/load cell, relays, exhaust fan, filters |
| [[03-Sensor-Components|Sensors]] | $64.90 | 8% | Camera, IR thermo, load cells, NTC |
| **Component Total** | **$543.25** | **69%** | Electronic components only |

---

## Detailed Component Breakdown

### Compute Modules ($199.50)

| Item | Cost |
|------|------|
| Raspberry Pi CM5 (4GB) | $45.00 |
| CM5 IO Board (carrier) | $20.00 |
| STM32G474RE Nucleo | $18.00 |
| 10.1" IPS Display | $80.00 |
| Storage + Cables | $25.00 |
| ISO1050DUB (isolated CAN transceiver) | $3.50 |

### Actuation ($194.85)

| Item | Cost |
|------|------|
| Microwave Induction Surface (CAN) | $60.00 |
| DS3225 Servo (main arm) | $15.00 |
| P-ASD Pneumatic System (pump, valves, accumulator, regulator, sensor, tubing, cartridges, relief valve, PCF8574) | $90.50 |
| Linear Actuators — CID (2x) | $16.00 |
| Peristaltic Pumps — SLD (2x) | $20.00 |
| Solenoid Valves — SLD (2x) | $8.00 |
| Load Cells + HX711 — SLD (2×) | $16.00 |
| H-Bridge Driver — CID | $5.00 |
| Limit Switches — CID (4x) | $2.00 |
| CAN Termination + Decoupling | $0.13 |
| Safety Relay Module (2x) | $6.00 |
| Motor Driver Board | $8.00 |
| Connectors + Wiring | $17.00 |
| Exhaust Fan + Filtration | $22.50 |
| Piezo Buzzer + MOSFET | $0.85 |

### Sensors ($64.90)

| Item | Cost |
|------|------|
| IMX219 Camera | $25.00 |
| MLX90614 IR Thermometer | $12.00 |
| Load Cells (4x CZL635) | $16.00 |
| HX711 ADC | $3.00 |
| NTC Thermistors (2x) | $2.00 |
| Reed Switch + LED Ring | $6.00 |
| Passive Components | $0.90 |

---

## Additional Costs

| Item | Cost | Notes |
|------|------|-------|
| Enclosure (3D printed) | $80.00 | PLA/PETG filament, prototype enclosure + internal brackets |
| Mechanical Parts (shaft, brackets, fasteners) | $50.00 | Stainless steel shaft (8mm), aluminum brackets, M3/M4 fasteners |
| Custom PCB (carrier/interface boards) | $40.00 | 2-4 layer prototype boards, 5 pcs ea (JLCPCB) |
| Power Supply Module | $30.00 | Mean Well LRS-75-24 (24V/3.2A/76.8W) + buck converters (24V→5V) |
| Wiring / Connectors / Misc | $30.00 | JST, Dupont, ring terminals, heat shrink, cable ties |
| Pot (induction-compatible) | $20.00 | Stainless steel 304, 3-4L capacity, flat base |
| **Additional Total** | **$250.00** | |

---

## Prototype Total BOM

| Category | Cost |
|----------|------|
| Electronic Components | $543.25 |
| Mechanical / Other | $250.00 |
| **Total BOM (Prototype)** | **$793.25** |
| **With Contingency (+20%)** | **~$952** |
| **With Tools & Consumables** | **$1,100-1,350** |

---

## Prototype vs Production Cost Comparison

| Item | Prototype | Production (1000 qty) | Notes |
|------|-----------|----------------------|-------|
| CM5 Module (4GB) | $45.00 | $35.00 | Volume pricing from RPi Foundation |
| STM32G474 | $18.00 (Nucleo) | $5.00 (bare chip) | Custom PCB eliminates dev board |
| Display (10.1") | $80.00 | $45.00 | OEM panel with DSI, no HDMI |
| Microwave Induction Surface | $60.00 (CAN module) | $40.00 (bulk pricing) | Self-contained module, no custom driver |
| P-ASD system (pump+valves+cartridges) | $90.00 | $50.00 | Bulk pricing, simplified assembly |
| Linear Actuators — CID (2x) | $16.00 | $8.00 | Bulk pricing |
| Pumps + Solenoids — SLD | $28.00 | $14.00 | Bulk pricing |
| DS3225 Main Arm Servo | $15.00 | $8.00 | Bulk pricing |
| Sensors (all) | $64.90 | $35.00 | Direct from manufacturer, MOQ pricing |
| Enclosure | $80.00 (3D print) | $15.00 (injection mold) | Mold cost amortized over production run |
| PCBs | $40.00 (prototype) | $8.00 (panel production) | Integrated carrier + interface board |
| Power Supply | $30.00 | $12.00 | Integrated SMPS on main PCB |
| Mechanical | $50.00 | $15.00 | Stamped brackets, bulk fasteners |
| Pot + Accessories | $20.00 | $10.00 | OEM sourcing |
| Wiring / Connectors | $30.00 | $10.00 | Custom harness, bulk connectors |
| Exhaust + Filters | $22.50 | $8.00 (OEM blower + bulk filters) | Custom blower + injection-molded housing |
| Other (CAN, relays, drivers, load cell, cables, buzzer) | $94.85 | $20.00 (integrated into PCB + bulk) | Small components absorbed into custom PCB at volume |
| **Total Unit** | **~$793** | **~$337** | **~57% cost reduction** |

---

## Cost Breakdown Chart

```
┌────────────────────────────────────────────────────────────────────────────┐
│                 Epicura Prototype Component Costs                         │
│                                                                          │
│  Compute Modules (24%)  ████████████████████████                         │
│  └─ Display (10%)       ██████████                                       │
│  └─ CM5 (6%)            ██████                                           │
│  └─ STM32 (2%)          ██                                               │
│  └─ Other (6%)          ██████                                           │
│                                                                          │
│  Actuation (36%)        ████████████████████████████████████              │
│  └─ P-ASD system (11%)  ███████████                                      │
│  └─ Induction (8%)      ████████                                         │
│  └─ CID/SLD (7%)        ███████                                          │
│  └─ Other (10%)         ██████████                                       │
│                                                                          │
│  Sensors (8%)           ████████                                         │
│  └─ Camera (3%)         ███                                              │
│  └─ Load Cells (2%)     ██                                               │
│  └─ Other (3%)          ███                                              │
│                                                                          │
│  Additional (32%)       ████████████████████████████████                  │
│  └─ Enclosure (10%)     ██████████                                       │
│  └─ Mechanical (6%)     ██████                                           │
│  └─ PCBs/PSU (9%)       █████████                                        │
│                                                                          │
│  Total Prototype BOM: ~$793                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Budget Planning by Development Phase

| Phase | Description | Estimated Spend | Cumulative |
|-------|-------------|----------------|------------|
| Phase 1 | Hardware Setup (CM5 + STM32 + display + PSU) | $300-400 | $300-400 |
| Phase 2-3 | Induction + Arm (hob + servos + load cells + mechanical) | $200-300 | $500-700 |
| Phase 4 | Vision (camera + LED ring + training data ingredients) | $50-80 | $550-780 |
| Phase 5 | Dispensing (P-ASD pneumatic system, CID actuators, SLD pumps/solenoids/2× load cells) | $168-208 | $718-988 |
| Phase 6 | UI (display already counted; app dev = $0 software) | $0-20 | $600-880 |
| Phase 7 | Integration (consumables, replacements, debugging) | $50-100 | $650-980 |
| Contingency | Unexpected costs, rework, replacement parts | $200-400 | $850-1,380 |
| Tools | Soldering station, multimeter, 3D printer access | $100-200 | $950-1,580 |
| Ingredients | 30+ cook sessions for testing and training data | $50-100 | $1,000-1,680 |
| **Total Project Budget** | | **$1,500-2,500** | |

---

## Cost Drivers Analysis

### Highest Cost Components

| Rank | Component | Cost | % of BOM | Notes |
|------|-----------|------|----------|-------|
| 1 | P-ASD Pneumatic System | $90.00 | 11% | Pump+valves+cartridges; bulk: $50 |
| 2 | 10.1" Display | $80.00 | 10% | Largest single component; OEM reduces to $45 |
| 3 | Enclosure (3D print) | $80.00 | 10% | Prototype only; injection mold: $15/unit |
| 4 | Microwave Induction Surface | $60.00 | 8% | Self-contained CAN module; bulk: $40 |
| 5 | Mechanical Parts | $50.00 | 6% | Shaft, brackets, fasteners |
| 6 | Raspberry Pi CM5 | $45.00 | 6% | Volume pricing: $35 |
| 7 | Custom PCBs | $40.00 | 5% | Panel production: $8/unit |

### Cost Reduction Opportunities

| Opportunity | Potential Savings | Effort | Risk |
|-------------|-------------------|--------|------|
| Volume pricing (1000 qty) | 40-50% overall | Low | Low |
| Custom carrier PCB (integrate CM5+STM32) | $30-40/unit | High | Medium |
| OEM display panel (DSI, no HDMI) | $35/unit | Medium | Low |
| Custom induction driver | $20/unit | High | Medium |
| Injection-molded enclosure | $65/unit | High (tooling) | Low |
| Direct manufacturer sourcing (sensors) | $25-30/unit | Medium | Low |

---

## Target Pricing (Production)

| Volume | Unit BOM Cost | Target Selling Price | Gross Margin |
|--------|--------------|---------------------|-------------|
| 100 units | $400-450 | Not viable (pre-production) | - |
| 1,000 units | $320-370 | $599-799 | 47-54% |
| 10,000 units | $260-300 | $499-699 | 50-57% |

---

## Related Documentation

- [[01-Compute-Module-Components|Compute Module Components]]
- [[02-Actuation-Components|Actuation Components]]
- [[03-Sensor-Components|Sensor Components]]
- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../07-Development/Prototype-Development-Plan|Prototype Development Plan]]

---

#epicura #components #bom #cost-analysis

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-16 | Manas Pradhan | Update costs for P-ASD pneumatic redesign (+$84 to actuation); new prototype BOM ~$784 |
| 3.0 | 2026-02-16 | Manas Pradhan | Added PCF8574 I2C GPIO expander (+$0.50); prototype BOM ~$785 |
| 4.0 | 2026-02-20 | Manas Pradhan | Moved CAN transceiver from Actuation to Compute (ISO1050DUB $3.50 replaces $3.00 non-isolated); updated all totals; prototype BOM ~$793 |
