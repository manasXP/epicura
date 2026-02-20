---
tags: [epicura, testing, firmware, stm32]
created: 2026-02-16
aliases: [Firmware Test Strategy]
---

# Firmware Test Strategy — epicura-firmware

## Scope

Testing strategy for the STM32G474RE real-time control firmware: PID controller, servo driver, sensor polling, CAN bus interface, dispensers (P-ASD, CID, SLD), safety manager, and SPI protocol handler.

---

## Test Levels

### 1. Unit Tests (Host-Based)

**Framework:** Unity + CMock (or CeedlingTest)
**Runs on:** x86 host (CI-compatible, no hardware required)

| Module | Key Test Cases |
|--------|---------------|
| `pid_controller` | Proportional response, integral windup / anti-windup, derivative kick suppression, output clamping (0–100%), setpoint step response convergence |
| `calibration` | Load cell ADC-to-grams conversion, zero-offset calibration, out-of-range input handling |
| `spi_protocol` | Frame packing/unpacking, CRC16 calculation and verification, invalid frame rejection, buffer overflow protection |
| `can_interface` | CAN frame construction for power set commands, status response parsing, fault code decoding |
| `dispenser_asd` | Solenoid valve sequencing for puff-dosing, pressure threshold logic, cartridge selection |
| `dispenser_cid` | Linear actuator travel limits, push-plate sequencing |
| `dispenser_sld` | Peristaltic pump flow rate calculation, load-cell closed-loop dispensing, level alert thresholds |
| `safety_manager` | Over-temperature cutoff logic, watchdog feed timing, e-stop relay state transitions, interlock validation |
| `sensor_manager` | MLX90614 I2C read parsing, HX711 SPI read parsing, CAN coil temp parsing, sensor timeout detection |

**Approach:**
- Abstract HAL behind interfaces (`hal_gpio.h`, `hal_adc.h`, etc.) so unit tests can inject mock HAL implementations
- Use CMock to auto-generate mocks from HAL headers
- All safety-critical paths (thermal cutoff, e-stop, watchdog) must have 100% branch coverage

### 2. Integration Tests (Hardware-in-Loop — HIL)

**Runs on:** STM32G474RE dev board + test jig

| Test Area | Setup | Verification |
|-----------|-------|-------------|
| PID + MLX90614 | IR sensor aimed at heated target | PID converges to setpoint ±2°C within 60s |
| Servo driver | 24V BLDC motor on fixture | Spin through full speed range, verify velocity and direction via back-EMF feedback |
| CAN bus | CAN analyzer (e.g., PCAN-USB) | Send power command, verify response frame within 10ms |
| SPI protocol | CM5 SPI master (loopback or CM5 dev board) | Bidirectional message exchange, CRC verified |
| Load cells (SLD) | Calibrated test weights | 4× load cell readings within ±2g of known weight |
| P-ASD pneumatic | Pressure sensor + solenoid valve rig | Puff-dose sequence delivers within ±5% target volume |
| Safety relay | Relay test jig with continuity probe | E-stop cuts AC within 50ms, watchdog timeout triggers relay |
| Full dispenser cycle | All 3 dispensers connected | Sequenced dispensing completes without fault |

**Tooling:**
- OpenOCD + GDB for debug
- Logic analyzer (Saleae) for SPI/I2C/PWM timing verification
- Custom Python test harness on host PC for automated HIL sequencing

### 3. Static Analysis

| Tool | Purpose | CI Gate |
|------|---------|---------|
| `cppcheck` | General C static analysis | Errors = fail |
| `PC-lint` or `MISRA-C checker` | MISRA C:2012 compliance for safety-critical modules | Advisory = warn, Required = fail |
| `arm-none-eabi-gcc -Wall -Werror` | Compiler warnings as errors | Any warning = fail |

### 4. Timing / Real-Time Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| PID loop jitter | Toggle GPIO at PID entry/exit, measure with oscilloscope | 100 Hz ± 1% (10ms ± 0.1ms) |
| Servo task timing | Same GPIO toggle method | 50 Hz ± 2% |
| Sensor polling | Timestamp in sensor task, log via SWD | 10 Hz ± 5% |
| Worst-case interrupt latency | Trigger external interrupt, measure response | < 10 µs |
| FreeRTOS stack usage | `uxTaskGetStackHighWaterMark()` | All tasks > 20% headroom |

---

## CI Pipeline

```yaml
# .github/workflows/ci.yml
trigger: PR to develop or main

steps:
  1. Checkout
  2. Install arm-none-eabi-gcc toolchain
  3. Run cppcheck (static analysis)
  4. Build firmware (arm-none-eabi-gcc, Makefile)
  5. Run Unity unit tests (compiled for x86 host)
  6. Report coverage (gcov/lcov)
```

**Gate criteria:** Build succeeds, zero cppcheck errors, all unit tests pass, coverage ≥ 80% for safety modules.

---

## Test Data & Fixtures

- **PID test vectors:** Step response profiles (ramp, overshoot, steady-state) as CSV, compared against expected output
- **CAN test frames:** Known-good CAN frames captured from microwave induction module datasheet
- **Calibration tables:** Load cell ADC-to-grams lookup validated against reference weights

---

## Safety-Specific Testing

Per IEC 60335-1 and ISO 13482 requirements:

| Safety Function | Test | Pass Criteria |
|----------------|------|--------------|
| Thermal cutoff | Simulate sensor reading > 300°C | Induction power = 0 within 100ms |
| Watchdog timeout | Stop feeding watchdog in test | Safety relay opens within watchdog period (500ms) |
| E-stop | Assert e-stop GPIO | AC relay opens, all actuators stop, state = FAULT |
| Servo stall detection | Block servo mechanically | Motor current limit triggers stop within 2s |
| CAN bus timeout | Disconnect CAN | Induction power = 0, fault raised within 1s |
| Power-on self-test | Boot with faulty sensor (disconnected IR) | System refuses to enter COOK state |

---

## References

- [[__Workspaces/Epicura/docs/07-Development/02-Repository-Plan|Repository Plan]]
- [[__Workspaces/Epicura/docs/03-Software/02-Controller-Software-Architecture|Controller Software Architecture]]
- [[__Workspaces/Epicura/docs/05-Subsystems/01-Induction-Heating|Induction Heating]]
- [[__Workspaces/Epicura/docs/06-Compliance/01-Safety-Compliance|Safety & Compliance]]
