---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 4]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 4 — Thermal Safety + Arm (Weeks 7–8)

> **Phase:** Phase 1 — Thermal & Arm
> **Goal:** Complete PID tuning, add thermal safety interlocks and exhaust fan, implement servo arm control. Achieve Milestone M2: Thermal + Arm.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[02-Stories#THR-PID.01\|THR-PID.01]] | PID temperature controller (continued from Sprint 3) | THR-PID | - | (in progress) |
| [ ] | [[02-Stories#THR-SAF.01\|THR-SAF.01]] | Thermal safety interlocks (cutoff, coil NTC) | THR-SAF | 5 | EMB-SAF.01, THR-PID.01 |
| [ ] | [[02-Stories#THR-EXH.01\|THR-EXH.01]] | PWM exhaust fan control | THR-EXH | 5 | EMB-SET.01 |
| [ ] | [[02-Stories#ARM-SRV.01\|ARM-SRV.01]] | Servo arm control (patterns, stall detection) | ARM-SRV | 8 | EMB-SET.01, EMB-COM.01 |

**Total Points:** 18

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Embedded Dev 1 | 10 | 16 | Complete PID tuning, thermal safety |
| Embedded Dev 2 | 8 | 16 | Exhaust fan + servo arm |
| **Total** | **18** | **32** | |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] PID maintains temperature within ±5°C
- [ ] Thermal cutoff triggers at max temp
- [ ] Exhaust fan responds to temperature thresholds
- [ ] Servo arm executes stir/scrape patterns
- [ ] Servo stall detection works
- [ ] **Milestone M2: Thermal + Arm** achieved

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
