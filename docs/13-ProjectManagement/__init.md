---
created: 2026-02-15
modified: 2026-02-16
version: 2.0
status: Draft
---

# Project Management - Epicura

## Overview

This folder contains all project management documentation for the Epicura autonomous kitchen robot prototype development.

**Project Duration:** 30 weeks total
- **Pre-Sprint Phase:** 6 weeks (Weeks -6 to 0) — PCB design and fabrication
- **Sprint Phase:** 12 sprints × 2 weeks = 24 weeks (Weeks 1-24)

**Total Budget:** $149,500 - $164,666 (including labor, materials, tools)
**Total Story Points:** ~365 points across 12 epics (~58 stories)

---

## Document Index

### Epics (12 subsystem-based epics)

Individual epic files with detailed stories, acceptance criteria, and task breakdowns:

| Epic | File | Stories | Points |
|------|------|:-------:|:------:|
| **PCB** — PCB Design & Fabrication | [[PCB-pcb-design]] | 6 | ~34 |
| **EMB** — Embedded Platform | [[EMB-embedded]] | 7 | ~46 |
| **THR** — Thermal & Induction Control | [[THR-thermal]] | 4 | ~28 |
| **ARM** — Robotic Arm & Dispensing | [[ARM-actuation]] | 5 | ~35 |
| **CV** — Computer Vision | [[CV-vision]] | 4 | ~28 |
| **RCP** — Recipe Engine | [[RCP-recipe]] | 4 | ~28 |
| **UI** — Touchscreen UI (Kivy) | [[UI-touchscreen]] | 4 | ~24 |
| **BE** — Cloud Backend (Fastify) | [[BE-backend]] | 6 | ~38 |
| **IOS** — iOS App (SwiftUI) | [[IOS-ios]] | 5 | ~30 |
| **AND** — Android App (Kotlin/Compose) | [[AND-android]] | 5 | ~30 |
| **ADM** — Admin Portal (Next.js) | [[ADM-admin]] | 4 | ~22 |
| **INT** — Integration & Validation | [[INT-integration]] | 4 | ~24 |

See [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]] for dependency order and module coverage matrix.

---

### Sprints (12 two-week sprints + pre-sprint)

Individual sprint files with story assignments, capacity allocation, and review checklists:

| Sprint | Weeks | Focus | Milestone |
|--------|:-----:|-------|-----------|
| Pre-Sprint | -6 to 0 | PCB design & fabrication | **M0** — Hardware Ready |
| [[sprint-01]] | 1–2 | STM32 FreeRTOS, CM5 Yocto, SPI bridge | |
| [[sprint-02]] | 3–4 | Docker containers, safety, OTA | **M1** — Platform Ready |
| [[sprint-03]] | 5–6 | CAN bus, PID controller | |
| [[sprint-04]] | 7–8 | Thermal safety, servo arm | **M2** — Thermal + Arm |
| [[sprint-05]] | 9–10 | P-ASD, CID, backend start | |
| [[sprint-06]] | 11–12 | SLD, calibration, camera, recipe API | **M3** — Dispensing Complete |
| [[sprint-07]] | 13–14 | ML model, stage detection, device API | |
| [[sprint-08]] | 15–16 | Recipe engine, mobile apps start | **M4** — Vision + Recipe |
| [[sprint-09]] | 17–18 | State machine, Kivy UI, BLE pairing | |
| [[sprint-10]] | 19–20 | Cooking UI, admin portal, backend launch | **M5** — Software Complete |
| [[sprint-11]] | 21–22 | Integration testing, safety testing | |
| [[sprint-12]] | 23–24 | Reliability, launch readiness | **M6** — Launch Ready |

See [[__Workspaces/Epicura/docs/13-ProjectManagement/sprints/__init|Sprint Calendar]] for phase mapping and velocity tracking.

---

### Supporting Documents

| Doc | Description |
|-----|-------------|
| [[04-Procurement-Schedule]] | Component ordering timeline with suppliers and costs |
| [[05-Resource-Allocation]] | Personnel, labor costs, and budget breakdown |
| [[06-Weekly-Status-Report-Template]] | Weekly reporting template |

---

## Change Log

| Date | Version | Change |
|------|---------|--------|
| 2026-02-16 | 2.0 | Restructured to Urban.ai format: 12 separate epic files, 12 sprint files, stories embedded in epics |
| 2026-02-15 | 1.0 | Initial version with monolithic epics, stories, and sprints files |
