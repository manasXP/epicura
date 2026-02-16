---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Vision System

## Overview

The vision system provides real-time food monitoring and cooking stage detection using an overhead HD camera, LED illumination, and edge AI inference on the Raspberry Pi CM5. A TFLite model classifies the current cooking stage (raw, browning, boiling, simmering, done) from camera frames, feeding decisions back to the recipe state machine. The system also supports live video streaming to the touchscreen and companion mobile app, plus anomaly detection for safety-critical events (burning, boil-over, empty pot).

## Camera Selection

### Module Comparison

| Parameter | IMX219 (Standard) | IMX477 (Premium) |
|-----------|-------------------|-------------------|
| Resolution | 8 MP (3280 x 2464) | 12.3 MP (4056 x 3040) |
| Sensor Size | 1/4" (3.68 x 2.76 mm) | 1/2.3" (6.287 x 4.712 mm) |
| Pixel Size | 1.12 um | 1.55 um |
| Interface | MIPI CSI-2 (2-lane) | MIPI CSI-2 (2-lane) |
| Low-Light Performance | Adequate (small pixels) | Superior (larger pixels, better SNR) |
| Lens | Fixed M12 mount (62.2 deg FOV) | Interchangeable C/CS mount |
| Frame Rate (1080p) | 30 fps | 30 fps |
| Price (approx.) | $25 USD | $50 USD |
| Availability | Widely available | Widely available |
| Recommendation | **Prototype** -- low cost, sufficient quality | **Production** -- better low-light, lens flexibility |

### Selection Rationale

The IMX219 is selected for prototyping due to its low cost and adequate resolution for cooking stage classification (inference runs on 224x224 crops). The IMX477 is recommended for production because its larger sensor and interchangeable lens system provide better performance in the steam-heavy, variable-lighting environment inside the enclosure.

## Mounting and Steam Protection

### Camera Position

```
┌──────────────────────────────────────────────────┐
│                  ENCLOSURE LID                    │
│                                                   │
│     ┌───────────┐   ┌──────────────┐              │
│     │ LED Ring  │   │  Camera      │              │
│     │ (WS2812B) │   │  Module      │              │
│     │  ┌─────┐  │   │  ┌───────┐  │              │
│     │  │ O O │  │   │  │ Lens  │  │              │
│     │  │O   O│  │   │  │ (down)│  │              │
│     │  │ O O │  │   │  └───┬───┘  │              │
│     │  └─────┘  │   │      │      │              │
│     └───────────┘   └──────┼──────┘              │
│                            │                      │
│                     20-30cm distance               │
│                            │                      │
│                            ▼                      │
│     ┌──────────────────────────────────────┐      │
│     │           COOKING POT                │      │
│     │         (field of view)              │      │
│     └──────────────────────────────────────┘      │
└──────────────────────────────────────────────────┘
```

### Mounting Specifications

| Parameter | Value |
|-----------|-------|
| Position | Overhead, centered above pot |
| Distance to Pot | 20-30 cm (adjustable bracket) |
| Field of View | Covers entire pot opening plus 2 cm margin |
| Mounting | Gantry bracket, stainless steel |
| Angle Adjustment | +/- 10 degrees tilt (set screw) |
| Vibration Isolation | Rubber dampers (2x M3 silicone grommets) |

### Steam Protection Measures

| Measure | Implementation | Effectiveness |
|---------|---------------|---------------|
| Glass Lens Cover | Borosilicate glass disc, anti-fog hydrophilic coating | Primary barrier, prevents condensation buildup |
| Air Curtain | Small 5V fan (25mm) blowing across lens surface | Diverts rising steam, keeps lens clear |
| Hydrophobic Coating | RainX or nano-coating on glass cover (reapply monthly) | Beads water, reduces fogging |
| Software Dehazing | OpenCV CLAHE or dehazing algorithm on captured frames | Compensates for mild haze when physical measures insufficient |
| Periodic Wipe Reminder | UI notification after N cook cycles | Prompts user to clean lens cover |

## LED Illumination

### Ring Light Design

```
         ┌───────────────────────┐
         │     LED Ring          │
         │   (12-16 WS2812B)    │
         │                       │
         │    O  O  O  O         │
         │  O            O       │
         │  O  ┌──────┐  O      │
         │  O  │Camera│  O      │
         │  O  │ Lens │  O      │
         │  O  └──────┘  O      │
         │  O            O       │
         │    O  O  O  O         │
         │                       │
         └───────────────────────┘
```

### LED Specifications

| Parameter | Value |
|-----------|-------|
| LED Type | WS2812B (addressable RGB) |
| LED Count | 12-16 on ring PCB |
| Color Temperature | 5000K daylight white (for accurate food color) |
| Brightness | 60 mA per LED at max, ~960 mA total ring |
| Control Interface | Single-wire protocol (CM5 GPIO or SPI via DMA) |
| Diffuser | Frosted polycarbonate ring (reduces specular glare on liquids) |
| Power | 5V, max 1A (from 5V rail) |
| Mounting | Co-axial with camera, 5mm offset below lens plane |

### Illumination Modes

| Mode | RGB Value | Brightness | Use Case |
|------|-----------|------------|----------|
| Cooking (default) | Warm white (255, 220, 180) | 80% | Standard cooking illumination |
| Capture (inference) | Daylight white (255, 255, 255) | 100% | Brief flash during frame capture for CV |
| Night Mode | Dim warm (128, 110, 90) | 30% | Low ambient light, reduced eye strain |
| Off | (0, 0, 0) | 0% | Standby, lid open, cleaning |
| Alert | Red pulse (255, 0, 0) | 100% pulsing | Anomaly detected (burning, boil-over) |

## Image Processing Pipeline

### End-to-End Flow

```
┌──────────────┐    ┌───────────────┐    ┌────────────────┐
│ Camera       │    │ Capture       │    │ Preprocess     │
│ (IMX219/477) │──► │ (libcamera    │──► │ (OpenCV)       │
│ CSI-2 bus    │    │  or V4L2)     │    │                │
└──────────────┘    └───────────────┘    └───────┬────────┘
                                                  │
    ┌─────────────────────────────────────────────┘
    │
    ▼
┌────────────────┐    ┌───────────────┐    ┌────────────────┐
│ Resize         │    │ TFLite        │    │ Post-Process   │
│ 224 x 224      │──► │ Inference     │──► │ Confidence     │
│ RGB Normalize  │    │ (MobileNetV2  │    │ Thresholding   │
│                │    │  + custom     │    │ + Temporal      │
│                │    │  head)        │    │ Smoothing       │
└────────────────┘    └───────────────┘    └───────┬────────┘
                                                    │
                                                    ▼
                                           ┌────────────────┐
                                           │ Recipe Engine  │
                                           │ Decision       │
                                           │ (Stage ID +   │
                                           │  Confidence)  │
                                           └────────────────┘
```

### Pipeline Stage Details

| Stage | Input | Output | Library | Notes |
|-------|-------|--------|---------|-------|
| Capture | CSI-2 raw Bayer | 1920x1080 RGB frame | libcamera (Raspberry Pi stack) | 2 fps for inference, 15 fps for streaming |
| Preprocess | 1080p frame | 224x224 normalized tensor | OpenCV (cv2.resize, cv2.cvtColor) | RGB normalization: pixel / 255.0 |
| Histogram Eq. | 224x224 RGB | 224x224 enhanced | OpenCV CLAHE (optional) | Improves contrast in steamy conditions |
| Inference | 224x224 float32 tensor | 8-class probability vector | TFLite Interpreter (Python) | INT8 quantized model, <200ms on CM5 |
| Post-Process | Probability vector | Stage ID + confidence | Custom Python | Confidence threshold >0.6, 3-frame majority vote |

### Inference Timing Budget

```
Operation                Time (ms)    Cumulative
──────────────────────   ──────────   ──────────
Frame capture            10-15        15
Resize + normalize       5-10         25
TFLite inference         100-180      205
Post-processing          2-5          210
Total per frame          ~120-210 ms

Target: < 200ms average (5 fps inference throughput)
Actual inference rate: 2 fps (every 500ms, with headroom)
```

## Classification Stages

### Cooking Stage Definitions

| Stage ID | Stage Name | Visual Cues | Example Dish State |
|----------|-----------|-------------|---------------------|
| 0 | Raw | Uncooked ingredients visible, distinct colors and shapes | Raw onions and tomatoes in oil |
| 1 | Heating | Oil shimmer, steam wisps beginning, surface rippling | Oil surface showing movement |
| 2 | Browning | Color change from white/pale to golden/brown, Maillard reaction | Onions turning translucent then golden |
| 3 | Liquid Added | Visible water/broth/sauce covering ingredients | Water or tomato puree poured in |
| 4 | Boiling | Vigorous bubbling, large bubbles breaking surface | Rolling boil with active surface motion |
| 5 | Simmering | Gentle bubbles, slow surface movement, steady steam | Gentle bubbling dal or curry |
| 6 | Thickening | Reduced liquid level, glossy/viscous surface, less bubbling | Gravy coating spoon, reduced sauce |
| 7 | Done | Final color/texture matching recipe target, minimal activity | Thick dal, well-coated curry |

### Stage Transition Diagram

```
    ┌───────┐    Heat    ┌──────────┐   Browning   ┌──────────┐
    │  RAW  │──────────►│ HEATING  │────────────►│ BROWNING │
    │  (0)  │           │   (1)    │             │   (2)    │
    └───────┘           └──────────┘             └────┬─────┘
                                                      │
                                                      │ Add liquid
                                                      ▼
    ┌───────┐  Reduce   ┌──────────┐    Heat     ┌──────────┐
    │ DONE  │◄─────────│THICKENING│◄────────────│ LIQUID   │
    │  (7)  │          │   (6)    │             │ ADDED(3) │
    └───────┘          └──────────┘             └────┬─────┘
         ▲                  ▲                        │
         │                  │                        │ Heat
         │             Time + Evaporation            ▼
         │                  │               ┌──────────┐
         │                  └───────────────│ BOILING  │
         │                                  │   (4)    │
         │                                  └────┬─────┘
         │                                       │
         │                                       │ Reduce heat
         │                                       ▼
         │                              ┌──────────────┐
         └──────────────────────────────│  SIMMERING   │
                  (Direct finish)       │    (5)       │
                                        └──────────────┘
```

## AI Model Development

### Model Architecture

| Parameter | Value |
|-----------|-------|
| Backbone | MobileNetV2 (transfer learning from ImageNet) |
| Custom Head | Global Average Pooling -> Dense(128, ReLU) -> Dropout(0.3) -> Dense(8, Softmax) |
| Input Shape | 224 x 224 x 3 (RGB) |
| Output | 8-class probability vector (stages 0-7) |
| Total Parameters | ~2.3M (MobileNetV2) + ~130K (custom head) |
| Quantization | INT8 post-training quantization |
| Model Size | ~3.5 MB (INT8 .tflite) |
| Framework | TensorFlow / Keras (training), TFLite (inference) |

### Training Pipeline

```
┌────────────────┐    ┌───────────────┐    ┌────────────────┐
│ Data Collection│    │ Augmentation  │    │ Training       │
│ (1000+ images  │──► │ (rotation,    │──► │ (MobileNetV2   │
│  per stage,    │    │  brightness,  │    │  fine-tune,    │
│  real cooking) │    │  crop, color  │    │  50 epochs)    │
└────────────────┘    │  jitter)      │    └───────┬────────┘
                      └───────────────┘            │
                                                   ▼
┌────────────────┐    ┌───────────────┐    ┌────────────────┐
│ Deploy to CM5  │    │ INT8 Quantize │    │ Evaluate       │
│ (.tflite file  │◄── │ (TFLite       │◄── │ (Validation    │
│  on eMMC)      │    │  Converter)   │    │  accuracy,     │
└────────────────┘    └───────────────┘    │  confusion     │
                                           │  matrix)       │
                                           └────────────────┘
```

### Training Data Requirements

| Stage | Min Images | Collection Method | Augmented Total |
|-------|-----------|-------------------|-----------------|
| Raw (0) | 1,000 | Photograph raw ingredients in pot | 5,000 |
| Heating (1) | 1,000 | Video frames of oil heating | 5,000 |
| Browning (2) | 1,500 | Multiple browning levels, various ingredients | 7,500 |
| Liquid Added (3) | 1,000 | Various liquid types (water, broth, puree) | 5,000 |
| Boiling (4) | 1,000 | Video frames of active boiling | 5,000 |
| Simmering (5) | 1,000 | Extended captures during simmering | 5,000 |
| Thickening (6) | 1,500 | Gradual reduction sequences | 7,500 |
| Done (7) | 1,500 | Final states across many recipes | 7,500 |
| **Total** | **9,500** | | **47,500** (after augmentation) |

### Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Overall Accuracy | >85% | Across all 8 stages |
| Per-Stage Recall | >80% | No stage below 80% recall |
| Inference Latency | <200ms | On CM5 with INT8 quantization |
| Model Size | <5 MB | Fits comfortably on eMMC |
| False Positive Rate (anomaly) | <5% | Burning/boil-over false alarms |

## Rule-Based Fallback

When CV confidence drops below 0.6 or the camera is unavailable, the system falls back to sensor-based cooking stage estimation:

### Fallback Decision Table

| Stage | Temperature Indicator | Time Indicator | Weight Indicator |
|-------|----------------------|----------------|------------------|
| Raw (0) | T < 50 C | t = 0 | Initial weight stable |
| Heating (1) | 50 C < T < 120 C | 0 < t < 3 min | No change |
| Browning (2) | T > 150 C | 2 < t < 8 min | Slight decrease (moisture loss) |
| Liquid Added (3) | T drops sharply | After dispensing | Weight increase (liquid added) |
| Boiling (4) | T = 100 C (+/- 3 C) | After liquid stage | Weight slowly decreasing |
| Simmering (5) | 80 C < T < 95 C | After boil | Weight slowly decreasing |
| Thickening (6) | T rising above 95 C | >70% cook time elapsed | Significant weight loss (>15%) |
| Done (7) | Stable T, recipe timer expired | Cook time complete | Target weight reached |

### Fallback Activation

```
IF camera.status == OFFLINE OR last_inference.confidence < 0.6:
    mode = FALLBACK
    stage = estimate_from_sensors(temperature, weight, elapsed_time)
    notify_user("Vision degraded, using sensor-based cooking")
    log_event(VISION_FALLBACK, reason)
ELSE:
    mode = VISION
    stage = last_inference.stage_id
```

## Anomaly Detection

### Critical Anomalies

| Anomaly | Detection Method | Trigger Condition | Action |
|---------|-----------------|-------------------|--------|
| Burning | Sudden darkening in frame + temperature spike | Dark pixel ratio > 40% AND T > 220 C | Reduce heat to 0%, alert user, pause cooking |
| Boil-Over | Liquid detected at pot rim (region of interest) | Brightness/motion at rim ROI > threshold | Reduce power to 30%, pause stirring, alert |
| Empty Pot | No contents detected in pot area | Frame variance < threshold (flat surface) | Stop heating immediately, alert user |
| Foreign Object | Unexpected shape/color in pot | Classification confidence < 0.3 for all stages | Pause cooking, alert user to inspect |

### Anomaly Detection Pipeline

```
┌──────────────┐
│ Camera Frame │
└──────┬───────┘
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
┌──────────────┐                     ┌──────────────────┐
│ Stage        │                     │ Anomaly Checks   │
│ Classification│                    │ (parallel)       │
│ (TFLite)     │                     │                  │
└──────┬───────┘                     │ 1. Dark pixel %  │
       │                             │ 2. Rim ROI motion│
       │                             │ 3. Frame variance│
       │                             │ 4. Confidence    │
       │                             │    analysis      │
       │                             └────────┬─────────┘
       │                                      │
       ▼                                      ▼
┌──────────────┐                     ┌──────────────────┐
│ Recipe       │                     │ Safety Action    │
│ Engine       │                     │ (if anomaly)     │
│ (normal flow)│                     │ - Reduce heat    │
└──────────────┘                     │ - Alert user     │
                                     │ - Log event      │
                                     └──────────────────┘
```

## Live Feed Streaming

### Streaming Architecture

| Destination | Protocol | Resolution | Frame Rate | Latency Target |
|-------------|----------|------------|------------|----------------|
| Touchscreen (Kivy UI) | Kivy Camera widget (local) | 1080p or 720p | 15 fps | <100ms |
| Mobile App | MJPEG over HTTP or WebRTC | 720p | 15 fps | <500ms (LAN), <2s (WAN) |
| CV Inference | Direct memory buffer | 224x224 (cropped) | 2 fps | <50ms |

### Kivy Camera Widget (Touchscreen)

```python
# Kivy Camera widget for live CSI-2 feed on touchscreen
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout

class CookingCameraView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = Camera(
            resolution=(1280, 720),
            play=True,
            index=0  # CSI-2 camera device
        )
        self.add_widget(self.camera)
```

### MJPEG Streaming (Mobile App)

```python
# Minimal MJPEG HTTP streaming server
# Runs on CM5, accessible at http://<epicura-ip>:8080/stream
import cv2
from flask import Flask, Response

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.resize(frame, (1280, 720))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() + b'\r\n')
```

## Steam Management Solutions

### Multi-Layer Approach

| Layer | Solution | Maintenance | Effectiveness |
|-------|----------|-------------|---------------|
| 1. Physical Barrier | Borosilicate glass lens cover | Replace if cracked | Blocks direct steam contact |
| 2. Anti-Fog Coating | Hydrophilic coating on glass (Cat Crap or similar) | Reapply monthly | Prevents condensation droplets |
| 3. Air Curtain | 25mm 5V fan blowing across lens | Clean fan quarterly | Diverts rising steam column |
| 4. Software Dehaze | OpenCV dehazing on mild haze frames | None | Recovers detail in slightly foggy frames |
| 5. Capture Timing | Brief air puff (compressed air nozzle) before capture | Refill air canister | Clears lens immediately before frame |

## Calibration

### Factory Calibration

| Calibration | Method | Frequency |
|-------------|--------|-----------|
| Color Reference | X-Rite ColorChecker Mini placed in pot, capture reference image | Per-unit (factory) |
| White Balance | Capture under LED ring illumination, compute WB coefficients | Per-unit (factory) |
| Focus Distance | Set focus to pot depth (20-30cm), lock focus ring | Per-unit (factory) |
| LED Uniformity | Capture white reference surface, measure brightness variance | Per-unit (factory) |

### Runtime Calibration

| Calibration | Method | Frequency |
|-------------|--------|-----------|
| Auto White Balance | libcamera AWB with LED ring as known illuminant | Every capture session |
| Exposure Compensation | Auto-exposure with ROI set to pot center | Continuous |
| Steam Compensation | Compare frame clarity metric, apply dehaze if below threshold | Per-frame |

## Testing and Validation

### Test Procedures

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Classification Accuracy | 100 test images per stage, measure per-stage accuracy | >85% overall, >80% per-stage recall |
| Confusion Matrix | Full 8x8 confusion matrix on test set | No off-diagonal >10% |
| Inference Latency | 1000 inference runs, measure mean and P99 latency | Mean <200ms, P99 <300ms |
| Steam Resistance | 30-minute continuous steam exposure, capture frames | Frame clarity metric >70% throughout |
| LED Uniformity | Capture flat white surface, measure brightness std dev | Std dev <10% of mean brightness |
| Low-Light Performance | Capture at 50% LED brightness, run inference | Accuracy drop <5% vs. full brightness |
| Streaming Quality | Stream to app for 1 hour, measure frame drops and latency | Frame drop <2%, latency <500ms (LAN) |
| Anomaly Detection | 50 simulated anomaly events (burning, boil-over) | Detection rate >90%, false positive <5% |
| Fallback Mode | Disable camera, verify sensor-based cooking completes | Recipe completes within +/- 20% of normal cook time |
| Lens Cleaning | Run 10 cook cycles without cleaning, measure clarity degradation | Clarity remains >60% after 10 cycles |

### Prototype Validation Checklist

- [ ] Camera captures clear 1080p frames at 15 fps from mounted position
- [ ] LED ring provides uniform illumination (no hot spots on liquid surface)
- [ ] TFLite model loads and runs inference on CM5 within 200ms
- [ ] Classification correctly identifies at least 6 of 8 stages on real cooking data
- [ ] Steam protection keeps lens clear for 30-minute continuous cooking
- [ ] MJPEG stream accessible from mobile app on same WiFi network
- [ ] Burning anomaly detection triggers within 5 seconds of simulated burn
- [ ] Boil-over detection triggers before liquid exits pot
- [ ] Fallback mode activates automatically when camera is covered/disabled
- [ ] Color calibration produces consistent readings across 10 capture sessions

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[../02-Hardware/Epicura-Architecture|Hardware Architecture]]
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]]
- [[09-Induction-Heating|Induction Heating System]]
- [[10-Robotic-Arm|Robotic Arm System]]
- [[03-Ingredient-Dispensing|Ingredient Dispensing System]]
- [[../06-Compliance/06-Safety-Compliance|Safety & Compliance]]

#epicura #vision-system #computer-vision #ai-ml #subsystem

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |