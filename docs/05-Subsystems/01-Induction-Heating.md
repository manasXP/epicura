---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Induction Heating System

## Overview

The induction heating system is the primary thermal element of Epicura, delivering up to 1,800W of cooking power through electromagnetic induction. Epicura uses a **commercial microwave induction surface** — a self-contained module with its own power coil, driver electronics, and AC power stage. The module exposes a **CAN bus interface** for external control, allowing the STM32 controller to set power levels, read status, and receive fault notifications without dealing with high-power IGBT driver circuits directly.

This approach eliminates the need for custom high-voltage power electronics (IGBT half-bridge, gate drivers, resonant tank design, EMI filtering) and leverages a commercially certified, safety-tested heating module.

### Advantages of Commercial Microwave Surface

- **No custom high-voltage design:** Eliminates IGBT driver board, resonant tank tuning, and EMI filter design
- **Pre-certified safety:** Commercial module includes pot detection, over-temperature, overcurrent protection
- **CAN bus control:** Digital interface replaces analog PWM gate driving; clean separation between power and logic
- **Faster prototyping:** No need to source/test individual IGBT modules, gate drivers, or Litz wire coils
- **Reliability:** Production-tested power electronics vs. prototype IGBT board

### Advantages of Induction Over Resistive Heating

- **Speed:** Induction heats the pot directly, not the coil surface, reducing preheat time by 50-70%
- **Efficiency:** 85-90% of electrical energy reaches the food (vs. ~65% for radiant coils)
- **Precision:** Power can be modulated continuously from 0 to 1,800W via CAN commands
- **Safety:** No open flame, coil surface stays relatively cool, automatic shutoff without a pot
- **Cleanliness:** No combustion byproducts, easy wipe-down of flat glass-ceramic surface

## Heater Module

### Commercial Microwave Surface

The microwave surface is a self-contained induction heating module that includes:

- AC power inlet and internal EMI filter / rectifier
- IGBT or MOSFET driver stage with resonant coil (all internal)
- Built-in safety circuits (pot detection, thermal cutoff, overcurrent)
- Exposed CAN bus port for external control (power level, on/off, status)

The STM32 controller communicates with the module over CAN bus. All high-voltage power electronics are handled internally by the module — Epicura's controller PCB never touches mains voltage.

### System Block Diagram

```
AC Mains (220-240V 50Hz)
        │
        ▼
┌──────────────────────────────────────────────────┐
│         Microwave Induction Surface               │
│                                                    │
│  ┌────────────┐  ┌───────────┐  ┌──────────────┐ │
│  │ AC Input   │  │ Power     │  │ Induction    │ │
│  │ EMI Filter │─►│ Driver    │─►│ Coil         │─┼──► Heats Pot
│  │ Rectifier  │  │ (internal)│  │ (internal)   │ │
│  └────────────┘  └─────┬─────┘  └──────────────┘ │
│                        │                           │
│                  ┌─────▼─────┐                     │
│                  │ Onboard   │                     │
│                  │ Controller│                     │
│                  │ + Safety  │                     │
│                  └─────┬─────┘                     │
│                        │                           │
│                   CAN Bus Port                     │
└────────────────────┬───────────────────────────────┘
                     │
              CAN_H, CAN_L, GND
                     │
                     ▼
              ┌──────────────┐
              │ STM32G474RE  │
              │ FDCAN1       │
              │ (PB8/PB9)   │
              └──────────────┘
```

## CAN Bus Interface

### Physical Layer

| Parameter | Value |
|-----------|-------|
| Protocol | CAN 2.0B |
| Bit Rate | 500 kbps |
| Transceiver | Onboard in module; STM32 side uses FDCAN1 + external CAN transceiver |
| Termination | 120 ohm at each end (module + STM32 side) |
| Connector | Standard CAN connector on module (CAN_H, CAN_L, GND) |
| Wiring | Twisted pair, shielded, <1m length |

### CAN Message Protocol (Heater)

| CAN ID | Name | Direction | Payload | Description |
|--------|------|-----------|---------|-------------|
| 0x100 | HEAT_SET_POWER | STM32 → Module | Power level (0-100%), ramp rate | Set target heating power |
| 0x101 | HEAT_ON_OFF | STM32 → Module | 0=off, 1=on | Enable/disable heating |
| 0x102 | HEAT_QUERY | STM32 → Module | - | Request current status |
| 0x180 | HEAT_STATUS | Module → STM32 | Power %, coil temp, pot detected, fault flags | Periodic status (10Hz) |
| 0x181 | HEAT_FAULT | Module → STM32 | Fault code, details | Fault notification |
| 0x182 | HEAT_ACK | Module → STM32 | Original CAN ID, result | Command acknowledgment |

> [!note]
> Exact CAN message IDs and payload formats depend on the specific microwave surface module. The above is a reference protocol — adapt to the module's documentation.

## Specifications

| Parameter | Value |
|-----------|-------|
| Maximum Power | 1,800W |
| AC Input Voltage | 220-240V, 50Hz single-phase |
| Coil Diameter | 180-220mm (matched to pot base) |
| Efficiency | 85-90% (electrical to thermal) |
| Pot Compatibility | Ferromagnetic (cast iron, stainless w/ magnetic base) |
| Minimum Pot Diameter | 120mm |
| Control Interface | CAN bus (500 kbps) |
| Internal Safety | Pot detection, thermal cutoff, overcurrent, insulation monitoring |
| Temperature Range | 60-250C surface temperature |

## PID Temperature Controller

### Control Loop Architecture

The STM32 runs a discrete PID controller at 10Hz (100ms period) that modulates the induction power to track the temperature setpoint commanded by the CM5 recipe engine. Instead of directly driving an IGBT gate, the PID output is sent as a power level command over CAN bus to the microwave surface module.

```
┌──────────────┐    ┌──────────┐    ┌───────────┐    ┌────────────┐    ┌──────────────┐
│ Recipe Engine │    │  Error   │    │   PID     │    │ CAN Cmd    │    │ Microwave    │
│ (CM5)        │──► │ e(t) =   │──► │ Kp·e +   │──► │ Power %    │──► │ Surface      │
│ Setpoint T*  │    │ T* - T   │    │ Ki·∫e +  │    │ (0-100%)   │    │ Module       │
└──────────────┘    └──────────┘    │ Kd·de/dt │    └────────────┘    └──────┬───────┘
                         ▲          └───────────┘                            │
                         │                                                   ▼
                    ┌────┴────────┐                                ┌──────────────┐
                    │ Temperature │                                │ Induction    │
                    │ Measurement │◄───────────────────────────────│ Coil + Pot   │
                    │ (IR Sensor) │          Thermal Feedback      └──────────────┘
                    └─────────────┘
```

### PID Parameters

| Parameter | Symbol | Initial Value | Notes |
|-----------|--------|---------------|-------|
| Proportional Gain | Kp | TBD | To be tuned experimentally |
| Integral Gain | Ki | TBD | Eliminates steady-state error |
| Derivative Gain | Kd | TBD | Dampens overshoot |
| Update Rate | - | 10 Hz (100ms) | STM32 timer interrupt |
| Output Range | - | 0-100% | Mapped to CAN power level command |
| Anti-Windup | - | Integral clamping | Prevents integral term runaway |
| Setpoint Ramp | - | 5 C/s max | Limits thermal shock |
| Overshoot Limit | - | +10 C above setpoint | Triggers power reduction |

### Output Mapping

Power level (0-100%) sent via CAN maps to average power delivered by the module:

```
Power Level (%)    Power (W)     Application
──────────────    ──────────    ───────────────
     0%              0W        Off / Standby
    10-15%        180-270W     Warm / Keep-warm
    25-35%        450-630W     Simmer
    50%             900W       Medium cook
    80-85%      1440-1530W     Boil
    100%           1800W       Sear / Maximum
```

## Temperature Profiles

### Cooking Stage Targets

| Stage | Target Temp (C) | Power Level | Ramp Rate | Hold Time | Typical Use |
|-------|-----------------|-------------|-----------|-----------|-------------|
| Preheat | 200 | 100% (1800W) | Fast (~20 C/s) | Until target reached | Initial pot heating |
| Sear | 200-250 | 90-100% | - | 30-120s | Browning onions, tempering spices |
| Boil | 100 | 80% (1440W) | Maintain | Until rolling boil | Bringing water/gravy to boil |
| Simmer | 80-95 | 30-40% (540-720W) | Maintain | 10-60 min | Slow cooking dal, curry |
| Warm | 60-70 | 15-20% (270-360W) | Maintain | Until served | Keep-warm after cooking |

### Temperature Transition Diagram

```
Temp (C)
  250 ┤           ┌─── Sear ───┐
      │          /               \
  200 ┤    Preheat                \
      │   /                        \
  100 ┤──/                          └── Boil ──┐
      │                                         \
   80 ┤                                          └── Simmer ──────────┐
      │                                                                \
   60 ┤                                                                 └── Warm
      │
      └──────────────────────────────────────────────────────────────────────────►
        0         2         5        10        20        40        60   Time (min)
```

## Feedback Sources

| Source | Measurement | Interface | Range | Accuracy | Role |
|--------|-------------|-----------|-------|----------|------|
| MLX90614 IR Thermometer | Food surface temperature | I2C (STM32) | -70 to +380 C | +/- 0.5 C | Primary PID feedback |
| NTC Thermistor (Ambient) | Enclosure air temperature | ADC (STM32) | 0-80 C | +/- 2 C | Thermal management |
| Module CAN Status | Coil temperature, fault flags | CAN (STM32 FDCAN1) | Module-reported | Module accuracy | Module health monitoring |

### Sensor Priority Logic

```
IF IR_sensor.valid AND IR_sensor.confidence > threshold:
    feedback = IR_temperature          # Primary: food surface
ELIF module_can.coil_temp.valid:
    feedback = module_coil_temperature # Fallback: module-reported coil temp
    flag_degraded_mode()
ELSE:
    emergency_shutdown()               # No valid temperature data
```

## Safety

### Dual-Layer Safety Architecture

Safety is handled at two levels:

1. **Module-internal:** The microwave surface has its own safety circuits (pot detection, thermal fuse, overcurrent) that operate independently of the STM32. These cannot be overridden by external CAN commands.
2. **System-level:** The STM32 monitors temperature via IR sensor and module CAN status, and can command the module off via CAN or cut AC power via the safety relay.

> [!warning] Critical Safety Section
> The module's internal safety interlocks operate independently of the STM32 and cannot be overridden. The safety relay provides a system-level hard disconnect.

### Safety Summary

| Layer | Mechanism | Trigger | Action | Response Time |
|-------|-----------|---------|--------|---------------|
| Module | Pot detection (internal) | No ferromagnetic pot | Module will not heat | Immediate |
| Module | Thermal cutoff (internal) | Coil over-temperature | Module shuts down internally | <100ms |
| Module | Overcurrent (internal) | Excessive coil current | Module shuts down internally | <10us |
| System | Safety relay | E-stop, STM32 fault, CM5 heartbeat loss | Relay opens, cuts AC to module | <100ms |
| System | STM32 CAN command | IR temp >270C, NTC ambient >70C | Send HEAT_ON_OFF=0 via CAN | <100ms |
| System | STM32 watchdog | Firmware hang | STM32 resets, relay opens (fail-safe) | 1s |

### Safe State Definition

When any safety condition triggers, the system enters the following safe state:

```
1. CAN command ──► HEAT_ON_OFF = 0 (module stops heating)
2. Relay ──► OPEN (physical disconnect of AC to module)
3. Error flag ──► SET (logged to eMMC, displayed on UI)
4. Buzzer ──► ALERT pattern (3 short beeps, 1s pause, repeat)
5. CM5 notified ──► Push notification to companion app
```

## Power Management

### Power Level Table

| Level | Name | Power (W) | CAN Power % | Application |
|-------|------|-----------|-------------|-------------|
| 0 | Off | 0 | 0% | Idle, no cooking |
| 1 | Warm | 200 | 10-15% | Keep food warm after cooking |
| 2 | Low | 450 | 25% | Gentle simmer, slow cooking |
| 3 | Medium | 900 | 50% | Standard cooking, sauce reduction |
| 4 | High | 1,500 | 85% | Boiling water, rapid cooking |
| 5 | Sear | 1,800 | 100% | Browning, tempering spices |

### Soft-Start Sequence

To reduce inrush current and thermal shock, the STM32 ramps the CAN power command from 0 to target over 2-3 seconds:

```
Power (W)
  1800 ┤                            ┌────────── Target
       │                          /
  1200 ┤                        /
       │                      /
   600 ┤                    /
       │                  /
     0 ┤─────────────────/
       └──────────────────────────────────────►
       0s              2s              4s    Time
       │◄── Soft-Start ──►│◄── Steady ──►│
```

### Standby Power

- System standby: <5W total draw (CM5 idle, display off, module off)
- Deep sleep: <2W (CM5 suspended, STM32 in STOP mode, relay open)

## Software Safety

### Watchdog and Heartbeat

| Mechanism | Timeout | Action on Timeout |
|-----------|---------|-------------------|
| STM32 IWDG (Independent Watchdog) | 1 second | Resets STM32 to safe state (CAN off command + relay open) |
| CM5 Heartbeat | 5 seconds | STM32 sends CAN off, opens relay, enters safe standby |
| Maximum Cook Duration | Configurable (default 2 hours) | Graceful shutdown, alert user |
| Temperature Rate Limiter | >30 C/s rise detected | Reduce power to 50%, flag anomaly |

## Testing and Validation

### Test Procedures

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Power Accuracy | Measure input power at each CAN power level with calibrated meter | Within +/- 5% of rated power |
| Temperature Accuracy | Compare IR reading vs. calibrated thermocouple in water | Within +/- 5 C at 100 C |
| PID Step Response | Step setpoint from 25 C to 100 C, record response curve | <90s rise time, <10 C overshoot |
| Safety Relay Timing | Trigger E-stop, measure time to relay open | <100ms from trigger to cutoff |
| Pot Detection | Remove pot during operation, verify module stops heating | Module stops within 500ms |
| CAN Communication | Verify all message IDs send/receive correctly at 500 kbps | No errors over 10,000 messages |
| Thermal Cycling | 1,000 cycles: heat to 250 C, cool to ambient | No component failure or drift >5% |
| Insulation Resistance | 500V DC megger test, mains to logic | >7 Mohm |

### Prototype Validation Checklist

- [ ] Module powers on and responds to CAN queries
- [ ] CAN power level commands correctly modulate heating power
- [ ] Module's internal pot detection prevents heating without pot
- [ ] PID tracks setpoint within +/- 5 C after settling
- [ ] STM32 watchdog resets to safe state on firmware hang
- [ ] CM5 heartbeat loss triggers power cutoff within 5s
- [ ] Safety relay disconnects AC on E-stop
- [ ] Soft-start limits inrush current to acceptable levels
- [ ] Continuous 2-hour cook session completes without fault

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../02-Hardware/Epicura-Architecture|Hardware Architecture]]
- [[10-Robotic-Arm|Robotic Arm System]]
- [[03-Ingredient-Dispensing|Ingredient Dispensing System]]
- [[12-Vision-System|Vision System]]
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]]

#epicura #induction-heating #subsystem #pid-control #canbus

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
