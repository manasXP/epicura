---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Weekly Status Report Template

## How to Use This Template

1. **Copy this entire document** and create a new file named `Weekly-Status-YYYY-MM-DD.md` in a `reports/` subfolder
2. **Fill in all sections** each Friday before end of day
3. **Update the dashboard** with current week number and dates
4. **Distribute** to stakeholders via email or Slack
5. **Archive** previous week's report for historical tracking

---

# Epicura Prototype - Weekly Status Report

**Report Date:** [YYYY-MM-DD]
**Reporting Week:** Week [X] of 30
**Report Period:** [Start Date] to [End Date]
**Submitted By:** [Your Name]
**Project Phase:** [Pre-Sprint / Sprint X / Post-Project]

---

## Executive Summary

**Overall Status:** 🟢 On Track | 🟡 At Risk | 🔴 Delayed | ⏸️ On Hold

**Week Highlights (3-5 bullets):**
- [Major achievement or milestone completed this week]
- [Key decision made or blocker removed]
- [Important procurement received or ordered]
- [Notable risk identified or mitigated]

**Key Metrics:**
- **Story Points Completed:** [X] of [Y] planned ([Z]% completion)
- **Budget Spent This Week:** $[X,XXX]
- **Cumulative Budget Used:** $[XX,XXX] of $164,666 ([Z]%)
- **Team Utilization:** [X.X] FTE this week

---

## Current Sprint/Phase Status

### Active Sprint: [Sprint Name or Pre-Sprint Phase]
**Sprint Goal:** [One sentence describing the sprint objective]
**Sprint Dates:** [Start Date] to [End Date]
**Days Remaining:** [X] of [Y] days

### Story Progress

| Story ID | Story Name | Points | Status | % Complete | Owner | Notes |
|----------|------------|--------|--------|------------|-------|-------|
| ST-XXX | [Story Name] | 8 | ✅ Done | 100% | [Name] | Completed [date] |
| ST-XXX | [Story Name] | 13 | 🔄 In Progress | 60% | [Name] | On track, minor delay |
| ST-XXX | [Story Name] | 5 | ⏸️ Blocked | 10% | [Name] | Waiting on [component/decision] |
| ST-XXX | [Story Name] | 3 | 📋 Not Started | 0% | [Name] | Planned for next week |

**Legend:** ✅ Done | 🔄 In Progress | ⏸️ Blocked | 📋 Not Started | ❌ Cancelled

### Sprint Burndown

```
Story Points Remaining
25 |●
20 |  ●●
15 |    ●●
10 |      ●●
 5 |        ●●
 0 |__________●
   Mon Tue Wed Thu Fri

● = Actual burndown
/ = Ideal (linear) burndown
```

**Analysis:** [Brief comment on whether sprint is on track, ahead, or behind schedule]

---

## Accomplishments This Week

### Completed Work

#### 1. [Achievement Title]
- **Story:** ST-XXX ([Story Name])
- **Description:** [What was accomplished]
- **Impact:** [Why this matters for the project]
- **Artifacts:** [Links to code commits, docs, test results]

#### 2. [Achievement Title]
- **Story:** ST-XXX ([Story Name])
- **Description:** [What was accomplished]
- **Impact:** [Why this matters for the project]
- **Artifacts:** [Links to code commits, docs, test results]

#### 3. [Achievement Title]
- **Story:** ST-XXX ([Story Name])
- **Description:** [What was accomplished]
- **Impact:** [Why this matters for the project]
- **Artifacts:** [Links to code commits, docs, test results]

### Milestones Reached
- [ ] [Milestone Name] — [Date Achieved] ✅
- [ ] [Milestone Name] — [Planned Date: YYYY-MM-DD]

---

## Resource Utilization

### Team Capacity This Week

| Role | Planned % | Actual % | Variance | Hours | Notes |
|------|-----------|----------|----------|-------|-------|
| PCB Engineer | 100% | 80% | -20% | 32/40 | Sick day Wednesday |
| Embedded Developer | 100% | 110% | +10% | 44/40 | Overtime for critical fix |
| Mechanical Engineer | 60% | 70% | +10% | 28/40 | Extra iteration on servo arm |
| ML/CV Engineer | 0% | 0% | 0% | 0/40 | Not active this sprint |
| **Total FTE** | **2.6** | **2.6** | **0%** | **104** | |

**Notes:**
- [Explanation of significant variances]
- [Any planned time off next week]
- [Overtime justification if applicable]

### External Dependencies
- **Waiting On:** [What we're blocked by]
  - **Status:** [Vendor/person status]
  - **ETA:** [Expected resolution date]
  - **Impact:** [How this affects timeline]

---

## Procurement & Components

### Orders Placed This Week

| Item | Part Number | Qty | Supplier | Cost | Order Date | ETA | Status |
|------|-------------|-----|----------|------|------------|-----|--------|
| [Component] | [PN] | 2 | Mouser | $XX.XX | YYYY-MM-DD | YYYY-MM-DD | 🚚 Shipped |
| [Component] | [PN] | 5 | Digikey | $XX.XX | YYYY-MM-DD | YYYY-MM-DD | ⏳ Processing |

### Components Received This Week
- ✅ [Component Name] (Qty: X) — Inspected and stored
- ✅ [Component Name] (Qty: X) — Integrated into build

### Upcoming Orders (Next Week)
- [ ] [Component Name] — Week [X] ordering window — Budget: $XXX
- [ ] [Component Name] — Week [X] ordering window — Budget: $XXX

### Procurement Issues
- ⚠️ **[Component Name]:** Out of stock at Mouser
  - **Impact:** Delays Sprint X by [Y] days
  - **Mitigation:** Ordered from Digikey backup supplier, +2 days delivery

---

## Budget Status

### Weekly Spend

| Category | This Week | Cumulative | Allocated | Remaining | % Used |
|----------|-----------|------------|-----------|-----------|--------|
| Labor | $[X,XXX] | $[XX,XXX] | $147,240 | $[XXX,XXX] | [XX]% |
| Materials | $[XXX] | $[X,XXX] | $2,256 | $[X,XXX] | [XX]% |
| Tools | $[XX] | $[XXX] | $200 | $[XXX] | [XX]% |
| Contingency | $[X] | $[XXX] | $14,970 | $[XX,XXX] | [X]% |
| **Total** | **$[X,XXX]** | **$[XX,XXX]** | **$164,666** | **$[XXX,XXX]** | **[XX]%** |

### Budget Variance Analysis
- **Status:** 🟢 Under Budget | 🟡 On Budget | 🔴 Over Budget
- **Projected Overrun/Savings:** $[X,XXX] ([+/-]%)
- **Explanation:** [Why variance occurred, if significant]

### Major Expenses This Week
1. **[Expense Name]:** $[XXX] — [Justification]
2. **[Expense Name]:** $[XXX] — [Justification]

---

## Risks & Issues

### Active Risks

| Risk ID | Risk Description | Probability | Impact | Status | Owner | Mitigation |
|---------|------------------|-------------|--------|--------|-------|------------|
| R-001 | PCB design errors | Medium | Critical | 🟡 Monitor | [Name] | Design reviews scheduled |
| R-002 | Component shortage (CM5) | Medium | Critical | 🔴 Active | [Name] | Ordered 2x backup units |
| R-003 | PID tuning difficulty | Low | Medium | 🟢 Mitigated | [Name] | Auto-tune method working |

**Risk Status Legend:** 🔴 Active (immediate action) | 🟡 Monitor | 🟢 Mitigated | ⚫ Closed

### New Risks Identified This Week
1. **[Risk Title]**
   - **Probability:** High / Medium / Low
   - **Impact:** Critical / High / Medium / Low
   - **Description:** [What could go wrong]
   - **Mitigation Plan:** [What we'll do to prevent/reduce impact]

### Closed Risks This Week
- ⚫ **[Risk Title]:** [Why risk is no longer applicable]

---

## Issues & Blockers

### Critical Issues (Immediate Action Required)

#### Issue #1: [Issue Title]
- **Status:** 🔴 Critical
- **Discovered:** [Date]
- **Impact:** [How this affects timeline/deliverables]
- **Root Cause:** [What caused this issue]
- **Action Plan:**
  1. [Action item 1] — Owner: [Name] — Due: [Date]
  2. [Action item 2] — Owner: [Name] — Due: [Date]
- **ETA for Resolution:** [Date]

### Active Blockers

| Blocker | Blocking Story | Impact | Owner | Status | ETA |
|---------|---------------|--------|-------|--------|-----|
| [Blocker description] | ST-XXX | Sprint delayed 2 days | [Name] | Working | YYYY-MM-DD |

### Resolved Issues This Week
- ✅ **[Issue Title]:** Resolved on [Date] — [Brief explanation]

---

## Technical Highlights

### Code/Design Artifacts Produced
- **Git Commits:** [X] commits to [repo/branch]
  - Link: [GitHub/GitLab URL]
- **Documentation Updated:**
  - [Document name] — [Link]
- **Tests Written/Passed:**
  - [Test name]: [Pass/Fail] — [X/Y] test cases

### Technical Decisions Made
1. **Decision:** [What was decided]
   - **Rationale:** [Why this decision was made]
   - **Alternatives Considered:** [What else was evaluated]
   - **Impact:** [How this affects architecture/timeline]

### Design Reviews Completed
- **PCB Review:** Controller PCB schematic — [Pass/Fail with comments]
- **Code Review:** STM32 UART driver — Approved with minor changes

---

## Testing & Validation

### Tests Executed This Week

| Test | Type | Result | Issues Found | Notes |
|------|------|--------|--------------|-------|
| Power-on test (Controller PCB) | Integration | ✅ Pass | 0 | All rails within spec |
| UART loopback test | Unit | ✅ Pass | 0 | <5ms latency achieved |
| PID step response | Integration | ⚠️ Partial | 1 | Overshoot 15% (target: <10%) |

### Quality Metrics
- **Test Coverage:** [XX]% (target: 80%)
- **Defect Density:** [X] bugs per 100 lines of code
- **Mean Time to Fix:** [X] hours average

---

## Next Week Plan

### Sprint Goal for Next Week
[One sentence describing what you aim to accomplish]

### Planned Work

| Story ID | Story Name | Points | Owner | Key Tasks |
|----------|------------|--------|-------|-----------|
| ST-XXX | [Story Name] | 8 | [Name] | - Task 1<br>- Task 2<br>- Task 3 |
| ST-XXX | [Story Name] | 5 | [Name] | - Task 1<br>- Task 2 |

### Key Activities
- **Monday:** [Activity or meeting]
- **Tuesday:** [Activity or meeting]
- **Wednesday:** [Mid-week checkpoint] — Sprint review if applicable
- **Thursday:** [Activity or meeting]
- **Friday:** [Activity or meeting] — Next status report due

### Meetings & Reviews
- **Sprint Planning:** [Date/Time] — [Attendees]
- **Design Review:** [Date/Time] — [What's being reviewed]
- **Stakeholder Demo:** [Date/Time] — [What will be demonstrated]

### Procurement Actions
- [ ] Order [Component X] by [Day of Week]
- [ ] Confirm shipment for [Component Y]
- [ ] Receive and inspect [Component Z]

---

## Dependencies & Coordination

### Waiting On (External)
- **[Vendor/Person]:** [What we need] — ETA: [Date]
- **[Vendor/Person]:** [What we need] — ETA: [Date]

### Providing To (Internal/External)
- **[Team/Person]:** [What we're delivering] — Due: [Date]

---

## Stakeholder Communication

### Questions for Stakeholders
1. **Question:** [What you need clarification on]
   - **Context:** [Why this matters]
   - **Options:** [Potential paths forward]

### Decisions Needed
1. **Decision:** [What needs to be decided]
   - **By When:** [Deadline for decision]
   - **Impact if Delayed:** [Consequences of no decision]

### Feedback Requested
- **Topic:** [What you want feedback on]
  - **Artifact:** [Link to document/prototype]
  - **Due Date:** [When you need response]

---

## Lessons Learned (Optional)

### What Went Well This Week
- [Positive outcome or process that worked]
- [Something that exceeded expectations]

### What Could Be Improved
- [Challenge faced or inefficiency identified]
- [Process that needs refinement]

### Action Items for Improvement
- [ ] [Action to improve process] — Owner: [Name] — Due: [Date]

---

## Attachments & References

### Documents Updated This Week
- [[03-Sprints|Sprint Planning]] — Updated velocity tracking
- [[04-Procurement-Schedule|Procurement Schedule]] — Added new component orders
- [PCB Design Files] — v1.2 committed to git

### Photos/Diagrams
- [Link to image/diagram] — [Description]
- [Link to image/diagram] — [Description]

### External Links
- [JLCPCB Order Status] — [Tracking URL]
- [Mouser Order #12345] — [Tracking URL]

---

## Appendix: Detailed Metrics

### Velocity Tracking

| Sprint | Planned Points | Completed Points | Variance | Cumulative Velocity |
|--------|---------------|------------------|----------|---------------------|
| Pre-Sprint Week 1 | 5.7 | [X] | [+/-X] | [X] |
| Pre-Sprint Week 2 | 5.7 | [X] | [+/-X] | [X] |
| ... | ... | ... | ... | ... |

### Burndown Data (Copy for Charting)
```csv
Day,Ideal,Actual
Monday,[X],[Y]
Tuesday,[X],[Y]
Wednesday,[X],[Y]
Thursday,[X],[Y]
Friday,[X],[Y]
```

### Component Inventory

| Component | On Hand | Allocated | Available | Reorder Level | Status |
|-----------|---------|-----------|-----------|---------------|--------|
| STM32G474RET6 | 2 | 1 | 1 | 1 | 🟢 OK |
| CM5 Module | 2 | 1 | 1 | 1 | 🟢 OK |
| Load Cells | 4 | 4 | 0 | 2 | 🟡 Low |

---

## Report Distribution

**Primary Recipients:**
- Project Manager
- Technical Lead
- Stakeholders

**CC:**
- Team members
- Finance (if budget variance >10%)

**Filing:**
- Save as: `reports/Weekly-Status-YYYY-MM-DD.md`
- Link from: Project README or dashboard

---

## Sign-Off

**Prepared By:** [Your Name]
**Date:** [YYYY-MM-DD]
**Next Report Due:** [Next Friday Date]

**Approval (if required):**
- [ ] Project Manager: [Name] — [Date]
- [ ] Technical Lead: [Name] — [Date]

---

## Related Documentation

- [[03-Sprints|Sprint Planning]] — Current sprint details
- [[04-Procurement-Schedule|Procurement Schedule]] — Component ordering timeline
- [[05-Resource-Allocation|Resource Allocation]] — Team assignments and budget
- [[__init|Project Management Hub]] — Dashboard and overview

---

#epicura #status-report #weekly #project-tracking

**Template Version:** 1.0
**Last Updated:** 2026-02-15
**Status:** Template (Copy and customize for each week)
---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |