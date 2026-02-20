---
created: 2026-02-15
modified: 2026-02-20
version: 9.0
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
| **CM5 IO Board (CM5IO)** | Off-the-shelf (Raspberry Pi official) | Commercial carrier board; no custom PCB needed |
| **Microwave induction surface** | Commercial module with CAN port (see [[../05-Subsystems/09-Induction-Heating\|Induction Heating]]) | Self-contained coil + driver; controlled via CAN bus |

The CM5IO board is an off-the-shelf Raspberry Pi carrier board that sits on top of the stack. The two custom boards (Controller, Driver) form a stackable pair connected via 2x20-pin 2.54mm board-to-board headers, sharing a uniform 160x90mm footprint. The Controller PCB connects upward to the CM5IO board via **J_CM5** (2x20 pin socket that mates directly with the CM5IO's 40-pin GPIO header — SPI, IRQ, LED data, 5V power, and GND all route through this single connector) and downward to the Driver PCB via **J_STACK**. All real-time control, sensor acquisition, and safety monitoring runs on this controller board. Servo PWM and actuator GPIO signals pass through J_STACK to the Driver PCB where power electronics drive the actual actuators. The UPS-backed 5V rail from J_STACK is fed upward through J_CM5 to power the CM5IO and CM5 module.

---

## Board-Level Block Diagram

```
                   5V from J_STACK (UPS-backed)
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
         │    │  SPI2 ◄─────────────────────── J_CM5: SPI to CM5 (pins 19,21,23,24)
         │    │  PB3 (IRQ) ────────────────── J_CM5: IRQ to CM5 (pin 7)
         │    │                           │                │
         │    │  FDCAN1 (PB8/PB9) ─────────── J_CAN: CAN to Microwave Surface
         │    │                           │                │
         │    │  TIM1_CH1 (PA8) ───────────── J_STACK: DS3225 Servo (via Driver PCB)
         │    │                           │                │
         │    │  TIM2_CH1 (PA0) ──────────── J_STACK: P-ASD Pump PWM
         │    │  (P-ASD solenoids V1-V6 via PCF8574 on Driver PCB,
         │    │   I2C1 addr 0x20 — no direct GPIO needed)
         │    │                           │                │
         │    │  I2C1 (PB6/PB7) ───────────── J_IR: MLX90614
         │    │                           │                │
         │    │  GPIO (PC0/PC1) ───────────── J_STACK: HX711 (via Driver PCB)
         │    │                           │                │
         │    │  PA4/PA5 ─────────────────── Available (was NTC inputs)
         │    │                           │                │
         │    │  GPIO (PB0) ───────────────── Q1: Safety Relay Driver
         │    │  GPIO (PB1) ◄──────────────── SW1: Pot Detection
         │    │  GPIO (PB2) ◄──────────────── SW2: E-Stop
         │    │                           │                │
         │    │  SWD (PA13/PA14) ──────────── J_SWD: Debug Header
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
│  │  PB8  (FDCAN1_RX) ◄── ISO1050 TXD (isolated CAN xcvr)    │  │
│  │  PB9  (FDCAN1_TX) ──► ISO1050 RXD (isolated CAN xcvr)    │  │
│  │  500 kbps, 120Ω term, 5kV isolation barrier on J_CAN         │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── PWM: Main Servo Arm ────────┐                           │
│  │  PA8  (TIM1_CH1)  ──► DS3225 Signal (orange wire)         │  │
│  │  50 Hz, 500-2500 us pulse width                            │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── P-ASD: Pneumatic Seasoning Dispenser ─┐                           │
│  │  PA0  (TIM2_CH1)  ──► P-ASD Pump PWM (12V diaphragm pump)│  │
│  │  Solenoids V1-V6: driven by PCF8574 I2C GPIO expander              │  │
│  │    on Driver PCB (I2C1, addr 0x20, outputs P0-P5)                  │  │
│  │  I2C1 (PB6/PB7)   ──► ADS1015 Pressure Sensor (addr 0x48)         │  │
│  │                    ──► PCF8574 Solenoid Expander (addr 0x20)       │  │
│  └───────────────────────────────────────────┘                           │
│  Note: All actuator signals (servos, pumps) route via J_STACK │
│  to Driver PCB where power electronics drive the actuators.   │
│  P-ASD solenoids are controlled via PCF8574 on the Driver PCB,│
│  accessed over shared I2C1 bus through J_STACK.                 │
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
│  ┌─── Reserved / Available ───────┐                           │
│  │  PA4  ── Available (was NTC Coil)                          │  │
│  │  PA5  ── Available (was NTC Ambient)                       │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Safety & Control ─────┐                           │
│  │  PB0  (GPIO)      ──► Safety Relay (via MOSFET Q1)        │  │
│  │  PB1  (GPIO)      ◄── Pot Detection (reed switch)        │  │
│  │  PB2  (GPIO)      ◄── E-Stop Button (EXTI, active-low)   │  │
│  │  PC13 (GPIO)      ──► Status LED (green, active-low)     │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Power Fail Detection ───────┐                           │
│  │  PA1  (COMP2_INP) ◄── 24V voltage divider (100k/10k)     │  │
│  │       COMP2 threshold ~1.5V → trips at 24V < 16.5V       │  │
│  │       PWR_FAIL output on J_STACK Pin 16 (active-low)      │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── LED Ring Power Control ────┐                           │
│  │  PA2  (GPIO)     ──► Q2 gate (2N7002, N-MOSFET)          │  │
│  │       Q2 drain ──► Q3 gate (SI2301, P-MOSFET)            │  │
│  │       Q3 switches 5V to LED ring via J_LED                │  │
│  │       Data: CM5 GPIO18 → J_CM5 pin 12 → J_LED pin 2     │  │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Reserved / Unused ──────────┐                           │
│  │  PA9  (GPIO)      ── Available (was USART1_TX)            │  │
│  │  PA10 (GPIO)      ── Available (was USART1_RX)            │  │
│  │  PA11 (USB_DM)    ── Reserved for USB (future)            │  │
│  │  PA12 (USB_DP)    ── Reserved for USB (future)            │  │
│  │  PB4  (GPIO)      ── Available                            │  │
│  │  PB5  (GPIO)      ── Available                            │  │
│  │  PB8  (FDCAN1_RX)  ── CAN RX via ISO1050 (isolated)       │  │
│  │  PB9  (FDCAN1_TX)  ── CAN TX via ISO1050 (isolated)       │  │
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
| PA0 | TIM2_CH1 | P-ASD Pump PWM | Output | J_STACK Pin 15 | P-ASD |
| PA1 | COMP2_INP | 24V Power Fail Detection (COMP2) | Input | J_STACK Pin 16 (PWR_FAIL output) | Power |
| PA2 | GPIO | LED Ring Power Enable | Output | J_LED (via Q2/Q3 MOSFET) | Illumination |
| PA3 | — | Available (was P-ASD Sol V5) | — | — | — |
| PA4 | — | Available (was NTC Coil) | — | — | — |
| PA5 | — | Available (was NTC Ambient) | — | — | — |
| PA6 | TIM3_CH1 | Exhaust Fan 1 PWM | Output | J_STACK Pin 27 | Exhaust |
| PA7 | GPIO | SLD Solenoid 1 Enable | Output | J_STACK Pin 33 | SLD |
| PA8 | TIM1_CH1 | Main Servo (DS3225) | Output | J_STACK Pin 37 | Main |
| PA9 | GPIO | SLD Solenoid 2 Enable | Output | J_STACK Pin 34 | SLD |
| PA10 | TIM1_CH3/GPIO | CID Linear Actuator 1 EN | Output | J_STACK Pin 21 | CID |
| PA11 | TIM1_CH4 | Buzzer PWM | Output | J_STACK Pin 39 | Main |
| PA13 | SWDIO | SWD Debug | Bidir | J_SWD | Debug |
| PA14 | SWCLK | SWD Debug | Input | J_SWD | Debug |
| PB0 | GPIO | Safety Relay | Output | Q1 | Safety |
| PB1 | GPIO | Pot Detection | Input | SW1 | Safety |
| PB2 | GPIO (EXTI) | E-Stop | Input | SW2 | Safety |
| PB3 | GPIO | IRQ to CM5 | Output | J_CM5 | Comms |
| PB4 | GPIO | CID Linear Actuator 1 PH | Output | J_STACK Pin 22 | CID |
| PB5 | GPIO | CID Linear Actuator 2 EN | Output | J_STACK Pin 23 | CID |
| PB6 | I2C1_SCL | MLX90614/INA219 | Output | J_IR, J_STACK Pin 35 | Sensors |
| PB7 | I2C1_SDA | MLX90614/INA219 | Bidir | J_IR, J_STACK Pin 36 | Sensors |
| PB10 | TIM2_CH3 | Exhaust Fan 2 PWM | Output | J_STACK Pin 28 | Exhaust |
| PB11 | — | Available (was P-ASD Sol V6) | — | — | — |
| PB12 | SPI2_NSS | CM5 CE0 | Input | J_CM5 | Comms |
| PB13 | SPI2_SCK | CM5 SCLK | Input | J_CM5 | Comms |
| PB14 | SPI2_MISO | CM5 MISO | Output | J_CM5 | Comms |
| PB15 | SPI2_MOSI | CM5 MOSI | Input | J_CM5 | Comms |
| PC0 | GPIO | HX711 SCK (pot) | Output | J_STACK Pin 17 | Sensors |
| PC1 | GPIO | HX711 DOUT (pot) | Input | J_STACK Pin 18 | Sensors |
| PC2 | GPIO | CID Linear Actuator 2 PH | Output | J_STACK Pin 24 | CID |
| PC3 | GPIO | SLD Pump 1 PWM | Output | J_STACK Pin 29 | SLD |
| PC4 | GPIO | SLD Pump 1 DIR | Output | J_STACK Pin 30 | SLD |
| PC5 | GPIO | SLD Pump 2 PWM | Output | J_STACK Pin 31 | SLD |
| PC6 | GPIO | SLD Pump 2 DIR | Output | J_STACK Pin 32 | SLD |
| PC7 | — | Available (was P-ASD Sol V3) | — | — | — |
| PC13 | GPIO | Status LED | Output | D1 | Status |
| PD2 | — | Available (was P-ASD Sol V4) | — | — | — |

---

## Power Supply

### Input

The controller PCB receives 5V DC via J_STACK pins 11-12 from the Driver PCB's TPS54531 buck converter, which is powered from a UPS-backed 12V DC input. This ensures the STM32 remains powered during AC outages. A 3.3V LDO regulates this down for the STM32 and all 3.3V peripherals. No onboard buck converter is needed. The 5V rail is also fed upward through J_CM5 pins 2 and 4 to power the CM5IO board and CM5 module, eliminating the need for a separate USB-C power input on the CM5IO.

### Regulator Circuit

```
5V from J_STACK (pins 11-12, UPS-backed via TPS54531)
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
| Status LED | 5 | 10 | Via 330 ohm resistor |
| ISO1050 (3.3V side) | 15 | 20 | Isolated CAN transceiver VCC1 |
| **Total 3.3V** | **~105** | **~186** | Well within LDO capacity |

> [!note]
> Servo motors (DS3225) are powered from a separate 24V→6.5V buck converter on the Driver PCB, not from this 3.3V LDO. The 5V rail is sourced from a UPS-backed 12V→5V converter (TPS54531) on the Driver PCB, ensuring the controller and CM5 stay powered during AC outages. The 5V rail passes through the Controller PCB upward to the CM5IO via J_CM5 pins 2/4 (up to 3A for CM5 peak load). Only the PWM signal lines route through the controller PCB.

### Decoupling

- **Per VDD pin:** 100nF MLCC placed within 5mm of each VDD/VSS pin pair
- **VDDA (analog supply):** 1uF MLCC + ferrite bead from main 3.3V
- **Bulk:** 10uF MLCC at LDO output, 10uF MLCC at LDO input
- **Total decoupling caps:** 6-8x 100nF + 2x 10uF + 1x 1uF

---

## CM5 to STM32 SPI Interface

### Physical Connection

The CM5 IO Board's 40-pin GPIO header mates directly with **J_CM5** on the Controller PCB — a 2x20 pin socket (2.54mm pitch) that receives all 40 pins. No ribbon cable is needed; the boards stack directly. SPI, IRQ, LED ring data, 5V power, and GND all route through this single connector.

```
CM5 IO Board (40-pin GPIO Header)       Controller PCB (J_CM5, 2x20 socket)
┌───────────────────────┐                ┌───────────────────────┐
│                       │   stacking     │                       │
│  Pin  2  (5V)         ├◄──────────────┤ 5V out (UPS-backed)   │
│  Pin  4  (5V)         ├◄──────────────┤ 5V out (UPS-backed)   │
│  Pin  7  (GPIO4)      │◄──────────────┤ PB3  (IRQ, act-low)   │
│  Pin 12  (GPIO18)     ├──────────────►│ LED ring data (pass)  │
│  Pin 19  (GPIO10/MOSI)├──────────────►│ PB15 (SPI2_MOSI)     │
│  Pin 21  (GPIO9/MISO) │◄──────────────┤ PB14 (SPI2_MISO)     │
│  Pin 23  (GPIO11/SCLK)├──────────────►│ PB13 (SPI2_SCK)      │
│  Pin 24  (GPIO8/CE0)  ├──────────────►│ PB12 (SPI2_NSS)      │
│  Pin 6,9,14,20,25,    │               │                       │
│  30,34,39 (GND)       ├──────────────►│ GND                   │
│  (all other pins)     ├───── N/C ─────┤ (not connected)       │
│                       │                │                       │
└───────────────────────┘                └───────────────────────┘

Connection: Direct board-to-board stacking (no cable)
Logic level: 3.3V on both sides (no level shifter needed)
5V direction: Controller PCB → CM5IO (UPS-backed power)
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
| DISPENSE_PASD | 0x03 | CM5 → STM32 | cartridge_id (uint8: 1-6), target_g (uint16) |
| DISPENSE_CID | 0x06 | CM5 → STM32 | cid_id (uint8: 1-2), mode (uint8), pos_mm (uint8) |
| DISPENSE_SLD | 0x07 | CM5 → STM32 | channel (uint8: OIL=1, WATER=2), target_g (uint16) |
| E_STOP | 0x04 | CM5 → STM32 | reason_code (uint8) |
| HEARTBEAT | 0x05 | Bidirectional | uptime_ms (uint32) |
| TELEMETRY | 0x10 | STM32 → CM5 | ir_temp, ntc_temps, weight, duty_pct |
| SENSOR_DATA | 0x11 | STM32 → CM5 | adc_values[], ir_temp, load_cells[] |
| STATUS | 0x12 | STM32 → CM5 | safety_state, error_code, flags |
| PURGE_PASD | 0x0B | CM5 → STM32 | cartridge_id (uint8: 1-6, or 0xFF=all) |
| PRESSURE_STATUS | 0x0C | CM5 → STM32 | — (returns pressure_bar, 2 bytes fixed-point) |
| POWER_TELEMETRY | 0x13 | STM32 → CM5 | bus_voltage_mV (uint16), current_mA (uint16), power_mW (uint16) |
| POWER_FAIL | 0x14 | STM32 → CM5 | state (uint8: 0=OK, 1=FAIL), voltage_mV (uint16) |
| ACK | 0xFF | Bidirectional | ack_msg_id, result_code |

### STM32 SPI Slave Implementation Notes

- Configure SPI2 in slave mode with hardware NSS
- Use DMA for both TX and RX to avoid CPU overhead
- Double-buffer TX: while one buffer is being transmitted, the next telemetry frame is prepared in the other
- IRQ line driven by GPIO output (PB3), not tied to SPI hardware
- Timeout: if CM5 does not read within 500ms of IRQ assertion, STM32 enters WARNING state

---

## Connector Definitions

### J_CM5 — CM5IO GPIO Header Receptor (2x20 pin socket, 2.54mm)

Mates directly with the CM5IO board's 40-pin GPIO header. Only the pins listed below are actively routed on the Controller PCB; all other pins pass through unconnected.

| GPIO Pin | Signal | STM32 Pin / Destination | Direction | Purpose |
|----------|--------|------------------------|-----------|---------|
| 2, 4 | 5V | 5V rail (from J_STACK, UPS-backed) | Out to CM5IO | Powers CM5IO + CM5 module |
| 6, 9, 14, 20, 25, 30, 34, 39 | GND | GND | Power | Common ground |
| 7 | GPIO4 | PB3 (GPIO) | Out to CM5 | Data-ready IRQ (active-low, 10us pulse) |
| 12 | GPIO18 | J_LED pin 2 (passthrough) | Out from CM5 | WS2812B LED ring data |
| 19 | GPIO10 (MOSI) | PB15 (SPI2_MOSI) | In from CM5 | SPI data to STM32 |
| 21 | GPIO9 (MISO) | PB14 (SPI2_MISO) | Out to CM5 | SPI data from STM32 |
| 23 | GPIO11 (SCLK) | PB13 (SPI2_SCK) | In from CM5 | SPI clock |
| 24 | GPIO8 (CE0) | PB12 (SPI2_NSS) | In from CM5 | SPI chip select (active-low) |

> [!note]
> The 5V pins (2, 4) are driven by the Controller PCB from the UPS-backed 5V rail received via J_STACK. This means the CM5 module is powered through the same UPS-backed supply as the STM32, ensuring both processors stay alive during AC outages. The CM5IO's USB-C port can still be used for debug console access but is not the primary power source.

### J_CAN — CAN Bus to Microwave Surface (JST-XH 2.5mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | CAN_H | via CAN transceiver | CAN bus high |
| 2 | CAN_L | via CAN transceiver | CAN bus low |
| 3 | GND_ISO | GND2 (isolated) | Isolated bus ground (NOT system GND) |
| 4 | +5V (optional) | — | Transceiver power (if needed by module) |

> [!note]
> STM32 FDCAN1 pins PB8 (RX) and PB9 (TX) connect to an **ISO1050DUB isolated CAN transceiver** (TI, SOIC-8) on the controller PCB. The ISO1050 provides 5 kV RMS galvanic isolation (reinforced per UL 1577) between the STM32 logic side (VCC1 = 3.3V, GND1 = system ground) and the CAN bus side (VCC2 = 5V, GND2 = isolated bus ground). This isolation protects the STM32 and control electronics from ground bounce and EMI transients generated by the 1,800W induction module's IGBT switching, and satisfies IEC 60335 requirements for galvanic isolation between mains-connected power electronics and low-voltage control circuits. The transceiver drives CAN_H/CAN_L to J_CAN. 120Ω termination resistor on-board. CAN cable shield connects to GND_ISO at the Controller PCB end only (single-point ground).

### J_IR — MLX90614 I2C (JST-SH 1.0mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | SCL | PB6 (I2C1_SCL) | 4.7k pull-up on board |
| 2 | SDA | PB7 (I2C1_SDA) | 4.7k pull-up on board |
| 3 | VCC | 3.3V | — |
| 4 | GND | GND | — |

### J_SWD — SWD Debug (10-pin 1.27mm Cortex Debug or 6-pin TagConnect)

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

### J_SAFE — Safety I/O (JST-XH 2.5mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | RELAY_DRV | PB0 via Q1 | Drives safety relay coil |
| 2 | POT_DET | PB1 | Reed switch input, 10k pull-up |
| 3 | E_STOP | PB2 | NC button, 10k pull-up, RC debounce |
| 4 | GND | GND | — |

### J_LED — LED Ring (JST-XH 2.5mm, 3-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 5V_SW | Switched 5V from Q3 P-MOSFET (PA2 enable) |
| 2 | DATA | WS2812B data (passthrough from CM5 GPIO18) |
| 3 | GND | Power ground |

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
| **P-ASD Subsystem (Pins 15-20, 39)** ||||
| 15 | PASD_PUMP_PWM (PA0) | Out | 16 | PWR_FAIL (PA1) | Out |
| 17 | HX711_SCK (PC0) | Out | 18 | HX711_DOUT (PC1) | In |
| 19 | Reserved (was PASD_SOL4) | — | 20 | Reserved (was PASD_SOL5) | — |
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
| **Main Actuators & Audio (Pins 37-38, 40)** ||||
| 37 | MAIN_SERVO_PWM (PA8) | Out | 38 | BUZZER_PWM (PA11) | Out |
| 39 | Reserved (was PASD_SOL6) | — | 40 | GND | Power |

#### Pin Group Summary

| Group | Pins | Count | Purpose |
|-------|------|-------|---------|
| 24V Power | 1-4 | 4 | 24V from PSU (paralleled for 12A capacity) |
| GND | 5-10, 25-26, 40 | 9 | Low-impedance ground return |
| 5V | 11-12 | 2 | 5V passthrough |
| 3.3V | 13-14 | 2 | Logic reference |
| **P-ASD** (Seasoning) | 15 | 1 | 1× pump PWM (solenoids via PCF8574 on Driver PCB, I2C1) |
| **CID** (Coarse) | 21-26 | 6 | 2× actuator EN/PH, 2× GND |
| **Exhaust Fans** | 27-28 | 2 | 2× fan PWM (independent speed control, 120mm) |
| **SLD** (Liquid) | 29-36 | 8 | 2× pump PWM/DIR, 2× solenoid, I2C (INA219) |
| **Main** (Arm/Audio) | 37-38, 40 | 3 | Main servo, buzzer, 1× GND |

> [!note]
> Subsystem grouping enables modular wiring harnesses. All signals for ASD run together (pins 15-20), all CID signals together (21-28), etc. Servo and actuator external connectors are on the Driver PCB, not the Controller PCB. The Controller PCB only carries low-level PWM/GPIO signals.

---

## Protection Circuits

### ESD Protection

- TVS diode array (e.g., PRTR5V0U2X) on J_CM5 SPI lines
- TVS diodes on J_SAFE safety inputs (E-stop, pot detection)
- All external connectors have series 33 ohm resistors on signal lines

### Relay Driver (Q1)

```
PB0 ────┤ 330R ├──── Gate ─┐
                           │
                     ┌─────▼──────┐
                     │  Q1: 2N7002│
                     │  (N-MOSFET)│
                     └─────┬──────┘
                           │ Drain
                     ┌─────▼──────┐
                     │ Relay Coil │ ◄── 5V or 12V
                     │ (Omron G5V)│
                     └─────┬──────┘
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

### LED Ring Power Switch (Q2 + Q3)

A high-side P-MOSFET switch controls 5V power to the WS2812B LED ring. An N-MOSFET (Q2) level-shifts the 3.3V STM32 GPIO to drive the P-MOSFET (Q3) gate. The LED ring data line (WS2812B protocol) is driven directly by CM5 GPIO18 and passes through J_LED as a signal passthrough — no STM32 involvement on the data path.

```
5V (from J_STACK) ──── Q3: SI2301 (P-MOSFET, SOT-23) ──── J_LED Pin 1 (5V_SW)
                         │ Source              Drain │
                         │                           │
                         Gate ──┬── R18: 10k to 5V (default OFF)
                                │
                                └── Q2: 2N7002 Drain
                                         │
                                    Q2 Source ── GND
                                         │
                                    Q2 Gate ── R17: 100R ── PA2 (GPIO)
                                         │
                                    R19: 10k pull-down to GND

CM5 GPIO18 ── J_CM5 Pin 12 ── J_LED Pin 2 (DATA, PCB trace passthrough)
GND ─────────────── J_LED Pin 3 (GND)
```

| Parameter | Value |
|-----------|-------|
| Q2 | 2N7002 (N-MOSFET, SOT-23) — level shifter |
| Q3 | SI2301CDS (P-MOSFET, SOT-23) — high-side switch |
| Vds(max) Q3 | -20V |
| Rds(on) Q3 | 110 mΩ @ Vgs=-4.5V |
| Id(max) Q3 | -2.3A (sufficient for 1A LED ring peak) |
| R17 | 100Ω gate resistor on Q2 |
| R18 | 10kΩ pull-up to 5V on Q3 gate (LED OFF by default) |
| R19 | 10kΩ pull-down on Q2 gate (safe boot state) |
| Control Pin | PA2 (GPIO output) |
| Default State | OFF (Q2 gate pulled low → Q3 gate pulled to 5V → P-MOSFET off) |

> [!note]
> The WS2812B data line from CM5 GPIO18 routes through J_CM5 pin 12 to J_LED pin 2 via a PCB trace on the Controller PCB — no external jumper wire needed. No buffering or level shifting required (WS2812B accepts 3.3V logic at 5V supply). The STM32 controls only the power enable; the CM5 handles pixel data via `rpi_ws281x` Python library.

---

## PCB Stackup and Layout

### 4-Layer Stackup

```
┌──────────────────────────────────────────────┐
│  Layer 1 (Top)    — Signal + Components      │  35um Cu
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 2 (Inner1) — GND Plane (continuous)   │  35um Cu
├──────────────────────────────────────────────┤
│  Core             — FR4, 0.8mm               │
├──────────────────────────────────────────────┤
│  Layer 3 (Inner2) — 3.3V Power Plane         │  35um Cu
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 4 (Bottom) — Signal + Components      │  35um Cu
└──────────────────────────────────────────────┘

Total thickness: ~1.6mm (standard)
Material: FR4 (Tg 150°C minimum)
```

### Layout Guidelines

**Component Placement Zones:**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────┐  │
│  │   STM32G474RE  │  │  SPI + Debug   │  │  Power    │  │
│  │   + Crystal    │  │  Connectors    │  │  LDO +    │  │
│  │   + Decoupling │  │  (J_CM5, J_SWD)      │  │  Input    │  │
│  │                │  │                │  │  (J_STACK)    │  │
│  │  DIGITAL ZONE  │  │  COMM ZONE     │  │ PWR ZONE  │  │
│  └────────────────┘  └────────────────┘  └───────────┘  │
│                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────┐  │
│  │  CAN + I2C     │  │  Safety I/O    │  │  LED Ring │  │
│  │  Connectors    │  │  (J_SAFE)      │  │  (J_LED)  │  │
│  │  (J_CAN, J_IR) │  │                │  │           │  │
│  │                │  │                │  │           │  │
│  │  BUS ZONE      │  │  SAFETY ZONE   │  │ LED ZONE  │  │
│  └────────────────┘  └────────────────┘  └───────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  J_STACK Stacking Connector (2x20, center edge)  │   │
│  │  Signals to Driver PCB (ASD/CID/SLD/Main)        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  Board Edge ─────────────────── Mounting Holes (M3 x 4) │
└─────────────────────────────────────────────────────────┘
```

**Critical Layout Rules:**

| Rule | Specification | Rationale |
|------|---------------|-----------|
| STM32 decoupling | 100nF caps within 5mm of VDD pins | Reduce supply noise |
| VDDA isolation | Ferrite bead + 1uF from 3.3V | Clean analog reference |
| Crystal traces | Short, symmetric, guard ring GND | Minimize EMI coupling |
| SPI traces | Matched length (±2mm), 50 ohm impedance | Signal integrity at 2 MHz |
| PWM output traces | Away from analog section, wide traces | High-frequency switching noise |
| GND plane | Unbroken under STM32 and analog section | Low-impedance return path |
| I2C traces | Keep <30mm on board, pull-ups near STM32 | Minimize capacitance |
| Safety relay | Creepage >2mm between 5V/12V and 3.3V logic | IEC 60335 clearance |
| CAN isolation | Creepage ≥6.4mm between GND1 (system) and GND2 (bus) zones | IEC 60335 reinforced insulation; slot/gap in ground plane under ISO1050 |
| Thermal pad | Via array under STM32 to GND plane (9 vias min) | Thermal dissipation |

### Board Dimensions

- **Target size:** 160mm x 90mm (matches CM5IO and Driver PCB in 3-board stack)
- **Mounting:** 4x M3 mounting holes at corners (3.2mm drill), positions match stack
- **Connector placement:** J_CM5 (CM5IO stacking) on top edge, sensors on side edges; J_STACK centered on one long edge (bottom side, mates with Driver PCB)
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
- Through-hole: 2.54mm pin headers for J_STACK (stacking connector) and J_SWD (debug)
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
| Q2 | 2N7002 | SOT-23 | 1 | $0.05 | LED ring power switch (N-MOSFET level shifter) |
| Q3 | SI2301CDS | SOT-23 | 1 | $0.10 | LED ring power switch (P-MOSFET high-side) |
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
| R17 | 100 ohm | 0402 | 1 | $0.01 | Q2 gate resistor (LED switch) |
| R18 | 10k ohm | 0402 | 1 | $0.01 | Q3 gate pull-up to 5V (LED OFF default) |
| R19 | 10k ohm | 0402 | 1 | $0.01 | Q2 gate pull-down (safe boot) |
| C1-C2 | 10uF ceramic | 0805 | 2 | $0.10 | LDO input/output bulk |
| C3-C8 | 100nF ceramic | 0402 | 6 | $0.01 | VDD decoupling per pin |
| C9 | 1uF ceramic | 0402 | 1 | $0.02 | VDDA decoupling |
| C10-C11 | 18pF ceramic | 0402 | 2 | $0.01 | HSE crystal load caps |
| C12-C13 | 6.8pF ceramic | 0402 | 2 | $0.01 | LSE crystal load caps |
| C16 | 100nF ceramic | 0402 | 1 | $0.01 | E-stop debounce cap |
| SW1 | Tactile switch | 6x6mm | 1 | $0.05 | Reset button |
| SJ1 | Solder jumper | 0603 pad | 1 | — | IRQ/SWO select |
| **Connectors** | | | | | |
| J_CM5 | 2x20 pin socket | 2.54mm, 8.5mm stacking | 1 | $0.80 | CM5IO GPIO header receptor (SPI, IRQ, LED data, 5V power) |
| J_CAN | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | CAN bus to microwave surface |
| J_IR | JST-SH 4-pin | 1.0mm pitch | 1 | $0.20 | MLX90614 I2C |
| J_SWD | Pin header 2x5 | 1.27mm pitch | 1 | $0.30 | SWD debug |
| J_SAFE | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | Safety I/O |
| J_LED | JST-XH 3-pin | 2.5mm pitch | 1 | $0.12 | LED ring (5V_SW + DATA + GND) |
| J_STACK | 2x20 pin header | 2.54mm, 11mm stacking | 1 | $0.80 | Stacking connector to Driver PCB |
| U_CAN | ISO1050DUB | SOIC-8 | 1 | $3.50 | TI isolated CAN transceiver, 5kV RMS, CAN 2.0B up to 1 Mbps |
| C_CAN1 | 100nF MLCC | 0402 | 1 | $0.01 | VCC1 decoupling (3.3V STM32 side) |
| C_CAN2a | 100nF MLCC | 0402 | 1 | $0.01 | VCC2 high-freq decoupling (5V bus side) |
| C_CAN2b | 10uF MLCC | 0805 | 1 | $0.11 | VCC2 bulk decoupling (5V bus side) |
| R_TERM | 120 ohm | 0402 | 1 | $0.01 | CAN bus termination |
| **PCB** | 4-layer, 160x90mm | FR4 ENIG | 1 | $4.50 | JLCPCB batch pricing (5 pcs) |

**Estimated unit cost (components + PCB): ~$18 USD** (at single-unit prototype quantities; ~$10 at 100+ volume)

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
| 2.0 | 2026-02-16 | Manas Pradhan | Replaced ASD (3× servo + 3× vibration motor) pin allocations with P-ASD (1× pump PWM + 6× solenoid + pressure sensor); updated J_STACK pinout, pin summary, and SPI message types |
| 3.0 | 2026-02-16 | Manas Pradhan | Moved P-ASD solenoid control from 6× direct GPIO (PA1/PA2/PA3/PC7/PD2/PB11) to PCF8574 I2C GPIO expander on Driver PCB; freed 6 STM32 pins; J_STACK pins 16-20, 39 now Reserved |
| 4.0 | 2026-02-20 | Manas Pradhan | Reassigned PA1 to COMP2 for 24V power failure detection; J_STACK pin 16 now PWR_FAIL (active-low output); added POWER_FAIL (0x14) and POWER_TELEMETRY (0x13) SPI messages; updated 5V source from CM5IO to J_STACK (UPS-backed TPS54531 on Driver PCB); added LED ring power switch (PA2 → Q2/Q3 P-MOSFET high-side) with J_LED 3-pin connector |
| 5.0 | 2026-02-20 | Manas Pradhan | Replaced non-isolated CAN transceiver (SN65HVD230/MCP2551) with ISO1050DUB isolated CAN transceiver (5 kV RMS galvanic isolation); J2 pin 3 changed from GND to GND_ISO; added creepage ≥6.4mm layout rule for isolation barrier; updated power budget (+15 mA on 3.3V); added ISO1050 + decoupling caps to BOM |
| 6.0 | 2026-02-20 | Manas Pradhan | Renamed all connectors from numeric (J1-J11) to descriptive names: J_SPI, J_CAN, J_IR, J_LC, J_NTC, J_SWD, J_PWR, J_SAFE; removed J3 (servo connector now via J_STACK to Driver PCB) |
| 7.0 | 2026-02-20 | Manas Pradhan | Replaced J_SPI (6-pin JST-SH + ribbon cable) with J_CM5 (2x20 pin socket) that mates directly with CM5IO 40-pin GPIO header; 5V from J_STACK now feeds CM5IO through J_CM5 pins 2/4; LED ring data (GPIO18) routes through J_CM5 pin 12 instead of jumper wire; eliminates ribbon cable between Controller PCB and CM5IO |
| 8.0 | 2026-02-20 | Manas Pradhan | Removed J_LC (HX711 load cell connector); pot load cell signals (PC0/PC1) now route via J_STACK pins 17-18 to Driver PCB J_SLD connector; removed J_PWR (redundant, 5V comes via J_STACK) |
| 9.0 | 2026-02-20 | Manas Pradhan | Removed J_NTC and both NTC thermistors (coil temp reported via CAN by induction module; ambient NTC not needed); freed PA4/PA5; removed ADC filter circuit, related BOM items (R14-R15, C14-C15), and ADC layout rule |
