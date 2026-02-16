---
created: 2026-02-16
modified: 2026-02-16
version: 1.0
status: Draft
tags: [epicura, warranty, support, service, installation]
---

# Epicura — Installation, Warranty, Support & Service Plan

## Overview

This document covers the end-to-end customer experience from purchase to ongoing support for all Epicura product tiers: Lite ($399), Standard ($499), Pro ($599), and Pro Multipot ($799). It defines the installation journey, warranty structure, support channels, remote diagnostics, field service model, and service cost projections.

---

## 1. Customer Installation Journey

### 1.1 Purchase-to-First-Cook Flow

```mermaid
flowchart LR
    A["🛒 Purchase\n(Online / Retail)"] --> B["📦 Delivery\n(3–5 days)"]
    B --> C["📂 Unbox & Place\non countertop"]
    C --> D["📱 App Pairing\n(BLE)"]
    D --> E["⚙️ Guided Setup\nWizard"]
    E --> F["🍲 First Cook\n(Demo Recipe)"]
```

### 1.2 Step-by-Step Installation

| Step | Action | Duration | Support |
|---|---|---|---|
| **1. Unbox** | Remove unit, pot, cartridges, power cable, quick-start card from packaging | 5 min | Illustrated quick-start card (multilingual) |
| **2. Place** | Set on countertop near 15A power outlet; ensure 10 cm clearance on all sides for ventilation | 2 min | Footprint guide printed on box flap |
| **3. Power On** | Plug in, press power button; unit runs self-test (display lights up, arm homes, fan spins) | 1 min | On-screen self-test status with pass/fail indicators |
| **4. Download App** | Scan QR code on quick-start card; install Epicura app (iOS/Android) | 2 min | QR links to App Store / Play Store |
| **5. BLE Pairing** | App discovers unit via Bluetooth; tap to pair; unit displays 6-digit confirmation code | 1 min | On-screen + in-app pairing instructions |
| **6. WiFi Setup** | App provisions home WiFi credentials to unit over BLE; unit connects and syncs recipes | 2 min | Supports WPA2/WPA3; fallback to offline mode if no WiFi |
| **7. Account Setup** | Create Epicura account or sign in; set language, dietary preferences, spice tolerance | 3 min | Google/Apple SSO supported |
| **8. Load Consumables** | Insert seasoning cartridges into P-ASD slots, fill oil/water reservoirs in SLD | 5 min | Animated on-screen guide with slot labels |
| **9. First Cook (Demo)** | Guided demo recipe (e.g., "Simple Dal Tadka") walks user through loading ingredients and starting cook | 20-25 min | Step-by-step touchscreen prompts with camera preview |
| **10. Registration** | Unit auto-registers for warranty upon first successful WiFi sync | Automatic | Confirmation email + in-app warranty card |

**Total setup time: ~15 minutes (excluding first cook)**

### 1.3 Installation Modes

| Mode | Description | Target |
|---|---|---|
| **Self-Install** | Default; no technician needed. Quick-start card + in-app wizard + demo recipe | All customers |
| **Video-Assisted** | On-demand video call with support agent who guides setup via customer's phone camera | Elderly / non-tech-savvy customers |
| **White-Glove** | Technician visits home, unboxes, sets up, runs first cook with customer. Available in metro cities | Epicura Pro Multipot buyers (included free); optional add-on for other tiers ($15 / ₹1,249) |

### 1.4 Post-Installation Onboarding

| Day | Trigger | Action |
|---|---|---|
| Day 0 | First cook complete | Push notification: "Your first meal is ready! Rate your experience" |
| Day 1 | App open | Suggest 3 recipes based on dietary preferences |
| Day 3 | No second cook yet | Nudge: "Try Paneer Butter Masala — ready in 25 min" |
| Day 7 | Weekly summary | "You cooked 3 meals this week. Here's what others are cooking" |
| Day 14 | Feature discovery | Introduce meal planning and grocery list features |
| Day 30 | Retention check | "How's Epicura working for you?" — in-app survey + NPS score |

---

## 2. Warranty Structure

### 2.1 Warranty by Tier

| Tier | Standard Warranty | Extended Warranty | Coverage |
|---|---|---|---|
| **Epicura Standard** | 1 year | +1 year ($30 / ₹2,499) | Parts + labor |
| **Epicura Pro** | 2 years (included) | +1 year ($30 / ₹2,499) | Parts + labor + 1 free service visit |
| **Epicura Pro Multipot** | 2 years (included) | +1 year ($40 / ₹3,299) | Parts + labor + 2 free service visits + priority support |

### 2.2 What's Covered vs. Not Covered

| Covered | Not Covered |
|---|---|
| Manufacturing defects in electronics, motors, sensors | Physical damage from drops, water immersion, misuse |
| Induction module failure | Damage from use with non-compatible pots |
| Display defects (dead pixels >5, touch failure) | Cosmetic wear (scratches, discoloration) |
| Servo arm mechanical failure | Consumable wear (cartridges, filters, pot coating) |
| Software/firmware bugs (OTA fixes) | Damage from unauthorized modifications or third-party repairs |
| Camera and sensor malfunction | Power surge damage (surge protector recommended) |
| PCB and wiring defects | Normal wear of moving parts after warranty period |

---

## 3. Support Channels

| Channel | Availability | Response Time | Best For |
|---|---|---|---|
| **In-App Chat** | 24/7 (AI bot) + 8 AM–10 PM IST (human) | AI: instant; Human: <5 min | Recipe help, setup issues, general queries |
| **WhatsApp Support** | 8 AM–10 PM IST | <15 min | Quick troubleshooting, order status |
| **Phone Helpline** | 9 AM–8 PM IST (Mon–Sat) | <2 min wait | Urgent issues, elderly customers |
| **Email** | 24/7 | <24 hours | Detailed complaints, warranty claims |
| **Video Call** | By appointment (9 AM–6 PM IST) | Scheduled | Complex troubleshooting, installation help |
| **Community Forum** | 24/7 | Peer response | Tips, recipes, feature requests |

---

## 4. Remote Diagnostics

Every Epicura unit reports health telemetry via MQTT (when connected to WiFi):

| Diagnostic | Data Collected | Action |
|---|---|---|
| **Induction health** | Coil temperature trends, power draw anomalies, CAN error count | Proactive alert if degradation detected |
| **Servo arm** | Stall count, position accuracy drift, current draw | Flag maintenance before failure |
| **Camera** | Image quality score, lens obstruction detection | Prompt user to clean lens; escalate if hardware fault |
| **Sensor drift** | IR thermometer vs NTC delta, load cell calibration offset | Auto-recalibrate or prompt service visit |
| **Software** | Crash logs, OTA update status, storage usage | Auto-fix via OTA; escalate if persistent |
| **Usage patterns** | Cook count, recipe distribution, error frequency | Identify units needing proactive outreach |

Support agents can (with customer permission) remotely view device diagnostics dashboard to troubleshoot without a site visit — **expected to resolve 70–80% of issues remotely**.

---

## 5. Field Service Model

### 5.1 Service Network Strategy

| Phase | Coverage | Model |
|---|---|---|
| **Year 1** (0–2K units) | 6 metro cities (Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune) | Third-party service partners (appliance repair networks like UrbanClap/Urban Company) |
| **Year 2** (2K–12K units) | 15 cities (add Kolkata, Ahmedabad, Jaipur, Lucknow, Kochi, Chandigarh, Indore, Nagpur, Coimbatore) | Trained authorized service centers (2–3 per city) |
| **Year 3** (12K–42K units) | 30+ cities + Tier-2 coverage | Mix of owned service hubs in top 6 cities + authorized partners elsewhere |

### 5.2 Service Visit Types

| Type | Description | Cost to Customer | SLA |
|---|---|---|---|
| **Warranty Repair** | In-warranty hardware failure | Free | 48 hours in metro; 5 days in Tier-2 |
| **Out-of-Warranty Repair** | Post-warranty hardware fix | Parts at cost + ₹500 labor ($6) | 48–72 hours in metro |
| **Annual Maintenance** | Preventive checkup: recalibrate sensors, clean internals, inspect arm/induction, firmware update | ₹1,499/visit ($18) or included in AMC | Scheduled appointment |
| **Consumable Replacement** | Replace filters, cartridges, pot coating inspection | Consumable cost only (self-service) | N/A (shipped to customer) |
| **Unit Replacement** | DOA or irreparable unit within warranty | Free replacement | 5–7 days |

### 5.3 Spare Parts Strategy

| Approach | Details |
|---|---|
| **Modular design** | Key assemblies (servo arm, induction module, display, camera, P-ASD manifold) are field-replaceable in <30 min |
| **Spare parts inventory** | Top 10 failure-prone parts stocked at regional hubs (Mumbai, Delhi, Bangalore) |
| **Parts pricing** | Published spare parts price list on website; customers can order directly |
| **Right to repair** | Service manual and wiring diagrams available to authorized partners; open-source STM32 firmware for community repairs |

---

## 6. Annual Maintenance Contract (AMC)

| Plan | Price | Includes |
|---|---|---|
| **Basic AMC** | ₹2,999/year ($36) | 1 preventive visit + 10% discount on parts + priority phone support |
| **Comprehensive AMC** | ₹4,999/year ($60) | 2 preventive visits + all parts covered (except pot, cartridges) + priority support + loaner unit for repairs >3 days |

---

## 7. Service Cost Projections

| Metric | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Installed base (cumulative) | 2,000 | 12,000 | 42,000 |
| Expected warranty claims (3% of base/year) | 60 | 360 | 1,260 |
| Avg. warranty repair cost | $25 | $22 | $18 |
| **Total warranty cost** | **$1,500** | **$7,920** | **$22,680** |
| AMC attach rate | 10% | 20% | 30% |
| **AMC revenue** | **$7,200** | **$115,200** | **$756,000** |
| **Net service margin** | **$5,700** | **$107,280** | **$733,320** |

---

## 8. Customer Satisfaction Targets

| Metric | Year 1 Target | Year 3 Target |
|---|---|---|
| NPS (Net Promoter Score) | >40 | >55 |
| First-Contact Resolution Rate | >70% | >85% |
| Average Repair Turnaround (metro) | <72 hours | <48 hours |
| Warranty Claim Rate | <5% | <3% |
| Customer Retention (active monthly users) | >60% | >75% |
| App Store Rating | >4.0 | >4.3 |

---

## Related Documentation

- [[01-Market-Research-Report|Market Research Report]]
- [[../docs/01-Overview/01-Project-Overview|Project Overview]]
- [[../docs/08-Components/04-Total-Component-Cost|Total Component Cost]]
- [[../docs/04-UserInterface/01-UI-UX-Design|UI/UX Design]]
- [[../docs/11-API/04-BLE-Services|BLE Services]]

---

#epicura #warranty #support #service #installation
