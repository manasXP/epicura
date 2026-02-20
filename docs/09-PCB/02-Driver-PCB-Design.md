---
created: 2026-02-15
modified: 2026-02-20
version: 5.0
status: Draft
---

# Driver PCB Design

## Overview

The Driver PCB is the power electronics and actuator interface board in Epicura's 3-board stackable architecture. It receives low-level PWM and GPIO signals from the Controller PCB (STM32G474RE) through a 2x20 stacking connector and converts them into high-current drive signals for all actuators — servos, solenoids, linear actuators, peristaltic pumps, diaphragm pump, and the exhaust fan.

### 3-Board Stackable Architecture

```
┌─────────────────────────────────────┐
│  Board 3: CM5 IO Board (CM5IO)      │  160 x 90 mm
│  Raspberry Pi CM5 + peripherals     │
├─────────────[ 2x20 Header ]─────────┤
│  Board 2: Controller PCB            │  160 x 90 mm
│  STM32G474RE + sensors + safety     │
├─────────────[ 2x20 Header ]─────────┤
│  Board 1: Driver PCB (this doc)     │  160 x 90 mm
│  Power conversion + actuator drivers│
└─────────────────────────────────────┘
         ▲                    ▲
         │ 24V DC from PSU    │ 12V DC from UPS
```

The CM5IO board is an off-the-shelf Raspberry Pi carrier board that sits on top. The two custom boards (Controller, Driver) share a uniform 160x90mm footprint with M3 mounting holes at identical positions, connected via a 2x20-pin 2.54mm board-to-board header. The Driver PCB sits at the bottom of the stack, closest to the PSU, and distributes power and actuator connections.

### Scope

| Item | Status | Notes |
|------|--------|-------|
| **Driver PCB** (this document) | Custom design required | Power conversion + actuator drivers |
| **Controller PCB** | Custom design required | STM32G474RE + sensors (see [[Controller-PCB-Design]]) |
| **CM5 IO Board (CM5IO)** | Off-the-shelf (Raspberry Pi official) | Commercial carrier board; no custom PCB needed |
| **Mean Well PSU** | Commercial (LRS-75-24) | 24V 3.2A input to Driver PCB |

---

## Board-Level Block Diagram

```
12V UPS Input ─── F5 (3A Polyfuse) ─── SS34 ─── SMBJ12A TVS ─── 12V UPS Rail
                                                                      │
                                                              ┌───────▼────────┐
                                                              │  TPS54531      │
                                                              │  12V → 5V      │
                                                              │  5A max        │
                                                              └───────┬────────┘
                                                                      │
                                                                   5V Rail
                                                              (CM5 + Controller
                                                               + Buzzer + LED)

24V DC Input ─── Polyfuse ─── SS54 (Reverse Polarity) ─── SMBJ24A (TVS)
                                        │
                        ┌───────────────┼──────────────────┐
                        │               │                  │
                        ▼               ▼                  ▼
                ┌──────────────┐ ┌──────────────┐   Voltage Divider
                │  MP1584EN #1 │ │  MP1584EN #2 │   100kΩ / 10kΩ
                │  24V → 12V   │ │  24V → 6.5V  │       │
                │  3A max      │ │  3A max      │       ▼
                └──────┬───────┘ └──────┬───────┘   PA1 (COMP2)
                       │                │         Power Fail Detect
                12V Rail                6.5V Rail
                  │                      │
        ┌─────────┼──────────┐           │
        │         │          │           │
    ┌───▼───┐ ┌──▼──┐  ┌───▼────┐  ┌───▼───┐
    │2x Sol │ │Fan  │  │2x Lin  │  │DS3225 │
    │IRLML  │ │IRLML│  │Act     │  │Servo  │
    │6344   │ │6344 │  │DRV8876 │  │Direct │
    └───────┘ └─────┘  └────────┘  └───────┘
                                               ┌───────────────┐
                                               │P-ASD: 6x Sol │
                                               │+ 1x Pump     │
                                               │IRLML6344     │
                                               │(via PCF8574)  │
                                               └───────────────┘
                                                        │
                                                   ┌────▼────┐
                                                   │2x Peri  │
                                                   │Pump     │
                                                   │TB6612   │
                                                   └─────────┘

                   ┌──────────────┐
         24V ──────┤  INA219      │──── I2C1 (via stacking connector)
                   │  Current Mon │
                   └──────────────┘

                   ┌──────────────┐
         I2C1  ────┤  PCF8574     │──── P0-P5 → P-ASD Solenoid V1-V6 MOSFET gates
                   │  GPIO Exp.   │     (addr 0x20, 100Ω gate resistors)
                   │  (SOIC-16)   │     P6-P7 available for future use
                   └──────────────┘

All control signals arrive from Controller PCB via 2x20 stacking connector (J_STACK)
```

---

## Power Conversion

Two MP1584EN synchronous buck converters step down the 24V input to 12V and 6.5V rails for actuators and servo. A separate TPS54531 buck converter generates the 5V rail from a UPS-backed 12V DC input, ensuring the CM5 and STM32 remain powered during AC outages. The MP1584EN was selected for its wide input range (4.5-28V), high efficiency (up to 92%), and compact SOT-23-8 package with minimal external components.

### 24V → 12V Rail (MP1584EN #1)

| Parameter | Value |
|-----------|-------|
| Output Voltage | 12V |
| Max Current | 3A |
| Load | SLD solenoids (2x 0.5A), P-ASD solenoids (6x 0.5A, max 1 at a time), P-ASD pump (0.8A), exhaust fans (2x 0.5A), linear actuators (2x 1.5A peak), peristaltic pumps (2x 0.6A) |
| Inductor | 33µH, CDRH104R (Sumida), Isat > 4A |
| Output Cap | 2x 22µF MLCC (X5R, 25V) + 100µF electrolytic (25V) |
| Feedback Resistors | R_top = 100k, R_bot = 12.7k (Vout = 0.8V × (1 + 100/12.7) = 7.1V... adjusted: R_top = 140k, R_bot = 10k → 12.0V) |
| Schottky Diode | SS34 (3A, 40V) for bootstrap |
| Protection | 1.5A polyfuse + SMBJ12A TVS on output |

### 24V → 6.5V Rail (MP1584EN #2)

| Parameter | Value |
|-----------|-------|
| Output Voltage | 6.5V |
| Max Current | 3A |
| Load | DS3225 main stirring servo (stall current ~2.5A) |
| Inductor | 22µH, CDRH104R (Sumida), Isat > 4A |
| Output Cap | 2x 22µF MLCC (X5R, 16V) + 470µF electrolytic (10V, low-ESR) |
| Feedback Resistors | R_top = 71.5k, R_bot = 10k → 6.52V |
| Protection | 3A polyfuse + SMBJ6.5A TVS on output |

> [!note]
> The DS3225 servo is rated for 4.8-6.8V. Running at 6.5V provides maximum torque (25 kg·cm) while staying within safe limits. The 470µF bulk capacitor absorbs stall current transients without drooping the rail.

### 12V UPS → 5V Rail (TPS54531)

The 5V rail is now sourced from a UPS-backed 12V DC input via a TPS54531 synchronous buck converter (5A max). This ensures the CM5, STM32 controller (via 3.3V LDO on Controller PCB), buzzer, and LED ring remain powered during AC outages. The TPS54531 was selected for its wide input range (3.5-28V), high efficiency (up to 95%), integrated high-side MOSFET, and 5A output capability in a compact SOIC-8 package.

| Parameter | Value |
|-----------|-------|
| IC | TPS54531DDAR (SOIC-8) |
| Input Voltage | 12V (from UPS-backed DC input) |
| Output Voltage | 5V |
| Max Current | 5A |
| Load | CM5 (up to 3A), Controller PCB 3.3V LDO (0.17A), buzzer (0.03A), LED ring (1A peak) |
| Inductor | 10µH, CDRH127 (12.7x12.7mm), Isat > 6A |
| Output Cap | 2x 22µF MLCC (X5R, 10V) + 220µF electrolytic (10V) |
| Feedback Resistors | R_top = 52.3k, R_bot = 10k → 4.98V |
| Switching Frequency | 570 kHz (internal oscillator) |
| Protection | Integrated overcurrent, thermal shutdown, UVLO |

> [!note]
> The 5V rail was previously sourced from the 24V PSU via MP1584EN #3. Moving it to the 12V UPS input means the CM5 and STM32 stay alive during AC power outages while the UPS battery supplies 12V. The TPS54531's 5A rating provides adequate headroom for CM5 peak current (3A) plus all other 5V loads (total peak ~4.2A).

### 24V Power Failure Detection

A voltage divider on the 24V rail feeds the STM32's internal analog comparator (COMP2 on PA1) for fast hardware-based power failure detection. This enables the STM32 to immediately disable all actuators and notify the CM5 within <100µs of AC power loss.

```
24V Internal ─── R_DIV1 (100kΩ) ──┬── R_DIV2 (10kΩ) ─── GND
                                   │
                                   ├── C_DIV (100nF) ─── GND
                                   │
                                   └── PA1 (COMP2_INP) via J_STACK Pin 16
```

| Parameter | Value |
|-----------|-------|
| Divider Ratio | 10k / (100k + 10k) = 1/11 |
| Nominal Voltage at PA1 | 24V × 1/11 = 2.18V |
| Threshold (COMP2 ref) | ~1.5V (internal DAC reference) |
| Trip Voltage (24V rail) | 1.5V × 11 = 16.5V |
| Recovery Threshold | ~20V (with 2s debounce in firmware) |
| Filter Cap | 100nF on divider midpoint (noise filtering) |
| Response Time | <100µs (hardware comparator interrupt) |

> [!note]
> The INA219 continues to provide 24V rail voltage telemetry via I2C (polled every 1s in POWER_TELEMETRY messages). The comparator provides fast interrupt-driven detection for immediate safety response, while INA219 provides gradual voltage monitoring for logging and UI display.

### Power Budget Summary

| Rail | Source | Typical (A) | Peak (A) | Headroom | Notes |
|------|--------|------------|----------|----------|-------|
| 5V (5A max) | 12V UPS → TPS54531 | 1.5 | 4.0 | 20% | CM5 (3A peak) + Controller (0.17A) + buzzer + LED |
| 12V (3A max) | 24V → MP1584EN #1 | 1.9 | 3.0 | 0% | Actuators only (not needed during power fail) |
| 6.5V (3A max) | 24V → MP1584EN #2 | 0.5 | 2.5 | 17% | Servo only (not needed during power fail) |
| **24V input** | **Mean Well PSU** | **~2.0** | **~2.5** | Within PSU 3.2A rating | Reduced (5V rail no longer on 24V) |
| **12V UPS input** | **External UPS** | **1.5** | **4.0** | Within 5A fuse | UPS-backed, stays live during AC outage |

---

## Actuator Driver Circuits

### DS3225 Main Stirring Servo

The DS3225 (25 kg·cm, metal gear) connects directly to the 6.5V rail. No H-bridge is needed — standard hobby servos accept a PWM signal and have an internal driver.

```
6.5V Rail ──┬── 470µF Bulk Cap ──┬── J_SERVO_MAIN Pin 2 (VCC, red)
            │                    │
            └── SMBJ6.5A TVS ───┘
                                 │
                                GND ── J_SERVO_MAIN Pin 1 (GND, brown)

PA8 (TIM1_CH1) ── via J_STACK ── 33R ── J_SERVO_MAIN Pin 3 (Signal, orange)
```

| Parameter | Value |
|-----------|-------|
| PWM Frequency | 50 Hz |
| Pulse Width | 500-2500 µs |
| Supply | 6.5V from MP1584EN #2 |
| Bulk Cap | 470µF 10V electrolytic (low-ESR) |
| TVS | SMBJ6.5A on 6.5V rail |
| Signal Protection | 33Ω series resistor |

### P-ASD Solenoid Valves (6×)

Six 12V normally-closed solenoid valves for P-ASD (Pneumatic Advanced Seasoning Dispenser) cartridge air control, driven by low-side N-MOSFETs with flyback protection. One valve per spice cartridge. MOSFET gates are driven by a **PCF8574 I2C GPIO expander** (address 0x20) on the Driver PCB, eliminating the need for 6 dedicated STM32 GPIO pins. All six solenoids and the diaphragm pump connect via a single **J_PASD** 16-pin connector.

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
| Rds(on) | 29 mΩ @ Vgs=4.5V |
| Id(max) | 5A |
| Flyback Diode | SS14 (1A, 40V Schottky) |
| Gate Resistor | 100Ω (limits dI/dt, reduces EMI) |
| Gate Pull-down | 10kΩ to GND (safe state during STM32 boot/reset) |
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
| (Available) | P6 | Future use |
| (Available) | P7 | Future use |

**PCF8574 Configuration:**

| Parameter | Value |
|-----------|-------|
| IC | PCF8574 (SOIC-16 or DIP-16) |
| I2C Address | 0x20 (A0=A1=A2=GND) |
| I2C Bus | I2C1 (PB6/PB7 via J_STACK), shared with MLX90614 (0x5A), INA219 (0x40), ADS1015 (0x48) |
| Output Current | 25 mA sink per pin (sufficient for IRLML6344 gate charge) |
| Decoupling | 100nF MLCC on VDD |
| Cost | ~$0.50 |

### SLD Solenoid Valves (2x)

Two 12V solenoid valves for SLD (Standard Liquid Dispenser) drip prevention, driven by low-side N-MOSFETs with flyback protection.

```
12V Rail ──── Solenoid Coil ──┬── Drain (IRLML6344)
                              │
                         SS14 Flyback ─── 12V
                              │
                         10k Pull-down
                              │
PA7/PA9 ── via J_STACK ── 100R Gate Resistor ── Gate
                              │
                             GND ── Source
```

| Parameter | Value |
|-----------|-------|
| MOSFET | IRLML6344 (SOT-23) |
| Vds(max) | 30V |
| Rds(on) | 29 mΩ @ Vgs=4.5V |
| Id(max) | 5A |
| Flyback Diode | SS14 (1A, 40V Schottky) |
| Gate Resistor | 100Ω (limits dI/dt, reduces EMI) |
| Gate Pull-down | 10kΩ to GND (safe state during STM32 boot/reset) |
| Solenoid Current | ~0.5A per valve |

> [!tip]
> The 10kΩ pull-down resistors on all MOSFET gates ensure actuators remain OFF during STM32 boot, reset, or firmware crash. This is a critical safety feature.

### Exhaust Fans (2x)

Two independent 120mm 12V brushless DC fans for exhaust and fume extraction, driven by PWM via low-side MOSFETs. Independent control allows optimal airflow management.

```
12V Rail ──── Fan 1 (+) ──── Fan 1 (−) ──┬── Drain (IRLML6344 #1)
                                         │
                                    SS14 Flyback ─── 12V
                                         │
                                    10k Pull-down
                                         │
PA6 (TIM3_CH1) ── via J_STACK Pin 27 ── 100R ── Gate
                                         │
                                        GND ── Source

12V Rail ──── Fan 2 (+) ──── Fan 2 (−) ──┬── Drain (IRLML6344 #2)
                                         │
                                    SS14 Flyback ─── 12V
                                         │
                                    10k Pull-down
                                         │
PB10 (TIM2_CH3) ── via J_STACK Pin 28 ── 100R ── Gate
                                         │
                                        GND ── Source
```

| Parameter | Value |
|-----------|-------|
| Fan Size | 120mm diameter |
| PWM Frequency | 25 kHz (above audible range) |
| MOSFET | IRLML6344 (SOT-23) |
| Flyback Diode | SS14 |
| Gate Resistor | 100Ω |
| Gate Pull-down | 10kΩ |
| Fan Current | ~0.3-0.5A typical per fan |

> [!note]
> Independent control of both fans enables optimal airflow management. During light cooking, one fan may suffice; during high-heat operations, both fans can run at full speed for maximum exhaust capacity.

### CID Linear Actuators (2x) — DRV8876RGTR

Two linear actuators for CID (Coarse Ingredients Dispenser) push-plate sliders, each driven by a TI DRV8876RGTR H-bridge IC. The DRV8876 provides integrated current sensing, current regulation, and fault reporting.

```
12V Rail ──── VM (DRV8876) ──── OUT1 ──┐
                                       │  Linear Actuator
              VREF ◄── 3.3V           │  (12V, 1.5A nominal)
                                       │
              GND ─── GND      OUT2 ──┘
                │
                ├── EN/PWM ◄── PA10 or PB5 (via J_STACK, 100R gate)
                ├── PH/DIR ◄── PB4 or PC2 (via J_STACK, 100R)
                ├── nSLEEP ◄── 3.3V (always awake, or GPIO for sleep control)
                ├── nFAULT ──► (optional: route to STM32 via J_STACK reserved pin)
                ├── IPROPI ──► Sense resistor to GND (current monitor output)
                │
           C_VM: 100nF + 10µF bypass on VM
           C_VCC: 100nF bypass on VCC (internal regulator)
```

| Parameter | Value |
|-----------|-------|
| IC | DRV8876RGTR (WSON-8, 3x3mm) |
| Supply (VM) | 12V |
| Continuous Current | 3.5A per channel |
| Peak Current | 5A (transient) |
| Rds(on) (H+L) | 350 mΩ typical |
| Control Mode | PH/EN (Phase/Enable) |
| EN Pin | PWM speed control (up to 100 kHz) |
| PH Pin | Direction: HIGH = forward, LOW = reverse |
| nSLEEP | Tied to 3.3V via 10kΩ (always active) |
| Current Sense | IPROPI: 1500 µA/A ratio, 1kΩ sense resistor → 1.5V/A |
| Protection | Built-in: overcurrent, thermal shutdown, undervoltage lockout |
| Decoupling | 100nF + 10µF MLCC on VM, 100nF on VCC |
| Input Resistors | 100Ω series on EN, PH inputs |
| Gate Pull-down | 10kΩ on EN (motor off during boot) |

**Pin Allocation:**

| Actuator | EN/PWM Pin | PH/DIR Pin |
|----------|------------|------------|
| Linear Actuator 1 | PA10 | PB4 |
| Linear Actuator 2 | PB5 | PC2 |

### SLD Peristaltic Pumps (2x) — TB6612FNG

Two peristaltic pumps for SLD (Standard Liquid Dispenser) precise liquid dispensing (oil + water), driven by a single TB6612FNG dual H-bridge IC. The TB6612FNG handles both channels in one compact SSOP-24 package.

```
12V Rail ──── VM (TB6612FNG)
              │
         ┌────┤
         │    ├── PWMA ◄── PC3 (via J_STACK, 100R) ── Pump 1 Speed
         │    ├── AIN1 ◄── PC4 (via J_STACK, 100R) ── Pump 1 Direction
         │    ├── AIN2 ◄── (inverted from AIN1 via 74LVC1G04 or tied LOW)
         │    ├── AO1 ───┐
         │    ├── AO2 ───┤── Pump 1 Motor
         │    │          │
         │    ├── PWMB ◄── PC5 (via J_STACK, 100R) ── Pump 2 Speed
         │    ├── BIN1 ◄── PC6 (via J_STACK, 100R) ── Pump 2 Direction
         │    ├── BIN2 ◄── (inverted from BIN1 via 74LVC1G04 or tied LOW)
         │    ├── BO1 ───┐
         │    ├── BO2 ───┤── Pump 2 Motor
         │    │          │
         │    ├── STBY ◄── 3.3V (always active, 10kΩ pull-up)
         │    └── GND ─── GND
         │
    C_VM: 100nF + 10µF
```

| Parameter | Value |
|-----------|-------|
| IC | TB6612FNG (SSOP-24) |
| Supply (VM) | 12V (max 15V) |
| Supply (VCC) | 3.3V (logic supply, max 5.5V) |
| Continuous Current | 1.2A per channel |
| Peak Current | 3.2A per channel (pulsed) |
| Rds(on) | 0.5Ω typical (high + low side) |
| PWMA/PWMB | PWM speed control (up to 100 kHz) |
| AIN1/BIN1 | Direction control: H = forward, L = reverse |
| AIN2/BIN2 | Tied LOW on-board (single-direction default), or driven by inverter for H-bridge mode |
| STBY | Tied HIGH via 10kΩ to 3.3V |
| Decoupling | 100nF + 10µF MLCC on VM, 100nF on VCC |
| Input Resistors | 100Ω series on PWMA, PWMB, AIN1, BIN1 |
| Pull-downs | 10kΩ on PWMA, PWMB (pumps off during boot) |

**Pin Allocation:**

| Signal | STM32 Pin | TB6612 Pin | Function |
|--------|-----------|------------|----------|
| PUMP1_PWM | PC3 | PWMA | Pump 1 speed |
| PUMP1_DIR | PC4 | AIN1 | Pump 1 direction |
| PUMP2_PWM | PC5 | PWMB | Pump 2 speed |
| PUMP2_DIR | PC6 | BIN1 | Pump 2 direction |

> [!note]
> AIN2 and BIN2 are tied LOW on the driver board. For forward pumping, set AIN1/BIN1 HIGH and apply PWM on PWMA/PWMB. For reverse flush (cleaning), set AIN1/BIN1 LOW and pulse AIN2/BIN2 (requires cutting trace and routing to GPIO — not needed for prototype).

### Piezo Buzzer (1x)

Active piezo buzzer (5V, 3-24 kHz PWM-capable) for audio feedback on errors, faults, task completion, and timer initiation. Driven by a 2N7002 N-MOSFET with PWM from STM32.

```
5V Rail ──── Buzzer (+) ──── Buzzer (−) ──┬── Drain (2N7002)
                                          │
                                     10k Pull-down
                                          │
PA11 (TIM1_CH4) ── via J_STACK ── 100R ── Gate
                                          │
                                         GND ── Source
```

| Parameter | Value |
|-----------|-------|
| Buzzer | MLT-5030 or generic active piezo (5V) |
| MOSFET | 2N7002 (SOT-23) |
| Vds(max) | 60V |
| Rds(on) | 2.5Ω @ Vgs=4.5V |
| Id(max) | 300 mA |
| PWM Frequency | Variable (2-4 kHz for tones, 10 Hz for beeps) |
| Gate Resistor | 100Ω |
| Gate Pull-down | 10kΩ (buzzer off during boot) |
| Current | ~20-30 mA typical |

**Audio Alert Patterns:**

| Event | Pattern | Frequency | Duration |
|-------|---------|-----------|----------|
| Task Complete | 3 short beeps | 2.5 kHz | 200ms on, 100ms off, 3x |
| Error/Fault | Continuous beep | 1 kHz | Until acknowledged |
| Timer Start | 2 quick beeps | 3 kHz | 100ms on, 100ms off, 2x |
| Warning | Single beep | 2 kHz | 500ms |
| Cooking Stage Change | Ascending tones | 2-3 kHz sweep | 300ms |
| E-Stop | Pulsing alarm | 1-2 kHz alternating | Continuous |

### P-ASD Diaphragm Pump (1×)

A 12V micro diaphragm pump (3-4 L/min) pressurizes the P-ASD accumulator. Driven by an IRLML6344 N-MOSFET with PWM speed control from STM32.

```
12V Rail ──── Pump Motor (+) ──── Pump Motor (−) ──┬── Drain (IRLML6344)
                                                    │
                                               SS14 Flyback ─── 12V
                                                    │
                                               10k Pull-down
                                                    │
PA0 (TIM2_CH1) ── via J_STACK Pin 15 ── 100R ── Gate
                                                    │
                                                   GND ── Source
```

| Parameter | Value |
|-----------|-------|
| Pump | 12V micro diaphragm, 3-4 L/min, <45 dB |
| MOSFET | IRLML6344 (SOT-23) |
| Vds(max) | 30V |
| Rds(on) | 29 mΩ @ Vgs=4.5V |
| PWM Frequency | 25 kHz (above audible range) |
| Gate Resistor | 100Ω |
| Gate Pull-down | 10kΩ (pump off during boot) |
| Pump Current | 0.5–0.8A typical |

---

## Input Protection

### 24V Input Protection Chain

```
24V from PSU ──── F1 (5A Polyfuse) ──── D1 (SS54 Schottky) ──┬── D2 (SMBJ24A TVS) ──── 24V Internal
                                                               │
                                                              GND
```

| Component | Part | Function |
|-----------|------|----------|
| F1 | 5A resettable polyfuse (1812 package) | Overcurrent protection, self-resetting |
| D1 | SS54 (5A, 40V Schottky) | Reverse polarity protection (Vf = 0.5V drop) |
| D2 | SMBJ24A (24V TVS, 600W) | Transient voltage suppression from PSU spikes |

### 12V UPS Input Protection Chain

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

### Per-Rail Protection

| Rail | Polyfuse | TVS Diode | Notes |
|------|----------|-----------|-------|
| 12V | 1.5A (0805) | SMBJ12A | Protects solenoid/fan/actuator branch |
| 6.5V | 3A (1206) | SMBJ6.5A | Protects DS3225 servo branch |
| 5V | — | — | Protected at UPS input (F5 + D_UPS2); TPS54531 has integrated OCP |

### MOSFET Gate Safety

All MOSFET and H-bridge IC enable pins have:
- **100Ω series gate resistor** — limits gate charge current, reduces ringing and EMI
- **10kΩ pull-down to GND** — ensures actuators are OFF during STM32 boot, reset, or brown-out

This guarantees a safe default state for all actuators regardless of controller firmware status.

---

## Current Monitoring — INA219

An INA219 bidirectional current/power monitor on the 24V input rail provides real-time power consumption telemetry to the CM5 via I2C.

```
24V Input ──── R_shunt (10 mΩ, 2512, 1%) ──── 24V Internal
                    │                │
                    IN+             IN−
                    │                │
              ┌─────▼────────────────▼─────┐
              │         INA219             │
              │                            │
              │  VS+    VS−    SDA    SCL  │
              │   │      │      │      │   │
              │   │      │      │      │   │
              └───┼──────┼──────┼──────┼───┘
                  │      │      │      │
                 3.3V   GND     │      │
                                │      │
              PB7 (I2C1_SDA)  ◄─┘      └─► PB6 (I2C1_SCL)
              (via J_STACK)               (via J_STACK)
```

| Parameter | Value |
|-----------|-------|
| IC | INA219BIDR (SOT-23-8) |
| I2C Address | 0x40 (A0=GND, A1=GND) |
| Shunt Resistor | 10 mΩ, 2512 package, 1%, 1W rated |
| Bus Voltage Range | 0-26V (covers 24V rail) |
| Max Shunt Voltage | ±320 mV (supports up to 32A with 10 mΩ) |
| Current Resolution | ~0.1 mA per LSB (at 10 mΩ shunt, PGA /1) |
| I2C Bus | Shared with MLX90614 (0x5A) on Controller PCB |
| Decoupling | 100nF on VS+ |

The INA219 shares the I2C1 bus with the MLX90614 IR thermometer (0x5A) on the Controller PCB, the ADS1015 pressure sensor (0x48), and the PCF8574 GPIO expander (0x20) on the Driver PCB. All four devices have distinct addresses so no conflict exists. I2C signals route through the stacking connector.

---

## Stacking Connector — J_STACK

### Physical Specifications

| Parameter | Value |
|-----------|-------|
| Connector | 2x20 pin header/socket, 2.54mm pitch |
| Mating Height | 11mm (standard stacking height) |
| Current Rating | 3A per pin (paralleled for power) |
| Orientation | Pin 1 marked with silkscreen triangle + square pad |
| Location | Center of board long edge (matching Controller PCB) |

### Pinout (Bottom View — Driver PCB)

| Pin | Signal | Direction | Pin | Signal | Direction |
|-----|--------|-----------|-----|--------|-----------|
| **Power Rails (Pins 1-14)** ||||
| 1 | 24V_IN | Power In | 2 | 24V_IN | Power In |
| 3 | 24V_IN | Power In | 4 | 24V_IN | Power In |
| 5 | GND | Power | 6 | GND | Power |
| 7 | GND | Power | 8 | GND | Power |
| 9 | GND | Power | 10 | GND | Power |
| 11 | 5V | Power | 12 | 5V | Power |
| 13 | 3.3V | Power | 14 | 3.3V | Power |
| **P-ASD Subsystem (Pins 15-20, 39)** ||||
| 15 | PASD_PUMP_PWM (PA0) | In | 16 | PWR_FAIL (PA1) | Out |
| 17 | HX711_SCK (PC0) | In | 18 | HX711_DOUT (PC1) | Out |
| 19 | Reserved (was PASD_SOL4) | — | 20 | Reserved (was PASD_SOL5) | — |
| **CID Subsystem (Pins 21-26)** ||||
| 21 | CID_LACT1_EN (PA10) | In | 22 | CID_LACT1_PH (PB4) | In |
| 23 | CID_LACT2_EN (PB5) | In | 24 | CID_LACT2_PH (PC2) | In |
| 25 | GND | Power | 26 | GND | Power |
| **Exhaust Fans (Pins 27-28)** ||||
| 27 | FAN1_PWM (PA6) | In | 28 | FAN2_PWM (PB10) | In |
| **SLD Subsystem (Pins 29-36)** ||||
| 29 | SLD_PUMP1_PWM (PC3) | In | 30 | SLD_PUMP1_DIR (PC4) | In |
| 31 | SLD_PUMP2_PWM (PC5) | In | 32 | SLD_PUMP2_DIR (PC6) | In |
| 33 | SLD_SOL1_EN (PA7) | In | 34 | SLD_SOL2_EN (PA9) | In |
| 35 | I2C1_SCL (PB6) | Bidir | 36 | I2C1_SDA (PB7) | Bidir |
| **Main Actuators & Audio (Pins 37-40)** ||||
| 37 | MAIN_SERVO_PWM (PA8) | In | 38 | BUZZER_PWM (PA11) | In |
| 39 | Reserved (was PASD_SOL6) | — | 40 | GND | Power |

### Pin Group Summary

| Group | Pins | Count | Purpose |
|-------|------|-------|---------|
| 24V Power | 1-4 | 4 | Paralleled for 12A total capacity (4x 3A) |
| GND | 5-10, 25-26, 40 | 9 | Low-impedance ground return (6 main + 2 CID + 1 main actuators) |
| 5V | 11-12 | 2 | 5V reference/supply passthrough |
| 3.3V | 13-14 | 2 | Logic-level reference passthrough |
| **P-ASD** (Seasoning) | 15 | 1 | 1× pump PWM (PA0); solenoids V1-V6 via PCF8574 (I2C1, 0x20) on Driver PCB |
| **CID** (Coarse) | 21-26 | 6 | 2× actuator EN/PH (PA10/PB4, PB5/PC2), 2× GND |
| **Exhaust Fans** | 27-28 | 2 | FAN1 (PA6), FAN2 (PB10) |
| **SLD** (Liquid) | 29-36 | 8 | 2× pump PWM/DIR (PC3-PC6), 2× solenoid (PA7, PA9), I2C (INA219) |
| **Main** (Arm/Audio) | 37-38, 40 | 3 | Main servo (PA8), buzzer (PA11), 1× GND |

> [!note]
> Subsystem grouping enables modular wiring harnesses. P-ASD pump PWM on pin 15; solenoids V1-V6 are driven locally by a PCF8574 I2C GPIO expander on the Driver PCB (no J_STACK pins needed). CID signals (21-26) together, exhaust fans (27-28) together, etc. Dedicated GND pins (25-26 for CID, 40 for main actuators) improve current return paths for high-power actuators.

> [!warning]
> The 24V pins carry up to 3A total from the PSU. Four paralleled pins provide adequate current capacity, but traces on both boards must be sized for ≥1A per pin (minimum 0.5mm / 20 mil trace width on 2oz copper).

---

## PCB Stackup and Layout

### 4-Layer Stackup

```
┌──────────────────────────────────────────────┐
│  Layer 1 (Top)    — Signal + Components       │  70um Cu (2 oz)
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 2 (Inner1) — GND Plane (continuous)    │  35um Cu (1 oz)
├──────────────────────────────────────────────┤
│  Core             — FR4, 0.8mm               │
├──────────────────────────────────────────────┤
│  Layer 3 (Inner2) — 12V / 5V / 12V-UPS Split   │  35um Cu (1 oz)
├──────────────────────────────────────────────┤
│  Prepreg          — FR4, 0.2mm               │
├──────────────────────────────────────────────┤
│  Layer 4 (Bottom) — Signal + Power Traces     │  70um Cu (2 oz)
└──────────────────────────────────────────────┘

Total thickness: ~1.6mm (standard)
Material: FR4 (Tg 150°C minimum)
Outer copper: 2 oz (70µm) for high-current power traces
Inner copper: 1 oz (35µm) for planes
```

> [!note]
> 2oz outer copper allows power traces to carry higher current in less width. A 1mm (40 mil) trace on 2oz copper handles ~3A with <10°C rise. This is critical for the 24V input, 12V actuator, and 6.5V servo power paths.

### Component Placement Zones

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          160mm                                           │
│  ┌───────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │
│  │  INPUT PROTECTION │  │  BUCK CONVERTERS │  │  CURRENT MONITOR     │   │
│  │  24V: Polyfuse,   │  │  2x MP1584EN     │  │  INA219 + Shunt      │   │
│  │  SS54, SMBJ24A    │  │  1x TPS54531     │  │  + Power Fail Detect │   │
│  │  12V UPS: F5,     │  │  + inductors     │  │  (voltage divider    │   │ 90mm
│  │  SS34, SMBJ12A    │  │  + output caps   │  │   + COMP2)           │   │
│  │  24V + 12V CONNS  │  │                  │  │                      │   │
│  └───────────────────┘  └──────────────────┘  └──────────────────────┘   │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐    │
│  │  H-BRIDGE ICs    │  │  MOSFET DRIVERS  │  │  STACKING CONNECTOR  │    │
│  │  2x DRV8876      │  │  11x IRLML6344   │  │  J_STACK (2x20)      │    │
│  │  1x TB6612FNG    │  │  1x 2N7002       │  │  Center of board     │    │
│  │  + decoupling    │  │  + flyback diodes│  │  long edge           │    │
│  │                  │  │  + gate resistors│  │                      │    │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘    │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │                    OUTPUT CONNECTORS                             │    │
│  │  J_SERVO_MAIN  J_PASD  J_FAN1-2  J_LACT[1-2]                     │    │
│  │  J_SLD  J_24V_IN  J_12V_UPS  J_BUZZER                           │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  Board Edge ──────────────────────── M3 Mounting Holes (4 corners)       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Board Dimensions

| Parameter | Value |
|-----------|-------|
| Board Size | 160mm x 90mm (matches CM5 IO Board and Controller PCB) |
| Mounting Holes | 4x M3 at corners (3.2mm drill), positions match stack |
| Stacking Connector | Center of one long edge, bottom side |
| Output Connectors | Distributed along remaining three edges |
| Keep-out Zone | 5mm from board edges for mounting clearance |

### Critical Layout Rules

| Rule | Specification | Rationale |
|------|---------------|-----------|
| Power input traces | ≥2mm wide (2oz Cu), as short as possible | Carry up to 3.2A from PSU |
| Buck converter loops | Minimize input cap → IC → inductor → output cap loop area | Reduce EMI radiation |
| Inductor placement | Within 5mm of MP1584EN IC, away from signal traces | Magnetic field coupling |
| GND plane | Continuous under all buck converters and H-bridge ICs | Low-impedance return path |
| Power plane split | 12V zone (left) / 6.5V zone (center) / 12V-UPS+5V zone (right) on Layer 3 | Isolate noisy actuator power from UPS-backed compute power |
| MOSFET drain traces | ≥1mm wide, short runs to output connectors | Current capacity + minimize parasitic inductance |
| I2C traces | Route away from switching nodes, 4.7kΩ pull-ups on Controller PCB | Signal integrity for INA219 |
| Thermal relief | Wide GND vias under MP1584EN and DRV8876 exposed pads | Heat dissipation to inner GND plane |
| Creepage | ≥2mm between 24V and logic signals | IEC 60335 clearance requirement |

---

## Connector Definitions

Connectors are organized by subsystem for modular wiring harness assembly.

### Power Inputs

**J_24V_IN — 24V DC Power Input (XT30 or JST-VH 2-pin)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | +24V | From Mean Well LRS-75-24 |
| 2 | GND | Power ground |

**J_12V_UPS — 12V UPS-Backed DC Input (XT30 2-pin)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | +12V | From external 12V UPS battery backup |
| 2 | GND | Power ground |

### P-ASD Subsystem Connector (1 connector)

**J_PASD — Combined P-ASD Connector (1x 16-pin JST-XH 2.5mm)**

All six solenoid valves and the diaphragm pump are combined into a single connector block for cleaner wiring harness assembly.

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 12V_SOL1 | Solenoid V1 power (switched by IRLML6344, gate via PCF8574 P0) |
| 2 | SOL1_OUT | Solenoid V1 drain (Turmeric) |
| 3 | 12V_SOL2 | Solenoid V2 power (switched by IRLML6344, gate via PCF8574 P1) |
| 4 | SOL2_OUT | Solenoid V2 drain (Chili) |
| 5 | 12V_SOL3 | Solenoid V3 power (switched by IRLML6344, gate via PCF8574 P2) |
| 6 | SOL3_OUT | Solenoid V3 drain (Cumin) |
| 7 | 12V_SOL4 | Solenoid V4 power (switched by IRLML6344, gate via PCF8574 P3) |
| 8 | SOL4_OUT | Solenoid V4 drain (Salt) |
| 9 | 12V_SOL5 | Solenoid V5 power (switched by IRLML6344, gate via PCF8574 P4) |
| 10 | SOL5_OUT | Solenoid V5 drain (Garam Masala) |
| 11 | 12V_SOL6 | Solenoid V6 power (switched by IRLML6344, gate via PCF8574 P5) |
| 12 | SOL6_OUT | Solenoid V6 drain (Coriander) |
| 13 | 12V_PUMP | Pump power (switched by IRLML6344, PA0 via J_STACK Pin 15) |
| 14 | PUMP_OUT | Pump drain |
| 15 | GND | Common ground |
| 16 | GND | Common ground |

### CID Subsystem Connectors (2 total)

**J_CID_LACT1, J_CID_LACT2 — Linear Actuators (2x 2-pin JST-XH 2.5mm)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | OUT1 | DRV8876 output 1 |
| 2 | OUT2 | DRV8876 output 2 |

### SLD Subsystem Connectors (1 connector)

**J_SLD — Combined SLD + Pot Load Cell Connector (1x 12-pin JST-XH 2.5mm)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | PUMP1_AO1 | TB6612 output A1 (oil pump +) |
| 2 | PUMP1_AO2 | TB6612 output A2 (oil pump −) |
| 3 | PUMP2_BO1 | TB6612 output B1 (water pump +) |
| 4 | PUMP2_BO2 | TB6612 output B2 (water pump −) |
| 5 | 12V_SOL1 | Oil solenoid power (switched) |
| 6 | SOL1_OUT | Oil solenoid drain (PA7) |
| 7 | 12V_SOL2 | Water solenoid power (switched) |
| 8 | SOL2_OUT | Water solenoid drain (PA9) |
| 9 | HX711_SCK | Clock output to HX711 (PC0 via J_STACK Pin 17) |
| 10 | HX711_DOUT | Data input from HX711 (PC1 via J_STACK Pin 18) |
| 11 | 3.3V | HX711 supply |
| 12 | GND | HX711 ground |

### Main Actuators (3 total)

**J_MAIN_SERVO — DS3225 Stirring Servo (3-pin header, 2.54mm)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | GND | Brown wire |
| 2 | 6.5V | Red wire (from MP1584EN #2) |
| 3 | Signal | Orange wire (PA8 via J_STACK) |

**J_FAN1, J_FAN2 — Exhaust Fans (2x 2-pin JST-XH 2.5mm)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 12V | Fan power (switched by MOSFET) |
| 2 | FAN1_OUT | Drain side of IRLML6344 #1 (PA6 via J_STACK Pin 27) |

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 12V | Fan power (switched by MOSFET) |
| 2 | FAN2_OUT | Drain side of IRLML6344 #2 (PB10 via J_STACK Pin 28) |

**J_BUZZER — Piezo Buzzer (2-pin JST-PH 2.0mm)**

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | 5V | Buzzer power (switched by 2N7002) |
| 2 | BUZZ_OUT | Drain side of 2N7002 (PA11 via J_STACK) |

### Inter-Board

**J_STACK — Stacking Connector to Controller PCB (2x20 socket, 2.54mm)**

See [[#Stacking Connector — J_STACK]] section for full pinout.

---

## STM32 Pin Allocation Update

The Driver PCB introduces 14 new STM32 pin assignments (beyond the existing Controller PCB allocations). These pins were previously marked as "Available" or "Reserved" in the Controller PCB design.

### New Pin Assignments

| Pin | Previous Status | New Function | Peripheral | Direction | Target |
|-----|----------------|--------------|------------|-----------|--------|
| PA6 | Available (was IGBT HIN) | TIM3_CH1 | Exhaust Fan 1 PWM (25 kHz) | Output | J_FAN1 via MOSFET |
| PB10 | Available | GPIO (software PWM) | Exhaust Fan 2 PWM (25 kHz) | Output | J_FAN2 via MOSFET |
| PA7 | Available (was IGBT LIN) | GPIO | SLD Solenoid 1 Enable | Output | J_SLD pin 6 via MOSFET |
| PA9 | Reserved | GPIO | SLD Solenoid 2 Enable | Output | J_SLD pin 8 via MOSFET |
| PA10 | Reserved | TIM1_CH3 / GPIO | Linear Actuator 1 EN/PWM | Output | DRV8876 #1 EN |
| PB4 | Available | GPIO | Linear Actuator 1 PH/DIR | Output | DRV8876 #1 PH |
| PB5 | Available | GPIO | Linear Actuator 2 EN/PWM | Output | DRV8876 #2 EN |
| PC2 | Available | GPIO | Linear Actuator 2 PH/DIR | Output | DRV8876 #2 PH |
| PC3 | Available | GPIO | Pump 1 Speed (PWMA) | Output | TB6612 PWMA |
| PC4 | Available | GPIO | Pump 1 Direction (AIN1) | Output | TB6612 AIN1 |
| PC5 | Available | GPIO | Pump 2 Speed (PWMB) | Output | TB6612 PWMB |
| PC6 | Available | GPIO | Pump 2 Direction (BIN1) | Output | TB6612 BIN1 |
| PA11 | Reserved (USB) | TIM1_CH4 | Piezo Buzzer PWM | Output | J_BUZZER via MOSFET |
| ~~PC7~~ | ~~Available~~ | ~~GPIO~~ | ~~P-ASD Solenoid V3~~ | ~~Output~~ | ~~Removed — now via PCF8574~~ |
| ~~PD2~~ | ~~Available~~ | ~~GPIO~~ | ~~P-ASD Solenoid V4~~ | ~~Output~~ | ~~Removed — now via PCF8574~~ |
| ~~PB11~~ | ~~Available~~ | ~~GPIO~~ | ~~P-ASD Solenoid V6~~ | ~~Output~~ | ~~Removed — now via PCF8574~~ |

### Complete Pin Usage Summary (Controller + Driver PCBs)

| Port | Used Pins | Total Used | Available |
|------|-----------|------------|-----------|
| PA | PA0-PA2, PA4-PA11, PA13, PA14 | 13 | PA3 (freed from P-ASD solenoid), PA12 (USB reserved), PA15 |
| PB | PB0-PB10, PB12-PB15 | 15 | PB11 (freed from P-ASD solenoid V6) |
| PC | PC0-PC6, PC9-PC12, PC13-PC15 | 12 | PC7 (freed from P-ASD solenoid V3), PC8 |
| PD | — | 0 | PD2 (freed from P-ASD solenoid V4) |

> [!note]
> P-ASD solenoids V1-V6 are now driven by a PCF8574 I2C GPIO expander (address 0x20) on the Driver PCB instead of direct STM32 GPIO pins. This freed 6 GPIO pins; PA1 is now COMP2 (power fail detection), PA2 is now LED ring power enable. Remaining free: PA3, PC7, PD2, PB11. The PCF8574 shares the I2C1 bus with MLX90614 (0x5A), INA219 (0x40), and ADS1015 (0x48) — no address conflicts.

All new signals pass through the J_STACK stacking connector — no additional cabling between Controller and Driver PCBs is needed.

---

## Firmware Integration

### New SPI Message Types

The following SPI message types are added to the CM5 ↔ STM32 protocol for Driver PCB actuators:

| Message | Type Code | Direction | Payload |
|---------|-----------|-----------|---------|
| SET_LINEAR_ACT | 0x06 | CM5 → STM32 | actuator_id (uint8), direction (uint8), speed_pct (uint8) |
| SET_PUMP | 0x07 | CM5 → STM32 | pump_id (uint8), direction (uint8), speed_pct (uint8), volume_ml (uint16) |
| SET_PASD_PUMP | 0x08 | CM5 → STM32 | speed_pct (uint8), state (uint8: 0=off, 1=on) |
| SET_SOLENOID | 0x09 | CM5 → STM32 | valve_id (uint8), state (uint8: 0=off, 1=on) |
| SET_BUZZER | 0x0A | CM5 → STM32 | pattern (uint8: 0=off, 1=beep, 2=error, 3=complete, 4=warning), duration_ms (uint16) |
| POWER_TELEMETRY | 0x13 | STM32 → CM5 | bus_voltage_mV (uint16), current_mA (uint16), power_mW (uint16) |
| POWER_FAIL | 0x14 | STM32 → CM5 | state (uint8: 0=OK, 1=FAIL), voltage_mV (uint16) |

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

### FreeRTOS Task Updates

| Task | Additions | Priority |
|------|-----------|----------|
| Actuator Task (new) | Linear actuator position control, pump volume metering | Medium (same as servo task, 50 Hz) |
| Sensor Task | Add INA219 I2C read every 1s (power monitoring) | Low (10 Hz, existing) |
| Comms Task | Handle new message types (0x06-0x09, 0x13) | High (20 Hz, existing) |

### STM32 Timer Allocation

| Timer | Existing Use | New Channels |
|-------|-------------|--------------|
| TIM1 | CH1: DS3225 servo (PA8) | CH3: Linear Actuator 1 PWM (PA10), CH4: Buzzer PWM (PA11) |
| TIM3 | Unused | CH1: Exhaust Fan 1 PWM (PA6, 25 kHz) |
| TIM2 | Previously ASD SG90 servos (removed) | CH1: P-ASD pump PWM (PA0, 25 kHz); PB10 for Fan 2 uses software/GPIO-based PWM at 25 kHz |

> [!note]
> PB10 (Fan 2) can use TIM2_CH3 alternate function. With ASD servos removed, TIM2 channels are now available. TIM2_CH1 (PA0) is used for P-ASD pump PWM. Fan 2 can use TIM2_CH3 on PB10, or software PWM if a timer conflict arises.

### INA219 Driver

```
I2C1 Read Sequence (every 1 second):
1. Write config register (0x00): PGA /1, 12-bit, continuous
2. Read shunt voltage register (0x01) → convert to current (I = V_shunt / R_shunt)
3. Read bus voltage register (0x02) → 24V rail voltage
4. Calculate power: P = V_bus × I_shunt
5. Pack into POWER_TELEMETRY message (0x13) for next SPI transaction
```

### Power Failure State Machine (Firmware)

The following describes the intended firmware behavior for power failure handling. Implementation is deferred to the embedded firmware phase.

**STM32 behavior:**

1. COMP2 interrupt fires (24V drops below ~16.5V) → set `power_fail = true`
2. Immediately disable all actuators:
   - Send CAN command to induction module: power OFF
   - Set all MOSFET gates LOW (pull-downs ensure safe state)
   - Set PCF8574 all outputs LOW (P-ASD solenoids off)
3. Send `POWER_FAIL(state=1, voltage_mV)` to CM5 via SPI
4. Assert `PWR_FAIL` signal LOW on J_STACK pin 16
5. Enter low-power monitoring loop: poll 24V via comparator
6. When 24V recovers (>20V sustained for >2 seconds debounce):
   - Deassert `PWR_FAIL` (HIGH)
   - Send `POWER_FAIL(state=0, voltage_mV)` to CM5
   - CM5 decides whether to resume cooking

**CM5 behavior:**

- On `POWER_FAIL(state=1)`: save cooking state to PostgreSQL, pause recipe engine, show "Power Lost" on UI
- On `POWER_FAIL(state=0)`: load saved state, prompt user or auto-resume based on elapsed time (<5 min: auto-resume, >5 min: prompt user)

---

## Thermal Analysis

### Component Power Dissipation

| Component | Condition | Power (W) | Thermal Path |
|-----------|-----------|-----------|--------------|
| MP1584EN #1 (12V) | 2A continuous | ~2.7 | IC + inductor, PCB copper pour |
| MP1584EN #2 (6.5V) | 1A average | ~1.0 | IC + inductor, PCB copper pour |
| TPS54531 (5V) | 2A average | ~0.5 | SOIC-8 + inductor, PCB copper pour (higher efficiency than MP1584EN) |
| DRV8876 #1 | 1.5A continuous | ~0.8 | WSON-8 exposed pad → GND plane vias |
| DRV8876 #2 | 1.5A continuous | ~0.8 | WSON-8 exposed pad → GND plane vias |
| TB6612FNG | 1.2A total | ~0.7 | SSOP-24 thermal pad → PCB |
| IRLML6344 (x11) | 0.5-1A each | ~0.03 each | SOT-23, negligible (4 SLD/fan + 7 P-ASD; max 1-2 P-ASD active at a time) |
| 2N7002 (x1) | 0.03A | ~0.002 | SOT-23, negligible (buzzer only) |
| INA219 | Monitoring only | ~0.01 | Negligible |
| SS54 input diode | 3A peak | ~1.5 | SMA package, PCB copper pour |
| Shunt resistor | 3A peak | ~0.09 | 2512 package |
| **Total** | | **~8.5W typical** | |

### Temperature Estimates

At 40°C ambient (inside Epicura enclosure near induction surface):

| Component | θJA (°C/W) | Dissipation (W) | Est. Junction Temp (°C) |
|-----------|-----------|-----------------|-------------------------|
| MP1584EN #1 | ~50 | 2.7 | 40 + 135 = 175 — **Needs attention** |
| DRV8876 | ~45 (with pad vias) | 0.8 | 40 + 36 = 76°C ✓ |
| TB6612FNG | ~80 | 0.7 | 40 + 56 = 96°C ✓ |
| SS54 | ~65 | 1.5 | 40 + 98 = 138°C ✓ (Tj max 150°C) |

> [!warning]
> The 12V buck converter (MP1584EN #1) at sustained 2A+ load may exceed thermal limits. Mitigations:
> 1. Use large copper pour (≥400mm²) around the IC and inductor
> 2. Add thermal vias (6+ vias, 0.3mm) under the exposed pad to inner GND plane
> 3. Derate: limit sustained 12V load to 2A (duty-cycle solenoids, don't run all actuators simultaneously)
> 4. Consider upgrading to MP2315 (higher efficiency at 12V output) if thermal budget is tight

---

## Driver PCB BOM

| Ref | Part | Package | Qty | Unit Cost (USD) | Notes |
|-----|------|---------|-----|----------------|-------|
| **Power Conversion** | | | | | |
| U1-U2 | MP1584EN | SOT-23-8 | 2 | $0.80 | 24V→12V, 24V→6.5V |
| U9 | TPS54531DDAR | SOIC-8 | 1 | $1.50 | 12V UPS→5V, 5A buck |
| L1 | 33µH inductor | CDRH104R (10x10mm) | 1 | $0.50 | 12V rail, Isat > 4A |
| L2 | 22µH inductor | CDRH104R (10x10mm) | 1 | $0.50 | 6.5V rail |
| L4 | 10µH inductor | CDRH127 (12.7x12.7mm) | 1 | $0.60 | 5V rail (TPS54531), Isat > 6A |
| D_BST1-2 | SS34 | SMA | 2 | $0.15 | Bootstrap Schottky diodes (MP1584EN) |
| **H-Bridge ICs** | | | | | |
| U4-U5 | DRV8876RGTR | WSON-8 (3x3mm) | 2 | $2.50 | CID linear actuator drivers |
| U6 | TB6612FNG | SSOP-24 | 1 | $1.50 | SLD dual peristaltic pump driver |
| **Discrete MOSFETs** | | | | | |
| Q1-Q11 | IRLML6344 | SOT-23 | 11 | $0.20 | SLD sol 1-2, fan 1-2, P-ASD sol V1-V6, P-ASD pump |
| Q12 | 2N7002 | SOT-23 | 1 | $0.05 | Buzzer |
| **I2C GPIO Expander** | | | | | |
| U8 | PCF8574 | SOIC-16 | 1 | $0.50 | P-ASD solenoid V1-V6 driver (I2C addr 0x20) |
| **Current Monitor** | | | | | |
| U7 | INA219BIDR | SOT-23-8 | 1 | $1.50 | 24V input current/power |
| R_SHUNT | 10 mΩ 1% 1W | 2512 | 1 | $0.30 | Current sense shunt |
| **Protection** | | | | | |
| F1 | 5A polyfuse | 1812 | 1 | $0.40 | 24V input overcurrent |
| F2-F3 | 1.5A/3A polyfuse | 0805/1206 | 2 | $0.25 | 12V and 6.5V per-rail protection |
| F5 | 3A polyfuse | 1812 | 1 | $0.30 | 12V UPS input overcurrent |
| D1 | SS54 | SMA | 1 | $0.20 | 24V input reverse polarity |
| D2 | SMBJ24A | SMB | 1 | $0.25 | 24V input TVS |
| D3 | SMBJ12A | SMB | 1 | $0.20 | 12V rail TVS |
| D4 | SMBJ6.5A | SMB | 1 | $0.20 | 6.5V rail TVS |
| D_UPS1 | SS34 | SMA | 1 | $0.15 | 12V UPS reverse polarity |
| D_UPS2 | SMBJ12A | SMB | 1 | $0.20 | 12V UPS input TVS |
| **Power Fail Detection** | | | | | |
| R_DIV1 | 100kΩ | 0402 | 1 | $0.01 | Voltage divider top (24V rail) |
| R_DIV2 | 10kΩ | 0402 | 1 | $0.01 | Voltage divider bottom |
| C_DIV | 100nF | 0402 | 1 | $0.01 | Divider filter cap |
| **Flyback Diodes** | | | | | |
| D6-D16 | SS14 | SMA | 11 | $0.10 | SLD sol 1-2, fan 1-2, P-ASD sol V1-V6, P-ASD pump |
| **Passive Components** | | | | | |
| R_GATE (x16) | 100Ω | 0402 | 16 | $0.01 | Gate/input series resistors (11 MOSFETs + 1 buzzer + 4 H-bridge inputs) |
| R_PD (x16) | 10kΩ | 0402 | 16 | $0.01 | Gate/enable pull-downs |
| R_FB (x6) | Various (10k-140k) | 0402 | 6 | $0.01 | Buck converter feedback dividers |
| R_SENSE (x2) | 1kΩ | 0402 | 2 | $0.01 | DRV8876 IPROPI sense |
| R_SIG (x1) | 33Ω | 0402 | 1 | $0.01 | Servo signal series termination (1 main DS3225) |
| C_IN (x3) | 10µF ceramic | 0805 (25V) | 3 | $0.15 | Buck input bypass |
| C_OUT (x6) | 22µF ceramic | 0805 (25V/16V/10V) | 6 | $0.12 | Buck output filter (2 per rail) |
| C_BULK1 | 470µF electrolytic | 10x10mm (10V) | 1 | $0.30 | DS3225 servo bulk |
| C_BULK3 | 100µF electrolytic | 8x8mm (25V) | 1 | $0.20 | 12V rail bulk |
| C_DEC (x10) | 100nF ceramic | 0402 | 10 | $0.01 | IC decoupling |
| C_IC (x3) | 10µF ceramic | 0805 | 3 | $0.10 | DRV8876/TB6612 VM bypass |
| **Connectors** | | | | | |
| J_STACK | 2x20 pin socket | 2.54mm, 11mm stacking | 1 | $0.80 | Stacking to Controller PCB |
| J_24V_IN | XT30 or JST-VH 2-pin | 2.5mm pitch | 1 | $0.40 | 24V DC input |
| J_12V_UPS | XT30 2-pin | 2.5mm pitch | 1 | $0.40 | 12V UPS-backed DC input |
| J_SERVO_MAIN | Pin header 3-pin | 2.54mm | 1 | $0.05 | DS3225 servo |
| J_SLD | JST-XH 12-pin | 2.5mm pitch | 1 | $0.40 | SLD combined (2× pumps + 2× solenoids + HX711 pot load cell) |
| J_PASD | JST-XH 16-pin | 2.5mm pitch | 1 | $0.60 | P-ASD combined (6× solenoids + 1× pump + 2× GND) |
| J_FAN1-2 | JST-XH 2-pin | 2.5mm pitch | 2 | $0.10 | Exhaust fans |
| J_LACT1-2 | JST-XH 2-pin | 2.5mm pitch | 2 | $0.10 | Linear actuators |
| J_BUZZER | JST-PH 2-pin | 2.0mm pitch | 1 | $0.08 | Piezo buzzer |
| BZ1 | MLT-5030 or generic | 12mm piezo | 1 | $0.80 | Active piezo buzzer 5V |
| **PCB** | 4-layer, 160x90mm | FR4 ENIG, 2oz outer Cu | 1 | $5.00 | JLCPCB batch (5 pcs) |

### Cost Summary

| Category | Prototype (1x) | Volume (100x) |
|----------|---------------|---------------|
| Power Conversion ICs + Passives | $9.50 | $6.00 |
| H-Bridge ICs (DRV8876 + TB6612) | $6.50 | $4.50 |
| Discrete MOSFETs + Diodes | $3.35 | $2.00 |
| Current Monitor (INA219 + shunt) | $1.80 | $1.20 |
| Protection + Power Fail Detection | $2.20 | $1.30 |
| Passive Components | $2.20 | $1.10 |
| Connectors | $3.30 | $2.00 |
| PCB | $5.00 | $2.00 |
| **Total** | **~$34** | **~$20** |

---

## Manufacturing Specifications

| Parameter | Value |
|-----------|-------|
| Layers | 4 |
| Board thickness | 1.6mm |
| Copper weight (outer) | 2 oz (70µm) — required for power traces |
| Copper weight (inner) | 1 oz (35µm) |
| Min trace width | 0.2mm (8 mil) signal, 1.0mm (40 mil) power |
| Min trace spacing | 0.2mm (8 mil) |
| Min via drill | 0.3mm |
| Via pad diameter | 0.6mm |
| Surface finish | ENIG (lead-free) |
| Solder mask | Green (both sides) |
| Silkscreen | White (both sides) |
| Board material | FR4, Tg ≥ 150°C |
| Panelization | 1x1 (board too large for paneling at JLCPCB standard) |

### Assembly Notes

- All ICs and passives are SMT (top side preferred)
- Through-hole: 2.54mm pin headers for servo connectors, XT30 for power input
- Stacking connector (2x20 socket) on bottom side of board
- Reflow for SMT, then wave or hand-solder through-hole components
- Mark pin 1 of J_STACK with silkscreen triangle on both top and bottom layers

---

## Design Verification Checklist

### Pre-Fabrication

- [ ] Schematic ERC passes with zero errors
- [ ] All buck converter feedback resistor values verified against MP1584EN datasheet formula
- [ ] Inductor saturation current ratings exceed maximum load current per rail
- [ ] DRV8876 IPROPI sense resistor value correct (1kΩ → 1.5V/A output)
- [ ] TB6612FNG VM decoupling adequate (100nF + 10µF within 5mm)
- [ ] All MOSFET gate pull-downs present (safe default state)
- [ ] INA219 I2C address (0x40) does not conflict with other I2C devices
- [ ] Stacking connector pinout matches Controller PCB J_STACK mirror layout
- [ ] 24V input protection chain in correct order: Polyfuse → Schottky → TVS
- [ ] No pin conflicts between new assignments (PA6/7/9/10, PB4/5, PC2-PC7, PD2) and existing Controller PCB pins

### PCB Layout

- [ ] DRC passes with zero errors
- [ ] GND plane continuous under all switching converters (no splits)
- [ ] Buck converter input/output cap loops minimized (<10mm total loop length)
- [ ] Power traces sized for current: ≥2mm for 24V input, ≥1mm for 12V/6.5V/5V rails
- [ ] Thermal vias under DRV8876 exposed pads (minimum 6 vias, 0.3mm drill each)
- [ ] Thermal copper pour around MP1584EN ICs and inductors (≥400mm² each)
- [ ] Creepage ≥2mm between 24V traces and logic-level signals
- [ ] All connectors accessible from board edges
- [ ] Mounting holes at same positions as Controller PCB and CM5IO (M3, 4 corners)
- [ ] Stacking connector centered on board long edge, bottom layer

### Post-Assembly

- [ ] 24V input draws <10mA with no actuators connected (quiescent)
- [ ] 12V rail measures 12.0V ±3% under 500mA dummy load
- [ ] 6.5V rail measures 6.5V ±3% under 500mA dummy load
- [ ] 5V rail measures 5.0V ±3% under 500mA dummy load
- [ ] INA219 responds at I2C address 0x40 (I2C scan from STM32)
- [ ] Each servo connector outputs correct PWM voltage on oscilloscope
- [ ] Solenoid MOSFETs switch correctly (GPIO high = solenoid energized)
- [ ] DRV8876 drives linear actuator in both directions (PH toggle test)
- [ ] TB6612FNG drives pump motor with variable speed (PWMA/PWMB sweep)
- [ ] All actuators OFF when STM32 is held in reset (pull-down verification)
- [ ] Input polyfuse trips at >5A sustained load (controlled test)
- [ ] No smoke test: apply 24V, observe current draw and check for shorts

---

## Related Documentation

- [[Controller-PCB-Design]] — STM32G474RE controller board with sensor interfaces
- [[../02-Hardware/Epicura-Architecture|Epicura Architecture]] — System-level wiring and block diagrams
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]] — Induction, sensors, power specs
- [[../05-Subsystems/09-Induction-Heating|Induction Heating]] — Microwave surface module (CAN bus, separate from Driver PCB)
- [[../05-Subsystems/10-Robotic-Arm|Robotic Arm]] — DS3225 servo arm patterns and control
- [[../05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing]] — ASD/CID/SLD dispensing subsystems
- [[../05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]] — Exhaust fan control
- [[../08-Components/02-Actuation-Components|Actuation Components]] — Servo and actuator BOM
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]] — Full system cost analysis

---

#epicura #pcb #driver #power-electronics #actuators #hardware-design

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-16 | Manas Pradhan | Replaced ASD (3× SG90 servo + 3× vibration motor) with P-ASD (6× solenoid valve + 1× diaphragm pump); updated 12V rail load, J_STACK pinout, connector definitions, BOM, and thermal analysis |
| 3.0 | 2026-02-16 | Manas Pradhan | Added PCF8574 I2C GPIO expander (addr 0x20) for P-ASD solenoid control; solenoid MOSFET gates now driven by PCF8574 P0-P5 instead of direct STM32 GPIO; freed 6 STM32 pins; J_STACK pins 16-20, 39 now Reserved |
| 4.0 | 2026-02-20 | Manas Pradhan | Added 12V UPS-backed DC input (J_12V_UPS) with TPS54531 12V→5V 5A buck converter replacing MP1584EN #3; added 24V power failure detection via voltage divider + COMP2 on PA1; J_STACK pin 16 now PWR_FAIL; added POWER_FAIL SPI message (0x14) and power failure state machine; updated BOM, thermal analysis, and block diagram |
| 5.0 | 2026-02-20 | Manas Pradhan | Moved pot load cell (HX711) from Controller PCB J_LC to Driver PCB J_SLD; J_STACK pins 17-18 now HX711_SCK/HX711_DOUT; J_SLD expanded from 8-pin to 12-pin (added HX711 SCK, DOUT, 3.3V, GND) |
