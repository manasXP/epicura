---
created: 2026-02-15
modified: 2026-02-20
version: 2.0
status: Draft
---

# Robotic Arm System

## Overview

The robotic arm is a single-axis rotary stirring mechanism mounted above the cooking pot on a gantry frame. It provides autonomous stirring, scraping, and folding actions driven by the recipe state machine. The arm is driven by a 24V BLDC motor with integrated ESC, controlled by the STM32 via PWM speed control, EN (enable), and DIR (direction) signals, and communicates with the CM5 application processor for pattern selection and speed commands.

## Arm Assembly Design

### Mechanical Configuration

- **Type:** Single-axis rotary arm, gantry-mounted above pot center
- **Motion:** 360-degree continuous rotation around the vertical axis
- **Depth:** Fixed paddle depth in V1 (adjustable via manual set screw during setup)
- **Paddle:** Removable silicone or nylon blade, heat-resistant, food-safe
- **Drive:** 24V BLDC motor at top of gantry, coupled to a vertical drive shaft through a bearing and seal

### Assembly Diagram

```
┌─────────────────────────────────────────────┐
│                 GANTRY TOP                  │
│                                             │
│            ┌──────────────┐                 │
│            │ BLDC Motor   │ ◄── PWM+EN+DIR from STM32
│            │ (24V, integ. │                 │
│            │  ESC)        │                 │
│            └──────┬───────┘                 │
│                   │                         │
│            ┌──────┴───────┐                 │
│            │ Shaft Coupler│                 │
│            │ (Aluminum)   │                 │
│            └──────┬───────┘                 │
│                   │                         │
│            ┌──────┴───────┐                 │
│            │ Drive Shaft  │                 │
│            │ (304 SS,     │                 │
│            │  6mm dia.)   │                 │
│            └──────┬───────┘                 │
│                   │                         │
│            ┌──────┴───────┐                 │
│            │ Bearing +    │ ◄── Sealed bearing
│            │ Steam Seal   │     prevents ingress
│            └──────┬───────┘                 │
│                   │                         │
│  ┌────────────────┴────────────────────┐    │
│  │          COOKING POT                │    │
│  │                                     │    │
│  │         ┌───────────┐               │    │
│  │         │  Paddle   │ ◄── Twist-lock
│  │         │  (Silicone│     removable
│  │         │   Blade)  │               │    │
│  │         └───────────┘               │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│                                             │
└─────────────────────────────────────────────┘
```

## Motor Selection

### BLDC Motor Specifications

| Parameter | Value |
|-----------|-------|
| Motor Type | 24V brushless DC (BLDC) with integrated driver/ESC |
| Supply Voltage | 24V DC (direct from PSU rail) |
| Stall Torque | 30-50 kg-cm (model TBD) |
| Speed Range | 0-300 RPM (proportional to PWM duty cycle) |
| Control Interface | PWM (10 kHz, 0-100% duty) + EN (digital) + DIR (digital) |
| Tachometer | FG output (deferred; PA3 reserved for future use) |
| Gear Type | Planetary gearbox (integrated) |
| IP Rating | IP54 or better recommended (kitchen environment) |
| Weight | ~200-400g (varies by model) |
| Price (approx.) | $20-30 USD |

### Selection Rationale

The 24V BLDC motor replaces the DS3225 hobby servo for the following advantages:

- **True continuous rotation** — no modification needed (servos require continuous-rotation mod)
- **Higher torque** — 30-50 kg-cm vs 25 kg-cm for DS3225, better margin for thick Indian gravies
- **Better thermal handling** — brushless design eliminates brush wear and reduces heat buildup during sustained operation
- **No gear wear** — planetary gearbox more durable than servo spur gears under continuous load
- **Direct 24V operation** — eliminates the dedicated 6.5V buck converter (MP1584EN #2 retained for future use)
- **Speed feedback** — FG (tachometer) output available for closed-loop speed control (deferred to post-prototype)
- **Direction control** — hardware DIR pin for instant CW/CCW switching (no pulse-width manipulation)

## Materials

### Food-Contact Components

| Component | Material | Properties | Compliance |
|-----------|----------|------------|------------|
| Drive Shaft | 304 Stainless Steel, 6mm diameter | Corrosion resistant, food-safe, autoclavable | FDA 21 CFR 175-178, EU 1935/2004 |
| Paddle Blade | Silicone (platinum cured) | Heat resistant to 250 C, non-stick, flexible | FDA grade, BPA-free |
| Paddle Blade (alt.) | Nylon 66 (food grade) | Heat resistant to 220 C, rigid, dishwasher-safe | FDA grade |
| Shaft Sleeve | PTFE (Teflon) | Low friction, chemical inert, seals shaft entry | FDA grade |
| Shaft Coupler | 6061 Aluminum (anodized) | Lightweight, corrosion resistant | Not food-contact (above seal line) |
| Motor Housing | ABS or 3D-printed PETG | Steam resistant, lightweight | Not food-contact (above seal line) |

## Stirring Patterns

### Pattern Definitions

| Pattern | Speed (RPM) | Motion Type | Duration | Use Case |
|---------|-------------|-------------|----------|----------|
| Continuous | 60 | Constant clockwise | Ongoing | General cooking, gravy mixing |
| Intermittent | 30 | 5s on / 10s off cycle | Periodic | Simmering, gentle heat distribution |
| Reverse | 45 | Alternating CW/CCW every 10s | Ongoing | Prevent sticking, unstick food from base |
| Scrape | 20 | Slow rotation with edge-seeking offset | 30s bursts | Deglazing, scraping fond from pot bottom |
| Fold | 15 | Gentle wide sweep, half rotation | 20s cycles | Delicate mixing, incorporating fragile ingredients |
| Vigorous | 90 | Fast constant clockwise | 10-30s bursts | Emulsifying, breaking up lumps |
| Off | 0 | Stationary (parked at home position) | - | Idle, ingredient loading, dispensing |

### Pattern Timing Diagram

```
Continuous:  ┌──────────────────────────────────────────────────┐
             │  CW @ 60 RPM (constant)                         │
             └──────────────────────────────────────────────────┘

Intermittent:┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐
             │ ON  │     │ ON  │     │ ON  │     │ ON  │
             └─────┘     └─────┘     └─────┘     └─────┘
              5s    10s   5s    10s   5s    10s   5s

Reverse:     ┌────CW────┐┌───CCW────┐┌────CW────┐┌───CCW────┐
             │  @ 45 RPM ││ @ 45 RPM ││ @ 45 RPM ││ @ 45 RPM │
             └───────────┘└──────────┘└───────────┘└──────────┘
                 10s          10s         10s          10s
```

## Speed Control

### PWM Configuration

| Parameter | Value |
|-----------|-------|
| PWM Frequency | 10 kHz |
| Duty Cycle Range | 0-100% |
| Speed at 0% duty | Stopped |
| Speed at 100% duty | ~300 RPM (max, motor-dependent) |
| EN Pin | PA4 (GPIO) — high = enabled, low = disabled |
| DIR Pin | PA5 (GPIO) — high = CW, low = CCW |
| STM32 Timer | TIM1_CH1 (PA8), ARR=16999, PSC=0 at 170 MHz → 10 kHz |

### Speed Ramping

To prevent splashing and mechanical shock, speed changes are ramped:

```
Target Speed
     ▲
     │            ┌──────────── Steady state
     │           /
     │          / ◄── Acceleration limit: 30 RPM/s
     │         /
     │        /
     │───────/
     │  Ramp-up
     └──────────────────────────────────────────► Time
     0     0.5s    1.0s    1.5s    2.0s
```

- **Acceleration limit:** 30 RPM/s (prevents sudden splashing)
- **Deceleration limit:** 60 RPM/s (faster stop for safety)
- **Emergency stop:** Immediate halt (no ramp, used for safety conditions only)

## Home Position Sensor

### Calibration Reference

- **Sensor Type:** Hall effect sensor (SS49E or equivalent) with small magnet on shaft
- **Position:** Fixed mount at gantry, detects one specific rotational position
- **Purpose:** Zero reference for absolute position tracking and parking
- **Calibration:** On system boot, arm rotates slowly until Hall sensor triggers, establishing home position
- **Parking:** Arm returns to home position after cooking to allow pot removal and ingredient loading

## STM32 Control Interface

### PWM Hardware Configuration

```c
// Timer configuration for BLDC motor PWM
// STM32G4 TIM1 Channel 1, 10 kHz output
TIM1->PSC  = 0;                                   // No prescaler (170 MHz)
TIM1->ARR  = 17000 - 1;                           // 10 kHz period
TIM1->CCR1 = 0;                                   // Initial: stopped (0% duty)

// GPIO configuration for BLDC EN and DIR
// PA4 = BLDC_EN (output, default LOW = disabled)
// PA5 = BLDC_DIR (output, default LOW = CW)
```

### Command Protocol (CM5 to STM32)

| Command | Code | Parameters | Response | Description |
|---------|------|------------|----------|-------------|
| SET_PATTERN | 0x20 | pattern_id (1 byte), speed (2 bytes, RPM), direction (1 byte: 0=CW, 1=CCW) | ACK/NAK | Set stirring pattern, speed, and direction |
| SET_SPEED | 0x21 | speed (2 bytes, RPM), direction (1 byte: 0=CW, 1=CCW) | ACK/NAK | Direct speed and direction override |
| STOP | 0x22 | none | ACK | Immediately stop arm (with decel ramp) |
| HOME | 0x23 | none | ACK | Return to home position |
| STATUS | 0x24 | none | status_byte, current_rpm, position | Query arm status |
| SET_RAMP | 0x25 | accel_limit (2 bytes, RPM/s) | ACK/NAK | Configure acceleration limit |

### FreeRTOS Task Configuration

| Task | Priority | Stack Size | Update Rate | Description |
|------|----------|------------|-------------|-------------|
| Motor Control | 3 (high) | 256 words | 50 Hz (20ms) | BLDC PWM duty cycle + EN/DIR GPIO update, speed ramping, pattern execution |
| Home Seek | 2 (medium) | 128 words | On-demand | Calibration sequence on boot or command |
| Stall Monitor | 3 (high) | 128 words | 10 Hz | Current monitoring for stall detection |

## Safety

### Torque and Stall Protection

| Safety Feature | Detection Method | Threshold | Action |
|----------------|------------------|-----------|--------|
| Stall Detection | INA219 24V rail current spike or FG dropout (future) | >3.0A sustained for 500ms | Disable EN, retry up to 3 times, then error |
| Over-Torque | INA219 current spike detection | >4.0A instantaneous | Immediate EN disable, log event |
| Thermal Protection | Motor current monitoring (thermal proxy) | Sustained high current | Reduce speed 50%, alert if threshold exceeded |
| Mechanical Guard | Physical shroud above pot rim | - | Prevents finger access to paddle zone |

### Stall Recovery Sequence

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Stall   │    │ Stop     │    │ Wait     │    │ Retry    │
│ Detected│──► │ Motor    │──► │ 2s       │──► │ Reverse  │
│ (>3.0A) │    │          │    │          │    │ 180 deg  │
└─────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                      │
                                              ┌───────▼───────┐
                                              │ Resume Pattern │
                                              │ (if clear)     │
                                              │                │
                                              │ OR             │
                                              │                │
                                              │ Error State    │
                                              │ (after 3       │
                                              │  retries)      │
                                              └────────────────┘
```

### Lid Interlock (Future Enhancement)

- Magnetic reed switch on lid detects open/closed state
- Arm will not operate if lid is open (user safety)
- Opening lid during operation triggers arm stop and cook pause

## Cleaning Design

### Tool-Less Disassembly

| Component | Removal Method | Dishwasher Safe | Notes |
|-----------|----------------|-----------------|-------|
| Paddle Blade | Twist-lock (quarter turn) | Yes | Silicone or nylon, hand-wash or dishwasher |
| Shaft Sleeve | Pull-off after paddle removed | Yes | PTFE sleeve slides off shaft |
| Cooking Pot | Lift out | Yes | Standard removable pot |
| Motor Housing | Wipe-down only | No | Above splash zone, sealed |
| Drive Shaft | Not user-removable | N/A | Cleaned in-place with damp cloth |

### Cleaning Sequence

1. Remove pot from unit
2. Twist-lock paddle counterclockwise (quarter turn) and pull down to release
3. Slide shaft sleeve off the drive shaft
4. Place paddle and sleeve in dishwasher or hand-wash with warm soapy water
5. Wipe exposed shaft with damp cloth
6. Reassemble in reverse order (sleeve on shaft, paddle twist-lock clockwise)

## Testing and Validation

### Test Procedures

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Torque Under Load | Stir 2L thick curry (butter chicken consistency) | Continuous operation at 60 RPM without stall |
| Continuous Operation | Run at 45 RPM for 4 hours with medium-viscosity load | No overheating, no stall, no bearing failure |
| Stall Recovery | Manually block paddle, verify detection and retry | Stall detected within 500ms, 3 retries, error state |
| Splash Containment | Run at 90 RPM with 1.5L water, measure splatter | No liquid escapes pot rim (with guard installed) |
| Cleaning Cycle | Disassemble, wash, reassemble 100 times | No wear on twist-lock, secure fit maintained |
| Noise Level | Measure at 30cm during operation at 60 RPM | <50 dB(A) |
| Speed Accuracy | Tachometer measurement at each speed setting | Within +/- 5 RPM of commanded speed |
| Ramp Profile | Record speed vs. time during acceleration | Within +/- 10% of configured ramp rate |
| Home Position | 50 consecutive home-seek operations | Repeatable within +/- 2 degrees |

### Prototype Validation Checklist

- [ ] BLDC motor drives paddle through 360-degree rotation smoothly
- [ ] Twist-lock paddle attachment holds securely during vigorous stirring
- [ ] Stall detection triggers within 500ms of blockage
- [ ] Speed ramping prevents visible splashing at all pattern transitions
- [ ] Steam seal prevents moisture ingress to motor housing over 2-hour cook
- [ ] Home position sensor calibrates reliably on every boot
- [ ] All food-contact surfaces pass dishwasher cycle without degradation
- [ ] Noise level below 50 dB(A) at maximum operational speed

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../02-Hardware/Epicura-Architecture|Hardware Architecture]]
- [[09-Induction-Heating|Induction Heating System]]
- [[03-Ingredient-Dispensing|Ingredient Dispensing System]]
- [[12-Vision-System|Vision System]]
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]]

#epicura #robotic-arm #subsystem #bldc-motor

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
| 2.0 | 2026-02-20 | Manas Pradhan | Replaced DS3225 servo with 24V BLDC motor (integrated ESC); updated motor selection, PWM config (10 kHz), control interface (PWM+EN+DIR), command protocol (added direction param), stall detection (INA219-based), and testing procedures |