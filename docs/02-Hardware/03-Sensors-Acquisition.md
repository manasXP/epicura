---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Sensors & Data Acquisition

## Sensor Overview

| Sensor | Type | Interface | Range | Accuracy | Sampling Rate | Connected To |
|--------|------|-----------|-------|----------|---------------|--------------|
| Camera (IMX219/477) | CMOS image sensor | MIPI CSI-2 (2-lane) | 1080p @ 30fps | N/A (pixel-level) | 2 Hz (CV frames) | CM5 CSI port |
| IR Thermometer (MLX90614) | Non-contact thermopile | I2C (0x5A) | -70 to +380C | +/-0.5C | 10 Hz | STM32 I2C1 |
| Load Cells (4x 5kg) | Strain gauge (Wheatstone bridge) | SPI-like via HX711 | 0-20 kg total | +/-1g | 10 Hz | STM32 GPIO |
| Pot Detection | Reed switch / Hall effect | Digital GPIO | On/Off | N/A | Interrupt-driven | STM32 GPIO |

---

## Camera System

### Module Selection

| Parameter | IMX219 (Standard) | IMX477 (HQ Option) |
|-----------|-------------------|---------------------|
| Resolution | 8 MP (3280x2464) | 12.3 MP (4056x3040) |
| Sensor Size | 1/4" | 1/2.3" |
| Pixel Size | 1.12 um | 1.55 um |
| Max Video | 1080p @ 30fps | 1080p @ 30fps (4K capable) |
| Interface | MIPI CSI-2 (2-lane) | MIPI CSI-2 (2-lane) |
| Lens | Fixed focus, 62.2 deg FOV | C/CS mount (interchangeable) |
| Low-Light Performance | Adequate | Better (larger pixels) |
| Estimated Cost | $25 | $50 |
| Recommendation | **Default choice** (cost, simplicity) | Upgrade for better CV accuracy |

**Selection Rationale:** The IMX219 is the default choice for the prototype. Its fixed-focus lens and adequate resolution are sufficient for food color/texture classification. The IMX477 with a C-mount lens offers more flexibility if fine-grained visual analysis is needed (e.g., detecting individual spice particles or subtle color gradients).

### Camera Mounting

```
┌────────────────────────────────────────────────────┐
│                    Gantry (Top)                     │
│                                                     │
│    Camera Module ──► Mounted on gantry arm          │
│    (facing downward into pot)                       │
│                                                     │
│         ┌──────────────┐                            │
│         │   Camera      │                           │
│         │   (IMX219)    │                           │
│         │   ┌──────┐    │                           │
│         │   │ Lens │    │   ◄── LED Ring            │
│         │   └──┬───┘    │       (surrounding lens)  │
│         └──────┼────────┘                           │
│                │                                    │
│                │  20-30 cm                           │
│                │                                    │
│         ┌──────▼──────────────────────┐             │
│         │                             │             │
│         │         Pot                 │             │
│         │    (diameter ~22cm)         │             │
│         │                             │             │
│         └─────────────────────────────┘             │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Field of View Calculation

At a mounting height of 25cm above a 22cm diameter pot:

```
Camera FOV (IMX219): 62.2 degrees horizontal
Half-angle: 31.1 degrees
Coverage at 25cm: 2 x 25 x tan(31.1) = 2 x 25 x 0.603 = 30.2 cm

Result: 30.2 cm coverage > 22 cm pot diameter
Margin: ~37% extra coverage (captures pot rim and surroundings)
```

For the IMX477 with a suitable lens, FOV can be tuned via lens selection. A 6mm lens at 25cm gives approximately 28cm coverage. A wider 3.6mm lens gives approximately 45cm coverage.

### Lighting System

#### LED Ring Specifications

| Parameter | Value |
|-----------|-------|
| Type | WS2812B addressable RGB LEDs |
| Count | 12-16 LEDs in ring configuration |
| Ring Diameter | 50-60mm (surrounds camera lens) |
| Color Temperature | Neutral white (5000-6500K, RGB mixed) |
| Brightness | Software-adjustable, 0-100% |
| Interface | Single-wire data (SPI/GPIO from CM5 or STM32) |
| Power | 5V, ~60mA per LED at full white (total ~1A max) |

#### Lighting Design

- **Consistent Illumination:** Ring around camera lens provides even, shadow-free lighting on food surface
- **Anti-Glare:** Diffuser film over LEDs reduces specular reflections from liquid surfaces (oil, water)
- **Color Accuracy:** Neutral white enables reliable food color detection (e.g., golden-brown vs. burnt)
- **Adjustable:** Software dims LEDs during non-imaging periods to reduce heat/power

### Calibration

- **White Balance:** Calibrate on boot using a white reference card placed on pot. Store AWB gains per unit.
- **Color Reference:** Optional X-Rite ColorChecker patch card for factory calibration of color reproduction
- **Per-Unit Calibration:** Each unit stores calibration data in `/data/calibration/camera.json` on eMMC
- **Recalibration:** User-triggered recalibration via Settings menu (place white card, press button)

---

## IR Thermometer (MLX90614)

### Specifications

| Parameter | Value |
|-----------|-------|
| Part Number | MLX90614ESF-BAA |
| Type | Non-contact infrared thermopile |
| Object Temperature Range | -70C to +380C |
| Ambient Temperature Range | -40C to +125C |
| Accuracy (0-50C ambient) | +/-0.5C |
| Accuracy (full range) | +/-1.0C |
| Resolution | 0.02C |
| Field of View | 90 degrees (wide FOV variant) |
| Interface | I2C / SMBus (address 0x5A) |
| Supply Voltage | 3.3V (2.6V to 3.6V) |
| Current Consumption | 1.5 mA (typical) |
| Response Time | 100ms (to 90% of final value) |

### Mounting Configuration

```
                     ┌──── Gantry Arm ────┐
                     │                    │
                     │   ┌────────────┐   │
                     │   │  MLX90614  │   │
                     │   │  (angled   │   │
                     │   │   ~30 deg) │   │
                     │   └─────┬──────┘   │
                     │         │          │
                     │         │ IR beam  │
                     │         │ (90 deg  │
                     │         │  FOV)    │
                     │         ▼          │
              ┌──────┴─────────────────────┴──────┐
              │                                    │
              │         Pot (center area)           │
              │     Food surface measurement        │
              │                                    │
              └────────────────────────────────────┘

Mounting distance: 5-10 cm from food surface
Aim: Center of pot
FOV at 7cm distance: covers ~14cm diameter circle
(adequate for pot center measurement)
```

### Emissivity Calibration

Different food surfaces have different IR emissivity values, affecting temperature accuracy:

| Surface | Emissivity | Notes |
|---------|-----------|-------|
| Water | 0.95-0.98 | Highly consistent |
| Cooking Oil | 0.90-0.95 | Depends on oil type |
| Food (general) | 0.90-0.97 | Curries, stews, sauces |
| Metal (pot rim) | 0.10-0.30 | Avoid measuring bare metal |
| Non-stick coating | 0.85-0.95 | Ceramic or PTFE |

- **Default Emissivity:** 0.95 (suitable for most food/water surfaces)
- **Configurable:** Recipe engine can set emissivity per recipe stage (e.g., dry spices vs. liquid gravy)
- **Calibration:** Compare IR reading against reference thermometer in water bath at 50C, 70C, 90C

### I2C Wiring Diagram

```
STM32G474RE                        MLX90614ESF-BAA
┌──────────────────┐              ┌──────────────────┐
│                  │              │                  │
│  PB6 (SCL) ─────┼──────┬──────┼──── Pin 3 (SCL) │
│                  │      │      │                  │
│  PB7 (SDA) ─────┼──────┼──┬───┼──── Pin 1 (SDA) │
│                  │      │  │   │                  │
│  3.3V ───────────┼──┬───┘  │   │  Pin 2 (VDD) ───┼── 3.3V
│                  │  │      │   │                  │
│                  │  R1     R2  │  Pin 4 (VSS) ───┼── GND
│                  │  4.7k   4.7k│                  │
│                  │  │      │   │                  │
│  GND ────────────┼──┴──────┴───┼──── GND          │
│                  │              │                  │
└──────────────────┘              └──────────────────┘

R1, R2: 4.7k ohm pull-up resistors to 3.3V
C1: 100nF ceramic decoupling cap on VDD (close to MLX90614)
Cable: Shielded 4-wire, <30cm length
Shield: Connected to GND at STM32 end only
```

### STM32 Software Interface

```c
// MLX90614 I2C read sequence (simplified)
#define MLX90614_ADDR   0x5A
#define MLX90614_TOBJ1  0x07  // Object temperature register

float mlx90614_read_object_temp(I2C_HandleTypeDef *hi2c) {
    uint8_t buf[3];
    HAL_I2C_Mem_Read(hi2c, MLX90614_ADDR << 1,
                     MLX90614_TOBJ1, I2C_MEMADD_SIZE_8BIT,
                     buf, 3, 100);
    uint16_t raw = buf[0] | (buf[1] << 8);
    // Temperature in Kelvin * 50, convert to Celsius
    float temp_c = (raw * 0.02f) - 273.15f;
    return temp_c;
}
```

---

## Load Cell System

### Strain Gauge Configuration

Four 5kg strain gauges are arranged in a full Wheatstone bridge under the pot platform, providing 20kg total capacity with excellent sensitivity and temperature compensation.

```
                    Excitation+ (E+, 5V from HX711)
                         │
                    ┌────┴────┐
                    │         │
                R1 (SG)    R2 (SG)
                (5kg)      (5kg)
                    │         │
                    ├── A+ ───┤
                    │  (Signal │
                    │   Out+) │
                R4 (SG)    R3 (SG)
                (5kg)      (5kg)
                    │         │
                    └────┬────┘
                         │
                    Excitation- (E-, GND)

SG = Strain Gauge (5 kg full scale)
A+ / A- = Differential signal output to HX711
Total capacity: 20 kg
Nominal resistance: 350 ohm per gauge (typical)
Full-scale output: ~2 mV/V (at rated load)
At 5V excitation: ~10 mV full scale
```

### HX711 ADC Wiring

```
Load Cell Bridge                HX711 Module              STM32G474RE
┌──────────────────┐          ┌──────────────────┐       ┌──────────────┐
│                  │          │                  │       │              │
│  E+ (Red) ──────┼─────────►┼── E+             │       │              │
│  E- (Black) ────┼─────────►┼── E-             │       │              │
│  A+ (Green) ────┼─────────►┼── A+  (Ch A)     │       │              │
│  A- (White) ────┼─────────►┼── A-             │       │              │
│                  │          │                  │       │              │
│                  │          │  DOUT ───────────┼──────►┼── PC1 (IN)  │
│                  │          │  SCK  ◄──────────┼───────┼── PC0 (OUT) │
│                  │          │                  │       │              │
│                  │          │  VCC ◄── 3.3-5V  │       │              │
│                  │          │  GND ◄── GND     │       │              │
│                  │          │                  │       │              │
│                  │          │  RATE: GND=10Hz  │       │              │
│                  │          │        VCC=80Hz  │       │              │
└──────────────────┘          └──────────────────┘       └──────────────┘

HX711 Specifications:
  - Input: Differential, from Wheatstone bridge
  - ADC Resolution: 24-bit (effective ~20-bit noise-free)
  - Gain: 128 (Channel A, default) or 64 (Channel A) or 32 (Channel B)
  - Sampling Rate: 10 Hz (RATE pin LOW) or 80 Hz (RATE pin HIGH)
  - Output: Serial data via DOUT/SCK protocol
  - Excitation: On-chip 5V regulated output for bridge
```

### Calibration Procedure

1. **Zero Offset (Tare):**
   - On system boot (no pot), read 10 samples and average
   - Store as `tare_offset` (raw ADC counts)
   - Repeat tare when pot is placed (pot weight becomes new zero)

2. **Scale Factor:**
   - Place known calibration weight (e.g., 500g) on platform
   - Read raw ADC value, subtract tare_offset
   - `scale_factor = known_weight_g / (raw_value - tare_offset)`
   - Store in `/data/calibration/loadcell.json`

3. **Linearity Check:**
   - Test at 100g, 500g, 1000g, 2000g, 5000g
   - Verify readings are within +/-1% of linear fit
   - If nonlinear, apply polynomial correction (2nd or 3rd order)

4. **Temperature Drift:**
   - Full Wheatstone bridge provides first-order temperature compensation
   - For high accuracy, recalibrate tare when ambient temp changes >10C

### Measurements and Use Cases

| Measurement | Method | Accuracy | Use Case |
|-------------|--------|----------|----------|
| Ingredient Weight | Dispense, measure delta | +/-2g | Verify correct amount dispensed |
| Evaporation Rate | Continuous weight monitoring | +/-5g | Detect water loss during simmering |
| Pot Detection | Weight > threshold (500g) | Binary | Interlock: don't heat without pot |
| Total Food Weight | Current weight - pot tare | +/-5g | Portion tracking, recipe scaling |
| Stirring Torque (indirect) | Weight oscillation during stir | Qualitative | Detect thick vs. thin consistency |

### STM32 Software Interface

```c
// HX711 read sequence (bit-bang GPIO)
#define HX711_SCK_PIN  GPIO_PIN_0  // PC0
#define HX711_DOUT_PIN GPIO_PIN_1  // PC1
#define HX711_PORT     GPIOC

int32_t hx711_read_raw(void) {
    // Wait for DOUT to go LOW (data ready)
    while (HAL_GPIO_ReadPin(HX711_PORT, HX711_DOUT_PIN) == GPIO_PIN_SET);

    int32_t value = 0;
    for (int i = 0; i < 24; i++) {
        HAL_GPIO_WritePin(HX711_PORT, HX711_SCK_PIN, GPIO_PIN_SET);
        delay_us(1);
        value = (value << 1) | HAL_GPIO_ReadPin(HX711_PORT, HX711_DOUT_PIN);
        HAL_GPIO_WritePin(HX711_PORT, HX711_SCK_PIN, GPIO_PIN_RESET);
        delay_us(1);
    }
    // 25th pulse: set gain to 128 for next read (Channel A)
    HAL_GPIO_WritePin(HX711_PORT, HX711_SCK_PIN, GPIO_PIN_SET);
    delay_us(1);
    HAL_GPIO_WritePin(HX711_PORT, HX711_SCK_PIN, GPIO_PIN_RESET);
    delay_us(1);

    // Sign-extend 24-bit to 32-bit
    if (value & 0x800000) {
        value |= 0xFF000000;
    }
    return value;
}

float hx711_read_grams(int32_t tare_offset, float scale_factor) {
    int32_t raw = hx711_read_raw();
    return (float)(raw - tare_offset) * scale_factor;
}
```

---

---

## Pot Detection

### Mechanism

A reed switch (or Hall effect sensor) detects the presence of a ferromagnetic pot on the induction platform. A small magnet is embedded in the pot base; when the pot is placed on the platform, the reed switch closes.

```
        ┌── Pot Base (with embedded magnet) ──┐
        │                                      │
        │          [N ▓▓ S]  Magnet            │
        │                                      │
        └──────────────────────────────────────┘
                         │
                    ~2-5mm gap
                         │
        ┌──────────────────────────────────────┐
        │      Platform Surface                │
        │                                      │
        │     ┌──────────────────┐             │
        │     │   Reed Switch    │             │
        │     │   (NC or NO)     │             │
        │     └───┬──────────┬───┘             │
        │         │          │                 │
        └─────────┼──────────┼─────────────────┘
                  │          │
              STM32 PB1   GND (with 10k pull-up to 3.3V)
              (GPIO input,
               interrupt-capable)

Alternative: Hall effect sensor (SS49E or A3144)
  - More robust (no mechanical contacts)
  - Analog output (SS49E) or digital (A3144)
  - Requires small magnet in pot base
```

### Interlock Logic

1. On boot, STM32 queries microwave surface module via CAN for pot detection status
2. If pot not detected, display "Place pot" on UI
3. Module will not heat without pot detected (internal interlock)
4. If pot removed during cooking, module stops heating internally; STM32 receives status via CAN
5. Recipe pauses and UI shows "Pot removed" warning
6. When pot replaced, resume after 3-second confirmation delay

---

## Sensor Fusion

### Multi-Sensor Cooking Stage Detection

The recipe engine on CM5 combines data from multiple sensors to determine the current cooking stage and trigger transitions:

```
┌─────────────────────────────────────────────────────────┐
│                  Sensor Fusion Pipeline                  │
│                                                         │
│  Camera (2Hz)                                           │
│  ├── Color histogram ──────────┐                        │
│  ├── Texture features ─────────┤                        │
│  └── Bubble detection ─────────┤                        │
│                                │                        │
│  IR Temp (10Hz)                ├──► Stage Classifier    │
│  ├── Surface temperature ──────┤    (CM5, TFLite/       │
│  └── Rate of change ───────────┤     OpenCV logic)      │
│                                │         │              │
│  Load Cells (10Hz)             │         ▼              │
│  ├── Current weight ───────────┤    Cooking Stage ID    │
│  └── Weight delta/min ─────────┘    (e.g., "browning",  │
│                                      "boiling",         │
│                                      "simmering",       │
│                                      "done")            │
│                                         │               │
│                                         ▼               │
│                                   Recipe State Machine   │
│                                   (next action:          │
│                                    adjust temp,          │
│                                    add ingredient,       │
│                                    change stir speed)    │
└─────────────────────────────────────────────────────────┘
```

### Decision Matrix

| Cooking Stage | Camera Signal | IR Temp (C) | Weight Change | Confidence |
|---------------|---------------|-------------|---------------|------------|
| Raw/Cold | Raw ingredient colors, no bubbles | <50 | Stable | High |
| Heating | Slight color shift, steam wisps | 50-90 | Stable | Medium |
| Boiling | Active bubbles, steam, rolling motion | 95-102 | Slow decrease | High |
| Browning | Golden-brown color shift, darkening edges | 120-180 | Moderate decrease | High |
| Simmering | Gentle bubbles, consistent color | 80-95 | Slow decrease | High |
| Thickening | Darker color, less liquid visible | 85-100 | Significant decrease | Medium |
| Done | Target color/texture reached | Recipe-specific | Recipe-specific | Recipe-dependent |
| Burning (ALERT) | Dark/black spots, smoke detection | >200 | Rapid decrease | High |

### Sampling Rate Summary

| Sensor | Acquisition Rate | Processing Rate | Latency Budget |
|--------|-----------------|-----------------|----------------|
| Camera | 30 fps capture | 2 Hz CV inference | <500ms per frame |
| IR Thermometer | 10 Hz read | 10 Hz to PID | <100ms |
| Load Cells | 10 Hz read | 10 Hz to recipe engine | <100ms |
| Pot Detection | Interrupt-driven | Immediate (<1ms) | <1ms |

---

## Sensor Quality Monitoring

### Health Check Table

| Sensor | Health Check | Pass Criteria | Failure Mode |
|--------|-------------|---------------|--------------|
| Camera | Frame received, not black/white | Valid histogram, >10% variance | Lens blocked, cable loose, module fault |
| IR Thermometer | I2C ACK, reading in range | ACK on address, -20C < T < 350C | I2C bus fault, sensor damaged |
| Load Cells | Zero drift check, range valid | Drift < 5g/hour, 0 < raw < 0xFFFFFF | Bridge wire break, HX711 fault |
| Pot Detection | State change matches expectations | Toggles when pot placed/removed | Switch stuck, magnet missing |

### Degradation Fallback Strategy

| Primary Sensor Failed | Fallback Strategy | Limitations |
|-----------------------|-------------------|-------------|
| Camera fails | Timer-based cooking (no CV stage detection) | Cannot detect browning, must rely on time/temp |
| IR thermometer fails | CAN coil temp + camera (color-based temp estimation) | Less accurate food temp, wider PID margins |
| Load cells fail | Timer-based dispensing (open gate for N seconds) | Cannot verify dispensed weight, +/-20% accuracy |

---

## Testing & Validation

### Camera Test Procedures

- [ ] Mount camera at 25cm height, verify full pot is in frame
- [ ] Capture image of white card, verify white balance (R/G/B within +/-10%)
- [ ] Capture image of X-Rite ColorChecker, verify color accuracy (deltaE < 5)
- [ ] LED ring on: verify even illumination (no hot spots >20% variance)
- [ ] LED ring off: verify camera captures adequate image under typical kitchen lighting
- [ ] Steam test: boil water for 10 minutes, verify lens does not fog (shroud effective)
- [ ] FPS test: verify 30fps capture sustained over 30 minutes

### IR Thermometer Test Procedures

- [ ] Read room temperature, compare to reference thermometer (+/-1C)
- [ ] Read boiling water surface, verify 97-102C (altitude-dependent)
- [ ] Read 70C water bath, compare to reference (+/-1C)
- [ ] Read cooking oil at 180C, compare to reference (+/-3C)
- [ ] Emissivity test: compare readings for water (0.95) vs. oil (0.92)
- [ ] Steam interference: verify stable reading during active boiling
- [ ] Response time: apply sudden temp change, verify 90% response in <200ms

### Load Cell Test Procedures

- [ ] Tare with empty platform, verify drift <2g over 10 minutes
- [ ] Place 100g weight, verify reading 98-102g
- [ ] Place 500g weight, verify reading 495-505g
- [ ] Place 2000g weight, verify reading 1990-2010g
- [ ] Linearity: plot weight vs. reading for 5 points, R-squared >0.999
- [ ] Temperature test: verify drift <5g over 0-40C ambient range
- [ ] Dynamic test: dispense water into pot, verify weight tracks smoothly

### Pot Detection Test Procedures

- [ ] Place pot: verify detection within 100ms
- [ ] Remove pot: verify detection within 100ms
- [ ] Verify interlock: attempt to enable induction without pot, confirm rejection
- [ ] Verify interlock: remove pot during heating, confirm shutdown within 100ms
- [ ] Test with non-magnetic pot: verify no false detection

---

## Related Documentation

- [[02-Technical-Specifications|Technical Specifications]]
- [[Epicura-Architecture|Hardware Architecture & Wiring Diagrams]]
- [[07-Mechanical-Design|Mechanical Design]]
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software]]

#epicura #sensors #data-acquisition

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
