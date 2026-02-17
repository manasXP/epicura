---
tags: [epicura, project-management, epic, embedded, firmware]
created: 2026-02-16
aliases: [EMB Epic, Embedded Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-16 | Manas Pradhan | Initial version — 7 stories across Sprints 1–2 and 11–12 |
> | 2026-02-17 | Manas Pradhan | Split >5pt stories for sprint-sized delivery |

# Epic: EMB — Embedded Platform

Set up the dual-processor platform: STM32G474 FreeRTOS firmware foundation and CM5 Yocto Linux + Docker environment. This epic establishes the hardware abstraction layer, inter-processor communication, database, MQTT broker, safety systems, and OTA update infrastructure.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| SET — Platform Setup | 5 | 21 | 1–2 |
| COM — Inter-Processor Communication | 2 | 8 | 1 |
| SAF — Safety Systems | 1 | 5 | 2 |
| OTA — Over-The-Air Updates | 1 | 5 | 2 |
| LCH — Launch Readiness | 1 | 5 | 12 |
| **Total** | **10** | **~46** | |

---

## Phase 0 — Foundation (Sprints 1–2)

### EMB-SET.01: STM32 FreeRTOS project — HAL config, task scaffold
- **Sprint:** [[sprint-01|Sprint 1]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[PCB-pcb-design#PCB-FAB.02|PCB-FAB.02]]
- **Blocks:** [[EMB-embedded#EMB-SET.01b|EMB-SET.01b]]

**Acceptance Criteria:**
- [ ] STM32CubeIDE project created with STM32G474RE target; HAL drivers generated
- [ ] HAL peripherals configured: SPI1, USART1, I2C1, FDCAN1, TIM1-4, ADC1-2
- [ ] FreeRTOS configured with 4 tasks: PID (100Hz), Servo (50Hz), Sensor (10Hz), Comms (20Hz)

**Tasks:**
- [ ] `EMB-SET.01a` — Create STM32CubeIDE project; configure clock tree (170 MHz HSE+PLL)
- [ ] `EMB-SET.01b` — Enable and configure HAL peripherals: SPI1, USART1, I2C1, FDCAN1, TIM1-4, ADC1-2
- [ ] `EMB-SET.01c` — Configure FreeRTOS: 4 tasks with priorities (PID=4, Servo=3, Sensor=2, Comms=1)

---

### EMB-SET.01b: STM32 debug and watchdog — IWDG, UART printf, heartbeat
- **Sprint:** [[sprint-01|Sprint 1]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** [[THR-thermal#THR-CAN.01|THR-CAN.01]], [[ARM-actuation#ARM-SRV.01|ARM-SRV.01]], All STM32-dependent stories

**Acceptance Criteria:**
- [ ] Hardware watchdog (IWDG) enabled with 500ms timeout; kicks in all task loops
- [ ] UART debug printf working via USART1 at 115200 baud
- [ ] LED heartbeat blink confirms RTOS scheduler running
- [ ] Stack overflow detection enabled (FreeRTOS configCHECK_FOR_STACK_OVERFLOW)
- [ ] RTOS stability verified over 1-hour run

**Tasks:**
- [ ] `EMB-SET.01d` — Implement IWDG watchdog with 500ms timeout; add kick to each task loop
- [ ] `EMB-SET.01e` — Implement UART debug printf via USART1; add startup banner with firmware version
- [ ] `EMB-SET.01f` — Add LED heartbeat toggle in idle hook; verify RTOS stability over 1-hour run

---

### EMB-SET.02: CM5 Yocto image — BSP layer, Docker engine, Compose
- **Sprint:** [[sprint-01|Sprint 1]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[PCB-pcb-design#PCB-FAB.02|PCB-FAB.02]]
- **Blocks:** [[EMB-embedded#EMB-SET.02b|EMB-SET.02b]]

**Acceptance Criteria:**
- [ ] Yocto Kirkstone image boots on CM5 with Docker engine enabled
- [ ] Docker Compose file defines services: PostgreSQL 16, Mosquitto, recipe-engine, cv-pipeline, kivy-ui, cm5-bridge
- [ ] SSH access enabled for development; disabled in production image

**Tasks:**
- [ ] `EMB-SET.02a` — Set up Yocto Kirkstone build environment; create Epicura BSP layer
- [ ] `EMB-SET.02b` — Configure Yocto recipe for Docker engine (moby) and Docker Compose
- [ ] `EMB-SET.02c` — Create Docker Compose file with all 6 service containers

---

### EMB-SET.02b: CM5 database and MQTT — PostgreSQL schema, Mosquitto config, boot validation
- **Sprint:** [[sprint-01|Sprint 1]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[EMB-embedded#EMB-SET.02|EMB-SET.02]]
- **Blocks:** [[CV-vision#CV-CAM.01|CV-CAM.01]], [[RCP-recipe#RCP-FMT.01|RCP-FMT.01]], [[UI-touchscreen#UI-SET.01|UI-SET.01]]

**Acceptance Criteria:**
- [ ] PostgreSQL container starts with Epicura schema (recipes, cook_sessions, telemetry tables)
- [ ] Mosquitto container starts with local bridge configuration
- [ ] CM5 boots to login within 30 seconds; Docker services start within 60 seconds

**Tasks:**
- [ ] `EMB-SET.02d` — Create PostgreSQL init script with Epicura schema migration
- [ ] `EMB-SET.02e` — Configure Mosquitto with local topics and optional cloud bridge
- [ ] `EMB-SET.02f` — Build and flash Yocto image to CM5 eMMC; verify boot and Docker services

---

### EMB-COM.01: CM5-STM32 SPI bridge — protocol, drivers, command dispatch
- **Sprint:** [[sprint-01|Sprint 1]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]], [[EMB-embedded#EMB-SET.02|EMB-SET.02]]
- **Blocks:** [[EMB-embedded#EMB-COM.02|EMB-COM.02]]

**Acceptance Criteria:**
- [ ] SPI communication at 1 MHz between CM5 (master) and STM32 (slave) verified
- [ ] Binary protocol defined: header (2B sync + 1B cmd + 1B len) + payload + CRC16
- [ ] Python bridge service on CM5 sends commands and receives telemetry
- [ ] STM32 SPI interrupt handler processes commands within 1ms
- [ ] Command dispatch on STM32: SET_TEMP, SET_SERVO, DISPENSE, GET_STATUS, E_STOP

**Tasks:**
- [ ] `EMB-COM.01a` — Define binary protocol specification: command IDs, payload formats, CRC16
- [ ] `EMB-COM.01b` — Implement STM32 SPI slave driver (HAL_SPI_TransmitReceive_IT) with ring buffer
- [ ] `EMB-COM.01c` — Implement Python bridge service: SPI master via spidev, message queue (asyncio)
- [ ] `EMB-COM.01d` — Implement command dispatch on STM32: SET_TEMP, SET_SERVO, DISPENSE, GET_STATUS, E_STOP

---

### EMB-COM.02: CM5-STM32 health monitoring — heartbeat, timeout detection, UART fallback
- **Sprint:** [[sprint-01|Sprint 1]]
- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[EMB-embedded#EMB-COM.01|EMB-COM.01]]
- **Blocks:** [[THR-thermal#THR-PID.01|THR-PID.01]], [[ARM-actuation#ARM-SRV.01|ARM-SRV.01]], [[RCP-recipe#RCP-FSM.01|RCP-FSM.01]]

**Acceptance Criteria:**
- [ ] Health monitoring: CM5 bridge detects STM32 timeout (>100ms); STM32 detects CM5 silence (>500ms)
- [ ] UART fallback path tested and documented
- [ ] Round-trip latency verified <5ms for command-response cycle

**Tasks:**
- [ ] `EMB-COM.02a` — Implement health monitoring: heartbeat ping/pong, timeout detection, error counters
- [ ] `EMB-COM.02b` — Test UART fallback path; document switchover procedure
- [ ] `EMB-COM.02c` — Test round-trip latency; verify <5ms for command-response cycle

---

### EMB-SET.03: Docker service containers — recipe engine, CV pipeline, Kivy UI scaffolds
- **Sprint:** [[sprint-02|Sprint 2]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.02|EMB-SET.02]]
- **Blocks:** [[CV-vision#CV-CAM.01|CV-CAM.01]], [[RCP-recipe#RCP-FMT.01|RCP-FMT.01]], [[UI-touchscreen#UI-SET.01|UI-SET.01]]

**Acceptance Criteria:**
- [ ] recipe-engine container: Python 3.11, YAML parser, MQTT client, PostgreSQL client
- [ ] cv-pipeline container: Python 3.11, OpenCV 4.x, TFLite runtime, libcamera bindings
- [ ] kivy-ui container: Python 3.11, Kivy 2.3+, GPU acceleration (EGL/DRM), DSI display output
- [ ] cm5-bridge container: Python 3.11, spidev, asyncio, MQTT client
- [ ] All containers build successfully on ARM64; total image size <2GB
- [ ] Inter-container communication via MQTT topics verified

**Tasks:**
- [ ] `EMB-SET.03a` — Create Dockerfiles for each service with ARM64 base images
- [ ] `EMB-SET.03b` — Configure recipe-engine container with dependencies; verify MQTT pub/sub
- [ ] `EMB-SET.03c` — Configure cv-pipeline container with OpenCV + TFLite; verify camera access
- [ ] `EMB-SET.03d` — Configure kivy-ui container with GPU passthrough; verify display output
- [ ] `EMB-SET.03e` — Configure cm5-bridge container with SPI device access (/dev/spidev0.0)
- [ ] `EMB-SET.03f` — Test all containers start via Docker Compose; verify MQTT communication

---

### EMB-SAF.01: Safety systems — e-stop relay, thermal cutoffs, safety relay for AC disconnect
- **Sprint:** [[sprint-02|Sprint 2]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.01|EMB-SET.01]]
- **Blocks:** [[THR-thermal#THR-SAF.01|THR-SAF.01]], [[INT-integration#INT-SAF.01|INT-SAF.01]]

**Acceptance Criteria:**
- [ ] E-stop button triggers hardware interrupt; STM32 de-energizes all actuators within 100ms
- [ ] Safety relay cuts AC power to induction module on e-stop or watchdog timeout
- [ ] Thermal cutoff: if any NTC reads >150°C or IR reads >300°C, immediate shutdown
- [ ] Watchdog timeout (STM32 hung) triggers safety relay open
- [ ] All safety states logged via UART; recovery requires manual reset
- [ ] Safety state machine: NORMAL → ALERT → SHUTDOWN → RECOVERY

**Tasks:**
- [ ] `EMB-SAF.01a` — Configure e-stop GPIO as EXTI interrupt (falling edge, highest priority)
- [ ] `EMB-SAF.01b` — Implement emergency shutdown routine: disable all PWM, open all solenoids, open safety relay
- [ ] `EMB-SAF.01c` — Implement thermal monitoring in Sensor task: NTC and IR threshold checks
- [ ] `EMB-SAF.01d` — Wire watchdog timeout to safety relay via dedicated GPIO (fail-safe: relay opens on MCU reset)
- [ ] `EMB-SAF.01e` — Implement safety state machine with transition logging
- [ ] `EMB-SAF.01f` — Test all safety paths: e-stop press, thermal overshoot, watchdog timeout

---

### EMB-OTA.01: OTA update system — swupdate, A/B partitions, rollback
- **Sprint:** [[sprint-02|Sprint 2]]
- **Priority:** P1
- **Points:** 5
- **Blocked by:** [[EMB-embedded#EMB-SET.02|EMB-SET.02]]
- **Blocks:** [[INT-integration#INT-LCH.01|INT-LCH.01]]

**Acceptance Criteria:**
- [ ] CM5 eMMC partitioned with A/B rootfs layout for atomic updates
- [ ] swupdate installed and configured with HTTPS update server support
- [ ] Update image (.swu) built from Yocto; includes rootfs + Docker images
- [ ] Successful update switches active partition; failed update rolls back automatically
- [ ] STM32 firmware update via CM5 (SWD or UART bootloader) included in OTA bundle
- [ ] Update progress reported via MQTT topic

**Tasks:**
- [ ] `EMB-OTA.01a` — Configure Yocto for A/B partition layout (boot, rootfs_a, rootfs_b, data)
- [ ] `EMB-OTA.01b` — Integrate swupdate into Yocto image; configure update handlers
- [ ] `EMB-OTA.01c` — Create .swu image build pipeline (rootfs delta + Docker image layers)
- [ ] `EMB-OTA.01d` — Implement rollback detection: boot counter, health check after update
- [ ] `EMB-OTA.01e` — Implement STM32 firmware update mechanism via CM5 (stm32flash or custom bootloader)
- [ ] `EMB-OTA.01f` — Test full OTA cycle: download → install → reboot → verify → rollback on failure

---

### EMB-LCH.01: Production firmware — release build, configuration management, factory provisioning
- **Sprint:** [[sprint-12|Sprint 12]]
- **Priority:** P0
- **Points:** 5
- **Blocked by:** [[INT-integration#INT-SYS.01|INT-SYS.01]]
- **Blocks:** [[INT-integration#INT-LCH.01|INT-LCH.01]]

**Acceptance Criteria:**
- [ ] STM32 release build with optimizations (-O2), debug symbols stripped
- [ ] CM5 production Yocto image: SSH disabled, serial console disabled, Docker auto-start
- [ ] Factory provisioning script: flash STM32, flash CM5 eMMC, set device UUID, run self-test
- [ ] Configuration stored in persistent data partition (not overwritten by OTA)
- [ ] Firmware version reporting via MQTT and UI settings screen

**Tasks:**
- [ ] `EMB-LCH.01a` — Create STM32 release build configuration; strip debug symbols; verify binary size
- [ ] `EMB-LCH.01b` — Create CM5 production Yocto image variant; harden security settings
- [ ] `EMB-LCH.01c` — Write factory provisioning script: flash, provision, self-test, report
- [ ] `EMB-LCH.01d` — Implement persistent configuration storage (device UUID, calibration data, WiFi credentials)
- [ ] `EMB-LCH.01e` — Verify firmware version displayed in UI and reported via MQTT

---

## Dependencies

### What EMB blocks (downstream consumers)

| EMB Story | Blocks | Reason |
|-----------|--------|--------|
| EMB-SET.01 | EMB-SET.01b | Task scaffold needed before debug/watchdog setup |
| EMB-SET.01b | THR-CAN.01, ARM-SRV.01 | STM32 HAL and watchdog required for all peripheral drivers |
| EMB-SET.02 | EMB-SET.02b | Docker environment needed before database/MQTT setup |
| EMB-SET.02b | CV-CAM.01, RCP-FMT.01, UI-SET.01 | CM5 platform with database and MQTT required for CM5 services |
| EMB-COM.01 | EMB-COM.02 | SPI bridge needed before health monitoring |
| EMB-COM.02 | THR-PID.01, ARM-SRV.01, RCP-FSM.01 | Bridge with health monitoring needed for CM5→STM32 commands |
| EMB-SET.03 | CV-CAM.01, RCP-FMT.01, UI-SET.01 | Docker containers needed for services |
| EMB-SAF.01 | THR-SAF.01, INT-SAF.01 | Safety framework needed for thermal and integration testing |
| EMB-OTA.01 | INT-LCH.01 | OTA needed for production deployment |
| EMB-LCH.01 | INT-LCH.01 | Production firmware for launch |

### What blocks EMB (upstream dependencies)

| EMB Story | Blocked by | Reason |
|-----------|------------|--------|
| EMB-SET.01 | PCB-FAB.02 | Need validated controller board |
| EMB-SET.01b | EMB-SET.01 | Need STM32 project and task scaffold |
| EMB-SET.02 | PCB-FAB.02 | Need CM5IO carrier board verified |
| EMB-SET.02b | EMB-SET.02 | Need CM5 Docker environment |
| EMB-COM.01 | EMB-SET.01, EMB-SET.02 | Need both processors running |
| EMB-COM.02 | EMB-COM.01 | Need SPI bridge working |
| EMB-SET.03 | EMB-SET.02 | Need CM5 Docker environment |
| EMB-SAF.01 | EMB-SET.01 | Need STM32 GPIO and interrupt setup |
| EMB-OTA.01 | EMB-SET.02 | Need CM5 Yocto image |
| EMB-LCH.01 | INT-SYS.01 | Need integration tests passing |

---

## References

- [[__Workspaces/Epicura/docs/02-Hardware/01-Epicura-Architecture|System Architecture]]
- [[__Workspaces/Epicura/docs/03-Software/02-Controller-Software-Architecture|Controller Software Architecture]]
- [[__Workspaces/Epicura/docs/02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
