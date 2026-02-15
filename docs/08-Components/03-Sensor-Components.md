---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Sensor Components

## Overview

This document details the sensing subsystem components for the Epicura kitchen robot prototype, including the vision camera, infrared thermometer, load cells, temperature sensors, and supporting components.

## Sensor Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Sensor Subsystem                             │
│                                                                 │
│  ┌──────────────┐  CSI-2   ┌──────────────┐                   │
│  │  IMX219      │─────────►│  Raspberry   │                   │
│  │  Camera      │          │  Pi CM5      │                   │
│  └──────────────┘          │  (Vision AI) │                   │
│                            └──────────────┘                   │
│  ┌──────────────┐                                              │
│  │  WS2812B     │◄── GPIO (NeoPixel data line)                │
│  │  LED Ring    │                                              │
│  └──────────────┘                                              │
│                                                                 │
│  ┌──────────────┐  I2C     ┌──────────────┐                   │
│  │  MLX90614    │─────────►│  STM32G474RE │                   │
│  │  IR Thermo   │          │  (Controller)│                   │
│  └──────────────┘          │              │                   │
│                            │              │                   │
│  ┌──────────────┐  SPI     │              │                   │
│  │  HX711 ADC   │─────────►│              │                   │
│  │  (Load Cell) │          │              │                   │
│  └──────┬───────┘          │              │                   │
│         │                  │              │                   │
│  ┌──┐┌──┐┌──┐┌──┐         │              │                   │
│  │LC││LC││LC││LC│ x4      │              │                   │
│  └──┘└──┘└──┘└──┘         │              │                   │
│                            │              │                   │
│  ┌──────────────┐  ADC     │              │                   │
│  │  NTC x2      │─────────►│              │                   │
│  │  Thermistors │          │              │                   │
│  └──────────────┘          │              │                   │
│                            │              │                   │
│  ┌──────────────┐  GPIO    │              │                   │
│  │  Reed Switch │─────────►│              │                   │
│  │  (Pot Detect)│          └──────────────┘                   │
│  └──────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component List

### Option A: Standard Camera (Recommended for Prototype)

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| Camera Module IMX219 | RPi Camera Module V2 | 1 | $25.00 | $25.00 | RPi Foundation | 8MP, CSI-2, fixed focus, sufficient for CV |

### Option B: Premium Camera (Production Consideration)

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| Camera Module IMX477 | RPi HQ Camera | 1 | $50.00 | $50.00 | RPi Foundation | 12.3MP, C-mount lens, adjustable focus |

### Thermal & Weight Sensors

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| IR Thermometer | MLX90614ESF-BAA | 1 | $12.00 | $12.00 | Mouser / DigiKey | Non-contact, I2C, 90° FOV, -70 to +380°C |
| Load Cell (5kg) | CZL635 | 4 | $4.00 | $16.00 | Amazon / AliExpress | Wheatstone bridge, aluminum alloy |
| HX711 ADC Module | HX711 breakout | 1 | $3.00 | $3.00 | Amazon / AliExpress | 24-bit, 80 SPS, SPI/GPIO interface |
| NTC Thermistor (100k ohm) | NTCLE100E3104 | 2 | $1.00 | $2.00 | Mouser | Coil temp + ambient temp monitoring |

### Detection & Illumination

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| Reed Switch | MKA-14103 | 1 | $1.00 | $1.00 | Amazon | Pot detection (magnet in pot base) |
| LED Ring (WS2812B) | 12-LED NeoPixel Ring | 1 | $5.00 | $5.00 | Adafruit / Amazon | Camera illumination, consistent lighting |

### Passive Components

| Component | Part Number | Qty | Unit Price | Subtotal | Supplier | Notes |
|-----------|-------------|-----|------------|----------|----------|-------|
| Resistors (10k ohm, NTC divider) | 0603, 1% | 2 | $0.10 | $0.20 | Any | Voltage divider for NTC thermistor ADC input |
| Decoupling Caps (100nF) | 0603, X7R | 5 | $0.10 | $0.50 | Any | I2C/SPI line filtering and bypass |
| Pull-up Resistors (4.7k ohm) | 0603, 1% | 2 | $0.10 | $0.20 | Any | I2C bus pull-ups for MLX90614 |

---

## Cost Summary

### With IMX219 (Recommended for Prototype)

| Item | Cost |
|------|------|
| IMX219 Camera | $25.00 |
| MLX90614 IR Thermometer | $12.00 |
| Load Cells (4x CZL635) | $16.00 |
| HX711 ADC | $3.00 |
| NTC Thermistors (2x) | $2.00 |
| Reed Switch | $1.00 |
| LED Ring (WS2812B) | $5.00 |
| Passive Components | $0.90 |
| **Category Subtotal** | **$64.90** |

### With IMX477 (Premium Option)

| Item | Cost |
|------|------|
| IMX477 Camera | $50.00 |
| All other sensors (same) | $39.90 |
| **Category Subtotal** | **$89.90** |

---

## Design Notes

### Camera Selection

| Feature | IMX219 (V2) | IMX477 (HQ) |
|---------|-------------|-------------|
| Resolution | 8 MP (3280x2464) | 12.3 MP (4056x3040) |
| Sensor Size | 1/4" | 1/2.3" |
| Lens | Fixed (integrated) | C-mount (interchangeable) |
| Focus | Fixed (~30 cm to infinity) | Manual focus ring |
| Price | $25 | $50 |
| Prototype Use | Recommended | Overkill |
| Production Use | May suffice | Better for challenging conditions |

**Recommendation:** IMX219 for prototype. Fixed focus simplifies mounting. 8 MP is more than sufficient for food stage classification (model input is typically 224x224 pixels). Consider IMX477 for production if variable focus or better low-light performance is needed.

### MLX90614ESF-BAA IR Thermometer
- **90° FOV (BAA variant):** Covers entire pot surface from overhead mounting
- **Temperature range:** -70°C to +380°C (food range: 20°C to 250°C)
- **Accuracy:** ±0.5°C in 0-50°C range, ±2°C at higher temperatures
- **Interface:** I2C (SMBus compatible), default address 0x5A
- **Mounting:** 15-20 cm above pot surface for full pot coverage

### Load Cell Configuration
- **4x CZL635** in Wheatstone bridge configuration
- Mounted at corners of platform base
- Full-scale range: 5 kg per cell, 20 kg total (pot + ingredients max ~5 kg)
- **HX711 ADC:** 24-bit resolution, 80 SPS mode for responsive weight tracking
- Calibration: 5-point (0, 500g, 1000g, 2000g, 3000g) with known weights

### NTC Thermistor Usage
- **NTC 1 (enclosure hot-zone):** Mounted near microwave surface module, safety monitoring at 200°C
- **NTC 2 (ambient temperature):** Inside enclosure, used for temperature compensation
- **Voltage divider:** 10k ohm series resistor, midpoint to STM32 ADC (12-bit)
- **Steinhart-Hart equation** for accurate temperature conversion in firmware

---

## Related Documentation

- [[01-Compute-Module-Components|Compute Module Components]]
- [[02-Actuation-Components|Actuation Components]]
- [[04-Total-Component-Cost|Total Component Cost]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]

---

#epicura #components #sensors #bom

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
