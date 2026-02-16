---
tags: [epicura, testing, cm5, python, docker]
created: 2026-02-16
aliases: [CM5 Test Strategy]
---

# CM5 Test Strategy — epicura-cm5

## Scope

Testing strategy for all CM5-side Docker Compose services: recipe engine, CV pipeline, Kivy UI, CM5-STM32 bridge, PostgreSQL, and Mosquitto broker.

---

## Test Levels

### 1. Unit Tests

**Framework:** pytest + pytest-cov
**Runs on:** Host (x86/ARM), no hardware required

| Service | Key Test Cases |
|---------|---------------|
| **recipe-engine** | YAML recipe parsing (valid/invalid/malformed), state machine transitions (IDLE→PREHEAT→DISPENSE→COOK→DONE), step timeout handling, dispenser command generation, cloud sync conflict resolution |
| **cv-pipeline** | Image preprocessor (resize, normalize, ROI crop) with sample images, TFLite classifier wrapper with mock model, stage detection logic (raw→boiling→done), anomaly threshold triggers |
| **kivy-ui** | Screen navigation state machine, widget data binding (temp gauge updates on new reading), timer countdown logic, alert banner show/dismiss |
| **cm5-bridge** | Binary protocol frame encode/decode, CRC16 computation, message queue ordering, heartbeat timeout detection, reconnect logic |

**Approach:**
- Mock external dependencies: SPI hardware (`spidev`), camera (`picamera2`), MQTT broker, PostgreSQL
- Use `pytest-mock` for dependency injection
- Test YAML recipes against a schema validator (e.g., Cerberus or jsonschema)
- CV tests use a fixture set of 20+ labeled food images (stored in `tests/fixtures/`)

### 2. Integration Tests

**Framework:** pytest + Docker Compose (test profile)
**Runs on:** Host with Docker

| Test Area | Setup | Verification |
|-----------|-------|-------------|
| Recipe engine ↔ PostgreSQL | `docker compose -f docker-compose.test.yml up` | Recipe CRUD operations persist and query correctly |
| Recipe engine ↔ MQTT | Mosquitto container + test subscriber | State change events published to correct topics |
| CV pipeline ↔ recipe engine | Mock camera feed (pre-recorded frames) | Stage detection triggers recipe state transition |
| CM5 bridge ↔ recipe engine | Mock SPI responses via test double | Command sent → ACK received → recipe proceeds |
| Full cooking flow | All services up, mock SPI + mock camera | Complete recipe executes from IDLE to DONE without errors |

**Docker test profile:**
- `docker-compose.test.yml` — overrides with test env vars, mock hardware stubs, ephemeral PostgreSQL
- Test database seeded with `seed.sql` before each test suite
- MQTT messages captured by a test subscriber container

### 3. CV Model Validation

| Test | Dataset | Pass Criteria |
|------|---------|--------------|
| Classification accuracy | 200-image labeled test set | ≥ 85% accuracy on food stage classes |
| Inference latency | 50 sample images on CM5 hardware | < 200ms per frame (MobileNetV2 INT8) |
| Edge cases | Burnt food, empty pot, partially obscured | No false "DONE" detection; anomaly flag raised |

### 4. Performance Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Docker boot time | `time docker compose up` on CM5 | All services healthy within 60s |
| Memory usage | `docker stats` under cooking load | Total < 3 GB (fits 4 GB CM5 RAM) |
| PostgreSQL query latency | pgbench + recipe queries | p95 < 50ms for recipe lookup |
| MQTT throughput | Publish 100 telemetry msgs/sec | Zero dropped messages |
| OTA update | Apply `.swu` update, reboot | A/B partition swap completes, services recover |

---

## CI Pipeline

```yaml
# .github/workflows/ci.yml
trigger: PR to develop or main

steps:
  1. Checkout
  2. Install Python 3.11, Docker
  3. Run ruff lint (all services)
  4. Run mypy type check (all services)
  5. Run pytest unit tests per service (parallel)
  6. Build Docker images
  7. Run integration tests (docker compose test profile)
  8. Report coverage (pytest-cov, combined across services)
```

**Gate criteria:** Lint clean, type-check clean, all tests pass, coverage ≥ 75% per service.

---

## Test Fixtures

- **Sample recipes:** 10 YAML recipes covering all dispenser types, multi-step cooking, edge cases (empty steps, zero quantities)
- **CV test images:** 200 labeled images across 5 food stages (raw, simmering, boiling, thickened, done) + 20 anomaly images
- **Mock SPI responses:** Binary files with known-good STM32 response frames for each command type
- **PostgreSQL seed data:** Users, recipes, device records for integration tests

---

## Yocto Image Testing

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Image boot | Flash eMMC, power on | Login prompt within 30s |
| Docker service startup | `systemctl status docker` | Docker daemon running, all containers healthy |
| Network connectivity | `ping` + `curl` cloud endpoint | WiFi connects, API reachable |
| swupdate OTA | Push update, trigger install | System reboots to new partition, rollback on failure |
| Factory reset | Trigger factory provision script | Returns to clean state, all containers rebuilt |

---

## References

- [[__Workspaces/Epicura/docs/07-Development/02-Repository-Plan|Repository Plan]]
- [[__Workspaces/Epicura/docs/03-Software/02-Controller-Software-Architecture|Controller Software Architecture]]
- [[__Workspaces/Epicura/docs/05-Subsystems/04-Vision-System|Vision System]]
- [[__Workspaces/Epicura/docs/03-Software/03-Main-Loop-State-Machine|Main Loop State Machine]]
