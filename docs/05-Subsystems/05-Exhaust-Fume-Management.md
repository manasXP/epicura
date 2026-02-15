---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Exhaust & Fume Management System

## Overview

Indian one-pot cooking — especially tadka (tempering), searing, and deep-frying — produces significant steam, oil smoke, and volatile fumes inside the semi-enclosed Epicura enclosure. Without active extraction, these byproducts degrade the camera image (fogging), corrode electronics, and create an unpleasant user experience. The exhaust system must extract cooking fumes while maintaining safe internal temperatures and protecting sensitive components.

### Design Goals

- Extract steam and oil smoke before they reach the camera lens and electronics
- Filter odors and grease particles before exhausting into the kitchen
- Operate quietly (<45 dB) at typical cooking speeds
- Scale fan speed automatically based on cooking stage (idle → simmer → sear)
- Replaceable filter cartridge accessible without tools

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                   Exhaust Airflow Path (Side View)               │
│                                                                  │
│   Kitchen Air ◄──── Exhaust Outlet ◄──── Carbon Filter          │
│   (clean/filtered)   (rear-top grille)    (odor absorption)     │
│                                              ▲                   │
│                                       ┌──────┴───────┐          │
│                                       │  Mesh/Grease │          │
│                                       │  Pre-Filter  │          │
│                                       │  (washable)  │          │
│                                       └──────┬───────┘          │
│                                              ▲                   │
│                                       ┌──────┴───────┐          │
│                                       │  Exhaust Fan │          │
│                                       │  60mm, PWM   │          │
│                                       │  (12V, STM32)│          │
│                                       └──────┬───────┘          │
│                                              ▲                   │
│                              ┌───────────────┴────────┐         │
│                              │   Fume Collection Hood │         │
│                              │   (above pot opening)  │         │
│                              │   ┌─────────────────┐  │         │
│                              │   │  Camera + LEDs  │  │         │
│                              │   └─────────────────┘  │         │
│                              └────────────┬───────────┘         │
│                                           ▲                      │
│                                    ┌──────┴───────┐             │
│                                    │     Pot      │             │
│                                    │  (cooking)   │             │
│                                    └──────────────┘             │
│                                                                  │
│   Fresh air ────► Intake vent (side/bottom)                      │
│   (ambient)       (passive or fan-assisted)                      │
└──────────────────────────────────────────────────────────────────┘
```

### Airflow Sequence

1. **Source:** Steam, oil smoke, and volatile fumes rise from the pot during cooking
2. **Collection:** Fume collection hood above the pot opening captures rising fumes via natural convection + fan suction
3. **Fan:** 60mm PWM exhaust fan draws air upward through the extraction path
4. **Pre-filter:** Stainless steel mesh / grease filter catches oil droplets and larger particles
5. **Carbon filter:** Activated carbon cartridge absorbs odors and volatile organics
6. **Exhaust:** Filtered air exits through rear-top grille into the kitchen
7. **Makeup air:** Fresh ambient air enters through side/bottom intake vents (passive, no fan needed — negative pressure from exhaust fan draws air in)

---

## Exhaust Fan

### Specifications

| Parameter | Value |
|-----------|-------|
| **Type** | Axial fan, brushless DC |
| **Size** | 60x60x25mm (prototype) |
| **Voltage** | 12V DC |
| **Current** | 0.15-0.25A |
| **Airflow** | 15-25 CFM (at full speed) |
| **Static Pressure** | 2-4 mm H2O (sufficient for filter resistance) |
| **Noise** | <35 dB at 50% speed, <45 dB at 100% |
| **Control** | 4-pin PWM (25 kHz) from STM32 TIM channel |
| **Connector** | Standard 4-pin fan header |
| **Bearing** | Sleeve or dual ball-bearing (kitchen humidity tolerance) |
| **Mounting** | Rear-top panel, rubber anti-vibration grommets |

### Speed Control Profiles

The STM32 modulates fan speed based on the current cooking stage commanded by the recipe engine:

| Cooking Stage | Fan PWM Duty | Speed | Rationale |
|---------------|-------------|-------|-----------|
| **Off / Idle** | 0% | Off | No fumes |
| **Warm (60-70C)** | 20% | Low | Minimal steam |
| **Simmer (80-95C)** | 40% | Medium | Moderate steam |
| **Boil (100C)** | 70% | High | Heavy steam |
| **Sear / Tadka (200-250C)** | 100% | Max | Oil smoke + volatile fumes |
| **Post-cook cooldown** | 50% | Medium | Clear residual fumes, 2-min timer |

### STM32 Control Interface

```c
// Exhaust fan PWM configuration
// TIM4 CH3, 25 kHz PWM, 12V fan via MOSFET
#define EXHAUST_FAN_TIM        TIM4
#define EXHAUST_FAN_CHANNEL    TIM_CHANNEL_3
#define EXHAUST_FAN_GPIO       GPIOB
#define EXHAUST_FAN_PIN        GPIO_PIN_8

typedef struct {
    uint8_t  duty_percent;    // 0-100%
    uint8_t  stage_override;  // manual override from CM5
    uint16_t rpm_feedback;    // tachometer reading (optional)
} exhaust_fan_t;

void exhaust_set_speed(uint8_t duty_percent) {
    uint32_t pulse = (EXHAUST_FAN_TIM->ARR * duty_percent) / 100;
    __HAL_TIM_SET_COMPARE(EXHAUST_FAN_TIM, EXHAUST_FAN_CHANNEL, pulse);
}
```

### CM5-STM32 Command Integration

| Command | Code | Payload | Description |
|---------|------|---------|-------------|
| `SET_EXHAUST` | `0x60` | `uint8_t duty` | Set fan speed (0-100%) |
| `GET_EXHAUST` | `0x61` | — | Query current speed + RPM |
| `EXHAUST_AUTO` | `0x62` | `uint8_t stage_id` | Auto-select speed for cooking stage |

The recipe engine sends `EXHAUST_AUTO` at each cooking stage transition. Manual override via `SET_EXHAUST` is available for recipes that need custom fume management (e.g., dry-roasting spices).

---

## Filtration System

### Dual-Stage Filter Stack

```
┌────────────────────────────────────┐
│         Filter Cartridge           │
│    (slides out from rear panel)    │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Stage 2: Activated Carbon   │  │
│  │  - Granular coconut shell    │  │
│  │  - 10-15mm thick layer       │  │
│  │  - Absorbs VOCs and odors    │  │
│  │  - Replace every 3-6 months  │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Stage 1: Grease Mesh        │  │
│  │  - 304 stainless steel mesh  │  │
│  │  - Captures oil droplets     │  │
│  │  - Dishwasher-safe           │  │
│  │  - Clean every 2-4 weeks     │  │
│  └──────────────────────────────┘  │
│                                    │
│  Frame: PP or ABS, snap-fit        │
│  Dimensions: ~80x80x30mm           │
└────────────────────────────────────┘
```

### Filter Specifications

| Filter Stage | Material | Purpose | Maintenance | Estimated Cost |
|-------------|----------|---------|-------------|----------------|
| **Stage 1: Grease mesh** | 304 SS woven mesh (40-60 mesh) | Trap oil particles, prevent carbon fouling | Wash in dishwasher every 2-4 weeks | $3 (reusable) |
| **Stage 2: Carbon** | Coconut shell activated carbon granules | Absorb odors, smoke VOCs, spice volatiles | Replace cartridge every 3-6 months | $5-8 per refill |

### Filter Housing

- **Slide-out cartridge** accessible from rear panel — no tools required
- **Snap-fit frame** holds both filter stages in correct order
- **Gasket seal** (silicone) prevents fume bypass around the filter edges
- **Visual indicator:** Carbon filter has a date label; future production could add a filter-hours counter in the UI

### Filter Performance

| Pollutant | Source | Pre-filter Capture | Carbon Capture | Combined |
|-----------|--------|-------------------|----------------|----------|
| Oil droplets | Tadka, frying | >90% | — | >90% |
| Smoke particles | Searing, burning | 40-60% | 30-40% | 70-80% |
| VOCs / odors | Spices, onions, garlic | <10% | 70-90% | 70-90% |
| Steam (water vapor) | Boiling, simmering | <5% | <5% | <5% (passes through) |

> [!note]
> Steam (water vapor) is not filtered — it passes through and exits as moisture. A condensation approach (cold surface or lid drip channel) can reduce steam volume before it reaches the filter. See [[../02-Hardware/07-Mechanical-Design|Mechanical Design]] for pot lid condensation channel design.

---

## Fume Collection Hood

### Design

The fume collection hood sits above the pot opening, integrated into the overhead gantry that already holds the camera and LED ring. It uses the natural upward convection of hot cooking fumes combined with exhaust fan suction.

```
┌───────────────────────────────────────┐
│          Gantry (Top View)            │
│                                       │
│   ┌───────────────────────────────┐   │
│   │         Hood Opening          │   │
│   │   ┌───────────────────────┐   │   │
│   │   │   Camera + LED Ring   │   │   │
│   │   └───────────────────────┘   │   │
│   │                               │   │
│   │   Angled baffles direct fumes │   │
│   │   toward exhaust duct ────────┼───┼──► To filter + fan
│   │                               │   │
│   └───────────────────────────────┘   │
│                                       │
│   Pot opening below                   │
└───────────────────────────────────────┘
```

### Key Design Points

- **Hood material:** Stainless steel or heat-resistant PP (same as enclosure interior)
- **Camera protection:** The hood directs fumes laterally toward the exhaust duct, away from the camera lens. Combined with the camera's anti-fog glass cover (see [[12-Vision-System|Vision System]]), this minimizes lens fogging
- **Baffle angle:** 15-30° inward slope channels rising fumes toward the exhaust duct
- **Hood clearance:** 30-50mm above pot rim to allow paddle/arm movement
- **Duct cross-section:** 60x60mm (matches fan) with smooth interior to reduce resistance

---

## Steam Management

### Pot Lid Integration

For recipes that require covered cooking (e.g., rice, pressure-style dal), the pot lid provides passive steam management:

| Lid Feature | Purpose |
|-------------|---------|
| **Vent hole** | Controlled steam release (prevents pressure buildup) |
| **Condensation ring** | Underside ridge returns condensed water to pot (reduces steam volume) |
| **Silicone gasket** | Loose-fit seal — allows steam out through vent, not around edges |

### Condensation Strategy

For heavy-steam recipes (boiling, covered simmering), reducing steam volume before it reaches the exhaust:

1. **Lid condensation:** ~30-40% of steam condenses on the lid underside and drips back
2. **Hood cool surface:** Stainless steel hood interior acts as secondary condensation surface
3. **Remaining steam:** Passes through grease mesh + carbon filter and exits as warm moist air
4. **Kitchen ventilation:** Users should still use their kitchen exhaust fan / chimney for heavy cooking (same as any stovetop appliance)

---

## Safety Considerations

### Fire Risk Mitigation

| Hazard | Mitigation |
|--------|-----------|
| Grease buildup in filter | Washable SS mesh; cleaning reminder in app every 2-4 weeks |
| Carbon filter ignition | Carbon is downstream of grease mesh (minimal oil exposure); max air temp at filter <80C during normal operation |
| Fan failure during high-heat cooking | STM32 monitors fan RPM via tachometer; if fan stalls during sear/tadka, sends CAN command to reduce power to simmer and alerts user |
| Blocked exhaust (clogged filter) | Pressure drop sensor (optional) or timer-based replacement reminder |

### Fan-Induction Interlock

The exhaust fan is interlocked with the microwave induction surface for safety:

```
┌─────────────────────────────────────────────────┐
│           Fan-Heater Interlock                    │
│                                                   │
│   Heating ON ──► Fan must be running              │
│                  (minimum 20% duty)               │
│                                                   │
│   Fan stall detected ──► Send CAN command to      │
│                          reduce to simmer (400W)   │
│                          Alert CM5 + user          │
│                                                   │
│   Fan confirmed OFF ──► Block sear/boil profiles  │
│                         (allow simmer/warm only)   │
│                                                   │
│   Post-cook ──► Fan runs 2 min after heating      │
│                 off (clear residual fumes)         │
└─────────────────────────────────────────────────────┘
```

### Compliance Notes

- Fan and filter assembly must meet IEC 60335-2-6 requirements for cooking appliance ventilation
- Grease filter material must be non-flammable (304 SS passes; PP frame must be flame-retardant grade V-0)
- Carbon filter must not release particles into food zone (downstream position + sealed cartridge prevents this)
- Exhaust outlet must not direct hot/moist air toward user-facing surfaces

---

## Component List

| Component | Part | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|------|-----|------------|----------|----------|-------|
| Exhaust Fan (60mm, PWM) | Noctua NF-A6x25 or generic | 1 | $8.00 | $8.00 | Amazon / AliExpress | 4-pin PWM, 12V, ball-bearing |
| Grease Mesh Filter | 304 SS woven, 40-mesh | 1 | $3.00 | $3.00 | AliExpress | Cut to 80x80mm, reusable |
| Activated Carbon Cartridge | Coconut shell granular | 1 | $5.00 | $5.00 | Amazon | ~100g, refillable frame |
| Filter Frame (3D printed) | ABS or PP, snap-fit | 1 | $2.00 | $2.00 | Self-fabricated | Holds both filter stages |
| Exhaust Duct (60mm) | Sheet metal or PP tube | 1 | $3.00 | $3.00 | Hardware store | Hood-to-fan channel |
| Silicone Gasket (filter seal) | Food-grade silicone strip | 1 | $1.00 | $1.00 | Amazon | Prevents fume bypass |
| Fan MOSFET (PWM driver) | IRLZ44N or AO3400 | 1 | $0.50 | $0.50 | DigiKey / LCSC | Logic-level gate, STM32 PWM |
| **Category Subtotal** | | | | **$22.50** | | |

### Production Cost Projection

| Item | Prototype | Production (1000 qty) | Savings |
|------|-----------|----------------------|---------|
| Exhaust fan | $8.00 | $3.00 (OEM blower) | 63% |
| Filters (mesh + carbon) | $8.00 | $3.00 | 63% |
| Duct + housing + gasket | $6.00 | $2.00 (injection molded) | 67% |
| MOSFET + wiring | $0.50 | $0.20 | 60% |
| **Total** | **$22.50** | **~$8.20** | **64%** |

---

## Maintenance Schedule

| Task | Frequency | User Action | Time |
|------|-----------|-------------|------|
| Wash grease mesh | Every 2-4 weeks | Remove cartridge, wash mesh in dishwasher or hot soapy water | 5 min |
| Replace carbon filter | Every 3-6 months | Slide out cartridge, swap carbon refill, slide back in | 2 min |
| Clean exhaust duct | Every 6 months | Wipe interior with damp cloth | 5 min |
| Check fan operation | Monthly (automated) | STM32 runs fan self-test on boot; alerts user if RPM drops | Automatic |

The companion app tracks filter usage hours and sends maintenance reminders.

---

## Testing & Validation

### Test Procedures

- [ ] Fan speed: verify PWM duty maps to expected RPM (0%, 25%, 50%, 75%, 100%)
- [ ] Airflow: confirm 15+ CFM with both filters installed (anemometer at exhaust outlet)
- [ ] Noise: measure <45 dB at 300mm distance at full speed
- [ ] Grease capture: cook tadka (oil + mustard seeds), inspect mesh for oil residue
- [ ] Odor reduction: cook onion-garlic base, compare exhaust smell with/without carbon filter
- [ ] Steam handling: boil 2L water for 10 min, check camera lens for fogging
- [ ] Fan interlock: simulate fan stall during sear mode, verify heater power reduction via CAN
- [ ] Post-cook purge: verify fan runs 2 min after heating off
- [ ] Filter replacement: verify tool-less cartridge removal and reinsertion
- [ ] Long-duration: run 20+ cook cycles, inspect duct for grease accumulation

### Prototype Validation Checklist

- [ ] Exhaust fan draws air upward from pot opening (smoke test with incense)
- [ ] Camera lens remains clear during 30-min simmer cook
- [ ] Camera lens remains clear during 5-min tadka (high smoke)
- [ ] Filter cartridge slides in/out smoothly
- [ ] No fume leakage around filter gasket
- [ ] Fan stall detection triggers interlock within 2 seconds
- [ ] Noise acceptable in quiet kitchen environment

---

## Related Documentation

- [[09-Induction-Heating|Induction Heating]] - Heat source and PID control (fan speed tracks cooking stage)
- [[12-Vision-System|Vision System]] - Camera anti-fog measures and steam protection
- [[../02-Hardware/07-Mechanical-Design|Mechanical Design]] - Enclosure airflow, pot lid design, vent placement
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]] - Power budget and communication interfaces
- [[../02-Hardware/Epicura-Architecture|Epicura Architecture]] - STM32 GPIO allocation for exhaust fan PWM
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]] - IEC 60335 ventilation requirements
- [[../08-Components/02-Actuation-Components|Actuation Components]] - Exhaust fan BOM entry

---

#epicura #exhaust #fume-management #filtration #subsystem

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
