# Epicura

An autonomous countertop kitchen robot that cooks one-pot meals using AI vision, robotic stirring, and precise induction heat control. Designed for compact Indian kitchens, under 2kW power draw.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Epicura System Overview                          │
│                                                                     │
│  ┌──────────────────────┐        ┌──────────────────────┐           │
│  │  Raspberry Pi CM5    │        │  STM32 MCU           │           │
│  │  (Yocto Linux)       │◄──────►│  (FreeRTOS)          │           │
│  │  - Recipe Engine     │  UART  │  - PID Control       │           │
│  │  - CV Pipeline       │  /SPI  │  - Servo Driver      │           │
│  │  - Kivy UI           │        │  - Sensor Polling    │           │
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

## Key Features

- **Autonomous Cooking** — Hands-off operation after ingredient loading with state machine recipe execution
- **AI Vision** — Overhead camera with TFLite MobileNetV2 for food color/texture analysis and cooking stage detection
- **Induction PID Control** — 1,800W microwave induction surface (CAN bus) with closed-loop PID, ±5°C accuracy
- **Robotic Stirring Arm** — Single-axis servo arm with multiple stir patterns and auto-scraping
- **Three-Subsystem Dispensing** — Seasonings (servo-gated hoppers), coarse ingredients (linear actuator trays), liquids (peristaltic pumps)
- **Touchscreen + Mobile Apps** — 10" Kivy touchscreen UI, native iOS (Swift) and Android (Kotlin) companion apps
- **100+ Indian Recipes** — Curries, dal, rice, biryani with regional variations and dietary customization
- **Cloud + Offline** — Cloud-updatable recipe library with full local fallback

## Hardware Architecture

| Component | Part | Purpose |
|-----------|------|---------|
| Compute (AI) | Raspberry Pi CM5 (4GB, 64GB eMMC) | Vision, recipe engine, UI, cloud sync |
| Compute (Control) | STM32G474 (Cortex-M4F, 170 MHz) | PID, servo driver, sensor polling, safety |
| Carrier Board | CMIO (official RPi IO board) | CM5 carrier with all breakouts |
| Camera | IMX219 (8MP) | Food stage detection via CV |
| IR Thermometer | MLX90614 | Non-contact food surface temp |
| Load Cells | 4× strain gauge + HX711 | Weight-based dispensing verification |
| Induction Surface | 1,800W commercial module | CAN bus controlled cooking heat |
| Servo Arm | DS3225 (25 kg·cm) | Stirring and scraping |
| Display | 10" 1280×800 capacitive | Kivy touchscreen UI |

## Software Stack

### CM5 (Yocto Linux + Docker Compose)

- **Database**: PostgreSQL 16 — same schema as cloud
- **MQTT**: Mosquitto broker with cloud bridge
- **Backend API**: FastAPI (Python) — REST endpoints
- **Recipe Engine**: Python — YAML parsing, state machine
- **CV Pipeline**: OpenCV + TFLite MobileNetV2 INT8
- **UI**: Kivy — touchscreen interface
- **OTA Updates**: swupdate with A/B partitions

### STM32 (FreeRTOS)

- 4 tasks: PID (100 Hz), servo (50 Hz), sensor (10 Hz), comms (20 Hz)
- C (MISRA subset for safety-critical paths)
- Hardware watchdog, thermal cutoffs, e-stop relay

## Project Status

**Phase:** Design & Documentation

Comprehensive documentation exists across 30+ documents covering hardware, software, subsystems, compliance, PCB design, backend, APIs, mobile apps, and project management.

See [`docs/README.md`](docs/README.md) for the full documentation index.

## Estimated BOM

~$614 for prototype. See [Total Component Cost](docs/08-Components/04-Total-Component-Cost.md) for breakdown.

## Development Roadmap

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Prototype | 3–6 months | Hardware prototype, basic recipe execution, vision PoC |
| Alpha | 3–6 months | Core features, 20+ recipes, app integration, safety testing |
| Beta | 3–6 months | 100+ recipes, field testing, regulatory pre-compliance |
| Production | 3–6 months | Manufacturing, certifications, market launch |

## License

[Apache License 2.0](LICENSE)
