---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Compute Module Components

## Overview

This document details the compute subsystem components for the Epicura kitchen robot prototype, including the Raspberry Pi CM5 (AI/vision processing), STM32G474RE (motor/safety control), display module, and supporting components.

## Compute Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Compute Subsystem                            │
│                                                                 │
│  ┌──────────────┐    UART     ┌──────────────┐                 │
│  │  Raspberry   │◄───────────►│  STM32G474RE │                 │
│  │  Pi CM5      │             │  Nucleo      │                 │
│  │  (4GB RAM)   │             │  (FreeRTOS)  │                 │
│  └──────┬───────┘             └──────┬───────┘                 │
│         │                            │                         │
│    CSI-2│  HDMI/DSI              PWM │  ADC  I2C              │
│         │    │                    │  │    │    │               │
│         ▼    ▼                    ▼  ▼    ▼    ▼               │
│      Camera Display           Servos NTC  Load MLX            │
│      IMX219 10.1"             Arm   Temp  Cell 90614          │
│             IPS               Gates       HX711               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component List

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| Raspberry Pi CM5 (4GB RAM, 64GB eMMC) | SC1441 | 1 | $65.00 | $65.00 | RPi Foundation | Core compute: AI inference, vision, UI, recipe engine, Docker containers |
| CM5IO Board (carrier) | SC1439 | 1 | $20.00 | $20.00 | RPi Foundation | Official CM5 carrier board (CM5IO) with all breakouts |
| STM32G474RE Nucleo | NUCLEO-G474RE | 1 | $18.00 | $18.00 | STMicroelectronics / Mouser | Motor controller dev board; CAN-FD + advanced timers |
| 10.1" IPS Display (1280x800) | Waveshare 10.1" HDMI | 1 | $80.00 | $80.00 | Waveshare / Amazon | HDMI input + I2C capacitive touch; prototype display |
| (Storage on eMMC) | - | - | - | - | Included | 64GB eMMC on CM5 module for OS and data |
| USB-C Cable (debug/power) | - | 1 | $5.00 | $5.00 | Generic | CM5 debug console and power delivery |
| CSI-2 Ribbon Cable (15-pin) | 15-pin FFC, 200mm | 1 | $3.00 | $3.00 | Generic | Camera module to CM5 CSI connector |
| HDMI Cable (flat ribbon) | Micro-HDMI to HDMI | 1 | $5.00 | $5.00 | Generic | CM5 to display connection |

---

## Cost Summary

| Item | Cost |
|------|------|
| Raspberry Pi CM5 (4GB, 64GB eMMC) | $65.00 |
| CM5IO Board | $20.00 |
| STM32G474RE Nucleo | $18.00 |
| 10.1" Display | $80.00 |
| Cables | $13.00 |
| **Category Subtotal** | **$196.00** |

---

## Design Notes

### CM5 Selection Rationale
- **4GB RAM** sufficient for Yocto Linux + Docker + PostgreSQL + Python services + OpenCV + TFLite
- **64GB eMMC** provides ample space for:
  - Base OS (~500MB)
  - Docker images (PostgreSQL, MQTT, Python services) (~2-3GB)
  - Recipe database with images (~5-10GB)
  - Cooking logs and telemetry (~5GB)
  - Firmware updates (A/B partitions) (~2GB)
  - Remaining space for future expansion (~40GB+)
- CM5IO carrier board provides all necessary breakouts without custom PCB
- CM5 provides dual CSI-2 camera interfaces (one used, one spare)
- WiFi 802.11ac + Bluetooth 5.0 built-in (no external wireless module needed)
- 40-pin GPIO header provides UART, I2C, SPI for STM32 bridge communication

### STM32G474RE Selection Rationale
- **Cortex-M4F @ 170 MHz** with FPU for PID calculations
- **CAN-FD** peripheral (future production bus architecture)
- **Advanced timers** (TIM1, TIM8) with complementary PWM for servo control
- **12-bit ADC** (5 Msps) for NTC thermistor and load cell reading
- **UART** for CM5 communication link
- Nucleo board provides ST-Link debugger and Arduino-compatible headers

### Display Choice
- Prototype uses standalone HDMI display (simpler integration)
- Production will use **OEM panel** with direct DSI connection to CM5
- I2C touch controller allows CM5 to handle touch input directly

### Production Upgrade Path

| Item | Prototype | Production |
|------|-----------|------------|
| CM5 carrier | CM5IO Board | CM5IO Board (off-the-shelf, same for production) |
| STM32 | Nucleo dev board | Bare STM32G474RE on controller PCB |
| Display | Standalone HDMI | OEM DSI panel, bezel-mounted |
| Storage | 64GB eMMC on CM5 | 64GB/128GB eMMC on CM5 |
| Software | Docker Compose | Docker Swarm or K3s for orchestration |

---

## Related Documentation

- [[02-Actuation-Components|Actuation Components]]
- [[03-Sensor-Components|Sensor Components]]
- [[04-Total-Component-Cost|Total Component Cost]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]

---

#epicura #components #compute #bom

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
