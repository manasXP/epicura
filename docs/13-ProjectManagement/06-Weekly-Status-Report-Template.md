---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Weekly Status Report Template

## 1. How to Use This Template

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

## 2. Executive Summary

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

## 3. Current Sprint/Phase Status

### 3.1 Active Sprint: [Sprint Name or Pre-Sprint Phase]
**Sprint Goal:** [One sentence describing the sprint objective]
**Sprint Dates:** [Start Date] to [End Date]
**Days Remaining:** [X] of [Y] days

### 3.2 Story Progress

| Story ID | Story Name | Points | Status | % Complete | Owner | Notes |
|----------|------------|--------|--------|------------|-------|-------|
| ST-XXX | [Story Name] | 8 | ✅ Done | 100% | [Name] | Completed [date] |
| ST-XXX | [Story Name] | 13 | 🔄 In Progress | 60% | [Name] | On track, minor delay |
| ST-XXX | [Story Name] | 5 | ⏸️ Blocked | 10% | [Name] | Waiting on [component/decision] |
| ST-XXX | [Story Name] | 3 | 📋 Not Started | 0% | [Name] | Planned for next week |

**Legend:** ✅ Done | 🔄 In Progress | ⏸️ Blocked | 📋 Not Started | ❌ Cancelled

### 3.3 Sprint Burndown

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

## 4. Accomplishments This Week

### 4.1 Completed Work

#### 4.1.1 [Achievement Title]
- **Story:** ST-XXX ([Story Name])
- **Description:** [What was accomplished]
- **Impact:** [Why this matters for the project]
- **Artifacts:** [Links to code commits, docs, test results]

#### 4.1.2 [Achievement Title]
- **Story:** ST-XXX ([Story Name])
- **Description:** [What was accomplished]
- **Impact:** [Why this matters for the project]
- **Artifacts:** [Links to code commits, docs, test results]

#### 4.1.3 [Achievement Title]
- **Story:** ST-XXX ([Story Name])
- **Description:** [What was accomplished]
- **Impact:** [Why this matters for the project]
- **Artifacts:** [Links to code commits, docs, test results]

### 4.2 Milestones Reached
- [ ] [Milestone Name] — [Date Achieved] ✅
- [ ] [Milestone Name] — [Planned Date: YYYY-MM-DD]

---

## 5. Resource Utilization

### 5.1 Team Capacity This Week

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

### 5.2 External Dependencies
- **Waiting On:** [What we're blocked by]
  - **Status:** [Vendor/person status]
  - **ETA:** [Expected resolution date]
  - **Impact:** [How this affects timeline]

---

## 6. Procurement & Components

### 6.1 Orders Placed This Week

| Item | Part Number | Qty | Supplier | Cost | Order Date | ETA | Status |
|------|-------------|-----|----------|------|------------|-----|--------|
| [Component] | [PN] | 2 | Mouser | $XX.XX | YYYY-MM-DD | YYYY-MM-DD | 🚚 Shipped |
| [Component] | [PN] | 5 | Digikey | $XX.XX | YYYY-MM-DD | YYYY-MM-DD | ⏳ Processing |

### 6.2 Components Received This Week
- ✅ [Component Name] (Qty: X) — Inspected and stored
- ✅ [Component Name] (Qty: X) — Integrated into build

### 6.3 Upcoming Orders (Next Week)
- [ ] [Component Name] — Week [X] ordering window — Budget: $XXX
- [ ] [Component Name] — Week [X] ordering window — Budget: $XXX

### 6.4 Procurement Issues
- ⚠️ **[Component Name]:** Out of stock at Mouser
  - **Impact:** Delays Sprint X by [Y] days
  - **Mitigation:** Ordered from Digikey backup supplier, +2 days delivery

---

## 7. Budget Status

### 7.1 Weekly Spend

| Category | This Week | Cumulative | Allocated | Remaining | % Used |
|----------|-----------|------------|-----------|-----------|--------|
| Labor | $[X,XXX] | $[XX,XXX] | $147,240 | $[XXX,XXX] | [XX]% |
| Materials | $[XXX] | $[X,XXX] | $2,256 | $[X,XXX] | [XX]% |
| Tools | $[XX] | $[XXX] | $200 | $[XXX] | [XX]% |
| Contingency | $[X] | $[XXX] | $14,970 | $[XX,XXX] | [X]% |
| **Total** | **$[X,XXX]** | **$[XX,XXX]** | **$164,666** | **$[XXX,XXX]** | **[XX]%** |

### 7.2 Budget Variance Analysis
- **Status:** 🟢 Under Budget | 🟡 On Budget | 🔴 Over Budget
- **Projected Overrun/Savings:** $[X,XXX] ([+/-]%)
- **Explanation:** [Why variance occurred, if significant]

### 7.3 Major Expenses This Week
1. **[Expense Name]:** $[XXX] — [Justification]
2. **[Expense Name]:** $[XXX] — [Justification]

---

## 8. Risks & Issues

### 8.1 Active Risks

| Risk ID | Risk Description | Probability | Impact | Status | Owner | Mitigation |
|---------|------------------|-------------|--------|--------|-------|------------|
| R-001 | PCB design errors | Medium | Critical | 🟡 Monitor | [Name] | Design reviews scheduled |
| R-002 | Component shortage (CM5) | Medium | Critical | 🔴 Active | [Name] | Ordered 2x backup units |
| R-003 | PID tuning difficulty | Low | Medium | 🟢 Mitigated | [Name] | Auto-tune method working |

**Risk Status Legend:** 🔴 Active (immediate action) | 🟡 Monitor | 🟢 Mitigated | ⚫ Closed

### 8.2 New Risks Identified This Week
1. **[Risk Title]**
   - **Probability:** High / Medium / Low
   - **Impact:** Critical / High / Medium / Low
   - **Description:** [What could go wrong]
   - **Mitigation Plan:** [What we'll do to prevent/reduce impact]

### 8.3 Closed Risks This Week
- ⚫ **[Risk Title]:** [Why risk is no longer applicable]

---

## 9. Issues & Blockers

### 9.1 Critical Issues (Immediate Action Required)

#### 9.1.1 Issue #1: [Issue Title]
- **Status:** 🔴 Critical
- **Discovered:** [Date]
- **Impact:** [How this affects timeline/deliverables]
- **Root Cause:** [What caused this issue]
- **Action Plan:**
  1. [Action item 1] — Owner: [Name] — Due: [Date]
  2. [Action item 2] — Owner: [Name] — Due: [Date]
- **ETA for Resolution:** [Date]

### 9.2 Active Blockers

| Blocker | Blocking Story | Impact | Owner | Status | ETA |
|---------|---------------|--------|-------|--------|-----|
| [Blocker description] | ST-XXX | Sprint delayed 2 days | [Name] | Working | YYYY-MM-DD |

### 9.3 Resolved Issues This Week
- ✅ **[Issue Title]:** Resolved on [Date] — [Brief explanation]

---

## 10. Technical Highlights

### 10.1 Code/Design Artifacts Produced
- **Git Commits:** [X] commits to [repo/branch]
  - Link: [GitHub/GitLab URL]
- **Documentation Updated:**
  - [Document name] — [Link]
- **Tests Written/Passed:**
  - [Test name]: [Pass/Fail] — [X/Y] test cases

### 10.2 Technical Decisions Made
1. **Decision:** [What was decided]
   - **Rationale:** [Why this decision was made]
   - **Alternatives Considered:** [What else was evaluated]
   - **Impact:** [How this affects architecture/timeline]

### 10.3 Design Reviews Completed
- **PCB Review:** Controller PCB schematic — [Pass/Fail with comments]
- **Code Review:** STM32 UART driver — Approved with minor changes

---

## 11. Testing & Validation

### 11.1 Tests Executed This Week

| Test | Type | Result | Issues Found | Notes |
|------|------|--------|--------------|-------|
| Power-on test (Controller PCB) | Integration | ✅ Pass | 0 | All rails within spec |
| UART loopback test | Unit | ✅ Pass | 0 | <5ms latency achieved |
| PID step response | Integration | ⚠️ Partial | 1 | Overshoot 15% (target: <10%) |

### 11.2 Quality Metrics
- **Test Coverage:** [XX]% (target: 80%)
- **Defect Density:** [X] bugs per 100 lines of code
- **Mean Time to Fix:** [X] hours average

---

## 12. Next Week Plan

### 12.1 Sprint Goal for Next Week
[One sentence describing what you aim to accomplish]

### 12.2 Planned Work

| Story ID | Story Name | Points | Owner | Key Tasks |
|----------|------------|--------|-------|-----------|
| ST-XXX | [Story Name] | 8 | [Name] | - Task 1<br>- Task 2<br>- Task 3 |
| ST-XXX | [Story Name] | 5 | [Name] | - Task 1<br>- Task 2 |

### 12.3 Key Activities
- **Monday:** [Activity or meeting]
- **Tuesday:** [Activity or meeting]
- **Wednesday:** [Mid-week checkpoint] — Sprint review if applicable
- **Thursday:** [Activity or meeting]
- **Friday:** [Activity or meeting] — Next status report due

### 12.4 Meetings & Reviews
- **Sprint Planning:** [Date/Time] — [Attendees]
- **Design Review:** [Date/Time] — [What's being reviewed]
- **Stakeholder Demo:** [Date/Time] — [What will be demonstrated]

### 12.5 Procurement Actions
- [ ] Order [Component X] by [Day of Week]
- [ ] Confirm shipment for [Component Y]
- [ ] Receive and inspect [Component Z]

---

## 13. Dependencies & Coordination

### 13.1 Waiting On (External)
- **[Vendor/Person]:** [What we need] — ETA: [Date]
- **[Vendor/Person]:** [What we need] — ETA: [Date]

### 13.2 Providing To (Internal/External)
- **[Team/Person]:** [What we're delivering] — Due: [Date]

---

## 14. Stakeholder Communication

### 14.1 Questions for Stakeholders
1. **Question:** [What you need clarification on]
   - **Context:** [Why this matters]
   - **Options:** [Potential paths forward]

### 14.2 Decisions Needed
1. **Decision:** [What needs to be decided]
   - **By When:** [Deadline for decision]
   - **Impact if Delayed:** [Consequences of no decision]

### 14.3 Feedback Requested
- **Topic:** [What you want feedback on]
  - **Artifact:** [Link to document/prototype]
  - **Due Date:** [When you need response]

---

## 15. Lessons Learned (Optional)

### 15.1 What Went Well This Week
- [Positive outcome or process that worked]
- [Something that exceeded expectations]

### 15.2 What Could Be Improved
- [Challenge faced or inefficiency identified]
- [Process that needs refinement]

### 15.3 Action Items for Improvement
- [ ] [Action to improve process] — Owner: [Name] — Due: [Date]

---

## 16. Attachments & References

### 16.1 Documents Updated This Week
- [[__Workspaces/Epicura/docs/13-ProjectManagement/sprints/__init|Sprint Planning]] — Updated velocity tracking
- [[04-Procurement-Schedule|Procurement Schedule]] — Added new component orders
- [PCB Design Files] — v1.2 committed to git

### 16.2 Photos/Diagrams
- [Link to image/diagram] — [Description]
- [Link to image/diagram] — [Description]

### 16.3 External Links
- [JLCPCB Order Status] — [Tracking URL]
- [Mouser Order #12345] — [Tracking URL]

---

## 17. Appendix: Detailed Metrics

### 17.1 Velocity Tracking

| Sprint | Planned Points | Completed Points | Variance | Cumulative Velocity |
|--------|---------------|------------------|----------|---------------------|
| Pre-Sprint Week 1 | 5.7 | [X] | [+/-X] | [X] |
| Pre-Sprint Week 2 | 5.7 | [X] | [+/-X] | [X] |
| ... | ... | ... | ... | ... |

### 17.2 Burndown Data (Copy for Charting)
```csv
Day,Ideal,Actual
Monday,[X],[Y]
Tuesday,[X],[Y]
Wednesday,[X],[Y]
Thursday,[X],[Y]
Friday,[X],[Y]
```

### 17.3 Component Inventory

| Component | On Hand | Allocated | Available | Reorder Level | Status |
|-----------|---------|-----------|-----------|---------------|--------|
| STM32G474RET6 | 2 | 1 | 1 | 1 | 🟢 OK |
| CM5 Module | 2 | 1 | 1 | 1 | 🟢 OK |
| Load Cells | 4 | 4 | 0 | 2 | 🟡 Low |

---

## 18. Report Distribution

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

## 19. Sign-Off

**Prepared By:** [Your Name]
**Date:** [YYYY-MM-DD]
**Next Report Due:** [Next Friday Date]

**Approval (if required):**
- [ ] Project Manager: [Name] — [Date]
- [ ] Technical Lead: [Name] — [Date]

---

## 20. Related Documentation

- [[__Workspaces/Epicura/docs/13-ProjectManagement/sprints/__init|Sprint Planning]] — Current sprint details
- [[04-Procurement-Schedule|Procurement Schedule]] — Component ordering timeline
- [[05-Resource-Allocation|Resource Allocation]] — Team assignments and budget
- [[__Workspaces/Epicura/docs/13-ProjectManagement/__init|Project Management Hub]] — Dashboard and overview

---

#epicura #status-report #weekly #project-tracking

**Template Version:** 1.0
**Last Updated:** 2026-02-15
**Status:** Template (Copy and customize for each week)
---

## 21. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |