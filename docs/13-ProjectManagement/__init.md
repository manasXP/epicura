---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Project Management - Epicura

## Overview

This folder contains all project management documentation for the Epicura autonomous kitchen robot prototype development.

**⚠️ CRITICAL UPDATE (2026-02-15):** A **Pre-Sprint PCB Development Phase** has been added to the project plan. The project now spans **30 weeks total** (6 weeks pre-sprint + 24 weeks of sprints).

**Project Duration:** 30 weeks total
- **Pre-Sprint Phase:** 6 weeks (Weeks -6 to 0) — PCB design and fabrication
- **Sprint Phase:** 12 sprints × 2 weeks = 24 weeks (Weeks 1-24)

**Total Budget:** $149,500 - $164,666 (including labor, materials, tools)
**Total Story Points:** 280 core + 51 carryover = 331 points

---

## Document Index

### 1. [[01-Epics|Epics]]
High-level project themes and feature groupings (7 epics: EP-001 through EP-007).

**Status:** Original documentation
**Last Updated:** 2026-02-14

---

### 2. [[02-Stories|User Stories]]
Detailed story definitions with acceptance criteria, story points, and technical notes (29 stories).

**Status:** Original documentation
**Last Updated:** 2026-02-14

---

### 3. [[03-Sprints|Sprint Planning]] ⭐ **UPDATED**
Complete sprint plan including the **critical Pre-Sprint PCB Development Phase**.

**Status:** ⚠️ **UPDATED 2026-02-15** — Now includes Pre-Sprint Phase (Weeks -6 to 0)
**Last Updated:** 2026-02-15

**Major Changes:**
- ✅ Added Pre-Sprint Phase with 3 new stories (PCB-001, PCB-002, PCB-003)
- ✅ Updated timeline to 30 weeks total
- ✅ Added critical path analysis with PCB fabrication dependencies
- ✅ Expanded risk register with Pre-Sprint risks
- ✅ Updated velocity tracking

**Critical Action Required:** PCB design must start **immediately** (Week -8) to meet Sprint 1 deadline.

---

### 4. [[04-Procurement-Schedule|Procurement Schedule]] ⭐ **NEW**
Detailed component ordering timeline with part numbers, suppliers, lead times, and costs.

**Status:** ✅ **NEW — Created 2026-02-15**
**Last Updated:** 2026-02-15

**Content:**
- Pre-Sprint procurement ($725)
- Sprint-by-sprint ordering windows
- Specific Mouser/Digikey part numbers
- Supplier contact info
- Total material cost: $2,056

**Immediate Actions:**
- Order CM5 (2x) by Week -4
- Order STM32G474, DRV8876, TB6612FNG by Week -8
- Order induction surface by Week -2

---

### 5. [[05-Resource-Allocation|Resource Allocation]] ⭐ **NEW**
Personnel assignments, Gantt chart, and labor cost estimates.

**Status:** ✅ **NEW — Created 2026-02-15**
**Last Updated:** 2026-02-15

**Content:**
- Text-based Gantt chart (30 weeks)
- Resource allocation per sprint
- Labor costs: $147,240 total
- Team options (solo / core team / full team)

**Key Insight:** Sprint 10 requires peak staffing (3.3 FTE) with 3 concurrent UI developers.

---

### 6. [[06-Weekly-Status-Report-Template|Weekly Status Report Template]] ⭐ **NEW**
Comprehensive weekly reporting template for tracking progress, budget, risks, and next steps.

**Status:** ✅ **NEW — Created 2026-02-15**
**Last Updated:** 2026-02-15

**Content:**
- Executive summary with KPIs
- Sprint/story progress tracking
- Resource utilization metrics
- Budget status and variance analysis
- Risks, issues, and blockers
- Procurement tracking
- Next week plan
- Lessons learned section

**How to Use:**
1. Copy template each Friday
2. Save as `reports/Weekly-Status-YYYY-MM-DD.md`
3. Distribute to stakeholders
4. Archive for historical tracking

---

## Quick Start Guide

### Immediate Actions (This Week - Week -8)

1. **Hire PCB Design Engineer**
   - Skills: KiCad, STM32, power electronics
   - Budget: $14,400 (4 weeks)
   - Start: This week

2. **Order Long-Lead Components**
   - CM5 (2x): $90 — 4-week lead time
   - STM32G474RET6 (2x): $17 — 3-week lead time
   - See [[04-Procurement-Schedule#Critical Path Items|Procurement Schedule]]

3. **Set Up Infrastructure**
   - Create git repository
   - Set up project tracking (Jira/Trello)
   - Schedule PCB design kickoff

---

## Project Status

### Timeline

| Phase | Weeks | Status | Completion |
|-------|-------|--------|------------|
| Pre-Sprint (PCB) | -6 to 0 | ⏸️ Not Started | 0% |
| Sprint 1-3 (Foundation) | 1-6 | ⏸️ Not Started | 0% |
| Sprint 4-7 (Subsystems) | 7-14 | ⏸️ Not Started | 0% |
| Sprint 8-10 (Integration) | 15-20 | ⏸️ Not Started | 0% |
| Sprint 11-12 (Validation) | 21-24 | ⏸️ Not Started | 0% |

**Current Week:** Week -8 (8 weeks before Sprint 1)

---

### Budget

| Category | Allocated | Spent | % Used |
|----------|-----------|-------|--------|
| Labor | $147,240 | $0 | 0% |
| Materials | $2,256 | $0 | 0% |
| Tools | $200 | $0 | 0% |
| Contingency | $14,970 | $0 | 0% |
| **Total** | **$164,666** | **$0** | **0%** |

---

### Critical Risks

| Risk | Impact | Status |
|------|--------|--------|
| PCB design errors | Critical | 🔴 Monitor |
| Component shortages | Critical | 🔴 Mitigate Now |
| No PCB engineer | Critical | 🔴 Hire ASAP |

🔴 Immediate action | 🟡 Monitor | 🟢 Under control

---

## Key Milestones

| Milestone | Week | Status |
|-----------|------|--------|
| PCB Design Kickoff | -8 | ⏸️ Not Started |
| PCB Submission to JLCPCB | -6 | ⏸️ Not Started |
| PCBs Arrive | -2 | ⏸️ Not Started |
| Sprint 1 Start | 0 | ⏸️ Not Started |
| Thermal Control Complete | 6 | ⏸️ Not Started |
| CV Model Deployed | 14 | ⏸️ Not Started |
| First Recipe Cooked | 18 | ⏸️ Not Started |
| UI Complete | 20 | ⏸️ Not Started |
| Project Complete | 24 | ⏸️ Not Started |

---

## Success Metrics

### MVP Criteria (Minimum Viable Prototype)
- Cook 3 recipes end-to-end autonomously
- Temperature control within ±10°C
- Basic touchscreen UI functional
- Safety interlocks operational
- Dispensing working for all 3 subsystems (ASD, CID, SLD)
- Custom PCBs validated and operational

### Should-Have Criteria
- 5 recipes validated with >80% success rate
- CV-guided stage detection (>85% accuracy)
- Mobile app with live camera feed
- Temperature accuracy ±5°C
- Weight-verified dispensing (±10% accuracy)
- 50+ cook cycle endurance test passed

---

## Methodology

**Framework:** Scrum/Agile
**Sprint Length:** 2 weeks
**Total Sprints:** 12 + Pre-Sprint Phase (6 weeks)
**Team Size:** 1-3 developers (variable based on sprint)

**Sprint Ceremonies:**
- Sprint Planning: 2 hours (start of sprint)
- Daily Standup: 15 minutes
- Sprint Review: 1 hour (end of sprint)
- Sprint Retrospective: 1 hour (end of sprint)

---

## Related Documentation

### Hardware Design
- [[../09-PCB/01-Controller-PCB-Design|Controller PCB Design]] — STM32G474RE board
- [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]] — Power and actuators
- [[../08-Components/04-Total-Component-Cost|Component Cost]] — Full BOM
- [[../02-Hardware/01-Epicura-Architecture|System Architecture]] — Block diagrams

### Software Architecture
- [[../03-Software/01-Tech-Stack|Tech Stack]] — Yocto, FreeRTOS, Kivy, Swift/Kotlin
- [[../03-Software/02-Controller-Software-Architecture|Controller Software]] — Recipe engine

### Project Planning
- [[../07-Development/01-Prototype-Development-Plan|Original Prototype Plan]] — 20-24 week baseline (superseded by 30-week plan)
- [[../../__todo|Project Todo List]] — Current tasks

---

## Change Log

| Date | Document | Change |
|------|----------|--------|
| 2026-02-15 | [[06-Weekly-Status-Report-Template\|Weekly Status Template]] | Created comprehensive reporting template |
| 2026-02-15 | [[04-Procurement-Schedule\|Procurement]] | Created new document |
| 2026-02-15 | [[05-Resource-Allocation\|Resources]] | Created new document |
| 2026-02-15 | [[03-Sprints\|Sprints]] | Added Pre-Sprint Phase |
| 2026-02-15 | `__init.md` | Updated overview |
| 2026-02-14 | [[01-Epics\|Epics]], [[02-Stories\|Stories]] | Original docs |

---

#epicura #projectmanagement #agile #scrum #dashboard

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
