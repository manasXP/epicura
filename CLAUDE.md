# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

Epicura is an autonomous countertop kitchen robot that cooks one-pot meals using AI vision, robotic stirring, and precise induction heat control. It is modeled after the commercial Posha robot chef. Target environment: compact Indian kitchens, under 2kW power draw.

## Project Status

Design/documentation phase. Comprehensive documentation exists across 35+ documents in `docs/`. No source code exists yet.

## Hardware Architecture

### Dual-Processor System

| Component | Processor | Role |
|-----------|-----------|------|
| **CM5** | Raspberry Pi CM5 (BCM2712, Cortex-A76 quad-core) | AI/vision, recipe engine, Kivy UI, cloud sync |
| **STM32** | STM32G474 (Cortex-M4F, 170 MHz) | PID control, servo driver, sensor polling, safety watchdog |

### Shared Components (both models)

| Component | Part | Interface | Purpose |
|-----------|------|-----------|---------|
| Carrier Board | CM5IO (official Raspberry Pi IO board) | Board-to-board connectors | CM5 carrier with all breakouts |
| Camera | IMX219 (8MP) or IMX477 (12.3MP) | CSI-2 to CM5 | Food stage detection via CV |
| IR Thermometer | MLX90614 | I2C to STM32 | Non-contact food surface temp |
| Load Cells | 4x strain gauge + HX711 | SPI to STM32 | Weight-based dispensing verification |
| NTC Thermistors | 100K NTC | ADC to STM32 | Coil and ambient temp monitoring |
| Microwave Induction Surface | 1,800W commercial module | CAN bus to STM32 FDCAN1 | Cooking heat source (self-contained coil + driver) |
| BLDC Stirring Motor | 24V BLDC (30-50 kg·cm, integrated ESC) | PWM (10kHz) + EN + DIR from STM32 | Stirring and scraping |
| Display | 10" 1280x800 capacitive | DSI/HDMI to CM5 | Kivy touchscreen UI |
| P-ASD (Pneumatic Seasoning Dispenser) | 1× 12V diaphragm pump + 6× 12V NC solenoid valves + ADS1015 pressure sensor | PWM+GPIO+I2C from STM32 | Pneumatic puff-dosing, 6× sealed 60 mL cartridges |
| CID (Coarse Ingredient Dispenser) | 2× 12V DC linear actuators | GPIO+PWM from STM32 | Push-plate slider trays for vegetables, dal, meat |
| SLD (Standard Liquid Dispenser) | 2× peristaltic pumps + 2× solenoid valves + 2× 2 kg load cells (one per reservoir) | PWM+GPIO from STM32 | Closed-loop oil and water dispensing + individual level alerts |

### Interface Constraints

- CM5 ↔ STM32 communication: SPI (primary) or UART (fallback) via Python bridge service
- STM32 ↔ Microwave surface: CAN bus (FDCAN1, 500 kbps)
- Power budget: total <2kW on 220-240V AC Indian household outlets
- Camera CSI-2 ribbon cable: max 150mm for signal integrity

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Compute platform | CM5 (4GB RAM, 64GB eMMC) over Jetson Nano | Lower cost, sufficient for Docker + PostgreSQL + ML, better Linux support |
| Carrier board | CM5IO (official) | Off-the-shelf, all necessary breakouts, no custom PCB needed for prototype |
| Motor controller | STM32G4 over ESP32 | Hardware FPU for PID, MISRA C compliance, CAN peripheral |
| Database | PostgreSQL (Docker) over SQLite | Schema consistency with cloud, JSONB support, full-text search, production-grade |
| Containerization | Docker Compose | Modular services, easy updates, consistent dev/prod environments |
| Camera | IMX219 (prototype) | $25 vs $50, 8MP sufficient for food classification |
| Power supply | Mean Well LRS-75-24 (24V single output) | Single reliable PSU feeds both CM5IO+CM5 and controller; downstream buck/LDO for 5V/3.3V |
| Heating module | Commercial microwave surface with CAN bus | Eliminates custom IGBT driver; pre-certified safety; CAN control |
| UI framework | Kivy over Qt6/QML | Python-only development (no C++/QML), GPU acceleration, sufficient widgets; Qt6/QML is overkill (medical-grade UX) |
| Mobile apps | Native (SwiftUI + Kotlin/Compose) over Flutter | Direct BLE/camera APIs, platform-native UX, reliable background processing |
| Cloud backend | Fastify (Node.js/TypeScript) | High-performance API server, TypeScript type safety, modular service architecture |
| Admin portal | Next.js | React-based, SSR, recipe/device/user management |
| CM5-STM32 Comm | Python bridge service | Dedicated service for protocol handling, message queuing, health monitoring |

## Software Stack

### CM5 (Yocto Linux + Docker)

- **OS**: Yocto (Kirkstone/Scarthgap), custom BSP with Docker support
- **Container Orchestration**: Docker Compose for all services
- **Database**: PostgreSQL 16 (Docker container) - same schema as cloud for consistency
- **MQTT**: Mosquitto broker (Docker container) with cloud bridge
- **Recipe Engine**: Python service (Docker container) - YAML parsing, state machine
- **CV Pipeline**: Python service (Docker container) - OpenCV + TFLite MobileNetV2 INT8
- **UI**: Kivy (Python, Docker container) - touchscreen interface, camera widget
- **CM5-STM32 Bridge**: Python service (Docker container) - SPI/UART protocol handler
- **Cloud Sync**: Bidirectional PostgreSQL sync, recipe/image caching
- **OTA Updates**: swupdate with A/B partitions

### STM32 (FreeRTOS)

- **RTOS**: FreeRTOS with 4 tasks (PID 100Hz, servo 50Hz, sensor 10Hz, comms 20Hz)
- **Language**: C (MISRA subset for safety-critical paths)
- **PID**: Closed-loop temperature control, Kp=2.0/Ki=0.5/Kd=0.1 defaults
- **Safety**: Hardware watchdog, thermal cutoffs, e-stop relay, safety relay for module AC disconnect
- **CAN**: FDCAN1 interface to microwave induction surface (power control, status, faults)
- **HAL**: STM32 HAL drivers for ADC, PWM, UART, SPI, I2C

### Cloud Backend

- **API Server**: Fastify (Node.js / TypeScript) - REST API for mobile apps and admin portal
- **Database**: PostgreSQL (cloud) - recipes, users, devices, telemetry
- **MQTT Broker**: Mosquitto / AWS IoT - device telemetry and commands
- **Admin Portal**: Next.js - recipe management, device monitoring, user administration

### Mobile Apps (Native)

- **iOS**: SwiftUI, Core Bluetooth (BLE pairing/WiFi provisioning), AVFoundation (camera streaming)
- **Android**: Kotlin + Jetpack Compose, CompanionDeviceManager (BLE), CameraX (streaming)

## Documentation Structure

```
docs/
├── README.md                          Documentation index
├── 01-Overview/
│   └── 01-Project-Overview            Product definition and use cases
├── 02-Hardware/
│   ├── 01-Epicura-Architecture        System block diagrams and wiring
│   ├── 02-Technical-Specifications    Induction, sensors, power specs
│   ├── 03-Sensors-Acquisition         Camera, IR, load cells, NTC
│   └── 04-Mechanical-Design           Enclosure, arm, thermal management
├── 03-Software/
│   ├── 01-Tech-Stack                  Yocto, Kivy, FreeRTOS, native mobile
│   ├── 02-Controller-Software-Architecture    Recipe state machine, CV, PID
│   └── 03-Main-Loop-State-Machine     Cooking state machine across UI/CM5/STM32
├── 04-UserInterface/
│   └── 01-UI-UX-Design               Touchscreen wireframes, companion app
├── 05-Subsystems/
│   ├── 01-Induction-Heating           PID control, safety interlocks
│   ├── 02-Robotic-Arm                 Servo patterns, stall detection
│   ├── 03-Ingredient-Dispensing       ASD/CID/SLD dispensing subsystems
│   ├── 04-Vision-System              TFLite pipeline, anomaly detection
│   └── 05-Exhaust-Fume-Management    PWM fan, grease/carbon filtration
├── 06-Compliance/
│   └── 01-Safety-Compliance           IEC 60335, food safety, BIS
├── 07-Development/
│   └── 01-Prototype-Development-Plan  20-24 week phased roadmap
├── 08-Components/
│   ├── 01-Compute-Module-Components   CM5 + STM32 BOM ($188)
│   ├── 02-Actuation-Components        ASD/CID/SLD + induction BOM ($197)
│   ├── 03-Sensor-Components           Sensors BOM ($65)
│   └── 04-Total-Component-Cost        Full BOM ($700 prototype)
├── 09-PCB/
│   ├── 01-Controller-PCB-Design       STM32G474RE controller board (160x90mm)
│   └── 02-Driver-PCB-Design           Power electronics &  drivers (160x90mm)
├── 10-Backend/
│   ├── 01-Backend-Architecture        Fastify API, cloud services, MQTT
│   ├── 02-Database-Schema             PostgreSQL schema for cloud and device
│   └── 03-Admin-Portal                Next.js admin dashboard
├── 11-API/
│   ├── 01-REST-API-Reference          Mobile and admin REST endpoints
│   ├── 02-WebSocket-Events            Real-time cooking event streams
│   ├── 03-MQTT-Topics                 Device telemetry and command topics
│   └── 04-BLE-Services                BLE pairing and WiFi provisioning
├── 12-MobileApps/
│   ├── 01-Mobile-Architecture         Native app strategy and shared patterns
│   ├── 02-iOS-App                     SwiftUI implementation details
│   └── 03-Android-App                 Kotlin/Compose implementation details
└── 13-ProjectManagement/
    ├── 01-Epics                       High-level project epics
    ├── 02-Stories                     User stories breakdown
    ├── 03-Sprints                     Sprint planning and schedule
    ├── 04-Procurement-Schedule        Component procurement timeline
    ├── 05-Resource-Allocation         Team resource planning
    └── 06-Weekly-Status-Report-Template  Status report template
```

## Story Workflow — GitHub Project as Single Source of Truth

All story tracking happens exclusively through **GitHub Project #3** (`manasXP/epicura`). Do NOT use local todo files, TaskCreate, or any other local tracking. The GitHub project is the single source of truth.

### GitHub Project IDs

| Resource | ID |
|----------|-----|
| Project | `PVT_kwHOAD5QWs4BPXSp` |
| Status field | `PVTSSF_lAHOAD5QWs4BPXSpzg9yy_8` |
| Epic field | `PVTSSF_lAHOAD5QWs4BPXSpzg90S9I` |

### Status Options

| Status | Option ID | When |
|--------|-----------|------|
| **Todo** | `f75ad846` | Default — story is in backlog |
| **In Progress** | `47fc9ee4` | Work has started on the story |
| **Done** | `98236657` | All AC fulfilled and unit tests pass |

### Workflow When Assigned a Story

1. **Before starting work** — Move the story to "In Progress":
   ```
   gh api graphql -f query='mutation {
     updateProjectV2ItemFieldValue(input: {
       projectId: "PVT_kwHOAD5QWs4BPXSp"
       itemId: "<ITEM_ID>"
       fieldId: "PVTSSF_lAHOAD5QWs4BPXSpzg9yy_8"
       value: {singleSelectOptionId: "47fc9ee4"}
     }) { projectV2Item { id } }
   }'
   ```

2. **During development** — Read the issue body for acceptance criteria and tasks:
   ```
   gh issue view <NUMBER> --repo manasXP/epicura
   ```

3. **On completion** — Only after ALL acceptance criteria are met AND unit tests pass, move to "Done":
   ```
   gh api graphql -f query='mutation {
     updateProjectV2ItemFieldValue(input: {
       projectId: "PVT_kwHOAD5QWs4BPXSp"
       itemId: "<ITEM_ID>"
       fieldId: "PVTSSF_lAHOAD5QWs4BPXSpzg9yy_8"
       value: {singleSelectOptionId: "98236657"}
     }) { projectV2Item { id } }
   }'
   ```

4. **Close the issue** after marking Done:
   ```
   gh issue close <NUMBER> --repo manasXP/epicura
   ```

### Finding the Project Item ID for an Issue

To get the project item ID needed for status updates:
```
gh api graphql -f query='query {
  node(id: "PVT_kwHOAD5QWs4BPXSp") {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          id
          content { ... on Issue { number } }
        }
      }
    }
  }
}' | python3 -c "import json,sys; [print(n['id']) for n in json.load(sys.stdin)['data']['node']['items']['nodes'] if n.get('content',{}).get('number')==ISSUE_NUM]"
```

### Epic Field Option IDs

| Epic | Option ID |
|------|-----------|
| PCB | `8203536b` |
| EMB | `f3240268` |
| THR | `b66d5bba` |
| ARM | `832b12d6` |
| CV | `32ac1868` |
| RCP | `82971625` |
| UI | `1dd69618` |
| BE | `1667d462` |
| IOS | `1201f22f` |
| AND | `bb117488` |
| ADM | `e5a55951` |
| INT | `e2f6a7f7` |
| UX | `9898d825` |

### Rules

- **NEVER** track progress locally (no `__todo.md`, no TaskCreate/TaskUpdate for story tracking)
- **ALWAYS** read the GitHub issue for the current acceptance criteria before starting work
- **ALWAYS** move status to "In Progress" before writing any code
- **NEVER** mark "Done" unless all acceptance criteria checkboxes can be checked off and tests pass
- If blocked, add a comment to the GitHub issue explaining the blocker

## Workspace Conventions

- `__init.md` — Project definition and requirements
- `docs/` — Structured documentation
- Follow the Obsidian vault conventions from the parent `CLAUDE.md` for note formatting and linking
