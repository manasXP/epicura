---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Epicura - Autonomous Kitchen Robot - Documentation Index

Welcome to the comprehensive documentation for the Epicura autonomous kitchen robot project. This documentation provides detailed specifications, design considerations, and implementation guidance for all subsystems of an AI-powered countertop cooking robot designed for Indian kitchens.

## Quick Navigation

### Core Documentation

#### 01. Overview
1. **[[01-Overview/01-Project-Overview|Project Overview]]** - Executive summary, key features, and target use cases

#### 02. Hardware
2. **[[02-Hardware/02-Technical-Specifications|Technical Specifications]]** - Induction, robotic arm, sensors, and performance requirements
3. **[[02-Hardware/Epicura-Architecture|Epicura Architecture]]** - System block diagrams and hardware wiring
4. **[[02-Hardware/05-Sensors-Acquisition|Sensors & Acquisition]]** - Camera, IR thermometer, load cells, and NTC probes
5. **[[02-Hardware/07-Mechanical-Design|Mechanical Design]]** - Enclosure, arm mechanism, and industrial design

#### 03. Software
6. **[[03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]]** - Dual-processor software modules, recipe state machine, and control flow
7. **[[03-Software/03-Main-Loop-State-Machine|Main Loop State Machine]]** - Cooking state diagram, state-layer impact matrix, sequence diagrams, and transition triggers
8. **[[03-Software/08-Tech-Stack|Tech Stack]]** - Hardware platforms, software frameworks, and development tools
9. **[[03-Software/04-MPU-Functional-Specification|MPU Functional Specification]]** - CM5 (Cortex-A76) functional requirements, interfaces, and software architecture
10. **[[03-Software/05-MCU-Functional-Specification|MCU Functional Specification]]** - STM32G474RE functional requirements, pin assignments, and FreeRTOS tasks

#### 04. User Interface
8. **[[04-UserInterface/03-UI-UX-Design|UI/UX Design]]** - Touchscreen interface, companion app, and multi-language support

#### 05. Subsystems
9. **[[05-Subsystems/09-Induction-Heating|Induction Heating]]** - 1,800W microwave induction surface (CAN bus), PID temperature control, and power management
10. **[[05-Subsystems/10-Robotic-Arm|Robotic Arm]]** - Single-axis servo arm, stirring patterns, and STM32 motor control
11. **[[05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing]]** - Three-subsystem dispensing: ASD (seasonings), CID (coarse), SLD (liquids)
12. **[[05-Subsystems/12-Vision-System|Vision System]]** - HD camera, edge AI inference, and cooking stage detection
13. **[[05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]]** - Exhaust fan, grease/carbon filtration, and fume extraction

#### 06. Compliance
13. **[[06-Compliance/06-Safety-Compliance|Safety & Compliance]]** - Electrical safety, food contact regulations, and BIS standards

#### 07. Development
14. **[[07-Development/01-Prototype-Development-Plan|Prototype Development Plan]]** - Phased plan from prototype to production (20-24 weeks)

#### 08. Project Management
15. **[[13-ProjectManagement/epics/__init|Epics]]** - 12 subsystem-based epics (~58 stories, ~365 points) covering PCB, embedded, thermal, actuation, vision, recipe, UI, backend, iOS, Android, admin, and integration
16. **[[13-ProjectManagement/sprints/__init|Sprint Calendar]]** - 6-week pre-sprint PCB phase + 12 two-week sprints (30 weeks total)

#### 09. Components (BOM)
18. **[[08-Components/01-Compute-Module-Components|Compute Module Components]]** - Raspberry Pi CM5, STM32, carrier boards
19. **[[08-Components/02-Actuation-Components|Actuation Components]]** - Servo motors, induction driver, solenoids
20. **[[08-Components/03-Sensor-Components|Sensor Components]]** - Camera, IR thermometer, NTC probes, load cells
21. **[[08-Components/04-Total-Component-Cost|Total Component Cost]]** - Full BOM and cost analysis ($614 prototype)

#### 10. PCB Design
22. **[[09-PCB/01-Controller-PCB-Design|Controller PCB Design]]** - STM32G474RE controller board (160x90mm)
23. **[[09-PCB/02-Driver-PCB-Design|Driver PCB Design]]** - Power electronics and actuator driver board (160x90mm)

#### 11. Backend
24. **[[10-Backend/01-Backend-Architecture|Backend Architecture]]** - Cloud backend (Fastify, PostgreSQL, Redis, MQTT bridge)
25. **[[10-Backend/02-Database-Schema|Database Schema]]** - PostgreSQL tables, indexes, sync strategy
26. **[[10-Backend/03-Admin-Portal|Admin Portal]]** - Next.js admin dashboard for recipe and appliance management

#### 12. API
27. **[[11-API/01-REST-API-Reference|REST API Reference]]** - Complete endpoint documentation with examples
28. **[[11-API/02-WebSocket-Events|WebSocket Events]]** - Real-time cooking event protocol
29. **[[11-API/03-MQTT-Topics|MQTT Topics]]** - Device telemetry topic hierarchy
30. **[[11-API/04-BLE-Services|BLE Services]]** - BLE GATT services for pairing and WiFi provisioning

#### 13. Mobile Apps
31. **[[12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]** - MVVM architecture, networking, design system
32. **[[12-MobileApps/02-iOS-App|iOS App]]** - Swift/SwiftUI implementation (Core Bluetooth, APNs)
33. **[[12-MobileApps/03-Android-App|Android App]]** - Kotlin/Compose implementation (CompanionDeviceManager, FCM)

#### 14. Testing
34. **[[14-Testing/01-Firmware-Test-Strategy|Firmware Test Strategy]]** - Unity/CMock unit tests, HIL tests, MISRA static analysis, safety tests
35. **[[14-Testing/02-CM5-Test-Strategy|CM5 Test Strategy]]** - pytest per Docker service, Docker Compose integration, CV model validation
36. **[[14-Testing/03-API-Test-Strategy|API & Admin Test Strategy]]** - Vitest monorepo tests, Testcontainers integration, API contract tests
37. **[[14-Testing/04-iOS-Test-Strategy|iOS Test Strategy]]** - XCTest/XCUITest, performance benchmarks, security tests
38. **[[14-Testing/05-Android-Test-Strategy|Android Test Strategy]]** - JUnit 5/Compose UI tests, Macrobenchmark, security tests

## Documentation Structure

```
docs/
├── README.md                                    (this file)
├── 01-Overview/
│   └── 01-Project-Overview.md                   Core project description
├── 02-Hardware/
│   ├── 01-Epicura-Architecture.md               System architecture & wiring
│   ├── 02-Technical-Specifications.md           Hardware specifications
│   ├── 03-Sensors-Acquisition.md                Sensor system design
│   └── 04-Mechanical-Design.md                  Physical/industrial design
├── 03-Software/
│   ├── 01-Tech-Stack.md                         Technology choices
│   ├── 02-Controller-Software-Architecture.md   Software architecture
│   ├── 03-Main-Loop-State-Machine.md            Cooking state machine & layer impacts
│   ├── 04-MPU-Functional-Specification.md       CM5 functional spec
│   └── 05-MCU-Functional-Specification.md       STM32 functional spec
├── 04-UserInterface/
│   └── 01-UI-UX-Design.md                       Touchscreen & app design
├── 05-Subsystems/
│   ├── 01-Induction-Heating.md                  Induction heater subsystem
│   ├── 02-Robotic-Arm.md                        Stirring arm subsystem
│   ├── 03-Ingredient-Dispensing.md              Dispensing subsystem
│   ├── 04-Vision-System.md                      Computer vision subsystem
│   └── 05-Exhaust-Fume-Management.md            Exhaust fan and filtration
├── 06-Compliance/
│   └── 01-Safety-Compliance.md                  Regulatory compliance
├── 07-Development/
│   └── 01-Prototype-Development-Plan.md         Development roadmap (20-24 weeks)
├── 08-Components/
│   ├── 01-Compute-Module-Components.md          Compute & control BOM
│   ├── 02-Actuation-Components.md               Motors & actuators BOM
│   ├── 03-Sensor-Components.md                  Sensors & cameras BOM
│   └── 04-Total-Component-Cost.md               Full cost analysis ($614)
├── 09-PCB/
│   ├── 01-Controller-PCB-Design.md              STM32G474RE controller board
│   └── 02-Driver-PCB-Design.md                  Power electronics & actuator drivers
├── 10-Backend/
│   ├── 01-Backend-Architecture.md               Cloud backend architecture
│   ├── 02-Database-Schema.md                    PostgreSQL schema & sync
│   └── 03-Admin-Portal.md                       Next.js admin dashboard
├── 11-API/
│   ├── 01-REST-API-Reference.md                 REST endpoints & examples
│   ├── 02-WebSocket-Events.md                   Real-time event protocol
│   ├── 03-MQTT-Topics.md                        Device telemetry topics
│   └── 04-BLE-Services.md                       BLE pairing & WiFi setup
├── 12-MobileApps/
│   ├── 01-Mobile-Architecture.md                MVVM, networking, design
│   ├── 02-iOS-App.md                            Swift/SwiftUI implementation
│   └── 03-Android-App.md                        Kotlin/Compose implementation
├── 14-Testing/
│   ├── 01-Firmware-Test-Strategy.md           STM32 firmware testing
│   ├── 02-CM5-Test-Strategy.md                CM5 Docker services testing
│   ├── 03-API-Test-Strategy.md                API & admin portal testing
│   ├── 04-iOS-Test-Strategy.md                iOS app testing
│   └── 05-Android-Test-Strategy.md            Android app testing
└── 13-ProjectManagement/
    ├── __init.md                                PM overview
    ├── epics/
    │   ├── __init.md                            Epic index (12 epics, ~365 points)
    │   ├── PCB-pcb-design.md                    PCB Design & Fabrication
    │   ├── EMB-embedded.md                      Embedded Platform (STM32 + CM5)
    │   ├── THR-thermal.md                       Thermal & Induction Control
    │   ├── ARM-actuation.md                     Robotic Arm & Dispensing
    │   ├── CV-vision.md                         Computer Vision
    │   ├── RCP-recipe.md                        Recipe Engine
    │   ├── UI-touchscreen.md                    Touchscreen UI (Kivy)
    │   ├── BE-backend.md                        Cloud Backend (Fastify)
    │   ├── IOS-ios.md                           iOS App (SwiftUI)
    │   ├── AND-android.md                       Android App (Kotlin/Compose)
    │   ├── ADM-admin.md                         Admin Portal (Next.js)
    │   └── INT-integration.md                   Integration & Validation
    └── sprints/
        ├── __init.md                            Sprint calendar (12 sprints)
        ├── sprint-01.md                         STM32 FreeRTOS, CM5 Yocto, SPI
        ├── sprint-02.md                         Docker, safety, OTA
        ├── sprint-03.md                         CAN bus, PID start
        ├── sprint-04.md                         PID, thermal safety, servo arm
        ├── sprint-05.md                         P-ASD, CID, backend start
        ├── sprint-06.md                         SLD, calibration, camera
        ├── sprint-07.md                         ML model, stage detection
        ├── sprint-08.md                         Recipe engine, mobile apps
        ├── sprint-09.md                         State machine, Kivy UI
        ├── sprint-10.md                         Cooking UI, admin portal
        ├── sprint-11.md                         Integration & safety testing
        └── sprint-12.md                         Reliability, launch readiness
```

## Getting Started

### For Project Managers
Start with:
1. [[01-Overview/01-Project-Overview|Project Overview]] - Understand the project scope and target market
2. [[13-ProjectManagement/epics/__init|Epics]] - 12 subsystem-based epics (~58 stories, ~365 points)
3. [[13-ProjectManagement/sprints/__init|Sprint Calendar]] - 6-week pre-sprint PCB phase + 12 two-week sprints
5. [[07-Development/01-Prototype-Development-Plan|Prototype Development Plan]] - Phased development roadmap (20-24 weeks)
6. [[03-Software/01-Tech-Stack|Tech Stack]] - Review technology choices
7. [[06-Compliance/01-Safety-Compliance|Safety & Compliance]] - Understand electrical and food safety requirements

### For Hardware Engineers
Start with:
1. [[02-Hardware/02-Technical-Specifications|Technical Specifications]] - System requirements and power budget
2. [[02-Hardware/01-Epicura-Architecture|Epicura Architecture]] - Block diagrams and wiring
3. [[02-Hardware/03-Sensors-Acquisition|Sensors & Acquisition]] - Camera, thermal, and load cell design
4. [[02-Hardware/04-Mechanical-Design|Mechanical Design]] - Enclosure, arm mechanism, and thermal management

### For Software Engineers
Start with:
1. [[03-Software/02-Controller-Software-Architecture|Controller & Software Architecture]] - Dual-processor design and recipe state machine
2. [[03-Software/01-Tech-Stack|Tech Stack]] - Development environment and tools
3. [[04-UserInterface/01-UI-UX-Design|UI/UX Design]] - Touchscreen and companion app interface requirements

### For Backend Engineers
Start with:
1. [[10-Backend/01-Backend-Architecture|Backend Architecture]] - Fastify, PostgreSQL, Redis, MQTT bridge
2. [[10-Backend/02-Database-Schema|Database Schema]] - Tables, indexes, CM5 sync strategy
3. [[11-API/01-REST-API-Reference|REST API Reference]] - Endpoint specifications with examples
4. [[11-API/03-MQTT-Topics|MQTT Topics]] - Device telemetry protocol

### For Mobile Developers
Start with:
1. [[12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] - MVVM architecture, networking, BLE
2. [[12-MobileApps/02-iOS-App|iOS App]] or [[12-MobileApps/03-Android-App|Android App]] - Platform-specific guide
3. [[11-API/04-BLE-Services|BLE Services]] - Device pairing and WiFi provisioning
4. [[11-API/01-REST-API-Reference|REST API Reference]] - Backend API endpoints

### For Industrial Designers
Start with:
1. [[02-Hardware/04-Mechanical-Design|Mechanical Design]] - Enclosure form factor and material selection
2. [[04-UserInterface/01-UI-UX-Design|UI/UX Design]] - Physical controls, display layout, and user flow
3. [[01-Overview/01-Project-Overview|Project Overview]] - Product vision and target user profile

## Key Features Summary

- **Autonomous Cooking** - Hands-off operation after ingredient loading; state machine recipe execution
- **AI Vision Monitoring** - Overhead HD camera with TFLite edge AI for food color/texture analysis and cooking stage detection
- **Induction PID Control** - 1,800W microwave induction surface (CAN-controlled) with closed-loop PID, sear at 250°C, simmer at 60°C, ±5°C accuracy
- **Robotic Stirring Arm** - Single-axis servo arm (STM32-driven) with multiple stir patterns and auto-scraping
- **Three-Subsystem Dispensing** - ASD (3 servo-gated seasoning hoppers), CID (2 linear actuator coarse trays), SLD (2 peristaltic pump liquid channels with dedicated per-reservoir load cells + low-level alerts)
- **Touchscreen + Companion Apps** - 10" Kivy touchscreen on device, native mobile apps (iOS + Android) for remote control and live camera feed
- **100+ Indian Recipes** - Curated recipe database covering curries, dal, rice, biryani, and more with regional variations
- **Cloud + Offline Operation** - Cloud-updatable recipe library with full local SQLite fallback for offline cooking
- **Under 2kW Power Draw** - Designed for standard Indian household 15A outlets with dynamic power management

## Development Phases

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Prototype** | 3-6 months | Hardware prototype, basic recipe execution, vision proof-of-concept |
| **Alpha** | 3-6 months | Core features, 20+ recipes, app integration, safety testing |
| **Beta** | 3-6 months | 100+ recipes, field testing, regulatory pre-compliance |
| **Production** | 3-6 months | Manufacturing, final certifications, market launch |
| **Total** | 12-24 months | Market-ready product |

## Subsystem Overview

### Hardware Subsystems
- **Compute Platform** - Raspberry Pi CM5 (AI/vision/UI) + STM32 (motor/arm control)
- **Induction Heater** - 1,800W induction cooktop with NTC + IR temperature feedback
- **Display** - 10" 1280x800 capacitive touchscreen (Kivy interface)
- **Robotic Arm** - Single-axis servo arm for stirring and ingredient dispensing
- **Vision System** - Overhead HD camera + IR thermometer + load cells
- **Ingredient Dispensing** - ASD (seasoning servos) + CID (linear actuator sliders) + SLD (peristaltic pumps + solenoids)

### Software Subsystems
- **CM5 (Yocto Linux)** - Recipe engine, computer vision pipeline, Kivy UI, cloud sync, SQLite data management
- **STM32 (FreeRTOS)** - PID temperature control, servo motor driver, sensor polling, safety watchdog

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Epicura System Overview                          │
│                                                                     │
│  ┌──────────────────────┐        ┌──────────────────────┐           │
│  │  Raspberry Pi CM5    │        │  STM32 MCU           │           │
│  │  (Yocto Linux)       │◄──────►│  (FreeRTOS)          │           │
│  │  - Recipe Engine     │  UART  │  - PID Control       │           │
│  │  - CV Pipeline       │  /SPI  │  - Servo Driver      │           │
│  │  - Kivy UI            │        │  - Sensor Polling    │           │
│  │  - Cloud Sync        │        │  - Safety Watchdog   │           │
│  └──────────┬───────────┘        └──────────┬───────────┘           │
│             │                               │                       │
│  ┌──────────▼───────────┐        ┌──────────▼───────────┐           │
│  │  10" Touchscreen     │        │  Induction Heater    │           │
│  │  HD Camera           │        │  Servo Arm           │           │
│  │  WiFi/BT             │        │  Load Cells          │           │
│  │                      │        │  NTC + IR Sensors    │           │
│  └──────────────────────┘        └──────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

## Tags

#epicura #kitchen-robot #documentation #index

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |