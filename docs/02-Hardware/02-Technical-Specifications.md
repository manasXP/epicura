---
created: 2026-02-15
modified: 2026-02-16
version: 2.0
status: Draft
---

# Technical Specifications

## Heating System

### Induction Heater (Microwave Surface Module)

The primary cooking element is a commercial microwave induction surface — a self-contained module with its own power coil, driver electronics, and AC power stage. The module handles all high-voltage power electronics internally and exposes a CAN bus interface for external control. This eliminates the need for custom IGBT driver circuits.

- **Rated Power:** 1,800W maximum
- **AC Input:** 220-240V, 50Hz single-phase (standard Indian household outlet) — connected directly to module
- **Coil Diameter:** 180-220mm (matched to pot base, internal to module)
- **Temperature Range:** 60-250C surface temperature
- **Control:** PID loop at 10Hz on STM32, power commands sent via CAN bus to module
- **Control Interface:** CAN 2.0B at 500 kbps (STM32 FDCAN1)
- **Pot Detection:** Internal to module (won't heat without compatible pot)
- **Internal Safety:** Pot detection, thermal cutoff, overcurrent protection (all module-internal)

### Power Level Profiles

| Profile | Power (W) | Temp Range (C) | Use Case | Duty Cycle |
|---------|-----------|-----------------|----------|------------|
| **Sear** | 1,800 | 200-250 | Browning onions, tempering spices | 100% |
| **Boil** | 1,500 | 100 | Bringing water/gravy to boil | 85% |
| **Simmer** | 400-600 | 80-95 | Slow cooking dal, curry reduction | 25-35% |
| **Warm** | 200 | 60-70 | Keep-warm after cooking complete | 10-15% |
| **Off** | 0 | Ambient | Idle, cool-down | 0% |

### PID Control Parameters

- **Setpoint Source:** Recipe state machine (via CM5 command)
- **Feedback:** IR thermometer (primary), NTC thermistor (secondary/safety)
- **Loop Rate:** 10Hz (100ms period)
- **Output:** Power level command (0-100%) via CAN bus to microwave surface module
- **Overshoot Protection:** Maximum 10C above setpoint triggers power reduction
- **Safety Cutoff:** NTC >280C or IR >270C triggers immediate shutdown

## Sensor Specifications

### Camera Module

| Parameter | Value |
|-----------|-------|
| Module | IMX219 (standard) or IMX477 (HQ option) |
| Resolution | 1920x1080 at 30fps (1080p) |
| Interface | MIPI CSI-2 (2-lane) to CM5 |
| Sensor Size | 1/4" (IMX219) or 1/2.3" (IMX477) |
| Field of View | 62.2 (IMX219) or adjustable C/CS mount (IMX477) |
| White Balance | Auto white balance with LED ring compensation |
| Illumination | WS2812B LED ring (12-16 LEDs) or white LED ring with diffuser |
| Mounting | Overhead gantry, 20-30cm above pot center |
| Purpose | Food color/texture analysis, stage detection via CV |

### IR Thermometer

| Parameter | Value |
|-----------|-------|
| Part | MLX90614ESF-BAA (medical/food grade) |
| Type | Non-contact infrared thermopile |
| Interface | I2C (address 0x5A default), connected to STM32 |
| Object Temp Range | -70C to +380C |
| Accuracy | +/-0.5C (0-50C ambient), +/-1.0C (full range) |
| Field of View | 90 (wide FOV variant) |
| Resolution | 0.02C |
| Supply Voltage | 3.3V |
| Mounting | Angled toward pot center, 5-10cm distance |
| Purpose | Food surface temperature, PID feedback |

### Load Cells

| Parameter | Value |
|-----------|-------|
| Configuration | 4x 5kg strain gauges in full Wheatstone bridge |
| Total Capacity | 20kg (pot + ingredients + margin) |
| ADC | HX711 24-bit sigma-delta, 2 channels |
| Interface | SPI-like protocol (DOUT/SCK) to STM32 GPIO |
| Sampling Rate | 10Hz or 80Hz (selectable) |
| Resolution | ~1g at 10Hz, ~3g at 80Hz |
| Tare | Software tare on boot and on pot placement |
| Excitation | 5V from HX711 on-chip regulator |
| Purpose | Ingredient weight, evaporation tracking, pot detection |

### NTC Thermistors

| Parameter | Value |
|-----------|-------|
| Type | NTC 100k ohm at 25C (B25/85 = 3950K typical) |
| Quantity | 2 (coil temperature + ambient enclosure) |
| Interface | Voltage divider with 100k ohm reference resistor, STM32 ADC |
| ADC Resolution | 12-bit STM32 internal ADC |
| Range | 0-300C (coil), 0-80C (ambient) |
| Accuracy | +/-2C (with Steinhart-Hart calibration) |
| Purpose | Coil over-temperature protection, ambient monitoring |

## Data Storage

### Storage Architecture

| Storage | Medium | Capacity | Purpose |
|---------|--------|----------|---------|
| **eMMC** | On-board CM5 carrier | 8-16 GB | OS, application, recipe DB, cooking logs |
| **SD Card** | MicroSD slot on CM5 | 16-64 GB (optional) | Recipe backup, logs archive, user media |
| **RAM** | LPDDR4 on CM5 | 4-8 GB | Runtime, CV inference, UI frame buffer |

### Recipe Database

- **Format:** JSON or YAML per recipe file
- **Recipe Count:** 100+ initial, expandable via OTA
- **Size per Recipe:** ~30-50 KB (steps, temps, timings, images)
- **Total DB Size:** ~5-10 MB initial
- **Storage:** SQLite index + individual recipe files on eMMC
- **Sync:** Cloud download to local, offline fallback guaranteed

### Cooking Logs

- **Format:** SQLite database
- **Fields:** Timestamp, recipe ID, step transitions, temperatures (IR + NTC), weights, durations, errors, user feedback
- **Retention:** Last 500 cook sessions (~50 MB)
- **Export:** JSON via app or USB

### User Preferences

- **Format:** JSON configuration file
- **Contents:** Spice levels, allergens, dietary restrictions, portion sizes, WiFi credentials
- **Backup:** Synced to cloud account when connected

## Power Specifications

| Parameter | Specification |
|-----------|---------------|
| **AC Input** | 220-240V, 50Hz, single-phase |
| **Maximum Draw** | <2,000W (1,800W induction + 75W system) |
| **Fuse Rating** | 10A (IEC C14 inlet with integrated fuse) |
| **PSU** | Mean Well LRS-75-24 (24V / 3.2A / 76.8W) |
| **24V Rail** | 24V / 3.2A — main bus from PSU; feeds actuators (12V, 6.5V rails), induction CAN control, safety relay |
| **12V UPS Input** | 12V DC from off-the-shelf UPS — feeds TPS54531 12V→5V 5A buck on Driver PCB |
| **5V Rail** | 5V / 5A (UPS-backed, from TPS54531) — CM5, STM32 controller (via 3.3V LDO), LED ring, buzzer |
| **3.3V Rail** | 3.3V / 500mA (LDO from 5V on Controller PCB) — STM32, sensors, I2C devices |
| **Standby Power** | <5W (CM5 idle, display off, induction off) |
| **PSU Type** | Mean Well enclosed AC-DC, single 24V output |
| **Efficiency** | >87% at full load (Mean Well LRS-75 series) |

### 12V UPS Recommended Specifications

An off-the-shelf 12V UPS powers the 5V rail (CM5 + STM32) independently of the 24V PSU, allowing the system to detect AC power loss, save cooking state, and gracefully pause.

| Parameter | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| Output Voltage | 12V DC | 12V DC (regulated) | Must be within TPS54531 input range (3.5-28V) |
| Output Current | 3A | 5A | 5V rail peak is ~4A; headroom for inrush |
| Battery Capacity | 7Ah (84Wh) | 9Ah (108Wh) | At ~20W load (CM5 + STM32 + display), 7Ah gives ~25 min runtime |
| Battery Type | Sealed lead-acid (SLA) | Lithium iron phosphate (LiFePO4) | LiFePO4: lighter, longer cycle life, flat discharge curve |
| Charging | Integrated (AC mains) | Integrated with auto-switchover | UPS charges from AC; switches to battery on AC loss |
| Switchover Time | <20ms | <10ms | Must be faster than CM5's hold-up (bulk caps provide ~50ms) |
| Output Connector | Bare wire or barrel jack | XT30 (to match J_12V_UPS) | Adapter cable may be needed |
| Form Factor | — | Compact, <2kg | Must fit inside or adjacent to Epicura enclosure |

**Example products:** Mini DC UPS modules (e.g., "12V 5A UPS module" on AliExpress/Amazon, ~$15-30) that accept 12V AC adapter input, contain a LiFePO4 or Li-ion battery pack, and provide uninterrupted 12V output with automatic switchover.

> [!tip]
> During AC power failure, only the 5V rail (CM5 + STM32 + display) remains powered. The 24V rail (actuators, induction) goes down immediately. The STM32 detects 24V loss via COMP2 comparator (<100µs), disables all actuators, and notifies the CM5 to save state. At ~20W idle draw, a 7Ah 12V battery provides approximately 25 minutes — enough time to save state and wait for power restoration. If power returns within 5 minutes, cooking auto-resumes; otherwise the user is prompted.

### Power Budget Breakdown

| Subsystem | Typical (W) | Peak (W) |
|-----------|-------------|----------|
| Induction heater | 600 | 1,800 |
| CM5 + camera + display | 15 | 25 |
| STM32 + sensors | 2 | 3 |
| Servo arm (stirring) | 5 | 15 |
| P-ASD pump + solenoids | 1 | 10 |
| CID linear actuators (x2) | 0 | 5 |
| SLD pumps (x2) + solenoids (x2) | 0 | 16 |
| LED ring | 2 | 5 |
| Exhaust fan | 1 | 3 |
| PSU losses | 10 | 30 |
| **Total** | **637** | **1,894** |

## Performance Requirements

| Parameter | Target | Notes |
|-----------|--------|-------|
| CV Inference Latency | <500ms | Food stage classification per frame |
| PID Control Loop | 10Hz (100ms) | Temperature regulation on STM32 |
| Motor Control Loop | 50Hz (20ms) | Servo position updates on STM32 |
| UI Response Time | <200ms | Touch-to-visual feedback on display |
| System Boot Time | <30s | Power-on to recipe selection screen |
| Temperature Accuracy | +/-5C | IR sensor to actual food surface |
| Dispensing Accuracy | ±10% (P-ASD), ±5% (SLD) | P-ASD by pot weight, SLD by dedicated per-reservoir load cells (2× 2 kg) |
| Camera Latency | <100ms | Capture to frame available in memory |
| Recipe Step Transition | <2s | From stage detection to actuator response |
| WiFi Connection | <10s | Auto-reconnect to saved network |
| OTA Update | <5 min | Full recipe DB refresh over WiFi |

## Communication Interfaces

| Interface | Protocol | Speed | Endpoints | Purpose |
|-----------|----------|-------|-----------|---------|
| CM5 <-> STM32 | UART (primary) | 115200 baud | CM5 UART0 <-> STM32 USART1 | Commands, telemetry, heartbeat |
| CM5 <-> STM32 | CAN (alternative) | 500 kbps | CM5 SPI-CAN <-> STM32 CAN1 | Higher reliability option |
| CM5 <-> Camera | MIPI CSI-2 | 2-lane | CM5 CSI port <-> IMX219/477 | Video frames for CV |
| CM5 <-> Display | DSI or HDMI | 1080p/60Hz | CM5 DSI/HDMI <-> 10" panel | UI rendering |
| CM5 <-> Touch | I2C | 400 kHz | CM5 I2C1 <-> touch controller | Touch input events |
| STM32 <-> IR Sensor | I2C | 100 kHz | STM32 I2C1 <-> MLX90614 | Temperature readings |
| STM32 <-> Load Cells | SPI-like GPIO | 10-80 Hz | STM32 GPIO <-> HX711 | Weight measurements |
| STM32 <-> NTC | ADC | 1 Hz | STM32 ADC1 CH0/CH1 | Thermistor voltages |
| STM32 <-> Servos | PWM | 50Hz | STM32 TIM1/TIM2 <-> servo signal | Arm + gate positions |
| STM32 <-> Microwave Surface | CAN 2.0B | 500 kbps | STM32 FDCAN1 (PB8/PB9) <-> module CAN port | Induction power control via CAN |
| STM32 <-> Exhaust Fan | PWM | 25 kHz | STM32 TIM4 CH3 <-> fan 4-pin | Fume extraction speed |
| CM5 <-> WiFi | 802.11ac | Up to 867 Mbps | Onboard CM5 radio | App, cloud, OTA |
| CM5 <-> BT | BLE 5.0 | 2 Mbps | Onboard CM5 radio | Initial app pairing, proximity |

## Related Documentation

- [[Epicura-Architecture|Hardware Architecture & Wiring Diagrams]]
- [[05-Sensors-Acquisition|Sensors & Data Acquisition]]
- [[07-Mechanical-Design|Mechanical Design]]
- [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]]
- [[../01-Overview/01-Project-Overview|Project Overview]]

#epicura #technical-specifications #hardware

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-16 | Manas Pradhan | Update power budget and dispensing accuracy for P-ASD pneumatic redesign |
