---
tags: [epicura, project-management, epic, integration, validation, testing]
created: 2026-02-16
aliases: [INT Epic, Integration Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 4 stories across Sprints 11–12 |

# Epic: INT — Integration & Validation

Full system integration testing, safety certification testing, reliability endurance testing, and production readiness. This epic depends on all other epics and validates the complete Epicura system.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SYS — System Integration | 1 | 8 | 11 |
| SAF — Safety Certification | 1 | 5 | 11 |
| REL — Reliability Testing | 1 | 5 | 12 |
| LCH — Launch Readiness | 1 | 5 | 12 |
| **Total** | **4** | **~24** | |

---

## Phase 4 — Integration (Sprints 11–12)

### INT-SYS.01: Full system integration test — end-to-end autonomous cooking
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P0
- **Points:** 8
- **Blocked by:** [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]], [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]], [[UI-touchscreen#UI-COK.01|UI-COK.01]], [[THR-thermal#THR-PID.01|THR-PID.01]], [[ARM-actuation#ARM-SRV.01|ARM-SRV.01]]
- **Blocks:** [[INT-integration#INT-REL.01|INT-REL.01]], [[EMB-embedded#EMB-LCH.01|EMB-LCH.01]]

**Acceptance Criteria:**
- [ ] Cook 3 recipes autonomously end-to-end: dal tadka, rice, khichdi
- [ ] Each cook completes without manual intervention (except ingredient loading)
- [ ] Temperature control within ±10°C of recipe targets throughout cooking
- [ ] All 3 dispensing subsystems (P-ASD, CID, SLD) dispense within ±15% accuracy
- [ ] CV correctly identifies at least 4 of 6 cooking stages per recipe
- [ ] UI displays correct status, camera feed, and controls throughout
- [ ] Cook session data logged to PostgreSQL with complete telemetry
- [ ] No safety faults triggered during normal operation

**Tasks:**
- [ ] `INT-SYS.01a` — Set up integration test environment: load ingredients, calibrate dispensers
- [ ] `INT-SYS.01b` — Execute dal tadka recipe: record all telemetry, note deviations
- [ ] `INT-SYS.01c` — Execute rice recipe: verify water dispensing accuracy and boil detection
- [ ] `INT-SYS.01d` — Execute khichdi recipe: verify multi-ingredient dispensing sequence
- [ ] `INT-SYS.01e` — Analyze telemetry data: temperature accuracy, dispensing accuracy, timing
- [ ] `INT-SYS.01f` — Document integration test results and create issue tickets for failures

---

### INT-SAF.01: Safety certification testing — IEC 60335, food safety, BIS
- **Sprint:** [[sprint-11|Sprint 11]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SAF.01|EMB-SAF.01]], [[THR-thermal#THR-SAF.01|THR-SAF.01]]
- **Blocks:** [[INT-integration#INT-LCH.01|INT-LCH.01]]

**Acceptance Criteria:**
- [ ] E-stop test: press e-stop during cooking → all actuators off within 100ms, heat off within 500ms
- [ ] Thermal runaway test: simulate sensor failure → system shuts down safely
- [ ] Watchdog test: freeze STM32 main loop → safety relay opens within 600ms
- [ ] Power surge test: 10% overvoltage for 5 minutes → no component damage
- [ ] Food contact materials verified: stainless steel pot, food-grade silicone, FDA-approved tubing
- [ ] IEC 60335-1 (household appliances) checklist completed for prototype
- [ ] All safety test results documented with pass/fail and evidence

**Tasks:**
- [ ] `INT-SAF.01a` — Execute e-stop test: time from press to all-off across 10 trials
- [ ] `INT-SAF.01b` — Execute thermal runaway test: disconnect IR sensor, verify shutdown
- [ ] `INT-SAF.01c` — Execute watchdog test: halt STM32 via debugger, verify safety relay timing
- [ ] `INT-SAF.01d` — Execute power surge test: use variable transformer for overvoltage
- [ ] `INT-SAF.01e` — Verify food contact material certifications and documentation
- [ ] `INT-SAF.01f` — Complete IEC 60335-1 prototype compliance checklist

---

### INT-REL.01: Reliability testing — 100-hour endurance, MTBF estimation
- **Sprint:** [[sprint-12|Sprint 12]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[INT-integration#INT-SYS.01|INT-SYS.01]]
- **Blocks:** [[INT-integration#INT-LCH.01|INT-LCH.01]]

**Acceptance Criteria:**
- [ ] 100-hour continuous operation test: cycle through 3 recipes repeatedly
- [ ] No component failures or degradation during test period
- [ ] Servo arm: no position drift after 1000 cycles
- [ ] Dispensing accuracy: no degradation after 500 dispense cycles
- [ ] Temperature control: no PID drift or sensor calibration shift
- [ ] System uptime >99.5% (total unplanned downtime <30 minutes in 100 hours)
- [ ] All failures documented with root cause analysis

**Tasks:**
- [ ] `INT-REL.01a` — Design endurance test plan: recipe cycle sequence, monitoring points
- [ ] `INT-REL.01b` — Set up automated test runner: cycle through recipes with logging
- [ ] `INT-REL.01c` — Monitor and log: sensor readings, actuator currents, CPU/memory usage
- [ ] `INT-REL.01d` — At 25h/50h/75h/100h checkpoints: measure dispensing accuracy, servo position, temp calibration
- [ ] `INT-REL.01e` — Compile reliability report: MTBF estimate, failure modes, recommendations

---

### INT-LCH.01: Production readiness — documentation, packaging, launch checklist
- **Sprint:** [[sprint-12|Sprint 12]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[INT-integration#INT-SAF.01|INT-SAF.01]], [[INT-integration#INT-REL.01|INT-REL.01]], [[EMB-embedded#EMB-LCH.01|EMB-LCH.01]], [[EMB-embedded#EMB-OTA.01|EMB-OTA.01]], [[BE-backend#BE-LCH.01|BE-LCH.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] User manual created: setup, first cook, ingredient loading, cleaning, troubleshooting
- [ ] Manufacturing BOM finalized with verified suppliers and lead times
- [ ] Factory provisioning process documented and tested on 3 units
- [ ] Cloud backend in production: API, database, MQTT broker operational
- [ ] Mobile apps submitted to TestFlight and Play internal testing
- [ ] All safety certifications documented and filed
- [ ] Launch checklist completed: 100% items checked off

**Tasks:**
- [ ] `INT-LCH.01a` — Write user manual with diagrams: setup, ingredient loading, first cook, cleaning
- [ ] `INT-LCH.01b` — Finalize manufacturing BOM with verified alternates for unavailable parts
- [ ] `INT-LCH.01c` — Test factory provisioning on 3 prototype units: flash, calibrate, test, package
- [ ] `INT-LCH.01d` — Verify cloud backend production deployment: health checks, monitoring
- [ ] `INT-LCH.01e` — Submit iOS to TestFlight and Android to Play internal track
- [ ] `INT-LCH.01f` — Execute final launch checklist; sign off on all items

---

## Dependencies

### What INT blocks

| INT Story | Blocks | Reason |
|-----------|--------|--------|
| INT-SYS.01 | INT-REL.01, EMB-LCH.01 | Integration tests must pass before reliability and production firmware |
| INT-SAF.01 | INT-LCH.01 | Safety certification required for launch |
| INT-REL.01 | INT-LCH.01 | Reliability validation required for launch |

### What blocks INT

| INT Story | Blocked by | Reason |
|-----------|------------|--------|
| INT-SYS.01 | RCP-FSM.01, RCP-DSP.01, UI-COK.01, THR-PID.01, ARM-SRV.01 | Needs all subsystems working |
| INT-SAF.01 | EMB-SAF.01, THR-SAF.01 | Needs safety systems implemented |
| INT-REL.01 | INT-SYS.01 | Needs integration tests passing |
| INT-LCH.01 | INT-SAF.01, INT-REL.01, EMB-LCH.01, EMB-OTA.01, BE-LCH.01 | Needs everything complete |

---

## References

- [[__Workspaces/Epicura/docs/06-Compliance/01-Safety-Compliance|Safety & Compliance]]
- [[__Workspaces/Epicura/docs/07-Development/01-Prototype-Development-Plan|Prototype Development Plan]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
