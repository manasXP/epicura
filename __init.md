

Epicura is an autonomous countertop kitchen robot that cooks full meals like a human chef using AI vision, robotic stirring, and precise heat control. Its core features include home use, tailored for compact kitchens with embedded tech integration. It closely follows the design of a commercically available product from Posha.com 

## Core Design Overview

The robot resembles a large microwave in size, featuring an induction cooktop base, proprietary non-stick pot, overhead camera for real-time food monitoring, and a single robotic arm for stirring and ingredient dispensing. It supports one-pot recipes (e.g., curries, pasta, stir-fries) with customization for diets, spices, or swaps. Power draw stays under 2kW for standard outlets, with a companion app for recipe selection and live viewing.

## Hardware Components

- **Base and Heating**: Commercial microwave induction surface (1,800W) with CAN bus control, temperature sensors for dynamic adjustment (e.g., sear at 200°C, simmer at 90°C).[[theverge](https://www.theverge.com/tech/840599/posha-robot-chef-review)]​
    
- **Robotics**: Single-axis arm with servo motors (e.g., STM32-driven for precision, akin to your medical device work) for rhythmic stirring and timed ingredient drops from 4-6 top-loading compartments.[[posha](https://www.posha.com/)]​
    
- **Vision and Sensors**: Overhead HD camera with edge AI (e.g., Raspberry Pi CM5 or Nvidia Jetson for color/texture analysis) plus IR thermometer and load cells for portion feedback.[[youtube](https://www.youtube.com/watch?v=yturqqp64Ng)]​[[theverge](https://www.theverge.com/tech/840599/posha-robot-chef-review)]​
    
- **UI Display**: 10-inch touchscreen or app-paired interface using Kivy for recipe browsing, grocery lists, and progress cams.[[posha](https://www.posha.com/)]​
    

## Software Architecture

Culinary AI runs on embedded Linux (e.g., Yocto on CM5), processing recipes as state machines: detect stage (via CV), adjust heat/stir, add next ingredient. Supports 100+ recipes initially, with cloud updates for new ones; local fallback for offline use. Custom logic handles imperfections like imprecise measuring. Integrate MISRA C for safety-critical timing, similar to your ventilator/ECG projects.

## Key Features Comparison

| Feature       | Posha Capability                                                                                       | Epicura Design Match                     |
| ------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| Autonomy      | Fully hands-off after prep [[theverge](https://www.theverge.com/tech/840599/posha-robot-chef-review)]​ | Identical, with CV fallback loops        |
| Customization | Spice/allergen swaps [[posha](https://www.posha.com/)]​                                                | App-driven, recipe DB with substitutions |
| Monitoring    | Live camera feed [[posha](https://www.posha.com/)]​                                                    | App + local screen, anomaly alerts       |
| Cleanup       | Dishwasher-safe pot [[youtube](https://www.youtube.com/watch?v=yturqqp64Ng)]​                          | Removable pot, auto-rinse cycle          |
| Size/Power    | Countertop, 1.8kW [[theverge](https://www.theverge.com/tech/840599/posha-robot-chef-review)]​          | 50x40x30cm, <2kW for India outlets       |

## Prototyping Steps

Start with off-the-shelf: Raspberry Pi CM5 carrier board for AI/compute, ST STM32 for arm control, and a commercial induction hob. Code device UI in Kivy (Python). Test one-pot Indian recipes (e.g., dal tadka) to validate stirring/heat logic. Estimated BOM: $800-1,200 for prototype, scalable for production.

## Documentation

Comprehensive documentation has been organized in the [[docs/README|docs folder]]. See the following detailed specifications:

### Core Documentation

**Overview**
1. [[docs/01-Overview/01-Project-Overview|Project Overview]] - Product definition, features, and target use cases

**Hardware**
2. [[docs/02-Hardware/02-Technical-Specifications|Technical Specifications]] - Induction, sensors, power, and performance specs
3. [[docs/02-Hardware/Epicura-Architecture|Epicura Architecture]] - System block diagrams and hardware wiring
4. [[docs/02-Hardware/05-Sensors-Acquisition|Sensors & Acquisition]] - Camera, IR thermometer, load cells, and NTC probes
5. [[docs/02-Hardware/07-Mechanical-Design|Mechanical Design]] - Enclosure, arm mechanism, and industrial design

**Software**
6. [[docs/03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]] - Dual-processor software modules and recipe state machine
7. [[docs/03-Software/08-Tech-Stack|Tech Stack]] - Hardware platforms, software frameworks, and development tools

**User Interface**
8. [[docs/04-UserInterface/03-UI-UX-Design|UI/UX Design]] - Touchscreen interface, companion app, and multi-language support

**Subsystems**
9. [[docs/05-Subsystems/09-Induction-Heating|Induction Heating]] - 1,800W microwave induction surface (CAN bus), PID control, and power management
10. [[docs/05-Subsystems/10-Robotic-Arm|Robotic Arm]] - Single-axis servo arm, stirring patterns, and motor control
11. [[docs/05-Subsystems/11-Ingredient-Dispensing|Ingredient Dispensing]] - Multi-compartment hopper system and timed dispensing
12. [[docs/05-Subsystems/12-Vision-System|Vision System]] - HD camera, edge AI inference, and cooking stage detection
13. [[docs/05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]] - Exhaust fan, grease/carbon filtration, and fume extraction

**Compliance**
13. [[docs/06-Compliance/06-Safety-Compliance|Safety & Compliance]] - Electrical safety, food contact regulations, and BIS standards

**Development**
14. [[docs/07-Development/Prototype-Development-Plan|Prototype Development Plan]] - Phased plan from prototype to production

**Components & BOM**
15. [[docs/08-Components/01-Compute-Module-Components|Compute Module Components]] - Raspberry Pi CM5, STM32, carrier boards
16. [[docs/08-Components/02-Actuation-Components|Actuation Components]] - Servo motors, induction driver, solenoids
17. [[docs/08-Components/03-Sensor-Components|Sensor Components]] - Camera, IR thermometer, NTC probes, load cells
18. [[docs/08-Components/04-Total-Component-Cost|Total Component Cost]] - Full BOM and cost analysis

**Start here:** [[docs/README|Documentation Index]]

---

#project/epicura #kitchen-robot #autonomous-cooking #embedded-systems