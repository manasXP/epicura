---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 3]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 3 — Thermal Control Start (Weeks 5–6)

> **Phase:** Phase 1 — Thermal & Arm
> **Goal:** Establish thermal control foundation with CAN bus interface to induction module and begin PID temperature controller implementation.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[02-Stories#THR-CAN.01\|THR-CAN.01]] | CAN bus interface to induction module | THR-CAN | 8 | EMB-SET.01 |
| [ ] | [[02-Stories#THR-PID.01\|THR-PID.01]] | PID temperature controller (start, continues Sprint 4) | THR-PID | 8 | EMB-COM.01, THR-CAN.01 |

**Total Points:** 16

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Embedded Dev 1 | 8 | 16 | CAN bus driver and testing |
| Embedded Dev 2 | 8 | 16 | PID controller foundation |
| **Total** | **16** | **32** | Conservative sprint for Phase 1 start |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] CAN bus sends power commands to induction module
- [ ] CAN bus receives status and fault messages
- [ ] PID controller structure implemented (tuning continues Sprint 4)
- [ ] IR thermometer reading integrated into PID loop

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
