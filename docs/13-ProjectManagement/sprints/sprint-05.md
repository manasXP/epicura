---
tags: [epicura, project-management, sprint]
created: 2026-02-16
aliases: [Sprint 5]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version |

# Sprint 5 — Dispensing + Backend Start (Weeks 9–10)

> **Phase:** Phase 2 — Dispensing & Vision
> **Goal:** Implement P-ASD pneumatic seasoning and CID coarse ingredient dispensers. Start backend infrastructure with Fastify project setup.

## Stories

| Status | ID | Title | Epic | Points | Blocked By |
|:------:|-----|-------|------|:------:|------------|
| [ ] | [[02-Stories#ARM-ASD.01\|ARM-ASD.01]] | P-ASD pneumatic seasoning dispenser | ARM-ASD | 8 | EMB-SET.01 |
| [ ] | [[02-Stories#ARM-CID.01\|ARM-CID.01]] | CID coarse ingredient dispenser | ARM-CID | 5 | EMB-SET.01 |
| [ ] | [[02-Stories#BE-SET.01\|BE-SET.01]] | Fastify project setup (TypeScript, PostgreSQL, MQTT) | BE-SET | 8 | - |

**Total Points:** 21

## Capacity Allocation

| Team Member | Allocated | Available | Notes |
|-------------|:---------:|:---------:|-------|
| Embedded Dev 1 | 8 | 16 | P-ASD pneumatic system |
| Embedded Dev 2 | 5 | 16 | CID linear actuator control |
| Backend Dev 1 | 8 | 8 | Fastify project foundation (NEW TEAM MEMBER) |
| **Total** | **21** | **40** | Backend team starts |

## Sprint Review Checklist

- [ ] All stories demo-ready
- [ ] No P0 bugs remaining
- [ ] Documentation updated
- [ ] QA sign-off on completed stories
- [ ] P-ASD dispenses accurate puffs from 6 cartridges
- [ ] P-ASD pressure monitoring works
- [ ] CID push-plate sliders dispense coarse ingredients
- [ ] Fastify server runs with PostgreSQL connection
- [ ] MQTT broker connected to Fastify

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
