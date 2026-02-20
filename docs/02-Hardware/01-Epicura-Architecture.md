---
created: 2026-02-15
modified: 2026-02-15
version: 2.0
status: Draft
---

# Epicura Hardware Architecture & Wiring Diagrams

## Overview

This document provides the comprehensive hardware architecture, wiring diagrams, and interface specifications for the Epicura autonomous kitchen robot. The system uses a dual-processor architecture: a Raspberry Pi CM5 running Yocto Linux for AI/vision/UI, and an STM32G4 microcontroller running FreeRTOS for real-time motor control, sensing, and safety.

---

## System Block Diagram

```
                              ┌─────────────────────────────────┐
                              │          AC Mains Input         │
                              │      220-240V 50Hz <2kW         │
                              └────────────────┬────────────────┘
                                               │
                                        ┌──────▼──────┐
                                        │  EMI Filter  │
                                        │  + IEC C14   │
                                        └──────┬──────┘
                                               │
                              ┌────────────────▼────────────────┐
                              │       Switch-Mode PSU           │
                              │  AC-DC Multi-Output + PFC       │
                              └──┬────────┬────────┬────────┬───┘
                                 │        │        │        │
                              5V/3A   3.3V/500mA 12V/2A  24V/1A
                                 │        │        │        │
          ┌──────────────────────┼────────┼────────┼────────┼──────────────────┐
          │                      │        │        │        │                  │
          │                      ▼        │        ▼        ▼                  │
          │  ┌───────────────────────┐    │   ┌────────────────────────────┐   │
          │  │  Raspberry Pi CM5     │    │   │  STM32G474RE              │   │
          │  │  (Yocto Linux)        │    │   │  (FreeRTOS)               │   │
          │  │                       │    │   │                            │   │
          │  │  - Recipe Engine      │    │   │  - PID Heat Control       │   │
          │  │  - CV Inference       │    │   │  - Servo Motor Control    │   │
          │  │  - UI Rendering       │    │   │  - Sensor Acquisition     │   │
          │  │  - Cloud/WiFi/BT     │    │   │  - Dispensing Logic       │   │
          │  │  - OTA Updates        │    │   │  - Safety Monitoring     │   │
          │  │                       │    │   │                            │   │
          │  │  ┌─────┐  ┌────────┐  │    │   │  ┌──────┐  ┌───────────┐  │   │
          │  │  │CSI-2│  │DSI/HDMI│  │    │   │  │ PWM  │  │ ADC/GPIO  │  │   │
          │  │  └──┬──┘  └───┬────┘  │    │   │  └──┬───┘  └─────┬─────┘  │   │
          │  └─────┼─────────┼───────┘    │   └─────┼─────────────┼────────┘   │
          │        │         │    ▲       │         │             │             │
          │        │         │    │ SPI (2 MHz)      │             │             │
          │        │         │    │ + IRQ line        │             │             │
          │        │         │    └─────────────────►│             │             │
          │        ▼         ▼                       ▼             ▼             │
          │   ┌────────┐ ┌──────────┐      ┌──────────────┐ ┌──────────────┐   │
          │   │IMX219/ │ │10" Touch │      │Microwave     │ │  Sensors     │   │
          │   │IMX477  │ │Display   │      │Induction     │ │  MLX90614    │   │
          │   │Camera  │ │(DSI+I2C) │      │Surface (CAN) │ │  HX711      │   │
          │   └────────┘ └──────────┘      └──────────────┘ │             │   │
          │                                                  └──────────────┘   │
          │   ┌────────┐ ┌──────────┐      ┌──────────────┐ ┌──────────────┐   │
          │   │WiFi    │ │eMMC/SD   │      │DS3225 Main   │ │ASD SG90 x3  │   │
          │   │802.11ac│ │8-16GB    │      │Servo Arm     │ │CID LinAct x2│   │
          │   │BLE 5.0 │ │Storage   │      │(Stirring)    │ │SLD Pumps x2 │   │
          │   └────────┘ └──────────┘      └──────────────┘ └──────────────┘   │
          │                                                                     │
          │   ┌────────────────────────────────────────────────────────────┐    │
          │   │  LED Ring (WS2812B x 12-16) ── GPIO/SPI from CM5 or STM32│    │
          │   └────────────────────────────────────────────────────────────┘    │
          └─────────────────────────────────────────────────────────────────────┘
```

---

## Main Component List

| Component | Part Number | Interface | Connected To | Purpose |
|-----------|-------------|-----------|--------------|---------|
| Compute Module | Raspberry Pi CM5 | - | Carrier board | AI/vision, recipe engine, UI, networking |
| CM5 Carrier Board | Custom or IO Board | GPIO/CSI/DSI/USB | CM5 module | Breakout for all CM5 interfaces |
| Motor Controller | STM32G474RE (LQFP-64) | - | Custom PCB | Real-time control: PID, servos, sensors, safety |
| Camera Module | IMX219 or IMX477 | MIPI CSI-2 | CM5 CSI port | Overhead food monitoring, CV inference |
| IR Thermometer | MLX90614ESF-BAA | I2C | STM32 I2C1 | Non-contact food surface temperature |
| Load Cell ADC | HX711 | SPI-like GPIO | STM32 GPIO | 24-bit weight measurement from strain gauges |
| Strain Gauges | 4x 5kg load cells | Wheatstone bridge | HX711 | Weight sensing under pot platform |
| Main Servo Motor | DS3225 25kg-cm | PWM (50Hz) | STM32 TIM1 CH1 (PA8) | Stirring arm rotation |
| ASD Gate Servos | SG90 (x3) | PWM (50Hz) | STM32 TIM2 CH1-3 (PA0-PA2) | Seasoning dispenser gates |
| ASD Vibration Motors | ERM 3V (x3) | GPIO | STM32 PC7, PD2, PA3 via MOSFET | Anti-clog mechanism (one per hopper) |
| CID Linear Actuators | 12V DC (x2) via DRV8876 | GPIO (EN/PH) | STM32 PA10/PB4, PB5/PC2 | Coarse ingredient push-plate sliders |
| SLD Peristaltic Pumps | 12V DC (x2) via TB6612 | GPIO (PWM/DIR) | STM32 PC3-PC6 | Oil and water dispensing |
| SLD Solenoid Valves | 12V NC (x2) | GPIO | STM32 PA7, PA9 via MOSFET | Liquid drip prevention |
| Exhaust Fans | 2× 120mm 12V DC brushless | PWM (25kHz) | STM32 PA6, PB10 via MOSFET | Fume extraction, independent control |
| Piezo Buzzer | 5V active | PWM | STM32 PA11 via MOSFET | Audio alerts |
| Microwave Induction Surface | Commercial module w/ CAN | CAN 2.0B (500kbps) | STM32 FDCAN1 (PB8/PB9) | Self-contained induction heating with internal coil, driver, and safety |
| 10" Touchscreen | Generic DSI/HDMI 10.1" IPS | DSI or HDMI + I2C | CM5 DSI/HDMI + I2C | User interface display |
| PSU Module | Mean Well LRS-75-24 | AC-DC 24V | AC mains input | 24V DC for CM5IO, controller, servos |
| Safety Relay | Omron G5V-2 or equiv. | GPIO (via MOSFET) | STM32 GPIO | Induction mains disconnect |
| LED Ring | WS2812B strip (12-16 LEDs) | SPI/GPIO data line | CM5 or STM32 GPIO | Pot illumination for camera |
| E-Stop Button | Normally-closed mushroom | GPIO (interrupt) | STM32 GPIO + relay | Emergency power cutoff |
| Pot Detection | Internal to microwave surface | CAN status | Module-reported via CAN | Detect pot presence (module-internal) |

---

## 1. Compute Platform (Raspberry Pi CM5)

### CM5 Module Specifications

| Specification | Value |
|--------------|-------|
| Processor | Broadcom BCM2712, Quad Cortex-A76 @ 2.4GHz |
| RAM | 4 GB LPDDR4X |
| Storage | 64 GB eMMC (on-module) |
| GPU | VideoCore VII (OpenGL ES 3.1, Vulkan 1.2) |
| Video Output | 2x HDMI 2.0 or 2x 4-lane DSI |
| Camera | 2x 4-lane MIPI CSI-2 |
| Networking | WiFi 802.11ac, Bluetooth 5.0 / BLE |
| USB | 1x USB 3.0, 1x USB 2.0 (from carrier) |
| PCIe | 1x PCIe 2.0 (from carrier) |
| Operating System | Yocto Linux (custom BSP) |
| Form Factor | CM4-compatible, 55x40mm |

### Carrier Board Design (CM5IO)

The CM5 mounts on the CM5IO (Raspberry Pi Compute Module IO Board) carrier that breaks out:

```
┌────────────────────────────────────────────────────────────────┐
│              CM5IO (CM5 Carrier Board)                          │
│                                                                │
│  ┌──────────────────┐                                          │
│  │  Raspberry Pi CM5 │                                         │
│  │  (mounted via      │                                        │
│  │   board-to-board   │                                        │
│  │   connectors)      │                                        │
│  └────────┬───────────┘                                        │
│           │                                                    │
│  ┌────────▼────────────────────────────────────────────────┐   │
│  │                  Interface Breakout                      │   │
│  │                                                         │   │
│  │  CSI-2 ──────► 15-pin FFC (Camera)                      │   │
│  │  DSI/HDMI ───► HDMI Type-A or 15-pin FFC (Display)     │   │
│  │  I2C1 ───────► 4-pin header (Touch Panel)              │   │
│  │  SPI0 ───────► 6-pin header (STM32 Bridge)             │   │
│  │  UART ───────► STM32 communication (fallback)          │   │
│  │  GPIO ───────► LED ring data, E-stop input              │   │
│  │  USB-C ──────► Power input (5V/3A PD) + debug           │   │
│  │  USB 2.0 ────► Expansion header                         │   │
│  │  Ethernet ───► RJ45 (debug/wired network, optional)     │   │
│  │  40-pin GPIO ► Breakout for all interfaces             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
│  Power Input: 5V / 3A from PSU 5V rail                        │
└────────────────────────────────────────────────────────────────┘
```

### CM5 GPIO Allocation

| GPIO | Function | Direction | Notes |
|------|----------|-----------|-------|
| GPIO8 (CE0) | SPI0 Chip Select to STM32 | Output | Active-low, 3.3V logic |
| GPIO9 (MISO) | SPI0 MISO from STM32 | Input | 2 MHz, 3.3V logic |
| GPIO10 (MOSI) | SPI0 MOSI to STM32 | Output | 2 MHz, 3.3V logic |
| GPIO11 (SCLK) | SPI0 Clock to STM32 | Output | 2 MHz, 3.3V logic |
| GPIO4 | IRQ from STM32 (data-ready) | Input | Active-low, interrupt |
| GPIO2 (SDA1) | I2C SDA (touch panel) | Bidirectional | 400kHz, pull-up to 3.3V |
| GPIO3 (SCL1) | I2C SCL (touch panel) | Bidirectional | 400kHz, pull-up to 3.3V |
| GPIO18 | LED ring data (WS2812B) | Output | SPI MOSI or bitbang |
| GPIO4 | E-Stop status input | Input | Active-low, interrupt |
| CSI-2 (FFC) | Camera data lanes | Input | 2-lane MIPI |
| DSI (FFC) | Display data lanes | Output | Or HDMI via carrier |

---

## 2. STM32 Motor Controller

### STM32G474RE Specifications

| Specification | Value |
|--------------|-------|
| Core | ARM Cortex-M4F @ 170 MHz |
| Flash | 512 KB |
| RAM | 128 KB SRAM |
| ADC | 5x 12-bit ADC (up to 4 Msps) |
| Timers | 17 timers (advanced, general, basic) |
| UART | 5x USART/UART |
| I2C | 4x I2C |
| SPI | 4x SPI |
| CAN | 3x FDCAN |
| PWM | Multiple channels across timers |
| GPIO | Up to 51 I/O pins (LQFP-64) |
| Supply | 3.3V (from PSU 3.3V rail) |
| RTOS | FreeRTOS |

### STM32 Pin Allocation

```
STM32G474RE (LQFP-64)
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ┌─── SPI2: CM5 Communication (Slave) ──────────────────┐     │
│  │  PB12 (SPI2_NSS)  ◄── CM5 GPIO8  (CE0)              │     │
│  │  PB13 (SPI2_SCK)  ◄── CM5 GPIO11 (SCLK)             │     │
│  │  PB14 (SPI2_MISO) ──► CM5 GPIO9  (MISO)             │     │
│  │  PB15 (SPI2_MOSI) ◄── CM5 GPIO10 (MOSI)             │     │
│  │  PB3  (GPIO IRQ)  ──► CM5 GPIO4  (data-ready, low)  │     │
│  │  Mode: SPI Mode 0, 2 MHz clock, 8-bit, DMA          │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌─── CAN: Microwave Surface ─────┐                           │
│  │  PB8  (FDCAN1_RX) ◄── J_STACK Pin 19 → Driver PCB ISO1050│
│  │  PB9  (FDCAN1_TX) ──► J_STACK Pin 20 → Driver PCB ISO1050│
│  │  Bit rate: 500 kbps, isolation + termination on Driver PCB │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── PWM: Main Servo Arm ────────┐                           │
│  │  PA8  (TIM1_CH1)  ──► DS3225 Signal (orange wire)          │
│  │  50Hz, 500-2500us pulse width                               │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── P-ASD Subsystem (Pneumatic Seasoning Dispenser) ──┐     │
│  │  PA0  (TIM2_CH1)  ──► P-ASD Diaphragm Pump PWM           │
│  │  Solenoids V1-V6: PCF8574 I2C GPIO expander              │
│  │    (I2C1 addr 0x20, on Driver PCB, outputs P0-P5)        │
│  │  I2C1 (PB6/PB7)  ──► ADS1015 Pressure Sensor (0x48)     │
│  │                   ──► PCF8574 Solenoid Expander (0x20)    │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── CID Subsystem (Coarse Ingredients Dispenser) ──┐        │
│  │  PA10 (TIM1_CH3)   ──► CID-1 Linear Actuator EN (DRV8876)│
│  │  PB4  (GPIO)       ──► CID-1 Linear Actuator PH/DIR      │
│  │  PB5  (GPIO)       ──► CID-2 Linear Actuator EN (DRV8876)│
│  │  PC2  (GPIO)       ──► CID-2 Linear Actuator PH/DIR      │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── SLD Subsystem (Standard Liquid Dispenser) ──┐           │
│  │  PC3  (GPIO)       ──► SLD-OIL Pump PWM (TB6612 PWMA)    │
│  │  PC4  (GPIO)       ──► SLD-OIL Pump DIR (TB6612 AIN1)    │
│  │  PC5  (GPIO)       ──► SLD-WATER Pump PWM (TB6612 PWMB)  │
│  │  PC6  (GPIO)       ──► SLD-WATER Pump DIR (TB6612 BIN1)  │
│  │  PA7  (GPIO)       ──► SLD-OIL Solenoid (via MOSFET)     │
│  │  PA9  (GPIO)       ──► SLD-WATER Solenoid (via MOSFET)   │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Exhaust Fans (2x 120mm) ────┐                            │
│  │  PA6  (TIM3_CH1)  ──► Exhaust Fan 1 PWM (25 kHz, HW PWM)  │
│  │  PB10 (GPIO)      ──► Exhaust Fan 2 PWM (25 kHz, SW PWM)  │
│  │  Independent control for optimal airflow                   │
│  │  Note: PB10 uses software PWM (TIM2_CH3 conflicts with PA2)│
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Audio ───────────────────────┐                           │
│  │  PA11 (TIM1_CH4)  ──► Piezo Buzzer PWM                    │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── I2C: IR Thermometer ────────┐                           │
│  │  PB6  (I2C1_SCL) ──► MLX90614 SCL                         │
│  │  PB7  (I2C1_SDA) ◄─► MLX90614 SDA                         │
│  │  100 kHz, pull-ups 4.7k to 3.3V                            │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Load Cells (HX711) ───┐                           │
│  │  PC0  (GPIO)      ──► HX711 SCK (clock out)               │
│  │  PC1  (GPIO)      ◄── HX711 DOUT (data in)                │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Safety & Control ─────┐                           │
│  │  PB0  (GPIO)      ──► Safety Relay (via MOSFET driver)     │
│  │  PB1  (GPIO)      ◄── Pot Detection (reed switch)         │
│  │  PB2  (GPIO)      ◄── E-Stop Button (interrupt, act-low)  │
│  │  PC13 (GPIO)      ──► Status LED (on-board)               │
│  └─────────────────────────────────┘                           │
│                                                                │
│  Power: 3.3V / GND from PSU rail                              │
│  Debug: SWD (PA13/PA14) via TagConnect or 10-pin header       │
│                                                                │
│  Note: All actuator signals route via J_STACK connector to     │
│  Driver PCB where power electronics drive the actuators.       │
│  J_STACK organized by subsystem: ASD (pin 15), CAN (pins 19-20),│
│  CID (21-26), Exhaust (27-28), SLD (29-36), Main (37-40) for  │
│  modular wiring harnesses.                                     │
└────────────────────────────────────────────────────────────────┘
```

---

## 3. Camera Interface

### CSI-2 Wiring (CM5 to Camera Module)

```
CM5 Carrier Board                    Camera Module (IMX219/IMX477)
(15-pin FFC Connector)               (15-pin FFC Connector)
┌──────────────────┐                 ┌──────────────────┐
│                  │   15-pin FFC    │                  │
│  CSI_D0_P ──────┼────────────────┼──── MIPI_D0_P    │
│  CSI_D0_N ──────┼────────────────┼──── MIPI_D0_N    │
│  CSI_D1_P ──────┼────────────────┼──── MIPI_D1_P    │
│  CSI_D1_N ──────┼────────────────┼──── MIPI_D1_N    │
│  CSI_CLK_P ─────┼────────────────┼──── MIPI_CLK_P   │
│  CSI_CLK_N ─────┼────────────────┼──── MIPI_CLK_N   │
│  SCL (I2C) ─────┼────────────────┼──── SCCB_SCL     │
│  SDA (I2C) ─────┼────────────────┼──── SCCB_SDA     │
│  3.3V ──────────┼────────────────┼──── VCC           │
│  GND ───────────┼────────────────┼──── GND           │
│  GPIO (CAM_EN) ─┼────────────────┼──── PWDN/EN      │
│                  │                │                  │
└──────────────────┘                └──────────────────┘

Cable: 15-pin 1.0mm pitch FFC, <20cm length
Signal: 2-lane MIPI CSI-2, up to 1Gbps/lane
```

### LED Ring Illumination

```
CM5 GPIO18 (or STM32 SPI)
      │
      │  Data (3.3V logic)
      ▼
┌───────────────────────────────────────┐
│          WS2812B LED Ring             │
│    (12-16 addressable RGB LEDs)       │
│                                       │
│  DIN ◄── Data from GPIO18            │
│  VCC ◄── 5V from PSU rail            │
│  GND ◄── Common ground               │
│                                       │
│  Mounted: Ring around camera lens     │
│  Color: Neutral white (5000-6000K)    │
│  Brightness: Software-adjustable      │
│  Current: ~60mA per LED at max white  │
│  Total: ~1A max (16 LEDs full white)  │
└───────────────────────────────────────┘

Note: 3.3V logic from CM5 may need level shift to 5V for WS2812B.
Use SN74HCT125 or similar buffer if reliability issues arise.
```

---

## 4. IR Thermometer Interface

### MLX90614 I2C Wiring

```
STM32G474RE                        MLX90614ESF-BAA
┌──────────────────┐              ┌──────────────────┐
│                  │              │                  │
│  PB6 (I2C1_SCL) ┼──────┬──────┼── SCL (Pin 3)   │
│                  │      │      │                  │
│  PB7 (I2C1_SDA) ┼──────┼──┬───┼── SDA (Pin 1)   │
│                  │      │  │   │                  │
│  3.3V ───────────┼──┬───┘  │   │                  │
│                  │  │      │   │  VDD (Pin 2) ────┼─── 3.3V
│                  │  │   4.7k   │                  │
│                  │  │      │   │  VSS (Pin 4) ────┼─── GND
│                  │  4.7k   │   │                  │
│                  │  │      │   │  I2C Addr: 0x5A  │
│  GND ────────────┼──┴──────┴───┼── GND            │
│                  │              │                  │
└──────────────────┘              └──────────────────┘

Decoupling: 100nF ceramic cap on VDD close to MLX90614
Pull-ups: 4.7k ohm to 3.3V on both SCL and SDA
Bus speed: 100 kHz (SMBus compatible)
Cable length: <30cm (keep short for I2C reliability)
```

### MLX90614 Mounting

- Mounted on a bracket angled ~30 degrees toward pot center
- Distance from food surface: 5-10cm
- FOV of 90 degrees covers pot diameter at this distance
- Protected from steam with small shroud or filter window
- Emissivity configurable in firmware (default 0.95 for food/water)

---

## 5. Display Interface

### DSI Display Wiring (Primary Option)

```
CM5 Carrier Board                    10.1" IPS Touchscreen
(DSI FFC Connector)                  (DSI + I2C Touch)
┌──────────────────┐                ┌──────────────────────────┐
│                  │  15-pin FFC    │                          │
│  DSI_D0_P ──────┼───────────────┼──── MIPI DSI D0+         │
│  DSI_D0_N ──────┼───────────────┼──── MIPI DSI D0-         │
│  DSI_D1_P ──────┼───────────────┼──── MIPI DSI D1+         │
│  DSI_D1_N ──────┼───────────────┼──── MIPI DSI D1-         │
│  DSI_CLK_P ─────┼───────────────┼──── MIPI DSI CLK+        │
│  DSI_CLK_N ─────┼───────────────┼──── MIPI DSI CLK-        │
│  3.3V ──────────┼───────────────┼──── VCC_IO               │
│  GND ───────────┼───────────────┼──── GND                  │
│  BL_EN ─────────┼───────────────┼──── Backlight Enable     │
│                  │               │                          │
└──────────────────┘               │  Touch Controller:       │
                                   │  ┌────────────────────┐  │
CM5 I2C1                           │  │  Capacitive Touch  │  │
┌──────────────────┐               │  │  Controller (I2C)  │  │
│  GPIO2 (SDA) ────┼──────────────┼──┼── SDA              │  │
│  GPIO3 (SCL) ────┼──────────────┼──┼── SCL              │  │
│  GPIO_INT ───────┼──────────────┼──┼── INT (touch event) │  │
│  GND ────────────┼──────────────┼──┼── GND              │  │
└──────────────────┘               │  └────────────────────┘  │
                                   └──────────────────────────┘

Alternative: HDMI Type-A cable from CM5 carrier HDMI port
to HDMI-input display panel (simpler, no FFC routing needed).
```

### Display Specifications

| Parameter | Value |
|-----------|-------|
| Size | 10.1 inches diagonal |
| Resolution | 1280 x 800 pixels (WXGA) |
| Panel Type | IPS TFT LCD |
| Interface | MIPI DSI (primary) or HDMI (alternative) |
| Touch | 5-point capacitive (I2C, GT911 or FT5406 controller) |
| Backlight | LED, PWM dimmable via CM5 GPIO |
| Viewing Angle | 170 degrees (IPS) |
| Brightness | 300-400 cd/m2 (adequate for kitchen ambient) |
| Supply | 3.3V logic, 12V backlight (from PSU) |

---

## 6. CM5-STM32 Communication

### SPI Wiring (Primary)

```
Raspberry Pi CM5 (SPI0 Master)     STM32G474RE (SPI2 Slave)
┌──────────────────┐               ┌──────────────────┐
│                  │               │                  │
│  GPIO8  (CE0)  ──┼──────────────►┼── PB12 (NSS)    │
│  GPIO9  (MISO) ◄─┼───────────────┼── PB14 (MISO)   │
│  GPIO10 (MOSI) ──┼──────────────►┼── PB15 (MOSI)   │
│  GPIO11 (SCLK) ──┼──────────────►┼── PB13 (SCK)    │
│  GPIO4  (IRQ)  ◄─┼───────────────┼── PB3  (IRQ)    │
│  GND ────────────┼───────────────┼── GND            │
│                  │               │                  │
└──────────────────┘               └──────────────────┘

SPI Configuration:
  Role:       CM5 = Master, STM32 = Slave
  Clock:      2 MHz
  Mode:       SPI Mode 0 (CPOL=0, CPHA=0)
  Data:       8-bit, MSB first
  NSS:        Hardware, active-low
  IRQ:        STM32 → CM5, active-low pulse (data-ready)
  DMA:        Enabled on STM32 SPI2 RX and TX
  Logic:      3.3V (both CM5 and STM32 are 3.3V native)
  Cable:      6-wire JST-SH, <30cm length
```

### CAN Bus Wiring (Microwave Surface)

CAN bus is used for controlling the microwave induction surface module. The STM32's FDCAN1 logic signals (PB8/PB9) route via J_STACK pins 19-20 to the **Driver PCB**, where an ISO1050DUB isolated CAN transceiver (5 kV RMS) converts them to differential CAN_H/CAN_L signals on J_CAN.

```
Microwave Surface              Driver PCB                    Controller PCB
(built-in CAN port)            (ISO1050DUB + J_CAN)          (STM32 FDCAN1)
┌──────────────────┐           ┌──────────────────────┐      ┌──────────────────┐
│  Onboard         │           │  ISO1050DUB          │      │  FDCAN1          │
│  CAN controller  │           │  (5kV isolation)     │      │                  │
│           │      │           │       │              │      │  PB8 (RX) ◄─────┼── J_STACK Pin 19
│  CAN_H ──┼──────┼───────────┼── CANH│              │      │  PB9 (TX) ──────┼── J_STACK Pin 20
│  CAN_L ──┼──────┼───────────┼── CANL│   R_TERM     │      │                  │
│  GND ────┼──────┼───────────┼── GND_ISO  120Ω      │      │  3.3V logic      │
│           │      │           │                      │      │  (no isolation   │
│       120 ohm    │           │  VCC1=3.3V VCC2=5V   │      │   needed here)   │
│      termination │           │  (from J_STACK)      │      │                  │
└──────────────────┘           └──────────────────────┘      └──────────────────┘

CAN Configuration:
  Bit Rate:    500 kbps (standard CAN 2.0B)
  Termination: 120 ohm at each end (module + Driver PCB)
  Isolation:   ISO1050DUB on Driver PCB (5 kV RMS, ≥6.4mm creepage)
  Nodes:       Microwave surface (required), STM32 via Driver PCB (required)
```

### Message Protocol (SPI or CAN)

| Message ID | Name | Direction | Payload | Description |
|------------|------|-----------|---------|-------------|
| 0x01 | SET_TEMP | CM5 -> STM32 | Target temp (C), ramp rate | Set induction PID setpoint |
| 0x02 | SET_STIR | CM5 -> STM32 | Speed (RPM), pattern ID | Set stirring motor parameters |
| 0x03 | DISPENSE | CM5 -> STM32 | Subsystem (ASD/CID/SLD), ID, grams/mode | Dispense via ASD servo, CID actuator, or SLD pump |
| 0x04 | E_STOP | Bidirectional | - | Emergency shutdown command |
| 0x10 | STATUS | STM32 -> CM5 | Bit flags: pot, arm, gates, heat | Current system status word |
| 0x11 | TELEMETRY | STM32 -> CM5 | IR temp, CAN coil temp, weight, duty% | Periodic sensor data (10Hz) |
| 0x12 | HEARTBEAT | Bidirectional | Sequence number, uptime | Watchdog keepalive (1Hz) |
| 0x13 | ACK/NACK | STM32 -> CM5 | Original msg ID, status code | Command acknowledgment |
| 0x20 | SET_LED | CM5 -> STM32 | LED pattern, brightness | LED ring control (if on STM32) |
| 0xFF | FAULT | STM32 -> CM5 | Fault code, sensor data | Critical fault notification |

### Protocol Format (SPI)

```
┌──────┬────────┬─────────┬───────────────┬──────────┐
│ TYPE │ MSG_ID │ LENGTH  │   PAYLOAD     │  CRC-16  │
│1 byte│ 1 byte │ 1 byte  │  0-60 bytes   │ 2 bytes  │
└──────┴────────┴─────────┴───────────────┴──────────┘

CM5 (master) initiates all transactions.
STM32 asserts IRQ (PB3 → CM5 GPIO4) when it has data to send.
Full duplex: command on MOSI, response on MISO simultaneously.
```

---

## 7. Power Supply

### AC-DC Power Supply Architecture

```
AC Mains (220-240V 50Hz)
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
┌───────────────────┐                    ┌──────────────────────────┐
│  IEC C14 Inlet    │                    │  Microwave Induction     │
│  + Fuse (10A)     │                    │  Surface Module          │
│  + EMI Filter     │                    │  (self-contained AC      │
│  (X2 cap + CMs)   │                    │   power + coil + driver) │
└────────┬──────────┘                    │  1,800W max              │
         │                               │  CAN bus ──► STM32      │
         ▼                               └──────────────────────────┘
┌────────────────────────────────────┐
│  Mean Well LRS-75-24               │
│  24V / 3.2A / 76.8W               │
│  Universal input: 85-264VAC       │
│  Efficiency: >87%                  │
│  PFC built-in                      │
└────────────────┬───────────────────┘
                 │
                 │ 24V DC Bus
                 │
     ┌───────────┼───────────┐
     │           │           │
     ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ CM5IO    │ │ Buck    │ │ Direct  │
│ Board   │ │ 24V→5V  │ │ 24V     │
│ (24V in)│ │ (servo  │ │ safety  │
│ Onboard │ │  rail,  │ │ relay,  │
│ reg→5V  │ │  LEDs)  │ │ fan     │
│ ──► CM5 │ │         │ │         │
│  +displ │ │         │ │         │
└────┬────┘ └─────────┘ └─────────┘
     │
     │ 40-pin GPIO connector
     │ (5V on pins 2,4; GND on pins 6,9,etc.)
     ▼
┌────────────┐
│ Controller │
│ PCB        │
│ 5V ──► LDO │
│ LDO→3.3V  │
│ ──► STM32  │
│     sensors│
└────────────┘

Note: Microwave induction surface has its own AC power
inlet (not through the 24V PSU). The PSU only feeds
logic, sensors, servos, and display. Controller PCB is
powered via the CM5IO board's 40-pin connector (5V rail).
STM32 controls the module via CAN bus (FDCAN1).
```

### Mean Well LRS-75-24 Specifications

| Parameter | Value |
|-----------|-------|
| Output Voltage | 24V DC |
| Output Current | 3.2A max |
| Output Power | 76.8W |
| Input Range | 85-264VAC (universal) |
| Efficiency | >87% |
| Dimensions | 129 x 97 x 30mm |
| Protections | Short circuit, overload, over-voltage |
| Certifications | UL, CE, CB |

### Power Budget Table

| Rail | Subsystem | Typical (W) | Peak (W) | Notes |
|------|-----------|-------------|----------|-------|
| AC direct | Microwave induction surface | 600 | 1,800 | Self-contained module, own AC inlet |
| 24V (via CM5IO reg) | CM5 compute module | 8 | 15 | CM5IO onboard buck to 5V, includes eMMC, WiFi, camera |
| 24V (via CM5IO reg) | Display backlight | 3 | 5 | Fed from CM5IO board 5V/12V rail |
| 24V → 5V buck | DS3225 servo | 3 | 12 | 5-7.4V via buck, peak during stall |
| 24V → 5V buck | ASD SG90 servos (x3) | 0.5 | 3 | 4.8-6V via same buck |
| 24V → 12V | CID linear actuators (x2) | 0 | 5 | 12V, only during dispense |
| 24V → 12V | SLD peristaltic pumps (x2) | 0 | 6 | 12V, only during dispense |
| 24V → 12V | SLD solenoid valves (x2) | 0 | 10 | 5W each when energized |
| 24V → 5V buck | LED ring (WS2812B) | 2 | 5 | 16 LEDs at partial brightness |
| 24V direct | Safety relay coil | 0.5 | 1 | Mains disconnect for microwave surface |
| 24V → 12V | Exhaust fans (x2) | 1 | 6 | 12V DC, 120mm, 0.3-0.5A each |
| CM5IO 5V → 3.3V | STM32G474RE | 0.3 | 0.5 | Controller PCB via CM5IO 40-pin, LDO to 3.3V |
| CM5IO 5V → 3.3V | MLX90614 + HX711 | 0.05 | 0.1 | Low-power I2C/SPI devices |
| - | Regulator losses | 5 | 10 | Buck + LDO inefficiency |
| **24V PSU Total** | | **~25W** | **~62W** | **Within 76.8W PSU capacity** |
| **System Total (incl. induction)** | | **~625W** | **~1,862W** | **Within 2kW limit** |

---

## 8. Microwave Induction Surface Module

### Module Integration

The microwave induction surface is a self-contained commercial module with its own AC power inlet, power electronics, induction coil, and onboard safety circuits. Epicura interfaces with the module exclusively via CAN bus — no high-voltage wiring touches the controller PCB.

```
┌──────────────────────────────────────────────────────────┐
│              Microwave Induction Surface                   │
│                                                            │
│  AC Mains ──► EMI Filter ──► Rectifier ──► Driver ──► Coil │
│                                                            │
│  Internal safety: pot detection, thermal cutoff,           │
│  overcurrent protection                                    │
│                                                            │
│  Exposed CAN Port:                                         │
│    CAN_H ──────────────────┐                               │
│    CAN_L ──────────────────┤                               │
│    GND ────────────────────┤                               │
└────────────────────────────┼───────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Driver PCB     │
                    │  ISO1050DUB     │
                    │  (5kV isolation)│
                    │  + 120Ω term   │
                    │  + J_CAN conn  │
                    └────────┬────────┘
                             │ J_STACK Pins 19-20
                    ┌────────▼────────┐
                    │  STM32 FDCAN1   │
                    │  PB8 (CAN_RX)  │
                    │  PB9 (CAN_TX)  │
                    └─────────────────┘

System Safety:
  - Module-internal: pot detection, thermal fuse, overcurrent (cannot be overridden)
  - System-level: safety relay on AC mains to module (STM32 GPIO ──► relay)
  - STM32 can send CAN off command or open relay on fault/E-stop
```

---

## 9. Ingredient Dispensing System (ASD / CID / SLD)

The dispensing system comprises three subsystems. See [[../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing System]] for full details.

### P-ASD — Pneumatic Seasoning Dispenser Wiring

```
  12V Rail (from Driver PCB MP1584EN #1)
  │
  ├──► Diaphragm Pump ◄── PA0 (TIM2_CH1) via J_STACK Pin 15, IRLML6344 MOSFET
  │
  ├──► Solenoid V1-V6 (6×) ◄── PCF8574 P0-P5 (I2C1, addr 0x20)
  │      PCF8574 on Driver PCB, gates drive IRLML6344 MOSFETs
  │
  I2C1 (PB6/PB7 via J_STACK Pins 35-36):
    ├── ADS1015 (0x48) — Accumulator pressure sensor
    └── PCF8574 (0x20) — Solenoid GPIO expander

  Note: P-ASD uses pneumatic puff-dosing (no servo gates or vibration motors)
```

### CID — Linear Actuator Wiring

```
  12V Rail (from Driver PCB MP1584EN #1)
  │
  ├──► CID-1 Linear Actuator (via DRV8876 #1 on Driver PCB)
  │      EN/PWM ◄── PA10 (TIM1_CH3) via J_STACK Pin 21
  │      PH/DIR ◄── PB4  (GPIO)     via J_STACK Pin 22
  │
  └──► CID-2 Linear Actuator (via DRV8876 #2 on Driver PCB)
         EN/PWM ◄── PB5  (GPIO)     via J_STACK Pin 23
         PH/DIR ◄── PC2  (GPIO)     via J_STACK Pin 24

  GND ──► Dedicated GND on J_STACK Pins 25-26 for CID subsystem

  Note: Limit switches not currently implemented (reserved J_STACK Pins 27-28)
```

### SLD — Liquid Dispensing Wiring

```
  12V Rail (from Driver PCB MP1584EN #1)
  │
  ├──► Peristaltic Pump (Oil) — TB6612 Channel A on Driver PCB
  │      PWMA ◄── PC3 (GPIO) via J_STACK Pin 29
  │      AIN1 ◄── PC4 (GPIO) via J_STACK Pin 30
  │
  ├──► Peristaltic Pump (Water) — TB6612 Channel B on Driver PCB
  │      PWMB ◄── PC5 (GPIO) via J_STACK Pin 31
  │      BIN1 ◄── PC6 (GPIO) via J_STACK Pin 32
  │
  ├──► Solenoid Valve (Oil)   ◄── PA7 (GPIO) via J_STACK Pin 33, MOSFET + flyback
  └──► Solenoid Valve (Water) ◄── PA9 (GPIO) via J_STACK Pin 34, MOSFET + flyback

  I2C for INA219 current monitor (on Driver PCB):
    SCL ◄── PB6 (I2C1_SCL) via J_STACK Pin 35
    SDA ◄── PB7 (I2C1_SDA) via J_STACK Pin 36

  SLD Load Cells (2× 2 kg, one per reservoir):
    HX711 #1 (oil):   SCK ◄── PC11 (GPIO), DOUT ──► PC12 (GPIO)
    HX711 #2 (water): SCK ◄── PC9  (GPIO), DOUT ──► PC10 (GPIO)
    Low-level alert when reservoir weight < configurable threshold
```

### Dispensing Summary

| Subsystem | Actuators | Metering | Min Dispense |
|-----------|-----------|----------|-------------|
| P-ASD (seasonings) | 1× diaphragm pump + 6× solenoid valve (PCF8574 I2C) | Pot load cells (±10%) | ~1 g |
| CID (coarse) | 2× linear actuator (DRV8876 drivers) | Position-based / user pre-measured | Full tray |
| SLD (liquids) | 2× peristaltic pump (TB6612) + 2× solenoid + 2× 2 kg load cell | Closed-loop via dedicated per-reservoir load cells + low-level alerts | ~5 g |
| Exhaust | 2× 120mm fans (independent PWM control) | Temperature/fume-based control | — |

**J_STACK Connector Organization:**
- **P-ASD**: Pin 15 (pump PWM); solenoids V1-V6 via PCF8574 on Driver PCB (I2C1, no J_STACK pins needed)
- **CAN**: Pins 19-20 (FDCAN1_RX/TX → Driver PCB ISO1050DUB → J_CAN)
- **CID**: Pins 21-26 (2× actuator EN/PH, 2× GND)
- **Exhaust Fans**: Pins 27-28 (FAN1 PWM, FAN2 PWM)
- **SLD**: Pins 29-36 (2× pump PWM/DIR, 2× solenoid, I2C for INA219)
- **Main**: Pins 37-40 (main servo, buzzer, reserved, GND)

---

## 10. WiFi / Bluetooth

### CM5 Onboard Wireless

The Raspberry Pi CM5 includes onboard WiFi and Bluetooth. No external modules are needed.

| Feature | Specification |
|---------|---------------|
| WiFi Standard | 802.11ac (WiFi 5), 2.4GHz + 5GHz dual-band |
| Max Throughput | Up to 867 Mbps (5GHz), 150 Mbps (2.4GHz) |
| Bluetooth | BLE 5.0 |
| Antenna | Onboard PCB antenna (or u.FL for external) |
| Security | WPA3, WPA2 |

### Wireless Use Cases

| Function | Protocol | Description |
|----------|----------|-------------|
| App Pairing | BLE 5.0 | Initial device discovery and WiFi credential transfer |
| Recipe Download | HTTPS | Fetch new recipes from cloud API |
| Live Camera Feed | RTSP/MJPEG | Stream camera to companion app (local WiFi) |
| Telemetry Upload | MQTT/HTTPS | Cooking session data to cloud (optional) |
| OTA Firmware Update | HTTPS + SWUpdate | CM5 OS/app and STM32 firmware updates |
| Remote Monitoring | WebSocket | Real-time status to app during cooking |
| NTP Time Sync | NTP (UDP) | Clock synchronization on boot |

### Antenna Considerations

- CM5 PCB antenna sufficient for typical kitchen distances (<10m)
- If mounted inside metal enclosure, route u.FL to external antenna on rear panel
- Keep antenna away from induction coil EMI (rear-top placement preferred)

---

## 11. Storage Architecture

### CM5 Storage

```
┌────────────────────────────────────────────────────────┐
│                   CM5 Storage Layout                   │
│                                                        │
│  ┌──────────────────┐    ┌──────────────────┐          │
│  │  eMMC (on-module)│    │  MicroSD Slot    │          │
│  │  8-16 GB         │    │  (carrier board) │          │
│  └────────┬─────────┘    └────────┬─────────┘          │
│           │                       │                    │
│  ┌────────▼─────────┐    ┌────────▼─────────┐          │
│  │  Partition Map:   │    │  Optional Use:   │          │
│  │                   │    │                   │          │
│  │  /boot   256MB    │    │  Recipe backup   │          │
│  │  /rootfs 4-8GB    │    │  Cooking logs    │          │
│  │  /data   4-8GB    │    │  User media      │          │
│  │  (recipes, logs,  │    │  Debug dumps     │          │
│  │   user prefs)     │    │                   │          │
│  └───────────────────┘    └───────────────────┘          │
│                                                        │
│  File Systems:                                         │
│  - /boot: FAT32 (CM5 bootloader requirement)           │
│  - /rootfs: ext4 (Yocto Linux root)                    │
│  - /data: ext4 (application data, wear-leveled)        │
│  - SD: FAT32 or ext4 (removable, user-accessible)     │
└────────────────────────────────────────────────────────┘
```

---

## PCB Layout Considerations

### Induction EMI Shielding

- The induction coil radiates strong magnetic fields at 20-40 kHz
- **Shielding:** Ferrite sheet between coil and electronics compartment
- **Distance:** Maintain minimum 50mm between coil and sensitive PCBs
- **Orientation:** Route I2C/SPI traces perpendicular to coil field lines
- **Grounding:** Copper ground pour on STM32 PCB, connected to chassis ground

### Sensor Signal Routing

- Keep I2C lines (MLX90614) short (<30cm), with 4.7k pull-ups near STM32
- HX711 clock/data lines: shielded twisted pair if >20cm, ground guard traces
- Camera CSI-2: differential pairs, matched length, <20cm FFC cable

### Power / Signal Ground Separation

```
┌─────────────────────────────────────────────────────┐
│                  Ground Architecture                 │
│                                                      │
│  AC Mains Earth ──────────────┐                      │
│                               │                      │
│  Chassis Ground ◄─────────────┤                      │
│  (metal enclosure)            │                      │
│                               │                      │
│  Power Ground ◄───────────────┤ (star connection)    │
│  (PSU output returns,         │                      │
│   induction power stage)      │                      │
│                               │                      │
│  Signal Ground ◄──────────────┘                      │
│  (CM5, STM32, sensors,                               │
│   low-current digital/analog)                        │
│                                                      │
│  Single-point star ground at PSU output              │
│  Ferrite bead between power GND and signal GND       │
└─────────────────────────────────────────────────────┘
```

### Thermal Relief

- Microwave surface module: internal cooling; ensure adequate ventilation around module
- STM32: thermal vias under exposed pad to ground plane
- CM5: passive heatsink (low-profile), adequate ventilation space
- PSU: ventilated enclosure area, thermal shutdown at 85C internal

---

## BOM Summary

### Prototype Bill of Materials

| Category | Component | Quantity | Est. Unit Cost (USD) | Est. Total (USD) |
|----------|-----------|----------|---------------------|-------------------|
| **Compute** | Raspberry Pi CM5 (4GB) | 1 | $45 | $45 |
| | CM5 IO Board (off-the-shelf) | 1 | $35 | $35 |
| | MicroSD 32GB | 1 | $10 | $10 |
| **MCU** | STM32G474RE Nucleo Board (proto) | 1 | $20 | $20 |
| | STM32G474RE IC (production) | 1 | $8 | $8 |
| **Display** | 10.1" IPS DSI/HDMI touchscreen | 1 | $60 | $60 |
| **Camera** | IMX219 CSI-2 module | 1 | $25 | $25 |
| | IMX477 HQ Camera (upgrade) | 1 | $50 | $50 |
| **Sensors** | MLX90614ESF-BAA (IR thermo) | 1 | $12 | $12 |
| | HX711 breakout board | 1 | $3 | $3 |
| | 5kg load cells | 4 | $4 | $16 |
| | Reed switch (pot detect — backup/optional) | 1 | $1 | $1 |
| **Actuators** | DS3225 25kg servo (main arm) | 1 | $20 | $20 |
| | SG90 micro servos (ASD gates) | 3 | $3 | $9 |
| | ERM vibration motors (ASD anti-clog) | 3 | $2 | $6 |
| | 12V DC linear actuators (CID) | 2 | $8 | $16 |
| | 12V peristaltic pumps (SLD) | 2 | $10 | $20 |
| | 12V NC solenoid valves (SLD) | 2 | $4 | $8 |
| | 120mm 12V DC brushless fans (exhaust) | 2 | $5 | $10 |
| | 5V piezo buzzer (active) | 1 | $2 | $2 |
| **Induction** | Microwave induction surface (CAN-enabled) | 1 | $60 | $60 |
| **Power** | Mean Well LRS-75-24 (24V/3.2A) | 1 | $20 | $20 |
| | IEC C14 inlet + EMI filter | 1 | $8 | $8 |
| | Safety relay (Omron G5V-2) | 1 | $5 | $5 |
| **Misc** | WS2812B LED ring (16 LEDs) | 1 | $5 | $5 |
| | E-Stop mushroom button | 1 | $4 | $4 |
| | CAN transceiver (for FDCAN1) | 1 | $3 | $3 |
| | Passive components (R, C, etc.) | Lot | - | $20 |
| | Custom PCBs (4-layer, 2 boards) | 1 set | $40 | $40 |
| | Wiring, connectors, FFC cables | Lot | - | $25 |
| **Enclosure** | 3D-printed enclosure (prototype) | 1 | $80 | $80 |
| | Pot (off-shelf induction-compatible) | 1 | $25 | $25 |
| | Gantry hardware (rods, brackets) | Lot | - | $30 |

**Estimated Prototype BOM Total: $700 - $800 USD**

*Note: Production BOM would be lower per unit at volume. Prototype uses Nucleo dev board that would be replaced with bare STM32G474RE on the controller PCB. The CM5 IO Board is used as-is (off-the-shelf) in both prototype and production.*

---

## Hardware Validation Checklist

### Power Supply
- [ ] Verify 24V rail from Mean Well PSU within spec (24V +/-5%)
- [ ] Measure ripple on each rail (<50mV peak-to-peak)
- [ ] Load test at full power (microwave surface 1800W + all subsystems)
- [ ] Verify standby power <5W
- [ ] Test EMI filter effectiveness (conducted emissions)
- [ ] Verify fuse blows at rated overcurrent

### Compute (CM5)
- [ ] CM5 boots Yocto Linux from eMMC
- [ ] SPI communication to STM32 (loopback test, then bidirectional)
- [ ] Camera captures 1080p/30fps frames via CSI-2
- [ ] Display renders UI via DSI/HDMI
- [ ] Touch input registers on all screen areas
- [ ] WiFi connects to AP, achieves >10 Mbps throughput
- [ ] BLE advertises and pairs with test phone
- [ ] eMMC read/write speed adequate (>50 MB/s sequential)

### Microwave Induction Surface
- [ ] Module responds to CAN queries (HEAT_QUERY → HEAT_STATUS)
- [ ] CAN power level commands correctly modulate heating
- [ ] Module heats water from 20C to 100C within 5 minutes (1.5L)
- [ ] PID holds temperature within +/-5C of setpoint
- [ ] All four power profiles (sear/boil/simmer/warm) verified
- [ ] Module-internal pot detection prevents heating without pot
- [ ] Safety relay disconnects AC to module on E-stop or fault
- [ ] CAN off command stops heating within 500ms

### Servo System
- [ ] Main arm (DS3225) rotates full 360 degrees smoothly
- [ ] Stirring speed controllable from 10-60 RPM
- [ ] Arm torque sufficient to stir thick curry/dal
- [ ] Each ASD gate servo (SG90) opens/closes reliably
- [ ] ASD gate servos hold closed position under seasoning weight
- [ ] No servo jitter at idle (proper PWM signal quality)

### Sensors
- [ ] Camera: white balance calibrated, image sharp across full pot FOV
- [ ] IR (MLX90614): reads boiling water as 98-102C
- [ ] IR: reads room temp object within +/-1C of reference thermometer
- [ ] Load cells: tare on boot, measure 500g calibration weight within +/-5g
- [ ] Load cells: track water evaporation over 30-minute simmer
- [ ] Pot detection: reliably detects pot on/off

### Dispensing (ASD / CID / SLD)
- [ ] ASD: Each hopper dispenses 5g powder within ±10%
- [ ] ASD: Vibration motors (3x) activate before dispense (200ms pulse)
- [ ] ASD: Anti-clog retry mechanism clears blockages within 2 attempts
- [ ] CID: Linear actuators (DRV8876) push full tray contents into pot
- [ ] CID: Actuators return to home position reliably
- [ ] SLD: Each pump (TB6612) dispenses 50g liquid within ±5%
- [ ] SLD: Solenoid valves seal (no drips when idle)
- [ ] Both exhaust fans: PWM control from 0-100%, no audible whine
- [ ] Both exhaust fans: Independent control verified (each can run separately)
- [ ] Buzzer: All alert patterns audible and distinct
- [ ] No cross-contamination between subsystems
- [ ] J_STACK connector: All subsystem pins connected correctly

---

## Safety Considerations

### Electrical Safety

- **Galvanic Isolation:** The microwave induction surface is a self-contained AC module — no mains voltage reaches the controller or driver PCBs. The ISO1050DUB isolated CAN transceiver on the Driver PCB provides 5 kV RMS galvanic isolation between the CAN bus and STM32 logic. PSU provides transformer-isolated DC outputs.
- **Earth Bonding:** Metal enclosure parts connected to AC earth via IEC C14 inlet. Chassis ground bonded to PSU earth.
- **Fuse Protection:** 10A ceramic fuse in IEC C14 inlet. Self-resetting PTC fuse on 5V rail (3A).

### Thermal Safety

- **Module Thermal:** Microwave surface has internal thermal cutoff. Module reports coil temperature via CAN status.
- **Food Over-Temperature:** IR thermometer monitors food surface. If >270C (beyond any recipe requirement), STM32 sends CAN off command and opens safety relay.
- **Enclosure Thermal:** Exhaust fan provides ventilation. Module reports internal temp via CAN for enclosure monitoring.

### Mechanical Safety

- **E-Stop Button:** Red mushroom-head button on front panel. Normally-closed contact wired to STM32 interrupt AND safety relay. Pressing E-stop: (1) STM32 sends CAN off to module, (2) relay disconnects AC to microwave surface, (3) servos return to safe position.
- **Pot Detection Interlock:** Handled internally by microwave surface module. Module will not heat without compatible pot detected. Status reported via CAN.
- **Pinch Protection:** Arm mechanism has limited torque (DS3225 stall current fused). Arm speed limited in firmware to prevent splash/injury.

### Overcurrent Protection

- **Mains:** 10A fuse (IEC C14)
- **DC Rails:** PTC self-resetting fuses on each rail
- **Induction Module:** Internal overcurrent protection (module-handled)
- **Servos:** Individual PTC fuses or current-limited driver

---

## Related Documentation

- [[02-Technical-Specifications|Technical Specifications]]
- [[05-Sensors-Acquisition|Sensors & Data Acquisition]]
- [[07-Mechanical-Design|Mechanical Design]]
- [[../09-PCB/Controller-PCB-Design|Controller PCB Design]]
- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../03-Software/08-Tech-Stack|Tech Stack]]
- [[../07-Development/Prototype-Development-Plan|Prototype Development Plan]]

---

#epicura #hardware-architecture #wiring #system-design

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-20 | Manas Pradhan | Updated CAN bus architecture: ISO1050DUB transceiver and J_CAN connector moved from Controller PCB to Driver PCB; FDCAN1 logic signals route via J_STACK pins 19-20; updated block diagrams, wiring, safety notes, and J_STACK organization |
