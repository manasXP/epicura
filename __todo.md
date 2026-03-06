# Epicura - Task Tracking

## Documentation

- [x] Create documentation folder structure
- [x] [[__Workspaces/Epicura/docs/README|Documentation Index]] (README.md)
- [x] [[__Workspaces/Epicura/docs/01-Overview/01-Project-Overview|Project Overview]]
- [x] [[__Workspaces/Epicura/docs/02-Hardware/02-Technical-Specifications|Technical Specifications]]
- [x] [[docs/02-Hardware/Epicura-Architecture|Epicura Architecture]]
- [x] [[docs/02-Hardware/05-Sensors-Acquisition|Sensors & Acquisition]]
- [x] [[07-Mechanical-Design|Mechanical Design]]
- [x] [[04-Controller-Software-Architecture|Controller & Software Architecture]]
- [x] [[08-Tech-Stack|Tech Stack]]
- [x] [[03-UI-UX-Design|UI/UX Design]]
- [x] [[docs/05-Subsystems/09-Induction-Heating|Induction Heating]]
- [x] [[docs/05-Subsystems/10-Robotic-Arm|Robotic Arm]]
- [x] [[docs/05-Subsystems/11-Ingredient-Dispensing|Ingredient Dispensing]]
- [x] [[docs/05-Subsystems/12-Vision-System|Vision System]]
- [x] [[docs/05-Subsystems/13-Exhaust-Fume-Management|Exhaust & Fume Management]]
- [x] [[06-Safety-Compliance|Safety & Compliance]]
- [x] [[__Workspaces/Medical/ECG/docs/07-Development/Prototype-Development-Plan|Prototype Development Plan]]
- [x] [[01-Compute-Module-Components|Compute Module Components]]
- [x] [[02-Actuation-Components|Actuation Components]]
- [x] [[03-Sensor-Components|Sensor Components]]
- [x] [[__Workspaces/Epicura/docs/08-Components/04-Total-Component-Cost|Total Component Cost]]
- [x] Update `__init.md` with documentation links
- [x] Expand `CLAUDE.md` with technical context

## Prototype Hardware

- [ ] Order Raspberry Pi CM5 + carrier board
- [ ] Order STM32G474 Nucleo dev board
- [ ] Source commercial induction hob for teardown
- [ ] Order 24V BLDC motor (30-50 kg-cm, integrated ESC)
- [ ] Order IMX219 camera module
- [ ] Order MLX90614 IR thermometer
- [ ] Order HX711 + load cells
- [ ] Order 10" touchscreen display
- [ ] 3D print enclosure prototype

## Firmware Development

- [ ] CM5 Yocto BSP bring-up
- [ ] STM32 FreeRTOS project setup
- [ ] CM5 ↔ STM32 UART communication
- [ ] Induction PID control loop
- [ ] Servo arm stirring patterns
- [ ] Load cell calibration
- [ ] IR thermometer integration
- [ ] Camera capture pipeline
- [ ] TFLite model inference
- [ ] Recipe state machine engine
- [ ] Kivy touchscreen UI
- [ ] Ingredient dispensing control
- [ ] Safety watchdog and interlocks

## Software Development

- [ ] Recipe YAML format definition
- [ ] SQLite database schema
- [ ] OpenCV preprocessing pipeline
- [ ] MobileNetV2 training data collection
- [ ] Model training and INT8 quantization
- [ ] Cloud MQTT telemetry
- [ ] OTA update mechanism
- [ ] Native companion mobile apps (iOS + Android)

## Testing & Validation

- [ ] Power budget measurement
- [ ] Temperature accuracy validation (±5°C)
- [ ] CV inference latency (<500ms)
- [ ] End-to-end dal tadka cook test
- [ ] Safety interlock verification
- [ ] EMC pre-compliance scan

---

#epicura #tasks #project-tracking
