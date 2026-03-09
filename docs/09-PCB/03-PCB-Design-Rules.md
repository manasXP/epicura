# PCB Design Rules

Design rules reference for the Epicura unified PCB (STM32 controller + power/driver electronics on a single 4-layer board). Rules are enforced via KiCad DRC in the `.kicad_pro` file.

**Related:** [[01-Unified-PCB-Design]]

---

## 1. Applicable Standards

| Standard | Scope |
|----------|-------|
| **IPC-2221B Class 2** | Dedicated-service electronics — track width, clearance, via sizing |
| **IPC-7351C** | Land pattern geometry (footprints) |
| **IEC 60335-1** | Household appliance safety — creepage & clearance for mains isolation |
| **JLCPCB DFM** | Fabrication capability limits for prototype and production runs |

---

## 2. Board Stackup

| Parameter | Value |
|-----------|-------|
| Layer count | 4 (F.Cu, GND plane, split power plane, B.Cu) |
| Board thickness | 1.6 mm |
| Substrate | FR-4 (Tg ≥ 150°C) |
| Copper weight (outer) | 2 oz (70 µm) — required for power traces |
| Copper weight (inner) | 1 oz (35 µm) — planes |
| Surface finish | ENIG (lead-free) |
| Solder mask | Green LPI, both sides |
| Silkscreen | White, both sides |
| Board dimensions | 160 × 90 mm |
| Layer 1 (Top) | Signal + Components (2 oz) |
| Layer 2 (Inner1) | GND Plane — continuous (1 oz) |
| Layer 3 (Inner2) | Split Power Plane: 5V/3.3V, 12V, 24V (1 oz) |
| Layer 4 (Bottom) | Signal + Power Traces (2 oz) |

---

## 3. Track Width by Current

Based on IPC-2221B external layer, 10°C temperature rise, 1 oz copper.

| Application | Width (mm) | Current Rating | Usage |
|-------------|-----------|----------------|-------|
| Signal (default) | 0.20 | < 0.5 A | GPIO, logic, misc signals |
| Bus (I2C/SPI/CAN) | 0.25 | < 0.5 A | Controlled-impedance bus signals |
| Light load | 0.30 | ~ 0.7 A | LED drivers, low-power rails |
| 1 A | 0.50 | 1.0 A | 5V rail, moderate loads |
| 2 A | 0.80 | 2.0 A | 12V distribution, motor enable |
| 3 A | 1.00 | 3.0 A | 24V main rail, induction supply |
| 5 A | 1.50 | 5.0 A | High-current motor/actuator feeds |

> [!tip] For currents above 5 A, use copper pours or parallel traces rather than single tracks.

---

## 4. Clearance Rules

| Context | Clearance (mm) | Rationale |
|---------|---------------|-----------|
| Signal-to-signal | 0.20 | IPC-2221B Class 2 minimum |
| Power-to-signal | 0.30 | Noise margin for DC rails |
| High-current-to-any | 0.50 | Thermal and voltage margin |
| CAN bus isolation (ISO1050) | 6.00 | IEC 60664-1 reinforced isolation |
| Mains relay AC traces | 2.50 | IEC 60335-1 basic insulation (250 VAC) |
| Copper-to-board-edge | 0.30 | JLCPCB minimum + margin |

---

## 5. Via Specifications

| Type | Pad Dia (mm) | Drill (mm) | Annular Ring (mm) | Usage |
|------|-------------|-----------|-------------------|-------|
| Standard | 0.60 | 0.30 | 0.15 | Signal routing, bus lines |
| Power | 0.80 | 0.40 | 0.20 | 5V, 12V, GND stitching |
| High-current | 1.00 | 0.50 | 0.25 | 24V, motor/actuator feeds |

> [!note] Use multiple vias in parallel for high-current layer transitions (e.g., 3× power vias for 24V feed).

---

## 6. Copper Pour

| Parameter | Value |
|-----------|-------|
| Bottom layer | GND flood fill (continuous ground plane) |
| Top layer | Selective pours for power rails where needed |
| Zone clearance | 0.50 mm (to pads and traces) |
| Thermal relief | Spoke width 0.5 mm, gap 0.5 mm |
| Min spoke count | 2 |
| Isolated copper | Remove (DRC warning → manual review) |

---

## 7. Creepage & Clearance (IEC 60335-1)

These rules apply to the **unified board** where mains-referenced signals exist (relay AC switching, induction module CAN interface).

| Insulation Type | Min Distance (mm) | Application |
|----------------|-------------------|-------------|
| Functional | 1.5 | Low-voltage signal separation |
| Basic (250 VAC) | 2.5 | Relay AC trace to DC traces |
| Reinforced | 6.0 | ISO1050 CAN bus isolation slot |

- Route an **isolation slot** (milled cutout) under the ISO1050 CAN transceiver, ≥ 6 mm wide
- No copper pour or traces may cross the isolation boundary
- Keep mounting holes and connectors ≥ 3 mm from isolation boundaries

---

## 8. Silkscreen

| Parameter | Min Value |
|-----------|-----------|
| Text height | 0.80 mm |
| Text line width | 0.15 mm |
| Clearance to pads | 0.15 mm |
| Reference designators | All components — F.Silkscreen |

---

## 9. JLCPCB Capability Limits

Absolute manufacturing minimums — our design rules are set above these for margin.

| Parameter | JLCPCB Min | Our Design Min |
|-----------|-----------|----------------|
| Trace width | 0.127 mm (5 mil) | 0.15 mm |
| Trace spacing | 0.127 mm (5 mil) | 0.20 mm |
| Drill diameter | 0.30 mm | 0.30 mm |
| Annular ring | 0.13 mm | 0.13 mm |
| Via pad diameter | 0.50 mm | 0.60 mm |
| Board-edge clearance | 0.20 mm | 0.30 mm |
| Silkscreen line | 0.10 mm | 0.15 mm |
| Silkscreen text | 0.80 mm height | 0.80 mm |

---

## 10. Net Class Definitions (Unified Board)

| Net Class | Track (mm) | Clearance (mm) | Via Pad/Drill (mm) | Nets |
|-----------|-----------|----------------|--------------------:|------|
| Default | 0.20 | 0.20 | 0.6 / 0.3 | All unassigned signals, GPIO |
| SPI | 0.25 | 0.20 | 0.6 / 0.3 | `SPI2_*` |
| I2C | 0.25 | 0.20 | 0.6 / 0.3 | `I2C1_SCL`, `I2C1_SDA` |
| CAN | 0.25 | 0.20 | 0.6 / 0.3 | `CAN_H`, `CAN_L`, `FDCAN1_*` |
| Power_3V3 | 0.50 | 0.30 | 0.8 / 0.4 | `+3V3`, `VDDA` |
| Power_5V | 0.50 | 0.30 | 0.8 / 0.4 | `+5V` |
| Power_12V | 0.80 | 0.30 | 0.8 / 0.4 | `12V_OUT`, `12V_UPS` |
| Power_24V | 1.00 | 0.30 | 1.0 / 0.5 | `24V_INT`, 24V nets |
| Power_GND | 0.50 | 0.30 | 0.8 / 0.4 | `GND` (uses L2 plane primarily) |
| USB | 0.20 | 0.20 | 0.6 / 0.3 | `USB_DP`, `USB_DM` — 90R differential impedance, length-matched within 0.5mm |
| HighCurrent | 1.50 | 0.50 | 1.0 / 0.5 | `LACT_O*`, `PUMP_O*`, `SOL*_D`, `FAN*_D` |

---

## 11. DRC Severity Policy

Rules configured in each `.kicad_pro` — key severity overrides from KiCad defaults:

| Check | Severity | Rationale |
|-------|----------|-----------|
| `clearance` | **error** | Hard constraint — must not violate |
| `track_width` | **error** | Must meet current-carrying minimums |
| `annular_width` | **error** | Manufacturing reliability |
| `hole_to_hole` | **error** | Upgraded from warning — structural integrity |
| `silk_over_copper` | **error** | Upgraded from warning — readability |
| `missing_courtyard` | **warning** | Upgraded from ignore — placement checking |
| `copper_sliver` | **warning** | Manufacturing defect risk |
| `isolated_copper` | **warning** | Review and remove manually |
| `footprint_type_mismatch` | **warning** | Upgraded from ignore — catch wrong footprints |

---

## 12. Design Settings Summary (`.kicad_pro`)

Global DRC minimums for the unified board:

```
min_clearance:             0.20 mm
min_track_width:           0.15 mm
min_via_annular_width:     0.13 mm
min_via_diameter:          0.60 mm
min_through_hole_diameter: 0.30 mm
min_copper_edge_clearance: 0.30 mm
min_hole_clearance:        0.25 mm
min_hole_to_hole:          0.25 mm
min_silk_clearance:        0.15 mm
min_text_height:           0.80 mm
min_text_thickness:        0.08 mm
```

---

## 13. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-03-09 | Manas Pradhan | Added USB differential pair net class (90R impedance, length-matched) for USB-C programming port |
| 1.0 | 2026-03-06 | Manas Pradhan | Initial design rules document for unified PCB — stackup, track widths, clearances, via specs, net classes, DRC policy, JLCPCB limits |
