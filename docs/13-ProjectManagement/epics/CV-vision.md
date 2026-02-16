---
tags: [epicura, project-management, epic, vision, cv, ml]
created: 2026-02-16
aliases: [CV Epic, Vision Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 4 stories across Sprints 6–7 |

# Epic: CV — Computer Vision Pipeline

Camera setup, image preprocessing, TFLite MobileNetV2 INT8 food classification model, and cooking stage detection with anomaly alerts. Runs on CM5 as a Docker container service.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| CAM — Camera Setup | 1 | 5 | 6 |
| PRE — Image Preprocessing | 1 | 5 | 6 |
| MDL — ML Model | 1 | 10 | 7 |
| DET — Stage Detection | 1 | 8 | 7 |
| **Total** | **4** | **~28** | |

---

## Phase 2 — Vision Setup (Sprint 6)

### CV-CAM.01: Camera setup — IMX219, libcamera, CSI-2, image capture service
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.02|EMB-SET.02]], [[EMB-embedded#EMB-SET.03|EMB-SET.03]]
- **Blocks:** [[CV-vision#CV-PRE.01|CV-PRE.01]]

**Acceptance Criteria:**
- [ ] IMX219 camera detected via libcamera on CM5; CSI-2 ribbon cable ≤150mm
- [ ] Image capture at 1280×720, 30 fps via libcamera-vid or picamera2 Python API
- [ ] Still capture at 3280×2464 (full resolution) for recipe thumbnails
- [ ] Camera accessible from cv-pipeline Docker container via device passthrough
- [ ] Auto-exposure and auto-white-balance enabled; manual override available
- [ ] Test image captured and saved to /data/images/test.jpg

**Tasks:**
- [ ] `CV-CAM.01a` — Connect IMX219 to CM5 CSI-2 port; verify detection with `libcamera-hello`
- [ ] `CV-CAM.01b` — Install picamera2 in cv-pipeline container; configure device passthrough in Docker
- [ ] `CV-CAM.01c` — Implement image capture service: continuous 720p stream + on-demand full-res capture
- [ ] `CV-CAM.01d` — Configure auto-exposure and white balance for kitchen lighting conditions
- [ ] `CV-CAM.01e` — Test capture under various lighting: bright, dim, steam, colored ingredients

---

### CV-PRE.01: Image preprocessing — OpenCV pipeline, ROI extraction, augmentation
- **Sprint:** [[sprint-06|Sprint 6]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[CV-vision#CV-CAM.01|CV-CAM.01]]
- **Blocks:** [[CV-vision#CV-MDL.01|CV-MDL.01]]

**Acceptance Criteria:**
- [ ] Preprocessing pipeline: capture → crop ROI (pot area) → resize 224×224 → normalize
- [ ] ROI detection: circular Hough transform or fixed-region crop for pot boundary
- [ ] Image augmentation for training data: rotation, brightness, contrast, steam overlay
- [ ] Preprocessing latency <50ms per frame on CM5
- [ ] Preprocessed images published to MQTT topic `epicura/cv/frame` as JPEG bytes

**Tasks:**
- [ ] `CV-PRE.01a` — Implement ROI extraction: detect pot boundary using edge detection or fixed coordinates
- [ ] `CV-PRE.01b` — Implement resize and normalization pipeline (224×224, float32 [0,1])
- [ ] `CV-PRE.01c` — Implement data augmentation module for training dataset expansion
- [ ] `CV-PRE.01d` — Optimize pipeline for ARM64: use OpenCV NEON intrinsics where possible
- [ ] `CV-PRE.01e` — Benchmark preprocessing latency; target <50ms per frame

---

## Phase 2 — ML Model & Detection (Sprint 7)

### CV-MDL.01: TFLite food classification model — training, quantization, deployment
- **Sprint:** [[sprint-07|Sprint 7]]
- **Priority:** P0
- **Points:** 10
- **Blocked by:** [[CV-vision#CV-PRE.01|CV-PRE.01]]
- **Blocks:** [[CV-vision#CV-DET.01|CV-DET.01]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]

**Acceptance Criteria:**
- [ ] MobileNetV2 fine-tuned on cooking stage dataset (raw, boiling, simmering, browned, burnt, done)
- [ ] INT8 quantization via TFLite converter; model size <5MB
- [ ] Inference time <100ms on CM5 (CPU, no GPU/NPU)
- [ ] Classification accuracy >85% on validation set (6 classes)
- [ ] Model deployed as .tflite file in cv-pipeline container
- [ ] Inference results published to MQTT: `epicura/cv/classification` with class, confidence, timestamp

**Tasks:**
- [ ] `CV-MDL.01a` — Collect/curate training dataset: 500+ images per class (raw, boiling, simmering, browned, burnt, done)
- [ ] `CV-MDL.01b` — Fine-tune MobileNetV2 on cooking stage dataset (transfer learning from ImageNet)
- [ ] `CV-MDL.01c` — Apply INT8 post-training quantization via TFLite converter
- [ ] `CV-MDL.01d` — Deploy .tflite model to cv-pipeline container; implement inference wrapper
- [ ] `CV-MDL.01e` — Benchmark inference on CM5: measure latency and accuracy on test set
- [ ] `CV-MDL.01f` — Implement MQTT publisher for classification results

---

### CV-DET.01: Cooking stage detection — state tracking, anomaly alerts, confidence thresholds
- **Sprint:** [[sprint-07|Sprint 7]]
- **Priority:** P0
- **Points:** 8
- **Blocked by:** [[CV-vision#CV-MDL.01|CV-MDL.01]]
- **Blocks:** [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]

**Acceptance Criteria:**
- [ ] Stage tracker: smooths classification over 5-frame window (majority vote) to reduce flickering
- [ ] Stage transition detection: publishes `epicura/cv/stage_change` on confirmed transition
- [ ] Anomaly detection: burnt class with confidence >0.7 triggers immediate alert to recipe engine
- [ ] Confidence threshold: only report classification if confidence >0.6; else report "uncertain"
- [ ] Stage history logged to PostgreSQL: timestamp, class, confidence for each transition
- [ ] Visual overlay: current stage label + confidence rendered on camera feed for UI

**Tasks:**
- [ ] `CV-DET.01a` — Implement sliding window classifier: 5-frame majority vote with confidence averaging
- [ ] `CV-DET.01b` — Implement stage transition detector with hysteresis (must hold new class for 3 consecutive windows)
- [ ] `CV-DET.01c` — Implement anomaly alerting: subscribe to classification, publish alert on burnt/overflow detection
- [ ] `CV-DET.01d` — Implement PostgreSQL logging of stage transitions
- [ ] `CV-DET.01e` — Implement visual overlay renderer for Kivy UI camera widget
- [ ] `CV-DET.01f` — Test with recorded cooking videos: verify stage detection accuracy and alert timing

---

## Dependencies

### What CV blocks (downstream consumers)

| CV Story | Blocks | Reason |
|----------|--------|--------|
| CV-CAM.01 | CV-PRE.01 | Camera needed for preprocessing |
| CV-PRE.01 | CV-MDL.01 | Preprocessed images needed for model |
| CV-MDL.01 | CV-DET.01, RCP-FSM.01 | Model needed for stage detection and recipe engine |
| CV-DET.01 | RCP-FSM.01 | Stage detection feeds recipe state machine |

### What blocks CV (upstream dependencies)

| CV Story | Blocked by | Reason |
|----------|------------|--------|
| CV-CAM.01 | EMB-SET.02, EMB-SET.03 | Need CM5 platform and Docker containers |
| CV-PRE.01 | CV-CAM.01 | Need camera images |
| CV-MDL.01 | CV-PRE.01 | Need preprocessing pipeline |
| CV-DET.01 | CV-MDL.01 | Need classification model |

---

## References

- [[__Workspaces/Epicura/docs/05-Subsystems/04-Vision-System|Vision System]]
- [[__Workspaces/Epicura/docs/02-Hardware/03-Sensors-Acquisition|Sensors & Acquisition]]
- [[__Workspaces/Epicura/docs/03-Software/02-Controller-Software-Architecture|Controller Software Architecture]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
