---
tags: [epicura, project-management, sprints, index]
created: 2026-02-16
aliases: [Sprint Calendar, Sprint Index]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 12 sprints across 4 phases + pre-sprint PCB phase |

# Sprints — Calendar & Index

A 6-week pre-sprint PCB phase followed by 12 two-week sprints spanning ~30 weeks total.

## Sprint Calendar

| Sprint | Weeks | Phase | Focus | Milestone |
|--------|:-----:|-------|-------|-----------|
| Pre-Sprint | -6 to 0 | PCB | PCB design, fabrication, board bring-up | **M0** — Hardware Ready |
| [[sprint-01]] | 1–2 | Phase 0 | STM32 FreeRTOS, CM5 Yocto, SPI bridge | |
| [[sprint-02]] | 3–4 | Phase 0 | Docker containers, safety, OTA | **M1** — Platform Ready |
| [[sprint-03]] | 5–6 | Phase 1 | CAN bus, PID controller start | |
| [[sprint-04]] | 7–8 | Phase 1 | PID completion, thermal safety, servo arm | **M2** — Thermal + Arm |
| [[sprint-05]] | 9–10 | Phase 2 | P-ASD, CID dispensing, backend start | |
| [[sprint-06]] | 11–12 | Phase 2 | SLD, calibration, camera, backend API | **M3** — Dispensing Complete |
| [[sprint-07]] | 13–14 | Phase 2 | ML model, stage detection, device API | |
| [[sprint-08]] | 15–16 | Phase 3 | Recipe engine, mobile apps start, user API | **M4** — Vision + Recipe |
| [[sprint-09]] | 17–18 | Phase 3 | State machine, dispensing orchestration, Kivy UI, recipe sync | |
| [[sprint-10]] | 19–20 | Phase 3 | Cooking UI, admin portal, backend launch | **M5** — Software Complete |
| [[sprint-11]] | 21–22 | Phase 4 | Integration testing, safety testing, mobile profiles, device monitoring | |
| [[sprint-12]] | 23–24 | Phase 4 | Reliability testing, launch readiness, admin users, production firmware | **M6** — Launch Ready |

## Phase Mapping

| Phase | Sprints | Duration | Primary Deliverables |
|-------|---------|----------|---------------------|
| **Pre-Sprint** — PCB | -6 to 0 | 6 weeks | Controller + Driver PCBs designed, fabricated, validated |
| **Phase 0** — Foundation | 1–2 | 4 weeks | STM32 + CM5 platform, SPI bridge, Docker, safety, OTA |
| **Phase 1** — Thermal & Arm | 3–4 | 4 weeks | CAN, PID control, thermal safety, exhaust, servo arm |
| **Phase 2** — Dispensing & Vision | 5–7 | 6 weeks | All dispensers, camera, ML model, backend foundation |
| **Phase 3** — Software | 8–10 | 6 weeks | Recipe engine, state machine, Kivy UI, mobile apps, admin portal |
| **Phase 4** — Integration & Launch | 11–12 | 4 weeks | System integration, safety cert, reliability, production readiness |

## Sprint Ceremonies

| Ceremony | When | Duration |
|----------|------|----------|
| Sprint Planning | Monday, sprint start | 1.5 hours |
| Daily Standup | Every day | 15 minutes |
| Sprint Review | Friday, sprint end | 1 hour |
| Sprint Retrospective | Friday, sprint end | 30 minutes |

## Velocity Tracking

| Metric | Target |
|--------|--------|
| Total points per sprint | ~20–30 |
| Embedded capacity | ~16 pts (1–2 engineers) |
| Backend capacity | ~8 pts (1 dev, starting Sprint 5) |
| Mobile/Web capacity | ~8 pts (shared, starting Sprint 8) |
| ML/CV capacity | ~8 pts (1 engineer, Sprints 6–7) |

---

## References

- [[__Workspaces/Epicura/docs/13-ProjectManagement/01-Epics|Epic Index]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/__init|Project Management Index]]
