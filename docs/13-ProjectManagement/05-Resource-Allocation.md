---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Resource Allocation & Gantt Chart

## Overview

This document provides detailed resource allocation across all project phases, including the critical Pre-Sprint PCB Development Phase. It shows personnel assignments, workload distribution, and identifies potential bottlenecks.

**Project Duration:** 30 weeks total (6 weeks pre-sprint + 24 weeks sprints)
**Target Team Size:** 1-3 developers (variable based on sprint requirements)

---

## Personnel Roles & Hourly Rates

| Role | Skills Required | Hourly Rate (USD) | Availability Model |
|------|----------------|-------------------|-------------------|
| **PCB Design Engineer** | KiCad/Altium, STM32, power electronics | $75-120/hr | Contract (4 weeks) |
| **Embedded Developer** | C, FreeRTOS, STM32 HAL, Yocto | $60-100/hr | Full-time (24 weeks) |
| **Mechanical Engineer** | CAD (Fusion 360), 3D printing, fabrication | $50-80/hr | Part-time (8 weeks) |
| **ML/CV Engineer** | Python, TensorFlow, OpenCV, data labeling | $70-110/hr | Full-time (4 weeks) |
| **Frontend Developer** | Kivy, Python, UI/UX design | $55-90/hr | Full-time (4 weeks) |
| **Backend Developer** | Python, Flask/FastAPI, REST API, MQTT | $60-95/hr | Full-time (2 weeks) |
| **Mobile Developer** | Flutter, Dart, REST integration | $60-95/hr | Full-time (2 weeks) |
| **QA/Test Engineer** | Safety testing, reliability analysis, documentation | $45-70/hr | Full-time (4 weeks) |
| **Cook/Lab Assistant** | Food prep, data collection, taste testing | $20-30/hr | Part-time (12 weeks) |

---

## Pre-Sprint Phase: PCB Development (Weeks -6 to 0)

### Week -6 to Week -3: PCB Design

| Week | PCB Engineer | Embedded Dev | Power Engineer | Total Person-Weeks |
|------|--------------|--------------|----------------|-------------------|
| -6 | 100% (Controller schematic) | 20% (pin review) | 20% (power review) | 1.4 |
| -5 | 100% (Driver schematic) | 20% (review) | 40% (buck converter design) | 1.6 |
| -4 | 100% (CM5IO design) | 30% (CM5 integration review) | 10% (final review) | 1.4 |
| -3 | 100% (PCB layout all 3 boards) | 10% (DRC review) | 10% (thermal review) | 1.2 |
| **Subtotal** | **4.0 weeks** | **0.8 weeks** | **0.8 weeks** | **5.6 weeks** |

**Deliverables:**
- Controller PCB schematic + layout (KiCad files)
- Driver PCB schematic + layout (KiCad files)
- CM5IO PCB schematic + layout (KiCad files)
- Gerber files for JLCPCB submission
- BOM with part numbers (Mouser/Digikey)
- Assembly drawings

**Key Milestone:** PCB order submitted to JLCPCB by end of Week -6 (start of Week -3 design phase)

---

### Week -3 to Week 0: PCB Fabrication & Testing

| Week | PCB Engineer | Embedded Dev | Mechanical Eng | Total Person-Weeks |
|------|--------------|--------------|----------------|-------------------|
| -3 | 20% (JLCPCB liaison) | 40% (test plan) | - | 0.6 |
| -2 | 10% (Q&A with fab) | 60% (Yocto build setup) | 20% (mount design) | 0.9 |
| -1 | 30% (PCB receiving/inspection) | 100% (power-on testing) | 40% (test fixture) | 1.7 |
| 0 | 20% (rework support) | 100% (bring-up debug) | - | 1.2 |
| **Subtotal** | **0.8 weeks** | **3.0 weeks** | **0.6 weeks** | **4.4 weeks** |

**Deliverables:**
- Assembled PCBs (10x Controller, 10x Driver, 5x CM5IO)
- Power-on test reports
- Continuity and short-circuit checks passed
- STM32 SWD connectivity verified
- Yocto minimal image booting on CM5

**Key Milestone:** All 3 PCB types powered and basic I/O verified by Week 0 (Sprint 1 start)

---

## Sprint-by-Sprint Resource Allocation

### Sprint 1 (Weeks 1-2): Foundation

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Embedded Developer | 100% | Yocto image build, STM32 FreeRTOS setup, UART protocol | 40 |
| PCB Engineer | 10% (consult) | Debug PCB issues if any | 4 |

**Total:** 1.1 person-weeks per week × 2 weeks = **2.2 person-weeks**

---

### Sprint 2 (Weeks 3-4): Power & Thermal Setup

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Embedded Developer | 100% | Power distribution, CAN bus integration, MLX90614 I2C | 40 |
| Power Engineer | 20% (consult) | Review power rail stability, voltage ripple | 8 |

**Total:** 1.2 person-weeks per week × 2 weeks = **2.4 person-weeks**

---

### Sprint 3 (Weeks 5-6): Thermal Control - PID & Safety

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Embedded Developer | 100% | PID controller, safety interlocks, NTC integration | 40 |
| Cook/Lab Assistant | 20% | Water boil tests, temperature logging | 8 |

**Total:** 1.2 person-weeks per week × 2 weeks = **2.4 person-weeks**

---

### Sprint 4 (Weeks 7-8): Robotic Arm

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Mechanical Engineer | 100% | Servo arm CAD, 3D printing, assembly | 40 |
| Embedded Developer | 50% | Servo PWM patterns, torque limiting | 20 |
| Cook/Lab Assistant | 10% | Stirring pattern testing in water/dal | 4 |

**Total:** 1.6 person-weeks per week × 2 weeks = **3.2 person-weeks**

---

### Sprint 5 (Weeks 9-10): Load Cells

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Embedded Developer | 80% | HX711 integration, calibration, weight-based control | 32 |
| Mechanical Engineer | 60% | Load cell platform fabrication, mounting | 24 |

**Total:** 1.4 person-weeks per week × 2 weeks = **2.8 person-weeks**

---

### Sprint 6 (Weeks 11-12): Computer Vision - Camera Setup

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| ML/CV Engineer | 100% | Camera setup, lighting, preprocessing pipeline | 40 |
| Embedded Developer | 30% | libcamera integration, GStreamer setup | 12 |
| Mechanical Engineer | 20% | Camera mount design and fabrication | 8 |

**Total:** 1.5 person-weeks per week × 2 weeks = **3.0 person-weeks**

---

### Sprint 7 (Weeks 13-14): CV Training & Deployment

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| ML/CV Engineer | 100% | Data labeling, model training, TFLite conversion | 40 |
| Cook/Lab Assistant | 100% | Cook 20 dishes, capture images, assist labeling | 40 |
| Embedded Developer | 20% | TFLite runtime integration on CM5 | 8 |

**Total:** 2.2 person-weeks per week × 2 weeks = **4.4 person-weeks**

---

### Sprint 8 (Weeks 15-16): Recipe State Machine

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Embedded Developer | 80% | Recipe YAML parser, state machine engine, asyncio | 32 |
| Backend Developer | 40% | Recipe schema design, validation logic | 16 |

**Total:** 1.2 person-weeks per week × 2 weeks = **2.4 person-weeks**

---

### Sprint 9 (Weeks 17-18): Dispensing & UI

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Mechanical Engineer | 100% | Dispensing tray CAD, 3D printing, gate calibration | 40 |
| Embedded Developer | 60% | SG90 control, weight-based dispensing logic | 24 |
| Frontend Developer | 80% | Kivy UI screens (start) | 32 |
| Cook/Lab Assistant | 30% | Recipe testing (3 minimum recipes) | 12 |

**Total:** 2.7 person-weeks per week × 2 weeks = **5.4 person-weeks**

---

### Sprint 10 (Weeks 19-20): UI & API

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Frontend Developer | 100% | Kivy touchscreen UI completion, camera widget | 40 |
| Backend Developer | 100% | Flask REST API, MQTT telemetry | 40 |
| Mobile Developer | 100% | Flutter app (discovery, browse, live view) | 40 |
| Embedded Developer | 30% | API integration with recipe engine | 12 |

**Total:** 3.3 person-weeks per week × 2 weeks = **6.6 person-weeks**

---

### Sprint 11 (Weeks 21-22): Integration Part 1

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| Embedded Developer | 100% | Full system integration, subsystem testing | 40 |
| Mechanical Engineer | 60% | Enclosure assembly, cable management | 24 |
| Frontend Developer | 40% | UI polish, WiFi pairing flow | 16 |
| Cook/Lab Assistant | 100% | Cook 25 sessions (5 recipes × 5 iterations) | 40 |

**Total:** 3.0 person-weeks per week × 2 weeks = **6.0 person-weeks**

---

### Sprint 12 (Weeks 23-24): Integration Part 2

| Role | Allocation | Tasks | Hours/Week |
|------|------------|-------|------------|
| QA/Test Engineer | 100% | Safety testing, reliability testing, reporting | 40 |
| Embedded Developer | 60% | Bug fixes, performance tuning | 24 |
| Cook/Lab Assistant | 100% | 50+ endurance cook cycles | 40 |
| Technical Writer | 50% | Prototype report, assembly docs | 20 |

**Total:** 3.1 person-weeks per week × 2 weeks = **6.2 person-weeks**

---

## Gantt Chart (Text-Based)

```
Timeline (Weeks): -6  -5  -4  -3  -2  -1   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24

PHASES:
Pre-Sprint (PCB)  [████████████████████████]
Sprint 1-2        |                         [████████████]
Sprint 3-4        |                                      [████████████████]
Sprint 5-6        |                                                      [████████████████]
Sprint 7-8        |                                                                      [████████████████]
Sprint 9-10       |                                                                                      [████████████████]
Sprint 11-12      |                                                                                                      [████████████████]

ROLES:

PCB Engineer      [████████]                |
Embedded Dev      [██  ████████████████████████████████████████████████████████████████████████████████████████████████]
Mechanical Eng    [  ░░]                    |           [████████]    [████]        [██]        [████]        [████]
ML/CV Engineer    |                                                            [████████████████]
Frontend Dev      |                                                                                  [████████████████████]
Backend Dev       |                                                                      [████][████████]
Mobile Dev        |                                                                                  [████████]
QA/Test Eng       |                                                                                                  [████████]
Cook/Assistant    |                              [░░]    [░░]        [██]        [████████████]    [████████]    [████]    [████████]

Legend:
████ = Full-time (100%)
████ = 80%+
████ = 60-80%
░░░░ = 20-40%
░░░░ = <20%
```

---

## Detailed Resource Timeline

### Pre-Sprint Phase (Weeks -6 to 0)

| Week | PCB Eng | Embed Dev | Mech Eng | Power Eng | Total FTE |
|------|---------|-----------|----------|-----------|-----------|
| -6 | 100% | 20% | - | 20% | 1.40 |
| -5 | 100% | 20% | - | 40% | 1.60 |
| -4 | 100% | 30% | - | 10% | 1.40 |
| -3 | 100% | 10% | - | 10% | 1.20 |
| -2 | 20% | 40% | 20% | - | 0.80 |
| -1 | 10% | 60% | 20% | - | 0.90 |
| 0 | 30% | 100% | 40% | - | 1.70 |
| **Avg** | **66%** | **40%** | **11%** | **11%** | **1.29 FTE** |

---

### Sprint Phase (Weeks 1-24)

| Sprint | Week | Embed | Mech | ML/CV | Front | Back | Mobile | QA | Cook | Total FTE |
|--------|------|-------|------|-------|-------|------|--------|-----|------|-----------|
| 1 | 1-2 | 100% | - | - | - | - | - | - | - | 1.00 |
| 2 | 3-4 | 100% | - | - | - | - | - | - | - | 1.00 |
| 3 | 5-6 | 100% | - | - | - | - | - | - | 20% | 1.20 |
| 4 | 7-8 | 50% | 100% | - | - | - | - | - | 10% | 1.60 |
| 5 | 9-10 | 80% | 60% | - | - | - | - | - | - | 1.40 |
| 6 | 11-12 | 30% | 20% | 100% | - | - | - | - | - | 1.50 |
| 7 | 13-14 | 20% | - | 100% | - | - | - | - | 100% | 2.20 |
| 8 | 15-16 | 80% | - | - | - | 40% | - | - | - | 1.20 |
| 9 | 17-18 | 60% | 100% | - | 80% | - | - | - | 30% | 2.70 |
| 10 | 19-20 | 30% | - | - | 100% | 100% | 100% | - | - | 3.30 |
| 11 | 21-22 | 100% | 60% | - | 40% | - | - | - | 100% | 3.00 |
| 12 | 23-24 | 60% | - | - | - | - | - | 100% | 100% | 2.60 |
| **Avg** | | **68%** | **28%** | **17%** | **18%** | **12%** | **8%** | **8%** | **30%** | **1.88 FTE** |

---

## Peak Resource Demand Analysis

### Highest Staffing Requirements

| Period | Total FTE | Roles Needed | Cost/Week | Bottleneck Risk |
|--------|-----------|--------------|-----------|-----------------|
| **Sprint 10 (Weeks 19-20)** | **3.30** | Embed (30%), Front (100%), Back (100%), Mobile (100%) | $7,920 | High - 3 concurrent UI developers |
| **Sprint 11 (Weeks 21-22)** | **3.00** | Embed (100%), Mech (60%), Front (40%), Cook (100%) | $6,400 | Medium - Integration bottleneck |
| **Sprint 12 (Weeks 23-24)** | **2.60** | Embed (60%), QA (100%), Cook (100%) | $4,800 | Low - Testing phase |
| **Sprint 9 (Weeks 17-18)** | **2.70** | Embed (60%), Mech (100%), Front (80%), Cook (30%) | $6,080 | Medium - Dispensing + UI overlap |
| **Sprint 7 (Weeks 13-14)** | **2.20** | Embed (20%), ML/CV (100%), Cook (100%) | $5,200 | Medium - Data collection intensive |

**Critical Insight:** Sprint 10 requires 3.3 FTE with 3 specialized developers (frontend, backend, mobile) working concurrently. This is the project's resource peak.

---

## Resource Optimization Strategies

### Strategy 1: Serial UI Development (Reduces Peak to 2.3 FTE)

**Current Plan (Sprint 10):**
- Frontend (100%) + Backend (100%) + Mobile (100%) = 3.0 FTE UI work

**Optimized Plan:**
- Sprint 9: Frontend 100% + Backend 50% = 1.5 FTE
- Sprint 10: Frontend 50% (polish) + Backend 100% + Mobile 100% = 2.5 FTE
- Sprint 11: Mobile 50% (polish) + Frontend 20% (WiFi pairing) = 0.7 FTE

**Pros:** Reduces peak staffing, smoother cash flow
**Cons:** Extends UI work across 3 sprints, delays mobile app readiness

---

### Strategy 2: Outsource Mobile App (Flutter)

**Approach:** Contract mobile app to external Flutter agency for fixed bid.

**Cost Estimate:** $4,000-6,000 for MVP (4 screens, API integration, tested)
**Timeline:** 3-4 weeks (Weeks 17-20, runs parallel to Sprint 9-10)
**Savings:** Eliminates 2 weeks × 40 hrs = 80 hrs × $75/hr = $6,000 in-house cost
**Net Impact:** Break-even or slight savings, reduces internal coordination overhead

---

### Strategy 3: Part-Time Cook/Assistant

**Current Plan:** 100% during Sprint 7, 11, 12
**Optimized Plan:** 20 hrs/week across Weeks 13-24 (12 weeks)

**Total Hours:** Same (240 hrs), but spread over longer period
**Benefit:** More flexible scheduling, better ingredient procurement, iterative testing
**Risk:** Slower feedback loops during data collection phase

---

## Labor Cost Estimates

### Pre-Sprint Phase (Weeks -6 to 0)

| Role | Total Hours | Rate/Hr | Total Cost |
|------|-------------|---------|------------|
| PCB Engineer | 160 hrs (4 weeks × 40) | $90 | $14,400 |
| Embedded Developer | 120 hrs (3 weeks × 40) | $80 | $9,600 |
| Mechanical Engineer | 24 hrs (0.6 weeks × 40) | $65 | $1,560 |
| Power Engineer (consult) | 32 hrs (0.8 weeks × 40) | $100 | $3,200 |
| **Subtotal** | **336 hrs** | | **$28,760** |

---

### Sprint Phase (Weeks 1-24)

| Role | Total Weeks | Avg % | Total Hours | Rate/Hr | Total Cost |
|------|-------------|-------|-------------|---------|------------|
| Embedded Developer | 24 weeks | 68% | 653 hrs | $80 | $52,240 |
| Mechanical Engineer | 8 weeks (4 sprints) | 70% avg | 224 hrs | $65 | $14,560 |
| ML/CV Engineer | 4 weeks (2 sprints) | 60% avg | 96 hrs | $90 | $8,640 |
| Frontend Developer | 6 weeks (3 sprints) | 73% avg | 176 hrs | $75 | $13,200 |
| Backend Developer | 4 weeks (2 sprints) | 70% avg | 112 hrs | $80 | $8,960 |
| Mobile Developer | 2 weeks (1 sprint) | 100% | 80 hrs | $75 | $6,000 |
| QA/Test Engineer | 4 weeks (2 sprints) | 80% avg | 128 hrs | $60 | $7,680 |
| Cook/Lab Assistant | 12 weeks (scattered) | 60% avg | 288 hrs | $25 | $7,200 |
| **Subtotal** | | | **1,757 hrs** | | **$118,480** |

---

### Total Project Labor Cost

| Phase | Hours | Cost |
|-------|-------|------|
| Pre-Sprint PCB Development | 336 | $28,760 |
| Sprint 1-12 Execution | 1,757 | $118,480 |
| **Total** | **2,093 hrs** | **$147,240** |

---

## Budget Summary (Labor + Materials)

| Category | Cost | % of Total |
|----------|------|------------|
| **Labor** | $147,240 | 85% |
| **Materials & Components** | $2,256 | 13% |
| **Tools & Equipment** | $200 | 1% |
| **Contingency (10%)** | $14,970 | 8.6% |
| **Total Project Budget** | **$164,666** | **100%** |

> **Note:** This assumes market-rate contractors. For in-house team or lower-cost regions, labor costs can be reduced by 30-50%.

---

## Team Composition Recommendations

### Option 1: Solo Developer (Extended Timeline)

**Team:**
- 1 × Full-stack embedded/software developer (all roles except mechanical)
- Contract mechanical work as needed (Weeks 4-5, 9, 11)

**Timeline:** 36-40 weeks (50% longer)
**Cost:** ~$80,000 labor + $2,500 materials = **$82,500**
**Pros:** Lowest cost, single point of accountability
**Cons:** Longer timeline, knowledge silos, burnout risk

---

### Option 2: Core Team of 2 (Recommended)

**Team:**
- 1 × Embedded developer (full-time, Weeks -2 to 24)
- 1 × Full-stack developer (ML/CV → Frontend → Backend, Weeks 11-20)
- Contract specialists: PCB engineer (Weeks -6 to -3), Mechanical (part-time)

**Timeline:** 26 weeks (24 sprints + 2 week PCB buffer)
**Cost:** ~$95,000 labor + $2,500 materials = **$97,500**
**Pros:** Balanced cost/speed, knowledge sharing, parallel work
**Cons:** Requires coordination, some waiting for specialists

---

### Option 3: Full Team (Fastest)

**Team:**
- 1 × Embedded developer (Weeks -2 to 24)
- 1 × Mechanical engineer (part-time, Weeks -1, 4-5, 9, 11, 17-18)
- 1 × ML/CV engineer (Weeks 11-14)
- 1 × Frontend developer (Weeks 17-22)
- 1 × Backend developer (Weeks 15-16, 19-20)
- 1 × Mobile developer (Weeks 19-20)
- Contract PCB engineer (Weeks -6 to -3)

**Timeline:** 24 weeks (as planned)
**Cost:** ~$147,000 labor + $2,500 materials = **$149,500**
**Pros:** Fastest time-to-market, specialist expertise, lowest technical risk
**Cons:** Highest cost, coordination overhead

---

## Critical Path & Dependencies

### Sequential Dependencies (Cannot Parallelize)

```
Week -6: PCB Design Complete
   ↓ (3 weeks - JLCPCB fab)
Week -3: PCBs Ship
   ↓ (1 week - customs/delivery)
Week -2: PCBs Arrive → Power-On Testing
   ↓ (2 weeks - bring-up)
Week 0: Sprint 1 Starts (Foundation)
   ↓ (2 weeks)
Week 2: Sprint 2 (Power & CAN Integration) ← Blocked until Sprint 1 UART works
   ↓ (2 weeks)
Week 4: Sprint 3 (PID Control) ← Blocked until CAN + sensors work
   ↓ (Sprints 4-7 can partially parallelize)
Week 14: Sprint 8 (Recipe Engine) ← Blocked until CV model deployed
   ↓
Week 18: Sprint 9 (Dispensing) ← Blocked until recipe engine works
   ↓
Week 20: Sprint 10 (UI/API) ← Blocked until state machine reliable
   ↓
Week 22: Sprint 11 (Integration) ← All subsystems must be complete
   ↓
Week 24: Sprint 12 (Validation) ← Integration complete
```

**Critical Path Items:**
1. PCB fabrication (Week -6 to -2): 4 weeks → **Cannot compress**
2. CM5 procurement (Week -4 to -1): 3 weeks → **Order immediately**
3. Induction surface (Week -2 to +2): 4 weeks → **Order immediately**
4. CV model training (Sprint 7): 2 weeks → **Cannot compress** (data collection time)
5. Recipe testing (Sprint 9): 2 weeks → **Cannot compress** (cook time + iterations)

---

## Risk Mitigation - Resource Bottlenecks

### Risk 1: PCB Engineer Unavailable

**Probability:** Medium (specialized skill)
**Impact:** High (blocks entire project)

**Mitigation:**
- Contract 2-3 PCB engineers for quotes during Week -8
- Have backup: Use Nucleo dev boards + breakout PCBs (add 4 weeks to timeline)
- Consider PCB design services (JLCPCB offers design service ~$500-800 per board)

---

### Risk 2: Embedded Developer Leaves Mid-Project

**Probability:** Low-Medium
**Impact:** Critical (single point of failure)

**Mitigation:**
- Document all design decisions in git commits + wiki
- Weekly knowledge-sharing sessions with mechanical/ML engineers
- Contract backup embedded developer on retainer ($1,000/month) for emergency coverage

---

### Risk 3: ML/CV Model Fails to Achieve Accuracy

**Probability:** Medium (new dataset, unproven approach)
**Impact:** High (blocks recipe automation)

**Mitigation:**
- Sprint 7 includes rule-based fallback (color thresholds + temperature)
- Allocate 1 extra week buffer after Sprint 7 for model iteration
- If accuracy <70% after Sprint 7, pivot to timer-based recipe execution (removes CV dependency)

---

### Risk 4: Component Shortages (CM5, STM32, DRV8876)

**Probability:** Medium (ongoing chip shortage)
**Impact:** High (blocks sprints)

**Mitigation:**
- Order 2x critical components immediately (Week -8)
- Identify drop-in replacements: STM32G474 → STM32F446, DRV8876 → L298N (lower performance)
- Monitor stock levels weekly on Mouser/Digikey

---

## Deliverables by Phase

### Pre-Sprint Phase Deliverables (Week 0)
- [ ] Controller PCB (10 pcs) assembled and powered
- [ ] Driver PCB (10 pcs) assembled and powered
- [ ] CM5IO PCB (5 pcs) assembled and powered
- [ ] Yocto minimal image booting on CM5
- [ ] STM32 FreeRTOS blinking LED on all Controller PCBs
- [ ] Complete BOM with Mouser/Digikey part numbers
- [ ] PCB design files (KiCad) in git repository

---

### Sprint Deliverables (Week 24)
- [ ] 5 recipes cook successfully end-to-end
- [ ] Touchscreen UI functional (5 core screens)
- [ ] Mobile app deployed (Android APK)
- [ ] Safety interlocks tested and documented
- [ ] 50+ cook cycle endurance test complete
- [ ] Prototype report published
- [ ] Assembly documentation with photos
- [ ] Known issues tracker

---

## Resource Allocation Tools

### Recommended Project Management Tools

**For Small Team (1-2 people):**
- **Trello** or **Notion**: Sprint boards, task tracking (free tier sufficient)
- **Git + GitHub/GitLab**: Code, docs, PCB files (free for public repos)
- **Google Sheets**: BOM tracking, procurement schedule (free)

**For Larger Team (3+ people):**
- **GitHub Issues**: Bug tracking and task management, linked to story IDs (free)
- **GitHub Projects**: Kanban boards for sprint planning — one board per sprint (free)
- **Slack**: Team communication (free tier OK)

**Time Tracking:**
- **Toggl Track**: Time tracking per task (free for solo, $10/user/month team)
- **Harvest**: Invoicing + time tracking ($12/user/month)

---

## Weekly Status Report Template

```markdown
# Epicura Weekly Status - Week X

## Sprint: [Sprint Name]

### Completed This Week
- [ ] Task 1 (8 story points)
- [ ] Task 2 (5 story points)

### In Progress
- [ ] Task 3 (13 story points) - 60% complete

### Blocked
- [ ] Task 4 - waiting on component delivery (ETA: Week X+1)

### Resource Utilization
| Role | Planned % | Actual % | Variance |
|------|-----------|----------|----------|
| Embedded Dev | 100% | 85% | -15% (sick day Wed) |
| Mechanical Eng | 60% | 70% | +10% (extra iteration) |

### Budget Status
- Spent this week: $X,XXX
- Cumulative spend: $X,XXX / $164,666 budget
- Projected variance: +/- $X,XXX

### Risks & Issues
1. **Issue:** PCB connector J3 intermittent contact
   - **Impact:** Sprint 2 delayed 1 day
   - **Mitigation:** Ordered replacement connectors, arriving Friday

### Next Week Plan
- Complete ST-004 (Power Distribution)
- Begin ST-005 (CAN Integration)
- Order Sprint 3 components (NTC, thermal fuse)
```

---

## Related Documentation

- [[03-Sprints|Sprint Planning]]
- [[02-Stories|User Stories]]
- [[04-Procurement-Schedule|Procurement Schedule]]
- [[01-Epics|Project Epics]]
- [[../07-Development/01-Prototype-Development-Plan|Prototype Development Plan]]

---

#epicura #resource-allocation #gantt #project-management #staffing #budget

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
