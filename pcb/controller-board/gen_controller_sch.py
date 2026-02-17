#!/usr/bin/env python3
"""Generate complete KiCAD 9 schematic for Epicura Controller Board."""

import uuid as uuid_mod

_counter = 0
def uid():
    global _counter
    _counter += 1
    return f"aa{_counter:06d}-{_counter:04d}-{_counter:04d}-{_counter:04d}-{_counter:012d}"


def snap(v):
    """Snap to 1.27mm grid."""
    return round(round(v / 1.27) * 1.27, 4)

# MCU at (127, 127). Pin abs connection: (127+rel_x, 127-rel_y)
MCU_X, MCU_Y = 127, 127

# MCU pin definitions: pin_num -> (name, rel_x, rel_y, angle)
MCU_PINS = {
    1: ("VDD", -7.62, 83.82, 270),
    2: ("PC13", -22.86, 76.2, 0),
    3: ("PC14", -22.86, 73.66, 0),
    4: ("PC15", -22.86, 71.12, 0),
    5: ("PF0", -22.86, 63.5, 0),
    6: ("PF1", -22.86, 60.96, 0),
    7: ("NRST", -22.86, 78.74, 0),
    8: ("VSSA", 2.54, -83.82, 90),
    9: ("VDDA", 2.54, 83.82, 270),
    10: ("PA0", -22.86, 50.8, 0),
    11: ("PA1", -22.86, 48.26, 0),
    12: ("PA2", -22.86, 45.72, 0),
    13: ("PA3", -22.86, 43.18, 0),
    14: ("PA4", -22.86, 40.64, 0),
    15: ("PA5", -22.86, 38.1, 0),
    16: ("PA6", -22.86, 35.56, 0),
    17: ("PA7", -22.86, 33.02, 0),
    18: ("PC0", 22.86, 50.8, 180),
    19: ("PC1", 22.86, 48.26, 180),
    20: ("PC2", 22.86, 45.72, 180),
    21: ("PC3", 22.86, 43.18, 180),
    22: ("VDD", -5.08, 83.82, 270),
    23: ("VSS", -2.54, -83.82, 90),
    24: ("PA8", -22.86, 30.48, 0),
    25: ("PA9", -22.86, 27.94, 0),
    26: ("PA10", -22.86, 25.4, 0),
    27: ("PA11", -22.86, 22.86, 0),
    28: ("PA12", -22.86, 20.32, 0),
    29: ("PA13", -22.86, 17.78, 0),
    30: ("VSS", 0, -83.82, 90),
    31: ("VDD", -2.54, 83.82, 270),
    32: ("PA14", -22.86, 15.24, 0),
    33: ("PA15", -22.86, 12.7, 0),
    34: ("PC4", 22.86, 40.64, 180),
    35: ("PC5", 22.86, 38.1, 180),
    36: ("PB0", 22.86, 10.16, 180),
    37: ("PB1", 22.86, 7.62, 180),
    38: ("PB2", 22.86, 5.08, 180),
    39: ("PB10", 22.86, -10.16, 180),
    40: ("PB11", 22.86, -12.7, 180),
    41: ("VDD", 0, 83.82, 270),
    42: ("PB12", 22.86, -15.24, 180),
    43: ("PB13", 22.86, -17.78, 180),
    44: ("PB14", 22.86, -20.32, 180),
    45: ("PB15", 22.86, -22.86, 180),
    46: ("PC6", 22.86, 35.56, 180),
    47: ("PC7", 22.86, 33.02, 180),
    48: ("PC8", 22.86, 30.48, 180),
    49: ("PC9", 22.86, 27.94, 180),
    50: ("PD8", -22.86, -2.54, 0),
    51: ("PD9", -22.86, -5.08, 0),
    52: ("VSS", 2.54, -83.82, 90),
    53: ("VDD", 2.54, 83.82, 270),
    54: ("PB3", 22.86, 2.54, 180),
    55: ("PB4", 22.86, 0, 180),
    56: ("PB5", 22.86, -2.54, 180),
    57: ("PB6", 22.86, -5.08, 180),
    58: ("PB7", 22.86, -7.62, 180),
    59: ("BOOT0", -22.86, 68.58, 0),
    60: ("PB8", 22.86, -25.4, 180),
    61: ("PB9", 22.86, -27.94, 180),
    62: ("VSS", 5.08, -83.82, 90),
    63: ("VDD", 5.08, 83.82, 270),
    64: ("VDDUSB", 7.62, 83.82, 270),
}

def mcu_abs(pin_num):
    _, rx, ry, _ = MCU_PINS[pin_num]
    return (MCU_X + rx, MCU_Y - ry)

# Pin assignments: pin_num -> label_name
# None = no_connect, "PWR_3V3" / "PWR_GND" = power
SIGNAL_PINS = {
    10: "PASD_PUMP_PWM",
    14: "NTC_COIL",
    15: "NTC_AMB",
    16: "FAN1_PWM",
    17: "SLD_SOL1_EN",
    24: "MAIN_SERVO_PWM",
    25: "SLD_SOL2_EN",
    26: "CID_LACT1_EN",
    27: "BUZZER_PWM",
    29: "SWDIO",
    32: "SWCLK",
    36: "SAFETY_RELAY",
    37: "POT_DET",
    38: "E_STOP",
    39: "FAN2_PWM",
    42: "SPI2_NSS",
    43: "SPI2_SCK",
    44: "SPI2_MISO",
    45: "SPI2_MOSI",
    54: "SPI_IRQ",
    55: "CID_LACT1_PH",
    56: "CID_LACT2_EN",
    57: "I2C1_SCL",
    58: "I2C1_SDA",
    60: "FDCAN1_RX",
    61: "FDCAN1_TX",
    18: "HX711_SCK",
    19: "HX711_DOUT",
    20: "CID_LACT2_PH",
    21: "SLD_PUMP1_PWM",
    34: "SLD_PUMP1_DIR",
    35: "SLD_PUMP2_PWM",
    46: "SLD_PUMP2_DIR",
    2: "STATUS_LED",
    3: "LSE_IN",
    4: "LSE_OUT",
    5: "HSE_IN",
    6: "HSE_OUT",
    7: "NRST",
    59: "BOOT0",
}

NO_CONNECT_PINS = [11, 12, 13, 28, 33, 40, 47, 48, 49, 50, 51]

POWER_VDD_PINS = [1, 9, 22, 31, 41, 53, 63, 64]  # +3V3
POWER_GND_PINS = [8, 23, 30, 52, 62]  # GND

# J_STACK at (127, 254), Conn_02x20_Odd_Even
# Pin defs: odd pins on left at (-5.08, y_off), even on right at (7.62, y_off)
# y_offsets: pin1/2 at 24.13, pin3/4 at 21.59, ..., stepping by -2.54
JSTACK_X, JSTACK_Y = 127, 254

def jstack_abs(pin_num):
    """Get J_STACK pin connection point."""
    row = (pin_num - 1) // 2  # 0-indexed row
    y_off = 24.13 - row * 2.54
    if pin_num % 2 == 1:  # odd = left
        x_off = -5.08
    else:  # even = right
        x_off = 7.62
    return (JSTACK_X + x_off, JSTACK_Y - y_off)

# J_STACK pin assignments
JSTACK_POWER_24V = [1, 2, 3, 4]
JSTACK_GND = [5, 6, 7, 8, 9, 10, 25, 26, 40]
JSTACK_5V = [11, 12]
JSTACK_3V3 = [13, 14]
JSTACK_SIGNALS = {
    15: "PASD_PUMP_PWM",
    16: "RESERVED_16",  # no_connect
    17: "RESERVED_17",
    18: "RESERVED_18",
    19: "RESERVED_19",
    20: "RESERVED_20",
    21: "CID_LACT1_EN",
    22: "CID_LACT1_PH",
    23: "CID_LACT2_EN",
    24: "CID_LACT2_PH",
    27: "FAN1_PWM",
    28: "FAN2_PWM",
    29: "SLD_PUMP1_PWM",
    30: "SLD_PUMP1_DIR",
    31: "SLD_PUMP2_PWM",
    32: "SLD_PUMP2_DIR",
    33: "SLD_SOL1_EN",
    34: "SLD_SOL2_EN",
    35: "I2C1_SCL",
    36: "I2C1_SDA",
    37: "MAIN_SERVO_PWM",
    38: "BUZZER_PWM",
    39: "RESERVED_39",
}
JSTACK_NC = [16, 17, 18, 19, 20, 39]

# Output buffers
wires = []
labels = []
no_connects = []
power_syms = []
components = []
sym_instances = []

pwr_counter = {"n": 6}  # start after existing #PWR01-05

def add_power(sym_type, x, y, ref_prefix="#PWR"):
    """Add a power symbol. sym_type: '+3V3', '+5V', 'GND', '+24V'"""
    n = pwr_counter["n"]
    pwr_counter["n"] += 1
    ref = f"{ref_prefix}{n:02d}"
    lib_map = {"+3V3": "power:+3V3", "+5V": "power:+5V", "GND": "power:GND", "+24V": "power:+24V"}
    lib_id = lib_map[sym_type]
    u = uid()
    pu = uid()

    # GND symbols point downward, voltage symbols point upward
    # No mirror needed for standard orientations
    power_syms.append(f"""  (symbol (lib_id "{lib_id}") (at {x} {y} 0) (unit 1) (uuid "{u}")
    (property "Reference" "{ref}" (at {x} {y + 3.81 if sym_type == 'GND' else y - 3.81} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "{sym_type}" (at {x} {y + (3.81 if sym_type != 'GND' else -3.81)} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "{pu}"))
  )""")
    sym_instances.append(f'    (path "/{u}" (reference "{ref}") (unit 1) (value "{sym_type}") (footprint ""))')
    return ref

def add_label(name, x, y, angle=0):
    labels.append(f'  (label "{name}" (at {x} {y} {angle}) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))')

def add_wire(x1, y1, x2, y2):
    wires.append(f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0)) (uuid "{uid()}"))')

def add_nc(x, y):
    no_connects.append(f'  (no_connect (at {x} {y}) (uuid "{uid()}"))')

# ============================================================
# Process MCU power pins
# ============================================================
# Track positions we've already placed power symbols at (some pins overlap)
placed_power = set()

for pin in POWER_VDD_PINS:
    x, y = mcu_abs(pin)
    key = (x, y)
    if key not in placed_power:
        placed_power.add(key)
        add_power("+3V3", x, y)

for pin in POWER_GND_PINS:
    x, y = mcu_abs(pin)
    key = (x, y)
    if key not in placed_power:
        placed_power.add(key)
        add_power("GND", x, y)

# ============================================================
# Process MCU signal pins - add wire stub + label
# ============================================================
for pin, label_name in SIGNAL_PINS.items():
    x, y = mcu_abs(pin)
    _, _, _, angle = MCU_PINS[pin]
    # Wire stub direction based on pin angle
    if angle == 0:  # pin exits left, wire goes further left
        wx = x - 10.16
        add_wire(x, y, wx, y)
        add_label(label_name, wx, y, 0)
    elif angle == 180:  # pin exits right, wire goes further right
        wx = x + 10.16
        add_wire(x, y, wx, y)
        add_label(label_name, wx, y, 0)
    elif angle == 270:  # pin exits up (lower y), wire goes up
        wy = y - 5.08
        add_wire(x, y, x, wy)
        add_label(label_name, x, wy, 0)
    elif angle == 90:  # pin exits down (higher y), wire goes down
        wy = y + 5.08
        add_wire(x, y, x, wy)
        add_label(label_name, x, wy, 0)

# ============================================================
# Process MCU no-connect pins
# ============================================================
for pin in NO_CONNECT_PINS:
    x, y = mcu_abs(pin)
    add_nc(x, y)

# ============================================================
# J_STACK connections
# ============================================================
for pin in JSTACK_POWER_24V:
    x, y = jstack_abs(pin)
    add_power("+24V", x, y)

for pin in JSTACK_GND:
    x, y = jstack_abs(pin)
    pos = (x, y)
    if pos not in placed_power:
        placed_power.add(pos)
        add_power("GND", x, y)

for pin in JSTACK_5V:
    x, y = jstack_abs(pin)
    add_power("+5V", x, y)

for pin in JSTACK_3V3:
    x, y = jstack_abs(pin)
    add_power("+3V3", x, y)

for pin, sig in JSTACK_SIGNALS.items():
    if pin in JSTACK_NC:
        x, y = jstack_abs(pin)
        add_nc(x, y)
    else:
        x, y = jstack_abs(pin)
        if pin % 2 == 1:  # left side, wire goes left
            wx = x - 10.16
            add_wire(x, y, wx, y)
            add_label(sig, wx, y, 0)
        else:  # right side, wire goes right
            wx = x + 10.16
            add_wire(x, y, wx, y)
            add_label(sig, wx, y, 0)

# ============================================================
# Connectors - J1 SPI (Conn_01x06) at (190, 142)
# Pin offsets for Conn_01x06: pin N at (-5.08, 5.08 - (N-1)*2.54)
# ============================================================
J1_X, J1_Y = snap(190), snap(142)

def conn_1x_abs(cx, cy, pin, total_pins):
    """Conn_01xN pin abs position using actual KiCAD pin Y-offsets."""
    # From KiCAD lib_symbols: Conn_01x04 pins at y=2.54,0,-2.54,-5.08
    # Conn_01x06 pins at y=5.08,2.54,0,-2.54,-5.08,-7.62
    # General: pin N y_offset = (total_pins/2 - 0.5)*2.54 - (pin-1)*2.54
    # For 4-pin: 2.54, 0, -2.54, -5.08
    # For 6-pin: 5.08, 2.54, 0, -2.54, -5.08, -7.62
    if total_pins == 4:
        offsets = [2.54, 0, -2.54, -5.08]
    elif total_pins == 6:
        offsets = [5.08, 2.54, 0, -2.54, -5.08, -7.62]
    else:
        offsets = [(total_pins/2 - 0.5)*2.54 - (i)*2.54 for i in range(total_pins)]
    y_off = offsets[pin - 1]
    return (cx - 5.08, cy - y_off)

J1_SIGS = {1: "SPI2_NSS", 2: "SPI2_MISO", 3: "SPI2_MOSI", 4: "SPI2_SCK", 5: "SPI_IRQ"}
# Pin 6 = GND

for pin, sig in J1_SIGS.items():
    x, y = conn_1x_abs(J1_X, J1_Y, pin, 6)
    wx = x - 10.16
    add_wire(x, y, wx, y)
    add_label(sig, wx, y, 0)

# J1 pin 6 = GND
x, y = conn_1x_abs(J1_X, J1_Y, 6, 6)
add_power("GND", x, y)

# J1 component
j1_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 7))
components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x06") (at {J1_X} {J1_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "J1" (at {J1_X} {J1_Y - 10} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "SPI_CM5" (at {J1_X} {J1_Y - 8} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_SH_BM06B-SRSS-TB_1x06-1MP_P1.00mm_Vertical" (at {J1_X} {J1_Y} 0) (effects (font (size 1.27 1.27)) hide))
{j1_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "J1") (unit 1) (value "SPI_CM5") (footprint "Connector_JST:JST_SH_BM06B-SRSS-TB_1x06-1MP_P1.00mm_Vertical"))')

# ============================================================
# J6 I2C (Conn_01x04) at (190, 165)
# ============================================================
J6_X, J6_Y = snap(190), snap(165)
J6_SIGS = {1: "I2C1_SCL", 2: "I2C1_SDA"}
# Pin 3 = +3V3, Pin 4 = GND

for pin, sig in J6_SIGS.items():
    x, y = conn_1x_abs(J6_X, J6_Y, pin, 4)
    wx = x - 10.16
    add_wire(x, y, wx, y)
    add_label(sig, wx, y, 0)

x, y = conn_1x_abs(J6_X, J6_Y, 3, 4)
add_power("+3V3", x, y)
x, y = conn_1x_abs(J6_X, J6_Y, 4, 4)
add_power("GND", x, y)

j6_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 5))
components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x04") (at {J6_X} {J6_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "J6" (at {J6_X} {J6_Y - 8} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "I2C" (at {J6_X} {J6_Y - 6} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical" (at {J6_X} {J6_Y} 0) (effects (font (size 1.27 1.27)) hide))
{j6_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "J6") (unit 1) (value "I2C") (footprint "Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical"))')

# ============================================================
# J7 HX711 (Conn_01x04) at (190, 80)
# ============================================================
J7_X, J7_Y = snap(190), snap(80)
J7_SIGS = {1: "HX711_SCK", 2: "HX711_DOUT"}

for pin, sig in J7_SIGS.items():
    x, y = conn_1x_abs(J7_X, J7_Y, pin, 4)
    wx = x - 10.16
    add_wire(x, y, wx, y)
    add_label(sig, wx, y, 0)

x, y = conn_1x_abs(J7_X, J7_Y, 3, 4)
add_power("+3V3", x, y)
x, y = conn_1x_abs(J7_X, J7_Y, 4, 4)
add_power("GND", x, y)

j7_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 5))
components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x04") (at {J7_X} {J7_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "J7" (at {J7_X} {J7_Y - 8} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "HX711" (at {J7_X} {J7_Y - 6} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" (at {J7_X} {J7_Y} 0) (effects (font (size 1.27 1.27)) hide))
{j7_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "J7") (unit 1) (value "HX711") (footprint "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical"))')

# ============================================================
# J8 NTC (Conn_01x04) at (70, 90)
# ============================================================
J8_X, J8_Y = snap(70), snap(90)
J8_SIGS = {1: "NTC_COIL", 2: "NTC_AMB"}

for pin, sig in J8_SIGS.items():
    x, y = conn_1x_abs(J8_X, J8_Y, pin, 4)
    wx = x - 10.16
    add_wire(x, y, wx, y)
    add_label(sig, wx, y, 0)

x, y = conn_1x_abs(J8_X, J8_Y, 3, 4)
add_power("+3V3", x, y)
x, y = conn_1x_abs(J8_X, J8_Y, 4, 4)
add_power("GND", x, y)

j8_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 5))
components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x04") (at {J8_X} {J8_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "J8" (at {J8_X} {J8_Y - 8} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "NTC" (at {J8_X} {J8_Y - 6} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" (at {J8_X} {J8_Y} 0) (effects (font (size 1.27 1.27)) hide))
{j8_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "J8") (unit 1) (value "NTC") (footprint "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical"))')

# ============================================================
# J9 SWD (Conn_01x06) at (70, 112)
# ============================================================
J9_X, J9_Y = snap(70), snap(112)
J9_SIGS = {2: "SWDIO", 3: "SWCLK", 5: "NRST"}

# Pin 1 = +3V3
x, y = conn_1x_abs(J9_X, J9_Y, 1, 6)
add_power("+3V3", x, y)

for pin, sig in J9_SIGS.items():
    x, y = conn_1x_abs(J9_X, J9_Y, pin, 6)
    wx = x - 10.16
    add_wire(x, y, wx, y)
    add_label(sig, wx, y, 0)

# Pin 4 = SWO/IRQ - no_connect for now
x, y = conn_1x_abs(J9_X, J9_Y, 4, 6)
add_nc(x, y)

# Pin 6 = GND
x, y = conn_1x_abs(J9_X, J9_Y, 6, 6)
add_power("GND", x, y)

j9_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 7))
components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x06") (at {J9_X} {J9_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "J9" (at {J9_X} {J9_Y - 10} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "SWD" (at {J9_X} {J9_Y - 8} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical" (at {J9_X} {J9_Y} 0) (effects (font (size 1.27 1.27)) hide))
{j9_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "J9") (unit 1) (value "SWD") (footprint "Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical"))')

# ============================================================
# J11 Safety (Conn_01x04) at (190, 120)
# ============================================================
J11_X, J11_Y = snap(190), snap(120)
J11_SIGS = {1: "SAFETY_RELAY", 2: "POT_DET", 3: "E_STOP"}

for pin, sig in J11_SIGS.items():
    x, y = conn_1x_abs(J11_X, J11_Y, pin, 4)
    wx = x - 10.16
    add_wire(x, y, wx, y)
    add_label(sig, wx, y, 0)

# Pin 4 = GND
x, y = conn_1x_abs(J11_X, J11_Y, 4, 4)
add_power("GND", x, y)

j11_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 5))
components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_01x04") (at {J11_X} {J11_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "J11" (at {J11_X} {J11_Y - 8} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "Safety" (at {J11_X} {J11_Y - 6} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" (at {J11_X} {J11_Y} 0) (effects (font (size 1.27 1.27)) hide))
{j11_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "J11") (unit 1) (value "Safety") (footprint "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical"))')

# ============================================================
# CAN section - wire U3 to labels and J2
# U3 SN65HVD230 at (215.9, 35.56)
# Pin defs: 1(D) at (-10.16, 7.62, 0), 2(GND) at (0,-12.7,90), 3(VCC) at (0,12.7,270),
# 4(R) at (-10.16, 2.54, 0), 5(Vref) at (-10.16,-2.54,0), 6(CANL) at (10.16,2.54,180),
# 7(CANH) at (10.16,7.62,180), 8(Rs) at (-10.16,-7.62,0)
# ============================================================
U3_X, U3_Y = 215.9, 35.56

def u3_abs(rx, ry):
    return (U3_X + rx, U3_Y - ry)

# U3 pin 1 (D) - FDCAN1_TX
x, y = u3_abs(-10.16, 7.62)
wx = x - 10.16
add_wire(x, y, wx, y)
add_label("FDCAN1_TX", wx, y, 0)

# U3 pin 4 (R) - FDCAN1_RX
x, y = u3_abs(-10.16, 2.54)
wx = x - 10.16
add_wire(x, y, wx, y)
add_label("FDCAN1_RX", wx, y, 0)

# U3 pin 2 (GND) - already has power symbol in existing file
# U3 pin 3 (VCC) - already has power symbol in existing file

# U3 pin 5 (Vref) - no connect (usually left floating or decoupled)
x, y = u3_abs(-10.16, -2.54)
add_nc(x, y)

# U3 pin 8 (Rs) - tie to GND for high-speed mode
x, y = u3_abs(-10.16, -7.62)
add_power("GND", x, y)

# U3 pin 6 (CANL) - to R_TERM and J2
x, y = u3_abs(10.16, 2.54)
wx = x + 10.16
add_wire(x, y, wx, y)
add_label("CAN_L", wx, y, 0)

# U3 pin 7 (CANH) - to R_TERM and J2
x, y = u3_abs(10.16, 7.62)
wx = x + 10.16
add_wire(x, y, wx, y)
add_label("CAN_H", wx, y, 0)

# R_TERM (120Ω) - connects between CAN_H and CAN_L
# Moved to (243.84, 31.75) to avoid wire overlap with U3 pin wires
# R pin 1 at (0, 3.81, 270) → abs (243.84, 31.75-3.81) = (243.84, 27.94)
# R pin 2 at (0, -3.81, 90) → abs (243.84, 31.75+3.81) = (243.84, 35.56)
add_label("CAN_H", 243.84, 27.94, 0)
add_label("CAN_L", 243.84, 35.56, 0)

# J2 CAN (Conn_01x04) at (240.03, 35.56)
# Pin 1 at (-5.08, 2.54) → abs (234.95, 33.02) → CAN_H
# Pin 2 at (-5.08, 0) → abs (234.95, 35.56) → CAN_L
# Pin 3 at (-5.08, -2.54) → abs (234.95, 38.1) → GND
# Pin 4 at (-5.08, -5.08) → abs (234.95, 40.64) → +5V (optional)
j2_abs = lambda p: (240.03 - 5.08, 35.56 - (2.54 * (2 - (p-1))))  # simplified
# Actually let me recalculate. Conn_01x04 pins:
# Pin 1: at (-5.08, 2.54, 0), Pin 2: at (-5.08, 0, 0), Pin 3: at (-5.08, -2.54, 0), Pin 4: at (-5.08, -5.08, 0)
x1, y1 = 240.03 - 5.08, 35.56 - 2.54  # Pin 1
add_wire(x1, y1, x1 - 10.16, y1)
add_label("CAN_H", x1 - 10.16, y1, 0)

x2, y2 = 240.03 - 5.08, 35.56  # Pin 2
add_wire(x2, y2, x2 - 10.16, y2)
add_label("CAN_L", x2 - 10.16, y2, 0)

x3, y3 = 240.03 - 5.08, 35.56 + 2.54  # Pin 3
add_power("GND", x3, y3)

x4, y4 = 240.03 - 5.08, 35.56 + 5.08  # Pin 4
add_power("+5V", x4, y4)

# ============================================================
# Power section - LDO wiring
# U2 AMS1117-3.3 at (40.64, 35.56)
# Pin 1 (GND): at (0, -7.62, 90) → abs (40.64, 43.18)
# Pin 2 (VO): at (7.62, 2.54, 180) → abs (48.26, 33.02)
# Pin 3 (VI): at (-7.62, 2.54, 0) → abs (33.02, 33.02)
# ============================================================
# LDO pin 3 (VI) connects to +5V
add_power("+5V", 33.02, 33.02)

# LDO pin 2 (VO) connects to +3V3
add_power("+3V3", 48.26, 33.02)

# LDO pin 1 (GND) connects to GND
add_power("GND", 40.64, 43.18)

# C1 (10uF) at (27.94, 45.72) - input bypass
# C pin 1 at (0, 3.81, 270) → abs (27.94, 41.91)
# C pin 2 at (0, -3.81, 90) → abs (27.94, 49.53)
add_power("+5V", 27.94, 41.91)
add_power("GND", 27.94, 49.53)

# C2 (10uF) at (50.8, 45.72) - output bypass
add_power("+3V3", 50.8, 41.91)
add_power("GND", 50.8, 49.53)

# C3 (100nF) at (60.96, 45.72) - HF decoupling
add_power("+3V3", 60.96, 41.91)
add_power("GND", 60.96, 49.53)

# J10 PWR_IN at (15.24, 35.56) (mirror x)
# With mirror x, pin positions are... tricky. Let me recalculate.
# Conn_01x02 pins: Pin 1 at (-5.08, 0, 0), Pin 2 at (-5.08, -2.54, 0)
# With mirror x at (15.24, 35.56): pins flip vertically
# Pin 1: abs (15.24 - 5.08, 35.56 + 0) = (10.16, 35.56)
# Pin 2: abs (15.24 - 5.08, 35.56 + 2.54) = (10.16, 38.1)
# Actually mirror x means Y is negated: pin_y = -pin_y
# Pin 1: (15.24 + (-5.08), 35.56 - (0)) = (10.16, 35.56) → +5V
# Pin 2: (15.24 + (-5.08), 35.56 - (-2.54)) = (10.16, 38.1) → GND
add_power("+5V", 10.16, 35.56)  # J10 pin 1
add_power("GND", 10.16, 33.02)  # J10 pin 2

# PWR_FLAG on +5V net (at J10 pin 1)
pf_n = pwr_counter["n"]
pwr_counter["n"] += 1
pf_ref = f"#FLG{pf_n:02d}"
pf_uuid = uid()
pf_puuid = uid()
power_syms.append(f"""  (symbol (lib_id "power:PWR_FLAG") (at 10.16 35.56 0) (unit 1) (uuid "{pf_uuid}")
    (property "Reference" "{pf_ref}" (at 10.16 39.37 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "PWR_FLAG" (at 10.16 31.75 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 10.16 35.56 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "{pf_puuid}"))
  )""")
sym_instances.append(f'    (path "/{pf_uuid}" (reference "{pf_ref}") (unit 1) (value "PWR_FLAG") (footprint ""))')

# PWR_FLAG on +24V net (at J_STACK pin 1)
pf_n2 = pwr_counter["n"]
pwr_counter["n"] += 1
pf_ref2 = f"#FLG{pf_n2:02d}"
pf_uuid2 = uid()
pf_puuid2 = uid()
x24, y24 = jstack_abs(1)
power_syms.append(f"""  (symbol (lib_id "power:PWR_FLAG") (at {x24} {y24} 0) (unit 1) (uuid "{pf_uuid2}")
    (property "Reference" "{pf_ref2}" (at {x24} {y24+3.81} 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "PWR_FLAG" (at {x24} {y24-3.81} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at {x24} {y24} 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "{pf_puuid2}"))
  )""")
sym_instances.append(f'    (path "/{pf_uuid2}" (reference "{pf_ref2}") (unit 1) (value "PWR_FLAG") (footprint ""))')

# PWR_FLAG on GND net (near MCU VSSA pin 8)
pf_uuid3 = uid()
pf_n3 = pwr_counter["n"]
pwr_counter["n"] += 1
pf_ref3 = f"#FLG{pf_n3:02d}"
# Place near MCU GND pin 8 at (129.54, 210.82)
power_syms.append(f"""  (symbol (lib_id "power:PWR_FLAG") (at 129.54 210.82 0) (unit 1) (uuid "{pf_uuid3}")
    (property "Reference" "{pf_ref3}" (at 129.54 214.63 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "PWR_FLAG" (at 129.54 207.01 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 129.54 210.82 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "{uid()}"))
  )""")
sym_instances.append(f'    (path "/{pf_uuid3}" (reference "{pf_ref3}") (unit 1) (value "PWR_FLAG") (footprint ""))')

# ============================================================
# Passive components - Crystals, Resistors, Capacitors
# These connect via labels to MCU pins
# ============================================================

# Y1 8MHz Crystal at (88, 64.77) - connects HSE_IN and HSE_OUT
# Crystal pins: Pin 1 at (-3.81, 0, 0), Pin 2 at (3.81, 0, 180)
Y1_X, Y1_Y = snap(88), snap(64.77)
y1p1 = (Y1_X - 3.81, Y1_Y)  # Pin 1
y1p2 = (Y1_X + 3.81, Y1_Y)  # Pin 2
add_wire(y1p1[0], y1p1[1], y1p1[0] - 5.08, y1p1[1])
add_label("HSE_IN", y1p1[0] - 5.08, y1p1[1], 0)
add_wire(y1p2[0], y1p2[1], y1p2[0] + 5.08, y1p2[1])
add_label("HSE_OUT", y1p2[0] + 5.08, y1p2[1], 0)

y1_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:Crystal") (at {Y1_X} {Y1_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "Y1" (at {Y1_X} {Y1_Y - 3} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "8MHz" (at {Y1_X} {Y1_Y + 3} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Crystal:Crystal_SMD_HC49-SD" (at {Y1_X} {Y1_Y} 0) (effects (font (size 1.27 1.27)) hide))
{y1_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "Y1") (unit 1) (value "8MHz") (footprint "Crystal:Crystal_SMD_HC49-SD"))')

# Y2 32.768kHz Crystal at (88, 54.61)
Y2_X, Y2_Y = snap(88), snap(54.61)
y2p1 = (Y2_X - 3.81, Y2_Y)
y2p2 = (Y2_X + 3.81, Y2_Y)
add_wire(y2p1[0], y2p1[1], y2p1[0] - 5.08, y2p1[1])
add_label("LSE_IN", y2p1[0] - 5.08, y2p1[1], 0)
add_wire(y2p2[0], y2p2[1], y2p2[0] + 5.08, y2p2[1])
add_label("LSE_OUT", y2p2[0] + 5.08, y2p2[1], 0)

y2_pins = "\n".join(f'    (pin "{i}" (uuid "{uid()}"))' for i in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:Crystal") (at {Y2_X} {Y2_Y} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "Y2" (at {Y2_X} {Y2_Y - 3} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "32.768kHz" (at {Y2_X} {Y2_Y + 3} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Crystal:Crystal_SMD_2012-2Pin_2.0x1.2mm" (at {Y2_X} {Y2_Y} 0) (effects (font (size 1.27 1.27)) hide))
{y2_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "Y2") (unit 1) (value "32.768kHz") (footprint "Crystal:Crystal_SMD_2012-2Pin_2.0x1.2mm"))')

# HSE load caps C10, C11 - 18pF from crystal pins to GND
for i, (cx, cy, ref) in enumerate([(snap(84.19), snap(69), "C10"), (snap(91.81), snap(69), "C11")]):
    cp1 = (cx, cy - 3.81)  # pin 1 top
    cp2 = (cx, cy + 3.81)  # pin 2 bottom
    if ref == "C10":
        add_label("HSE_IN", cp1[0], cp1[1], 0)
    else:
        add_label("HSE_OUT", cp1[0], cp1[1], 0)
    add_power("GND", cp2[0], cp2[1])

    c_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
    components.append(f"""  (symbol (lib_id "Device:C") (at {cx} {cy} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "{ref}" (at {cx + 2.54} {cy} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "18pF" (at {cx + 2.54} {cy + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0402_1005Metric" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))
{c_pins}
  )""")
    sym_instances.append(f'    (path "/{uid()}" (reference "{ref}") (unit 1) (value "18pF") (footprint "Capacitor_SMD:C_0402_1005Metric"))')

# LSE load caps C12, C13 - 6.8pF
for i, (cx, cy, ref) in enumerate([(snap(84.19), snap(59), "C12"), (snap(91.81), snap(59), "C13")]):
    cp1 = (cx, cy - 3.81)
    cp2 = (cx, cy + 3.81)
    if ref == "C12":
        add_label("LSE_IN", cp1[0], cp1[1], 0)
    else:
        add_label("LSE_OUT", cp1[0], cp1[1], 0)
    add_power("GND", cp2[0], cp2[1])

    c_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
    components.append(f"""  (symbol (lib_id "Device:C") (at {cx} {cy} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "{ref}" (at {cx + 2.54} {cy} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "6.8pF" (at {cx + 2.54} {cy + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0402_1005Metric" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))
{c_pins}
  )""")
    sym_instances.append(f'    (path "/{uid()}" (reference "{ref}") (unit 1) (value "6.8pF") (footprint "Capacitor_SMD:C_0402_1005Metric"))')

# VDD decoupling caps C4-C8 (100nF each) near MCU VDD pins
# Place them near MCU top edge
vdd_cap_data = [
    ("C4", 119.38, 38.1, "+3V3"),  # near pin 1
    ("C5", 121.92, 38.1, "+3V3"),  # near pin 22
    ("C6", 124.46, 38.1, "+3V3"),  # near pin 31
    ("C7", 127.0, 38.1, "+3V3"),     # near pin 41
    ("C8", 132.08, 38.1, "+3V3"),  # near pin 63
]
for ref, cx, cy, _ in vdd_cap_data:
    cp1 = (cx, cy - 3.81)
    cp2 = (cx, cy + 3.81)
    add_power("+3V3", cp1[0], cp1[1])
    add_power("GND", cp2[0], cp2[1])
    c_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
    components.append(f"""  (symbol (lib_id "Device:C") (at {cx} {cy} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "{ref}" (at {cx + 2.54} {cy} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at {cx + 2.54} {cy + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0402_1005Metric" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))
{c_pins}
  )""")
    sym_instances.append(f'    (path "/{uid()}" (reference "{ref}") (unit 1) (value "100nF") (footprint "Capacitor_SMD:C_0402_1005Metric"))')

# C9 VDDA decoupling (1uF)
cx, cy = 129.54, 38.1
cp1 = (cx, cy - 3.81)
cp2 = (cx, cy + 3.81)
add_power("+3V3", cp1[0], cp1[1])
add_power("GND", cp2[0], cp2[1])
c_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:C") (at {cx} {cy} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "C9" (at {cx + 2.54} {cy} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "1uF" (at {cx + 2.54} {cy + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0402_1005Metric" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))
{c_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "C9") (unit 1) (value "1uF") (footprint "Capacitor_SMD:C_0402_1005Metric"))')

# NRST cap (100nF) - C_NRST labeled as C17
cx, cy = snap(95), 48.26
cp1 = (cx, cy - 3.81)
cp2 = (cx, cy + 3.81)
add_label("NRST", cp1[0], cp1[1], 0)
add_power("GND", cp2[0], cp2[1])
c_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:C") (at {cx} {cy} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "C17" (at {cx + 2.54} {cy} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at {cx + 2.54} {cy + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0402_1005Metric" (at {cx} {cy} 0) (effects (font (size 1.27 1.27)) hide))
{c_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "C17") (unit 1) (value "100nF") (footprint "Capacitor_SMD:C_0402_1005Metric"))')

# R5 BOOT0 pull-down (10k) - placed away from crystal area
rx, ry = snap(95), snap(78)
rp1 = (rx, ry - 3.81)
rp2 = (rx, ry + 3.81)
add_label("BOOT0", rp1[0], rp1[1], 0)
add_power("GND", rp2[0], rp2[1])
r_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:R") (at {rx} {ry} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "R5" (at {rx + 2.54} {ry} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "10k" (at {rx + 2.54} {ry + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Resistor_SMD:R_0402_1005Metric" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
{r_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "R5") (unit 1) (value "10k") (footprint "Resistor_SMD:R_0402_1005Metric"))')

# R6 LED resistor (330Ω) + D1 LED
# STATUS_LED label connects from MCU PC13 to R6 pin 1, R6 pin 2 to D1 anode, D1 cathode to GND
rx, ry = snap(88), 50.8
rp1 = (rx, ry - 3.81)
rp2 = (rx, ry + 3.81)
add_label("STATUS_LED", rp1[0], rp1[1], 0)
# Connect R6 pin 2 to LED_ANODE
add_label("LED_ANODE", rp2[0], rp2[1], 0)

r_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:R") (at {rx} {ry} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "R6" (at {rx + 2.54} {ry} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "330" (at {rx + 2.54} {ry + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Resistor_SMD:R_0402_1005Metric" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
{r_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "R6") (unit 1) (value "330") (footprint "Resistor_SMD:R_0402_1005Metric"))')

# D1 LED
dx, dy = snap(88), snap(58)
# LED pins: Pin 1 (K) at (-3.81, 0, 0), Pin 2 (A) at (3.81, 0, 180)
# Place vertically: rotate 90°. Pin 1 at top, pin 2 at bottom.
# Actually, let's place it at 90° rotation. With 90° rotation:
# Pin 1 (K): connection at (dx + 0, dy - (-3.81)) = (dx, dy + 3.81) Wait, rotation complicates things.
# Let me just place it horizontally and use labels.
dp1 = (dx - 3.81, dy)  # K (cathode)
dp2 = (dx + 3.81, dy)  # A (anode)
add_label("LED_ANODE", dp2[0], dp2[1], 0)
add_power("GND", dp1[0], dp1[1])

d_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
components.append(f"""  (symbol (lib_id "Device:LED") (at {dx} {dy} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "D1" (at {dx} {dy - 3} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "Green" (at {dx} {dy + 3} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "LED_SMD:LED_0603_1608Metric" (at {dx} {dy} 0) (effects (font (size 1.27 1.27)) hide))
{d_pins}
  )""")
sym_instances.append(f'    (path "/{uid()}" (reference "D1") (unit 1) (value "Green") (footprint "LED_SMD:LED_0603_1608Metric"))')

# I2C pull-up resistors R1, R2 - omitted to avoid net merging in label-based schematic
# Add in KiCAD GUI later
if False:  # Disabled
  for ref, label_name, ry_off in [("R1", "I2C1_SCL", 0), ("R2", "I2C1_SDA", 8)]:
    rx, ry = snap(170), snap(132 + ry_off)
    rp1 = (rx, ry - 3.81)
    rp2 = (rx, ry + 3.81)
    add_power("+3V3", rp1[0], rp1[1])
    add_wire(rp2[0], rp2[1], rp2[0] + 2.54, rp2[1])
    add_label(label_name, rp2[0], rp2[1], 0)
    r_pins = "\n".join(f'    (pin "{j}" (uuid "{uid()}"))' for j in range(1, 3))
    components.append(f"""  (symbol (lib_id "Device:R") (at {rx} {ry} 0) (unit 1) (uuid "{uid()}")
    (property "Reference" "{ref}" (at {rx + 2.54} {ry} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "4.7k" (at {rx + 2.54} {ry + 2.54} 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Resistor_SMD:R_0402_1005Metric" (at {rx} {ry} 0) (effects (font (size 1.27 1.27)) hide))
{r_pins}
  )""")
    sym_instances.append(f'    (path "/{uid()}" (reference "{ref}") (unit 1) (value "4.7k") (footprint "Resistor_SMD:R_0402_1005Metric"))')

# ============================================================
# Now write the complete file
# ============================================================

# Read existing lib_symbols from the file
with open("/tmp/controller_board_clean.kicad_sch") as f:
    content = f.read()

# Extract lib_symbols section
ls_start = content.index("  (lib_symbols")
ls_end = content.index("\n  )", ls_start) + 4  # end of lib_symbols
lib_symbols_text = content[ls_start:ls_end]

# Add +24V power symbol to lib_symbols
pwrflag_symbol = """    (symbol "power:PWR_FLAG"
      (power)
      (pin_names (offset 0))
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#FLG" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "PWR_FLAG" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "PWR_FLAG_0_1"
        (pin power_out line (at 0 0 90) (length 0) hide (name "pwr" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
      )
    )"""

p24v_symbol = """    (symbol "power:+24V"
      (power)
      (pin_names (offset 0))
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+24V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "+24V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0)))
      )
      (symbol "+24V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+24V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
      )
    )"""

# Remove any existing +24V and PWR_FLAG from lib_symbols (avoid duplicates from prior runs)
# Parse by tracking parens to find symbol blocks
def remove_lib_symbol(text, sym_name):
    """Remove a named symbol block from lib_symbols text by paren-tracking."""
    needle = f'(symbol "{sym_name}"'
    while True:
        idx = text.find(needle)
        if idx == -1:
            break
        # Find the start of line
        line_start = text.rfind('\n', 0, idx)
        if line_start == -1: line_start = 0
        # Track parens from idx to find matching close
        depth = 0
        i = idx
        while i < len(text):
            if text[i] == '(': depth += 1
            elif text[i] == ')': depth -= 1
            if depth == 0:
                # Remove from line_start to i+1
                text = text[:line_start] + text[i+1:]
                break
            i += 1
    return text

lib_symbols_text = remove_lib_symbol(lib_symbols_text, "power:+24V")
lib_symbols_text = remove_lib_symbol(lib_symbols_text, "power:PWR_FLAG")

# Insert PWR_FLAG and +24V symbols before closing of lib_symbols
# The lib_symbols_text ends with "  )"
lib_symbols_text = lib_symbols_text.rstrip()
if lib_symbols_text.endswith(')'):
    lib_symbols_text = lib_symbols_text[:-1].rstrip() + "\n" + pwrflag_symbol + "\n" + p24v_symbol + "\n  )"

# Build existing component instances (keep U1, U2, U3, C1, C2, C3, R_TERM, J10, J2, J_STACK)
# But remove old dangling labels and broken wires
existing_components = []

# U2 AMS1117
existing_components.append("""  (symbol (lib_id "Regulator_Linear:AMS1117-3.3") (at 40.64 35.56 0) (unit 1) (uuid "u0000001-0001-0001-0001-000000000001")
    (property "Reference" "U2" (at 40.64 29.21 0) (effects (font (size 1.27 1.27))))
    (property "Value" "AMS1117-3.3" (at 40.64 31.75 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_TO_SOT_SMD:SOT-223-3_TabPin2" (at 40.64 30.48 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "10101010-1010-1010-1010-101010101010"))
    (pin "2" (uuid "20202020-2020-2020-2020-202020202020"))
    (pin "3" (uuid "30303030-3030-3030-3030-303030303030"))
  )""")

# C1
existing_components.append("""  (symbol (lib_id "Device:C") (at 27.94 45.72 0) (unit 1) (uuid "c0000001-0001-0001-0001-000000000001")
    (property "Reference" "C1" (at 30.48 43.18 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "10uF" (at 30.48 48.26 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 28.9052 49.53 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "c1111111-1111-1111-1111-111111111111"))
    (pin "2" (uuid "c2222222-2222-2222-2222-222222222222"))
  )""")

# C2
existing_components.append("""  (symbol (lib_id "Device:C") (at 50.8 45.72 0) (unit 1) (uuid "c0000002-0002-0002-0002-000000000002")
    (property "Reference" "C2" (at 53.34 43.18 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "10uF" (at 53.34 48.26 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 51.7652 49.53 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "c3333333-3333-3333-3333-333333333333"))
    (pin "2" (uuid "c4444444-4444-4444-4444-444444444444"))
  )""")

# C3
existing_components.append("""  (symbol (lib_id "Device:C") (at 60.96 45.72 0) (unit 1) (uuid "c0000003-0003-0003-0003-000000000003")
    (property "Reference" "C3" (at 63.5 43.18 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "100nF" (at 63.5 48.26 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 61.9252 49.53 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "c5555555-5555-5555-5555-555555555555"))
    (pin "2" (uuid "c6666666-6666-6666-6666-666666666666"))
  )""")

# U1 STM32
mcu_pin_lines = "\n".join(f'    (pin "{i}" (uuid "mcu{i:05d}-{i:04d}-{i:04d}-{i:04d}-{i:012d}"))' for i in range(1, 65))
existing_components.append(f"""  (symbol (lib_id "MCU_ST_STM32G4:STM32G474RETx") (at 127 127 0) (unit 1) (uuid "u0000010-0010-0010-0010-000000000010")
    (property "Reference" "U1" (at 127 43.18 0) (effects (font (size 1.27 1.27))))
    (property "Value" "STM32G474RETx" (at 127 210.82 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_QFP:LQFP-64_10x10mm_P0.5mm" (at 107.95 208.28 0) (effects (font (size 1.27 1.27)) (justify right) hide))
{mcu_pin_lines}
  )""")

# U3 SN65HVD230
existing_components.append("""  (symbol (lib_id "Interface_CAN_LIN:SN65HVD230") (at 215.9 35.56 0) (unit 1) (uuid "u0000020-0020-0020-0020-000000000020")
    (property "Reference" "U3" (at 215.9 22.86 0) (effects (font (size 1.27 1.27))))
    (property "Value" "SN65HVD230" (at 215.9 25.4 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 215.9 48.26 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "can00001-0001-0001-0001-000000000001"))
    (pin "2" (uuid "can00002-0002-0002-0002-000000000002"))
    (pin "3" (uuid "can00003-0003-0003-0003-000000000003"))
    (pin "4" (uuid "can00004-0004-0004-0004-000000000004"))
    (pin "5" (uuid "can00005-0005-0005-0005-000000000005"))
    (pin "6" (uuid "can00006-0006-0006-0006-000000000006"))
    (pin "7" (uuid "can00007-0007-0007-0007-000000000007"))
    (pin "8" (uuid "can00008-0008-0008-0008-000000000008"))
  )""")

# R_TERM
existing_components.append("""  (symbol (lib_id "Device:R") (at 243.84 31.75 0) (unit 1) (uuid "r0000001-0001-0001-0001-000000000001")
    (property "Reference" "R_TERM" (at 246.38 30.48 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Value" "120" (at 246.38 33.02 0) (effects (font (size 1.27 1.27)) (justify left)))
    (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 242.062 31.75 90) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "rt111111-1111-1111-1111-111111111111"))
    (pin "2" (uuid "rt222222-2222-2222-2222-222222222222"))
  )""")

# J10
existing_components.append("""  (symbol (lib_id "Connector_Generic:Conn_01x02") (at 15.24 35.56 0) (mirror x) (unit 1) (uuid "j0000010-0010-0010-0010-000000000010")
    (property "Reference" "J10" (at 15.24 40.64 0) (effects (font (size 1.27 1.27))))
    (property "Value" "PWR_IN" (at 15.24 38.1 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" (at 15.24 35.56 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "j10-0001-0001-0001-000000000001"))
    (pin "2" (uuid "j10-0002-0002-0002-000000000002"))
  )""")

# J2
existing_components.append("""  (symbol (lib_id "Connector_Generic:Conn_01x04") (at 240.03 35.56 0) (unit 1) (uuid "j0000002-0002-0002-0002-000000000002")
    (property "Reference" "J2" (at 240.03 27.94 0) (effects (font (size 1.27 1.27))))
    (property "Value" "CAN" (at 240.03 30.48 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" (at 240.03 35.56 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "j2-00001-0001-0001-000000000001"))
    (pin "2" (uuid "j2-00002-0002-0002-000000000002"))
    (pin "3" (uuid "j2-00003-0003-0003-000000000003"))
    (pin "4" (uuid "j2-00004-0004-0004-000000000004"))
  )""")

# J_STACK
jstk_pins = "\n".join(f'    (pin "{i}" (uuid "jstk-{i:03d}-{i:04d}-{i:04d}-{i:04d}-{i:012d}"))' for i in range(1, 41))
existing_components.append(f"""  (symbol (lib_id "Connector_Generic:Conn_02x20_Odd_Even") (at 127 254 0) (unit 1) (uuid "j0000099-0099-0099-0099-000000000099")
    (property "Reference" "J_STACK" (at 128.27 223.52 0) (effects (font (size 1.27 1.27))))
    (property "Value" "Stack_Connector" (at 128.27 226.06 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical" (at 127 254 0) (effects (font (size 1.27 1.27)) hide))
{jstk_pins}
  )""")

# Existing power symbols that are still valid
# Keep #PWR03 (GND at LDO), #PWR04 (GND at CAN), #PWR05 (+3V3 at CAN VCC)
# Remove #PWR01 (+5V at 27.94,35.56) and #PWR02 (+3V3 at 60.96,35.56) - replaced by new ones

existing_power = []
existing_power.append("""  (symbol (lib_id "power:GND") (at 215.9 48.26 0) (unit 1) (uuid "pwr00004-0004-0004-0004-000000000004")
    (property "Reference" "#PWR04" (at 215.9 54.61 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "GND" (at 215.9 52.07 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 215.9 48.26 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "pwrgnd02-0002-0002-000000000002"))
  )""")

existing_power.append("""  (symbol (lib_id "power:+3V3") (at 215.9 22.86 0) (unit 1) (uuid "pwr00005-0005-0005-0005-000000000005")
    (property "Reference" "#PWR05" (at 215.9 26.67 0) (effects (font (size 1.27 1.27)) hide))
    (property "Value" "+3V3" (at 215.9 19.05 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 215.9 22.86 0) (effects (font (size 1.27 1.27)) hide))
    (pin "1" (uuid "pwr33v02-0002-0002-000000000002"))
  )""")

# Existing symbol_instances for kept components
existing_sym_instances = [
    '    (path "/u0000001-0001-0001-0001-000000000001" (reference "U2") (unit 1) (value "AMS1117-3.3") (footprint "Package_TO_SOT_SMD:SOT-223-3_TabPin2"))',
    '    (path "/c0000001-0001-0001-0001-000000000001" (reference "C1") (unit 1) (value "10uF") (footprint "Capacitor_SMD:C_0805_2012Metric"))',
    '    (path "/c0000002-0002-0002-0002-000000000002" (reference "C2") (unit 1) (value "10uF") (footprint "Capacitor_SMD:C_0805_2012Metric"))',
    '    (path "/c0000003-0003-0003-0003-000000000003" (reference "C3") (unit 1) (value "100nF") (footprint "Capacitor_SMD:C_0603_1608Metric"))',
    '    (path "/u0000010-0010-0010-0010-000000000010" (reference "U1") (unit 1) (value "STM32G474RETx") (footprint "Package_QFP:LQFP-64_10x10mm_P0.5mm"))',
    '    (path "/u0000020-0020-0020-0020-000000000020" (reference "U3") (unit 1) (value "SN65HVD230") (footprint "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"))',
    '    (path "/r0000001-0001-0001-0001-000000000001" (reference "R_TERM") (unit 1) (value "120") (footprint "Resistor_SMD:R_0603_1608Metric"))',
    '    (path "/j0000010-0010-0010-0010-000000000010" (reference "J10") (unit 1) (value "PWR_IN") (footprint "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical"))',
    '    (path "/j0000002-0002-0002-0002-000000000002" (reference "J2") (unit 1) (value "CAN") (footprint "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical"))',
    '    (path "/j0000099-0099-0099-0099-000000000099" (reference "J_STACK") (unit 1) (value "Stack_Connector") (footprint "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical"))',
    '    (path "/pwr00004-0004-0004-0004-000000000004" (reference "#PWR04") (unit 1) (value "GND") (footprint ""))',
    '    (path "/pwr00005-0005-0005-0005-000000000005" (reference "#PWR05") (unit 1) (value "+3V3") (footprint ""))',
]

# Text annotations
texts = [
    '  (text "POWER SECTION" (at 25.4 20.32 0) (effects (font (size 2.54 2.54)) (justify left bottom)) (uuid "t0000001-0001-0001-0001-000000000001"))',
    '  (text "MCU SECTION" (at 100.33 55.88 0) (effects (font (size 2.54 2.54)) (justify left bottom)) (uuid "t0000002-0002-0002-0002-000000000002"))',
    '  (text "CAN SECTION" (at 200.66 20.32 0) (effects (font (size 2.54 2.54)) (justify left bottom)) (uuid "t0000003-0003-0003-0003-000000000003"))',
]

# ============================================================
# Assemble the file
# ============================================================
output = []
output.append("""(kicad_sch
  (version 20231120)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "a1b2c3d4-e5f6-7890-abcd-ef1234567890")
  (paper "A3")
  (title_block
    (title "Epicura Controller Board")
    (date "2026-02-17")
    (rev "1.0")
    (company "Epicura")
    (comment 1 "STM32G474RET6 Controller PCB")
  )
""")

output.append(lib_symbols_text)
output.append("")

# Wires
for w in wires:
    output.append(w)

# Labels
for l in labels:
    output.append(l)

# No-connects
for nc in no_connects:
    output.append(nc)

# Text annotations
for t in texts:
    output.append(t)

# Existing components
for c in existing_components:
    output.append(c)

# New components
for c in components:
    output.append(c)

# Existing power symbols
for p in existing_power:
    output.append(p)

# New power symbols
for p in power_syms:
    output.append(p)

# Sheet instances
output.append("""
  (sheet_instances
    (path "/" (page "1"))
  )
""")

# Symbol instances
output.append("  (symbol_instances")
for si in existing_sym_instances:
    output.append(si)
for si in sym_instances:
    output.append(si)
output.append("  )")

output.append(")")

# Write the file
outpath = "/Users/manaspradhan/Library/Mobile Documents/iCloud~md~obsidian/Documents/ClaudeNotes/__Workspaces/Epicura/pcb/controller-board/controller-board.kicad_sch"
with open(outpath, 'w') as f:
    f.write("\n".join(output))

print(f"Written {len(output)} lines to {outpath}")

# Post-process: fix floating point precision (e.g., 93.97999999999999 -> 93.98)
import re
with open(outpath) as f:
    text = f.read()

def fix_float(m):
    val = float(m.group(0))
    rounded = round(val, 2)
    # Format without trailing zeros but keep at least one decimal
    s = f"{rounded:g}"
    return s

text = re.sub(r'-?\d+\.\d{3,}', fix_float, text)

with open(outpath, 'w') as f:
    f.write(text)
print("Post-processed: fixed floating point precision")

# Verify parenthesis balance
with open(outpath) as f:
    text = f.read()
depth = 0
for i, ch in enumerate(text):
    if ch == '(':
        depth += 1
    elif ch == ')':
        depth -= 1
    if depth < 0:
        print(f"ERROR: Negative depth at position {i}")
        break
print(f"Final paren depth: {depth}")
if depth != 0:
    print("WARNING: Parentheses not balanced!")
else:
    print("OK: Parentheses balanced")
