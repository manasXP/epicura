---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 6]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 6 — Liquid Dispensing + Vision + Backend (Weeks 11–12)

> **Phase:** Phase 2 — Dispensing & Vision
> **Goal:** Complete all dispensing systems with SLD liquid dispenser and calibration. Start vision pipeline with camera setup and preprocessing. Build backend recipe API. Achieve Milestone M3: Dispensing Complete.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[02-Stories#ARM-SLD.01\|ARM-SLD.01]] | SLD liquid dispenser (peristaltic pumps + load cells) | ARM-SLD | 8 | EMB-SET.01 |
| [ ] | [[02-Stories#ARM-CAL.01\|ARM-CAL.01]] | Dispenser calibration routines | ARM-CAL | 5 | ARM-ASD.01, ARM-CID.01, ARM-SLD.01 |
| [ ] | [[02-Stories#CV-CAM.01\|CV-CAM.01]] | Camera setup (IMX219, CSI-2, streaming) | CV-CAM | 5 | EMB-SET.02, EMB-SET.03 |
| [ ] | [[02-Stories#CV-PRE.01\|CV-PRE.01]] | Image preprocessing pipeline | CV-PRE | 5 | CV-CAM.01 |
| [ ] | [[02-Stories#BE-RCP.01\|BE-RCP.01]] | Recipe CRUD API | BE-RCP | 8 | BE-SET.01 |

**Total Points:** 31

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Embedded Dev 1 | 8 | 16 | SLD liquid dispenser |
| Embedded Dev 2 | 5 | 16 | Dispenser calibration |
| CV Engineer | 10 | 16 | Camera + preprocessing (NEW TEAM MEMBER) |
| Backend Dev 1 | 8 | 8 | Recipe CRUD API |
| **Total** | **31** | **56** | CV team starts |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] SLD dispenses accurate oil and water volumes
- [ ] Load cell feedback validates dispensing
- [ ] All three dispensers (P-ASD, CID, SLD) calibrated
- [ ] Camera streams to CV service
- [ ] Image preprocessing (resize, normalize) works
- [ ] Backend recipe API supports CRUD operations
- [ ] **Milestone M3: Dispensing Complete** achieved

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
