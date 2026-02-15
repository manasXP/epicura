---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Controller PCB Design

## Overview

This document covers the design of the custom controller PCB for Epicura. This board hosts the STM32G474RE microcontroller and all its peripheral interfaces — sensor inputs, PWM outputs for actuators, SPI communication to the CM5, and safety circuits.

### Scope

| Item | Status | Notes |
|------|--------|-------|
| **Controller PCB** (this document) | Custom design required | STM32G474RE + peripherals, 160x90mm |
| **Driver PCB** | Custom design required | Power conversion + actuator drivers (see [[Driver-PCB-Design]]) |
| **CM5 IO Board (CMIO)** | Custom design required | CM5 carrier board, 160x90mm to match stack |
| **Microwave induction surface** | Commercial module with CAN port (see [[../05-Subsystems/09-Induction-Heating\|Induction Heating]]) | Self-contained coil + driver; controlled via CAN bus |

The three boards (CMIO, Controller, Driver) form a stackable architecture connected via 2x20-pin 2.54mm board-to-board headers, all sharing a uniform 160x90mm footprint. The Controller PCB sits in the middle of the stack — it connects upward to the CMIO board via SPI (J1) and downward to the Driver PCB via a stacking connector (J_STACK). All real-time control, sensor acquisition, and safety monitoring runs on this controller board. Servo PWM and actuator GPIO signals pass through J_STACK to the Driver PCB where power electronics drive the actual actuators.

---

## Board-Level Block Diagram

```
                        5V from PSU
                            │
                     ┌──────▼──────┐
                     │  3.3V LDO   │
                     │ AMS1117-3.3 │
                     └──────┬──────┘
                            │ 3.3V
         ┌──────────────────┼──────────────────────────────┐
         │                  │                              │
         │    ┌─────────────▼─────────────┐                │
         │    │      STM32G474RE          │                │
         │    │       (LQFP-64)           │                │
         │    │                           │                │
         │    │  SPI2 ◄─────────────────────── J1: SPI to CM5
         │    │  PB3 (IRQ) ────────────────── J1: IRQ to CM5
         │    │                           │                │
         │    │  FDCAN1 (PB8/PB9) ─────────── J2: CAN to Microwave Surface
         │    │                           │                │
         │    │  TIM1_CH1 (PA8) ───────────── J3: DS3225 Servo
         │    │                           │                │
         │    │  TIM2_CH1-3 (PA0-PA2) ─────── J_STACK: ASD Servos 1-3
         │    │  PA3/PC7/PD2 ─────────────── J_STACK: ASD Vibration Motors
         │    │                           │                │
         │    │  I2C1 (PB6/PB7) ───────────── J6: MLX90614
         │    │                           │                │
         │    │  GPIO (PC0/PC1) ───────────── J7: HX711
         │    │                           │                │
         │    │  ADC2 (PA4/PA5) ───────────── J8: NTC Inputs
         │    │                           │                │
         │    │  GPIO (PB0) ───────────────── Q1: Safety Relay Driver
         │    │  GPIO (PB1) ◄──────────────── SW1: Pot Detection
         │    │  GPIO (PB2) ◄──────────────── SW2: E-Stop
         │    │                           │                │
         │    │  SWD (PA13/PA14) ──────────── J9: Debug Header
         │    │                           │                │
         │    │  PC13 ─────────────────────── D1: Status LED
         │    │                           │                │
         │    └───────────────────────────┘                │
         │                                                 │
         │    ┌───────────────┐   ┌──────────────────┐    │
         │    │ 8 MHz HSE     │   │ 32.768 kHz LSE   │    │
         │    │ Crystal       │   │ Crystal           │    │
         │    └───────────────┘   └──────────────────┘    │
         └─────────────────────────────────────────────────┘
```

---

## STM32G474RE Pin Allocation

### Pin Map (LQFP-64)

```
STM32G474RE (LQFP-64) — Controller PCB Pin Assignment
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ┌─── SPI2: CM5 Communication (Master=CM5, Slave=STM32) ──┐  │
│  │  PB12 (SPI2_NSS)  ◄── CM5 GPIO8 (CE0)                  │  │
│  │  PB13 (SPI2_SCK)  ◄── CM5 GPIO11 (SCLK)                │  │
│  │  PB14 (SPI2_MISO) ──► CM5 GPIO9 (MISO)                 │  │
│  │  PB15 (SPI2_MOSI) ◄── CM5 GPIO10 (MOSI)                │  │
│  │  PB3  (GPIO IRQ)  ──► CM5 GPIO4 (data-ready, act-low)  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─── CAN: Microwave Surface ─────┐                           │
│  │  PB8  (FDCAN1_RX) ◄── CAN transceiver RXD               │  │
│  │  PB9  (FDCAN1_TX) ──► CAN transceiver TXD               │  │
│  │  500 kbps, 120Ω termination on J2                         │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── PWM: Main Servo Arm ────────┐                           │
│  │  PA8  (TIM1_CH1)  ──► DS3225 Signal (orange wire)         │  │
│  │  50 Hz, 500-2500 us pulse width                            │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── PWM: ASD Seasoning Servos ──┐                           │
│  │  PA0  (TIM2_CH1)  ──► ASD-1 SG90 Signal                  │  │
│  │  PA1  (TIM2_CH2)  ──► ASD-2 SG90 Signal                  │  │
│  │  PA2  (TIM2_CH3)  ──► ASD-3 SG90 Signal                  │  │
│  │  50 Hz, 500-2500 us pulse width                            │  │
│  └─────────────────────────────────┘                           │
│  Note: All actuator signals (servos, pumps, solenoids,        │
│  vibration motors) route via J_STACK to Driver PCB where      │
│  power electronics drive the actual actuators.                 │
│                                                                │
│  ┌─── I2C1: IR Thermometer ───────┐                           │
│  │  PB6  (I2C1_SCL) ──► MLX90614 SCL                        │  │
│  │  PB7  (I2C1_SDA) ◄─► MLX90614 SDA                        │  │
│  │  100 kHz, 4.7k pull-ups to 3.3V                           │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Load Cells (HX711) ───┐                           │
│  │  PC0  (GPIO)      ──► HX711 SCK (clock out)              │  │
│  │  PC1  (GPIO)      ◄── HX711 DOUT (data in)               │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── ADC: NTC Thermistors ───────┐                           │
│  │  PA4  (ADC2_IN17) ◄── NTC Coil divider midpoint          │  │
│  │  PA5  (ADC2_IN13) ◄── NTC Ambient divider midpoint       │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Safety & Control ─────┐                           │
│  │  PB0  (GPIO)      ──► Safety Relay (via MOSFET Q1)        │  │
│  │  PB1  (GPIO)      ◄── Pot Detection (reed switch)        │  │
│  │  PB2  (GPIO)      ◄── E-Stop Button (EXTI, active-low)   │  │
│  │  PC13 (GPIO)      ──► Status LED (green, active-low)     │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Reserved / Unused ──────────┐                           │
│  │  PA9  (GPIO)      ── Available (was USART1_TX)            │  │
│  │  PA10 (GPIO)      ── Available (was USART1_RX)            │  │
│  │  PA11 (USB_DM)    ── Reserved for USB (future)            │  │
│  │  PA12 (USB_DP)    ── Reserved for USB (future)            │  │
│  │  PB4  (GPIO)      ── Available                            │  │
│  │  PB5  (GPIO)      ── Available                            │  │
│  │  PB8  (FDCAN1_RX)  ── CAN RX to microwave surface         │  │
│  │  PB9  (FDCAN1_TX)  ── CAN TX to microwave surface         │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  Debug: SWD via PA13 (SWDIO) / PA14 (SWCLK)                  │
│  Power: 3.3V / GND from on-board LDO                         │
│  Clock: 8 MHz HSE (OSC_IN PA0-alt / PF0, PF1)               │
│  Clock: 32.768 kHz LSE (PC14, PC15) for RTC                 │
│  Reset: NRST with 100nF cap + external reset button          │
│  BOOT0: Tied low via 10k pull-down (jumper for bootloader)   │
└────────────────────────────────────────────────────────────────┘
```

### Pin Summary Table

| Pin | Function | Peripheral | Direction | Connector | Subsystem |
|-----|----------|------------|-----------|-----------|-----------|
| PA0 | TIM2_CH1 | ASD Servo 1 PWM | Output | J_STACK Pin 15 | ASD |
| PA1 | TIM2_CH2 | ASD Servo 2 PWM | Output | J_STACK Pin 16 | ASD |
| PA2 | TIM2_CH3 | ASD Servo 3 PWM | Output | J_STACK Pin 17 | ASD |
| PA3 | GPIO | ASD Vibration Motor 3 | Output | J_STACK Pin 20 | ASD |
| PA4 | ADC2_IN17 | NTC Coil | Input | J8 | Sensors |
| PA5 | ADC2_IN13 | NTC Ambient | Input | J8 | Sensors |
| PA6 | TIM3_CH1 | Exhaust Fan 1 PWM | Output | J_STACK Pin 27 | Exhaust |
| PA7 | GPIO | SLD Solenoid 1 Enable | Output | J_STACK Pin 33 | SLD |
| PA8 | TIM1_CH1 | Main Servo (DS3225) | Output | J_STACK Pin 37 | Main |
| PA9 | GPIO | SLD Solenoid 2 Enable | Output | J_STACK Pin 34 | SLD |
| PA10 | TIM1_CH3/GPIO | CID Linear Actuator 1 EN | Output | J_STACK Pin 21 | CID |
| PA11 | TIM1_CH4 | Buzzer PWM | Output | J_STACK Pin 39 | Main |
| PA13 | SWDIO | SWD Debug | Bidir | J9 | Debug |
| PA14 | SWCLK | SWD Debug | Input | J9 | Debug |
| PB0 | GPIO | Safety Relay | Output | Q1 | Safety |
| PB1 | GPIO | Pot Detection | Input | SW1 | Safety |
| PB2 | GPIO (EXTI) | E-Stop | Input | SW2 | Safety |
| PB3 | GPIO | IRQ to CM5 | Output | J1 | Comms |
| PB4 | GPIO | CID Linear Actuator 1 PH | Output | J_STACK Pin 22 | CID |
| PB5 | GPIO | CID Linear Actuator 2 EN | Output | J_STACK Pin 23 | CID |
| PB6 | I2C1_SCL | MLX90614/INA219 | Output | J6, J_STACK Pin 35 | Sensors |
| PB7 | I2C1_SDA | MLX90614/INA219 | Bidir | J6, J_STACK Pin 36 | Sensors |
| PB10 | TIM2_CH3 | Exhaust Fan 2 PWM | Output | J_STACK Pin 28 | Exhaust |
| PB11 | Available | — | — | — | — |
| PB12 | SPI2_NSS | CM5 CE0 | Input | J1 | Comms |
| PB13 | SPI2_SCK | CM5 SCLK | Input | J1 | Comms |
| PB14 | SPI2_MISO | CM5 MISO | Output | J1 | Comms |
| PB15 | SPI2_MOSI | CM5 MOSI | Input | J1 | Comms |
| PC0 | GPIO | HX711 SCK (pot) | Output | J7 | Sensors |
| PC1 | GPIO | HX711 DOUT (pot) | Input | J7 | Sensors |
| PC2 | GPIO | CID Linear Actuator 2 PH | Output | J_STACK Pin 24 | CID |
| PC3 | GPIO | SLD Pump 1 PWM | Output | J_STACK Pin 29 | SLD |
| PC4 | GPIO | SLD Pump 1 DIR | Output | J_STACK Pin 30 | SLD |
| PC5 | GPIO | SLD Pump 2 PWM | Output | J_STACK Pin 31 | SLD |
| PC6 | GPIO | SLD Pump 2 DIR | Output | J_STACK Pin 32 | SLD |
| PC7 | GPIO | ASD Vibration Motor 1 | Output | J_STACK Pin 18 | ASD |
| PC13 | GPIO | Status LED | Output | D1 | Status |
| PD2 | GPIO | ASD Vibration Motor 2 | Output | J_STACK Pin 19 | ASD |

---

## Power Supply

### Input

The controller PCB receives 5V DC from the CMIO board's 40-pin GPIO connector (pins 2/4: 5V, pins 6/9/14/20/25/30/34/39: GND). A 3.3V LDO regulates this down for the STM32 and all 3.3V peripherals. No onboard buck converter is needed — the CMIO board handles 24V→5V regulation from the Mean Well PSU.

### Regulator Circuit

```
5V from CMIO 40-pin (pins 2,4)
    │
    ├──── C1: 10uF ceramic (input bypass)
    │
    ▼
┌──────────────────┐
│  U2: AMS1117-3.3 │
│  or AP2112K-3.3  │
│                  │
│  VIN ◄── 5V      │
│  VOUT ──► 3.3V   │
│  GND ──► GND     │
│                  │
│  Dropout: 1.0V   │
│  Iout max: 800mA │
└──────────────────┘
    │
    ├──── C2: 10uF ceramic (output bypass)
    ├──── C3: 100nF ceramic (high-freq decoupling)
    │
    ▼
3.3V Rail ──► STM32 VDD, VDDA, sensors, pull-ups
```

### Power Budget (Controller PCB Only)

| Consumer | Typical (mA) | Peak (mA) | Notes |
|----------|-------------|----------|-------|
| STM32G474RE | 80 | 150 | All peripherals active |
| MLX90614 | 1.5 | 2 | I2C, continuous measurement |
| HX711 | 1.5 | 2 | 10 Hz mode |
| I2C pull-ups (2x 4.7k) | 1.4 | 1.4 | At 3.3V |
| NTC dividers (2x 100k) | 0.07 | 0.07 | Negligible |
| Status LED | 5 | 10 | Via 330 ohm resistor |
| **Total 3.3V** | **~90** | **~166** | Well within LDO capacity |

> [!note]
> Servo motors (DS3225, SG90) are powered from a separate 24V→5V buck converter on the servo rail, not from this 3.3V LDO. Only the PWM signal lines route through the controller PCB.

### Decoupling

- **Per VDD pin:** 100nF MLCC placed within 5mm of each VDD/VSS pin pair
- **VDDA (analog supply):** 1uF MLCC + ferrite bead from main 3.3V
- **Bulk:** 10uF MLCC at LDO output, 10uF MLCC at LDO input
- **Total decoupling caps:** 6-8x 100nF + 2x 10uF + 1x 1uF

---

## CM5 to STM32 SPI Interface

### Physical Connection

The CM5 IO Board's GPIO header connects to J1 on the controller PCB via a 7-wire ribbon cable or JST-SH connector.

```
CM5 IO Board (GPIO Header)              Controller PCB (J1)
┌───────────────────────┐                ┌───────────────────────┐
│                       │                │                       │
│  GPIO8  (CE0)   Pin 24├───────────────►│Pin 1  PB12 (SPI2_NSS)│
│  GPIO9  (MISO)  Pin 21│◄──────────────┤Pin 2  PB14 (SPI2_MISO)│
│  GPIO10 (MOSI)  Pin 19├───────────────►│Pin 3  PB15 (SPI2_MOSI)│
│  GPIO11 (SCLK)  Pin 23├───────────────►│Pin 4  PB13 (SPI2_SCK)│
│  GPIO4  (IRQ)   Pin  7│◄──────────────┤Pin 5  PB3  (IRQ)     │
│  GND            Pin 25├───────────────►│Pin 6  GND            │
│  3.3V           Pin  1├───── (N/C) ───┤       (not connected) │
│                       │                │                       │
└───────────────────────┘                └───────────────────────┘

Cable: 7-wire flat ribbon or JST-SH, length <30cm
Logic level: 3.3V on both sides (no level shifter needed)
```

### SPI Configuration

| Parameter | Value |
|-----------|-------|
| Role | CM5 = Master, STM32 = Slave |
| Clock Speed | 2 MHz (sufficient for command/telemetry traffic) |
| SPI Mode | Mode 0 (CPOL=0, CPHA=0) |
| Data Width | 8-bit |
| Byte Order | MSB first |
| NSS Management | Hardware (active-low, driven by CM5 CE0) |
| DMA | Enabled on STM32 SPI2 RX and TX |
| IRQ Line | PB3 → CM5 GPIO4, active-low, pulse 10us |

### Why SPI Over UART

| Criteria | SPI | UART |
|----------|-----|------|
| Throughput | 2 Mbps (16 MHz max) | 115.2 kbps typical |
| Duplex | Full duplex (simultaneous TX/RX) | Full duplex (but half in practice) |
| Clocking | Synchronous (no baud mismatch) | Asynchronous (requires matching baud) |
| DMA efficiency | Excellent (continuous clocked transfer) | Good (byte-at-a-time interrupts) |
| Wires | 5 (MOSI, MISO, SCK, NSS, IRQ) | 3 (TX, RX, GND) |
| Error rate | Lower (clocked, no framing errors) | Higher at speed (noise-sensitive) |

### SPI Transaction Protocol

The CM5 (master) initiates all SPI transactions. The STM32 (slave) asserts the IRQ line low to signal that it has telemetry or event data ready for the CM5 to read.

**Transaction format (both directions):**

```
┌──────┬────────┬─────────┬───────────────┬──────────┐
│ TYPE │ MSG_ID │ LENGTH  │   PAYLOAD     │  CRC-16  │
│1 byte│ 1 byte │ 1 byte  │  0-60 bytes   │ 2 bytes  │
└──────┴────────┴─────────┴───────────────┴──────────┘
```

**Command flow (CM5 → STM32):**
1. CM5 asserts NSS low
2. CM5 clocks out command frame on MOSI
3. STM32 simultaneously clocks out last-prepared response on MISO (or 0x00 padding if no data)
4. CM5 deasserts NSS high
5. STM32 processes command, prepares response, pulses IRQ if needed

**Event flow (STM32 → CM5):**
1. STM32 prepares telemetry/event frame in TX buffer
2. STM32 asserts IRQ low (10us pulse)
3. CM5 detects IRQ on GPIO4 interrupt
4. CM5 initiates SPI read transaction (sends dummy bytes on MOSI, reads response on MISO)
5. STM32 deasserts IRQ after data is clocked out

### Message Types

| Message | Type Code | Direction | Payload |
|---------|-----------|-----------|---------|
| SET_TEMP | 0x01 | CM5 → STM32 | target_temp (float), ramp_rate (float) |
| SET_STIR | 0x02 | CM5 → STM32 | pattern (uint8), speed_rpm (uint16) |
| DISPENSE_ASD | 0x03 | CM5 → STM32 | asd_id (uint8: 1-3), target_g (uint16) |
| DISPENSE_CID | 0x06 | CM5 → STM32 | cid_id (uint8: 1-2), mode (uint8), pos_mm (uint8) |
| DISPENSE_SLD | 0x07 | CM5 → STM32 | channel (uint8: OIL=1, WATER=2), target_g (uint16) |
| E_STOP | 0x04 | CM5 → STM32 | reason_code (uint8) |
| HEARTBEAT | 0x05 | Bidirectional | uptime_ms (uint32) |
| TELEMETRY | 0x10 | STM32 → CM5 | ir_temp, ntc_temps, weight, duty_pct |
| SENSOR_DATA | 0x11 | STM32 → CM5 | adc_values[], ir_temp, load_cells[] |
| STATUS | 0x12 | STM32 → CM5 | safety_state, error_code, flags |
| ACK | 0xFF | Bidirectional | ack_msg_id, result_code |

### STM32 SPI Slave Implementation Notes

- Configure SPI2 in slave mode with hardware NSS
- Use DMA for both TX and RX to avoid CPU overhead
- Double-buffer TX: while one buffer is being transmitted, the next telemetry frame is prepared in the other
- IRQ line driven by GPIO output (PB3), not tied to SPI hardware
- Timeout: if CM5 does not read within 500ms of IRQ assertion, STM32 enters WARNING state

---

## Connector Definitions

### J1 — SPI to CM5 (JST-SH 1.0mm, 6-pin)

| Pin | Signal | STM32 Pin | Direction |
|-----|--------|-----------|-----------|
| 1 | NSS | PB12 | In (from CM5) |
| 2 | MISO | PB14 | Out (to CM5) |
| 3 | MOSI | PB15 | In (from CM5) |
| 4 | SCK | PB13 | In (from CM5) |
| 5 | IRQ | PB3 | Out (to CM5) |
| 6 | GND | GND | — |

### J2 — CAN Bus to Microwave Surface (JST-XH 2.5mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | CAN_H | via CAN transceiver | CAN bus high |
| 2 | CAN_L | via CAN transceiver | CAN bus low |
| 3 | GND | GND | Common ground |
| 4 | +5V (optional) | — | Transceiver power (if needed by module) |

> [!note]
> STM32 FDCAN1 pins PB8 (RX) and PB9 (TX) connect to a CAN transceiver IC (SN65HVD230 or MCP2551) on the controller PCB. The transceiver drives CAN_H/CAN_L to J2. 120Ω termination resistor on-board.

### J6 — MLX90614 I2C (JST-SH 1.0mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | SCL | PB6 (I2C1_SCL) | 4.7k pull-up on board |
| 2 | SDA | PB7 (I2C1_SDA) | 4.7k pull-up on board |
| 3 | VCC | 3.3V | — |
| 4 | GND | GND | — |

### J7 — HX711 Load Cell ADC (JST-XH 2.5mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | SCK | PC0 (GPIO) | Clock output to HX711 |
| 2 | DOUT | PC1 (GPIO) | Data input from HX711 |
| 3 | VCC | 3.3V | HX711 supply |
| 4 | GND | GND | — |

### J8 — NTC Thermistor Inputs (JST-XH 2.5mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | NTC_COIL | PA4 (ADC2_IN17) | Voltage divider midpoint |
| 2 | NTC_AMB | PA5 (ADC2_IN13) | Voltage divider midpoint |
| 3 | 3.3V | 3.3V | Top of voltage dividers |
| 4 | GND | GND | — |

### J9 — SWD Debug (10-pin 1.27mm Cortex Debug or 6-pin TagConnect)

| Pin | Signal | STM32 Pin |
|-----|--------|-----------|
| 1 | VCC | 3.3V |
| 2 | SWDIO | PA13 |
| 3 | SWCLK | PA14 |
| 4 | SWO | PB3 (shared with IRQ — select via solder jumper) |
| 5 | NRST | NRST |
| 6 | GND | GND |

> [!note]
> PB3 is shared between SPI IRQ and SWD SWO. A solder jumper (SJ1) selects between the two. Default position: IRQ. Set to SWO for debug tracing only.

### J10 — Power Input (JST-XH 2.5mm, 2-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | +5V | From PSU 5V rail |
| 2 | GND | Power ground |

### J11 — Safety I/O (JST-XH 2.5mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | RELAY_DRV | PB0 via Q1 | Drives safety relay coil |
| 2 | POT_DET | PB1 | Reed switch input, 10k pull-up |
| 3 | E_STOP | PB2 | NC button, 10k pull-up, RC debounce |
| 4 | GND | GND | — |

### J_STACK — Stacking Connector to Driver PCB (2x20 pin header, 2.54mm, 11mm stacking height)

The stacking connector passes 24V power, ground, 5V/3.3V references, all servo PWM signals, actuator GPIO signals, and I2C (for INA219 current monitor) down to the Driver PCB. Pins are organized by subsystem for cleaner wiring harnesses. See [[Driver-PCB-Design#Stacking Connector — J_STACK]] for the full 40-pin pinout.

#### J_STACK Pinout (Top View — Controller PCB Side)

| Pin | Signal | Direction | Pin | Signal | Direction |
|-----|--------|-----------|-----|--------|-----------|
| 1 | 24V_IN | Power Out | 2 | 24V_IN | Power Out |
| 3 | 24V_IN | Power Out | 4 | 24V_IN | Power Out |
| 5 | GND | Power | 6 | GND | Power |
| 7 | GND | Power | 8 | GND | Power |
| 9 | GND | Power | 10 | GND | Power |
| 11 | 5V | Power | 12 | 5V | Power |
| 13 | 3.3V | Power | 14 | 3.3V | Power |
| **ASD Subsystem (Pins 15-20)** ||||
| 15 | ASD_SERVO1_PWM (PA0) | Out | 16 | ASD_SERVO2_PWM (PA1) | Out |
| 17 | ASD_SERVO3_PWM (PA2) | Out | 18 | ASD_VIB1_EN (PC7) | Out |
| 19 | ASD_VIB2_EN (PD2) | Out | 20 | ASD_VIB3_EN (PA3) | Out |
| **CID Subsystem (Pins 21-26)** ||||
| 21 | CID_LACT1_EN (PA10) | Out | 22 | CID_LACT1_PH (PB4) | Out |
| 23 | CID_LACT2_EN (PB5) | Out | 24 | CID_LACT2_PH (PC2) | Out |
| 25 | GND | Power | 26 | GND | Power |
| **Exhaust Fans (Pins 27-28)** ||||
| 27 | FAN1_PWM (PA6) | Out | 28 | FAN2_PWM (PB10) | Out |
| **SLD Subsystem (Pins 29-36)** ||||
| 29 | SLD_PUMP1_PWM (PC3) | Out | 30 | SLD_PUMP1_DIR (PC4) | Out |
| 31 | SLD_PUMP2_PWM (PC5) | Out | 32 | SLD_PUMP2_DIR (PC6) | Out |
| 33 | SLD_SOL1_EN (PA7) | Out | 34 | SLD_SOL2_EN (PA9) | Out |
| 35 | I2C1_SCL (PB6) | Bidir | 36 | I2C1_SDA (PB7) | Bidir |
| **Main Actuators & Audio (Pins 37-40)** ||||
| 37 | MAIN_SERVO_PWM (PA8) | Out | 38 | BUZZER_PWM (PA11) | Out |
| 39 | Reserved | — | 40 | GND | Power |

#### Pin Group Summary

| Group | Pins | Count | Purpose |
|-------|------|-------|---------|
| 24V Power | 1-4 | 4 | 24V from PSU (paralleled for 12A capacity) |
| GND | 5-10, 25-26, 40 | 9 | Low-impedance ground return |
| 5V | 11-12 | 2 | 5V passthrough |
| 3.3V | 13-14 | 2 | Logic reference |
| **ASD** (Seasoning) | 15-20 | 6 | 3× servo PWM, 3× vibration motor enable |
| **CID** (Coarse) | 21-26 | 6 | 2× actuator EN/PH, 2× GND |
| **Exhaust Fans** | 27-28 | 2 | 2× fan PWM (independent speed control, 120mm) |
| **SLD** (Liquid) | 29-36 | 8 | 2× pump PWM/DIR, 2× solenoid, I2C (INA219) |
| **Main** (Arm/Audio) | 37-40 | 4 | Main servo, buzzer, 1× reserved, 1× GND |

> [!note]
> Subsystem grouping enables modular wiring harnesses. All signals for ASD run together (pins 15-20), all CID signals together (21-28), etc. Servo and actuator external connectors are on the Driver PCB, not the Controller PCB. The Controller PCB only carries low-level PWM/GPIO signals.

---

## Protection Circuits

### ESD Protection

- TVS diode array (e.g., PRTR5V0U2X) on J1 SPI lines
- TVS diodes on J11 safety inputs (E-stop, pot detection)
- All external connectors have series 33 ohm resistors on signal lines

### Relay Driver (Q1)

```
PB0 ────┤ 330R ├──── Gate ┐
                           │
                     ┌─────▼─────┐
                     │  Q1: 2N7002│
                     │  (N-MOSFET)│
                     └─────┬─────┘
                           │ Drain
                     ┌─────▼─────┐
                     │ Relay Coil │ ◄── 5V or 12V
                     │ (Omron G5V)│
                     └─────┬─────┘
                           │
                      D1 (1N4148) ◄── Flyback diode across coil
                           │
                          GND
```

### E-Stop Input

```
E-Stop Button (NC)
    │
    ├──── R: 10k pull-up to 3.3V
    │
    ├──── C: 100nF to GND (RC debounce, tau ~1ms)
    │
    └──── PB2 (EXTI, falling edge interrupt)

Button pressed → PB2 goes LOW → immediate interrupt
Button released (or wire break) → PB2 stays LOW → fail-safe
```

### Pot Detection Input

```
Reed Switch (NO)
    │
    ├──── R: 10k pull-up to 3.3V
    │
    └──── PB1 (GPIO input)

Pot present → magnet closes reed → PB1 = LOW
Pot absent → reed open → PB1 = HIGH (pulled up)
```

### ADC Input Filtering (NTC Channels)

```
NTC Thermistor ──┬── R_pull (100k to 3.3V)
                 │
                 ├── R_filter (10k)──┬── PA4 or PA5 (ADC input)
                 │                   │
                 │                   C_filter (100nF to GND)
                 │
                GND

RC filter cutoff: 1 / (2π × 10k × 100nF) ≈ 160 Hz
Sufficient to attenuate induction EMI at 20-40 kHz
```

---

## PCB Stackup and Layout

### 4-Layer Stackup

```
┌──────────────────────────────────────────────┐
│  Layer 1 (Top)    — Signal + Components       │  35um Cu
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 2 (Inner1) — GND Plane (continuous)    │  35um Cu
├──────────────────────────────────────────────┤
│  Core             — FR4, 0.8mm               │
├──────────────────────────────────────────────┤
│  Layer 3 (Inner2) — 3.3V Power Plane          │  35um Cu
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 4 (Bottom) — Signal + Components       │  35um Cu
└──────────────────────────────────────────────┘

Total thickness: ~1.6mm (standard)
Material: FR4 (Tg 150°C minimum)
```

### Layout Guidelines

**Component Placement Zones:**

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────┐  │
│  │   STM32G474RE  │  │  SPI + Debug   │  │  Power    │  │
│  │   + Crystal    │  │  Connectors    │  │  LDO +    │  │
│  │   + Decoupling │  │  (J1, J9)      │  │  Input    │  │
│  │                │  │                │  │  (J10)    │  │
│  │  DIGITAL ZONE  │  │  COMM ZONE     │  │ PWR ZONE  │  │
│  └────────────────┘  └────────────────┘  └───────────┘  │
│                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────┐  │
│  │  CAN + I2C     │  │  ADC + Sensors │  │  Safety   │  │
│  │  Connectors    │  │  Connectors    │  │  Relay    │  │
│  │  (J2, J6)      │  │  (J7, J8)      │  │  E-Stop   │  │
│  │                │  │                │  │  (J11)    │  │
│  │  BUS ZONE      │  │  SENSOR ZONE   │  │ SAFETY    │  │
│  └────────────────┘  └────────────────┘  └───────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  J_STACK Stacking Connector (2x20, center edge)  │    │
│  │  Signals to Driver PCB (ASD/CID/SLD/Main)       │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  Board Edge ─────────────────── Mounting Holes (M3 x 4) │
└──────────────────────────────────────────────────────────┘
```

**Critical Layout Rules:**

| Rule | Specification | Rationale |
|------|---------------|-----------|
| STM32 decoupling | 100nF caps within 5mm of VDD pins | Reduce supply noise |
| VDDA isolation | Ferrite bead + 1uF from 3.3V | Clean analog reference |
| Crystal traces | Short, symmetric, guard ring GND | Minimize EMI coupling |
| SPI traces | Matched length (±2mm), 50 ohm impedance | Signal integrity at 2 MHz |
| ADC input traces | Route over GND plane, away from PWM | Minimize noise pickup |
| PWM output traces | Away from analog section, wide traces | High-frequency switching noise |
| GND plane | Unbroken under STM32 and analog section | Low-impedance return path |
| I2C traces | Keep <30mm on board, pull-ups near STM32 | Minimize capacitance |
| Safety relay | Creepage >2mm between 5V/12V and 3.3V logic | IEC 60335 clearance |
| Thermal pad | Via array under STM32 to GND plane (9 vias min) | Thermal dissipation |

### Board Dimensions

- **Target size:** 160mm x 90mm (matches CMIO and Driver PCB in 3-board stack)
- **Mounting:** 4x M3 mounting holes at corners (3.2mm drill), positions match stack
- **Connector placement:** SPI (J1) and sensors on board edges; J_STACK centered on one long edge (bottom side, mates with Driver PCB)
- **Layer 2 GND plane:** Continuous, no cuts or splits under STM32

---

## Manufacturing Specifications

| Parameter | Value |
|-----------|-------|
| Layers | 4 |
| Board thickness | 1.6mm |
| Copper weight | 1 oz (35um) all layers |
| Min trace width | 0.15mm (6 mil) |
| Min trace spacing | 0.15mm (6 mil) |
| Min via drill | 0.3mm |
| Via pad diameter | 0.6mm |
| Surface finish | ENIG (lead-free) |
| Solder mask | Green (both sides) |
| Silkscreen | White (both sides) |
| Board material | FR4, Tg ≥ 150°C |
| Impedance control | 50 ohm single-ended on SPI lines |
| Panelization | 2x2 panel with V-score for JLCPCB |

### Assembly

- All components SMT (both sides if needed, prefer top-side only)
- Through-hole: 2.54mm pin headers for J3 (DS3225 servo), J_STACK (stacking connector), and J9 (debug)
- Reflow soldering for SMT components
- Hand-solder through-hole headers after reflow

---

## Controller PCB BOM

| Ref | Part | Package | Quantity | Unit Cost (USD) | Notes |
|-----|------|---------|----------|----------------|-------|
| U1 | STM32G474RET6 | LQFP-64 | 1 | $8.00 | Cortex-M4F, 170 MHz |
| U2 | AMS1117-3.3 | SOT-223 | 1 | $0.30 | 3.3V LDO, 800mA |
| Y1 | 8 MHz crystal | HC49/SMD | 1 | $0.20 | HSE, 20ppm, 18pF load |
| Y2 | 32.768 kHz crystal | 2x1.2mm SMD | 1 | $0.30 | LSE for RTC |
| Q1 | 2N7002 | SOT-23 | 1 | $0.05 | Relay driver MOSFET |
| D1 | Green LED | 0603 | 1 | $0.03 | Status indicator |
| D2 | 1N4148WS | SOD-323 | 1 | $0.03 | Flyback diode for relay |
| D3 | PRTR5V0U2X | SOT-143B | 2 | $0.15 | ESD protection on SPI + safety I/O |
| FB1 | Ferrite bead 600R | 0603 | 1 | $0.05 | VDDA isolation |
| R1-R2 | 4.7k ohm | 0402 | 2 | $0.01 | I2C pull-ups |
| R3-R4 | 10k ohm | 0402 | 2 | $0.01 | Pot detect + E-stop pull-ups |
| R5 | 10k ohm | 0402 | 1 | $0.01 | BOOT0 pull-down |
| R6 | 330 ohm | 0402 | 1 | $0.01 | LED current limit |
| R7 | 330 ohm | 0402 | 1 | $0.01 | Relay gate resistor |
| R8-R13 | 33 ohm | 0402 | 6 | $0.01 | Series termination on SPI + safety |
| R14-R15 | 10k ohm | 0402 | 2 | $0.01 | NTC ADC filter resistors |
| C1-C2 | 10uF ceramic | 0805 | 2 | $0.10 | LDO input/output bulk |
| C3-C8 | 100nF ceramic | 0402 | 6 | $0.01 | VDD decoupling per pin |
| C9 | 1uF ceramic | 0402 | 1 | $0.02 | VDDA decoupling |
| C10-C11 | 18pF ceramic | 0402 | 2 | $0.01 | HSE crystal load caps |
| C12-C13 | 6.8pF ceramic | 0402 | 2 | $0.01 | LSE crystal load caps |
| C14-C15 | 100nF ceramic | 0402 | 2 | $0.01 | ADC RC filter caps |
| C16 | 100nF ceramic | 0402 | 1 | $0.01 | E-stop debounce cap |
| SW1 | Tactile switch | 6x6mm | 1 | $0.05 | Reset button |
| SJ1 | Solder jumper | 0603 pad | 1 | — | IRQ/SWO select |
| **Connectors** | | | | | |
| J1 | JST-SH 6-pin | 1.0mm pitch | 1 | $0.30 | SPI to CM5 |
| J2 | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | CAN bus to microwave surface |
| J6 | JST-SH 4-pin | 1.0mm pitch | 1 | $0.20 | MLX90614 I2C |
| J7 | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | HX711 |
| J8 | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | NTC inputs |
| J9 | Pin header 2x5 | 1.27mm pitch | 1 | $0.30 | SWD debug |
| J10 | JST-XH 2-pin | 2.5mm pitch | 1 | $0.10 | 5V power input |
| J11 | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | Safety I/O |
| J_STACK | 2x20 pin header | 2.54mm, 11mm stacking | 1 | $0.80 | Stacking connector to Driver PCB |
| **PCB** | 4-layer, 160x90mm | FR4 ENIG | 1 | $4.50 | JLCPCB batch pricing (5 pcs) |

**Estimated unit cost (components + PCB): ~$14 USD** (at single-unit prototype quantities; ~$10 at 100+ volume)

---

## Design Verification Checklist

### Pre-Fabrication

- [ ] Schematic ERC (Electrical Rule Check) passes with zero errors
- [ ] All STM32 pin assignments verified against datasheet alternate function table
- [ ] SPI2 peripheral confirmed available on PB12-PB15 for LQFP-64 package
- [ ] No pin conflicts between SPI2, TIM1, TIM2, TIM3, I2C1, ADC2
- [ ] BOOT0 has pull-down resistor (prevents accidental bootloader entry)
- [ ] All VDD/VSS pins connected with individual decoupling caps
- [ ] VDDA has ferrite bead isolation from digital 3.3V
- [ ] Crystal load capacitors match crystal specifications
- [ ] I2C pull-up values appropriate for 100 kHz bus speed

### PCB Layout

- [ ] DRC (Design Rule Check) passes with zero errors
- [ ] GND plane continuous under STM32 (no splits or traces cutting plane)
- [ ] SPI traces matched length within 2mm
- [ ] ADC traces routed over solid GND, away from PWM traces
- [ ] Thermal vias under STM32 exposed pad (minimum 9 vias, 0.3mm drill)
- [ ] All connectors accessible from board edges
- [ ] Mounting holes clear of traces and copper (1mm clearance)
- [ ] Silkscreen labels on all connectors and test points

### Post-Assembly

- [ ] 3.3V rail measures 3.3V ±3% under load
- [ ] STM32 responds to SWD probe (ST-Link connects, reads device ID)
- [ ] SPI loopback test with CM5 passes (echo bytes)
- [ ] All PWM channels output correct frequency on oscilloscope
- [ ] ADC reads known voltage within ±1 LSB
- [ ] I2C scan detects MLX90614 at address 0x5A
- [ ] HX711 returns stable readings with no load cell attached
- [ ] E-stop interrupt triggers on button press
- [ ] Safety relay clicks when PB0 driven high

---

## Related Documentation

- [[Driver-PCB-Design]] — Driver PCB: power conversion, actuator drivers, stacking connector details
- [[../02-Hardware/Epicura-Architecture|Epicura Architecture]] — System-level wiring and block diagrams
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]] — Induction, sensors, power specs
- [[../02-Hardware/05-Sensors-Acquisition|Sensors & Acquisition]] — Sensor interface details
- [[../05-Subsystems/09-Induction-Heating|Induction Heating]] — Microwave surface module with CAN bus interface
- [[../08-Components/01-Compute-Module-Components|Compute Module Components]] — CM5 and STM32 BOM

---

#epicura #pcb #controller #stm32 #hardware-design #spi

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
