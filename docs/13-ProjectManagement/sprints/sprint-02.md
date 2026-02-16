---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 2]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 2 — Platform Completion (Weeks 3–4)

> **Phase:** Phase 0 — Foundation
> **Goal:** Complete platform foundation with Docker service containers, safety systems, and OTA update infrastructure. Achieve Milestone M1: Platform Ready.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[02-Stories#EMB-SET.03\|EMB-SET.03]] | Docker service containers (PostgreSQL, MQTT, Recipe, CV, UI) | EMB-SET | 5 | EMB-SET.02 |
| [ ] | [[02-Stories#EMB-SAF.01\|EMB-SAF.01]] | Safety systems (watchdog, e-stop, relay) | EMB-SAF | 5 | EMB-SET.01 |
| [ ] | [[02-Stories#EMB-OTA.01\|EMB-OTA.01]] | OTA update system (swupdate + A/B partitions) | EMB-OTA | 5 | EMB-SET.02 |

**Total Points:** 15

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Embedded Dev 1 | 10 | 16 | Docker containers + OTA system |
| Embedded Dev 2 | 5 | 8 | Safety systems implementation |
| **Total** | **15** | **24** | Lower sprint load for stability |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] All Docker containers start and communicate
- [ ] Safety e-stop triggers STM32 shutdown
- [ ] OTA update successfully swaps A/B partitions
- [ ] **Milestone M1: Platform Ready** achieved

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
