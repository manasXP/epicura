---
created: 2026-02-15
modified: 2026-02-20
version: 2.0
status: Draft
---

# Mechanical Design

## Form Factor

### Device Type
**Autonomous Countertop Kitchen Robot** - Stationary appliance designed for compact Indian kitchens

### Dimensions
- **Width:** 500 mm
- **Depth:** 400 mm
- **Height:** 300 mm
- **Weight:** 8-12 kg (assembled, without pot contents)
- **Comparable Size:** Large microwave oven or bread maker

### Design Philosophy
- Compact footprint for limited countertop space
- All cooking operations contained within enclosure
- Removable components for easy cleaning
- Professional yet approachable kitchen appliance aesthetic
- All user-facing surfaces food-safe and wipe-clean

---

## Enclosure Design

### Material Selection

| Material | Pros | Cons | Cost | Recommendation |
|----------|------|------|------|----------------|
| **Polypropylene (PP)** | Food-safe, lightweight, cheap, chemical resistant | Lower rigidity, limited finish options | Low | **Prototype default** |
| **Stainless Steel (304 or 430)** | Premium look, durable, excellent heat resistance, easy to clean | Heavy, expensive, harder to fabricate complex shapes | High | Production premium model |
| **PC/ABS Blend** | Balanced strength/cost, good finish, common in appliances | Requires food-safe coating on interior surfaces | Medium | Production standard model |
| **Sheet Metal + PP Interior** | Hybrid: metal exterior, PP food-contact surfaces | More complex assembly | Medium-High | Best compromise |

### Pot Specifications

| Parameter | Value |
|-----------|-------|
| Material | Ferritic stainless steel base (induction-compatible) + aluminum body |
| Interior Coating | Ceramic non-stick or PTFE (Teflon) |
| Capacity | 3-4 liters |
| Diameter | 220 mm (matches microwave surface coil) |
| Height | 120-150 mm |
| Weight (empty) | 0.8-1.2 kg |
| Handles | Two folding side handles (heat-resistant silicone or Bakelite) |
| Lid | Optional, vented (for steam release during certain recipes) |
| Cleaning | Dishwasher-safe, removable |
| Detection | Ferromagnetic base detected by microwave surface module (internal pot detection) |

### Surface Finish

- **Exterior:** Matte anti-fingerprint texture (fine sand or soft-touch)
- **Interior (food zone):** Smooth, non-porous, food-grade approved
- **Color:** White body with dark gray or stainless accents (appliance standard)
- **Certification:** All food-contact materials comply with FDA 21 CFR / EU 10/2011

---

## Enclosure Layout

### Top View

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    ┌───────────────────────────────────────────────────┐     │
│    │                 Gantry Bridge                      │     │
│    │    ┌────────┐                     ┌─────────┐     │     │
│    │    │ Camera │                     │  Arm    │     │     │
│    │    │ + LED  │                     │  Motor  │     │     │
│    │    │ Ring   │                     │ (BLDC) │     │     │
│    │    └───┬────┘                     └────┬────┘     │     │
│    │        │                               │          │     │
│    └────────┼───────────────────────────────┼──────────┘     │
│             │                               │                │
│    ┌────────┼───────────────────────────────┼──────────┐     │
│    │        ▼          Pot Well             ▼          │     │
│    │   ┌─────────────────────────────────────────┐    │     │
│    │   │              ┌─────────┐                │    │     │
│    │   │              │  Pot    │                │    │     │
│    │   │              │ (22cm)  │                │    │     │
│    │   │              │         │                │    │     │
│    │   │              └─────────┘                │    │     │
│    │   │          Stirring Paddle Path           │    │     │
│    │   └─────────────────────────────────────────┘    │     │
│    │                                                   │     │
│    │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │     │
│    │  │ASD-1│ │ASD-2│ │ASD-3│  SLD-OIL  SLD-H2O   │     │
│    │  │     │ │     │ │     │  [pump]    [pump]    │     │
│    │  └──┬──┘ └──┬──┘ └──┬──┘                      │     │
│    │     └───────┴───────┘    CID-1    CID-2       │     │
│    │     ASD (Seasonings)    [tray]    [tray]       │     │
│    └───────────────────────────────────────────────────┘     │
│                                                              │
│    [E-STOP]                                   [Status LEDs] │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                        500 mm
```

### Front View

```
                         500 mm
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│              ┌──────────────────────────────┐                │
│              │      Gantry + Camera         │    300 mm      │
│              │         + Arm                │    (height)    │
│              └──────────────────────────────┘                │
│                                                              │
│    ┌──────────────────────────────────────────────────┐      │
│    │                                                  │      │
│    │          10" Touchscreen Display                 │      │
│    │          (angled 15-30 degrees)                  │      │
│    │                                                  │      │
│    │   ┌──────────────────────────────────────────┐   │      │
│    │   │                                          │   │      │
│    │   │        Recipe UI / Camera Feed           │   │      │
│    │   │        Progress / Controls               │   │      │
│    │   │                                          │   │      │
│    │   └──────────────────────────────────────────┘   │      │
│    │                                                  │      │
│    └──────────────────────────────────────────────────┘      │
│                                                              │
│  [E-STOP]          Pot Access Opening         [Status LEDs]  │
│  (Red button)      (user inserts/removes pot)  (RGB strip)   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Non-slip rubber feet (4x corner)
```

### Rear View

```
                         500 mm
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    ┌────────────────────────────────────────────────────┐    │
│    │              Ventilation Grille                     │    │
│    │    (air exhaust from internal fan)                  │    │
│    └────────────────────────────────────────────────────┘    │
│                                                              │
│    ┌────────┐    ┌─────────┐    ┌─────────┐                  │
│    │ IEC C14│    │ USB-C   │    │ Reset   │                  │
│    │ Power  │    │ Debug/  │    │ Button  │                  │
│    │ Inlet  │    │ Update  │    │ (recessed│                  │
│    │ + Fuse │    │         │    │  pinhole)│                  │
│    └────────┘    └─────────┘    └─────────┘                  │
│                                                              │
│    ┌────────────────────────────────────────────────────┐    │
│    │              Ventilation Grille                     │    │
│    │    (air intake for PSU cooling)                    │    │
│    └────────────────────────────────────────────────────┘    │
│                                                              │
│    Rating plate: Model, serial, certifications, power specs  │
└──────────────────────────────────────────────────────────────┘
```

### Side View (Cross-Section)

```
                         400 mm (depth)
    ◄──────────────────────────────────────────────────────►

    ┌──────────────────────────────────────────────────────┐ ─┬─
    │            Gantry (Camera + Arm Motor)                │  │
    │    ┌────────┐                        ┌──────────┐    │  │
    │    │ Camera │                        │ BLDC    │    │  │
    │    │ + LEDs │        Arm Shaft       │ Motor   │    │  │
    │    └────┬───┘        ▼               └────┬─────┘    │  │
    │         │   ┌────────────────────┐        │          │  │
    ├─────────┼───┤  Pot + Food Zone   ├────────┼──────────┤  │
    │         │   │  (open top access)  │        │          │  │ 300mm
    │         │   └────────┬───────────┘        │          │  │
    │         │            │                    │          │  │
    │  ┌──────┴────────────┴──────────────┬─────┴──────┐   │  │
    │  │          Pot Platform            │            │   │  │
    │  │   (Load Cells underneath)        │            │   │  │
    │  ├──────────────────────────────────┤  Display   │   │  │
    │  │   Induction Coil + Ferrite       │  (tilted   │   │  │
    │  │   (center-bottom)                │   15-30)   │   │  │
    │  ├────────┬─────────────────────────┤            │   │  │
    │  │  PSU   │  STM32 PCB │ CM5 Module │            │   │  │
    │  │ (rear  │  (side)    │ (rear-top) │            │   │  │
    │  │ bottom)│            │            │            │   │  │
    │  └────────┴────────────┴────────────┴────────────┘   │  │
    │  ▓▓▓▓ Fan (PSU intake) ▓▓▓▓ Fan (exhaust) ▓▓▓▓▓▓▓  │  │
    └──────────────────────────────────────────────────────┘ ─┴─
```

---

## Internal Layout

### Component Arrangement (Cross-Section, Top Down)

```
┌──────────────────────────────────────────────────────────────┐
│                        REAR                                  │
│                                                              │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐  │
│  │  PSU Module   │  │  CM5 Module   │  │  Ventilation    │  │
│  │  (AC-DC)      │  │  (+ Carrier)  │  │  Fan (exhaust)  │  │
│  │  Multi-rail   │  │  WiFi antenna │  │  40mm, 12V      │  │
│  │               │  │  near rear    │  │                  │  │
│  └──────┬────────┘  └──────┬────────┘  └──────────────────┘  │
│         │                  │                                 │
│  ┌──────▼──────────────────▼──────────────────────────────┐  │
│  │                  Thermal Barrier                       │  │
│  │   (aluminum sheet or silicone thermal pad)             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────┐  ┌─────────────────────────────────────┐  │
│  │  STM32 PCB   │  │     Microwave Induction Surface      │  │
│  │  (motor ctrl │  │    (self-contained module,            │  │
│  │   + sensors) │  │     center-bottom, CAN interface)     │  │
│  │              │  │                                       │  │
│  └──────────────┘  └─────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Load Cells (4x corners of platform)       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│                        FRONT                                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Pot Design

### Specifications

| Parameter | Value |
|-----------|-------|
| Body Material | Aluminum alloy (3003 or 5052, food-grade) |
| Base | Ferritic stainless steel disc (430 grade, induction-compatible) |
| Interior Coating | Ceramic non-stick (PFOA-free) or PTFE |
| Capacity | 3-4 liters (useful volume) |
| Outer Diameter | 220 mm |
| Inner Diameter | 210 mm |
| Height | 130 mm |
| Wall Thickness | 3 mm (aluminum body) |
| Base Thickness | 5 mm (stainless + aluminum composite) |
| Weight (empty) | 0.8-1.2 kg |
| Max Operating Temp | 260C (limited by non-stick coating) |

### Detection Mechanism

- Pot detection is handled internally by the microwave induction surface module
- Module detects ferromagnetic pot base via impedance sensing
- No external reed switch or magnet required
- Interlock: module will not heat without pot detected (internal safety)

### Handle Design

- Two folding side handles: stow flat against pot body, flip out for lifting
- Material: Bakelite or silicone-wrapped stainless steel
- Heat rating: handles remain <60C even when pot contents at 250C
- Clearance: handles fit through gantry opening when folded

---

## Robotic Arm Assembly

### Gantry-Mounted Stirring System

```
┌─────────────────────────────────────────────────────────┐
│                    Gantry Top View                       │
│                                                         │
│    ┌──────────────────────────────────────────────┐     │
│    │              Gantry Bridge                    │     │
│    │                                               │     │
│    │   ┌─────────┐                 ┌────────────┐  │     │
│    │   │ Camera  │   Gantry Arm    │  BLDC     │  │     │
│    │   │ Module  │◄───────────────►│  Motor    │  │     │
│    │   │ + LED   │                 │  (24V)    │  │     │
│    │   └─────────┘                 └─────┬──────┘  │     │
│    │                                     │         │     │
│    └─────────────────────────────────────┼─────────┘     │
│                                          │               │
│                                     Shaft (vertical)     │
│                                          │               │
│                                     ┌────▼─────┐         │
│                                     │ Silicone │         │
│                                     │ Gasket   │         │
│                                     │ (IPX5    │         │
│                                     │  seal)   │         │
│                                     └────┬─────┘         │
│                                          │               │
│                                     ┌────▼─────┐         │
│                                     │ Paddle   │         │
│                                     │ Attach-  │         │
│                                     │ ment     │         │
│                                     │ (remov-  │         │
│                                     │  able)   │         │
│                                     └──────────┘         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Arm Specifications

| Parameter | Value |
|-----------|-------|
| Actuator | 24V BLDC motor with integrated ESC (30-50 kg-cm torque) |
| Rotation | 360 degrees continuous (modified servo or stepper alternative) |
| Speed Range | 10-60 RPM (adjustable via recipe) |
| Shaft Material | 304 stainless steel, 8mm diameter |
| Shaft Length | 150 mm (extends from gantry into pot) |
| Depth Adjustment | Fixed depth (set during assembly for target pot) |
| Paddle | Food-grade silicone or nylon, removable twist-lock |
| Seal | Silicone gasket around shaft penetration (IPX5 rated) |
| Cleaning | Shaft and paddle removable, dishwasher-safe |

### Stirring Patterns

The recipe engine commands different stirring patterns:

| Pattern ID | Name | Description | RPM | Use Case |
|------------|------|-------------|-----|----------|
| 0 | Stop | Arm stationary | 0 | Idle, dispensing, settling |
| 1 | Slow Continuous | Steady rotation | 10-15 | Gentle simmer, prevent sticking |
| 2 | Medium Continuous | Moderate rotation | 20-30 | Active cooking, mixing ingredients |
| 3 | Fast Continuous | Vigorous rotation | 40-60 | Rapid mixing, emulsification |
| 4 | Intermittent | 5s on / 10s off | 20 | Light stirring during slow cook |
| 5 | Reverse Alternating | CW 10s / CCW 10s | 25 | Better mixing, prevent vortex |

---

## Ingredient Dispensing Subsystems

See [[../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing System]] for full details.

### Layout and Design

```
                    ┌─────────────────────────────────────┐
                    │     Dispensing Layout (Top View)      │
                    │                                       │
                    │  ASD (Rear, behind pot):               │
                    │  ┌──────┐ ┌──────┐ ┌──────┐           │
                    │  │ASD-1 │ │ASD-2 │ │ASD-3 │           │
                    │  │Turmer│ │Chili │ │Salt/ │           │
                    │  │ 80mL │ │ 80mL │ │Masala│           │
                    │  └──┬───┘ └──┬───┘ └──┬───┘           │
                    │     │SG90    │SG90    │SG90            │
                    │     └────────┴────────┘                │
                    │            ▼ Gravity Drop              │
                    │                                       │
                    │  SLD (Left/Right sides):               │
                    │  SLD-OIL ═══► Pot ◄═══ SLD-WATER      │
                    │  [pump+sol]         [pump+sol]         │
                    │                                       │
                    │  CID (Front, below pot):               │
                    │  ┌──────────┐  ┌──────────┐           │
                    │  │  CID-1   │  │  CID-2   │           │
                    │  │Vegetables│  │ Dal/Rice │           │
                    │  │ 400mL   │  │ 400mL    │           │
                    │  │[LinAct] │  │[LinAct]  │           │
                    │  └─────┬────┘  └─────┬────┘           │
                    │        ▼             ▼                 │
                    │      Push into Pot                     │
                    └─────────────────────────────────────┘
```

### Subsystem Specifications

| Parameter | ASD (Seasonings) | CID (Coarse) | SLD (Liquids) |
|-----------|-----------------|-------------|--------------|
| Count | 3 hoppers | 2 trays | 2 channels (oil + water) |
| Capacity | 80 mL each | 400 mL each | 200 mL (oil), 500 mL (water) |
| Material | Food-grade PP | Food-grade PP | PP reservoirs + silicone tubing |
| Actuator | SG90 servo gate | 12V linear actuator | Peristaltic pump + solenoid valve |
| Metering | Pot load cells (±10%) | Position-based | Dedicated load cell (±5%) |
| Cleaning | Removable, dishwasher-safe | Slide-out, dishwasher-safe | Removable reservoir; tubing replaceable |

### Dispensing Sequence

**ASD:** Recipe engine sends `DISPENSE_ASD(id, target_g)` → STM32 opens servo gate → monitors pot weight → closes at target

**CID:** Recipe engine sends `DISPENSE_CID(id, FULL)` → STM32 drives linear actuator → ingredients pushed off tray into pot → actuator retracts

**SLD:** Recipe engine sends `DISPENSE_SLD(channel, target_g)` → STM32 opens solenoid + starts pump → monitors reservoir weight loss → stops pump + closes solenoid at target
8. Recipe engine logs dispensed amount and proceeds

---

## Thermal Management

### Heat Sources

| Source | Typical Heat Dissipation | Location |
|--------|--------------------------|----------|
| Microwave surface module | 30-100W (waste heat at 85% efficiency) | Center-bottom |
| PSU (switch-mode) | 15-30W (at full load, ~85% efficient) | Rear-bottom |
| CM5 compute module | 3-5W | Rear-top |
| STM32 + sensors | <1W | Side |
| BLDC stirring motor | 12-48W (intermittent) | Top gantry |

### Cooling Strategy

```
┌────────────────────────────────────────────────────────────┐
│                    Airflow Path (Side View)                 │
│                                                            │
│    Exhaust ◄──── Fan 2 (40mm, 12V)                        │
│    Grille        (rear-top, pulls hot air out)             │
│    (rear)                  ▲                               │
│                            │                               │
│                   ┌────────┴──────────┐                    │
│                   │  CM5 heatsink     │                    │
│                   │  (passive, aluminum)                   │
│                   └───────────────────┘                    │
│                            ▲                               │
│                   ┌────────┴──────────┐                    │
│                   │  Thermal barrier  │                    │
│                   │  (isolates coil   │                    │
│                   │   heat from PCBs) │                    │
│                   └───────────────────┘                    │
│                            ▲                               │
│                   ┌────────┴──────────┐                    │
│                   │  Module heatsink  │                    │
│                   │  (internal to     │                    │
│                   │   module)         │                    │
│                   └───────────────────┘                    │
│                            ▲                               │
│    Intake ────► Fan 1 (40mm, 12V)                         │
│    Grille       (rear-bottom, pushes cool air in)          │
│    (rear)                                                  │
└────────────────────────────────────────────────────────────┘

Dual-fan push-pull configuration:
  Fan 1 (bottom): intake fresh air, cools PSU and electronics
  Fan 2 (top): exhaust hot air past CM5
  Airflow path avoids pot/food zone (no contamination risk)
```

### Thermal Barriers

- **Silicone thermal pad** or **aluminum shield** between microwave surface module and PSU compartment
- **Air gap** (minimum 10mm) between microwave surface module and PSU
- **Operating ambient range:** 0-40C (indoor kitchen environment)
- **Maximum internal temp:** 70C at any PCB location (exhaust fan manages airflow)

### Cooking Fume Exhaust

A separate exhaust system handles cooking fumes (steam, oil smoke, spice volatiles) from the pot zone. This is independent of the electronics cooling airflow to prevent food contamination of electronic components.

- **Exhaust fan:** 60mm PWM fan, mounted rear-top, draws fumes upward from pot zone
- **Filtration:** Dual-stage slide-out cartridge (stainless steel grease mesh + activated carbon)
- **Collection hood:** Integrated into gantry above pot, directs fumes toward exhaust duct
- **Intake:** Passive side/bottom vents provide makeup air via negative pressure

See [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]] for full specifications, filter design, and safety interlocks.

---

## Ergonomics

### Touchscreen

- **Angle:** Tilted 15-30 degrees from vertical (optimal viewing while standing at kitchen counter)
- **Height:** Screen center at ~200mm from countertop (within natural downward gaze)
- **Size:** 10.1" diagonal, large enough for recipe steps and camera feed
- **Touch:** Capacitive (works with dry fingers, not with wet/gloved hands -- design assumes user dries hands)

### Cleaning Design

| Component | Cleaning Method | Removable |
|-----------|----------------|-----------|
| Pot | Dishwasher or hand wash | Yes |
| Stirring paddle | Dishwasher or hand wash | Yes (twist-lock) |
| Stirring shaft | Wipe with damp cloth | Yes (pull-out) |
| ASD hoppers (×3) | Dishwasher or hand wash | Yes (lift out) |
| CID trays (×2) | Dishwasher or hand wash | Yes (slide out) |
| SLD reservoirs (×2) | Dishwasher or hand wash | Yes (lift out) |
| SLD tubing (×2) | Hand wash / boil sterilize | Yes (disconnect) |
| Pot platform | Wipe with damp cloth | No (fixed, sealed surface) |
| Exterior surfaces | Wipe with damp cloth | No |
| Display | Wipe with soft cloth | No |
| Gantry area | Wipe with damp cloth | No (sealed against steam) |

### Auto-Rinse Cycle (Future Feature)

Optional automated cleaning: fill pot with water, heat to 60C, stir for 5 minutes, drain. Requires drain valve (not included in prototype).

### Cable Management

- Single power cable (IEC C14 with detachable cord)
- Cable exit from rear-bottom
- No user-facing cables during operation
- USB-C debug port recessed on rear panel (not for daily use)

### Non-Slip Feet

- 4x rubber feet at corners of base
- Diameter: 20mm each
- Height: 5mm (provides ventilation clearance under base)
- Material: Silicone or TPE (thermoplastic elastomer)

---

## DFM Considerations

### Prototype Phase

| Component | Fabrication Method | Notes |
|-----------|-------------------|-------|
| Enclosure (body) | 3D printed (FDM, PETG or ABS) | Iterative design, <$100 per print |
| Enclosure (pot well) | 3D printed + aluminum sheet insert | Heat-resistant surface near coil |
| Pot | Off-the-shelf induction pot (22cm) | Modified with embedded magnet |
| Gantry | Aluminum extrusion + 3D printed brackets | Standard 2020 or 2040 V-slot |
| ASD hoppers + CID trays | 3D printed (food-safe PETG) | Or silicone mold for flexibility |
| PCBs | 4-layer custom PCB (JLCPCB or similar) | 2 boards: CM5 carrier, STM32 control |
| Wiring | Hand-soldered, JST/Dupont connectors | Label all connectors |

### Production Phase

| Component | Fabrication Method | Notes |
|-----------|-------------------|-------|
| Enclosure (body) | Injection mold (PC/ABS blend) | Tooling cost ~$5,000-15,000, <$5/unit |
| Enclosure (pot well) | Stamped stainless steel | Press-formed, integrated with base |
| Pot | Custom die-cast aluminum + SS base | With embedded magnet, non-stick coated |
| Gantry | Zinc die-cast or stamped steel | Integrated camera/motor mounts |
| ASD/CID housings | Injection mold (food-grade PP) | Tooling ~$2,000 per shape |
| PCBs | SMT assembly (pick-and-place) | Panelized, automated testing |
| Assembly | Semi-automated line | Target 30 min per unit |

### Assembly Sequence (Prototype)

1. Mount microwave induction surface module into base
2. Route CAN bus cable from module to controller PCB
3. Place load cells on platform mounting points
4. Install pot platform over load cells
5. Mount PSU module in rear-bottom compartment
6. Install STM32 control PCB on side bracket
7. Install CM5 + carrier board in rear-top area
8. Wire PSU to all DC loads (color-coded connectors)
9. Wire STM32 to sensors, servos, CAN bus (to microwave surface)
10. Wire CM5 UART to STM32
11. Connect camera FFC cable, mount camera on gantry
12. Mount display, connect DSI/HDMI and I2C touch
13. Install gantry assembly (bridge + arm motor + camera)
14. Install dispensing subsystems: ASD hoppers + servos, CID trays + linear actuators, SLD pumps + solenoids + tubing
15. Install fans, E-stop button, LED ring
16. Close enclosure, connect power cord
17. Power-on test and calibration

---

## Related Documentation

- [[02-Technical-Specifications|Technical Specifications]]
- [[Epicura-Architecture|Hardware Architecture & Wiring Diagrams]]
- [[05-Sensors-Acquisition|Sensors & Data Acquisition]]
- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]]
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]]

#epicura #mechanical-design #enclosure #industrial-design

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-20 | Manas Pradhan | Replaced DS3225 servo references with 24V BLDC motor |
