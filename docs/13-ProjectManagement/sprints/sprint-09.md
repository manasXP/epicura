---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 9]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 9 — State Machine + UI + Mobile (Weeks 17–18)

> **Phase:** Phase 3 — Software Integration
> **Goal:** Complete recipe state machine, build dispensing orchestration, implement Kivy UI scaffold, and develop mobile BLE pairing.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[01-Epics#RCP-FSM.01\|RCP-FSM.01]] | Cooking state machine (continued) | RCP | 10 | (from Sprint 8) |
| [ ] | [[01-Epics#RCP-DSP.01\|RCP-DSP.01]] | Dispensing orchestration | RCP | 8 | ARM-ASD.01, ARM-CID.01, ARM-SLD.01, ARM-CAL.01 |
| [ ] | [[01-Epics#RCP-SYN.01\|RCP-SYN.01]] | Cloud recipe sync | RCP | 5 | BE-RCP.01 |
| [ ] | [[01-Epics#UI-SET.01\|UI-SET.01]] | Kivy app scaffold | UI | 5 | EMB-SET.02, EMB-SET.03 |
| [ ] | [[01-Epics#UI-RCP.01\|UI-RCP.01]] | Recipe browser | UI | 5 | UI-SET.01, RCP-FMT.01 |
| [ ] | [[01-Epics#IOS-BLE.01\|IOS-BLE.01]] | BLE pairing | IOS | 8 | IOS-SET.01, BE-DEV.01 |
| [ ] | [[01-Epics#AND-BLE.01\|AND-BLE.01]] | BLE pairing | AND | 8 | AND-SET.01, BE-DEV.01 |

**Total Points:** 49

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Software Engineer | 18 | 20 | RCP-FSM.01 (10 cont.), RCP-DSP.01 (8) |
| Software Engineer (part-time RCP-SYN.01) | 5 | 20 | RCP-SYN.01 (5) |
| Frontend/Kivy Developer | 10 | 20 | UI-SET.01 (5), UI-RCP.01 (5) |
| iOS Developer | 8 | 20 | IOS-BLE.01 (8) |
| Android Developer | 8 | 20 | AND-BLE.01 (8) |
| **Total** | **49** | **100** | Peak sprint — may need to defer lower-priority stories |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] Capacity adjustment plan if stories deferred

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
