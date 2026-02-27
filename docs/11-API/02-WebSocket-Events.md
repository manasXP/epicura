---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# WebSocket Events

## 1. Overview

Epicura uses WebSocket connections for real-time communication between the cloud backend and mobile apps. The CM5 device publishes telemetry via MQTT (see [[03-MQTT-Topics|MQTT Topics]]), which the backend bridges to WebSocket clients. For local WiFi connections, apps can also connect directly to the CM5's WebSocket server.

---

## 2. Connection

### 2.1 Cloud Relay

```
URL:  wss://api.epicura.io/ws
Auth: Pass JWT access token as query parameter
```

```
wss://api.epicura.io/ws?token=eyJhbGciOiJIUzI1NiIs...
```

### 2.2 Local (Direct to CM5)

```
URL:  ws://<device-ip>:8080/ws
Auth: None (same WiFi network assumed trusted)
```

The CM5 device IP is discovered via mDNS (`_epicura._tcp.local`) or read from the BLE WiFi Provisioning service (see [[04-BLE-Services|BLE Services]]).

---

## 3. Connection Lifecycle

```
┌──────────┐                              ┌──────────┐
│  Mobile  │                              │  Server  │
│   App    │                              │ (Fastify)│
└────┬─────┘                              └────┬─────┘
     │  WS Connect + JWT                       │
     │────────────────────────────────────────►│
     │                                         │  Verify JWT
     │  { type: "connected", user_id: "..." }  │
     │◄────────────────────────────────────────│
     │                                         │
     │  { type: "subscribe",                   │
     │    appliance_id: "EPIC-001" }           │
     │────────────────────────────────────────►│  Verify ownership
     │                                         │
     │  { type: "subscribed",                  │
     │    appliance_id: "EPIC-001" }           │
     │◄────────────────────────────────────────│
     │                                         │
     │  ... real-time events flow ...          │
     │                                         │
     │  Ping (every 30s)                       │
     │────────────────────────────────────────►│
     │  Pong                                   │
     │◄────────────────────────────────────────│
```

### 3.1 Heartbeat

- Client sends `ping` frame every 30 seconds
- Server responds with `pong` frame
- If no `pong` received within 10 seconds, client should reconnect
- Server disconnects clients with no activity for 60 seconds

---

## 4. Event Format

All WebSocket messages use JSON with a consistent envelope:

```json
{
  "type": "event_type",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:30:00Z",
  "data": { ... }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Event type identifier |
| `appliance_id` | string | Source or target device ID |
| `timestamp` | ISO 8601 | Event timestamp |
| `data` | object | Event-specific payload |

---

## 5. Client Events (App → Server)

### 5.1 `subscribe`

Subscribe to real-time events from a specific appliance.

```json
{
  "type": "subscribe",
  "appliance_id": "EPIC-001"
}
```

**Response:**
```json
{
  "type": "subscribed",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:30:00Z",
  "data": {
    "current_status": "online"
  }
}
```

### 5.2 `cooking:start`

Request to start cooking a recipe on a paired appliance.

```json
{
  "type": "cooking:start",
  "appliance_id": "EPIC-001",
  "data": {
    "recipe_id": "recipe-uuid-001",
    "customizations": {
      "spice_level": 4,
      "servings": 2
    }
  }
}
```

### 5.3 `cooking:pause`

Pause the current cooking session.

```json
{
  "type": "cooking:pause",
  "appliance_id": "EPIC-001"
}
```

### 5.4 `cooking:resume`

Resume a paused cooking session.

```json
{
  "type": "cooking:resume",
  "appliance_id": "EPIC-001"
}
```

### 5.5 `cooking:stop`

Emergency stop — immediately halt cooking.

```json
{
  "type": "cooking:stop",
  "appliance_id": "EPIC-001"
}
```

---

## 6. Server Events (Server → App)

### 6.1 `cooking:started`

Cooking session has begun on the device.

```json
{
  "type": "cooking:started",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:30:05Z",
  "data": {
    "session_id": "session-uuid-001",
    "recipe_id": "recipe-uuid-001",
    "recipe_name": "Dal Tadka",
    "total_stages": 6,
    "estimated_time_minutes": 35
  }
}
```

### 6.2 `cooking:progress`

Periodic cooking progress update (every 5-10 seconds during active cooking).

```json
{
  "type": "cooking:progress",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:35:00Z",
  "data": {
    "session_id": "session-uuid-001",
    "current_stage": 3,
    "stage_name": "Saute Onions",
    "total_stages": 6,
    "progress_pct": 42,
    "temperature": 148.5,
    "target_temperature": 150,
    "stir_active": true,
    "stir_pattern": "continuous",
    "time_remaining_s": 185,
    "cv_status": {
      "class": "golden_brown",
      "confidence": 0.72
    }
  }
}
```

### 6.3 `cooking:stage_change`

A cooking stage transition has occurred.

```json
{
  "type": "cooking:stage_change",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:38:00Z",
  "data": {
    "session_id": "session-uuid-001",
    "previous_stage": {
      "index": 3,
      "name": "Saute Onions",
      "duration_s": 312,
      "result": "success",
      "transition": "cv_detected"
    },
    "next_stage": {
      "index": 4,
      "name": "Add Spices",
      "estimated_duration_s": 60
    }
  }
}
```

### 6.4 `cooking:complete`

Cooking session has finished successfully.

```json
{
  "type": "cooking:complete",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T13:05:22Z",
  "data": {
    "session_id": "session-uuid-001",
    "recipe_name": "Dal Tadka",
    "total_duration_s": 2122,
    "stages_completed": 6,
    "peak_temperature": 182.5,
    "cv_transitions": 5,
    "timer_transitions": 1
  }
}
```

### 6.5 `cooking:error`

An error occurred during cooking.

```json
{
  "type": "cooking:error",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:40:00Z",
  "data": {
    "session_id": "session-uuid-001",
    "error_code": "OVER_TEMPERATURE",
    "message": "Temperature exceeded safe threshold (260°C). Heating disabled.",
    "severity": "critical",
    "action_taken": "e_stop"
  }
}
```

### 6.6 `appliance:status`

Device status change (online, offline, cooking, error).

```json
{
  "type": "appliance:status",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:28:00Z",
  "data": {
    "status": "online",
    "firmware_version_cm5": "1.2.0",
    "firmware_version_stm32": "1.1.0"
  }
}
```

### 6.7 `appliance:alert`

Device alert requiring user attention.

```json
{
  "type": "appliance:alert",
  "appliance_id": "EPIC-001",
  "timestamp": "2026-02-14T12:29:00Z",
  "data": {
    "alert_type": "firmware_update_available",
    "message": "New firmware v1.2.1 available for CM5",
    "priority": "low"
  }
}
```

---

## 7. Cloud Relay Architecture

The cloud backend bridges MQTT telemetry from Epicura devices to WebSocket clients:

```
┌──────────┐     MQTT         ┌──────────────┐     Redis Pub/Sub    ┌───────────┐
│ Epicura  │────────────────►│  MQTT Broker  │────────────────────►│ API Server│
│ CM5      │                  │  (Mosquitto / │                     │ (Fastify) │
│          │                  │   AWS IoT)    │                     │           │
└──────────┘                  └──────────────┘                     └─────┬─────┘
                                                                         │
                                                                   WebSocket
                                                                         │
                                                              ┌──────────▼──────────┐
                                                              │    Mobile App       │
                                                              │  (iOS / Android)    │
                                                              └─────────────────────┘
```

**Flow:**

1. CM5 publishes telemetry to MQTT topic `epicura/EPIC-001/session/progress`
2. API server MQTT subscriber receives the message
3. Server translates MQTT payload to WebSocket event format
4. Server publishes to Redis pub/sub channel `ws:EPIC-001`
5. WebSocket handler sends event to all clients subscribed to `EPIC-001`

This ensures horizontal scalability — multiple API server instances can serve WebSocket clients using Redis as the message bus.

---

## 8. Error Events

| Error Code | Severity | Description |
|------------|----------|-------------|
| `SENSOR_FAILURE` | `warning` | Temperature or weight sensor malfunction |
| `OVER_TEMPERATURE` | `critical` | Temperature exceeded safe maximum (260°C) |
| `MOTOR_STALL` | `warning` | Stirring arm stalled (overcurrent detected) |
| `COMMUNICATION_LOST` | `critical` | CM5-STM32 communication timeout |
| `CV_FAILURE` | `warning` | Camera or ML model failure (timer fallback active) |
| `POWER_ANOMALY` | `critical` | Voltage or current out of range |
| `POT_REMOVED` | `warning` | Pot removed during cooking |

---

## 9. Client Reconnection Strategy

| Attempt | Delay | Notes |
|---------|-------|-------|
| 1 | 1 second | Immediate retry |
| 2 | 2 seconds | |
| 3 | 4 seconds | |
| 4 | 8 seconds | |
| 5+ | 15 seconds | Max backoff, retry indefinitely |

On reconnection, the client should re-send `subscribe` events for all previously subscribed appliances. The server will send the current appliance status immediately after subscription.

---

## 10. Related Documentation

- [[01-REST-API-Reference|REST API Reference]] - HTTP endpoints
- [[03-MQTT-Topics|MQTT Topics]] - Device-side telemetry protocol
- [[04-BLE-Services|BLE Services]] - BLE pairing and local connectivity
- [[../10-Backend/01-Backend-Architecture|Backend Architecture]] - WebSocket server setup
- [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] - Mobile WebSocket client

#epicura #websocket #real-time #events #api

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
