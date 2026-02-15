---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Robotic Arm System

## Overview

The robotic arm is a single-axis rotary stirring mechanism mounted above the cooking pot on a gantry frame. It provides autonomous stirring, scraping, and folding actions driven by the recipe state machine. The arm is controlled by the STM32 real-time controller via PWM and communicates with the CM5 application processor for pattern selection and speed commands.

## Arm Assembly Design

### Mechanical Configuration

- **Type:** Single-axis rotary arm, gantry-mounted above pot center
- **Motion:** 360-degree continuous rotation around the vertical axis
- **Depth:** Fixed paddle depth in V1 (adjustable via manual set screw during setup)
- **Paddle:** Removable silicone or nylon blade, heat-resistant, food-safe
- **Drive:** Servo motor at top of gantry, coupled to a vertical drive shaft through a bearing and seal

### Assembly Diagram

```
┌─────────────────────────────────────────────┐
│                 GANTRY TOP                  │
│                                             │
│            ┌──────────────┐                 │
│            │ Servo Motor  │ ◄── PWM from STM32
│            │ (DS3225)     │                 │
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

## Servo Selection

### Comparison Table

| Parameter | DS3225 (Recommended) | MG996R (Alternative) |
|-----------|---------------------|---------------------|
| Stall Torque | 25 kg-cm (at 6.8V) | 13 kg-cm (at 6V) |
| Operating Voltage | 5.0 - 8.4V | 4.8 - 7.2V |
| Speed (no load) | 0.16 s/60deg (at 6.8V) | 0.17 s/60deg (at 6V) |
| Rotation | 360-degree continuous (modded) | 360-degree continuous (modded) |
| Gear Type | Metal (25T spline) | Metal (25T spline) |
| Interface | Standard PWM (50Hz) | Standard PWM (50Hz) |
| Weight | 65g | 55g |
| IP Rating | None (requires housing) | None (requires housing) |
| Price (approx.) | $12-15 USD | $5-8 USD |
| Recommendation | **Primary choice** -- higher torque handles thick curry loads | Backup option for lighter dishes |

### Selection Rationale

The DS3225 is selected as the primary servo due to its 25 kg-cm stall torque, which provides sufficient margin for stirring thick Indian gravies (dal makhani, paneer butter masala) where resistance can reach 10-15 kg-cm. The MG996R serves as a cost-reduced alternative for recipes involving thinner liquids (rasam, sambar) where lower torque is acceptable.

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
| PWM Frequency | 50 Hz (standard servo protocol) |
| PWM Period | 20 ms |
| Pulse Width Range | 500 - 2500 us |
| Neutral (stop) | 1500 us |
| Full CW Speed | 2500 us |
| Full CCW Speed | 500 us |
| Speed Resolution | ~10 us steps (200 discrete speed levels) |
| STM32 Timer | TIM1 or TIM2 (16-bit, 50Hz output compare) |

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
// Timer configuration for servo PWM
// STM32G4 TIM1 Channel 1, 50Hz output
TIM1->PSC  = (SystemCoreClock / 1000000) - 1;  // 1us resolution
TIM1->ARR  = 20000 - 1;                         // 20ms period (50Hz)
TIM1->CCR1 = 1500;                               // Initial: stopped (neutral)
```

### Command Protocol (CM5 to STM32)

| Command | Code | Parameters | Response | Description |
|---------|------|------------|----------|-------------|
| SET_PATTERN | 0x20 | pattern_id (1 byte), speed (2 bytes, RPM) | ACK/NAK | Set stirring pattern and speed |
| SET_SPEED | 0x21 | speed (2 bytes, RPM, signed for direction) | ACK/NAK | Direct speed override |
| STOP | 0x22 | none | ACK | Immediately stop arm (with decel ramp) |
| HOME | 0x23 | none | ACK | Return to home position |
| STATUS | 0x24 | none | status_byte, current_rpm, position | Query arm status |
| SET_RAMP | 0x25 | accel_limit (2 bytes, RPM/s) | ACK/NAK | Configure acceleration limit |

### FreeRTOS Task Configuration

| Task | Priority | Stack Size | Update Rate | Description |
|------|----------|------------|-------------|-------------|
| Motor Control | 3 (high) | 256 words | 50 Hz (20ms) | PWM update, speed ramping, pattern execution |
| Home Seek | 2 (medium) | 128 words | On-demand | Calibration sequence on boot or command |
| Stall Monitor | 3 (high) | 128 words | 10 Hz | Current monitoring for stall detection |

## Safety

### Torque and Stall Protection

| Safety Feature | Detection Method | Threshold | Action |
|----------------|------------------|-----------|--------|
| Stall Detection | Motor current monitoring via ADC | >2.0A sustained for 500ms | Stop motor, retry up to 3 times, then error |
| Over-Torque | Current spike detection | >3.0A instantaneous | Immediate stop, log event |
| Thermal Protection | Motor housing NTC (optional) | >80 C motor case | Reduce speed 50%, alert if >100 C |
| Mechanical Guard | Physical shroud above pot rim | - | Prevents finger access to paddle zone |

### Stall Recovery Sequence

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Stall   │    │ Stop     │    │ Wait     │    │ Retry    │
│ Detected│──► │ Motor    │──► │ 2s       │──► │ Reverse  │
│ (>2.0A) │    │          │    │          │    │ 180 deg  │
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

- [ ] Servo drives paddle through 360-degree rotation smoothly
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

#epicura #robotic-arm #subsystem #servo-control

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |