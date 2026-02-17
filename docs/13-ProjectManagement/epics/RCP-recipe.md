---
tags: [epicura, project-management, epic, recipe, state-machine]
created: 2026-02-16
aliases: [RCP Epic, Recipe Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 4 stories across Sprints 8–9 |
> | 2026-02-17 | Manas Pradhan | Split RCP-FSM.01 (10pts) → FSM.01+FSM.02 (5+5); split RCP-DSP.01 (8pts) → DSP.01+DSP.02 (5+3); total 6 stories |

# Epic: RCP — Recipe Engine & State Machine

YAML recipe format, cooking state machine, dispensing orchestration, and cloud recipe sync. The recipe engine is the central orchestrator that coordinates thermal control, arm movement, dispensing, and vision feedback.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| FMT — Recipe Format | 1 | 5 | 8 |
| FSM — State Machine | 2 | 10 | 8–9 |
| DSP — Dispensing Orchestration | 2 | 8 | 9 |
| SYN — Cloud Sync | 1 | 5 | 9 |
| **Total** | **6** | **~28** | |

---

## Phase 3 — Recipe Engine (Sprints 8–9)

### RCP-FMT.01: YAML recipe format — schema definition, parser, validation
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.02|EMB-SET.02]], [[EMB-embedded#EMB-SET.03|EMB-SET.03]]
- **Blocks:** [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]], [[BE-backend#BE-RCP.01|BE-RCP.01]]

**Acceptance Criteria:**
- [ ] YAML schema defined: metadata (name, cuisine, servings, time), ingredients (type, dispenser, amount, unit), steps (action, params, duration, conditions)
- [ ] Python parser loads and validates YAML against schema (jsonschema or pydantic)
- [ ] 5 sample recipes created: dal tadka, rice, khichdi, poha, upma
- [ ] Parser validates ingredient dispenser assignments (P-ASD cartridge 1-6, CID tray 1-2, SLD liquid 1-2)
- [ ] Parser validates step action types: heat, stir, dispense, wait, detect_stage
- [ ] Invalid recipes rejected with clear error messages and line numbers

**Tasks:**
- [ ] `RCP-FMT.01a` — Define YAML recipe schema with all fields and types
- [ ] `RCP-FMT.01b` — Implement Python parser with pydantic model validation
- [ ] `RCP-FMT.01c` — Create 5 sample recipe YAML files with full step sequences
- [ ] `RCP-FMT.01d` — Implement error reporting with line numbers and field paths
- [ ] `RCP-FMT.01e` — Write unit tests for valid and invalid recipe parsing

---

### RCP-FSM.01: Cooking state machine — design, engine, step executor, transitions
- **Sprint:** [[sprint-08|Sprint 8]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-COM.01|EMB-COM.01]], [[THR-thermal#THR-PID.01|THR-PID.01]], [[ARM-actuation#ARM-SRV.01|ARM-SRV.01]], [[CV-vision#CV-MDL.02|CV-MDL.02]], [[CV-vision#CV-DET.02|CV-DET.02]], [[RCP-recipe#RCP-FMT.01|RCP-FMT.01]]
- **Blocks:** [[RCP-recipe#RCP-FSM.02|RCP-FSM.02]]

**Acceptance Criteria:**
- [ ] State machine: IDLE → PREHEAT → PREP → COOK → SIMMER → DONE → CLEANUP
- [ ] Asyncio event-driven engine with event-driven transitions
- [ ] Step executor maps recipe step actions to SPI bridge commands (temp, servo, dispense)
- [ ] Transitions based on: timer expiry, CV stage detection, temperature reached, weight dispensed

**Tasks:**
- [ ] `RCP-FSM.01a` — Design state machine with state definitions, transitions, and guard conditions
- [ ] `RCP-FSM.01b` — Implement state machine engine (Python, asyncio-based) with event-driven transitions
- [ ] `RCP-FSM.01c` — Implement step executor: maps recipe step actions to SPI bridge commands
- [ ] `RCP-FSM.01d` — Implement transition conditions: timer, CV stage, temperature threshold, weight target

---

### RCP-FSM.02: State machine controls and telemetry — pause/resume, abort, logging, MQTT status
- **Sprint:** [[sprint-08|Sprint 8]] → [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]
- **Blocks:** [[UI-touchscreen#UI-COK.01|UI-COK.01]], [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] Pause/resume: user can pause cooking; all actuators hold current state
- [ ] Abort: user can cancel; system performs safe shutdown (heat off, arm home, valves closed)
- [ ] Cook session logged to PostgreSQL: start time, recipe, state transitions, sensor data, completion status
- [ ] Real-time status published to MQTT: `epicura/cook/status` with current state, step, progress %
- [ ] Dry-run test with dal tadka recipe (simulated sensors)

**Tasks:**
- [ ] `RCP-FSM.02a` — Implement pause/resume and abort with safe state handling
- [ ] `RCP-FSM.02b` — Implement cook session logging to PostgreSQL
- [ ] `RCP-FSM.02c` — Implement MQTT status publisher with progress calculation
- [ ] `RCP-FSM.02d` — Test state machine with dal tadka recipe: full end-to-end dry run (simulated sensors)

---

### RCP-DSP.01: Dispensing orchestration — sequence generation, coordination, weight verification
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[ARM-actuation#ARM-ASD.01|ARM-ASD.01]], [[ARM-actuation#ARM-CID.01|ARM-CID.01]], [[ARM-actuation#ARM-SLD.01|ARM-SLD.01]], [[ARM-actuation#ARM-CAL.01|ARM-CAL.01]]
- **Blocks:** [[RCP-recipe#RCP-DSP.02|RCP-DSP.02]]

**Acceptance Criteria:**
- [ ] Dispensing orchestrator parses recipe ingredient list and generates dispense sequence
- [ ] Sequential dispensing: one dispenser at a time to prevent mechanical conflicts
- [ ] Weight verification: after each dispense, check load cell delta matches expected amount (±10%)

**Tasks:**
- [ ] `RCP-DSP.01a` — Implement dispensing sequence generator from recipe ingredient list
- [ ] `RCP-DSP.01b` — Implement sequential dispenser coordination (mutex across P-ASD, CID, SLD)
- [ ] `RCP-DSP.01c` — Implement weight verification after each dispense via HX711 load cells

---

### RCP-DSP.02: Dispensing integration — retry logic, state machine integration, recipe testing
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[RCP-recipe#RCP-DSP.01|RCP-DSP.01]]
- **Blocks:** [[INT-integration#INT-SYS.01|INT-SYS.01]]

**Acceptance Criteria:**
- [ ] Retry logic: if weight verification fails, retry dispense once; then alert user
- [ ] Dispense timing coordinated with cooking state: e.g., add oil before preheat, add spices at sizzle stage
- [ ] Dispensing progress published to MQTT: `epicura/cook/dispense` with ingredient, amount, status
- [ ] Tested with dal tadka recipe: oil, mustard seeds, cumin, dal, water, salt

**Tasks:**
- [ ] `RCP-DSP.02a` — Implement retry logic with user alert on verification failure
- [ ] `RCP-DSP.02b` — Integrate dispensing with state machine step executor
- [ ] `RCP-DSP.02c` — Test dispensing sequence for dal tadka recipe: oil, mustard seeds, cumin, dal, water, salt

---

### RCP-SYN.01: Cloud recipe sync — download, cache, versioning
- **Sprint:** [[sprint-09|Sprint 9]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[BE-backend#BE-RCP.01|BE-RCP.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Recipe sync service checks cloud API for new/updated recipes on WiFi connection
- [ ] Recipes cached locally in PostgreSQL with version tracking
- [ ] Offline-first: all cached recipes available without network
- [ ] Recipe images downloaded and cached in /data/recipes/images/
- [ ] Sync status shown in UI: last sync time, pending updates count
- [ ] Conflict resolution: cloud version always wins (server-authoritative)

**Tasks:**
- [ ] `RCP-SYN.01a` — Implement recipe sync service: poll cloud API, compare versions
- [ ] `RCP-SYN.01b` — Implement local recipe storage in PostgreSQL with version column
- [ ] `RCP-SYN.01c` — Implement image download and caching with disk space management
- [ ] `RCP-SYN.01d` — Implement sync status MQTT publication for UI display
- [ ] `RCP-SYN.01e` — Test sync: add recipe on cloud, verify it appears on device within 60 seconds

---

## Dependencies

### What RCP blocks (downstream consumers)

| RCP Story | Blocks | Reason |
|-----------|--------|--------|
| RCP-FMT.01 | RCP-FSM.01, BE-RCP.01 | Recipe format needed for engine and cloud API |
| RCP-FSM.01 | RCP-FSM.02 | Core state machine needed for controls and telemetry |
| RCP-FSM.02 | UI-COK.01, INT-SYS.01 | State machine drives cooking UI and integration tests |
| RCP-DSP.01 | RCP-DSP.02 | Core dispensing needed for integration and testing |
| RCP-DSP.02 | INT-SYS.01 | Dispensing needed for end-to-end cooking |

### What blocks RCP (upstream dependencies)

| RCP Story | Blocked by | Reason |
|-----------|------------|--------|
| RCP-FMT.01 | EMB-SET.02, EMB-SET.03 | Need CM5 platform for Python services |
| RCP-FSM.01 | EMB-COM.01, THR-PID.01, ARM-SRV.01, CV-MDL.02, CV-DET.02, RCP-FMT.01 | Orchestrates all subsystems |
| RCP-FSM.02 | RCP-FSM.01 | Needs core state machine |
| RCP-DSP.01 | ARM-ASD.01, ARM-CID.01, ARM-SLD.01, ARM-CAL.01 | Needs all dispensers working and calibrated |
| RCP-DSP.02 | RCP-DSP.01 | Needs core dispensing orchestration |
| RCP-SYN.01 | BE-RCP.01 | Needs cloud recipe API |

---

## References

- [[__Workspaces/Epicura/docs/03-Software/02-Controller-Software-Architecture|Controller Software Architecture]]
- [[__Workspaces/Epicura/docs/03-Software/03-Main-Loop-State-Machine|Main Loop State Machine]]
- [[__Workspaces/Epicura/docs/05-Subsystems/03-Ingredient-Dispensing|Ingredient Dispensing Subsystem]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
