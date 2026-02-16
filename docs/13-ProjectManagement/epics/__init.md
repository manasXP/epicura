---
tags: [epicura, project-management, epics, index]
created: 2026-02-16
aliases: [Epic Index, Epics]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 12 epics with story counts |

# Epics — Index

Twelve subsystem-based epics spanning a 6-week pre-sprint PCB phase and 12 two-week sprints.

## Epic Summary

| Epic | File | Stories | Points (est.) | Sprints Active | Owner |
|------|------|:-------:|:-------------:|----------------|-------|
| **PCB** — PCB Design & Fabrication | [[PCB-pcb-design]] | 6 | ~34 | Pre-Sprint | PCB Engineer |
| **EMB** — Embedded Platform | [[EMB-embedded]] | 7 | ~46 | 1–2, 11–12 | Embedded Engineer |
| **THR** — Thermal & Induction Control | [[THR-thermal]] | 4 | ~28 | 3–4 | Embedded Engineer |
| **ARM** — Robotic Arm & Dispensing | [[ARM-actuation]] | 5 | ~35 | 4–6 | Embedded + Mechanical |
| **CV** — Computer Vision | [[CV-vision]] | 4 | ~28 | 6–7 | ML Engineer |
| **RCP** — Recipe Engine | [[RCP-recipe]] | 4 | ~26 | 8–9 | Software Engineer |
| **UI** — Touchscreen UI (Kivy) | [[UI-touchscreen]] | 4 | ~24 | 9–10 | Frontend Engineer |
| **BE** — Cloud Backend (Fastify) | [[BE-backend]] | 6 | ~38 | 5–10 | Backend Engineer |
| **IOS** — iOS App (SwiftUI) | [[IOS-ios]] | 5 | ~30 | 8–12 | iOS Developer |
| **AND** — Android App (Kotlin/Compose) | [[AND-android]] | 5 | ~30 | 8–12 | Android Developer |
| **ADM** — Admin Portal (Next.js) | [[ADM-admin]] | 4 | ~22 | 10–12 | Web Developer |
| **INT** — Integration & Validation | [[INT-integration]] | 4 | ~24 | 11–12 | All Team |
| | | **~58** | **~365** | | |

## Dependency Order

Epics should be read (and largely built) in this order:

1. **PCB** — No dependencies; fabricated boards required by Sprint 2
2. **EMB** — Depends on PCB; everything depends on EMB platform
3. **THR** — Depends on EMB (STM32 HAL, CAN drivers)
4. **ARM** — Depends on EMB; partially overlaps with THR
5. **CV** — Depends on EMB (CM5 setup, camera CSI-2)
6. **BE** — Partially independent; cloud infrastructure
7. **RCP** — Depends on EMB, THR, ARM, CV (orchestrates all subsystems)
8. **UI** — Depends on RCP (state machine drives UI)
9. **IOS** — Depends on BE (API endpoints)
10. **AND** — Depends on BE (mirrors iOS structure)
11. **ADM** — Depends on BE (admin API endpoints)
12. **INT** — Depends on all other epics

## Module Coverage by Epic

| Module | PCB | EMB | THR | ARM | CV | RCP | UI | BE | IOS | AND | ADM | INT |
|--------|:---:|:---:|:---:|:---:|:--:|:---:|:--:|:--:|:---:|:---:|:---:|:---:|
| Controller PCB | x | x | | | | | | | | | | |
| Driver PCB | x | | x | x | | | | | | | | |
| STM32 Firmware | | x | x | x | | | | | | | | x |
| CM5 Platform | | x | | | x | x | x | | | | | x |
| CAN Bus | | | x | | | | | | | | | x |
| PID Control | | | x | | | x | | | | | | x |
| Servo Arm | | | | x | | x | | | | | | x |
| P-ASD | | | | x | | x | | | | | | x |
| CID | | | | x | | x | | | | | | x |
| SLD | | | | x | | x | | | | | | x |
| Camera/CV | | | | | x | x | x | | | | | x |
| Recipe Engine | | | | | | x | x | x | x | x | x | x |
| Kivy UI | | | | | | | x | | | | | x |
| Cloud API | | | | | | | | x | x | x | x | |
| MQTT | | x | | | | | | x | | | x | x |
| BLE Pairing | | | | | | | | | x | x | | |
| OTA Updates | | x | | | | | | | | | | x |

---

## References

- [[__Workspaces/Epicura/docs/13-ProjectManagement/__init|Project Management Index]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/sprints/__init|Sprint Calendar]]
