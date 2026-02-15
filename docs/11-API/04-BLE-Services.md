---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# BLE Services

## Overview

Epicura uses Bluetooth Low Energy (BLE) 5.0 for initial device setup: pairing the appliance with a user's mobile app and provisioning WiFi credentials. BLE is not used during cooking — all real-time communication happens over WiFi (REST, WebSocket, MQTT). The CM5's built-in Bluetooth 5.0 radio handles BLE advertising and GATT services.

---

## BLE Architecture

```
┌──────────────────┐          BLE 5.0           ┌──────────────────┐
│   Mobile App     │◄──────────────────────────►│   Epicura CM5    │
│   (Central)      │                            │   (Peripheral)   │
│                  │                            │                  │
│  ┌────────────┐  │                            │  ┌────────────┐  │
│  │ BLE Manager│  │   GATT Read/Write/Notify   │  │ BLE Server │  │
│  │ (CoreBT /  │  │                            │  │ (BlueZ)    │  │
│  │ Companion  │  │                            │  │            │  │
│  │ Device Mgr)│  │                            │  │ 3 Services │  │
│  └────────────┘  │                            │  └────────────┘  │
└──────────────────┘                            └──────────────────┘
```

---

## GATT Services

### Service 1: Device Information

**Service UUID:** `0000180A-0000-1000-8000-00805F9B34FB` (standard Device Information)

Provides read-only device identification and status.

| Characteristic | UUID | Properties | Format | Description |
|---------------|------|------------|--------|-------------|
| Device ID | `E001DA01-...` | Read | UTF-8 | Hardware device ID (e.g., `EPIC-001`) |
| Serial Number | `E001DA02-...` | Read | UTF-8 | Manufacturing serial |
| Firmware Version | `E001DA03-...` | Read | UTF-8 | CM5 firmware version string |
| Device Status | `E001DA04-...` | Read, Notify | UTF-8 | `setup`, `ready`, `cooking`, `error` |
| Pairing Code | `E001DA05-...` | Read | UTF-8 | 6-digit code for cloud pairing (rotated every 5 minutes) |

**Full Custom UUIDs:**

| Short | Full UUID |
|-------|-----------|
| `E001DA01` | `E001DA01-EPIC-4C5F-A123-456789ABCDEF` |
| `E001DA02` | `E001DA02-EPIC-4C5F-A123-456789ABCDEF` |
| `E001DA03` | `E001DA03-EPIC-4C5F-A123-456789ABCDEF` |
| `E001DA04` | `E001DA04-EPIC-4C5F-A123-456789ABCDEF` |
| `E001DA05` | `E001DA05-EPIC-4C5F-A123-456789ABCDEF` |

---

### Service 2: WiFi Provisioning

**Service UUID:** `E002WIFI-EPIC-4C5F-A123-456789ABCDEF`

Allows the mobile app to configure the CM5's WiFi connection during initial setup.

| Characteristic | UUID | Properties | Format | Description |
|---------------|------|------------|--------|-------------|
| SSID | `E002WF01-...` | Write | UTF-8 | WiFi network name (max 32 bytes) |
| Password | `E002WF02-...` | Write | AES-128 encrypted | WiFi password (encrypted with shared key) |
| WiFi Status | `E002WF03-...` | Read, Notify | uint8 | `0`: disconnected, `1`: connecting, `2`: connected, `3`: failed |
| IP Address | `E002WF04-...` | Read | UTF-8 | Assigned IP address (available after connected) |
| Error Message | `E002WF05-...` | Read | UTF-8 | Error description if connection failed |

**WiFi Password Encryption:**

The WiFi password is encrypted before writing to the BLE characteristic to prevent eavesdropping:

1. Mobile app reads the `Pairing Code` from Device Information service
2. App derives AES-128 key from: `SHA256(pairing_code + device_id)` truncated to 16 bytes
3. App encrypts the WiFi password using AES-128-CBC with random IV
4. App writes `IV (16 bytes) + ciphertext` to the Password characteristic
5. CM5 decrypts using the same derived key

---

### Service 3: Cooking Control (Limited)

**Service UUID:** `E003COOK-EPIC-4C5F-A123-456789ABCDEF`

Minimal cooking control for cases where WiFi is not yet configured. Primary cooking control happens over WiFi (REST/WebSocket).

| Characteristic | UUID | Properties | Format | Description |
|---------------|------|------------|--------|-------------|
| Start Cook | `E003CK01-...` | Write | uint8 | Write recipe index (0-255) to start cooking |
| Stop Cook | `E003CK02-...` | Write | uint8 | Write `1` to emergency stop |
| Cook Status | `E003CK03-...` | Read, Notify | JSON (UTF-8) | Compact status: `{"s":"cooking","t":148,"p":42}` |
| Temperature | `E003CK04-...` | Read, Notify | int16 | Current temperature in 0.1°C units (e.g., 1485 = 148.5°C) |

**Note:** BLE cooking control is limited to basic start/stop and status monitoring. Full features (recipe browsing, camera feed, detailed progress) require WiFi connection.

---

## Pairing Flow

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  Mobile  │                    │ Epicura  │                    │  Cloud   │
│   App    │                    │   CM5    │                    │   API    │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. Scan for BLE devices      │                               │
     │  (filter: "Epicura-XXXX")     │                               │
     │──────────────────────────────►│                               │
     │                               │                               │
     │  2. Connect BLE               │                               │
     │──────────────────────────────►│                               │
     │                               │                               │
     │  3. LESC Pairing (Just Works) │                               │
     │◄─────────────────────────────►│                               │
     │                               │                               │
     │  4. Read Device ID + Serial   │                               │
     │◄──────────────────────────────│                               │
     │                               │                               │
     │  5. Read Pairing Code         │                               │
     │◄──────────────────────────────│                               │
     │                               │                               │
     │  6. Display: "Pairing code    │                               │
     │     shown on Epicura screen:  │                               │
     │     482917. Match?"           │                               │
     │  [User confirms on both       │                               │
     │   app and device screen]      │                               │
     │                               │                               │
     │  7. Write WiFi SSID           │                               │
     │──────────────────────────────►│                               │
     │                               │                               │
     │  8. Write WiFi Password (enc) │                               │
     │──────────────────────────────►│                               │
     │                               │                               │
     │  9. Subscribe WiFi Status     │  10. CM5 connects to WiFi     │
     │──────────────────────────────►│──────────────────────────────►│
     │                               │       (network)               │
     │  11. Notify: status=connected │                               │
     │◄──────────────────────────────│                               │
     │                               │                               │
     │  12. Read IP Address          │                               │
     │◄──────────────────────────────│                               │
     │                               │                               │
     │  13. POST /appliances/pair    │                               │
     │  {pairing_code: "482917"}     │                               │
     │───────────────────────────────┼──────────────────────────────►│
     │                               │                               │
     │  14. Appliance linked to user │                               │
     │◄──────────────────────────────┼───────────────────────────────│
     │                               │                               │
     │  15. Disconnect BLE           │                               │
     │  (all further comms via WiFi) │                               │
     │──────────────────────────────►│                               │
```

### Pairing Steps Summary

| Step | Action | Channel |
|------|--------|---------|
| 1-3 | BLE discovery and connection | BLE |
| 4-6 | Device identification and code verification | BLE |
| 7-8 | WiFi credential provisioning | BLE |
| 9-12 | WiFi connection and IP retrieval | BLE + WiFi |
| 13-14 | Cloud account linking | HTTPS |
| 15 | BLE disconnect (WiFi takes over) | BLE |

---

## BLE Advertising

### Advertising Data

| Field | Value |
|-------|-------|
| Local Name | `Epicura-{last 4 of device_id}` (e.g., `Epicura-0001`) |
| Service UUIDs | `E002WIFI-EPIC-4C5F-A123-456789ABCDEF` (WiFi Provisioning) |
| Tx Power Level | 0 dBm |
| Advertising Interval | 100-200 ms (fast during setup mode) |
| Connectable | Yes |

### Advertising Modes

| Mode | When | Interval | Duration |
|------|------|----------|----------|
| **Fast** | First 2 minutes after power-on or setup button press | 100 ms | 2 minutes |
| **Slow** | After fast advertising period | 1000 ms | Indefinite |
| **Off** | After WiFi configured and device paired | — | BLE advertising stops |

The CM5 stops BLE advertising once WiFi is configured and the device is paired. BLE can be re-enabled by pressing a physical "Setup" button on the device or via the touchscreen Settings menu.

---

## Security

### BLE Security

| Feature | Configuration |
|---------|---------------|
| **Pairing** | LE Secure Connections (LESC) |
| **Association** | Just Works (no PIN entry — pairing code verified separately via cloud API) |
| **Encryption** | AES-128-CCM (BLE 5.0 standard) |
| **Bond** | Not required (BLE is only used during setup) |
| **MTU** | Negotiated to 247 bytes for efficient data transfer |

### WiFi Password Protection

- WiFi password is AES-128-CBC encrypted before BLE transmission
- Encryption key derived from pairing code + device ID (both must be known)
- Pairing code rotates every 5 minutes on the device
- Pairing code displayed on the Epicura touchscreen for physical verification

### Pairing Code Security

- 6-digit random code generated by CM5
- Displayed on the 10" touchscreen — requires physical access to the device
- Rotated every 5 minutes
- Single use: invalidated after successful cloud pairing
- Used to prevent unauthorized pairing by nearby BLE devices

---

## Platform Implementation Notes

### iOS (Core Bluetooth)

- Use `CBCentralManager` for scanning and connection
- Filter scan results by service UUID `E002WIFI-...`
- Handle state restoration for background BLE operations
- Request `NSBluetoothAlwaysUsageDescription` permission
- See [[../12-MobileApps/02-iOS-App|iOS App]] for implementation details

### Android (CompanionDeviceManager)

- Use `CompanionDeviceManager` API (Android 8.0+) for pairing
- Avoids `ACCESS_FINE_LOCATION` permission requirement
- Fall back to `BluetoothLeScanner` for devices < API 26
- Request `BLUETOOTH_CONNECT` and `BLUETOOTH_SCAN` (Android 12+)
- See [[../12-MobileApps/03-Android-App|Android App]] for implementation details

---

## Related Documentation

- [[01-REST-API-Reference|REST API Reference]] - `POST /appliances/pair` endpoint
- [[02-WebSocket-Events|WebSocket Events]] - WiFi-based real-time communication
- [[03-MQTT-Topics|MQTT Topics]] - Device telemetry after WiFi connected
- [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] - BLE manager architecture
- [[../12-MobileApps/02-iOS-App|iOS App]] - Core Bluetooth implementation
- [[../12-MobileApps/03-Android-App|Android App]] - CompanionDeviceManager implementation

#epicura #ble #bluetooth #pairing #wifi-provisioning #api

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
