#!/usr/bin/env python3
"""Generate complete KiCAD 9 schematic for Epicura Driver Board.
All lib_symbols are defined inline so KiCAD can load without crashes."""

from pathlib import Path

PROJECT_UUID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
_counter = 0

def uid():
    global _counter
    _counter += 1
    return f"dd{_counter:06d}-{_counter:04d}-{_counter:04d}-{_counter:04d}-{_counter:012d}"

# ── Buffers ──────────────────────────────────────────────────────
symbols_buf = []
wires_buf = []
labels_buf = []
pwr_n = [1]

# ── Helpers ──────────────────────────────────────────────────────
def pwr(sym_type, x, y):
    n = pwr_n[0]; pwr_n[0] += 1
    ref = f"#PWR{n:03d}"
    lib_map = {"+24V":"power:+24V","+12V":"power:+12V","+6V5":"power:+6V5",
               "+5V":"power:+5V","+3V3":"power:+3V3","GND":"power:GND"}
    is_gnd = sym_type == "GND"
    symbols_buf.append(f'''  (symbol (lib_id "{lib_map[sym_type]}") (at {x} {y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")
    (property "Reference" "{ref}" (at {x} {y+(3.81 if is_gnd else -3.81)} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "{sym_type}" (at {x} {y+(-3.81 if is_gnd else 3.81)} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "{uid()}"))
    (instances (project "" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )''')

def lbl(name, x, y, angle=0):
    labels_buf.append(f'  (label "{name}" (at {x} {y} {angle}) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uid()}"))')

def wire(x1, y1, x2, y2):
    wires_buf.append(f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))')

def comp(lib_id, ref, value, x, y, rot=0, mirror="", fp="", pins=None):
    u = uid()
    ms = f'\n    (mirror {mirror})' if mirror else ''
    ps = '\n'.join(f'    (pin "{p}" (uuid "{uid()}"))' for p in (pins or []))
    symbols_buf.append(f'''  (symbol (lib_id "{lib_id}") (at {x} {y} {rot}){ms} (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{u}")
    (property "Reference" "{ref}" (at {x} {y-3.81} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{value}" (at {x} {y+3.81} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "{fp}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
{ps}
    (instances (project "" (path "/{PROJECT_UUID}" (reference "{ref}") (unit 1))))
  )''')

# ── lib_symbols ──────────────────────────────────────────────────

def _pin(num, name, x, y, angle, length, etype="passive"):
    return (f'      (pin {etype} line (at {x} {y} {angle}) (length {length})'
            f' (name "{name}" (effects (font (size 1.27 1.27))))'
            f' (number "{num}" (effects (font (size 1.27 1.27)))))')

def _simple_2pin(sym_name, ref_prefix, body_lines=""):
    """2-pin passive: pin 1 top (0,3.81,270) pin 2 bot (0,-3.81,90)"""
    return f'''    (symbol "{sym_name}"
      (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "{ref_prefix}" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Value" "{sym_name}" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "{sym_name.split(':')[1]}_1_1"
{body_lines}
{_pin("1","~",0,3.81,270,1.27)}
{_pin("2","~",0,-3.81,90,1.27)}
      )
      (embedded_fonts no)
    )'''

def _rect_body(x1, y1, x2, y2):
    return f'        (rectangle (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.254) (type default)) (fill (type background)))'

def _power_sym(sym_name, val):
    """Power symbol lib def (1 pin)."""
    # GND pin goes down (270->90 for length direction), others go up
    is_gnd = "GND" in sym_name
    pa, pl = (90, 0) if is_gnd else (270, 0)
    return f'''    (symbol "{sym_name}"
      (pin_names (offset 0)) (exclude_from_sim no) (in_bom no) (on_board yes)
      (property "Reference" "#PWR" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "{val}" (at 0 {3.81 if is_gnd else -3.81} 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "{sym_name.split(':')[1]}_1_1"
{_pin("1",val,0,0,pa,pl,"power_in")}
      )
      (embedded_fonts no)
    )'''

def _conn_1xN(n):
    """Connector_Generic:Conn_01x0N lib symbol."""
    name = f"Connector_Generic:Conn_01x{n:02d}"
    short = f"Conn_01x{n:02d}"
    # pins: pin k at (-5.08, top_y - (k-1)*2.54, 0), length 3.81
    top_y = (n - 1) * 2.54 / 2
    pins = '\n'.join(_pin(str(k+1), f"Pin_{k+1}", -5.08, top_y - k*2.54, 0, 3.81) for k in range(n))
    h = top_y + 1.27
    return f'''    (symbol "{name}"
      (pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 {h+1.27} 0) (effects (font (size 1.27 1.27))))
      (property "Value" "{short}" (at 0 {-h-1.27} 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "{short}_1_1"
        (rectangle (start -1.27 {h}) (end 1.27 {-h}) (stroke (width 0.254) (type default)) (fill (type background)))
{pins}
      )
      (embedded_fonts no)
    )'''

def _conn_2x20():
    """Conn_02x20_Odd_Even"""
    top_y = 24.13
    pins_l = '\n'.join(_pin(str(2*k+1), f"Pin_{2*k+1}", -5.08, top_y - k*2.54, 0, 3.81) for k in range(20))
    pins_r = '\n'.join(_pin(str(2*k+2), f"Pin_{2*k+2}", 5.08, top_y - k*2.54, 180, 3.81) for k in range(20))
    return f'''    (symbol "Connector_Generic:Conn_02x20_Odd_Even"
      (pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 26.67 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_02x20_Odd_Even" (at 0 -26.67 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "Conn_02x20_Odd_Even_1_1"
        (rectangle (start -1.27 25.4) (end 1.27 -25.4) (stroke (width 0.254) (type default)) (fill (type background)))
{pins_l}
{pins_r}
      )
      (embedded_fonts no)
    )'''

def _fet_sym(name, ref_pfx):
    """N-MOSFET: pin1=G(-5.08,0,0) pin2=D(2.54,5.08,270) pin3=S(2.54,-5.08,90)"""
    return f'''    (symbol "{name}"
      (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "{ref_pfx}" (at 5.08 1.905 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "{name}" (at 5.08 -1.905 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "{name.split(':')[1]}_1_1"
        (rectangle (start -2.54 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type default)) (fill (type background)))
{_pin("1","G",-5.08,0,0,2.54,"input")}
{_pin("2","D",2.54,5.08,270,0,"passive")}
{_pin("3","S",2.54,-5.08,90,0,"passive")}
      )
      (embedded_fonts no)
    )'''

def _custom_ic(name, ref_pfx, pins_def, w=10.16, h=10.16):
    """Custom IC. pins_def = [(num, name, x, y, angle, etype), ...]"""
    pin_strs = '\n'.join(_pin(str(num), pname, px, py, pa, 2.54, pe) for num, pname, px, py, pa, pe in pins_def)
    short = name.split(':')[1]
    return f'''    (symbol "{name}"
      (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "{ref_pfx}" (at 0 {h/2+2.54} 0) (effects (font (size 1.27 1.27))))
      (property "Value" "{short}" (at 0 {-h/2-2.54} 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "{short}_1_1"
{_rect_body(-w/2, h/2, w/2, -h/2)}
{pin_strs}
      )
      (embedded_fonts no)
    )'''

def build_lib_symbols():
    parts = []
    # Power
    for s,v in [("power:+24V","+24V"),("power:+12V","+12V"),("power:+6V5","+6V5"),
                ("power:+5V","+5V"),("power:+3V3","+3V3"),("power:GND","GND")]:
        parts.append(_power_sym(s, v))
    # Passives
    for s,r in [("Device:R","R"),("Device:L","L"),("Device:Polyfuse","F")]:
        parts.append(_simple_2pin(s, r, _rect_body(-1.016, 2.54, 1.016, -2.54)))
    parts.append(_simple_2pin("Device:C", "C",
        '        (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))\n'
        '        (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))'))
    parts.append(_simple_2pin("Device:C_Polarized", "C",
        '        (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))\n'
        '        (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))'))
    # Diode
    parts.append(f'''    (symbol "Diode:SS54"
      (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "SS54" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "SS54_1_1"
        (polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -1.27 0) (xy 1.27 1.27) (xy 1.27 -1.27) (xy -1.27 0)) (stroke (width 0.254) (type default)) (fill (type outline)))
{_pin("1","K",-2.54,0,0,1.27)}
{_pin("2","A",2.54,0,180,1.27)}
      )
      (embedded_fonts no)
    )''')
    # FETs
    parts.append(_fet_sym("Transistor_FET:IRLML6344", "Q"))
    parts.append(_fet_sym("Transistor_FET:2N7002", "Q"))
    # Connectors
    for n in [2, 3, 8]:
        parts.append(_conn_1xN(n))
    parts.append(_conn_2x20())
    # Custom ICs
    # MP1584EN
    parts.append(_custom_ic("Driver:MP1584EN", "U", [
        (1,"IN",-12.7,5.08,0,"power_in"),
        (5,"EN",-12.7,2.54,0,"input"),
        (7,"FREQ",-12.7,-2.54,0,"passive"),
        (8,"SS",-12.7,-5.08,0,"passive"),
        (2,"SW",12.7,5.08,180,"output"),
        (6,"BST",12.7,2.54,180,"passive"),
        (4,"FB",12.7,0,180,"input"),
        (3,"GND",0,-10.16,90,"power_in"),
    ], 20.32, 15.24))
    # DRV8876
    parts.append(_custom_ic("Driver:DRV8876", "U", [
        (1,"VM",0,12.7,270,"power_in"),
        (2,"GND",0,-10.16,90,"power_in"),
        (5,"nSLEEP",-12.7,5.08,0,"input"),
        (8,"EN",-12.7,2.54,0,"input"),
        (7,"PH",-12.7,0,0,"input"),
        (6,"nFAULT",-12.7,-2.54,0,"output"),
        (3,"OUT1",12.7,2.54,180,"output"),
        (4,"OUT2",12.7,0,180,"output"),
    ], 20.32, 17.78))
    # TB6612FNG - simplified 14-pin functional view
    tb_pins = [
        (1,"AO1",15.24,10.16,180,"output"),
        (5,"AO2",15.24,7.62,180,"output"),
        (11,"BO1",15.24,2.54,180,"output"),
        (7,"BO2",15.24,5.08,180,"output"),
        (13,"VM",0,15.24,270,"power_in"),
        (21,"VCC",-2.54,15.24,270,"power_in"),
        (19,"GND",0,-12.7,90,"power_in"),
        (20,"STBY",-15.24,-5.08,0,"input"),
        (24,"PWMA",-15.24,10.16,0,"input"),
        (22,"AIN1",-15.24,7.62,0,"input"),
        (23,"AIN2",-15.24,5.08,0,"input"),
        (16,"PWMB",-15.24,2.54,0,"input"),
        (18,"BIN1",-15.24,0,0,"input"),
        (17,"BIN2",-15.24,-2.54,0,"input"),
        # Doubled/GND pins as passive
        (2,"AO1b",15.24,12.7,180,"passive"),
        (6,"AO2b",15.24,-2.54,180,"passive"),
        (8,"BO2b",15.24,-5.08,180,"passive"),
        (12,"BO1b",15.24,0,180,"passive"),
        (3,"PGND1",2.54,-12.7,90,"passive"),
        (4,"PGND1b",5.08,-12.7,90,"passive"),
        (9,"PGND2",-2.54,-12.7,90,"passive"),
        (10,"PGND2b",-5.08,-12.7,90,"passive"),
        (14,"VM2",2.54,15.24,270,"passive"),
        (15,"VM3",5.08,15.24,270,"passive"),
    ]
    parts.append(_custom_ic("Driver:TB6612FNG", "U", tb_pins, 25.4, 22.86))
    # PCF8574
    pcf_pins = [
        (1,"A0",-12.7,7.62,0,"input"),
        (2,"A1",-12.7,5.08,0,"input"),
        (3,"A2",-12.7,2.54,0,"input"),
        (14,"SCL",-12.7,0,0,"input"),
        (15,"SDA",-12.7,-2.54,0,"bidirectional"),
        (13,"~{INT}",-12.7,-5.08,0,"output"),
        (16,"VDD",0,12.7,270,"power_in"),
        (8,"VSS",0,-10.16,90,"power_in"),
        (4,"P0",12.7,7.62,180,"bidirectional"),
        (5,"P1",12.7,5.08,180,"bidirectional"),
        (6,"P2",12.7,2.54,180,"bidirectional"),
        (7,"P3",12.7,0,180,"bidirectional"),
        (9,"P4",12.7,-2.54,180,"bidirectional"),
        (10,"P5",12.7,-5.08,180,"bidirectional"),
        (11,"P6",12.7,-7.62,180,"bidirectional"),
        (12,"P7",12.7,-10.16,180,"bidirectional"),
    ]
    parts.append(_custom_ic("Driver:PCF8574", "U", pcf_pins, 20.32, 20.32))
    # INA219
    ina_pins = [
        (1,"SCL",-10.16,5.08,0,"input"),
        (2,"SDA",-10.16,2.54,0,"bidirectional"),
        (5,"A0",-10.16,-2.54,0,"input"),
        (6,"A1",-10.16,-5.08,0,"input"),
        (3,"VS",0,10.16,270,"power_in"),
        (4,"GND",0,-7.62,90,"power_in"),
        (7,"IN+",10.16,2.54,180,"passive"),
        (8,"IN-",10.16,-2.54,180,"passive"),
    ]
    parts.append(_custom_ic("Driver:INA219", "U", ina_pins, 15.24, 15.24))

    return "  (lib_symbols\n" + "\n".join(parts) + "\n  )"

# ── Component Placement ──────────────────────────────────────────

def place_components():
    # === INPUT PROTECTION (row at y=30) ===
    comp("Connector_Generic:Conn_01x02","J_24V_IN","XT30",20,30,180,"","Connector_XT:XT30PW-M",["1","2"])
    # Polyfuse
    comp("Device:Polyfuse","F1","5A",35,27,90,"","Resistor_SMD:R_1812_4532Metric",["1","2"])
    # SS54 reverse polarity
    comp("Diode:SS54","D1","SS54",45,27,0,"","Diode_SMD:D_SMA",["1","2"])
    # TVS
    comp("Device:C","D2","SMBJ24A",55,30,0,"","Diode_SMD:D_SMB",["1","2"])
    pwr("+24V",27,22)
    pwr("GND",27,35)
    pwr("GND",55,35)
    lbl("+24V_PROT",60,27)
    wire(25,27,31.19,27); wire(38.81,27,42.46,27); wire(47.54,27,55,27)
    wire(55,26.19,55,27)

    # === BUCK CONVERTER 1: 24V→12V (around x=90,y=55) ===
    comp("Driver:MP1584EN","U1","MP1584EN_12V",90,55,0,"","Package_TO_SOT_SMD:SOT-23-8",
         ["1","2","3","4","5","6","7","8"])
    comp("Device:L","L1","33uH",110,50,90,"","Inductor_SMD:L_1210_3225Metric",["1","2"])
    comp("Diode:SS54","D_BST1","SS34",105,45,0,"","Diode_SMD:D_SMA",["1","2"])
    comp("Device:C","C_IN1","10uF",75,60,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C","C_OUT1a","22uF",120,60,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C","C_OUT1b","22uF",125,60,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C_Polarized","C_BULK3","100uF/25V",130,60,0,"","Capacitor_THT:CP_Radial_D6.3mm_P2.50mm",["1","2"])
    comp("Device:R","R_FB1_TOP","140k",105,65,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:R","R_FB1_BOT","10k",105,75,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:Polyfuse","F2","1.5A",140,55,90,"","Resistor_SMD:R_0805_2012Metric",["1","2"])
    comp("Device:C","D3","SMBJ12A",148,60,0,"","Diode_SMD:D_SMB",["1","2"])
    lbl("+24V_PROT",77.3,50)
    pwr("GND",90,66); pwr("GND",75,65); pwr("GND",120,65); pwr("GND",125,65)
    pwr("GND",130,65); pwr("GND",105,80); pwr("GND",148,65)
    pwr("+12V",148,52)

    # === BUCK CONVERTER 2: 24V→6.5V (around x=90,y=100) ===
    comp("Driver:MP1584EN","U2","MP1584EN_6V5",90,100,0,"","Package_TO_SOT_SMD:SOT-23-8",
         ["1","2","3","4","5","6","7","8"])
    comp("Device:L","L2","22uH",110,95,90,"","Inductor_SMD:L_1210_3225Metric",["1","2"])
    comp("Diode:SS54","D_BST2","SS34",105,90,0,"","Diode_SMD:D_SMA",["1","2"])
    comp("Device:C","C_IN2","10uF",75,105,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C","C_OUT2a","22uF",120,105,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C","C_OUT2b","22uF",125,105,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C_Polarized","C_BULK1","470uF/10V",130,105,0,"","Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",["1","2"])
    comp("Device:R","R_FB2_TOP","71.5k",105,110,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:R","R_FB2_BOT","10k",105,120,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:Polyfuse","F3","3A",140,100,90,"","Resistor_SMD:R_1206_3216Metric",["1","2"])
    comp("Device:C","D4","SMBJ6.5A",148,105,0,"","Diode_SMD:D_SMB",["1","2"])
    lbl("+24V_PROT",77.3,95)
    pwr("GND",90,111); pwr("GND",75,110); pwr("GND",120,110); pwr("GND",125,110)
    pwr("GND",130,110); pwr("GND",105,125); pwr("GND",148,110)
    pwr("+6V5",148,97)

    # === BUCK CONVERTER 3: 24V→5V (around x=90,y=145) ===
    comp("Driver:MP1584EN","U3","MP1584EN_5V",90,145,0,"","Package_TO_SOT_SMD:SOT-23-8",
         ["1","2","3","4","5","6","7","8"])
    comp("Device:L","L3","22uH",110,140,90,"","Inductor_SMD:L_1210_3225Metric",["1","2"])
    comp("Diode:SS54","D_BST3","SS34",105,135,0,"","Diode_SMD:D_SMA",["1","2"])
    comp("Device:C","C_IN3","10uF",75,150,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C","C_OUT3a","22uF",120,150,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C","C_OUT3b","22uF",125,150,0,"","Capacitor_SMD:C_0805_2012Metric",["1","2"])
    comp("Device:C_Polarized","C_BULK5V","220uF/10V",130,150,0,"","Capacitor_THT:CP_Radial_D6.3mm_P2.50mm",["1","2"])
    comp("Device:R","R_FB3_TOP","52.3k",105,155,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:R","R_FB3_BOT","10k",105,165,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:Polyfuse","F4","2A",140,145,90,"","Resistor_SMD:R_1206_3216Metric",["1","2"])
    comp("Device:C","D5","SMBJ5.0A",148,150,0,"","Diode_SMD:D_SMB",["1","2"])
    lbl("+24V_PROT",77.3,140)
    pwr("GND",90,156); pwr("GND",75,155); pwr("GND",120,155); pwr("GND",125,155)
    pwr("GND",130,155); pwr("GND",105,170); pwr("GND",148,155)
    pwr("+5V",148,142)

    # === INA219 Current Monitor (x=200, y=40) ===
    comp("Driver:INA219","U7","INA219",200,40,0,"","Package_TO_SOT_SMD:SOT-23-8",
         ["1","2","3","4","5","6","7","8"])
    comp("Device:R","R_SHUNT","10mR",220,35,90,"","Resistor_SMD:R_2512_6332Metric",["1","2"])
    comp("Device:C","C_VS7","100nF",210,50,0,"","Capacitor_SMD:C_0402_1005Metric",["1","2"])
    pwr("+3V3",200,28); pwr("GND",200,49); pwr("GND",210,55)
    pwr("GND",189.84,45.48)  # A0 to GND
    pwr("GND",189.84,47.98)  # A1 to GND
    lbl("I2C1_SCL",185,35)
    lbl("I2C1_SDA",185,38)
    wire(189.84,35.08,185,35.08); wire(189.84,37.62,185,37.62)
    lbl("+24V_PROT",225,35)

    # === DRV8876 #1 (CID actuator 1, x=200, y=100) ===
    comp("Driver:DRV8876","U4","DRV8876",200,100,0,"","Package_SO:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm",
         ["1","2","3","4","5","6","7","8"])
    comp("Device:C","C_VM4","100nF",185,95,0,"","Capacitor_SMD:C_0402_1005Metric",["1","2"])
    comp("Device:R","R_SENSE1","1k",220,105,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Connector_Generic:Conn_01x02","J_CID_LACT1","CID_LACT1",230,100,0,"",
         "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",["1","2"])
    pwr("+12V",200,85); pwr("GND",200,112); pwr("GND",185,100); pwr("GND",220,110)
    pwr("+3V3",187.3,103)  # nSLEEP pull-up
    lbl("CID_LACT1_EN",183,97)
    lbl("CID_LACT1_PH",183,100)
    wire(187.3,102.54,187.3,103); wire(187.3,97.46,183,97.46); wire(187.3,100,183,100)

    # === DRV8876 #2 (CID actuator 2, x=200, y=135) ===
    comp("Driver:DRV8876","U5","DRV8876",200,135,0,"","Package_SO:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm",
         ["1","2","3","4","5","6","7","8"])
    comp("Device:C","C_VM5","100nF",185,130,0,"","Capacitor_SMD:C_0402_1005Metric",["1","2"])
    comp("Device:R","R_SENSE2","1k",220,140,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Connector_Generic:Conn_01x02","J_CID_LACT2","CID_LACT2",230,135,0,"",
         "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",["1","2"])
    pwr("+12V",200,120); pwr("GND",200,147); pwr("GND",185,135); pwr("GND",220,145)
    pwr("+3V3",187.3,138)
    lbl("CID_LACT2_EN",183,132)
    lbl("CID_LACT2_PH",183,135)
    wire(187.3,137.54,187.3,138); wire(187.3,132.54,183,132.54); wire(187.3,135,183,135)

    # === TB6612FNG (SLD pumps, x=200, y=185) ===
    comp("Driver:TB6612FNG","U6","TB6612FNG",200,185,0,"","Package_SO:SSOP-24_3.9x8.7mm_P0.635mm",
         [str(i) for i in range(1,25)])
    comp("Device:C","C_VM6","100nF",210,170,0,"","Capacitor_SMD:C_0402_1005Metric",["1","2"])
    comp("Device:C","C_VCC6","100nF",195,170,0,"","Capacitor_SMD:C_0402_1005Metric",["1","2"])
    comp("Connector_Generic:Conn_01x08","J_SLD","SLD",235,185,0,"",
         "Connector_JST:JST_XH_B8B-XH-A_1x08_P2.50mm_Vertical",["1","2","3","4","5","6","7","8"])
    pwr("+12V",200,168); pwr("+3V3",197.46,168); pwr("GND",200,199)
    pwr("GND",210,175); pwr("GND",195,175)
    pwr("+3V3",184.76,191)  # STBY pull-up
    lbl("SLD_PUMP1_PWM",180,175)
    lbl("SLD_PUMP1_DIR",180,178)
    lbl("SLD_PUMP2_PWM",180,183)
    lbl("SLD_PUMP2_DIR",180,185)
    wire(184.76,195.16,180,195.16); wire(184.76,192.62,180,192.62)
    wire(184.76,190.08,180,190.08); wire(184.76,187.54,180,187.54)
    wire(184.76,185,180,185); wire(184.76,182.46,180,182.46)

    # === MAIN SERVO (x=290, y=30) ===
    comp("Connector_Generic:Conn_01x03","J_MAIN_SERVO","DS3225",300,30,0,"y",
         "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",["1","2","3"])
    comp("Device:R","R_SERVO","33R",290,33,90,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    pwr("GND",305,28); pwr("+6V5",305,30)
    lbl("MAIN_SERVO_PWM",283,33)
    wire(286.19,32.54,283,32.54)

    # === FAN DRIVERS (x=290, y=65 and y=85) ===
    def mosfet_driver(qref, qlib, dref, jref, jval, rg_ref, rpd_ref, x, y, signal_label):
        comp(qlib, qref, qlib.split(":")[1], x, y, 0, "", "Package_TO_SOT_SMD:SOT-23", ["1","2","3"])
        comp("Device:R", rg_ref, "100R", x-10, y, 90, "", "Resistor_SMD:R_0402_1005Metric", ["1","2"])
        comp("Device:R", rpd_ref, "10k", x+2.54, y+8, 0, "", "Resistor_SMD:R_0402_1005Metric", ["1","2"])
        comp("Diode:SS54", dref, "SS14", x+5, y-5, 90, "", "Diode_SMD:D_SMA", ["1","2"])
        comp("Connector_Generic:Conn_01x02", jref, jval, x+15, y, 0, "",
             "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical", ["1","2"])
        pwr("+12V", x+5, y-8)
        pwr("GND", x+2.54, y+13)
        lbl(signal_label, x-18, y)
        wire(x-5.08, y, x-13.81, y)  # gate R to MOSFET
        wire(x-13.81, y, x-18, y)  # label to gate R

    mosfet_driver("Q3","Transistor_FET:IRLML6344","D8","J_FAN1","Fan1","R_Q3_GATE","R_Q3_PD",290,65,"FAN1_PWM")
    mosfet_driver("Q4","Transistor_FET:IRLML6344","D9","J_FAN2","Fan2","R_Q4_GATE","R_Q4_PD",290,85,"FAN2_PWM")

    # === SLD SOLENOID DRIVERS (x=290, y=105 and y=125) ===
    mosfet_driver("Q1","Transistor_FET:IRLML6344","D6","J_SLD_SOL1","SLD_SOL1","R_Q1_GATE","R_Q1_PD",290,105,"SLD_SOL1_EN")
    mosfet_driver("Q2","Transistor_FET:IRLML6344","D7","J_SLD_SOL2","SLD_SOL2","R_Q2_GATE","R_Q2_PD",290,125,"SLD_SOL2_EN")

    # === BUZZER DRIVER (x=290, y=145) ===
    comp("Transistor_FET:2N7002","Q12","2N7002",290,145,0,"","Package_TO_SOT_SMD:SOT-23",["1","2","3"])
    comp("Device:R","R_Q12_GATE","100R",280,145,90,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Device:R","R_Q12_PD","10k",292.54,153,0,"","Resistor_SMD:R_0402_1005Metric",["1","2"])
    comp("Connector_Generic:Conn_01x02","J_BUZZER","Buzzer",305,145,0,"",
         "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",["1","2"])
    pwr("+5V",295,137)
    pwr("GND",292.54,158)
    lbl("BUZZER_PWM",272,145)
    wire(284.92,145,280,145); wire(276.19,145,272,145)

    # === P-ASD PUMP DRIVER (x=290, y=170) ===
    mosfet_driver("Q5","Transistor_FET:IRLML6344","D10","J_PASD_PUMP","PASD_Pump","R_Q5_GATE","R_Q5_PD",290,170,"PASD_PUMP_PWM")

    # === PCF8574 (x=350, y=220) ===
    comp("Driver:PCF8574","U8","PCF8574",350,220,0,"","Package_SO:SOIC-16_3.9x9.9mm_P1.27mm",
         [str(i) for i in range(1,17)])
    comp("Device:C","C_VDD8","100nF",340,210,0,"","Capacitor_SMD:C_0402_1005Metric",["1","2"])
    pwr("+3V3",350,205); pwr("GND",350,232); pwr("GND",340,215)
    # A0,A1,A2 to GND for addr 0x20
    pwr("GND",337.3,213); pwr("GND",337.3,215); pwr("GND",337.3,218)
    lbl("I2C1_SCL",333,220)
    lbl("I2C1_SDA",333,223)
    wire(337.3,220,333,220); wire(337.3,222.54,333,222.54)

    # === P-ASD SOLENOID DRIVERS Q6-Q11 (x=380, y=200..300) ===
    for i in range(6):
        q_num = 6 + i
        y_pos = 200 + i * 18
        sol_name = f"PASD_SOL{i+1}"
        mosfet_driver(f"Q{q_num}","Transistor_FET:IRLML6344",
                      f"D{11+i}",f"J_PASD_SOL{i+1}",sol_name,
                      f"R_Q{q_num}_GATE",f"R_Q{q_num}_PD",
                      380, y_pos, f"PCF_P{i}")
        # Label PCF output to MOSFET gate
        lbl(f"PCF_P{i}", 362.7, 220 - 2.54*(3-i) if i < 4 else 220 - 2.54*(3-i))

    # Connect PCF8574 P0-P5 outputs to labels
    for i in range(6):
        pin_y = 220 - 7.62 + i * 2.54  # P0 at top
        lbl(f"PCF_P{i}", 367, pin_y)

    # === J_STACK (40-pin stacking connector, x=50, y=280) ===
    comp("Connector_Generic:Conn_02x20_Odd_Even","J_STACK","J_STACK",50,280,0,"",
         "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical",
         [str(i) for i in range(1,41)])

    # J_STACK power connections
    # Pins 1-4: +24V
    for p in [1,2,3,4]:
        row = (p-1)//2; x_off = -5.08 if p%2==1 else 5.08
        py = 280 - (24.13 - row*2.54)
        px = 50 + x_off
        pwr("+24V", px - (5 if p%2==1 else -5), py)
        wire(px, py, px - (5 if p%2==1 else -5), py)
    # Pins 5-10: GND
    for p in [5,6,7,8,9,10]:
        row = (p-1)//2; x_off = -5.08 if p%2==1 else 5.08
        py = 280 - (24.13 - row*2.54)
        px = 50 + x_off
        pwr("GND", px - (5 if p%2==1 else -5), py)
        wire(px, py, px - (5 if p%2==1 else -5), py)
    # Pins 11-12: +5V
    for p in [11,12]:
        row = (p-1)//2; x_off = -5.08 if p%2==1 else 5.08
        py = 280 - (24.13 - row*2.54)
        px = 50 + x_off
        pwr("+5V", px - (5 if p%2==1 else -5), py)
        wire(px, py, px - (5 if p%2==1 else -5), py)
    # Pins 13-14: +3V3
    for p in [13,14]:
        row = (p-1)//2; x_off = -5.08 if p%2==1 else 5.08
        py = 280 - (24.13 - row*2.54)
        px = 50 + x_off
        pwr("+3V3", px - (5 if p%2==1 else -5), py)
        wire(px, py, px - (5 if p%2==1 else -5), py)
    # Pins 25,26,40: GND
    for p in [25,26,40]:
        row = (p-1)//2; x_off = -5.08 if p%2==1 else 5.08
        py = 280 - (24.13 - row*2.54)
        px = 50 + x_off
        pwr("GND", px - (5 if p%2==1 else -5), py)
        wire(px, py, px - (5 if p%2==1 else -5), py)

    # J_STACK signal labels
    jstack_sigs = {
        15:"PASD_PUMP_PWM",
        21:"CID_LACT1_EN", 22:"CID_LACT1_PH",
        23:"CID_LACT2_EN", 24:"CID_LACT2_PH",
        27:"FAN1_PWM", 28:"FAN2_PWM",
        29:"SLD_PUMP1_PWM", 30:"SLD_PUMP1_DIR",
        31:"SLD_PUMP2_PWM", 32:"SLD_PUMP2_DIR",
        33:"SLD_SOL1_EN", 34:"SLD_SOL2_EN",
        35:"I2C1_SCL", 36:"I2C1_SDA",
        37:"MAIN_SERVO_PWM", 38:"BUZZER_PWM",
    }
    for p, sig in jstack_sigs.items():
        row = (p-1)//2; x_off = -5.08 if p%2==1 else 5.08
        py = 280 - (24.13 - row*2.54)
        px = 50 + x_off
        wx = px - 15 if p%2==1 else px + 15
        wire(px, py, wx, py)
        lbl(sig, wx, py)

# ── Main ─────────────────────────────────────────────────────────

def main():
    place_components()

    lib_symbols = build_lib_symbols()

    out = f'''(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "{PROJECT_UUID}")
  (paper "A2")
  (title_block
    (title "Epicura Driver PCB")
    (date "2026-02-17")
    (rev "2.0")
    (company "Epicura")
    (comment 1 "Power Electronics & Actuator Drivers")
    (comment 2 "160x90mm - Generated by gen_driver_sch.py")
  )
{lib_symbols}
{''.join(symbols_buf)}
{''.join(wires_buf)}
{''.join(labels_buf)}
  (sheet_instances
    (path "/" (page "1"))
  )
  (embedded_fonts no)
)
'''
    script_dir = Path(__file__).parent
    out_path = script_dir / "driver-board.kicad_sch"
    out_path.write_text(out)
    print(f"Written {len(out)} chars to {out_path}")
    # Verify
    refs = []
    for line in out.split('\n'):
        if '(property "Reference"' in line and '#PWR' not in line:
            r = line.split('"')[3]
            refs.append(r)
    print(f"{len(refs)} component references")
    # Check lib_id coverage
    import re
    lib_ids = set(re.findall(r'\(lib_id "([^"]+)"\)', out))
    lib_defs = set(re.findall(r'^\s+\(symbol "([^"]+)"', out, re.MULTILINE))
    missing = lib_ids - lib_defs
    if missing:
        print(f"WARNING: Missing lib_symbols for: {missing}")
    else:
        print("All lib_ids have matching lib_symbols ✓")

if __name__ == "__main__":
    main()
