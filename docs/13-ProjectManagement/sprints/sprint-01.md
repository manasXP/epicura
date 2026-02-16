---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 1]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 1 — Embedded Foundation (Weeks 1–2)

> **Phase:** Phase 0 — Foundation
> **Goal:** Establish core embedded platform with STM32 FreeRTOS, CM5 Yocto Linux + Docker, and SPI communication bridge between processors.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[02-Stories#EMB-SET.01\|EMB-SET.01]] | STM32 FreeRTOS project setup | EMB-SET | 8 | PCB-FAB.02 |
| [ ] | [[02-Stories#EMB-SET.02\|EMB-SET.02]] | CM5 Yocto image + Docker Compose | EMB-SET | 8 | PCB-FAB.02 |
| [ ] | [[02-Stories#EMB-COM.01\|EMB-COM.01]] | CM5-STM32 SPI bridge service | EMB-COM | 8 | EMB-SET.01, EMB-SET.02 |

**Total Points:** 24

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Embedded Dev 1 | 16 | 16 | STM32 + CM5 setup, SPI bridge |
| Embedded Dev 2 | 8 | 8 | Support Yocto image, Docker testing |
| **Total** | **24** | **24** | |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] FreeRTOS blinks LED on STM32
- [ ] CM5 boots Yocto with Docker Compose running
- [ ] SPI bridge can send/receive basic messages

## Retro Notes

> _To be filled during sprint retrospective._
>
> **What went well:**
> -
>
> **What could improve:**
> -
>
> **Action items:**
> -

---

## References

- [[__Workspaces/Epicura/docs/13-ProjectManagement/sprints/__init|Sprint Calendar]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/02-Stories|User Stories]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/01-Epics|Epic Index]]
