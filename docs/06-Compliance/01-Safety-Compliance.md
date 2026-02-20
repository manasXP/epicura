---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Safety & Compliance

## Product Classification

### Regulatory Classification
- **Class:** Consumer household cooking appliance with embedded electronics and robotic elements
- **Category:** NOT a medical device
- **Type:** Countertop cooking robot with induction heating, robotic stirring arm, and AI vision
- **Application:** Autonomous one-pot meal preparation for domestic kitchens
- **Target Market:** Indian households (primary), global (secondary)

### Key Characteristics
- Mains-powered appliance (230V AC, under 2kW)
- Contains robotic moving parts (servo arm)
- Contains induction heating element (1,800W)
- Contains embedded compute (RPi CM5 + STM32G4)
- WiFi-connected with cloud update capability
- Food-contact surfaces (pot, paddle, ASD hoppers, CID trays, SLD tubing/reservoirs)

---

## Applicable Standards

| Standard | Title | Relevance |
|----------|-------|-----------|
| IEC 60335-1 | Household appliances - General safety | Core safety standard for all household appliances |
| IEC 60335-2-6 | Cooking appliances (ranges, hobs, ovens) | Induction-specific heating requirements |
| IEC 60335-2-9 | Grills, toasters, and similar portable cooking appliances | Robotic cooking appliance category |
| IEC 62368-1 | ICT/AV equipment safety | CM5/STM32 embedded electronics |
| ISO 13482 | Robots and robotic devices - Personal care robots | Robotic arm safety principles |
| EN 50564 | Standby power measurement | Target: <0.5W standby power |
| CISPR 14-1 | EMC - Emissions for household appliances | Induction heater EMI emissions |
| CISPR 14-2 | EMC - Immunity for household appliances | Operation near other appliances |
| IEC 61000-3-2 | Harmonic current emissions | Power quality for 1,800W load |
| IEC 61000-3-3 | Voltage fluctuations and flicker | Induction power cycling effects |

---

## Electrical Safety

### Leakage Current Limits
- **Normal condition:** Patient leakage current < 0.75 mA (IEC 60335-1 Class I limit)
- **Single fault condition:** < 3.5 mA
- **Appliance class:** Class I (protective earth connection)

### Touch Temperature Limits
- **External surfaces (general):** < 60°C during operation
- **Handles and controls:** < 50°C during operation
- **Exhaust air openings:** < 70°C during operation
- **Top surface near pot:** Labelled hot zone, < 85°C (insulated from enclosure)

### Ground Fault Protection
- **Class I appliance** with protective earth conductor
- Recommended: use with RCD/GFCI (30mA) at household outlet
- Earth continuity resistance: < 0.1 ohm

### Induction EMF Safety
- Electromagnetic field within **ICNIRP 2010 reference levels** at 30 cm distance
- Operating frequency: 20-100 kHz (typical induction range)
- Shielding: ferrite sheet under induction coil, aluminum enclosure base

### Insulation Design
- **Double/reinforced insulation** between mains (230V AC) and low-voltage circuits (5V/3.3V)
- Creepage distance: >= 6 mm (mains to SELV)
- Clearance distance: >= 4 mm (mains to SELV)
- Isolation voltage: 3 kV AC for 1 minute (type test)

### Overcurrent Protection
- **Primary fuse:** T10A 250V on mains input (slow-blow for induction inrush)
- **Electronic current limit:** Internal to microwave induction surface module
- **Thermal fuse:** Internal to microwave induction surface module
- **CAN coil temperature monitoring:** Induction module reports coil temp via CAN with auto-shutoff on over-temp

---

## Food Contact Safety

### Regulatory Framework
- **USA:** FDA 21 CFR 174-186 (food contact materials)
- **EU:** Regulation (EC) 1935/2004 (materials in contact with food)
- **India:** FSSAI packaging regulations

### Material Requirements
- **BPA-free plastics** for all food-contact parts (ASD hoppers, CID trays, SLD reservoirs)
- **Food-grade silicone** for paddle/stirrer (FDA-compliant, heat-resistant to 250°C)
- **Stainless steel 304/316** for pot (induction-compatible, corrosion-resistant)
- **Non-stick coating:** PFOA-free ceramic or PTFE on pot interior

### Migration Testing
- **Pot coating:** Migration testing per EU 10/2011 (plastic) or specific coating standards
- **Dispensing materials (ASD/CID/SLD):** Overall migration limit < 10 mg/dm2
- **Paddle/stirrer:** Specific migration tests for silicone (organotin compounds)

### Hygiene Design Principles
- **No trapped food zones:** All surfaces accessible for cleaning or removable
- **Smooth transitions:** Radius >= 3 mm at all food-contact junctions
- **Removable parts:** Pot, paddle, ASD hoppers, CID trays, SLD reservoirs/tubing, drip tray - all removable
- **Dishwasher safe:** Removable food-contact parts rated to 65°C wash cycle
- **Maximum hold time:** Cooked food alert after 2 hours at ambient temperature

---

## Mechanical Safety

### Robotic Arm Safety (ISO 13482 Principles)
- **Collaborative robot approach:** Low force, limited speed, soft materials
- **Maximum arm torque:** Limited to 2 N.m via servo current limit
- **Maximum arm speed:** 60 RPM (stirring), 30 RPM (dispensing)
- **Finger guard:** Physical barrier around stirring zone when lid open
- **Force limiting:** Servo stalls at obstruction rather than forcing through

### Pot Interlock System
```
┌─────────────────────────────────────────┐
│            Interlock Logic              │
│                                         │
│  Reed Switch ──► STM32 ──► AND Gate     │
│  (pot detect)            ▼              │
│                    ┌──────────┐         │
│  Lid Switch ──────►│ Arm      │         │
│  (lid closed)      │ Enable   │         │
│                    └──────────┘         │
│                         │               │
│                         ▼               │
│                 Servo Power Relay        │
└─────────────────────────────────────────┘
```
- Arm will NOT operate without pot in place (reed switch)
- Arm will NOT operate with lid removed during cooking (lid switch)
- Induction will NOT activate without pot detected (inherent to induction + reed switch)

### Stability Requirements
- **Tip-over test:** Device must not tip when tilted to 15° on any axis
- **Non-slip feet:** Silicone pads, minimum 4 contact points
- **Weight distribution:** Center of gravity below 60% of device height
- **Vibration:** Arm operation must not cause walking on smooth surfaces

### Sharp Edges
- No sharp edges on any user-accessible surface (per IEC 60335-1 Clause 20)
- Internal edges guarded by enclosure panels
- Paddle edges rounded (radius >= 1 mm)

---

## Software Safety

### WiFi & Network Security
- **WiFi:** WPA3 encryption for all wireless connections
- **MQTT:** TLS 1.3 encrypted connection to cloud broker
- **OTA Updates:** Signed firmware images (RSA-2048 or Ed25519)
- **API:** HTTPS-only REST API for mobile app communication
- **AP Mode:** Isolated network for initial pairing (no internet forwarding)

### Safety-Critical Code (STM32)
- **MISRA C:2012** subset compliance for all safety-critical functions
- Safety-critical functions include:
  - Induction power control and thermal monitoring
  - Servo arm torque limiting and interlock logic
  - Emergency stop handler
  - Watchdog timer management
- **Code review:** All safety-critical code requires peer review

### Fail-Safe Defaults
```
┌─────────────────────────────────────────┐
│          Fail-Safe State Machine        │
│                                         │
│  Power Loss ──────────► All OFF         │
│  Watchdog Timeout ────► All OFF         │
│  CM5 Crash ───────────► STM32 Safe Mode │
│  STM32 Crash ─────────► HW Thermal Fuse│
│  Overtemp (>200°C) ──► Induction OFF    │
│  Pot Removed ─────────► Induction OFF   │
│  Lid Opened ──────────► Arm STOP        │
│  Communication Loss ──► Hold State 30s  │
│                         then Safe Stop  │
└─────────────────────────────────────────┘
```

### Data Privacy
- **Local storage:** All cooking data stored on device (microSD)
- **Cloud sync:** Opt-in only, user must explicitly enable
- **No PII collection:** No personal identification data collected
- **Recipe data:** Anonymized usage statistics only (if cloud enabled)
- **Deletion:** User can factory-reset all data from settings menu

---

## EMC Compliance

### Emissions (CISPR 14-1)
- **Conducted emissions:** 150 kHz - 30 MHz, limits per CISPR 14-1 Group 2
- **Radiated emissions:** 30 MHz - 1 GHz, limits per CISPR 14-1 Group 2
- **Primary EMI source:** Induction heater (20-100 kHz switching)
- **Secondary sources:** CM5 (1.5 GHz CPU), STM32 (170 MHz CPU), WiFi (2.4 GHz)

### Immunity (CISPR 14-2)
- **ESD:** ±4 kV contact, ±8 kV air
- **RF immunity:** 80 MHz - 2.7 GHz, 3 V/m
- **Electrical fast transient:** ±1 kV on mains
- **Surge:** ±1 kV differential, ±2 kV common mode
- Must operate correctly near microwave ovens, other induction hobs, and WiFi routers

### Induction-Specific EMI Mitigation
- **Ferrite sheet:** Under induction coil to direct flux into pot
- **EMI shielding:** Aluminum base plate under coil assembly
- **Ferrite beads:** On all signal lines crossing power/digital boundary
- **Input filter:** Common-mode choke + X2/Y2 capacitors on mains input
- **Spread spectrum:** Frequency dithering on induction driver to reduce peak emissions

---

## Environmental Compliance

### RoHS (Restriction of Hazardous Substances)
- Compliant with EU Directive 2011/65/EU (RoHS 2)
- **Lead-free solder** on all PCBs (SAC305 or equivalent)
- All components RoHS-compliant (verified via supplier declarations)
- Exemptions: None required for this product category

### REACH (Registration, Evaluation, Authorization of Chemicals)
- No SVHC (Substances of Very High Concern) in product
- Material declarations maintained for all suppliers
- Annual SVHC list review for new additions

### WEEE (Waste Electrical and Electronic Equipment)
- **Recyclable design:** Enclosure separable from electronics without special tools
- **Battery (if any):** Removable, clearly marked for separate disposal
- **Marking:** WEEE crossed-out wheelie bin symbol on product label
- **Packaging:** Recyclable cardboard, minimal plastic (paper-based cushioning)

---

## Risk Management

### Hazard Analysis

| Hazard | Severity | Likelihood | Risk Level | Mitigation |
|--------|----------|------------|------------|------------|
| Burns (hot surfaces) | High | Medium | **High** | Thermal insulation, warning labels, touch temp limits (<60°C external), cool-down alert |
| Electric shock | High | Low | **Medium** | Class I grounding, double insulation on mains, RCD recommendation in manual |
| Food contamination | Medium | Medium | **Medium** | Food-safe materials, cleanable design, max 2-hour hold time alert, cleaning reminders |
| Arm injury (pinch/cut) | Medium | Low | **Low** | Finger guard, servo torque limiting (2 N.m), pot interlock, lid interlock |
| Boil-over (spill) | Medium | Medium | **Medium** | CV detection of bubbling, auto power reduction, drip tray, max fill line on pot |
| Fire (overheating) | High | Low | **Medium** | Thermal fuse (240°C), CAN coil temp monitoring, max temp limit (200°C), auto shutoff timer |
| Allergen cross-contact | Medium | Medium | **Medium** | Dedicated subsystems (ASD/CID/SLD), cleaning alerts between recipes, user allergen warnings in UI |
| Water ingress | Medium | Low | **Low** | IPX1 rating (drip-proof), sealed electronics compartment, drain channels |
| Tip-over (hot liquid spill) | High | Low | **Medium** | Non-slip feet, low center of gravity, 15° tilt test, max 3L fill volume |

### Risk Assessment Matrix

```
┌────────────────────────────────────────────────┐
│           RISK ASSESSMENT MATRIX               │
│                                                │
│  Severity ►   Low      Medium     High         │
│  Likelihood                                    │
│      ▼                                         │
│  High         Medium   HIGH       CRITICAL     │
│  Medium       Low      MEDIUM     HIGH         │
│  Low          Low      LOW        MEDIUM       │
│                                                │
│  Legend: LOW = Accept  MEDIUM = Mitigate        │
│          HIGH = Redesign  CRITICAL = Eliminate  │
└────────────────────────────────────────────────┘
```

---

## Regulatory Submission

| Market | Standard / Body | Timeline Estimate | Notes |
|--------|----------------|-------------------|-------|
| India | BIS (IS 302 / IS 60335) | 6-12 months | Mandatory for domestic sale; BIS certification required |
| EU | CE Mark (IEC 60335 + EMC Directive) | 6-9 months | Self-declaration with notified body for EMC + safety testing |
| USA | UL/ETL (UL 858 - Cooking Appliances) | 9-12 months | Third-party lab testing (UL, Intertek, or CSA) |
| UK | UKCA Mark | 6-9 months | Post-Brexit; similar to CE but separate submission |
| GCC | G-Mark (GSO) | 3-6 months | Gulf Cooperation Council; based on IEC standards |
| ASEAN | Country-specific | Varies | Singapore (PSB), Thailand (TISI), Malaysia (SIRIM) |

### Submission Priority
1. **India (BIS)** - Primary market, begin during prototype testing
2. **CE Mark (EU)** - Largest secondary market, parallel with BIS
3. **UL/ETL (USA)** - If US market expansion planned
4. **Others** - Post-launch, market-driven

---

## Labeling Requirements

### Product Label
- Manufacturer name and address
- Model number and serial number
- Electrical ratings: 230V AC, 50Hz, 1800W
- Appliance Class I symbol
- CE/BIS/UL mark (as applicable)
- Date of manufacture
- Country of origin

### Safety Symbols
- Hot surface warning (near pot area)
- "Read instructions before use" symbol
- Earth terminal symbol
- WEEE disposal symbol
- Food-contact material symbol

---

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../03-Software/03-Software-Architecture|Software Architecture]]
- [[../07-Development/Prototype-Development-Plan|Prototype Development Plan]]

---

#epicura #safety #compliance #regulations

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
