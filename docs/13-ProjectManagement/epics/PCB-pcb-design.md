---
tags: [epicura, project-management, epic, pcb, hardware]
created: 2026-02-16
aliases: [PCB Epic, PCB Design Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 6 stories across pre-sprint phase |
> | 2026-02-17 | Manas Pradhan | Split >5pt stories for sprint-sized delivery |

# Epic: PCB — PCB Design & Fabrication

Design and fabricate the two custom PCBs: the STM32G474RE Controller Board (160×90mm) and the Power/Actuator Driver Board (160×90mm). The CM5 IO Board is off-the-shelf (Raspberry Pi official) and requires no custom design. This epic has no upstream dependencies and must complete before Sprint 2 to unblock embedded firmware development.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| CTL — Controller Board | 3 | 13 | Pre-Sprint W1–W3 |
| DRV — Driver Board | 3 | 13 | Pre-Sprint W1–W3 |
| FAB — Fabrication & Assembly | 2 | 8 | Pre-Sprint W4–W6 |
| **Total** | **8** | **~34** | |

---

## Pre-Sprint — Controller Board Design (Weeks -6 to -4)

### PCB-CTL.01: Controller PCB schematic — STM32G474RE core, power regulation, debug headers
- **Sprint:** Pre-Sprint (Weeks -6 to -5)
- **Priority:** P0
- **Points:** 5
- **Blocked by:** None
- **Blocks:** [[PCB-pcb-design#PCB-CTL.01b|PCB-CTL.01b]]

**Acceptance Criteria:**
- [ ] STM32G474RE pinout allocated for SPI (CM5), UART (debug), I2C (MLX90614, ADS1015), FDCAN1 (induction), PWM (servo, pumps, fans)
- [ ] Power section: 24V input, 5V buck (AP63205, 2A) for CM5IO, 3.3V LDO (AMS1117) for STM32
- [ ] SWD debug header (TC2030-IDC) and UART debug header present
- [ ] Decoupling capacitors per STM32 datasheet recommendations

**Tasks:**
- [ ] `PCB-CTL.01a` — Create KiCAD project; import STM32G474RE, AP63205, AMS1117 symbols and footprints
- [ ] `PCB-CTL.01b` — Design power section: 24V→5V buck (AP63205) + 5V→3.3V LDO (AMS1117)
- [ ] `PCB-CTL.01c` — Wire STM32 peripherals: SPI1 (CM5), USART1 (debug), I2C1 (sensors), FDCAN1 (induction)
- [ ] `PCB-CTL.01d` — Wire PWM outputs: TIM1 (servo), TIM2 (pump), TIM3 (fan), TIM4 (spare)

---

### PCB-CTL.01b: Controller PCB schematic — ADC, GPIO, connector interface, ERC validation
- **Sprint:** Pre-Sprint (Weeks -6 to -5)
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[PCB-pcb-design#PCB-CTL.01|PCB-CTL.01]]
- **Blocks:** [[PCB-pcb-design#PCB-CTL.02|PCB-CTL.02]], [[PCB-pcb-design#PCB-FAB.01|PCB-FAB.01]]

**Acceptance Criteria:**
- [ ] ADC channels allocated for NTC thermistors and current sensing
- [ ] GPIO allocated for 6× P-ASD solenoid valves + 2× SLD solenoid valves, e-stop input, safety relay output
- [ ] CM5IO SPI interface connector (2×10 pin header) with level shifting if needed
- [ ] ERC passes with zero errors in KiCAD

**Tasks:**
- [ ] `PCB-CTL.01e` — Add ADC channels for NTC thermistors, current sensing
- [ ] `PCB-CTL.01f` — Add GPIO for solenoid valve control (6× P-ASD + 2× SLD), e-stop input, safety relay output
- [ ] `PCB-CTL.01g` — Add CM5IO SPI connector with level shifting; run ERC; fix all errors; generate netlist

---

### PCB-CTL.02: Controller PCB layout — 4-layer, 160×90mm, mounting holes
- **Sprint:** Pre-Sprint (Weeks -5 to -4)
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[PCB-pcb-design#PCB-CTL.01b|PCB-CTL.01b]]
- **Blocks:** [[PCB-pcb-design#PCB-FAB.01|PCB-FAB.01]]

**Acceptance Criteria:**
- [ ] 4-layer stackup: Signal / GND / Power / Signal
- [ ] Board dimensions 160×90mm with 4× M3 mounting holes
- [ ] Power section isolated from signal section; adequate copper pour for 24V trace
- [ ] SWD and UART headers accessible from board edge
- [ ] CM5IO connector placed for ribbon cable routing
- [ ] DRC passes with JLCPCB 4-layer design rules (min 0.15mm trace, 0.2mm clearance)
- [ ] Gerber files exported and validated in JLCPCB viewer

**Tasks:**
- [ ] `PCB-CTL.02a` — Define board outline and mounting hole placement; set up JLCPCB design rules
- [ ] `PCB-CTL.02b` — Place components: STM32 center, power section upper-left, connectors at edges
- [ ] `PCB-CTL.02c` — Route power traces (24V, 5V, 3.3V) with appropriate widths
- [ ] `PCB-CTL.02d` — Route signal traces: SPI, UART, I2C, CAN, PWM, ADC, GPIO
- [ ] `PCB-CTL.02e` — Add ground and power planes; verify copper pours
- [ ] `PCB-CTL.02f` — Run DRC; export Gerbers, BOM, and pick-and-place files

---

## Pre-Sprint — Driver Board Design (Weeks -6 to -4)

### PCB-DRV.01: Driver PCB schematic — motor drivers, power regulation
- **Sprint:** Pre-Sprint (Weeks -6 to -5)
- **Priority:** P0
- **Points:** 5
- **Blocked by:** None
- **Blocks:** [[PCB-pcb-design#PCB-DRV.01b|PCB-DRV.01b]]

**Acceptance Criteria:**
- [ ] DRV8876 H-bridge driver for 2× CID linear actuators (12V, 3.5A per channel)
- [ ] TB6612FNG dual H-bridge for 2× peristaltic pumps (12V, 1.2A per channel)
- [ ] 12V input from 24V→12V buck converter (LM2596 or equivalent)

**Tasks:**
- [ ] `PCB-DRV.01a` — Create KiCAD project; import DRV8876, TB6612FNG, IRLZ44N symbols/footprints
- [ ] `PCB-DRV.01b` — Design 24V→12V buck converter section (LM2596, 3A)
- [ ] `PCB-DRV.01c` — Design DRV8876 circuit for CID linear actuators with current limiting
- [ ] `PCB-DRV.01d` — Design TB6612FNG circuit for SLD peristaltic pumps with PWM speed control

---

### PCB-DRV.01b: Driver PCB schematic — MOSFET drivers, protection, connector interface
- **Sprint:** Pre-Sprint (Weeks -6 to -5)
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[PCB-pcb-design#PCB-DRV.01|PCB-DRV.01]]
- **Blocks:** [[PCB-pcb-design#PCB-DRV.02|PCB-DRV.02]], [[PCB-pcb-design#PCB-FAB.01|PCB-FAB.01]]

**Acceptance Criteria:**
- [ ] IRLZ44N MOSFET circuits for 6× P-ASD solenoid valves + 1× diaphragm pump + 2× SLD solenoid valves
- [ ] Flyback diodes on all inductive loads
- [ ] Board-to-board connector to Controller PCB (signal interface)
- [ ] ERC passes with zero errors

**Tasks:**
- [ ] `PCB-DRV.01e` — Design MOSFET driver circuits for solenoid valves and diaphragm pump
- [ ] `PCB-DRV.01f` — Add flyback diodes (1N4007) on all inductive loads; add bulk capacitors
- [ ] `PCB-DRV.01g` — Design board-to-board connector interface (PWM, GPIO, enable signals from controller)
- [ ] `PCB-DRV.01h` — Run ERC; fix all errors; generate netlist

---

### PCB-DRV.02: Driver PCB layout — 4-layer, 160×90mm, thermal management
- **Sprint:** Pre-Sprint (Weeks -5 to -4)
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[PCB-pcb-design#PCB-DRV.01b|PCB-DRV.01b]]
- **Blocks:** [[PCB-pcb-design#PCB-FAB.01|PCB-FAB.01]]

**Acceptance Criteria:**
- [ ] 4-layer stackup: Signal / GND / Power / Signal
- [ ] Board dimensions 160×90mm with 4× M3 mounting holes (matching controller board)
- [ ] High-current traces (12V, motor drivers) sized for max current (≥1mm width for 3A)
- [ ] Thermal pads and vias under DRV8876 and LM2596 for heat dissipation
- [ ] Motor/solenoid connectors at board edges for wire routing
- [ ] DRC passes with JLCPCB 4-layer design rules

**Tasks:**
- [ ] `PCB-DRV.02a` — Define board outline; set up design rules matching controller board
- [ ] `PCB-DRV.02b` — Place components: buck converter upper-left, motor drivers center, MOSFETs right side
- [ ] `PCB-DRV.02c` — Route high-current power traces with adequate width; add thermal relief on pads
- [ ] `PCB-DRV.02d` — Route signal traces from board-to-board connector to driver ICs
- [ ] `PCB-DRV.02e` — Add ground planes; verify thermal via arrays under power components
- [ ] `PCB-DRV.02f` — Run DRC; export Gerbers, BOM, and pick-and-place files

---

## Pre-Sprint — Fabrication & Assembly (Weeks -4 to -1)

### PCB-FAB.01: PCB fabrication — JLCPCB order, SMT assembly
- **Sprint:** Pre-Sprint (Weeks -4 to -2)
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[PCB-pcb-design#PCB-CTL.02|PCB-CTL.02]], [[PCB-pcb-design#PCB-DRV.02|PCB-DRV.02]]
- **Blocks:** [[PCB-pcb-design#PCB-FAB.02|PCB-FAB.02]]

**Acceptance Criteria:**
- [ ] JLCPCB order placed for both boards (5 units each, 4-layer, HASL lead-free)
- [ ] SMT assembly ordered for passives and ICs (JLCPCB PCBA service)
- [ ] Through-hole components identified for hand soldering (connectors, headers)
- [ ] Order tracking confirms 10-14 day delivery estimate
- [ ] Boards received and visually inspected for defects

**Tasks:**
- [ ] `PCB-FAB.01a` — Upload Gerbers, BOM, and CPL files to JLCPCB for both boards
- [ ] `PCB-FAB.01b` — Verify component availability in JLCPCB parts library; substitute unavailable parts
- [ ] `PCB-FAB.01c` — Place order: 5× controller PCB + 5× driver PCB, 4-layer, PCBA
- [ ] `PCB-FAB.01d` — Order through-hole components separately (Mouser/Digikey): connectors, headers, terminal blocks
- [ ] `PCB-FAB.01e` — Receive boards; visual inspection and continuity check

---

### PCB-FAB.02: Board bring-up — power test, STM32 flash, basic I/O validation
- **Sprint:** Pre-Sprint (Weeks -2 to -1)
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[PCB-pcb-design#PCB-FAB.01|PCB-FAB.01]]
- **Blocks:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]

**Acceptance Criteria:**
- [ ] Controller board: 5V and 3.3V rails within ±5% tolerance
- [ ] STM32 detected via SWD (ST-Link); LED blink test firmware flashed successfully
- [ ] Driver board: 12V rail stable under no-load and light-load conditions
- [ ] Board-to-board communication verified (GPIO toggle test)
- [ ] No component overheating under 5-minute power-on test

**Tasks:**
- [ ] `PCB-FAB.02a` — Hand-solder through-hole components (connectors, headers, terminal blocks)
- [ ] `PCB-FAB.02b` — Power controller board; measure 24V→5V→3.3V rails with multimeter
- [ ] `PCB-FAB.02c` — Connect ST-Link; flash LED blink firmware; verify SWD connection
- [ ] `PCB-FAB.02d` — Power driver board; measure 24V→12V rail; test MOSFET gate drive with function generator
- [ ] `PCB-FAB.02e` — Connect both boards; verify signal pass-through via GPIO toggling

---

## Dependencies

### What PCB blocks (downstream consumers)

| PCB Story | Blocks | Reason |
|-----------|--------|--------|
| PCB-FAB.02 | EMB-SET.01 | STM32 firmware needs validated hardware |
| PCB-FAB.02 | EMB-SET.02 | CM5 platform needs carrier board verified |

### What blocks PCB (upstream dependencies)

None — PCB is the first epic in the critical path.

---

## References

- [[__Workspaces/Epicura/docs/09-PCB/01-Controller-PCB-Design|Controller PCB Design]]
- [[__Workspaces/Epicura/docs/09-PCB/02-Driver-PCB-Design|Driver PCB Design]]
- [[__Workspaces/Epicura/docs/08-Components/01-Compute-Module-Components|Compute Module BOM]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
