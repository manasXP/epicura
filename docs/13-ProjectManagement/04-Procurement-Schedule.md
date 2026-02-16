---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# Procurement Schedule

## Overview

This document provides a detailed procurement schedule for all hardware components required across the Epicura prototype development. Components are organized by sprint with specific part numbers, suppliers, lead times, and order windows.

**Key Principles:**
- Order long-lead items (4+ weeks) immediately
- Batch orders to same supplier to save shipping
- Order 2x critical single-point-of-failure components
- PCB fabrication starts 6 weeks before Sprint 1

---

## Procurement Timeline

```
Week -6: PCB designs complete → submit to JLCPCB
Week -3: PCB assembly complete → ship
Week -1: PCBs arrive → begin testing
Week 0: Sprint 1 starts with tested PCBs ready
```

---

## Pre-Sprint Phase: PCB Components

### Order Window: Week -8 to Week -6 (URGENT - Start Now)

#### Controller PCB Components

| Ref | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|-----|-------------|-------------|-----|----------|-----------|-----------|----------|
| U1 | STM32G474RET6 | MCU, LQFP-64, 170MHz | 2 | Mouser 511-STM32G474RET6 | $8.50 | 2-3 weeks | Week -8 |
| U2 | AMS1117-3.3 | LDO 3.3V 800mA SOT-223 | 5 | Mouser 926-AMS1117-3.3 | $0.35 | 1 week | Week -7 |
| Y1 | ABM8G-8.000MHZ-4Y-T3 | Crystal 8MHz 18pF SMD | 5 | Digikey 535-13917-1-ND | $0.28 | 1 week | Week -7 |
| Y2 | ABS07-32.768KHZ-T | Crystal 32.768kHz 12.5pF | 5 | Digikey 535-9122-1-ND | $0.42 | 1 week | Week -7 |
| Q1 | 2N7002 | N-MOSFET 60V SOT-23 | 10 | Mouser 512-2N7002 | $0.08 | 1 week | Week -7 |
| D1 | LTST-C150GKT | LED Green 0603 | 10 | Digikey 160-1169-1-ND | $0.18 | 1 week | Week -7 |
| D2 | 1N4148WS | Diode 100V SOD-323 | 10 | Mouser 512-1N4148WS | $0.06 | 1 week | Week -7 |
| D3 | PRTR5V0U2X | ESD Protection SOT-143B | 5 | Mouser 771-PRTR5V0U2X115 | $0.22 | 1 week | Week -7 |
| FB1 | BLM18PG601SN1D | Ferrite Bead 600R 0603 | 10 | Mouser 81-BLM18PG601SN1D | $0.08 | 1 week | Week -7 |
| - | Resistor Kit 0402 | 1% kit (1k-1M) | 1 kit | Amazon B07QJ8TW6S | $15 | 3 days | Week -7 |
| - | Capacitor Kit 0402/0805 | Ceramic MLCC kit | 1 kit | Amazon B07PBBX9V3 | $18 | 3 days | Week -7 |
| J1 | SM06B-SRSS-TB(LF)(SN) | JST-SH 6-pin 1.0mm | 5 | Digikey 455-1802-1-ND | $0.35 | 1 week | Week -7 |
| J2-J11 | JST-XH connector kit | 2-pin to 6-pin 2.5mm | 1 kit | Amazon B01MCZE2HM | $12 | 3 days | Week -7 |
| J9 | 20021321-00010T4LF | Pin header 2x5 1.27mm | 5 | Digikey 609-3711-ND | $0.65 | 1 week | Week -7 |
| PCB | Custom 4L 160x90mm | FR4 ENIG 1.6mm | 10 | JLCPCB | $9/ea | 3-4 weeks | Week -6 |

**Controller PCB Component Total:** ~$115 (with 2x critical ICs, 10 PCBs)

---

#### Driver PCB Components

| Ref | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|-----|-------------|-------------|-----|----------|-----------|-----------|----------|
| U1-U3 | MP1584EN-LF-Z | Buck Converter 24V 3A SOT-23-8 | 10 | Mouser 946-MP1584EN-LF-Z | $0.95 | 2 weeks | Week -8 |
| L1 | CDRH104R-330MC | Inductor 33µH 4.5A 10x10mm | 5 | Mouser 81-CDRH104R-330MC | $0.68 | 1 week | Week -7 |
| L2-L3 | CDRH104R-220MC | Inductor 22µH 5A 10x10mm | 10 | Mouser 81-CDRH104R-220MC | $0.62 | 1 week | Week -7 |
| U4-U5 | DRV8876RGTR | H-Bridge 3.5A WSON-8 | 5 | Mouser 595-DRV8876RGTR | $2.85 | 2-3 weeks | Week -8 |
| U6 | TB6612FNG(O,EL) | Dual H-Bridge SSOP-24 | 5 | Mouser 757-TB6612FNGOCEL | $1.68 | 2 weeks | Week -8 |
| Q1-Q3 | IRLML6344TRPBF | N-MOSFET 30V SOT-23 | 15 | Mouser 942-IRLML6344TRPBF | $0.28 | 1 week | Week -7 |
| Q4-Q5 | 2N7002 | N-MOSFET 60V SOT-23 | 10 | Mouser 512-2N7002 | $0.08 | 1 week | Week -7 |
| U7 | INA219BIDR | Current Monitor SOT-23-8 | 5 | Mouser 595-INA219BIDR | $1.72 | 1-2 weeks | Week -7 |
| R_SHUNT | WSL25121L000FEA | Shunt 10mΩ 1% 1W 2512 | 5 | Mouser 71-WSL25121L000FEA | $0.52 | 1 week | Week -7 |
| F1 | 0ZCJ0050FF2G | Polyfuse 5A 1812 | 10 | Mouser 576-0ZCJ0050FF2G | $0.58 | 1 week | Week -7 |
| D1 | SS54-E3/5AT | Schottky 5A 40V SMA | 10 | Mouser 625-SS54-E3 | $0.32 | 1 week | Week -7 |
| D2 | SMBJ24A-E3/52 | TVS 24V 600W SMB | 5 | Mouser 625-SMBJ24A-E3 | $0.38 | 1 week | Week -7 |
| D6-D8 | SS14-E3/5AT | Schottky 1A 40V SMA | 15 | Mouser 625-SS14-E3 | $0.18 | 1 week | Week -7 |
| - | Electrolytic Cap Kit | 10µF-470µF radial | 1 kit | Amazon B07PQKD4Y5 | $16 | 3 days | Week -7 |
| J_STACK | Headers 2x20 11mm stack | Socket + pin header | 5 sets | Amazon B07C89T16T | $12/set | 5 days | Week -7 |
| J_24V_IN | XT30U-F | XT30 female connector | 10 | Amazon B07TFJL65P | $8/10 | 3 days | Week -7 |
| PCB | Custom 4L 160x90mm 2oz Cu | FR4 ENIG 1.6mm | 10 | JLCPCB | $11/ea | 3-4 weeks | Week -6 |

**Driver PCB Component Total:** ~$180 (with spares, 10 PCBs)

---

#### CM5IO Board (CM5 Carrier) Components

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| PCB | Custom 4L 160x90mm | FR4 ENIG, CM5 footprint | 5 | JLCPCB | $15/ea | 3-4 weeks | Week -6 |
| - | CM5 carrier reference BOM | Connectors, power, GPIO | 1 | Mouser/Digikey | $80 | 1-2 weeks | Week -7 |

**CM5IO Total:** ~$155 (5 boards + components)

---

### PCB Fabrication Order (Week -6)

| Board | Specs | Quantity | Unit Cost | Total | Fabricator | Lead Time |
|-------|-------|----------|-----------|-------|------------|-----------|
| Controller PCB | 4L, 160x90mm, ENIG, 1oz Cu | 10 | $9 | $90 | JLCPCB | 3-4 weeks |
| Driver PCB | 4L, 160x90mm, ENIG, 2oz Cu outer | 10 | $11 | $110 | JLCPCB | 3-4 weeks |
| CM5IO Board | 4L, 160x90mm, ENIG, 1oz Cu | 5 | $15 | $75 | JLCPCB | 3-4 weeks |

**PCB Fabrication Total:** $275 (includes shipping DHL Express ~$30)

**Pre-Sprint Phase Total Cost:** ~$725

---

## Sprint 1 (Weeks 1-2): Foundation Components

### Order Window: Week -4 to Week 0

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| Raspberry Pi CM5 4GB | CM5004000 | Compute Module 5, 4GB RAM | 2 | Approved RPi Distributor | $45 | 2-4 weeks | Week -4 |
| CM5 IO Board | CM5IO | Official IO board (if not using CM5IO) | 1 | Approved RPi Distributor | $20 | 2-4 weeks | Week -4 |
| microSD Card | SDSQXAV-032G-GN6MA | SanDisk Extreme 32GB | 2 | Amazon B06XWMQ81P | $8 | 2 days | Week 0 |
| USB-C Power Supply | T6716DV | Anker 30W PD USB-C | 1 | Amazon B08T5QVTKW | $18 | 2 days | Week 0 |
| NUCLEO-G474RE | NUCLEO-G474RE | STM32 dev board (backup) | 1 | Mouser 511-NUCLEO-G474RE | $18 | 1-2 weeks | Week -2 |
| Jumper Wire Kit | - | Dupont M-F, M-M, F-F | 1 kit | Amazon B01EV70C78 | $7 | 2 days | Week 0 |

**Sprint 1 Total:** ~$157

---

## Sprint 2 (Weeks 3-4): Power & Thermal

### Order Window: Week -2 to Week 1

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| Mean Well PSU | LRS-75-24 | 24V 3.2A 76.8W enclosed | 2 | Mouser 709-LRS7524 | $18 | 1-2 weeks | Week -2 |
| Induction Surface | - | Microwave induction hob with CAN | 1 | AliExpress / Taobao | $60 | 3-4 weeks | Week -2 |
| CAN Transceiver | SN65HVD230DR | 3.3V CAN transceiver SO-8 | 5 | Mouser 595-SN65HVD230DR | $0.82 | 1 week | Week 0 |
| MLX90614ESF-BAA | MLX90614ESF-BAA-000-TU | IR Thermometer -40 to 125°C | 2 | Mouser 527-MLX90614ESFBAA | $11.50 | 2-3 weeks | Week -2 |
| 120Ω Resistor | - | 1/4W through-hole | 5 | Mouser (from kit) | - | - | - |
| Omron Relay | G5V-2-H1-DC5 | DPDT 5V 1A PCB mount | 2 | Mouser 653-G5V-2-H1DC5 | $3.20 | 1 week | Week 0 |
| Bench PSU (optional) | HY3005D | 30V 5A dual supply | 1 | Amazon B07C3D25QM | $90 | 5 days | Week 0 |

**Sprint 2 Total:** ~$218 (includes bench PSU; ~$128 without)

---

## Sprint 3 (Weeks 5-6): Thermal Control

### Order Window: Week 1 to Week 3

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| NTC Thermistor | NTCLE100E3103JB0 | 100K 1% 3950K radial | 5 | Mouser 594-2381-640-65103 | $0.45 | 1 week | Week 2 |
| Thermal Fuse | 240C 10A | Axial thermal cutoff | 2 | Mouser 576-240C10A | $2.80 | 1 week | Week 2 |
| E-Stop Button | XB4BS8442 | 22mm NC emergency stop red | 1 | Mouser 584-XB4BS8442 | $12 | 2 weeks | Week 1 |
| Test Pot | - | SS304 3L flat-bottom | 1 | Amazon B08XXXXX | $20 | 3 days | Week 4 |
| Reference Thermometer | TP3001 | Digital probe -50 to 300°C | 1 | Amazon B01IHHLB3W | $32 | 3 days | Week 4 |

**Sprint 3 Total:** ~$71

---

## Sprint 4 (Weeks 7-8): Robotic Arm

### Order Window: Week 3 to Week 5

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| DS3225 Servo | DS3225MG | 25kg·cm metal gear 270° | 2 | Amazon B07VPFR7KZ | $15 | 5 days | Week 6 |
| SS304 Shaft | - | 8mm dia x 250mm, SS304 rod | 1 | McMaster-Carr 8893K26 | $12 | 1 week | Week 5 |
| Silicone Paddle | - | Food-grade silicone spatula blade | 2 | Amazon B08XXXXX | $8 | 3 days | Week 6 |
| Aluminum Bracket | 6061-T6 | 3mm x 50mm x 100mm plate | 1 | McMaster-Carr 9246K12 | $15 | 1 week | Week 5 |
| M3 Fastener Kit | - | M3 bolts, nuts, washers, 240pc | 1 | Amazon B07CYNKLT2 | $10 | 2 days | Week 6 |
| PETG Filament | - | 1kg white PETG | 1 | Amazon B07PGZNM34 | $25 | 2 days | Week 6 |

**Sprint 4 Total:** ~$100

---

## Sprint 5 (Weeks 9-10): Load Cells

### Order Window: Week 5 to Week 7

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| Load Cell | CZL635-5kg | S-beam 5kg strain gauge | 4 | AliExpress | $4/ea | 2-3 weeks | Week 5 |
| HX711 Module | HX711 | 24-bit ADC breakout red PCB | 2 | Amazon B01LXKPEJR | $7/2 | 3 days | Week 8 |
| Load Cell Combinator | - | Wheatstone junction PCB | 1 | Amazon B075317R45 | $8 | 5 days | Week 8 |
| Calibration Weights | M1 | 500g, 1kg, 2kg, 3kg cast iron | 1 set | Amazon B0875SXXXX | $40 | 1 week | Week 7 |
| Aluminum Plate | 6061-T6 | 5mm x 200mm x 200mm | 1 | McMaster-Carr 9246K16 | $28 | 1 week | Week 7 |

**Sprint 5 Total:** ~$107

---

## Sprint 6 (Weeks 11-12): Computer Vision

### Order Window: Week 7 to Week 9

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| IMX219 Camera | IMX219-160 | 8MP 160° FOV CSI-2 | 2 | Amazon B07T43K741 | $25 | 1 week | Week 9 |
| WS2812B LED Ring | - | 12-LED NeoPixel RGB 37mm | 2 | Adafruit 1643 | $7.50 | 3 days | Week 10 |
| CSI Ribbon Cable | - | 15-pin 100mm flex cable | 2 | Adafruit 1648 | $2.95 | 3 days | Week 10 |
| Diffuser Material | - | Translucent acrylic sheet | 1 | Amazon B07XXXXX | $8 | 3 days | Week 10 |

**Sprint 6 Total:** ~$76

---

## Sprint 7 (Weeks 13-14): CV Training

### Order Window: Week 9 to Week 11

| Item | Description | Qty | Supplier | Cost | Lead Time | Order By |
|------|-------------|-----|----------|------|-----------|----------|
| Training Ingredients | Rice, dal, spices, veg (20 cooks) | - | Local grocery | $80 | Weekly | Week 11-14 |
| Cloud GPU Credits | Google Colab Pro or AWS | 2 months | Google/AWS | $20/mo | Instant | Week 11 |

**Sprint 7 Total:** ~$120

---

## Sprint 9 (Weeks 17-18): Dispensing

### Order Window: Week 13 to Week 15

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| SG90 Servo (ASD) | SG90 | 9g micro servo 180° | 4 | Amazon B07L2SF3R4 | $1.80/ea | 5 days | Week 16 |
| 12V Linear Actuator (CID) | Generic 50mm stroke | 12V DC, 20-50N | 2 | AliExpress | $8/ea | 10 days | Week 15 |
| Peristaltic Pump (SLD) | Generic 12V DC | 5-50 mL/min, silicone tube | 2 | AliExpress | $10/ea | 10 days | Week 15 |
| 12V NC Solenoid Valve (SLD) | Generic | Normally closed, spring return | 2 | Amazon | $4/ea | 5 days | Week 16 |
| 1 kg Load Cell + HX711 (SLD) | Generic | Strain gauge + 24-bit ADC | 1 | Amazon | $8 | 5 days | Week 16 |
| PETG Filament | - | 1kg natural PETG | 1 | Amazon B07PGZNM34 | $25 | 2 days | Week 16 |

**Sprint 9 Total:** ~$90

---

## Sprint 10 (Weeks 19-20): UI Display

### Order Window: Week 15 to Week 17

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| 10.1" Display | - | 1280x800 capacitive DSI/HDMI | 1 | Waveshare / Amazon | $80 | 2 weeks | Week 15 |

**Sprint 10 Total:** ~$80

---

## Sprint 11 (Weeks 21-22): Integration

### Order Window: Week 17 to Week 19

| Item | Description | Qty | Supplier | Cost | Lead Time | Order By |
|------|-------------|-----|----------|------|-----------|----------|
| Enclosure Filament | 3kg PETG black + white | 3 kg | Amazon | $75 | 3 days | Week 19 |
| Cook Test Ingredients | 25 cook sessions | - | Local grocery | $100 | Weekly | Week 19-22 |

**Sprint 11 Total:** ~$175

---

## Sprint 12 (Weeks 23-24): Validation

### Order Window: Week 19 to Week 21

| Item | Part Number | Description | Qty | Supplier | Unit Cost | Lead Time | Order By |
|------|-------------|-------------|-----|----------|-----------|-----------|----------|
| Thermal Camera Rental | FLIR E5-XT | 160x120 IR camera rental | 1 week | Test Equipment Rental | $200/wk | 3 days | Week 22 |
| Power Meter | P3 P4400 | Kill-A-Watt power meter | 1 | Amazon B00009MDBU | $28 | 2 days | Week 22 |
| Endurance Ingredients | 50+ cook sessions | - | Local grocery | $150 | Weekly | Week 21-24 |

**Sprint 12 Total:** ~$378

---

## Consolidated Supplier Order Summary

### Mouser Electronics (Order Week -8, -7, 0)

**Order 1 (Week -8): Long-lead ICs**
- STM32G474RET6 (2x) - $17.00
- DRV8876RGTR (5x) - $14.25
- TB6612FNG (5x) - $8.40
- MP1584EN (10x) - $9.50
- **Subtotal:** ~$50 + shipping $8 = **$58**

**Order 2 (Week -7): Passives & Connectors**
- All resistors, capacitors, inductors, connectors from BOM
- **Subtotal:** ~$120 + combine with Order 1 if possible

**Order 3 (Week 0-2): Sensors & Power**
- MLX90614 (2x), Relay, PSU, CAN transceiver
- **Subtotal:** ~$50 + $8 shipping = **$58**

**Total Mouser Orders:** ~$228

---

### Amazon (Ongoing)

**Week -7:**
- Resistor kit, capacitor kit, JST connector kit, XT30 connectors
- **Subtotal:** ~$65 (Prime shipping)

**Week 0:**
- microSD cards, USB-C PSU, jumper wires
- **Subtotal:** ~$35

**Week 4-6:**
- Test pot, thermometer, servo, filament, fasteners
- **Subtotal:** ~$100

**Week 8-10:**
- Load cell accessories, camera, LED ring
- **Subtotal:** ~$85

**Week 16-20:**
- SG90 servos, display, filament
- **Subtotal:** ~$140

**Total Amazon Orders:** ~$425

---

### JLCPCB (Order Week -6)

**Single Combined Order:**
- Controller PCB 4L 160x90mm ENIG (10 pcs)
- Driver PCB 4L 160x90mm ENIG 2oz Cu (10 pcs)
- CM5IO PCB 4L 160x90mm ENIG (5 pcs)
- Assembly service (optional): add $150-300
- DHL Express shipping: $30
- **Total:** $275 PCBs only, **$425-575 with assembly**

---

### McMaster-Carr (Order Week 5, 7)

**Week 5:**
- SS304 shaft 8mm x 250mm
- 6061-T6 aluminum bracket material
- **Subtotal:** ~$30 + $8 shipping = **$38**

**Week 7:**
- 6061-T6 aluminum platform plate 200x200x5mm
- **Subtotal:** ~$28 + $8 shipping = **$36**

**Total McMaster:** ~$74

---

### AliExpress / Alibaba (Order Week -2, Week 5)

**Week -2:**
- Commercial microwave induction surface with CAN port
- **Subtotal:** $60 + $15 shipping (ePacket 3-4 weeks) = **$75**

**Week 5:**
- CZL635 load cells (4x)
- **Subtotal:** $16 + $8 shipping = **$24**

**Total AliExpress:** ~$99

---

### Adafruit (Order Week 10)

**Week 10:**
- WS2812B LED ring (2x) - $15
- CSI ribbon cables (2x) - $6
- **Subtotal:** $21 + $5 shipping = **$26**

---

### Local Grocery (Weekly Weeks 11-24)

**Ongoing ingredient purchases:**
- Sprint 7: $80 (training data)
- Sprint 11: $100 (integration testing)
- Sprint 12: $150 (endurance testing)
- **Total:** ~$330

---

## Total Procurement Budget Summary

| Supplier | Subtotal | Shipping | Total | % of Budget |
|----------|----------|----------|-------|-------------|
| JLCPCB (PCBs only) | $275 | Included | **$275** | 12% |
| Mouser Electronics | $228 | $16 | **$244** | 11% |
| Amazon | $425 | Free (Prime) | **$425** | 19% |
| McMaster-Carr | $58 | $16 | **$74** | 3% |
| AliExpress | $76 | $23 | **$99** | 4% |
| Adafruit | $21 | $5 | **$26** | 1% |
| Local Grocery | $330 | - | **$330** | 15% |
| Test Equipment Rental | $200 | - | **$200** | 9% |
| Cloud Compute | $40 | - | **$40** | 2% |
| **TOTAL** | | | **$1,713** | **76%** |
| **Contingency (20%)** | | | **$343** | **15%** |
| **Tools (if needed)** | | | **$200** | **9%** |
| **GRAND TOTAL** | | | **$2,256** | **100%** |

---

## Critical Path Items (Order Immediately)

### Week -8 to Week -6: MUST ORDER NOW

| Item | Lead Time | Impact if Delayed |
|------|-----------|-------------------|
| **Raspberry Pi CM5** | 2-4 weeks | Sprint 1 blocked entirely |
| **STM32G474RET6** | 2-3 weeks | Can use Nucleo as backup, but custom PCB testing delayed |
| **DRV8876, TB6612FNG** | 2-3 weeks | Driver PCB cannot be tested, Sprint 9+ blocked |
| **Microwave Induction Surface** | 3-4 weeks | Sprint 2-3 blocked, critical path |
| **MLX90614 IR Thermometer** | 2-3 weeks | Sprint 2-3 blocked, thermal control impossible |
| **JLCPCB PCB Order** | 3-4 weeks | All sprints after Sprint 1 severely impacted |
| **Load Cells CZL635** | 2-3 weeks | Sprint 5 blocked |

**Action Required:** Place orders for all items above within next 3 days to maintain schedule.

---

## Procurement Checklist

### Week -8
- [ ] Order Raspberry Pi CM5 (2x) from approved distributor
- [ ] Order STM32G474RET6, DRV8876, TB6612FNG, MP1584EN from Mouser
- [ ] Order microwave induction surface from AliExpress

### Week -7
- [ ] Order all passive components (resistors, caps, inductors) from Mouser
- [ ] Order connector kits from Amazon
- [ ] Order MLX90614, load cells from respective suppliers
- [ ] Finalize CM5IO board BOM and add to Mouser cart

### Week -6
- [ ] Submit PCB fabrication order to JLCPCB (Controller + Driver + CM5IO)
- [ ] Decide on assembly service (add $150-300 but saves 2-3 days)
- [ ] Verify all component inventories match PCB BOM

### Week -4 to Week 0
- [ ] Track PCB shipment (DHL tracking)
- [ ] Order Sprint 1 items (microSD, PSU, cables)
- [ ] Prepare Yocto build environment on workstation

### Week 0 (Sprint 1 Start)
- [ ] Receive and inspect PCBs
- [ ] Visual inspection and continuity testing
- [ ] Power-on testing with bench supply

### Weeks 1-24
- [ ] Follow sprint-specific procurement windows above
- [ ] Monitor component inventory
- [ ] Re-order consumables (filament, ingredients) as needed

---

## Supplier Contact Information

### Electronics Distributors

**Mouser Electronics**
- Website: mouser.com
- Phone: 1-800-346-6873
- Shipping: $7.99 (2-day), free over $50
- Payment: Net 30 for business accounts

**Digikey**
- Website: digikey.com
- Phone: 1-800-344-4539
- Shipping: $8 (overnight available)
- Payment: Net 30 for business accounts

**Adafruit**
- Website: adafruit.com
- Shipping: $5-8 (USPS), UPS available
- Payment: Credit card, PayPal

### PCB Fabrication

**JLCPCB**
- Website: jlcpcb.com
- Support: support@jlcpcb.com
- Lead time: 24h production + 3-4 days shipping (DHL)
- Payment: Credit card, PayPal
- Min order: 5 pcs

**PCBWay** (backup)
- Website: pcbway.com
- Support: support@pcbway.com
- Lead time: 3-5 days production + shipping
- Payment: Credit card, PayPal, wire transfer

### Mechanical Components

**McMaster-Carr**
- Website: mcmaster.com
- Phone: 1-630-833-0300
- Shipping: Next-day available, $8 standard
- Payment: Credit card, Net 30

### Asia Sourcing

**AliExpress**
- Website: aliexpress.com
- Shipping: ePacket (15-30 days), DHL (5-7 days +$20)
- Payment: Credit card, PayPal
- Buyer protection: 60 days

**Alibaba** (for volume orders)
- Website: alibaba.com
- Contact suppliers directly for quotes
- MOQ typically 10-100 units

---

## Related Documentation

- [[03-Sprints|Sprint Planning]]
- [[02-Stories|User Stories]]
- [[05-Resource-Allocation|Resource Allocation]]
- [[../08-Components/04-Total-Component-Cost|Total Component Cost]]
- [[../09-PCB/01-Controller-PCB-Design|Controller PCB Design]]
- [[../09-PCB/02-Driver-PCB-Design|Driver PCB Design]]

---

#epicura #procurement #schedule #bom #logistics #suppliers

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |
