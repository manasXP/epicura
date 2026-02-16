---
tags: [epicura, mcu, stm32, functional-spec, firmware]
created: 2026-02-16
aliases: [STM32 Spec, MCU Spec]
---

# MCU Functional Specification — STM32G474RE

> **Document ID:** EPIC-SW-MCU-001
> **Processor:** STM32G474RE, Cortex-M4F @ 170 MHz
> **Flash / SRAM:** 512 KB / 128 KB
> **Package:** LQFP-64
> **Related:** [[04-MPU-Functional-Specification]], [[02-Controller-Software-Architecture]], [[01-Controller-PCB-Design]]

---

## 1 Overview

The STM32G474RE is the real-time motor/sensor controller and safety guardian for Epicura. It runs FreeRTOS with four primary tasks: PID temperature control (10 Hz), servo motor drive (50 Hz), sensor polling (10 Hz), and CM5 communications (20 Hz). It owns all safety-critical paths including the heater relay, E-stop handling, and watchdog supervision.

### 1.1 Hardware Summary

| Parameter | Value |
|-----------|-------|
| Core | Cortex-M4F @ 170 MHz, single-precision FPU |
| Flash | 512 KB |
| SRAM | 128 KB |
| ADC | 5× 12-bit (up to 4 Msps) |
| Timers | Advanced (TIM1), GP (TIM2/3/4), basic |
| Comm | 3× UART, 3× SPI, 4× I2C, FDCAN |
| Package | LQFP-64 |
| Power | 3.3 V via AMS1117-3.3 LDO (from 5 V), ~0.5 W typical |

---

## 2 Functional Requirements

### 2.1 PID Temperature Control

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MCU-001 | Closed-loop PID at 10 Hz (100 ms period) | Must | Steady-state error ≤ ±5 °C |
| FR-MCU-002 | Default PID gains: Kp=2.0, Ki=0.5, Kd=0.1 | Must | Tunable at runtime via SPI command |
| FR-MCU-003 | Overshoot protection: clamp at setpoint + 10 °C | Must | Integral windup reset when exceeded |
| FR-MCU-004 | Temperature ramp control (°C/min configurable) | Should | Linear ramp from current to target |
| FR-MCU-005 | Read IR thermometer (MLX90614) for food surface temp | Must | I2C @ 100 kHz, accuracy ±0.5 °C |
| FR-MCU-006 | Read NTC thermistors for coil and ambient temp | Must | ADC channels PA4/PA5, Steinhart-Hart conversion |
| FR-MCU-007 | Send power commands to induction module via CAN | Must | FDCAN1 @ 500 kbps, power level 0–1800 W |

### 2.2 Power Level Profiles

| Profile | Power (W) | Temp Range (°C) | Duty Cycle | CAN Command Value |
|---------|-----------|-----------------|------------|-------------------|
| Sear | 1,800 | 200–250 | 100% | 0xFF |
| Boil | 1,500 | 100 | 85% | 0xD9 |
| Simmer | 400–600 | 80–95 | 25–35% | 0x40–0x60 |
| Warm | 200 | 60–70 | 10–15% | 0x1A |
| Off | 0 | Ambient | 0% | 0x00 |

### 2.3 Servo Motor Control

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MCU-010 | Drive main servo (DS3225) at 50 Hz PWM via TIM1_CH1 (PA8) | Must | 500–2500 µs pulse width range |
| FR-MCU-011 | Support stir patterns: circular, figure-8, scrape, fold | Must | Pattern selected by CM5 command (0x02) |
| FR-MCU-012 | Stall detection via current monitoring | Should | Alert CM5 if servo draws >2 A for >500 ms |
| FR-MCU-013 | Drive P-ASD: pump PWM via TIM2_CH1 (PA0), 6× solenoid GPIO (PA1, PA2, PC7, PD2, PA3, PB11) | Must | Pump: 25 kHz PWM speed control; Solenoids: digital on/off via MOSFET |
| FR-MCU-014 | Motor control task at 50 Hz (20 ms period) | Must | Highest priority FreeRTOS task |

### 2.4 Sensor Polling

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MCU-020 | Read pot load cells (4× strain gauge + HX711) at 10 Hz | Must | Resolution ~1 g, total capacity 20 kg |
| FR-MCU-021 | Read SLD reservoir load cell at 10 Hz during dispensing | Must | Accuracy ±5% for closed-loop liquid dispensing |
| FR-MCU-022 | Read IR thermometer at 10 Hz | Must | MLX90614 via I2C1 (PB6/PB7) |
| FR-MCU-023 | Read NTC thermistors at 10 Hz | Must | ADC2_IN17 (PA4) coil, ADC2_IN13 (PA5) ambient |
| FR-MCU-024 | Read INA219 bus current monitor | Should | I2C1 @ address 0x40, 24 V rail monitoring |
| FR-MCU-025 | Sensor polling task at 10 Hz (100 ms period) | Must | All sensor data available within each cycle |

### 2.5 Ingredient Dispensing

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MCU-030 | P-ASD: Pressurize accumulator, open solenoid valve, puff-dose spice, monitor pot weight | Must | Accuracy ±10%, clog retry (3 attempts), post-dispense purge |
| FR-MCU-031 | CID: Drive linear actuators via DRV8876 (PH/EN) | Must | Home + full-extend limit switch detection |
| FR-MCU-032 | SLD: Drive peristaltic pumps + solenoids, closed-loop weight | Must | Accuracy ±5%, stop at target×0.95 |
| FR-MCU-033 | Tare load cells on command (0x37) | Must | Zero offset stored in SRAM |
| FR-MCU-034 | Report weight on query (0x35) | Must | Response within 100 ms |

#### 2.5.1 P-ASD Dispensing & Clog Recovery Sequence

**Normal dispense:**
1. Pre-purge: 100 ms pulse at 0.3 bar (loosen packed powder)
2. Main dispense: open solenoid for calibrated duration (100–400 ms)
3. Monitor pot weight at 10 Hz; additional 50 ms pulses if under target
4. Close at 90% target (in-flight compensation)
5. Post-dispense purge: 200 ms at 1.2 bar (clear orifice)

**Clog recovery (no weight change after main pulse):**
1. **Retry 1:** Increase pressure to 1.2 bar, repeat pulse
2. **Retry 2:** Rapid 50 ms on/off oscillating pulses (5 cycles)
3. **Failure:** Send CLOG ERROR (0x12) to CM5

#### 2.5.2 SLD Closed-Loop Dispensing

1. Tare reservoir load cell
2. Open solenoid + start pump
3. Monitor weight loss @ 10 Hz
4. Stop pump when `weight_dispensed ≥ target × 0.95`
5. Close solenoid, report final weight to CM5

### 2.6 CM5 Communication

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MCU-040 | SPI slave on SPI2 (PB12–PB15) | Must | Up to 10 MHz clock |
| FR-MCU-041 | Assert IRQ (PB3, active-low, 10 µs pulse) when data ready | Must | CM5 polls on IRQ |
| FR-MCU-042 | Validate CRC-16/CCITT on all received messages | Must | NAK on CRC mismatch |
| FR-MCU-043 | Send telemetry at 10 Hz (0x10) | Must | temp, motor_rpm, weight, state |
| FR-MCU-044 | Send status on safety state change (0x12) | Must | safety_state, error_code, flags |
| FR-MCU-045 | Comms task at 20 Hz (50 ms period) | Must | Process incoming commands + queue outgoing |
| FR-MCU-046 | Monitor CM5 heartbeat (expect every 2 s) | Must | If missed for 5 s → IWDG-triggered safe state |

### 2.7 Safety

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-MCU-050 | E-stop button (PB2, EXTI interrupt) → immediate shutdown | Must | <1 ms from button press to relay open |
| FR-MCU-051 | Safety relay control (PB0 → MOSFET → relay) | Must | Cuts AC mains to induction module |
| FR-MCU-052 | Thermal cutoff: IR >270 °C or NTC >280 °C → E_STOP | Must | Checked every 100 ms (sensor poll cycle) |
| FR-MCU-053 | Hardware watchdog (IWDG, 5 s timeout) | Must | Kick in main loop; timeout → full reset |
| FR-MCU-054 | Pot detection via CAN (module-reported) | Must | No heat command if pot absent |
| FR-MCU-055 | Boot-safe state: all actuator outputs OFF until initialized | Must | 100 kΩ pull-downs on MOSFET gates |

---

## 3 Hardware Interfaces

### 3.1 Pin Assignment (LQFP-64)

| Pin | Function | Peripheral | Target |
|-----|----------|------------|--------|
| **PA0** | TIM2_CH1 | PWM 25 kHz | P-ASD diaphragm pump (via IRLML6344) |
| **PA1** | GPIO output | Digital | P-ASD solenoid V1 (via IRLML6344) |
| **PA2** | GPIO output | Digital | P-ASD solenoid V2 (via IRLML6344) |
| **PA3** | GPIO output | Digital | P-ASD solenoid V5 (via IRLML6344) |
| **PA4** | ADC2_IN17 | Analog in | NTC thermistor — coil temp |
| **PA5** | ADC2_IN13 | Analog in | NTC thermistor — ambient temp |
| **PA6** | TIM3_CH1 | PWM 25 kHz | Exhaust fan 1 |
| **PA7** | GPIO output | Digital | Solenoid 1 enable (SLD, via IRLML6344) |
| **PA8** | TIM1_CH1 | PWM 50 Hz | Main servo DS3225 |
| **PA9** | GPIO output | Digital | Solenoid 2 enable (SLD, via IRLML6344) |
| **PA10** | GPIO output | Digital | CID linear actuator 1 EN (DRV8876) |
| **PA11** | TIM1_CH4 | PWM | Piezo buzzer |
| **PA13** | SWDIO | Debug | SWD programming |
| **PA14** | SWCLK | Debug | SWD programming |
| **PB0** | GPIO output | Digital | Safety relay (via N-MOSFET) |
| **PB1** | GPIO input | Digital | Pot detection (from CAN module status, optional hardwire) |
| **PB2** | EXTI | Interrupt | E-stop button (NC, active-low) |
| **PB3** | GPIO output | Digital | IRQ to CM5 (active-low, 10 µs pulse) |
| **PB4** | GPIO output | Digital | CID linear actuator 1 PH (DRV8876) |
| **PB5** | GPIO output | Digital | CID linear actuator 2 EN (DRV8876) |
| **PB6** | I2C1_SCL | I2C @ 100 kHz | MLX90614 + INA219 (shared bus) |
| **PB7** | I2C1_SDA | I2C @ 100 kHz | MLX90614 + INA219 (shared bus) |
| **PB8** | FDCAN1_RX | CAN | Induction module RX (via SN65HVD230) |
| **PB9** | FDCAN1_TX | CAN | Induction module TX (via SN65HVD230) |
| **PB10** | GPIO output | Software PWM 25 kHz | Exhaust fan 2 |
| **PB12** | SPI2_NSS | SPI slave | CM5 chip select |
| **PB13** | SPI2_SCK | SPI slave | CM5 clock |
| **PB14** | SPI2_MISO | SPI slave | STM32 → CM5 data |
| **PB15** | SPI2_MOSI | SPI slave | CM5 → STM32 data |
| **PC0** | GPIO output | Digital | HX711 SCK (pot load cells) |
| **PC1** | GPIO input | Digital | HX711 DOUT (pot load cells) |
| **PC2** | GPIO output | Digital | CID linear actuator 2 PH (DRV8876) |
| **PC3** | GPIO output | PWM (software) | SLD pump 1 PWM (TB6612) |
| **PC4** | GPIO output | Digital | SLD pump 1 DIR (TB6612) |
| **PC5** | GPIO output | PWM (software) | SLD pump 2 PWM (TB6612) |
| **PC6** | GPIO output | Digital | SLD pump 2 DIR (TB6612) |
| **PC7** | GPIO output | Digital | P-ASD solenoid V3 (via IRLML6344) |
| **PD2** | GPIO output | Digital | P-ASD solenoid V4 (via IRLML6344) |
| **PB11** | GPIO output | Digital | P-ASD solenoid V6 (via IRLML6344) |

### 3.2 I2C1 Bus (PB6/PB7)

| Address | Device | Data |
|---------|--------|------|
| 0x5A | MLX90614 | Object + ambient temperature |
| 0x40 | INA219 | 24 V rail voltage + current |
| 0x48 | ADS1015 | P-ASD accumulator pressure (via MPXV5100GP) |

### 3.3 CAN Bus (FDCAN1)

- Transceiver: SN65HVD230 (3.3 V)
- Bit rate: 500 kbps (CAN 2.0B)
- Bus: 2-wire (CANH/CANL) to induction module
- Termination: 120 Ω at each end
- Messages: power set, power query, status request, fault report

### 3.4 Load Cells (HX711)

- Interface: Bit-banged GPIO (PC0 = SCK, PC1 = DOUT)
- Sample rate: 10 Hz (RATE pin low) or 80 Hz (RATE pin high)
- Configuration: 4× 5 kg strain gauges in Wheatstone bridge (pot)
- SLD reservoir: Separate HX711 on SLD I2C load cell (shared I2C1)
- Resolution: 24-bit ADC → ~1 g at 20 kg full scale

---

## 4 Software Architecture

### 4.1 RTOS Configuration

- **RTOS:** FreeRTOS 10.x
- **Language:** C (MISRA C subset for safety-critical paths)
- **DSP:** CMSIS-DSP library for PID computation
- **Heap:** heap_4 (coalescing), ~64 KB allocated
- **Tick rate:** 1 kHz (1 ms)

### 4.2 Task Table

| Task | Rate | Period | Priority | Stack | Description |
|------|------|--------|----------|-------|-------------|
| Motor Control | 50 Hz | 20 ms | Highest (4) | 512 B | Servo PWM updates, stir patterns |
| Safety Monitor | 10 Hz | 100 ms | Highest (4) | 256 B | Thermal limits, E-stop, watchdog kick |
| PID Control | 10 Hz | 100 ms | High (3) | 512 B | Read IR/NTC, compute PID, send CAN |
| Sensor Poll | 10 Hz | 100 ms | Medium (2) | 512 B | Load cells, INA219, aggregate telemetry |
| CM5 Comms | 20 Hz | 50 ms | Medium (2) | 1024 B | SPI slave handler, command parser, telemetry TX |

### 4.3 Safety State Machine

```
NORMAL ──[warning condition]──→ WARNING
WARNING ──[critical condition]──→ CRITICAL
CRITICAL ──[any safety violation]──→ E_STOP
E_STOP ──[manual reset]──→ NORMAL
WARNING ──[condition cleared]──→ NORMAL
CRITICAL ──[condition cleared within timeout]──→ WARNING
```

**State Transitions:**

| From | To | Trigger |
|------|----|---------|
| NORMAL | WARNING | NTC > 250 °C, or load cell drift > 50 g/min unexpected |
| WARNING | CRITICAL | IR > 260 °C, or CAN fault from induction module |
| CRITICAL | E_STOP | IR > 270 °C, NTC > 280 °C, E-stop button, CM5 heartbeat timeout (5 s) |
| E_STOP | NORMAL | Manual hardware reset (E-stop button released + PB2 debounce) |

### 4.4 Boot Sequence

1. **Reset** → SystemInit (clock to 170 MHz HSE + PLL)
2. **HAL_Init** → SysTick, NVIC priorities
3. **Peripheral init** → GPIO (all outputs LOW/safe), ADC, TIM, SPI, I2C, FDCAN
4. **Safety check** → Verify E-stop not pressed, relay OFF, self-test sensors
5. **FreeRTOS start** → Create tasks, start scheduler
6. **Wait for CM5 heartbeat** → First heartbeat received → safety state NORMAL
7. **IDLE mode** → Sensors polling at 1 Hz, heartbeat monitoring, awaiting commands

---

## 5 Communication Protocols

### 5.1 SPI Slave Protocol (STM32 ↔ CM5)

See [[04-MPU-Functional-Specification#5.1 SPI Protocol]] for full frame definition.

- STM32 operates as SPI2 slave (PB12–PB15)
- NSS (PB12) driven by CM5 GPIO8
- On valid command: parse, execute, queue ACK/response
- On CRC mismatch: NAK (0xFF) response
- IRQ (PB3) asserted 10 µs when outgoing data queued

### 5.2 CAN Bus Protocol (STM32 ↔ Induction Module)

| CAN ID | Direction | DLC | Description |
|--------|-----------|-----|-------------|
| 0x100 | STM32 → Module | 2 | Set power level (0x00–0xFF) |
| 0x101 | STM32 → Module | 1 | Status request |
| 0x200 | Module → STM32 | 4 | Status response (temp, power, fault flags) |
| 0x201 | Module → STM32 | 2 | Fault report (fault code, severity) |

- Timeout: If no module response within 500 ms → CAN_FAULT, reduce to safe power
- Pot detection: Module reports pot-absent in status → STM32 blocks all SET_TEMP commands

### 5.3 I2C Protocol

- Bus speed: 100 kHz (standard mode)
- Pull-ups: 4.7 kΩ to 3.3 V (on Controller PCB)
- MLX90614 (0x5A): Read object temp register 0x07, ambient temp register 0x06
- INA219 (0x40): Read bus voltage register 0x02, current register 0x04

---

## 6 Power Management

### 6.1 Power Supply

- Input: 5 V from CM5IO 40-pin (or direct from Driver PCB 5 V rail)
- LDO: AMS1117-3.3 (SOT-223), 5 V → 3.3 V @ 800 mA max
- Decoupling: 10 µF input, 10 µF output, 100 nF per VDD pin
- Typical consumption: ~0.5 W (170 MHz, all peripherals active)

### 6.2 Power States

| State | Description | Current (3.3 V) |
|-------|-------------|-----------------|
| Active | All tasks running, PID + CAN + SPI active | ~150 mA |
| Idle | Sensors at 1 Hz, awaiting commands | ~80 mA |
| E_STOP | Relay open, buzzer on, minimal processing | ~100 mA |
| Reset | After IWDG timeout, re-initializing | ~50 mA |

---

## 7 Safety & Fault Handling

### 7.1 Safety Mechanisms

| Mechanism | Implementation | Response Time |
|-----------|---------------|---------------|
| E-stop button | PB2 EXTI interrupt (highest NVIC priority) | <1 ms |
| Safety relay | PB0 → N-MOSFET → relay coil (NC relay, fail-safe open) | <5 ms |
| Hardware watchdog (IWDG) | 5 s timeout, kicked in safety monitor task | 5 s (worst case) |
| Thermal cutoff (IR) | MLX90614 > 270 °C → E_STOP | ≤100 ms (poll interval) |
| Thermal cutoff (NTC) | NTC > 280 °C → E_STOP | ≤100 ms (poll interval) |
| CAN fault | No module response in 500 ms → reduce power | 500 ms |
| CM5 heartbeat loss | No heartbeat for 5 s → safe state | 5 s |
| Overcurrent | INA219 > threshold → warning/shutdown | ≤100 ms |

### 7.2 Fault Table

| Fault Code | Name | Severity | Action |
|------------|------|----------|--------|
| 0x01 | OVER_TEMP_IR | Critical | E_STOP, cut relay, log |
| 0x02 | OVER_TEMP_NTC | Critical | E_STOP, cut relay, log |
| 0x03 | E_STOP_PRESSED | Critical | E_STOP, cut relay, buzzer |
| 0x04 | CAN_FAULT | Critical | Reduce power to 0, alert CM5 |
| 0x05 | CM5_HEARTBEAT_LOSS | Critical | Safe state (hold temp at 0, stop servo) |
| 0x10 | SERVO_STALL | Warning | Stop servo, alert CM5 |
| 0x11 | LOAD_CELL_DRIFT | Warning | Alert CM5, flag dispense unreliable |
| 0x12 | PASD_CLOG | Warning | Pneumatic retry sequence (pressure increase + oscillating pulses), then alert CM5 |
| 0x13 | SLD_DISPENSE_ERROR | Warning | Stop pump, alert CM5 with actual vs target |
| 0x20 | CAN_TX_TIMEOUT | Info | Retry 3×, then CAN_FAULT |
| 0x21 | I2C_NACK | Info | Retry 3×, use last-known value |

### 7.3 E-Stop Sequence

1. **PB2 EXTI fires** (or software E_STOP from CM5 command 0x04)
2. Safety relay opened (PB0 LOW → relay de-energizes → AC cut)
3. All PWM outputs set to 0% (TIM1, TIM2, TIM3)
4. CAN: send power=0 to module (belt-and-suspenders with relay)
5. Buzzer activated (PA11 PWM)
6. Status packet (0x12) sent to CM5: `safety_state = E_STOP`
7. **Hold state** — only IWDG kick continues; no commands accepted
8. **Reset** — PB2 debounce clears → re-init → wait for CM5 heartbeat → NORMAL

---

## 8 Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| PID loop period | 100 ms ± 1 ms | TIM interrupt jitter |
| Motor control period | 20 ms ± 0.5 ms | TIM interrupt jitter |
| E-stop latency | <1 ms | PB2 edge → relay GPIO toggle |
| SPI command parse | <1 ms | NSS assert → response queued |
| CAN round-trip | <10 ms | TX → RX status |
| Sensor poll cycle | <50 ms (all sensors) | Cycle start → data ready |
| Temperature accuracy | ±5 °C (IR to food surface) | Calibrated against thermocouple |
| Dispensing accuracy (ASD) | ±10% | Load cell vs target weight |
| Dispensing accuracy (SLD) | ±5% | Load cell vs target weight |
| FreeRTOS CPU utilization | <70% | Idle task runtime measurement |
| Flash usage | <256 KB | Linker map |
| SRAM usage | <96 KB | Stack + heap analysis |

---

## 9 Dependencies & Constraints

### 9.1 Hardware Dependencies

- Controller PCB (160×90 mm) provides STM32 + LDO + connectors
- Driver PCB (160×90 mm) provides buck converters, H-bridges, MOSFETs
- Stacking connector (J_STACK, 2×20) bridges Controller ↔ Driver
- CM5IO provides SPI connection to CM5

### 9.2 Firmware Dependencies

- STM32 HAL drivers (STM32CubeMX generated): GPIO, ADC, TIM, SPI, I2C, FDCAN
- FreeRTOS 10.x kernel + CMSIS-RTOS2 wrapper
- CMSIS-DSP library (PID functions)
- Custom HX711 bit-bang driver
- CRC-16/CCITT lookup table

### 9.3 Constraints

- MISRA C compliance for safety-critical tasks (PID, safety monitor, E-stop handler)
- No dynamic memory allocation after boot (all FreeRTOS objects static)
- No floating-point in ISRs (FPU context save overhead)
- CAN bus requires 120 Ω termination at both ends
- I2C bus: max 2 devices (MLX90614 + INA219) to stay within 400 pF bus capacitance

### 9.4 Cross-References

| Topic | Document |
|-------|----------|
| CM5 MPU spec | [[04-MPU-Functional-Specification]] |
| State machine details | [[03-Main-Loop-State-Machine]] |
| Software architecture | [[02-Controller-Software-Architecture]] |
| Controller PCB design | [[01-Controller-PCB-Design]] |
| Driver PCB design | [[02-Driver-PCB-Design]] |
| Dispensing subsystems | [[03-Ingredient-Dispensing]] |
| Hardware architecture | [[01-Epicura-Architecture]] |
| Technical specifications | [[02-Technical-Specifications]] |
