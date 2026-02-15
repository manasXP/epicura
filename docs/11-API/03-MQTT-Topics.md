---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# MQTT Topics

## Overview

MQTT is the primary telemetry protocol between Epicura devices (CM5) and the cloud backend. The CM5 publishes real-time cooking data, device status, and alerts; the backend publishes commands for remote cooking control, OTA triggers, and configuration updates.

This document extends the MQTT telemetry format defined in [[../03-Software/04-Controller-Software-Architecture#6. Cloud Sync (CM5)|Controller Software Architecture - Cloud Sync]].

---

## Broker Configuration

| Setting | Development | Production |
|---------|-------------|------------|
| **Broker** | Eclipse Mosquitto 2.x | AWS IoT Core |
| **Port** | 1883 (TCP) / 9001 (WebSocket) | 8883 (TLS) |
| **Protocol** | MQTT 3.1.1 | MQTT 3.1.1 |
| **Auth (Dev)** | Username/password | X.509 device certificates |
| **Auth (Prod)** | — | AWS IoT policy per device |
| **TLS** | Optional (dev) | Required (mutual TLS) |
| **Max Message Size** | 256 KB | 128 KB (AWS IoT limit) |
| **Keep Alive** | 60 seconds | 60 seconds |

---

## Topic Hierarchy

All topics follow the pattern: `epicura/{device_id}/{category}/{event}`

```
epicura/
└── {device_id}/                          Device-specific namespace
    ├── telemetry                          Periodic sensor readings
    ├── session/
    │   ├── started                        Cooking session began
    │   ├── progress                       Stage/temp/stir updates
    │   ├── completed                      Cooking finished successfully
    │   └── error                          Cooking error or abort
    ├── status                             Device online/offline/health
    ├── alert                              Warnings and critical events
    └── cmd/                               Commands TO device (subscribed by CM5)
        ├── cook                           Start cooking remotely
        ├── stop                           Emergency stop
        ├── ota                            Trigger firmware update
        ├── recipe-sync                    Trigger recipe sync
        └── config                         Configuration update
```

---

## Device Telemetry (CM5 → Cloud)

### `epicura/{device_id}/telemetry`

Periodic sensor readings published every 10 seconds during cooking, every 60 seconds when idle.

**QoS:** 0 (at most once — acceptable loss for high-frequency telemetry)

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:30:00Z",
  "state": "COOKING",
  "recipe": "dal_tadka",
  "stage": "Simmer Dal",
  "temperature": 96.2,
  "target_temperature": 95.0,
  "stir_active": true,
  "stir_pattern": "intermittent",
  "stir_rpm": 30,
  "weight_g": 1250,
  "progress_pct": 72,
  "cv_class": "thick_consistency",
  "cv_confidence": 0.81,
  "power_pct": 45,
  "ambient_temp": 28.3,
  "coil_temp": 142.0
}
```

This extends the telemetry payload format from [[../03-Software/04-Controller-Software-Architecture#MQTT Telemetry|Controller Software Architecture]] with additional fields (`target_temperature`, `stir_pattern`, `stir_rpm`, `weight_g`, `cv_class`, `cv_confidence`, `power_pct`, `coil_temp`).

---

### `epicura/{device_id}/session/started`

Published when a cooking session begins.

**QoS:** 1 (at least once)

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:30:05Z",
  "session_id": "local-session-uuid",
  "recipe_id": "recipe-uuid-001",
  "recipe_name": "Dal Tadka",
  "total_stages": 6,
  "estimated_time_minutes": 35,
  "customizations": {
    "spice_level": 4,
    "servings": 2
  }
}
```

### `epicura/{device_id}/session/progress`

Published on stage transitions and significant events (every 5-10 seconds during cooking).

**QoS:** 0

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:38:00Z",
  "session_id": "local-session-uuid",
  "current_stage": 3,
  "stage_name": "Saute Onions",
  "total_stages": 6,
  "progress_pct": 42,
  "temperature": 148.5,
  "target_temperature": 150,
  "stir_active": true,
  "time_elapsed_s": 480,
  "cv_status": {
    "class": "golden_brown",
    "confidence": 0.72
  }
}
```

### `epicura/{device_id}/session/completed`

Published when cooking finishes successfully.

**QoS:** 1

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T13:05:22Z",
  "session_id": "local-session-uuid",
  "recipe_name": "Dal Tadka",
  "total_duration_s": 2122,
  "stages_completed": 6,
  "peak_temperature": 182.5,
  "result": "success"
}
```

### `epicura/{device_id}/session/error`

Published when a cooking error or abort occurs.

**QoS:** 1

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:40:00Z",
  "session_id": "local-session-uuid",
  "error_code": "OVER_TEMPERATURE",
  "message": "Temperature exceeded 260°C. E-stop activated.",
  "severity": "critical",
  "stage_at_error": "Saute Onions",
  "temperature_at_error": 262.3
}
```

---

### `epicura/{device_id}/status`

Device health and connectivity status. Published on state changes and every 60 seconds as a heartbeat.

**QoS:** 1
**Retained:** Yes (broker stores last status for new subscribers)

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:28:00Z",
  "status": "online",
  "firmware_cm5": "1.2.0",
  "firmware_stm32": "1.1.0",
  "uptime_s": 86400,
  "wifi_rssi": -42,
  "free_memory_mb": 1024,
  "disk_usage_pct": 34,
  "cpu_temp": 52.3
}
```

### `epicura/{device_id}/alert`

Device alerts that require backend processing or user notification.

**QoS:** 1

**Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:29:00Z",
  "alert_type": "sensor_degraded",
  "severity": "warning",
  "message": "IR thermometer readings unstable — using NTC fallback",
  "details": {
    "sensor": "MLX90614",
    "error_count": 5,
    "last_valid_reading": 145.2
  }
}
```

---

## Device Commands (Cloud → CM5)

The CM5 subscribes to command topics and acts on received messages. All commands use **QoS 1**.

### `epicura/{device_id}/cmd/cook`

Remotely start cooking a recipe (initiated from mobile app via backend).

**Payload:**
```json
{
  "command_id": "cmd-uuid-001",
  "recipe_id": "recipe-uuid-001",
  "customizations": {
    "spice_level": 4,
    "servings": 2
  },
  "initiated_by": "user-uuid-001",
  "timestamp": "2026-02-14T12:30:00Z"
}
```

**CM5 Response:** Publishes to `epicura/{device_id}/session/started` on success, or `epicura/{device_id}/session/error` on failure.

### `epicura/{device_id}/cmd/stop`

Emergency stop command.

**Payload:**
```json
{
  "command_id": "cmd-uuid-002",
  "reason": "user_requested",
  "initiated_by": "user-uuid-001",
  "timestamp": "2026-02-14T12:40:00Z"
}
```

### `epicura/{device_id}/cmd/ota`

Trigger firmware update download and installation.

**Payload:**
```json
{
  "command_id": "cmd-uuid-003",
  "target": "cm5",
  "version": "1.2.1",
  "binary_url": "https://cdn.epicura.io/firmware/cm5/1.2.1.img",
  "checksum_sha256": "a1b2c3d4...",
  "is_mandatory": false,
  "timestamp": "2026-02-14T14:00:00Z"
}
```

### `epicura/{device_id}/cmd/recipe-sync`

Trigger the CM5 to sync recipes from the cloud API.

**Payload:**
```json
{
  "command_id": "cmd-uuid-004",
  "timestamp": "2026-02-14T14:05:00Z"
}
```

### `epicura/{device_id}/cmd/config`

Push configuration updates to the device.

**Payload:**
```json
{
  "command_id": "cmd-uuid-005",
  "config": {
    "telemetry_interval_s": 5,
    "cv_confidence_threshold": 0.65,
    "mqtt_keepalive_s": 30
  },
  "timestamp": "2026-02-14T14:10:00Z"
}
```

---

## Retained Messages

| Topic | Retained | Reason |
|-------|----------|--------|
| `status` | Yes | New subscribers see current device state immediately |
| `telemetry` | No | High-frequency, no need for last value on connect |
| `session/*` | No | Session-specific, relevant only during active cooking |
| `alert` | No | Alerts are event-driven, processed once |
| `cmd/*` | No | Commands are one-time actions |

---

## Last Will and Testament (LWT)

Each CM5 device registers an LWT message on MQTT connect. If the device disconnects unexpectedly (without a clean DISCONNECT), the broker publishes the LWT:

**LWT Topic:** `epicura/{device_id}/status`
**LWT Payload:**
```json
{
  "device_id": "EPIC-001",
  "timestamp": "2026-02-14T12:00:00Z",
  "status": "offline",
  "reason": "unexpected_disconnect"
}
```
**LWT QoS:** 1
**LWT Retained:** Yes

---

## TLS Security

### Development (Mosquitto)

- TLS optional for local development
- Username/password authentication: `epicura_dev` / configured password
- ACL: devices can only publish/subscribe to their own `epicura/{device_id}/` subtree

### Production (AWS IoT Core)

- Mutual TLS with X.509 device certificates
- Each device provisioned with unique certificate + private key during manufacturing
- IoT Policy restricts each device to its own topic namespace:

```json
{
  "Effect": "Allow",
  "Action": ["iot:Publish", "iot:Subscribe", "iot:Receive"],
  "Resource": "arn:aws:iot:*:*:topic/epicura/${iot:ClientId}/*"
}
```

---

## Backend Subscription and Bridging

The API server subscribes to device topics and processes messages:

```
┌─────────────────────────────────────────────────────────┐
│                   API Server MQTT Handler                 │
│                                                           │
│  Subscribe: epicura/+/telemetry                          │
│  Subscribe: epicura/+/session/#                          │
│  Subscribe: epicura/+/status                             │
│  Subscribe: epicura/+/alert                              │
│                                                           │
│  On message:                                              │
│  ├── telemetry  → Store in telemetry_events (Postgres)   │
│  ├── session/*  → Update cooking_sessions, notify WS     │
│  ├── status     → Update appliances.status + last_seen   │
│  └── alert      → Log, evaluate push notification rules  │
│                                                           │
│  Publish: epicura/{device_id}/cmd/*                      │
│  ├── cook       → Forward remote cook request            │
│  ├── stop       → Forward emergency stop                 │
│  ├── ota        → Trigger firmware update                │
│  ├── recipe-sync→ Trigger recipe download                │
│  └── config     → Push configuration changes             │
└─────────────────────────────────────────────────────────┘
```

The wildcard `+` in subscriptions matches any device ID, so the server handles all devices on a single subscription set.

---

## Related Documentation

- [[01-REST-API-Reference|REST API Reference]] - HTTP endpoints
- [[02-WebSocket-Events|WebSocket Events]] - Mobile app real-time events (bridged from MQTT)
- [[04-BLE-Services|BLE Services]] - BLE pairing and WiFi provisioning
- [[../10-Backend/01-Backend-Architecture|Backend Architecture]] - MQTT bridge architecture
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]] - CM5 MQTT client and telemetry format

#epicura #mqtt #telemetry #iot #api #protocol

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
