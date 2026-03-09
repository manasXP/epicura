# Arduino UNO Q — 1000-Unit Batch Manufacturing Cost Estimate

**Board:** 68.58 × 53.34 mm | **Variant:** ABX00162 (2 GB RAM, 16 GB eMMC)
**Retail price:** $41 (for context)

---

### BOM — Component Costs at 1000 Units

| # | Component | Designator | Est. Unit Cost | Notes |
|---|-----------|------------|---------------|-------|
| 1 | **Qualcomm QRB2210 SoC** (quad-core A53 + Adreno 702) | SOC1 | **$13.00** | Largest uncertainty — not sold through standard distributors; estimate based on comparable Qualcomm IoT SoCs |
| 2 | **STM32U585** (Cortex-M33, UFBGA132) | MCU1 | **$6.00** | ~$4.30 at 125+ units for smaller package; BGA variant slightly more |
| 3 | **LPDDR4X 2 GB** (single-rank 32-bit) | DRAM1 | **$4.50** | Micron/SK Hynix at 1k units |
| 4 | **16 GB eMMC** (JEDEC 5.1) | EMMC1 | **$5.00** | Kioxia/Samsung tier-1 supplier |
| 5 | **WCBN3536A** (WCN3980, Wi-Fi 5 + BT 5.1 module) | U2901 | **$4.00** | Qualcomm module; semi-proprietary supply chain |
| 6 | **ANX7625** (MIPI-DSI → USB-C/DP Alt-Mode bridge) | U3001 | **$2.50** | Analogix chip |
| 7 | **PM4125 PMIC** (LDO + multi-rail buck) | PMIC1 | **$2.00** | Qualcomm PMIC |
| 8 | **P-channel MOSFET** (VBUS back-drive protection) | Q2801 | **$0.20** | Standard power MOSFET |
| 9 | **8×13 LED matrix** (104× blue SMD LEDs) | D27001–D27104 | **$1.10** | ~$0.01/LED × 104 |
| 10 | **4× RGB LEDs** (2× SoC-ctrl, 2× MCU-ctrl) | D27301/2, D27401/2 | **$0.40** | ~$0.10 each |
| 11 | **Power LED** (green, 3.3 V rail) | D27201 | **$0.05** | — |
| 12 | **USB-C connector** (USB 3.1 SuperSpeed) | JUSB1 | **$0.50** | Full-featured 24-pin for USB 3.1 |
| 13 | **60-pin high-density connectors ×2** (JMISC + JMEDIA, bottom-side mezzanine) | JMISC1, JMEDIA1 | **$3.00** | $1.50 each; impedance-controlled |
| 14 | **Standard headers/connectors** (10+18+14+6+4 pin) | JCTL1–QWIIC1 | **$0.80** | 2.54 mm + Qwiic JST |
| 15 | **Power button** (SMD tactile) | JBTN1 | **$0.10** | — |
| 16 | **Crystals** (32 MHz + 32.768 kHz) | — | **$0.50** | 2× crystals |
| 17 | **Buck regulators** (3× DC-DC for 5V→3.8V, 3.8V→3.3V) | — | **$1.50** | ~$0.50 each |
| 18 | **Power inductors** (3–4 for buck stages) | — | **$0.80** | — |
| 19 | **Passive components** (resistors, caps, ferrites, 300+ placements) | — | **$2.50** | Decoupling, filtering, pull-ups |

**BOM Total: ~$48.45 / board**

---

### Manufacturing Costs

| Item | Cost/Board | Notes |
|------|-----------|-------|
| **PCB fabrication** (6-layer, impedance controlled, 68×53 mm, 1000 pcs) | **$10.00** | Needs controlled impedance for LPDDR4X + USB 3.1. Budget: JLCPCB ~$6; quality CM: $10–15 |
| **PCBA — SMT assembly** (double-sided, multiple BGAs, X-ray inspection required) | **$10.00** | QRB2210 + STM32U585 + LPDDR4X + eMMC are all BGA. Complex stencil, reflow, X-ray |
| **Functional test** (boot, WiFi, BT, USB, LED matrix verification) | **$3.00** | Per-board test fixture + labor |

---

### Total Cost Summary

| | Per Board | 1,000 Boards |
|--|-----------|-------------|
| **BOM (components)** | $48.45 | $48,450 |
| **PCB fabrication** | $10.00 | $10,000 |
| **PCB assembly** | $10.00 | $10,000 |
| **Functional testing** | $3.00 | $3,000 |
| **Engineering/NRE (amortized)** | $2.00 | $2,000 |
| **Total** | **~$73.45** | **~$73,450** |

---

### Key Observations

**Why this is more expensive than Arduino's $41 retail price:**

1. **QRB2210 is subsidized by Qualcomm.** Since Qualcomm acquired Arduino, they supply the SoC to themselves at cost or below — effectively using the board as a platform play. An external buyer cannot get QRB2210 at commercial rates through standard distributors; you'd need a direct Qualcomm OEM agreement.

2. **Volume.** Arduino manufactures at scale (tens of thousands+), driving component costs down significantly — especially the memory and eMMC.

3. **1,000 units is a costly batch.** PCB setup fees, BGA assembly minimums, and SMT stencils have fixed costs that don't amortize well at 1k units.

**If you could replicate Arduino's internal pricing on the QRB2210 (~$6–8):** total drops to ~$60–65/board, still above retail.

---

### Practical Implication

Cloning or independently manufacturing the UNO Q at 1,000 units is **not economically viable** at current retail pricing. The design is intentionally loss-leader priced to promote the Qualcomm Dragonwing ecosystem. A commercially realistic variant would need either:
- 10,000+ unit volumes to drive costs below $50/board, or
- A substitute SoC (e.g., Rockchip RK3566 or MediaTek MT8390) that's available commercially for $5–8 and delivers similar performance

---

### Sources

- [Arduino UNO Q Datasheet (ABX00162)](https://docs.arduino.cc/resources/datasheets/ABX00162-datasheet.pdf)
- [Arduino UNO Q Schematics](https://docs.arduino.cc/resources/schematics/ABX00162-schematics.pdf)
- [Jeff Geerling — Arduino Uno Q Review](https://www.jeffgeerling.com/blog/2025/arduino-uno-q-weird-hybrid-sbc/)
- [STM32U585 at LCSC](https://www.lcsc.com/product-detail/C5271021.html)
- [STM32U585 DigiKey](https://www.digikey.com/en/products/base-product/stmicroelectronics/497/STM32U585/647544)
- [QRB2210 Product Page](https://www.qualcomm.com/internet-of-things/products/q2-series/qrb2210)
