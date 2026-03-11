---
created: 2026-03-06
modified: 2026-03-11
version: 1.9
status: Draft
---

# Unified PCB Design

## 1. Overview

This document covers the design of the single custom PCB for Epicura, merging the former Controller PCB and Driver PCB into one unified board. This board hosts the STM32G474RE microcontroller, all sensor interfaces, power conversion, actuator drivers, safety circuits, and the CAN transceiver — eliminating the J_STACK inter-board connector and reducing the 3-board stack to a 2-board stack (CM5IO + Unified PCB).

### 1.1 2-Board Architecture

```
┌─────────────────────────────────────┐
│  Board 2: Unified PCB (this doc)    │  160 x 90 mm (custom)
│  STM32 + power + drivers + sensors  │
├─────────────[ J_CM5 2x20 ]──────────┤  J_CM5 on bottom side of Unified PCB
│  Board 1: CM5 IO Board (CM5IO)      │  160 x 90 mm (off-the-shelf)
│  Raspberry Pi CM5 + peripherals     │
└─────────────────────────────────────┘
         ▲                    ▲
         │ 24V DC from PSU    │ 12V DC from UPS
```

### 1.2 Scope

| Item | Status | Notes |
|------|--------|-------|
| **Unified PCB** (this document) | Custom design required | STM32G474RE + power conversion + actuator drivers, 160x90mm, 4-layer |
| **CM5 IO Board (CM5IO)** | Off-the-shelf (Raspberry Pi official) | Commercial carrier board; no custom PCB needed |
| **Microwave induction surface** | Commercial module with CAN port (see [[../05-Subsystems/01-Induction-Heating\|Induction Heating]]) | Self-contained coil + driver; controlled via CAN bus |

### 1.3 Merger Rationale

| Benefit | Detail |
|---------|--------|
| Eliminates J_STACK | Removes 2 connectors + 40 inter-board signal routes |
| Reduces stack height | ~11mm shorter (one fewer stacking connector) |
| Saves ~$15.50/unit | 1 PCB instead of 2 + eliminated connectors + single assembly run |
| Shorter signal traces | STM32 routes directly to driver ICs (~20mm SPI, direct PWM) |
| Improved reliability | One fewer connector = one fewer failure point |
| Better GND plane | Continuous ground plane shared by digital and power sections |

### 1.4 Area Analysis

Combined components (~112 ICs/discretes + 17 connectors) occupy ~3,789 mm² of the ~12,000 mm² usable placement area = **32% utilization**. Well within typical PCB density limits (50-70% is tight). No board size increase needed.

---

## 2. Board-Level Block Diagram

```
24V DC Input ─── Polyfuse ─── SS54 ─── SMBJ24A TVS ─── 24V Internal Rail
                                                              │
                                    ┌─────────────────────────┼──────────────┐
                                    │                         │              │
                                    ▼                         ▼              ▼
                            ┌──────────────┐          ┌──────────────┐ VoltageDiv
                            │  MP1584EN #1 │          │  MP1584EN #2 │  100k/10k
                            │  24V → 12V   │          │  24V → 6.5V  │     │
                            │  3A max      │          │  3A (future) │     ▼
                            └──────┬───────┘          └──────┬───────┘  PA1 (COMP1)
                                   │                         │        Power Fail
                              12V Rail                   6.5V Rail
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                ┌───▼───┐    ┌───▼───┐    ┌─────▼─────┐
                │SLD Sol│    │Fans   │    │CID-2 LAct │
                │2×IRLML│    │2×IRLML│    │1×DRV8876  │
                └───────┘    └───────┘    └───────────┘

12V UPS Input ─── F5 (3A Polyfuse) ─── SS34 ─── SMBJ12A TVS ─── 12V UPS Rail
                                                                      │
                                                              ┌───────▼────────┐
                                                              │  TPS54531      │
                                                              │  12V → 5V      │
                                                              │  5A max        │
                                                              └───────┬────────┘
                                                                      │
                                                                  5V_MAIN ── D_OR1 (SS14) ──┐
                                                                                             │
USB-C VBUS ─── F_USB (500mA polyfuse) ──── 5V_USB ── D_OR2 (SS14) ──┼── 5V_MERGED
                       │                                              │
                 ┌─────▼───────┐                                      │
                 │  TP4056     │                                      │
                 │  Charger    │                                      │
                 └─────┬───────┘                                      │
                    Li-Ion Cell                                       │
                    (3.0-4.2V)                                        │
                       │                                              │
                 ┌─────▼───────┐                                      │
                 │  MT3608     │                                      │
                 │  Boost→5V   │                                      │
                 └─────┬───────┘                                      │
                   5V_BATT ──── D_OR3 (SS14) ─────────────────────────┘

                  5V_MERGED
                     │
              ┌──────▼──────┐
              │  AMS1117-3.3│        ┌──────────────┐
              │  5V → 3.3V  │        │  STM32G474RE │
              │  LDO        │        │  (LQFP-64)   │
              └──────┬──────┘        │              │
                     │               │  SPI2 ◄──────── J_CM5 (CM5IO GPIO)
                  3.3V Rail ────────►│  FDCAN1 ─────── ISO1050 → J_CAN
                                     │  USB ─────────── J_USB (PA11/PA12)
                                     │  TIM/GPIO ───── Actuator drivers
                                     │  I2C1 ──────── MLX90614, INA219,
                                     │                 PCF8574 x2, ADS1015
                                     └──────────────┘

                   ┌──────────────┐
         24V ──────┤  J_BLDC      │──── 24V BLDC Motor (integrated ESC)
                   └──────────────┘     PWM+EN+DIR direct from STM32

                   ┌──────────────┐
         24V ──────┤  INA219      │──── I2C1 (direct on-board)
                   │  Current Mon │
                   └──────────────┘
  .                ┌──────────────┐
         I2C1 ─────┤  PCF8574 #1  │──── P0-P5 → P-ASD Solenoid V1-V6 gates
                   │  GPIO Exp.   │     P6 ◄── CID-2 Full-Extend Limit
                   └──────────────┘     P7 ──► CID-1 Stepper ENA+
                                        (addr 0x20)

                   ┌──────────────┐
         I2C1 ─────┤  PCF8574 #2  │──── P0 → SLD Solenoid 1 (oil) gate
                   │  GPIO Exp.   │     P1 → SLD Solenoid 2 (water) gate
                   └──────────────┘     P2 → Status LED
                                        P3 → LED Ring Power Enable (Q_LED_N)
                                        P4-P7: Reserved
                                        (addr 0x21)

                   ┌──────────────┐
         12V ──────┤  TB6612FNG   │──── SLD 2× Peristaltic Pumps
                   └──────────────┘

                   ┌──────────────┐
                   │  P-ASD       │──── 6× Solenoid + 1× Diaphragm Pump
                   │  7× IRLML6344│     (via PCF8574 + PA0 PWM)
                   └──────────────┘
```

---

## 3. STM32G474RE Pin Allocation

### 3.1 Pin Map (LQFP-64)

```
STM32G474RE (LQFP-64) — Unified PCB Pin Assignment
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ┌─── SPI2: CM5 Communication (Master=CM5, Slave=STM32) ────┐  │
│  │  PB12 (SPI2_NSS)  ◄── CM5 GPIO8 (CE0)                    │  │
│  │  PB13 (SPI2_SCK)  ◄── CM5 GPIO11 (SCLK)                  │  │
│  │  PB14 (SPI2_MISO) ──► CM5 GPIO9 (MISO)                   │  │
│  │  PB15 (SPI2_MOSI) ◄── CM5 GPIO10 (MOSI)                  │  │
│  │  PB3  (GPIO IRQ)  ──► CM5 GPIO4 (data-ready, act-low)    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─── CAN: Microwave Surface ─────┐                            │
│  │  PB8  (FDCAN1_RX) ◄── ISO1050 RXD (on-board)                │
│  │  PB9  (FDCAN1_TX) ──► ISO1050 TXD (on-board)                │
│  │  500 kbps, isolation on-board                               │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── PWM+GPIO: BLDC Stirring Motor ─┐                         │
│  │  PA8  (TIM1_CH1)  ──► BLDC Motor PWM (10 kHz, speed)        │
│  │  PA4  (GPIO)      ──► BLDC Motor EN (enable)                │
│  │  PA5  (GPIO)      ──► BLDC Motor DIR (CW/CCW)               │
│  └─────────────────────────────────────┘                       │
│                                                                │
│  ┌─── P-ASD: Pneumatic Seasoning Dispenser ─┐                  │
│  │  PA0  (TIM2_CH1)  ──► P-ASD Pump PWM (12V diaphragm)        │
│  │  Solenoids V1-V6: driven by PCF8574 I2C GPIO expander       │
│  │    (I2C1, addr 0x20, outputs P0-P5, on-board)               │
│  │  I2C1 (PA15/PB7)  ──► ADS1015 Pressure Sensor (0x48)         │
│  │                   ──► PCF8574 Solenoid Expander (0x20)      │
│  └──────────────────────────────────────────┘                  │
│                                                                │
│  ┌─── CID: Coarse Ingredients Dispenser ──┐                    │
│  │  CID-1: NEMA 23 Stepper Motor (external driver)             │
│  │  PA10 (TIM1_CH3)  ──► CID-1 Stepper PUL+ (via 100R)        │
│  │  PB4  (GPIO)      ──► CID-1 Stepper DIR+ (via 100R)        │
│  │  PCF8574 P7       ──► CID-1 Stepper ENA+ (via 100R)        │
│  │  CID-2: DC Linear Actuator (DRV8876 #2)                    │
│  │  PB5  (GPIO)      ──► CID-2 Linear Actuator EN (DRV8876)    │
│  │  PC2  (GPIO)      ──► CID-2 Linear Actuator PH/DIR          │
│  │  PB6  (GPIO/EXTI) ◄── CID-1 Home Limit (NC, 10k PU)        │
│  │  PB11              ── Reserved (freed from CID-1 extend)    │
│  │  PD2  (GPIO/EXTI) ◄── CID-2 Home Limit (NC, 10k PU)        │
│  │  PCF8574 P6       ◄── CID-2 Full-Extend Limit (NC)          │
│  └─────────────────────────────────────────┘                   │
│                                                                │
│  ┌─── SLD: Standard Liquid Dispenser ──┐                       │
│  │  PC3  (GPIO)      ──► SLD-OIL Pump PWM (TB6612 PWMA)        │
│  │  PC4  (GPIO)      ──► SLD-OIL Pump DIR (TB6612 AIN1)        │
│  │  PC5  (GPIO)      ──► SLD-WATER Pump PWM (TB6612 PWMB)      │
│  │  PC6  (GPIO)      ──► SLD-WATER Pump DIR (TB6612 BIN1)      │
│  │  PCF8574 #2 P0    ──► SLD-OIL Solenoid (via MOSFET)         │
│  │  PCF8574 #2 P1    ──► SLD-WATER Solenoid (via MOSFET)       │
│  │  PC11 (GPIO)      ──► HX711 SCK (SLD oil reservoir)         │
│  │  PC12 (GPIO)      ◄── HX711 DOUT (SLD oil reservoir)        │
│  │  PC9  (GPIO)      ──► HX711 SCK (SLD water reservoir)       │
│  │  PC10 (GPIO)      ◄── HX711 DOUT (SLD water reservoir)      │
│  └─────────────────────────────────────────┘                   │
│                                                                │
│  ┌─── Exhaust Fans (2x 120mm) ────┐                            │
│  │  PA6  (TIM3_CH1)  ──► Fan 1 PWM (25 kHz)                    │
│  │  PB10 (TIM2_CH3)  ──► Fan 2 PWM (25 kHz)                    │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Audio ──────────────────────┐                            │
│  │  PC7  (TIM8_CH2)  ──► Piezo Buzzer PWM (via MOSFET)         │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── USB: Native USB 2.0 Full-Speed ───────────────────────┐  │
│  │  PA11 (USB_DM)    ◄─► 22R ── USBLC6-2SC6 ── J_USB D-     │  │
│  │  PA12 (USB_DP)    ◄─► 22R ── USBLC6-2SC6 ── J_USB D+     │  │
│  │  PA3  (ADC)       ◄── VBUS detect (100k/100k divider)     │  │
│  │  BOOT0 ── SW_BOOT (tactile to 3.3V) + 10k pull-down       │  │
│  │  CC1/CC2: 5.1kR to GND (UFP identification)               │  │
│  │  VBUS: 500mA polyfuse → 5V_USB → Schottky-OR              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─── I2C1: Sensors & Peripherals ──┐                          │
│  │  PA15 (I2C1_SCL)  ──► MLX90614 (0x5A) — J_IR                │
│  │  PB7  (I2C1_SDA)  ◄─► INA219 (0x40) — on-board              │
│  │                    ◄─► PCF8574 #1 (0x20) — on-board         │
│  │                    ◄─► PCF8574 #2 (0x21) — on-board         │
│  │                    ◄─► ADS1015 (0x48) — J_PRES            │
│  │  100 kHz, 4.7k pull-ups to 3.3V                             │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Load Cells (HX711) ───┐                            │
│  │  PC0  (GPIO)      ──► HX711 SCK (pot load cell)             │
│  │  PC1  (GPIO)      ◄── HX711 DOUT (pot load cell)            │
│  │  PC11 (GPIO)      ──► HX711 SCK (SLD oil reservoir)         │
│  │  PC12 (GPIO)      ◄── HX711 DOUT (SLD oil reservoir)        │
│  │  PC9  (GPIO)      ──► HX711 SCK (SLD water reservoir)       │
│  │  PC10 (GPIO)      ◄── HX711 DOUT (SLD water reservoir)      │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── Power Fail Detection ───────┐                            │
│  │  PA1  (COMP1_INP) ◄── 24V voltage divider (100k/10k)        │
│  │       COMP1 threshold ~1.5V → trips at 24V < 16.5V          │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── LED Ring Power Control ────┐                             │
│  │  PCF8574 #2 P3   ──► Q_LED_N gate (2N7002, N-MOSFET)        │
│  │       Q_LED_N drain ──► Q_LED_P gate (SI2301, P-MOSFET)     │
│  │       Q_LED_P switches 5V to LED ring via J_LED             │
│  │       Data: CM5 GPIO18 → J_CM5 pin 12 → J_LED pin 2         │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── GPIO: Safety & Control ─────┐                            │
│  │  PB0  (GPIO)      ──► Safety Relay (via MOSFET Q_RLY)       │
│  │  PB1  (GPIO)      ◄── Pot Detection (reed switch)           │
│  │  PB2  (GPIO/EXTI) ◄── E-Stop Button (active-low)            │
│  └─────────────────────────────────┘                           │
│                                                                │
│  ┌─── PCF8574 #2 (0x21): GPIO Headroom ─┐                     │
│  │  P0 ──► SLD Solenoid 1 (oil, IRLML6344)                     │
│  │  P1 ──► SLD Solenoid 2 (water, IRLML6344)                   │
│  │  P2 ──► Status LED (green, 330R, active-low)                │
│  │  P3 ──► LED Ring Power (Q_LED_N gate)                       │
│  │  P4-P7: Reserved (future expansion)                         │
│  └───────────────────────────────────────┘                     │
│                                                                │
│  Debug: SWD via PA13 (SWDIO) / PA14 (SWCLK)                    │
│  Power: 3.3V / GND from on-board LDO                           │
│  Clock: 8 MHz HSE (PF0, PF1)                                   │
│  Clock: 32.768 kHz LSE (PC14, PC15) for RTC                    │
│  Reset: NRST with 100nF cap + external reset button            │
│  BOOT0: Tied low via 10k pull-down (jumper for bootloader)     │
└────────────────────────────────────────────────────────────────┘
```

### 3.2 Pin Summary Table

| Pin | Function | Peripheral | Direction | Destination | Subsystem |
|-----|----------|------------|-----------|-------------|-----------|
| PA0 | TIM2_CH1 | P-ASD Pump PWM | Output | IRLML6344 gate | P-ASD |
| PA1 | COMP1_INP | 24V Power Fail Detection | Input | Voltage divider | Power |
| PA2 | — | Available (moved to PCF8574 #2 P3) | — | Freed: TIM2_CH3, USART2_TX, ADC1_IN3 | — |
| PA3 | ADC | USB VBUS Detect | Input | 100k/100k divider from 5V_USB | USB |
| PA4 | GPIO | BLDC Motor EN | Output | J_BLDC pin 4 (100R series) | Main |
| PA5 | GPIO | BLDC Motor DIR | Output | J_BLDC pin 5 (100R series) | Main |
| PA6 | TIM3_CH1 | Exhaust Fan 1 PWM | Output | IRLML6344 gate → J_FAN | Exhaust |
| PA7 | — | Available (moved to PCF8574 #2 P0) | — | Freed: TIM3_CH2, SPI1_MOSI, ADC2_IN4 | — |
| PA8 | TIM1_CH1 | BLDC Motor PWM (10 kHz) | Output | J_BLDC pin 3 (100R series) | Main |
| PA9 | — | Available (moved to PCF8574 #2 P1) | — | Freed: TIM1_CH2, USART1_TX, TIM15_CH1 | — |
| PA10 | TIM1_CH3 | CID-1 Stepper PUL+ | Output | J_CID pin 1 (100R series) | CID |
| PA11 | USB_DM | USB D- | Bidir | USBLC6-2SC6 ESD → 22R → J_USB | USB |
| PA12 | USB_DP | USB D+ | Bidir | USBLC6-2SC6 ESD → 22R → J_USB | USB |
| PA13 | SWDIO | SWD Debug | Bidir | J_SWD | Debug |
| PA14 | SWCLK | SWD Debug | Input | J_SWD | Debug |
| PA15 | I2C1_SCL | MLX90614/INA219/PCF8574 x2/ADS1015 | Output | J_IR, J_PRES, on-board ICs | Sensors |
| PB0 | GPIO | Safety Relay | Output | Q_RLY (2N7002) | Safety |
| PB1 | GPIO | Pot Detection | Input | Reed switch (10k pull-up) | Safety |
| PB2 | GPIO (EXTI) | E-Stop | Input | NC button (10k pull-up, RC debounce) | Safety |
| PB3 | GPIO | IRQ to CM5 | Output | J_CM5 pin 7 | Comms |
| PB4 | GPIO | CID-1 Stepper DIR+ | Output | J_CID pin 3 (100R series) | CID |
| PB5 | GPIO | CID Linear Actuator 2 EN | Output | DRV8876 #2 EN | CID |
| PB6 | GPIO (EXTI) | CID-1 Home Limit Switch | Input | J_CID pin 9 (10k pull-up, 100nF debounce) | CID |
| PB7 | I2C1_SDA | MLX90614/INA219/PCF8574 x2/ADS1015 | Bidir | J_IR, J_PRES, on-board ICs | Sensors |
| PB8 | FDCAN1_RX | CAN RX | Input | ISO1050 RXD (on-board) | CAN |
| PB9 | FDCAN1_TX | CAN TX | Output | ISO1050 TXD (on-board) | CAN |
| PB10 | TIM2_CH3 | Exhaust Fan 2 PWM | Output | IRLML6344 gate → J_FAN | Exhaust |
| PB11 | — | Reserved (freed from CID-1 extend) | — | Unassigned | — |
| PB12 | SPI2_NSS | CM5 CE0 | Input | J_CM5 pin 24 | Comms |
| PB13 | SPI2_SCK | CM5 SCLK | Input | J_CM5 pin 23 | Comms |
| PB14 | SPI2_MISO | CM5 MISO | Output | J_CM5 pin 21 | Comms |
| PB15 | SPI2_MOSI | CM5 MOSI | Input | J_CM5 pin 19 | Comms |
| PC0 | GPIO | HX711 SCK (pot load cell) | Output | J_SLD pin 9 | Sensors |
| PC1 | GPIO | HX711 DOUT (pot load cell) | Input | J_SLD pin 10 | Sensors |
| PC2 | GPIO | CID Linear Actuator 2 PH | Output | DRV8876 #2 PH | CID |
| PC3 | GPIO | SLD Pump 1 PWM | Output | TB6612 PWMA | SLD |
| PC4 | GPIO | SLD Pump 1 DIR | Output | TB6612 AIN1 | SLD |
| PC5 | GPIO | SLD Pump 2 PWM | Output | TB6612 PWMB | SLD |
| PC6 | GPIO | SLD Pump 2 DIR | Output | TB6612 BIN1 | SLD |
| PC7 | TIM8_CH2 | Buzzer PWM | Output | 2N7002 gate → J_BUZZER | Audio |
| PC8 | — | Available (moved to PCF8574 #2 P2) | — | Freed: General GPIO | — |
| PC9 | GPIO | HX711 SCK (SLD water reservoir) | Output | J_SLD pin 15 | SLD |
| PC10 | GPIO | HX711 DOUT (SLD water reservoir) | Input | J_SLD pin 16 | SLD |
| PC11 | GPIO | HX711 SCK (SLD oil reservoir) | Output | J_SLD pin 13 | SLD |
| PC12 | GPIO | HX711 DOUT (SLD oil reservoir) | Input | J_SLD pin 14 | SLD |
| PD2 | GPIO (EXTI) | CID-2 Home Limit Switch | Input | J_CID pin 10 (10k pull-up, 100nF debounce) | CID |

### 3.3 Complete Pin Usage Summary

| Port | Used Pins | Total Used | Available |
|------|-----------|------------|-----------|
| PA | PA0-PA15 | 16 | — |
| PB | PB0-PB15 | 16 | — |
| PC | PC0-PC12, PC14-PC15 | 15 | — |
| PD | PD2 | 1 | — |

---

## 4. Power Supply

### 4.1 24V Input Protection Chain

```
24V from PSU ──── F1 (5A Polyfuse) ──── D1 (SS54 Schottky) ────┬── D2 (SMBJ24A TVS) ──── 24V Internal
                                                               │
                                                              GND
```

| Component | Part | Function |
|-----------|------|----------|
| F1 | 5A resettable polyfuse (1812 package) | Overcurrent protection, self-resetting |
| D1 | SS54 (5A, 40V Schottky) | Reverse polarity protection (Vf = 0.5V drop) |
| D2 | SMBJ24A (24V TVS, 600W) | Transient voltage suppression from PSU spikes |

### 4.2 12V UPS Input Protection Chain

```
12V from UPS ──── F5 (3A Polyfuse) ──── D_UPS1 (SS34 Schottky) ──┬── D_UPS2 (SMBJ12A TVS) ──── 12V UPS Rail
                                                                    │
                                                                   GND
```

| Component | Part | Function |
|-----------|------|----------|
| F5 | 3A resettable polyfuse (1812 package) | Overcurrent protection, self-resetting |
| D_UPS1 | SS34 (3A, 40V Schottky) | Reverse polarity protection (Vf = 0.5V drop) |
| D_UPS2 | SMBJ12A (12V TVS, 600W) | Transient voltage suppression |

### 4.3 24V → 12V Rail (MP1584EN #1)

| Parameter | Value |
|-----------|-------|
| Output Voltage | 12V |
| Max Current | 3A |
| Load | SLD solenoids (2x 0.5A), P-ASD solenoids (6x 0.5A, max 1 at a time), P-ASD pump (0.8A), exhaust fans (2x 0.5A), linear actuators (2x 1.5A peak), peristaltic pumps (2x 0.6A) |
| Inductor | 33uH, CDRH104R (Sumida), Isat > 4A |
| Output Cap | 2x 22uF MLCC (X5R, 25V) + 100uF electrolytic (25V) |
| Feedback Resistors | R_top = 140k, R_bot = 10k → 12.0V |
| Schottky Diode | SS34 (3A, 40V) for bootstrap |
| Protection | 1.5A polyfuse + SMBJ12A TVS on output |

### 4.4 24V → 6.5V Rail (MP1584EN #2)

| Parameter | Value |
|-----------|-------|
| Output Voltage | 6.5V |
| Max Current | 3A |
| Load | Available for future use (was DS3225 servo) |
| Inductor | 22uH, CDRH104R (Sumida), Isat > 4A |
| Output Cap | 2x 22uF MLCC (X5R, 16V) + 470uF electrolytic (10V, low-ESR) |
| Feedback Resistors | R_top = 71.5k, R_bot = 10k → 6.52V |
| Protection | 3A polyfuse + SMBJ6.5A TVS on output |

> [!note]
> The 6.5V rail is retained for future use. The DS3225 servo has been replaced with a 24V BLDC motor with integrated driver/ESC, powered directly from the 24V rail via J_BLDC. The MP1584EN #2 and its output components remain populated but unloaded.

### 4.5 12V UPS → 5V Rail (TPS54531)

| Parameter | Value |
|-----------|-------|
| IC | TPS54531DDAR (SOIC-8) |
| Input Voltage | 12V (from UPS-backed DC input) |
| Output Voltage | 5V |
| Max Current | 5A |
| Load | CM5 (up to 3A), 3.3V LDO (0.17A), buzzer (0.03A), LED ring (1A peak) |
| Inductor | 10uH, CDRH127 (12.7x12.7mm), Isat > 6A |
| Output Cap | 2x 22uF MLCC (X5R, 10V) + 220uF electrolytic (10V) |
| Feedback Resistors | R_top = 52.3k, R_bot = 10k → 4.98V |
| Switching Frequency | 570 kHz (internal oscillator) |
| Protection | Integrated overcurrent, thermal shutdown, UVLO |

### 4.6 Three-Source 5V Schottky-OR → 3.3V Rail (AMS1117-3.3 LDO)

Three independent 5V sources are OR'd via SS14 Schottky diodes to create `5V_MERGED`. This allows the STM32 to be powered from any single source — the 24V PSU (via TPS54531), a USB-C cable, or the onboard Li-Ion battery (via MT3608 boost).

```
5V_MAIN (TPS54531, UPS-backed) ── D_OR1 (SS14) ──┐
                                                    │
5V_USB  (USB-C VBUS, polyfuse)  ── D_OR2 (SS14) ──┼── 5V_MERGED
                                                    │
5V_BATT (MT3608 boost, Li-Ion)  ── D_OR3 (SS14) ──┘
    │
    ├──── C_OR: 10uF ceramic (merged rail stabilization)
    ├──── C_LDO_IN: 10uF ceramic (input bypass)
    │
    ▼
┌──────────────────┐
│  U_LDO: AMS1117  │
│  or AP2112K-3.3  │
│  VIN ◄── 5V_MERGED│
│  VOUT ──► 3.3V   │
│  GND ──► GND     │
│  Dropout: 1.0V   │
│  Iout max: 800mA │
└──────────────────┘
    │
    ├──── C_LDO_OUT: 10uF ceramic (output bypass)
    ├──── 100nF ceramic (high-freq decoupling)
    │
    ▼
3.3V Rail ──► STM32 VDD, VDDA, sensors, pull-ups, ISO1050 VCC1
```

| Component | Part | Function |
|-----------|------|----------|
| D_OR1-3 | SS14 (1A, 40V Schottky) | Prevents backfeed between 5V sources (Vf ~0.35V) |
| C_OR | 10uF MLCC (0805, 10V) | Merged rail stabilization |

> [!note]
> The Schottky-OR introduces ~0.35V drop, so the LDO sees ~4.65V input minimum. With AMS1117's 1.0V dropout, the 3.3V output margin is 1.35V — adequate. When powered from battery alone, MT3608 output is regulated to 5.0V.

### 4.7 24V Power Failure Detection

```
24V Internal ─── R_DIV1 (100k) ──┬── R_DIV2 (10k) ─── GND
                                  │
                                  ├── C_DIV (100nF) ─── GND
                                  │
                                  └── PA1 (COMP1_INP)
```

| Parameter | Value |
|-----------|-------|
| Divider Ratio | 10k / (100k + 10k) = 1/11 |
| Nominal Voltage at PA1 | 24V x 1/11 = 2.18V |
| Threshold (COMP1 ref) | ~1.5V (internal DAC reference) |
| Trip Voltage (24V rail) | 1.5V x 11 = 16.5V |
| Recovery Threshold | ~20V (with 2s debounce in firmware) |
| Filter Cap | 100nF on divider midpoint (noise filtering) |
| Response Time | <100us (hardware comparator interrupt) |

### 4.8 Per-Rail Protection

| Rail | Polyfuse | TVS Diode | Notes |
|------|----------|-----------|-------|
| 12V | 1.5A (0805) | SMBJ12A | Protects solenoid/fan/actuator branch |
| 6.5V | 3A (1206) | SMBJ6.5A | Available for future use |
| 5V | — | — | Protected at UPS input (F5 + D_UPS2); TPS54531 has integrated OCP |

### 4.9 Decoupling

- **Per VDD pin:** 100nF MLCC placed within 5mm of each VDD/VSS pin pair
- **VDDA (analog supply):** 1uF MLCC + ferrite bead from main 3.3V
- **Bulk:** 10uF MLCC at LDO output, 10uF MLCC at LDO input
- **Total decoupling caps:** 6-8x 100nF + 2x 10uF + 1x 1uF (STM32) + per-IC decoupling

### 4.10 Power Budget Summary

| Rail | Source | Typical (A) | Peak (A) | Headroom | Notes |
|------|--------|------------|----------|----------|-------|
| 3.3V (0.8A max) | 5V → AMS1117 LDO | 0.09 | 0.17 | 79% | STM32, sensors, pull-ups |
| 5V_MERGED (5A max) | 3-way Schottky-OR: TPS54531 / USB-C / MT3608 | 1.5 | 4.0 | 20% | CM5 (3A peak) + LDO (0.17A) + buzzer + LED; ~0.35V Schottky drop |
| 12V (3A max) | 24V → MP1584EN #1 | 1.9 | 3.0 | 0% | Actuators only (not needed during power fail) |
| 6.5V (3A max) | 24V → MP1584EN #2 | 0 | 0 | 100% | Available for future use |
| 24V direct | 24V input | 1.0 | 3.0 | — | BLDC stirring motor (integrated ESC, via J_BLDC) |
| **24V input** | **Mean Well PSU** | **~2.0** | **~2.5** | Within PSU 3.2A rating | |
| **12V UPS input** | **External UPS** | **1.5** | **4.0** | Within 5A fuse | UPS-backed |

---

## 5. CM5 to STM32 SPI Interface

### 5.1 Physical Connection

The Unified PCB sits on top; its **J_CM5** 2x20 pin socket (2.54mm pitch) is mounted on the **bottom side** of the board, pointing downward to mate with the CM5 IO Board's upward-facing 40-pin GPIO header below. No ribbon cable is needed; the boards stack directly. SPI, IRQ, LED ring data, 5V power, and GND all route through this single connector.

```
CM5 IO Board (40-pin GPIO Header)       Unified PCB (J_CM5, 2x20 socket)
┌───────────────────────┐               ┌───────────────────────┐
│                       │   stacking    │                       │
│  Pin  2  (5V)         ├◄──────────────┤ 5V out (UPS-backed)   │
│  Pin  4  (5V)         ├◄──────────────┤ 5V out (UPS-backed)   │
│  Pin  7  (GPIO4)      │◄──────────────┤ PB3  (IRQ, act-low)   │
│  Pin 12  (GPIO18)     ├──────────────►│ LED ring data (pass)  │
│  Pin 19  (GPIO10/MOSI)├──────────────►│ PB15 (SPI2_MOSI)      │
│  Pin 21  (GPIO9/MISO) │◄──────────────┤ PB14 (SPI2_MISO)      │
│  Pin 23  (GPIO11/SCLK)├──────────────►│ PB13 (SPI2_SCK)       │
│  Pin 24  (GPIO8/CE0)  ├──────────────►│ PB12 (SPI2_NSS)       │
│  Pin 6,9,14,20,25,    │               │                       │
│  30,34,39 (GND)       ├──────────────►│ GND                   │
│  (all other pins)     ├───── N/C ─────┤ (not connected)       │
│                       │               │                       │
└───────────────────────┘               └───────────────────────┘

Connection: Direct board-to-board stacking (Unified PCB on top, CM5IO below)
Logic level: 3.3V on both sides (no level shifter needed)
5V direction: Unified PCB → CM5IO (UPS-backed power)
```

### 5.2 SPI Configuration

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

### 5.3 SPI Transaction Protocol

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
3. STM32 simultaneously clocks out last-prepared response on MISO (or 0x00 padding)
4. CM5 deasserts NSS high
5. STM32 processes command, prepares response, pulses IRQ if needed

**Event flow (STM32 → CM5):**
1. STM32 prepares telemetry/event frame in TX buffer
2. STM32 asserts IRQ low (10us pulse)
3. CM5 detects IRQ on GPIO4 interrupt
4. CM5 initiates SPI read transaction (sends dummy bytes on MOSI, reads response on MISO)
5. STM32 deasserts IRQ after data is clocked out

### 5.4 Message Types

| Message | Type Code | Direction | Payload |
|---------|-----------|-----------|---------|
| SET_TEMP | 0x01 | CM5 → STM32 | target_temp (float), ramp_rate (float) |
| SET_STIR | 0x02 | CM5 → STM32 | pattern (uint8), speed_rpm (uint16) |
| DISPENSE_PASD | 0x03 | CM5 → STM32 | cartridge_id (uint8: 1-6), target_g (uint16) |
| E_STOP | 0x04 | CM5 → STM32 | reason_code (uint8) |
| HEARTBEAT | 0x05 | Bidirectional | uptime_ms (uint32) |
| SET_LINEAR_ACT | 0x06 | CM5 → STM32 | actuator_id (uint8), direction (uint8), speed_pct (uint8) |
| SET_PUMP | 0x07 | CM5 → STM32 | pump_id (uint8), direction (uint8), speed_pct (uint8), volume_ml (uint16) |
| SET_PASD_PUMP | 0x08 | CM5 → STM32 | speed_pct (uint8), state (uint8: 0=off, 1=on) |
| SET_SOLENOID | 0x09 | CM5 → STM32 | valve_id (uint8), state (uint8: 0=off, 1=on) |
| SET_BUZZER | 0x0A | CM5 → STM32 | pattern (uint8), duration_ms (uint16) |
| PURGE_PASD | 0x0B | CM5 → STM32 | cartridge_id (uint8: 1-6, or 0xFF=all) |
| PRESSURE_STATUS | 0x0C | CM5 → STM32 | — (returns pressure_bar, 2 bytes fixed-point) |
| TELEMETRY | 0x10 | STM32 → CM5 | ir_temp, can_coil_temp, weight, duty_pct |
| SENSOR_DATA | 0x11 | STM32 → CM5 | adc_values[], ir_temp, load_cells[] |
| STATUS | 0x12 | STM32 → CM5 | safety_state, error_code, flags |
| POWER_TELEMETRY | 0x13 | STM32 → CM5 | bus_voltage_mV (uint16), current_mA (uint16), power_mW (uint16) |
| POWER_FAIL | 0x14 | STM32 → CM5 | state (uint8: 0=OK, 1=FAIL), voltage_mV (uint16) |
| ACK | 0xFF | Bidirectional | ack_msg_id, result_code |

**Buzzer Pattern Definitions:**

| Pattern Code | Name | Description |
|--------------|------|-------------|
| 0x00 | OFF | Buzzer off (silent) |
| 0x01 | BEEP | Single short beep (100ms, 2.5 kHz) |
| 0x02 | ERROR | Continuous alarm (1 kHz, until stopped) |
| 0x03 | COMPLETE | 3 ascending beeps (200ms each, 2-3 kHz sweep) |
| 0x04 | WARNING | Single long beep (500ms, 2 kHz) |
| 0x05 | TIMER_START | 2 quick beeps (100ms, 3 kHz) |
| 0x06 | E_STOP | Pulsing alarm (alternating 1-2 kHz) |
| 0x07 | STAGE_CHANGE | Ascending tone sweep (300ms, 2-3 kHz) |

### 5.5 STM32 SPI Slave Implementation Notes

- Configure SPI2 in slave mode with hardware NSS
- Use DMA for both TX and RX to avoid CPU overhead
- Double-buffer TX: while one buffer is being transmitted, the next telemetry frame is prepared in the other
- IRQ line driven by GPIO output (PB3), not tied to SPI hardware
- Timeout: if CM5 does not read within 500ms of IRQ assertion, STM32 enters WARNING state

---

## 6. Actuator Driver Circuits

### 6.1 24V BLDC Motor with Integrated Driver

The stirring mechanism uses a 24V BLDC motor with integrated driver/ESC, connected directly to the 24V rail. The motor accepts a 10 kHz PWM signal for speed control, plus digital EN and DIR signals. No external H-bridge needed.

```
24V Rail ──┬── J_BLDC Pin 1 (24V)
           │
          GND ── J_BLDC Pin 2 (GND)

PA8 (TIM1_CH1, BLDC_PWM) ── 100R ── J_BLDC Pin 3 (PWM)
PA4 (GPIO, BLDC_EN)       ── 100R ── J_BLDC Pin 4 (EN)
PA5 (GPIO, BLDC_DIR)      ── 100R ── J_BLDC Pin 5 (DIR)
                                      J_BLDC Pin 6 (FG) ── NC (tachometer, deferred)
```

| Parameter | Value |
|-----------|-------|
| Motor | 24V BLDC, 30-50 kg-cm, integrated ESC (model TBD) |
| PWM Frequency | 10 kHz |
| Duty Cycle Range | 0-100% (speed proportional) |
| EN Pin | Digital high = motor enabled, low = disabled |
| DIR Pin | Digital high = CW, low = CCW |
| FG Pin | Tachometer feedback (NC for prototype; PA3 reserved for future) |
| Supply | 24V direct from PSU rail |
| Typical Current | ~2A |
| Peak Current | ~3A (stall/startup) |
| Signal Protection | 100R series resistors on PWM, EN, DIR lines |
| Gate Pull-down | 10k on EN (motor disabled during boot) |

> [!warning]
> The BLDC motor draws up to 3A peak from the 24V rail. Combined with other 24V loads, the Mean Well LRS-75-24 (3.2A) may be tight. Monitor total 24V current via INA219; consider upgrading to LRS-100-24 (4.2A) if headroom is insufficient.

### 6.2 P-ASD Solenoid Valves (6x)

Six 12V normally-closed solenoid valves for P-ASD cartridge air control, driven by low-side N-MOSFETs with flyback protection. MOSFET gates driven by **PCF8574 I2C GPIO expander** (address 0x20) on-board.

```
12V Rail ──── Solenoid Coil ──┬── Drain (IRLML6344)
                              │
                         SS14 Flyback ─── 12V
                              │
                         10k Pull-down
                              │
PCF8574 P0-P5 (I2C1, 0x20) ── 100R Gate Resistor ── Gate
                              │
                             GND ── Source
```

| Parameter | Value |
|-----------|-------|
| MOSFET | IRLML6344 (SOT-23) |
| Vds(max) | 30V |
| Rds(on) | 29 mR @ Vgs=4.5V |
| Id(max) | 5A |
| Flyback Diode | SS14 (1A, 40V Schottky) |
| Gate Resistor | 100R (limits dI/dt, reduces EMI) |
| Gate Pull-down | 10k to GND (safe state during boot/reset) |
| Solenoid Current | ~0.5A per valve (max 1 energized at a time) |

**PCF8574 Output Allocation:**

| Valve | PCF8574 Pin | Cartridge |
|-------|-------------|-----------|
| Solenoid V1 | P0 | P-ASD-1 (Turmeric) |
| Solenoid V2 | P1 | P-ASD-2 (Chili) |
| Solenoid V3 | P2 | P-ASD-3 (Cumin) |
| Solenoid V4 | P3 | P-ASD-4 (Salt) |
| Solenoid V5 | P4 | P-ASD-5 (Garam Masala) |
| Solenoid V6 | P5 | P-ASD-6 (Coriander) |
| CID-2 Full-Extend Limit | P6 | CID limit switch input (NC to GND) |
| CID-1 Stepper ENA+ | P7 | Stepper driver enable via 100R to J_CID pin 5 |

**PCF8574 Configuration:**

| Parameter | Value |
|-----------|-------|
| IC | PCF8574 (SOIC-16) |
| I2C Address | 0x20 (A0=A1=A2=GND) |
| I2C Bus | I2C1 (PA15 SCL / PB7 SDA), shared with MLX90614 (0x5A), INA219 (0x40), ADS1015 (0x48) |
| Output Current | 25 mA sink per pin (sufficient for IRLML6344 gate charge) |
| Decoupling | 100nF MLCC on VDD |

### 6.3 PCF8574 #2 — GPIO Headroom Expander (0x21)

A second PCF8574 at I2C address 0x21 (A0=VCC, A1=A2=GND) offloads 4 simple on/off digital outputs from the STM32, freeing PA7, PA9, PC8, and PA2 for future use. These signals have no timing requirements and tolerate the ~1 ms I2C write latency.

**PCF8574 #2 Output Allocation:**

| Pin | Signal | Previous STM32 Pin | Notes |
|-----|--------|--------------------|-------|
| P0 | SLD Solenoid 1 (oil) | PA7 | On/off, no timing requirement |
| P1 | SLD Solenoid 2 (water) | PA9 | On/off, no timing requirement |
| P2 | Status LED (green) | PC8 | Active-low, 330R, latency irrelevant |
| P3 | LED Ring Power Enable | PA2 | On/off switch via Q_LED_N, not PWM |
| P4 | Reserved | — | Future expansion |
| P5 | Reserved | — | Future expansion |
| P6 | Reserved | — | Future expansion |
| P7 | Reserved | — | Future expansion |

**Freed STM32 Pins:**

| Pin | Available Alternate Functions | Potential Future Use |
|-----|-------------------------------|---------------------|
| PA7 | TIM3_CH2, SPI1_MOSI, ADC2_IN4 | Extra PWM, SPI device, analog input |
| PA9 | TIM1_CH2, USART1_TX, TIM15_CH1 | Extra PWM, serial debug output |
| PC8 | General GPIO | Digital I/O |
| PA2 | TIM2_CH3, USART2_TX, ADC1_IN3 | Analog input, serial, PWM |

Combined with existing free pins (PB11, PC13-15), the STM32 now has **7-8 unassigned GPIO** — substantial headroom for future features.

**PCF8574 #2 Configuration:**

| Parameter | Value |
|-----------|-------|
| IC | PCF8574 (SOIC-16) |
| I2C Address | 0x21 (A0=VCC, A1=GND, A2=GND) |
| I2C Bus | I2C1 (PA15 SCL / PB7 SDA), shared with PCF8574 #1 (0x20), MLX90614 (0x5A), INA219 (0x40), ADS1015 (0x48) |
| Output Current | 25 mA sink per pin (sufficient for IRLML6344 gate charge) |
| Decoupling | 100nF MLCC on VDD |
| Placement | Zone D, adjacent to U_EXP (PCF8574 #1) |
| Bus Capacitance | Adds ~10-15 pF; total 5 devices well under 400 pF limit |

> [!note]
> All MOSFET gate pull-downs (10k to GND) remain on the gate resistor side, ensuring safe boot state regardless of PCF8574 #2 I2C initialization order. The existing 4.7kΩ I2C pull-ups require no changes — 5 devices at 100 kHz with 4.7kΩ is standard and safe.

### 6.4 SLD Solenoid Valves (2x)

Two 12V solenoid valves for SLD drip prevention, driven by low-side N-MOSFETs with flyback protection. MOSFET gates driven by **PCF8574 #2 I2C GPIO expander** (address 0x21) on-board — moved from direct STM32 GPIO (PA7/PA9) to free pins for future use.

```
12V Rail ──── Solenoid Coil ──┬── Drain (IRLML6344)
                              │
                         SS14 Flyback ─── 12V
                              │
                         10k Pull-down
                              │
PCF8574 #2 P0/P1 (I2C1, 0x21) ── 100R Gate Resistor ── Gate
                              │
                             GND ── Source
```

| Parameter | Value |
|-----------|-------|
| MOSFET | IRLML6344 (SOT-23) |
| Flyback Diode | SS14 (1A, 40V Schottky) |
| Gate Resistor | 100R |
| Gate Pull-down | 10k to GND |
| Solenoid Current | ~0.5A per valve |

### 6.5 Exhaust Fans (2x)

Two independent 120mm 12V brushless DC fans, driven by PWM via low-side MOSFETs.

```
12V Rail ──── Fan (+) ──── Fan (-) ──┬── Drain (IRLML6344)
                                     │
                                SS14 Flyback ─── 12V
                                     │
                                10k Pull-down
                                     │
PA6/PB10 ── 100R ── Gate
                                     │
                                    GND ── Source
```

| Parameter | Value |
|-----------|-------|
| Fan Size | 120mm diameter |
| PWM Frequency | 25 kHz (above audible range) |
| MOSFET | IRLML6344 (SOT-23) |
| Flyback Diode | SS14 |
| Fan Current | ~0.3-0.5A typical per fan |

### 6.6 CID — Coarse Ingredients Dispenser

CID-1 uses a NEMA 23 stepper motor with an external pulse/direction/enable driver (DM542/TB6600-class). CID-2 retains the DC linear actuator with DRV8876 H-bridge. The stepper driver is powered from the 24V input rail via J_CID.

#### 6.6.1 CID-1 Stepper Motor (NEMA 23 + External Driver)

The STM32 provides 3 differential signal pairs (PUL+/-, DIR+/-, ENA+/-) to the external driver's optocoupler inputs. The "-" signals are connected to GND. 100R series resistors on all "+" lines limit current for optocoupler compatibility (~20 mA at 3.3V).

```
PA10 (TIM1_CH3) ── R_PUL (100R) ──► J_CID Pin 1 (STEP_PUL+)
                                      J_CID Pin 2 (STEP_PUL-) ── GND

PB4  (GPIO)      ── R_DIR (100R) ──► J_CID Pin 3 (STEP_DIR+)
                                      J_CID Pin 4 (STEP_DIR-) ── GND

PCF8574 P7       ── R_ENA (100R) ──► J_CID Pin 5 (STEP_ENA+)
                                      J_CID Pin 6 (STEP_ENA-) ── GND

24V Input Rail ──────────────────────► J_CID Pin 12 (24V_STEP)
GND ─────────────────────────────────► J_CID Pin 13 (GND_PWR)
```

| Parameter | Value |
|-----------|-------|
| Motor | NEMA 23, 1.8°/step (200 steps/rev), ~2A/phase |
| External Driver | DM542/TB6600-class (pulse/dir/ena, 24V input) |
| Pulse Signal | PA10 (TIM1_CH3), 200 Hz–10 kHz step rate |
| Direction Signal | PB4 (GPIO), high = extend, low = retract |
| Enable Signal | PCF8574 P7 (I2C), active-low on most drivers |
| Series Resistors | 3× 100R (0402) on PUL+, DIR+, ENA+ |
| Power | 24V from input rail via J_CID pin 12 (2–3A to driver) |
| Position Feedback | Home limit switch only (PB6); step counting for travel distance |
| Travel | Step count calibrated to linear slide pitch (e.g., 8mm lead screw) |

> [!note]
> CID-1 full-extend limit switch removed — step counting provides travel distance. PB11 is freed and marked as reserved/unassigned. The ENA signal uses PCF8574 P7 (the only remaining free I/O on the expander); ENA is not timing-critical so I2C latency (~1 ms) is acceptable.

> [!warning]
> The 24V_STEP pin (J_CID pin 12) carries 2–3A to the external stepper driver. Verify Hirose DF11 pin current rating (3A per pin max) is sufficient. If sustained current exceeds 3A, use dual pins or a separate power connector.

#### 6.6.2 CID-2 Linear Actuator — DRV8876RGTR

One linear actuator for CID-2 push-plate slider, driven by a TI DRV8876RGTR H-bridge IC (#2).

```
12V Rail ──── VM (DRV8876 #2) ──── OUT1 ──┐
                                           │  Linear Actuator
              VREF ◄── 3.3V                │  (12V, 1.5A nominal)
                                           │
              GND ─── GND          OUT2 ───┘
                │
                ├── EN/PWM ◄── PB5 (100R gate)
                ├── PH/DIR ◄── PC2 (100R)
                ├── nSLEEP ◄── 3.3V (always awake via 10k pull-up)
                ├── nFAULT ──► (optional: route to STM32 reserved pin)
                ├── IPROPI ──► 1k sense resistor to GND
                │
           C_VM: 100nF + 10uF bypass on VM
           C_VCC: 100nF bypass on VCC
```

| Parameter | Value |
|-----------|-------|
| IC | DRV8876RGTR (WSON-8, 3x3mm) |
| Supply (VM) | 12V |
| Continuous Current | 3.5A per channel |
| Peak Current | 5A (transient) |
| Rds(on) (H+L) | 350 mR typical |
| Control Mode | PH/EN (Phase/Enable) |
| Current Sense | IPROPI: 1500 uA/A ratio, 1k sense resistor → 1.5V/A |
| Protection | Built-in: overcurrent, thermal shutdown, undervoltage lockout |

**Pin Allocation:**

| Actuator | EN/PWM Pin | PH/DIR Pin |
|----------|------------|------------|
| CID-2 Linear Actuator | PB5 | PC2 |

#### 6.6.3 CID Limit Switches

CID-1 has a single home limit switch (step counting replaces the full-extend switch). CID-2 retains both home and full-extend switches. NC wiring provides fail-safe behavior: a broken wire reads as "at limit" and stops motion.

```
3.3V ── R_CID_PU (10k) ──┬── STM32 GPIO (EXTI, falling edge)
                         │
                    C_CID (100nF) ── GND
                         │
                   Limit Switch (NC) ── GND
                   (opens at limit position)

Switch pressed (at limit): pin LOW  (switch closed to GND)
Switch released (in travel): pin HIGH (pulled up via 10k)
Debounce time constant: 10k × 100nF = 1ms (adequate for ~10mm/s actuator)
```

| Switch | Signal | Pin | Type | Pull-up |
|--------|--------|-----|------|---------|
| CID-1 Home | CID1_HOME | PB6 | GPIO Input (EXTI) | 10k to 3.3V + 100nF debounce |
| CID-2 Home | CID2_HOME | PD2 | GPIO Input (EXTI) | 10k to 3.3V + 100nF debounce |
| CID-2 Full-Extend | CID2_EXTEND | PCF8574 P6 | I2C Input | Internal pull-up (PCF8574) |

> [!note]
> CID-2 Full-Extend uses PCF8574 P6 (I2C expander, addr 0x20) because no more direct GPIO pins are available. Polling rate via the Sensor task (10 Hz) is sufficient for the slow linear actuator (~10mm/s travel speed).

### 6.7 SLD Peristaltic Pumps (2x) — TB6612FNG

Two peristaltic pumps for precise liquid dispensing (oil + water), driven by a single TB6612FNG dual H-bridge IC.

```
12V Rail ──── VM (TB6612FNG)
              │
         ┌────┤
         │    ├── PWMA ◄── PC3 (100R) ── Pump 1 Speed
         │    ├── AIN1 ◄── PC4 (100R) ── Pump 1 Direction
         │    ├── AIN2 ◄── (tied LOW on-board)
         │    ├── AO1 ───┐
         │    ├── AO2 ───┤── Pump 1 Motor
         │    │          │
         │    ├── PWMB ◄── PC5 (100R) ── Pump 2 Speed
         │    ├── BIN1 ◄── PC6 (100R) ── Pump 2 Direction
         │    ├── BIN2 ◄── (tied LOW on-board)
         │    ├── BO1 ───┐
         │    ├── BO2 ───┤── Pump 2 Motor
         │    │          │
         │    ├── STBY ◄── 3.3V (always active, 10k pull-up)
         │    └── GND ─── GND
         │
    C_VM: 100nF + 10uF
```

| Parameter | Value |
|-----------|-------|
| IC | TB6612FNG (SSOP-24) |
| Supply (VM) | 12V (max 15V) |
| Supply (VCC) | 3.3V (logic supply) |
| Continuous Current | 1.2A per channel |
| Peak Current | 3.2A per channel (pulsed) |
| Pull-downs | 10k on PWMA, PWMB (pumps off during boot) |

### 6.8 SLD Reservoir Load Cells (2x) — HX711

Two dedicated 2 kg load cells (one under each SLD reservoir) for independent liquid level monitoring and closed-loop dispensing accuracy. Each load cell connects to its own HX711 24-bit ADC breakout board, routed to the STM32 via J_SLD.

```
3.3V ──── VDD (HX711 #2, oil) ──── 100nF decoupling
              │
         ┌────┤
         │    ├── SCK ◄── PC11 (100R series)
         │    ├── DOUT ──► PC12 (100R series)
         │    └── GND ─── GND
         │
   2 kg Load Cell (under oil reservoir)

3.3V ──── VDD (HX711 #3, water) ──── 100nF decoupling
              │
         ┌────┤
         │    ├── SCK ◄── PC9 (100R series)
         │    ├── DOUT ──► PC10 (100R series)
         │    └── GND ─── GND
         │
   2 kg Load Cell (under water reservoir)
```

| Parameter | Value |
|-----------|-------|
| Load Cells | 2× 2 kg strain gauge (one per SLD reservoir) |
| ADC | 2× HX711 24-bit (external breakout boards, connected via J_SLD) |
| STM32 Pins | PC11/PC12 (oil), PC9/PC10 (water) |
| Sampling | 10 Hz |
| Resolution | ±1 g (with averaging) |
| Purpose | Individual reservoir level monitoring + closed-loop dispensing weight feedback |
| Low-Level Alert | Configurable threshold per channel (default: 50 g remaining) |
| Decoupling | 100nF MLCC on each HX711 VDD |

> **Note:** The pot load cell (PC0/PC1) uses a separate HX711 on pins 9-10 of J_SLD. The SLD reservoir HX711s share the same 3.3V/GND supply from J_SLD pins 11-12.

### 6.9 Piezo Buzzer (1x)

Active piezo buzzer (5V, PWM-capable) driven by a 2N7002 N-MOSFET.

```
5V Rail ──── Buzzer (+) ──── Buzzer (-) ──┬── Drain (2N7002)
                                          │
                                     10k Pull-down
                                          │
PC7 (TIM8_CH2) ── 100R ── Gate
                                          │
                                         GND ── Source
```

| Parameter | Value |
|-----------|-------|
| Buzzer | MLT-5030 or generic active piezo (5V) |
| MOSFET | 2N7002 (SOT-23) |
| PWM Frequency | Variable (2-4 kHz for tones, 10 Hz for beeps) |
| Current | ~20-30 mA typical |

### 6.10 USB-C Programming Port (Native USB 2.0 Full-Speed)

The STM32G474RE has a built-in USB 2.0 Full-Speed Device peripheral on PA11 (USB_DM) and PA12 (USB_DP). No external USB-UART bridge IC is needed. The USB-C port provides DFU bootloader programming (BOOT0 HIGH during reset) and USB CDC virtual serial for debug.

```
USB-C Receptacle (J_USB, mid-mount 16-pin, board edge)
  ├── VBUS ── F_USB (500mA polyfuse) ── 5V_USB rail
  │                                        │
  │                                   R_VBUS1 (100k) ── PA3 (VBUS detect ADC)
  │                                        │
  │                                   R_VBUS2 (100k) ── GND
  │
  ├── CC1 ── R_CC1 (5.1kR) ── GND    (UFP/device identification)
  ├── CC2 ── R_CC2 (5.1kR) ── GND
  │
  ├── D+  ──┬── USBLC6-2SC6 (U_ESD) ── 22R (R_DP) ── PA12 (USB_DP)
  └── D-  ──┘                        ── 22R (R_DM) ── PA11 (USB_DM)
```

**BOOT0 DFU Entry Button:**

```
3.3V ──── SW_BOOT (tactile, 6x6mm) ──┬── BOOT0
                                      │
                                 R_BOOT (10k) ── GND (existing pull-down)
```

Hold SW_BOOT during reset → BOOT0 = HIGH → STM32 enters DFU bootloader on PA11/PA12.

| Parameter | Value |
|-----------|-------|
| Connector | USB-C 2.0, 16-pin mid-mount SMD (LCSC C168688) |
| ESD Protection | USBLC6-2SC6 (SOT-23-6, LCSC C7519) |
| Series Resistors | 22R 1% (0402) on D+/D- |
| CC Pulldowns | 5.1kR 1% (0402) on CC1, CC2 |
| VBUS Polyfuse | 500mA resettable (0603, LCSC C70069) |
| VBUS Detect | 100k/100k voltage divider → PA3 (ADC, ~2.5V when 5V present) |
| DFU Button | 6x6mm tactile switch on BOOT0 |
| Differential Impedance | 90R (matched-length traces, see [[03-PCB-Design-Rules]]) |

> [!tip]
> The USB-C port enables standalone programming and debug without the 24V PSU or 12V UPS. Simply plug in a USB-C cable and the Schottky-OR feeds 5V_USB to the AMS1117 LDO, powering the STM32 at 3.3V.

### 6.11 Li-Ion Battery Charger + Boost Converter (Micro-UPS)

A single-cell Li-Ion battery provides micro-UPS capability for STM32 RTC and state retention. The charger is powered from 5V_USB (USB-C VBUS), and the boost converter outputs 5V_BATT to the Schottky-OR.

**Charger: TP4056 + DW01A + FS8205A**

```
5V_USB ──── U_CHG: TP4056 (SOP-8)
              │
              ├── PROG ── R_PROG (2kR) ── GND    (sets 500mA charge current)
              ├── CHRG ── R_CHG_LED (1kR) ── D_CHG (Red LED) ── GND
              ├── STDBY ── R_STB_LED (1kR) ── D_STB (Blue LED) ── GND
              │
              └── BAT+ ──┬── U_PROT: DW01A (SOT-23-6)
                          │      │
                          │      ├── OC (over-charge 4.3V)
                          │      ├── OD (over-discharge 2.5V)
                          │      └── CS (short-circuit)
                          │              │
                          │     Q_BAT: FS8205A (TSSOP-8) ── dual N-MOSFET switch
                          │              │
                          └── J_BAT (JST-PH 2-pin) ── Li-Ion Cell (3.7V nominal)
```

**Boost Converter: MT3608**

```
BAT+ (3.0-4.2V) ──── L_BST (4.7µH, 4x4mm) ──┬── D_BST (SS14 Schottky)
                                                │
                                         U_BOOST: MT3608 (SOT-23-6)
                                                │
                                           R_FB_TOP (732kR) ──┬── 5V_BATT output
                                                │              │
                                           R_FB_BOT (100kR) ── GND
                                                │
                                           C_BST_OUT: 22uF (16V)
                                                │
                                           5V_BATT ── D_OR3 (SS14) ── 5V_MERGED
```

| Parameter | Value |
|-----------|-------|
| Charger IC | TP4056 (SOP-8, LCSC C16581) |
| Charge Current | 500mA (R_PROG = 2kR) |
| Protection IC | DW01A (SOT-23-6, LCSC C14213) — OVP 4.3V, UVP 2.5V, SCP |
| Protection FET | FS8205A (TSSOP-8, LCSC C32254) — dual N-MOSFET |
| Boost IC | MT3608 (SOT-23-6, LCSC C84817) — up to 2A output |
| Boost Inductor | 4.7µH, 4x4mm shielded (LCSC C408412) |
| Boost Output | 5.0V (732kR/100kR feedback divider) |
| Boost Schottky | SS14 (1A, 40V Schottky, SMA, LCSC C2480) |
| Battery Connector | JST-PH 2-pin, 2.0mm pitch (LCSC C131337) |
| LEDs | Red (charging), Blue (complete), 0603 |
| Charge Source | 5V_USB from USB-C VBUS only |

> [!warning]
> The Li-Ion battery is intended as a micro-UPS for STM32 state retention only (~50mA load). It is NOT sized to power the CM5 or actuators. At ~50mA, a 500mAh cell provides ~10 hours of STM32 standby.

### 6.12 P-ASD Diaphragm Pump (1x)

A 12V micro diaphragm pump (3-4 L/min) pressurizes the P-ASD accumulator. Driven by an IRLML6344 N-MOSFET with PWM speed control.

```
12V Rail ──── Pump Motor (+) ──── Pump Motor (-) ──┬── Drain (IRLML6344)
                                                    │
                                               SS14 Flyback ─── 12V
                                                    │
                                               10k Pull-down
                                                    │
PA0 (TIM2_CH1) ── 100R ── Gate
                                                    │
                                                   GND ── Source
```

| Parameter | Value |
|-----------|-------|
| Pump | 12V micro diaphragm, 3-4 L/min, <45 dB |
| MOSFET | IRLML6344 (SOT-23) |
| PWM Frequency | 25 kHz (above audible range) |
| Pump Current | 0.5-0.8A typical |

---

## 7. CAN Bus Transceiver — ISO1050DUB

An ISO1050DUB isolated CAN transceiver provides 5 kV RMS galvanic isolation between the STM32 logic side and the CAN bus connected to the microwave induction surface. With the unified board, the transceiver connects directly to the STM32 FDCAN1 pins — no inter-board routing needed.

### 7.1 Circuit

```
PB9 (FDCAN1_TX) ──► TXD ┐
                          │
               ┌──────────▼──────────┐
               │     ISO1050DUB      │
               │                     │
  VCC1 = 3.3V ─┤ VCC1           VCC2 ├──── 5V
               │                     │
  GND1 = GND  ─┤ GND1           GND2 ├──── GND_ISO (isolated)
               │                     │
               │  ─── 5 kV barrier ─ │
               │                     │
               └──────────┬──────────┘
                          │
  PB8 (FDCAN1_RX) ◄── RXD ┘
                          │
                   CANH ──┤── R_TERM (120R) ──┤── CANL
                          │                   │
                    J_CAN Pin 1            J_CAN Pin 2
```

### 7.2 Isolation Slot

A **6mm milled slot** in the PCB under the ISO1050 provides physical separation between system ground and isolated bus ground. No copper pour or traces cross this boundary. The slot is placed near the bottom edge of the board to avoid interfering with digital routing in Zone A.

### 7.3 Decoupling

| Ref | Part | Value | Notes |
|-----|------|-------|-------|
| C_CAN1 | 100nF MLCC | 0402 | VCC1 decoupling (3.3V logic side) |
| C_CAN2a | 100nF MLCC | 0402 | VCC2 high-freq decoupling (5V bus side) |
| C_CAN2b | 10uF MLCC | 0805 | VCC2 bulk decoupling (5V bus side) |
| R_TERM | 120R | 0402 | CAN bus termination |

> [!note]
> The ISO1050DUB provides 5 kV RMS galvanic isolation (reinforced per UL 1577). This protects the STM32 from ground bounce and EMI transients generated by the 1,800W induction module's IGBT switching, and satisfies IEC 60335 requirements for galvanic isolation.

---

## 8. Current Monitoring — INA219

An INA219 bidirectional current/power monitor on the 24V input rail provides real-time power consumption telemetry via I2C. On the unified board, it connects directly to I2C1 with no inter-board routing.

```
24V Input ──── R_shunt (10 mR, 2512, 1%) ──── 24V Internal
                    │                │
                    IN+             IN-
                    │                │
              ┌─────▼────────────────▼─────┐
              │         INA219             │
              │  VS+    VS-    SDA    SCL  │
              └───┼──────┼──────┼──────┼───┘
                  │      │      │      │
                 3.3V   GND    PB7    PA15
                               (I2C1)
```

| Parameter | Value |
|-----------|-------|
| IC | INA219BIDR (SOT-23-8) |
| I2C Address | 0x40 (A0=GND, A1=GND) |
| Shunt Resistor | 10 mR, 2512 package, 1%, 1W rated |
| Bus Voltage Range | 0-26V (covers 24V rail) |
| Current Resolution | ~0.1 mA per LSB (at 10 mR shunt, PGA /1) |
| Decoupling | 100nF on VS+ |

---

## 9. Protection Circuits

### 9.1 ESD Protection

- TVS diode array (PRTR5V0U2X) on J_CM5 SPI lines
- TVS diodes on J_SAFE safety inputs (E-stop, pot detection)
- All external connectors have series 33R resistors on signal lines

### 9.2 Relay Driver (Q_RLY)

```
PB0 ────┤ 330R ├──── Gate ─┐
                           │
                     ┌─────▼──────┐
                     │ Q_RLY:     │
                     │ 2N7002     │
                     └─────┬──────┘
                           │ Drain
                     ┌─────▼──────┐
                     │ Relay Coil │ ◄── 5V or 12V
                     │ (Omron G5V)│
                     └─────┬──────┘
                           │
                      D (1N4148) ◄── Flyback diode
                           │
                          GND
```

### 9.3 E-Stop Input

```
E-Stop Button (NC)
    │
    ├──── R: 10k pull-up to 3.3V
    ├──── C: 100nF to GND (RC debounce, tau ~1ms)
    └──── PB2 (EXTI, falling edge interrupt)

Button pressed → PB2 goes LOW → immediate interrupt
Button released (or wire break) → PB2 stays LOW → fail-safe
```

### 9.4 Pot Detection Input

```
Reed Switch (NO)
    │
    ├──── R: 10k pull-up to 3.3V
    └──── PB1 (GPIO input)

Pot present → magnet closes reed → PB1 = LOW
Pot absent → reed open → PB1 = HIGH (pulled up)
```

### 9.5 LED Ring Power Switch (Q_LED_N + Q_LED_P)

A high-side P-MOSFET switch controls 5V power to the WS2812B LED ring. An N-MOSFET level-shifts the 3.3V GPIO to drive the P-MOSFET gate.

```
5V ──── Q_LED_P: SI2301 (P-MOSFET, SOT-23) ──── J_LED Pin 1 (5V_SW)
          │ Source              Drain │
          Gate ──┬── R: 10k to 5V (default OFF)
                 └── Q_LED_N: 2N7002 Drain
                          │
                     Q_LED_N Source ── GND
                          │
                     Q_LED_N Gate ── 100R ── PCF8574 #2 P3 (I2C1, 0x21)
                          │
                     10k pull-down to GND

CM5 GPIO18 ── J_CM5 Pin 12 ── J_LED Pin 2 (DATA, PCB trace passthrough)
GND ──────── J_LED Pin 3 (GND)
```

| Parameter | Value |
|-----------|-------|
| Q_LED_N | 2N7002 (N-MOSFET, SOT-23) — level shifter |
| Q_LED_P | SI2301CDS (P-MOSFET, SOT-23) — high-side switch |
| Id(max) Q_LED_P | -2.3A (sufficient for 1A LED ring peak) |
| Control | PCF8574 #2 P3 (I2C1, 0x21) — moved from PA2 to free STM32 pin |
| Default State | OFF (Q_LED_N gate pulled low → Q_LED_P gate to 5V → P-MOSFET off) |

### 9.6 MOSFET Gate Safety

All MOSFET and H-bridge IC enable pins have:
- **100R series gate resistor** — limits gate charge current, reduces ringing and EMI
- **10k pull-down to GND** — ensures actuators are OFF during STM32 boot, reset, or brown-out

---

## 10. Connector Definitions (17 total)

### 10.1 J_CM5 — CM5IO GPIO Header Receptor (2x20 pin socket, 2.54mm)

Mates directly with the CM5IO board's 40-pin GPIO header. Only the pins listed below are actively routed; all others pass through unconnected.

| GPIO Pin | Signal | STM32 Pin / Destination | Direction | Purpose |
|----------|--------|------------------------|-----------|---------|
| 2, 4 | 5V | 5V rail (UPS-backed) | Out to CM5IO | Powers CM5IO + CM5 module |
| 6, 9, 14, 20, 25, 30, 34, 39 | GND | GND | Power | Common ground |
| 7 | GPIO4 | PB3 (GPIO) | Out to CM5 | Data-ready IRQ (active-low, 10us pulse) |
| 12 | GPIO18 | J_LED pin 2 (passthrough) | Out from CM5 | WS2812B LED ring data |
| 19 | GPIO10 (MOSI) | PB15 (SPI2_MOSI) | In from CM5 | SPI data to STM32 |
| 21 | GPIO9 (MISO) | PB14 (SPI2_MISO) | Out to CM5 | SPI data from STM32 |
| 23 | GPIO11 (SCLK) | PB13 (SPI2_SCK) | In from CM5 | SPI clock |
| 24 | GPIO8 (CE0) | PB12 (SPI2_NSS) | In from CM5 | SPI chip select (active-low) |

> [!note]
> The 5V pins (2, 4) are driven from the UPS-backed 5V rail. The CM5IO's USB-C port can still be used for debug console access but is not the primary power source.

### 10.2 J_24V_IN — 24V DC Power Input (XT30 or JST-VH 2-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | +24V | From Mean Well LRS-75-24 |
| 2 | GND | Power ground |

### 10.3 J_12V_UPS — 12V UPS-Backed DC Input (XT30 2-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | +12V | From external 12V UPS battery backup |
| 2 | GND | Power ground |

### 10.4 J_BLDC — 24V BLDC Stirring Motor (Hirose DF11-6DP-2DS, 2x3, 2.0mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 24V | Direct from 24V rail |
| 2 | GND | Power ground |
| 3 | PWM | 10 kHz speed control (PA8, 100R series) |
| 4 | EN | Enable (PA4, 100R series) |
| 5 | DIR | Direction CW/CCW (PA5, 100R series) |
| 6 | FG | Tachometer feedback (NC for prototype) |

### 10.5 J_PASD — Combined P-ASD Connector (Hirose DF11-16DP-2DS, 2x8, 2.0mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 12V_SOL1 | Solenoid V1 power (IRLML6344, gate via PCF8574 P0) |
| 2 | SOL1_OUT | Solenoid V1 drain (Turmeric) |
| 3 | 12V_SOL2 | Solenoid V2 power (IRLML6344, gate via PCF8574 P1) |
| 4 | SOL2_OUT | Solenoid V2 drain (Chili) |
| 5 | 12V_SOL3 | Solenoid V3 power (IRLML6344, gate via PCF8574 P2) |
| 6 | SOL3_OUT | Solenoid V3 drain (Cumin) |
| 7 | 12V_SOL4 | Solenoid V4 power (IRLML6344, gate via PCF8574 P3) |
| 8 | SOL4_OUT | Solenoid V4 drain (Salt) |
| 9 | 12V_SOL5 | Solenoid V5 power (IRLML6344, gate via PCF8574 P4) |
| 10 | SOL5_OUT | Solenoid V5 drain (Garam Masala) |
| 11 | 12V_SOL6 | Solenoid V6 power (IRLML6344, gate via PCF8574 P5) |
| 12 | SOL6_OUT | Solenoid V6 drain (Coriander) |
| 13 | 12V_PUMP | Pump power (IRLML6344, PA0 PWM) |
| 14 | PUMP_OUT | Pump drain |
| 15 | GND | Common ground |
| 16 | GND | Common ground |

### 10.6 J_PRES — P-ASD Pressure Sensor (Hirose DF11-4DP-2DS, 2x2, 2.0mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | I2C1_SCL | ADS1015 clock (PA15, 4.7k pull-up on PCB) |
| 2 | I2C1_SDA | ADS1015 data (PB7, 4.7k pull-up on PCB) |
| 3 | 3.3V | ADS1015 + MPXV5100GP supply |
| 4 | GND | Sensor return |

> [!note]
> Connects to ADS1015 + MPXV5100GP breakout near P-ASD accumulator. I2C pull-ups (4.7k) on main PCB only — no pull-ups on remote breakout. Max cable length 500 mm. Place adjacent to J_PASD on the board edge.

### 10.7 J_SLD — Combined SLD + Load Cells (Hirose DF11-16DP-2DS, 2x8, 2.0mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | PUMP1_AO1 | TB6612 output A1 (oil pump +) |
| 2 | PUMP1_AO2 | TB6612 output A2 (oil pump -) |
| 3 | PUMP2_BO1 | TB6612 output B1 (water pump +) |
| 4 | PUMP2_BO2 | TB6612 output B2 (water pump -) |
| 5 | 12V_SOL1 | Oil solenoid power (switched) |
| 6 | SOL1_OUT | Oil solenoid drain (PCF8574 #2 P0) |
| 7 | 12V_SOL2 | Water solenoid power (switched) |
| 8 | SOL2_OUT | Water solenoid drain (PCF8574 #2 P1) |
| 9 | HX711_POT_SCK | Clock output to pot HX711 (PC0) |
| 10 | HX711_POT_DOUT | Data input from pot HX711 (PC1) |
| 11 | 3.3V | HX711 supply (shared by all 3 HX711s) |
| 12 | GND | HX711 ground |
| 13 | HX711_OIL_SCK | Clock output to SLD oil reservoir HX711 (PC11) |
| 14 | HX711_OIL_DOUT | Data input from SLD oil reservoir HX711 (PC12) |
| 15 | HX711_WATER_SCK | Clock output to SLD water reservoir HX711 (PC9) |
| 16 | HX711_WATER_DOUT | Data input from SLD water reservoir HX711 (PC10) |

### 10.8 J_CID — Combined CID Stepper + Linear Actuator + Limit Switches (Hirose DF11-14DP-2DS, 2x7, 2.0mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | STEP_PUL+ | PA10 (TIM1_CH3) via 100R — stepper pulse signal |
| 2 | STEP_PUL- | GND — pulse return |
| 3 | STEP_DIR+ | PB4 (GPIO) via 100R — stepper direction signal |
| 4 | STEP_DIR- | GND — direction return |
| 5 | STEP_ENA+ | PCF8574 P7 via 100R — stepper enable signal |
| 6 | STEP_ENA- | GND — enable return |
| 7 | LACT2_OUT1 | DRV8876 #2 output 1 (CID-2 linear actuator) |
| 8 | LACT2_OUT2 | DRV8876 #2 output 2 (CID-2 linear actuator) |
| 9 | CID1_HOME | Limit switch → PB6 (10k pull-up, 100nF debounce) |
| 10 | CID2_HOME | Limit switch → PD2 (10k pull-up, 100nF debounce) |
| 11 | CID2_EXTEND | Limit switch → PCF8574 P6 (internal pull-up) |
| 12 | 24V_STEP | 24V power to external stepper driver (from 24V input rail) |
| 13 | GND_PWR | Power ground return for stepper driver |
| 14 | GND_SW | Limit switch common ground |

> [!note]
> CID-1 full-extend limit switch removed (step counting used for travel distance); PB11 freed → reserved. The 24V_STEP pin (12) carries 2–3A to the external driver; verify Hirose DF11 pin current rating (3A per pin max).

### 10.9 J_FAN — Combined Exhaust Fans (1x 4-pin JST-XH 2.5mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 12V_FAN1 | Fan 1 power (IRLML6344, PA6 PWM) |
| 2 | FAN1_OUT | Fan 1 drain |
| 3 | 12V_FAN2 | Fan 2 power (IRLML6344, PB10 PWM) |
| 4 | FAN2_OUT | Fan 2 drain |

### 10.10 J_CAN — CAN Bus to Microwave Surface (JST-XH 2.5mm, 4-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | CAN_H | CAN bus high |
| 2 | CAN_L | CAN bus low |
| 3 | GND_ISO | Isolated bus ground (NOT system GND) |
| 4 | NC | Reserved |

### 10.11 J_BUZZER — Piezo Buzzer (2-pin JST-PH 2.0mm)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 5V | Buzzer power (switched by 2N7002) |
| 2 | BUZZ_OUT | Drain side of 2N7002 (PA11 PWM) |

### 10.12 J_IR — MLX90614 I2C (JST-SH 1.0mm, 4-pin)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | SCL | PA15 (I2C1_SCL) | 4.7k pull-up on board |
| 2 | SDA | PB7 (I2C1_SDA) | 4.7k pull-up on board |
| 3 | VCC | 3.3V | — |
| 4 | GND | GND | — |

### 10.13 J_SWD — SWD Debug (10-pin 1.27mm Cortex Debug or 6-pin TagConnect)

| Pin | Signal | STM32 Pin |
|-----|--------|-----------|
| 1 | VCC | 3.3V |
| 2 | SWDIO | PA13 |
| 3 | SWCLK | PA14 |
| 4 | SWO | PB3 (shared with IRQ — select via solder jumper SJ1) |
| 5 | NRST | NRST |
| 6 | GND | GND |

> [!note]
> PB3 is shared between SPI IRQ and SWD SWO. Solder jumper SJ1 selects between the two. Default: IRQ.

### 10.14 J_SAFE — Safety I/O (Hirose DF11-4DP-2DS, 2x2, 2.0mm)

| Pin | Signal | STM32 Pin | Notes |
|-----|--------|-----------|-------|
| 1 | RELAY_DRV | PB0 via Q_RLY | Drives safety relay coil |
| 2 | POT_DET | PB1 | Reed switch input, 10k pull-up |
| 3 | E_STOP | PB2 | NC button, 10k pull-up, RC debounce |
| 4 | GND | GND | — |

### 10.15 J_LED — LED Ring (JST-XH 2.5mm, 3-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 5V_SW | Switched 5V from Q_LED_P (PCF8574 #2 P3 enable) |
| 2 | DATA | WS2812B data (passthrough from CM5 GPIO18) |
| 3 | GND | Power ground |

### 10.16 J_USB — USB-C Programming Port (USB-C 2.0, 16-pin mid-mount)

| Pin | Signal | Notes |
|-----|--------|-------|
| A1/B1 | GND | Ground |
| A4/B4 | VBUS | 5V USB power → F_USB (500mA polyfuse) → 5V_USB |
| A5 | CC1 | 5.1kR to GND (UFP identification) |
| B5 | CC2 | 5.1kR to GND (UFP identification) |
| A6/B6 | D+ | USB data positive → USBLC6 ESD → 22R → PA12 |
| A7/B7 | D- | USB data negative → USBLC6 ESD → 22R → PA11 |

> [!note]
> Only USB 2.0 signals are used. SuperSpeed (A2/A3/B2/B3) and SBU pins are not connected. The connector is mid-mount SMD, placed on the board edge in Zone B near J_SWD.

### 10.17 J_BAT — Li-Ion Battery (JST-PH 2.0mm, 2-pin)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | BAT+ | Li-Ion positive (3.0-4.2V) via DW01A/FS8205A protection |
| 2 | GND | Battery ground |

> [!note]
> Use a single-cell Li-Ion or LiPo battery, 500-1000mAh. The TP4056 charges at 500mA from USB-C VBUS. J_BAT is placed on the right board edge near J_12V_UPS.

---

## 11. 4-Layer Stackup and Zone Layout

### 11.1 Layer Stack

```
┌──────────────────────────────────────────────┐
│  Layer 1 (Top)    — Signal + Components      │  70um Cu (2 oz)
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 2 (Inner1) — GND Plane (continuous)   │  35um Cu (1 oz)
├──────────────────────────────────────────────┤
│  Core             — FR4, 0.8mm               │
├──────────────────────────────────────────────┤
│  Layer 3 (Inner2) — Split Power Plane        │  35um Cu (1 oz)
│                     (5V/3.3V | 12V | 24V)    │
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 4 (Bottom) — Signal + Power Traces    │  70um Cu (2 oz)
└──────────────────────────────────────────────┘

Total thickness: ~1.6mm (standard)
Material: FR4 (Tg >= 150C)
Outer copper: 2 oz (70um) for high-current power traces
Inner copper: 1 oz (35um) for planes
```

### 11.2 Board Layout Zones

```
┌─────────────────────── 160mm ───────────────────────┐
│  J_CM5 (2x20 socket, bottom side, top edge center)  │
│  ┌─────────────┐  ┌───────────┐  ┌───────────────┐  │
│  │ ZONE A:     │  │ ZONE B:   │  │ ZONE C:       │  │
│  │ DIGITAL     │  │ COMMS     │  │ POWER INPUT   │  │
│  │ STM32G474RE │  │ J_SWD     │  │ J_24V_IN XT30 │  │
│  │ Crystals    │  │ J_IR      │  │ J_12V_UPS XT30│  │
│  │ AMS1117 LDO │  │ J_SAFE    │  │ Polyfuses,TVS │  │ 90mm
│  │ ESD, relay  │  │ J_LED     │  │ INA219+shunt  │  │
│  │ Schottky-OR │  │ J_USB ◄───│  │ J_BAT ◄────── │  │
│  │ (D_OR1-3)   │  │ SW_BOOT   │  │ TP4056+DW01A  │  │
│  ├─────────────┤  │ USBLC6    │  │ MT3608 boost  │  │
│  │ ZONE D:     │  ├───────────┤  ├───────────────┤  │
│  │ ACTUATOR ICs│  │ ZONE E:   │  │ ZONE F:       │  │
│  │ 1x DRV8876  │  │ MOSFET    │  │ BUCK          │  │
│  │ TB6612FNG   │  │ ARRAY     │  │ CONVERTERS    │  │
│  │ PCF8574 x2  │  │ 11xMOSFET │  │ 2x MP1584EN   │  │
│  └─────────────┘  │ +flybacks │  │ TPS54531      │  │
│  ┌── CAN ISOLATION (6mm slot)─┐  │ +3 inductors  │  │
│  │ ISO1050 │ SLOT │ J_CAN     │  └───────────────┘  │
│  └────────────────────────────┘                     │
│J_BLDC  J_PASD  J_PRES  J_SLD  J_CID  J_FAN  J_BUZZER│
└─────────────────────────────────────────────────────┘
```

**Zone placement rationale:**
- **Zone A** (digital) directly above J_CM5 on the top side → shortest SPI traces (~20mm) via through-board vias
- **Zone F** (buck converters) 25mm+ from STM32 → thermal/EMI separation
- **CAN isolation slot** near bottom edge → doesn't interfere with digital routing
- **Output connectors** on bottom/side edges → cables route away from CM5IO

### 11.3 Noise and Thermal Isolation Strategy

- **GND plane (L2):** Continuous, unbroken under STM32 and SPI traces. Only break is the 6mm CAN isolation slot.
- **Power plane (L3):** Split into 5V/3.3V, 12V, and 24V zones matching physical layout.
- **Buck converter isolation:** 25mm+ from STM32; switching loops minimized on outer layers (2oz Cu).
- **Ferrite bead** on STM32 VDDA separates analog from digital 3.3V.
- **Thermal vias:** 9+ under STM32, 6+ under DRV8876 #2, 400mm2 copper pour around each buck converter.
- **0-ohm jumper links** between power zones for sectional debug isolation.
- **Test points** on each power rail + SPI + CAN for prototype bring-up.

### 11.4 Critical Layout Rules

| Rule | Specification | Rationale |
|------|---------------|-----------|
| STM32 decoupling | 100nF caps within 5mm of VDD pins | Reduce supply noise |
| VDDA isolation | Ferrite bead + 1uF from 3.3V | Clean analog reference |
| Crystal traces | Short, symmetric, guard ring GND | Minimize EMI coupling |
| USB D+/D- traces | Matched length (±0.5mm), 90R differential impedance | USB 2.0 FS signal integrity |
| USB to STM32 | Short traces (<30mm), no vias if possible | Minimize impedance discontinuity |
| SPI traces | Matched length (+-2mm), 50 ohm impedance | Signal integrity at 2 MHz |
| Power input traces | >=2mm wide (2oz Cu), as short as possible | Carry up to 3.2A from PSU |
| Buck converter loops | Minimize input cap → IC → inductor → output cap loop area | Reduce EMI radiation |
| Inductor placement | Within 5mm of MP1584EN IC, away from signal traces | Magnetic field coupling |
| GND plane | Continuous under STM32, SPI, and all switching converters | Low-impedance return path |
| I2C traces | Keep <30mm on board, pull-ups near STM32 | Minimize capacitance |
| MOSFET drain traces | >=1mm wide, short runs to output connectors | Current capacity |
| Safety relay creepage | >=2mm between 5V/12V and 3.3V logic | IEC 60335 clearance |
| CAN isolation | Creepage >=6.4mm between GND1 and GND2; 6mm milled slot | IEC 60335 reinforced |
| Thermal vias under STM32 | Minimum 9 vias, 0.3mm drill | Thermal dissipation |
| Thermal vias under DRV8876 #2 | Minimum 6 vias, 0.3mm drill | Heat to inner GND plane |
| Thermal copper pour | >=400mm2 around each buck converter IC + inductor | Heat spreading |

---

## 12. Thermal Analysis

### 12.1 Component Power Dissipation

| Component | Condition | Power (W) | Thermal Path |
|-----------|-----------|-----------|--------------|
| MP1584EN #1 (12V) | 2A continuous | ~2.7 | IC + inductor, PCB copper pour |
| MP1584EN #2 (6.5V) | 1A average | ~1.0 | IC + inductor, PCB copper pour |
| TPS54531 (5V) | 2A average | ~0.5 | SOIC-8 + inductor, PCB copper pour |
| DRV8876 #2 (CID-2) | 1.5A continuous | ~0.8 | WSON-8 exposed pad → GND plane vias |
| TB6612FNG | 1.2A total | ~0.7 | SSOP-24 thermal pad → PCB |
| IRLML6344 (x11) | 0.5-1A each | ~0.03 each | SOT-23, negligible |
| 2N7002 (x2) | <0.1A total | ~0.005 | SOT-23, negligible |
| AMS1117-3.3 LDO | 0.17A | ~0.29 | SOT-223, PCB copper |
| INA219 | Monitoring only | ~0.01 | Negligible |
| SS54 input diode | 3A peak | ~1.5 | SMA package, PCB copper pour |
| Shunt resistor | 3A peak | ~0.09 | 2512 package |
| **Total** | | **~9W typical** | |

### 12.2 Temperature Estimates

At 40C ambient (inside Epicura enclosure near induction surface):

| Component | theta_JA (C/W) | Dissipation (W) | Est. Junction Temp (C) |
|-----------|---------------|-----------------|-------------------------|
| MP1584EN #1 | ~50 | 2.7 | 40 + 135 = 175 — **Needs attention** |
| DRV8876 | ~45 (with pad vias) | 0.8 | 40 + 36 = 76C |
| TB6612FNG | ~80 | 0.7 | 40 + 56 = 96C |
| AMS1117-3.3 | ~90 | 0.29 | 40 + 26 = 66C |
| SS54 | ~65 | 1.5 | 40 + 98 = 138C (Tj max 150C) |

> [!warning]
> The 12V buck converter (MP1584EN #1) at sustained 2A+ load may exceed thermal limits. Mitigations:
> 1. Use large copper pour (>=400mm2) around the IC and inductor
> 2. Add thermal vias (6+ vias, 0.3mm) under the exposed pad to inner GND plane
> 3. Derate: limit sustained 12V load to 2A (duty-cycle solenoids, don't run all simultaneously)
> 4. Consider upgrading to MP2315 (higher efficiency at 12V output) if thermal budget is tight

---

## 13. Unified BOM

| Ref | Part | Package | Qty | Unit Cost (USD) | Notes |
|-----|------|---------|-----|----------------|-------|
| **Microcontroller** | | | | | |
| U_MCU | STM32G474RET6 | LQFP-64 | 1 | $8.00 | Cortex-M4F, 170 MHz |
| Y1 | 8 MHz crystal | HC49/SMD | 1 | $0.20 | HSE, 20ppm, 18pF load |
| Y2 | 32.768 kHz crystal | 2x1.2mm SMD | 1 | $0.30 | LSE for RTC |
| **Power Conversion** | | | | | |
| U_BUCK1-2 | MP1584EN | SOT-23-8 | 2 | $0.80 | 24V→12V, 24V→6.5V |
| U_BUCK3 | TPS54531DDAR | SOIC-8 | 1 | $1.50 | 12V UPS→5V, 5A |
| U_LDO | AMS1117-3.3 | SOT-223 | 1 | $0.30 | 5V→3.3V LDO, 800mA |
| L1 | 33uH inductor | CDRH104R (10x10mm) | 1 | $0.50 | 12V rail, Isat > 4A |
| L2 | 22uH inductor | CDRH104R (10x10mm) | 1 | $0.50 | 6.5V rail |
| L3 | 10uH inductor | CDRH127 (12.7x12.7mm) | 1 | $0.60 | 5V rail, Isat > 6A |
| D_BST1-2 | SS34 | SMA | 2 | $0.15 | Bootstrap Schottky (MP1584EN) |
| **H-Bridge ICs** | | | | | |
| U_DRV2 | DRV8876RGTR | WSON-8 (3x3mm) | 1 | $2.50 | CID-2 linear actuator driver |
| U_TB | TB6612FNG | SSOP-24 | 1 | $1.50 | SLD dual peristaltic pump driver |
| **Discrete MOSFETs** | | | | | |
| Q1-Q11 | IRLML6344 | SOT-23 | 11 | $0.20 | SLD sol x2, fan x2, P-ASD sol V1-V6, P-ASD pump |
| Q_BUZZ | 2N7002 | SOT-23 | 1 | $0.05 | Buzzer MOSFET |
| Q_RLY | 2N7002 | SOT-23 | 1 | $0.05 | Relay driver MOSFET |
| Q_LED_N | 2N7002 | SOT-23 | 1 | $0.05 | LED ring N-MOSFET (level shifter) |
| Q_LED_P | SI2301CDS | SOT-23 | 1 | $0.10 | LED ring P-MOSFET (high-side switch) |
| **I2C Peripherals** | | | | | |
| U_EXP | PCF8574 | SOIC-16 | 1 | $0.50 | P-ASD solenoid V1-V6 + CID (I2C 0x20) |
| U_EXP2 | PCF8574 | SOIC-16 | 1 | $0.50 | SLD solenoids + status LED + LED ring power (I2C 0x21) |
| C_EXP2 | 100nF MLCC | 0402 | 1 | $0.01 | U_EXP2 VDD decoupling |
| U_MON | INA219BIDR | SOT-23-8 | 1 | $1.50 | 24V input current/power monitor |
| R_SHUNT | 10 mR 1% 1W | 2512 | 1 | $0.30 | Current sense shunt |
| **CAN Transceiver** | | | | | |
| U_CAN | ISO1050DUB | SOIC-8 | 1 | $3.50 | Isolated CAN, 5kV RMS |
| C_CAN1 | 100nF MLCC | 0402 | 1 | $0.01 | VCC1 decoupling |
| C_CAN2a | 100nF MLCC | 0402 | 1 | $0.01 | VCC2 high-freq |
| C_CAN2b | 10uF MLCC | 0805 | 1 | $0.11 | VCC2 bulk |
| R_TERM | 120R | 0402 | 1 | $0.01 | CAN bus termination |
| **Protection** | | | | | |
| F1 | 5A polyfuse | 1812 | 1 | $0.40 | 24V input overcurrent |
| F2-F3 | 1.5A/3A polyfuse | 0805/1206 | 2 | $0.25 | 12V and 6.5V per-rail |
| F5 | 3A polyfuse | 1812 | 1 | $0.30 | 12V UPS input overcurrent |
| D_REV | SS54 | SMA | 1 | $0.20 | 24V input reverse polarity |
| D_TVS1 | SMBJ24A | SMB | 1 | $0.25 | 24V input TVS |
| D_TVS2 | SMBJ12A | SMB | 1 | $0.20 | 12V rail TVS |
| D_TVS3 | SMBJ6.5A | SMB | 1 | $0.20 | 6.5V rail TVS |
| D_UPS1 | SS34 | SMA | 1 | $0.15 | 12V UPS reverse polarity |
| D_UPS2 | SMBJ12A | SMB | 1 | $0.20 | 12V UPS input TVS |
| D_ESD1-2 | PRTR5V0U2X | SOT-143B | 2 | $0.15 | ESD on SPI + safety I/O |
| D_FLY | 1N4148WS | SOD-323 | 1 | $0.03 | Relay flyback diode |
| **USB-C Programming Port** | | | | | |
| J_USB | USB-C 2.0 receptacle, 16-pin mid-mount | USB-C SMD | 1 | $0.30 | DFU programming, CDC serial |
| U_ESD | USBLC6-2SC6 | SOT-23-6 | 1 | $0.15 | USB D+/D- ESD protection |
| R_DP, R_DM | 22R 1% | 0402 | 2 | $0.01 | USB series termination |
| R_CC1, R_CC2 | 5.1kR 1% | 0402 | 2 | $0.01 | CC pulldowns (UFP ID) |
| R_VBUS1, R_VBUS2 | 100k | 0402 | 2 | $0.01 | VBUS detect divider → PA3 |
| F_USB | 500mA polyfuse | 0603 | 1 | $0.10 | USB VBUS overcurrent |
| SW_BOOT | Tactile switch | 6x6mm | 1 | $0.05 | BOOT0 DFU entry |
| D_OR1-3 | SS14 (1A, 40V Schottky) | SMA | 3 | $0.10 | 5V Schottky-OR (3-way) |
| C_OR | 10uF MLCC | 0805 (10V) | 1 | $0.10 | Merged 5V rail stabilization |
| **Li-Ion Battery Charger + Boost** | | | | | |
| U_CHG | TP4056 | SOP-8 | 1 | $0.10 | CC/CV Li-Ion charger (500mA) |
| U_PROT | DW01A | SOT-23-6 | 1 | $0.05 | Over-charge/discharge/short protection |
| Q_BAT | FS8205A | TSSOP-8 | 1 | $0.08 | Dual N-MOSFET protection switch |
| U_BOOST | MT3608 | SOT-23-6 | 1 | $0.15 | 3.7V→5V boost converter |
| L_BST | 4.7µH inductor | 4x4mm shielded | 1 | $0.15 | Boost inductor |
| D_BST | SS14 Schottky | SMA | 1 | $0.10 | Boost diode |
| J_BAT | JST-PH 2-pin | 2.0mm pitch | 1 | $0.08 | Li-Ion battery connector |
| R_PROG | 2kR | 0402 | 1 | $0.01 | TP4056 charge current set |
| R_FB_BST (x2) | 732kR, 100kR | 0402 | 2 | $0.01 | MT3608 feedback divider |
| C_BST_IN | 10uF MLCC | 0805 (10V) | 1 | $0.10 | Boost input cap |
| C_BST_OUT | 22uF MLCC | 0805 (16V) | 1 | $0.12 | Boost output cap |
| D_CHG, D_STB | Red/Blue LED | 0603 | 2 | $0.03 | Charge status indicators |
| R_CHG_LED, R_STB_LED | 1kR | 0402 | 2 | $0.01 | LED current limit |
| **Flyback Diodes** | | | | | |
| D_FB1-11 | SS14 | SMA | 11 | $0.10 | Solenoid/fan/pump flybacks |
| **Power Fail Detection** | | | | | |
| R_DIV1 | 100k | 0402 | 1 | $0.01 | Voltage divider top |
| R_DIV2 | 10k | 0402 | 1 | $0.01 | Voltage divider bottom |
| C_DIV | 100nF | 0402 | 1 | $0.01 | Divider filter cap |
| **Passive Components** | | | | | |
| FB1 | Ferrite bead 600R | 0603 | 1 | $0.05 | VDDA isolation |
| D_LED | Green LED | 0603 | 1 | $0.03 | Status indicator |
| R_I2C (x2) | 4.7k | 0402 | 2 | $0.01 | I2C pull-ups |
| R_SAFE (x2) | 10k | 0402 | 2 | $0.01 | Pot detect + E-stop pull-ups |
| R_BOOT | 10k | 0402 | 1 | $0.01 | BOOT0 pull-down |
| R_LED | 330R | 0402 | 1 | $0.01 | LED current limit |
| R_RLY | 330R | 0402 | 1 | $0.01 | Relay gate resistor |
| R_SPI (x6) | 33R | 0402 | 6 | $0.01 | SPI + safety series termination |
| R_LED_N | 100R | 0402 | 1 | $0.01 | Q_LED_N gate resistor |
| R_LED_PU | 10k | 0402 | 1 | $0.01 | Q_LED_P gate pull-up to 5V |
| R_LED_PD | 10k | 0402 | 1 | $0.01 | Q_LED_N gate pull-down |
| R_GATE (x19) | 100R | 0402 | 19 | $0.01 | Gate/input series resistors |
| R_PD (x16) | 10k | 0402 | 16 | $0.01 | Gate/enable pull-downs |
| R_FB (x6) | Various (10k-140k) | 0402 | 6 | $0.01 | Buck converter feedback dividers |
| R_SENSE (x1) | 1k | 0402 | 1 | $0.01 | DRV8876 #2 IPROPI sense |
| C_LDO (x2) | 10uF ceramic | 0805 | 2 | $0.10 | LDO input/output bulk |
| C_VDD (x8) | 100nF ceramic | 0402 | 8 | $0.01 | STM32 VDD decoupling |
| C_VDDA | 1uF ceramic | 0402 | 1 | $0.02 | VDDA decoupling |
| C_HSE (x2) | 18pF ceramic | 0402 | 2 | $0.01 | HSE crystal load caps |
| C_LSE (x2) | 6.8pF ceramic | 0402 | 2 | $0.01 | LSE crystal load caps |
| C_ESTOP | 100nF ceramic | 0402 | 1 | $0.01 | E-stop debounce cap |
| **CID Limit Switches** | | | | | |
| R_CID_PU (x2) | 10k | 0402 | 2 | $0.01 | CID limit switch pull-ups (PB6, PD2) |
| C_CID (x2) | 100nF ceramic | 0402 | 2 | $0.01 | CID limit switch debounce caps |
| R_STEP (x3) | 100R | 0402 | 3 | $0.01 | CID-1 stepper signal series resistors (PUL+, DIR+, ENA+) |
| C_BUCK_IN (x3) | 10uF ceramic | 0805 (25V) | 3 | $0.15 | Buck input bypass |
| C_BUCK_OUT (x6) | 22uF ceramic | 0805 | 6 | $0.12 | Buck output filter (2 per rail) |
| C_BULK | 100uF electrolytic | 8x8mm (25V) | 1 | $0.20 | 12V rail bulk |
| C_IC_DEC (x10) | 100nF ceramic | 0402 | 10 | $0.01 | IC decoupling |
| C_IC_BULK (x2) | 10uF ceramic | 0805 | 2 | $0.10 | DRV8876 #2 / TB6612 VM bypass |
| **Mechanical** | | | | | |
| SW_RST | Tactile switch | 6x6mm | 1 | $0.05 | Reset button |
| SJ1 | Solder jumper | 0603 pad | 1 | — | IRQ/SWO select |
| BZ1 | MLT-5030 or generic | 12mm piezo | 1 | $0.80 | Active piezo buzzer 5V |
| **Connectors** | | | | | |
| J_CM5 | 2x20 pin socket | 2.54mm, 8.5mm stacking | 1 | $0.80 | CM5IO GPIO header receptor |
| J_24V_IN | XT30 or JST-VH 2-pin | 2.5mm pitch | 1 | $0.40 | 24V DC input |
| J_12V_UPS | XT30 2-pin | 2.5mm pitch | 1 | $0.40 | 12V UPS input |
| J_BLDC | Hirose DF11-6DP-2DS | 2x3, 2.0mm pitch | 1 | $0.50 | BLDC motor |
| J_SLD | Hirose DF11-16DP-2DS | 2x8, 2.0mm pitch | 1 | $0.80 | SLD + pot/reservoir load cells |
| J_PASD | Hirose DF11-16DP-2DS | 2x8, 2.0mm pitch | 1 | $0.80 | P-ASD combined |
| J_PRES | Hirose DF11-4DP-2DS | 2x2, 2.0mm pitch | 1 | $0.40 | P-ASD pressure sensor I2C |
| J_FAN | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | Exhaust fans |
| J_CID | Hirose DF11-14DP-2DS | 2x7, 2.0mm pitch | 1 | $0.70 | CID stepper + linear actuator + limit switches |
| J_CAN | JST-XH 4-pin | 2.5mm pitch | 1 | $0.15 | CAN bus |
| J_BUZZER | JST-PH 2-pin | 2.0mm pitch | 1 | $0.08 | Piezo buzzer |
| J_IR | JST-SH 4-pin | 1.0mm pitch | 1 | $0.20 | MLX90614 I2C |
| J_SWD | Pin header 2x5 | 1.27mm pitch | 1 | $0.30 | SWD debug |
| J_SAFE | Hirose DF11-4DP-2DS | 2x2, 2.0mm pitch | 1 | $0.40 | Safety I/O |
| J_LED | JST-XH 3-pin | 2.5mm pitch | 1 | $0.12 | LED ring |
| J_USB | USB-C 16-pin mid-mount | SMD | 1 | $0.30 | USB programming port |
| J_BAT | JST-PH 2-pin | 2.0mm pitch | 1 | $0.08 | Li-Ion battery |
| **PCB** | 4-layer, 160x90mm | FR4 ENIG, 2oz outer | 1 | $5.50 | JLCPCB batch (5 pcs) |

### 13.1 Cost Summary

| Category | Prototype (1x) | Volume (100x) |
|----------|---------------|---------------|
| Microcontroller + Crystals | $8.50 | $6.00 |
| Power Conversion (3 bucks + LDO + passives) | $10.50 | $6.50 |
| H-Bridge ICs (DRV8876 x1 + TB6612) | $4.00 | $3.25 |
| Discrete MOSFETs + Diodes | $3.70 | $2.20 |
| I2C Peripherals (PCF8574 x2 + INA219) | $2.81 | $2.00 |
| CAN Transceiver (ISO1050 + passives) | $3.64 | $2.50 |
| Protection (polyfuses + TVS + ESD) | $2.70 | $1.60 |
| Passive Components | $3.00 | $1.50 |
| USB-C + Schottky-OR | $1.13 | $0.75 |
| Li-Ion Charger + Boost | $1.45 | $0.95 |
| Connectors (17 total) | $6.18 | $3.80 |
| PCB | $5.50 | $2.50 |
| **Total** | **~$55.50** | **~$34.50** |

> [!note]
> **Cost comparison vs 2-board design:**
> | Item | 2-Board (old) | 1-Board (unified) | Savings |
> |------|--------------|-------------------|---------|
> | Bare PCBs | $9.50 (2x) | $5.50 (1x) | $4.00 |
> | J_STACK connectors | $1.60 (2x) | $0 | $1.60 |
> | SMT Assembly | $30 (2 boards) | $20 (1 board) | $10.00 |
> | **Total savings** | | | **~$15.50/unit** |

---

## 14. Manufacturing Specifications

| Parameter | Value |
|-----------|-------|
| Layers | 4 |
| Board thickness | 1.6mm |
| Copper weight (outer) | 2 oz (70um) — required for power traces |
| Copper weight (inner) | 1 oz (35um) |
| Min trace width | 0.15mm (6 mil) signal, 1.0mm (40 mil) power |
| Min trace spacing | 0.15mm (6 mil) |
| Min via drill | 0.3mm |
| Via pad diameter | 0.6mm |
| Surface finish | ENIG (lead-free) |
| Solder mask | Green (both sides) |
| Silkscreen | White (both sides) |
| Board material | FR4, Tg >= 150C |
| Board dimensions | 160mm x 90mm |
| Mounting holes | 4x M3 at corners (3.2mm drill), matching CM5IO pattern |
| Impedance control | 50 ohm single-ended on SPI lines; 90 ohm differential on USB D+/D- |
| Panelization | 1x1 (board size exceeds standard panel at JLCPCB) |

### 14.1 Assembly Notes

- All ICs and passives are SMT (top side preferred, bottom side available for passives)
- Through-hole: Hirose DF11 dual-row connectors, JST-XH connectors (J_FAN, J_CAN, J_LED), XT30 for power inputs, 2.54mm pin headers
- J_CM5 (2x20 socket) on bottom side, top edge center — mates downward with CM5IO below
- Reflow for SMT, then wave or hand-solder through-hole
- Mark pin 1 of all multi-pin connectors with silkscreen triangle

---

## 15. Firmware Integration Notes

### 15.1 FreeRTOS Task Allocation

| Task | Rate | Priority | Functions |
|------|------|----------|-----------|
| PID Control | 100 Hz | Highest | Temperature PID loop via CAN |
| Actuator | 50 Hz | Medium | BLDC, linear actuators, pumps, solenoids, buzzer |
| Sensor | 10 Hz | Low | MLX90614, HX711, INA219 reads |
| Comms | 20 Hz | High | SPI slave protocol, message handling |

### 15.2 STM32 Timer Allocation

| Timer | Channel | Pin | Function | Frequency |
|-------|---------|-----|----------|-----------|
| TIM1 | CH1 | PA8 | BLDC Motor PWM | 10 kHz |
| TIM1 | CH3 | PA10 | CID-1 Stepper PUL (step pulse) | 200 Hz–10 kHz |
| TIM8 | CH2 | PC7 | Buzzer PWM | Variable (1-4 kHz) |
| TIM2 | CH1 | PA0 | P-ASD Pump PWM | 25 kHz |
| TIM2 | CH3 | PB10 | Exhaust Fan 2 PWM | 25 kHz |
| TIM3 | CH1 | PA6 | Exhaust Fan 1 PWM | 25 kHz |

### 15.3 I2C1 Device Map

| Address | Device | Location | Read Rate |
|---------|--------|----------|-----------|
| 0x20 | PCF8574 #1 (P-ASD solenoids + CID) | On-board | On-demand |
| 0x21 | PCF8574 #2 (SLD solenoids + LED) | On-board | On-demand |
| 0x40 | INA219 (24V current monitor) | On-board | 1 Hz |
| 0x48 | ADS1015 (P-ASD pressure) | External (J_PRES) | On-demand |
| 0x5A | MLX90614 (IR thermometer) | External (J_IR) | 10 Hz |

### 15.4 Power Failure State Machine

**STM32 behavior:**
1. COMP1 interrupt fires (24V drops below ~16.5V) → set `power_fail = true`
2. Immediately disable all actuators (CAN power OFF, all MOSFET gates LOW, PCF8574 #1 all LOW, PCF8574 #2 all LOW)
3. Send `POWER_FAIL(state=1, voltage_mV)` to CM5 via SPI
4. Enter low-power monitoring loop
5. On recovery (>20V sustained 2s): send `POWER_FAIL(state=0)`, CM5 decides whether to resume

**CM5 behavior:**
- On `POWER_FAIL(state=1)`: save cooking state to PostgreSQL, pause recipe engine, show "Power Lost" on UI
- On `POWER_FAIL(state=0)`: load saved state, prompt user or auto-resume based on elapsed time

---

## 16. Design Verification Checklist

### 16.1 Pre-Fabrication

- [ ] Schematic ERC passes with zero errors
- [ ] All STM32 pin assignments verified against datasheet alternate function table
- [ ] SPI2 peripheral confirmed on PB12-PB15 for LQFP-64 package
- [ ] No pin conflicts between SPI2, TIM1, TIM2, TIM3, I2C1, FDCAN1
- [ ] BOOT0 has pull-down resistor
- [ ] All VDD/VSS pins connected with individual decoupling caps
- [ ] VDDA has ferrite bead isolation from digital 3.3V
- [ ] Crystal load capacitors match crystal specifications
- [ ] I2C pull-up values appropriate for 100 kHz bus speed
- [ ] All buck converter feedback resistor values verified
- [ ] Inductor saturation current ratings exceed maximum load current per rail
- [ ] DRV8876 #2 IPROPI sense resistor correct (1k → 1.5V/A)
- [ ] TB6612FNG VM decoupling adequate (100nF + 10uF within 5mm)
- [ ] CID-1 stepper signal 100R series resistors present on PUL+, DIR+, ENA+ lines
- [ ] PCF8574 P7 allocated to CID-1 ENA+ (verified I2C write toggles J_CID pin 5)
- [ ] All MOSFET gate pull-downs present (safe default state)
- [ ] INA219 I2C address (0x40) does not conflict with other devices
- [ ] 24V input protection chain in correct order: Polyfuse → Schottky → TVS
- [ ] J_CM5 pinout matches CM5IO 40-pin GPIO header exactly
- [ ] USB D+/D- series resistors (22R) and ESD (USBLC6) present
- [ ] USB CC1/CC2 pulldowns (5.1kR) correctly wired to GND
- [ ] VBUS detect divider (100k/100k) on PA3 verified
- [ ] SW_BOOT tactile switch between BOOT0 and 3.3V, with 10k pull-down
- [ ] Schottky-OR (D_OR1-3) connects 5V_MAIN, 5V_USB, 5V_BATT to 5V_MERGED
- [ ] TP4056 R_PROG = 2kR (500mA charge current)
- [ ] DW01A/FS8205A protection circuit correct
- [ ] MT3608 feedback divider (732kR/100kR) gives 5.0V output
- [ ] Buzzer PWM moved from PA11 (TIM1_CH4) to PC7 (TIM8_CH2) — independent timer
- [ ] CID limit switch pull-ups (10k to 3.3V) on PB6, PD2
- [ ] CID limit switch debounce caps (100nF) on PB6, PD2
- [ ] PCF8574 P6 assigned to CID-2 Full-Extend Limit (input with internal pull-up)
- [ ] PCF8574 P7 assigned to CID-1 Stepper ENA+ (output via 100R to J_CID pin 5)
- [ ] J_CID expanded to 14-pin with stepper signals, CID-2 motor, limit switches, 24V power, and GND
- [ ] All 17 external connectors have correct pinouts

### 16.2 PCB Layout

- [ ] DRC passes with zero errors
- [ ] GND plane continuous under STM32 and SPI traces (no splits except CAN slot)
- [ ] SPI traces matched length within 2mm
- [ ] Buck converter input/output cap loops minimized (<10mm total)
- [ ] Power traces sized: >=2mm for 24V, >=1mm for 12V/5V
- [ ] Thermal vias under STM32 exposed pad (9+ vias, 0.3mm)
- [ ] Thermal vias under DRV8876 #2 exposed pad (6+ vias)
- [ ] Thermal copper pour >=400mm2 around each buck converter
- [ ] Creepage >=2mm between 24V and logic signals
- [ ] CAN isolation slot >=6mm, no copper crossing boundary
- [ ] All connectors accessible from board edges
- [ ] Mounting holes at CM5IO-matching positions (M3, 4 corners)
- [ ] Silkscreen labels on all connectors and test points
- [ ] Zone A (digital) directly above J_CM5 (top side), Zone F (bucks) 25mm+ away

### 16.3 Post-Assembly

- [ ] 3.3V rail: 3.3V +/-3% under load
- [ ] 5V rail: 5.0V +/-3% under 500mA
- [ ] 12V rail: 12.0V +/-3% under 500mA
- [ ] 6.5V rail: 6.5V +/-3% under 500mA
- [ ] 24V input draws <10mA quiescent (no actuators)
- [ ] STM32 responds to SWD probe (device ID read)
- [ ] SPI loopback test with CM5 passes
- [ ] All PWM channels output correct frequency on oscilloscope
- [ ] I2C scan detects 5 devices: PCF8574 #1 (0x20), PCF8574 #2 (0x21), INA219 (0x40), ADS1015 (0x48), MLX90614 (0x5A)
- [ ] PCF8574 #2 P0 toggles SLD oil solenoid via IRLML6344
- [ ] PCF8574 #2 P1 toggles SLD water solenoid via IRLML6344
- [ ] PCF8574 #2 P2 toggles status LED (active-low, 330R)
- [ ] PCF8574 #2 P3 controls LED ring power (via Q_LED_N → Q_LED_P)
- [ ] PA7, PA9, PC8, PA2 confirmed unconnected (no trace to old loads)
- [ ] HX711 (pot, PC0/PC1) returns stable readings
- [ ] HX711 (SLD oil reservoir, PC11/PC12) returns stable readings (±1 g)
- [ ] HX711 (SLD water reservoir, PC9/PC10) returns stable readings (±1 g)
- [ ] SLD low-level alert triggers when reservoir weight < configured threshold
- [ ] E-stop interrupt triggers on button press
- [ ] Safety relay clicks when PB0 driven high
- [ ] J_BLDC PWM verified (10 kHz, 3.3V logic)
- [ ] Solenoid MOSFETs switch correctly
- [ ] DRV8876 #2 drives CID-2 actuator in both directions
- [ ] CID-1 stepper: PA10 outputs step pulses at J_CID pin 1 (200 Hz–10 kHz range, oscilloscope)
- [ ] CID-1 stepper: PB4 toggles direction at J_CID pin 3 (multimeter)
- [ ] CID-1 stepper: PCF8574 P7 controls ENA+ at J_CID pin 5 (I2C write)
- [ ] CID-1 stepper: all "-" pins (2, 4, 6) connected to board GND (continuity)
- [ ] CID-1 stepper: 100R series resistors present on signal lines
- [ ] CID-1 stepper: 24V present at J_CID pin 12, GND at pin 13
- [ ] CID-1 home switch on J_CID pin 9 triggers PB6 EXTI
- [ ] CID-2 limit switches read LOW when pressed (at limit), HIGH when released
- [ ] CID-2 actuator stops at home and full-extend limit positions
- [ ] PCF8574 P6 reads CID-2 Full-Extend switch state correctly
- [ ] TB6612FNG drives pump with variable speed
- [ ] All actuators OFF when STM32 held in reset (pull-down verify)
- [ ] CAN loopback test passes via ISO1050
- [ ] USB-C enumerates as DFU device (BOOT0 HIGH + reset)
- [ ] USB CDC serial works after firmware flash
- [ ] Battery charges to 4.2V from USB 5V
- [ ] DW01A protection triggers at ~2.5V (over-discharge)
- [ ] MT3608 boost outputs 5V from 3.7V battery
- [ ] STM32 boots from battery alone (USB + 24V disconnected)
- [ ] Schottky-OR prevents backfeed between 5V sources
- [ ] USB D+/D- differential impedance ~90R (TDR or VNA)
- [ ] No smoke test: apply 24V, observe current, check for shorts

---

## 17. Related Documentation

- [[../02-Hardware/01-Epicura-Architecture|Epicura Architecture]] — System-level wiring and block diagrams
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]] — Induction, sensors, power specs
- [[../02-Hardware/03-Sensors-Acquisition|Sensors & Acquisition]] — Sensor interface details
- [[../05-Subsystems/01-Induction-Heating|Induction Heating]] — Microwave surface module with CAN bus
- [[../05-Subsystems/02-Robotic-Arm|Robotic Arm]] — BLDC motor arm patterns and control
- [[../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing]] — ASD/CID/SLD dispensing subsystems
- [[../05-Subsystems/05-Exhaust-Fume-Management|Exhaust & Fume Management]] — Exhaust fan control
- [[../08-Components/01-Compute-Module-Components|Compute Module Components]] — CM5 and STM32 BOM
- [[../08-Components/02-Actuation-Components|Actuation Components]] — Actuator BOM
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]] — Full system cost analysis
- [[03-PCB-Design-Rules|PCB Design Rules]] — DRC rules and net classes

### Archived Documents

The following documents were merged into this unified design and are retained for reference:
- [[_archive/01-Controller-PCB-Design|Controller PCB Design (archived)]]
- [[_archive/02-Driver-PCB-Design|Driver PCB Design (archived)]]

---

#epicura #pcb #unified #stm32 #power-electronics #actuators #hardware-design

---

## 18. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.9 | 2026-03-11 | Manas Pradhan | Added PCF8574 #2 (0x21) I2C GPIO expander for GPIO headroom; moved SLD solenoids (PA7→P0, PA9→P1), status LED (PC8→P2), and LED ring enable (PA2→P3) to PCF8574 #2; freed 4 STM32 pins (PA2, PA7, PA9, PC8) for future use; 7-8 total free GPIO; +$0.51 BOM (PCF8574 $0.50 + 100nF $0.01); I2C bus now 5 devices, within 400pF budget |
| 1.8 | 2026-03-11 | Manas Pradhan | Replaced CID-1 DC linear actuator + DRV8876 #1 with NEMA 23 stepper motor + external driver (PUL/DIR/ENA differential signals); PA10→PUL+, PB4→DIR+, PCF8574 P7→ENA+ (all via 100R); J_CID expanded 10-pin→14-pin (2x7 Hirose DF11) with stepper signals + 24V power; DRV8876 qty 2→1; PB11 freed (CID-1 extend switch removed, step counting for travel); 3× 100R stepper resistors added; BOM/thermal/checklists updated |
| 1.7 | 2026-03-10 | Manas Pradhan | Converted 6 connectors from single-row JST-XH 2.5mm to dual-row Hirose DF11 2.0mm: J_BLDC (2x3), J_PASD (2x8), J_PRES (2x2), J_SLD (2x8), J_CID (2x5, +1 GND pin), J_SAFE (2x2); more compact layout, keyed/polarized; updated BOM and cost summary (+$2/unit) |
| 1.6 | 2026-03-10 | Manas Pradhan | Added CID limit switches: 4× micro switches (2 per actuator: home + full-extend) for position feedback; PB6, PB11, PD2 assigned as GPIO EXTI inputs with 10k pull-ups and 100nF debounce; PCF8574 P6 used for CID-2 Full-Extend (no more free GPIO); J_CID expanded from 4-pin to 9-pin (added 4 switch signals + GND return); NC wiring for fail-safe; updated pin summary, BOM, verification checklists |
| 1.5 | 2026-03-10 | Manas Pradhan | Added J_PRES 4-pin connector for ADS1015 pressure sensor (I2C1 + 3.3V + GND); placed adjacent to J_PASD; renumbered sections 10.6–10.16 → 10.7–10.17; +1 connector (now 17 total) |
| 1.4 | 2026-03-10 | Manas Pradhan | Datasheet review fixes: PA1 COMP2→COMP1 (PA1 has COMP1_INP per DS12288 Table 12); buzzer moved PB11/TIM2_CH4→PC7/TIM8_CH2 (TIM2 frequency conflict: fan 25kHz vs buzzer variable tone); status LED moved PC13→PC8 (PC13 limited to 3mA sink per DS12288 Note 2); updated pin summary, timer allocation, verification checklist |
| 1.3 | 2026-03-10 | Manas Pradhan | Fixed I2C1_SCL pin error: PB6 → PA15 (AF4) — PB6 has no I2C1_SCL on LQFP-64 per datasheet DS12288; PA15 (pin 51) confirmed as I2C1_SCL AF4; PB6 now available |
| 1.2 | 2026-03-09 | Manas Pradhan | Added USB-C programming port (native USB on PA11/PA12 with USBLC6 ESD, DFU+CDC) and Li-Ion battery charger (TP4056+DW01A+FS8205A+MT3608 boost); buzzer PWM moved PA11→PB11 (TIM2_CH4); PA3 repurposed for VBUS detect; 3-way Schottky-OR 5V power architecture; +2 connectors (J_USB, J_BAT); updated BOM, zone layout, verification checklists |
| 1.1 | 2026-03-07 | Manas Pradhan | Swapped board stacking order — Unified PCB now on top (Board 2), CM5IO on bottom (Board 1); J_CM5 socket moved to bottom side of Unified PCB, pointing downward to mate with CM5IO GPIO header below |
| 1.0 | 2026-03-06 | Manas Pradhan | Initial unified document — merged Controller PCB (v11.0) and Driver PCB (v8.0) into single board design; eliminated J_STACK inter-board connector; 2-board stack (CM5IO + Unified PCB) replaces 3-board stack; all components, connectors, pin allocations, and circuits preserved from both source documents |
