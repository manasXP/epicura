---
created: 2026-02-14
modified: 2026-02-15
version: 1.0
status: Draft
tags: [epicura, project-overview, kitchen-robot]
---

# Epicura - Project Overview

## Project Description

Development of an autonomous countertop kitchen robot that cooks complete one-pot meals using AI-powered computer vision, robotic stirring, and precise induction heat control. Epicura is designed for the Indian home market, inspired by the commercial Posha robot chef, and engineered to operate within compact Indian kitchens on standard household outlets (under 2kW). The system combines embedded Linux compute, real-time motor control, and edge AI inference to deliver fully autonomous cooking from ingredient loading to finished meal.

## Key Components

This project encompasses the following major subsystems:

- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]] - Induction, robotic arm, sensors, and power budget
- [[../02-Hardware/Epicura-Architecture|Epicura Architecture]] - System block diagrams and hardware wiring
- [[../02-Hardware/05-Sensors-Acquisition|Sensors & Acquisition]] - Camera, IR thermometer, load cells, and NTC probes
- [[../02-Hardware/07-Mechanical-Design|Mechanical Design]] - Enclosure, arm mechanism, and industrial design
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]] - Dual-processor software modules and recipe state machine
- [[../03-Software/08-Tech-Stack|Tech Stack]] - Hardware platforms, software frameworks, and tools
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]] - Touchscreen interface and companion mobile app
- [[../05-Subsystems/09-Induction-Heating|Induction Heating]] - 1,800W microwave induction surface with CAN bus control and PID
- [[../05-Subsystems/10-Robotic-Arm|Robotic Arm]] - Single-axis servo arm and stir patterns
- [[../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing]] - Three-subsystem dispensing (ASD/CID/SLD)
- [[../05-Subsystems/12-Vision-System|Vision System]] - HD camera, edge AI, and cooking stage detection
- [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]] - Exhaust fan, grease/carbon filtration
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]] - Electrical safety and food contact regulations

## Core Features

### Autonomous Cooking
- Fully hands-off operation after ingredient loading and recipe selection
- State machine recipe execution: detect cooking stage via CV, adjust heat/stir, dispense ingredients
- Automatic ingredient dispensing via three subsystems: ASD (seasonings, servo-gated), CID (coarse items, linear actuator), SLD (liquids, peristaltic pump)
- Supports one-pot recipes: curries, dal, rice, biryani, stir-fries, pasta, soups

### Recipe Intelligence
- 100+ curated Indian recipes at launch with regional variations (North, South, East, West)
- App-driven customization for spice levels, allergen substitutions, and dietary preferences
- Cloud-updatable recipe library with new recipes pushed via OTA
- Full offline fallback with local SQLite recipe database for uninterrupted cooking

### Precision Control
- PID-controlled induction heating with dynamic temperature range (60-250°C)
- Dual temperature sensing: NTC contact probe + IR non-contact thermometer
- Sear at 200-250°C, simmer at 60-100°C with ±5°C accuracy
- Dynamic power management to stay within 2kW household limit

### Vision System
- Overhead HD camera (1080p minimum) mounted inside enclosure lid
- Food color and texture analysis using TFLite edge AI models on Raspberry Pi CM5
- Real-time cooking stage detection: raw, browning, simmering, thickening, done
- Anomaly detection for burning, boiling over, or ingredient issues

### User Experience
- 10" capacitive touchscreen with Qt-based interface for recipe browsing and cooking status
- Native companion mobile apps (SwiftUI + Jetpack Compose) for remote recipe selection, live camera feed, and notifications
- Multi-language support: English, Hindi, Tamil, Telugu (extensible to more regional languages)
- Live camera feed on both touchscreen and mobile app during cooking
- Grocery list generation and meal planning features in companion app

## Target Use Cases

- **Daily Indian Cooking** - Curries, dal tadka, rajma, sambar, biryani, pulao, and everyday meals
- **Apartment/Compact Kitchens** - Countertop form factor (50x40x30cm) designed for space-constrained urban homes
- **Elderly/Mobility-Impaired Users** - Autonomous operation reduces physical effort; accessible UI with large touch targets
- **Hostel/Mess Kitchen Automation** - Scalable for small institutional kitchens with repeatable batch cooking
- **Meal Prep (Set-and-Forget)** - Load ingredients before work, schedule cooking, return to a ready meal

## Key Features Comparison

| Feature | Posha (Commercial) | Epicura (Design Target) |
|---------|--------------------|-----------------------|
| **Autonomy** | Fully hands-off after prep | Identical, with CV fallback loops and anomaly alerts |
| **Customization** | Spice/allergen swaps via app | App-driven recipe DB with ingredient substitutions and dietary profiles |
| **Monitoring** | Live camera feed in app | App + local 10" touchscreen, anomaly alerts with push notifications |
| **Cleanup** | Dishwasher-safe pot | Removable non-stick pot, optional auto-rinse cycle |
| **Size/Power** | Countertop, ~1.8kW | 50x40x30cm, <2kW for standard Indian 15A outlets |
| **Recipes** | Curated library, cloud-updated | 100+ Indian recipes at launch, cloud-updatable, offline fallback |
| **Connectivity** | WiFi, app-paired | WiFi + BT, native companion apps (iOS + Android), OTA updates |
| **Price Target** | ~$800 USD (commercial) | $400-600 USD (target retail for Indian market) |

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Epicura System Architecture                            │
│                                                                              │
│  ┌──────────────────────────────────────┐  ┌─────────────────────────────┐  │
│  │     Raspberry Pi CM5 + Carrier       │  │     STM32 MCU               │  │
│  │     (Application Processor)          │  │     (Real-Time Controller)  │  │
│  │                                      │  │                             │  │
│  │  ┌──────────────────────────────┐    │  │  ┌─────────────────────┐    │  │
│  │  │  Yocto Linux                 │    │  │  │  FreeRTOS           │    │  │
│  │  └────────────┬─────────────────┘    │  │  └────────────┬────────┘    │  │
│  │               │                      │  │               │            │  │
│  │  ┌────────────▼─────────────────┐    │  │  ┌────────────▼────────┐   │  │
│  │  │  Recipe State Machine        │    │  │  │  PID Temperature    │   │  │
│  │  │  CV Pipeline (TFLite)        │◄───┼──┼─►│  Servo Motor Driver │   │  │
│  │  │  Qt Touchscreen UI           │UART│  │  │  Sensor Polling     │   │  │
│  │  │  Cloud Sync / OTA            │/SPI│  │  │  Safety Watchdog    │   │  │
│  │  │  SQLite Recipe DB            │    │  │  │  Dispensing Control │   │  │
│  │  └──────────────────────────────┘    │  │  └─────────────────────┘   │  │
│  │                                      │  │                             │  │
│  └──────────┬─────────────┬─────────────┘  └──────┬──────────┬──────────┘  │
│             │             │                       │          │              │
│     ┌───────▼──────┐ ┌───▼──────────┐    ┌───────▼────┐ ┌───▼──────────┐  │
│     │ 10" Touch    │ │ HD Camera    │    │ Induction  │ │ Servo Arm    │  │
│     │ Display      │ │ (1080p)      │    │ Heater     │ │ (Stirring)   │  │
│     │ (Qt UI)      │ │              │    │ (1,800W)   │ │              │  │
│     └──────────────┘ └──────────────┘    └────────────┘ └──────────────┘  │
│                                                                            │
│     ┌──────────────┐ ┌──────────────┐    ┌────────────┐ ┌──────────────┐  │
│     │ WiFi / BT    │ │ IR Thermo-   │    │ NTC Temp   │ │ Ingredient   │  │
│     │ Module       │ │ meter        │    │ Probe      │ │ Hoppers      │  │
│     │              │ │              │    │            │ │ (4-6 compt.) │  │
│     └──────────────┘ └──────────────┘    └────────────┘ └──────────────┘  │
│                                                                            │
│     ┌──────────────────────────────────────────────────────────────────┐   │
│     │                    Load Cells (Pot Weight Sensing)               │   │
│     └──────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Overview

```
┌──────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  User    │    │  Recipe      │    │  CV Pipeline  │    │  Actuators   │
│  Input   │───►│  State       │───►│  (TFLite)     │───►│  (Heat/Stir/ │
│  (App/   │    │  Machine     │    │               │    │   Dispense)  │
│   Touch) │    │  (CM5)       │    │  Stage?       │    │  (STM32)     │
└──────────┘    └──────┬───────┘    └───────┬───────┘    └──────┬───────┘
                       │                    │                    │
                       │            ┌───────▼───────┐           │
                       │            │  HD Camera    │           │
                       │            │  IR Thermo    │           │
                       │            │  NTC Probe    │           │
                       │            │  Load Cells   │           │
                       │            └───────────────┘           │
                       │                                        │
                       ▼                                        ▼
                ┌──────────────┐                    ┌──────────────┐
                │  UI Display  │                    │  Physical    │
                │  (Status,    │                    │  Output      │
                │   Camera,    │                    │  (Cooked     │
                │   Progress)  │                    │   Meal)      │
                └──────────────┘                    └──────────────┘
```

## Physical Specifications

| Parameter | Value |
|-----------|-------|
| Dimensions | 50 x 40 x 30 cm (W x D x H) |
| Weight | ~12-15 kg (estimated) |
| Power Input | 220-240V AC, 50 Hz (Indian standard) |
| Max Power Draw | < 2,000W (compatible with 15A household outlets) |
| Induction Heater | 1,800W peak, variable power |
| Display | 10" 1280x800 capacitive touchscreen |
| Camera | 1080p HD, overhead mounted |
| Connectivity | WiFi 802.11ac, Bluetooth 5.0 |
| Pot Capacity | 3-5 liters (removable, non-stick, dishwasher-safe) |
| Ingredient Dispensing | ASD (3 seasoning hoppers) + CID (2 coarse trays) + SLD (2 liquid channels) |
| Operating Temperature | 5°C - 45°C ambient |

## Project Status

Early concept and design phase. No source code or hardware prototypes exist yet. The project definition and subsystem documentation are being established. Estimated timeline from prototype to production-ready product is 12-24 months.

### Milestone Timeline

```
Phase 1: Prototype          Phase 2: Alpha              Phase 3: Beta               Phase 4: Production
(3-6 months)                (3-6 months)                (3-6 months)                (3-6 months)
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│ - Off-shelf parts │       │ - Custom PCB      │       │ - 100+ recipes    │       │ - Manufacturing   │
│ - Basic recipe    │──────►│ - 20+ recipes     │──────►│ - Field testing   │──────►│ - BIS/CE cert     │
│   execution       │       │ - App integration │       │ - Pre-compliance  │       │ - Market launch   │
│ - Vision PoC      │       │ - Safety testing  │       │ - User feedback   │       │ - Support setup   │
└───────────────────┘       └───────────────────┘       └───────────────────┘       └───────────────────┘
```

## Related Documentation

- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]] - Detailed hardware specs
- [[../02-Hardware/Epicura-Architecture|Epicura Architecture]] - System block diagrams and wiring
- [[../02-Hardware/05-Sensors-Acquisition|Sensors & Acquisition]] - Sensor system design
- [[../02-Hardware/07-Mechanical-Design|Mechanical Design]] - Physical design and enclosure
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]] - Software design
- [[../03-Software/08-Tech-Stack|Tech Stack]] - Technology choices
- [[../04-UserInterface/03-UI-UX-Design|UI/UX Design]] - User interface design
- [[../05-Subsystems/09-Induction-Heating|Induction Heating]] - Heater subsystem
- [[../05-Subsystems/10-Robotic-Arm|Robotic Arm]] - Stirring arm subsystem
- [[../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing]] - Dispensing subsystem
- [[../05-Subsystems/12-Vision-System|Vision System]] - Computer vision subsystem
- [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]] - Fume extraction subsystem
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]] - Regulatory compliance
- [[../07-Development/Prototype-Development-Plan|Prototype Development Plan]] - Development roadmap
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]] - Full BOM and cost analysis

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | Manas Pradhan | Initial document creation |
| 1.0 | 2026-02-15 | Manas Pradhan | Added revision history and metadata |