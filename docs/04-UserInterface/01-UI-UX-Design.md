---
created: 2026-02-15
modified: 2026-02-15
version: 1.0
status: Draft
---

# UI/UX Design

## Display Overview

### Primary Display
- **Type:** 10" capacitive touchscreen (IPS TFT)
- **Resolution:** 1280x800 (recommended) or 800x480 (budget option)
- **Interface:** MIPI DSI from Raspberry Pi CM5
- **Touch:** 10-point capacitive multi-touch
- **Mounting:** Integrated into Epicura enclosure top panel

### Secondary Display
- **Native companion mobile apps** (iOS: SwiftUI, Android: Jetpack Compose)
- **Communication:** WiFi direct to Epicura device
- **Features:** Remote recipe browsing, live camera feed, cooking notifications

---

## Screen Layouts

### 1. Home Screen

```
┌──────────────────────────────────────────────┐
│ ☰  Epicura              12:30 PM    ⚙ WiFi   │
├──────────────────────────────────────────────┤
│                                              │
│   Good Afternoon, Manas!                     │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   Dal    │  │  Paneer  │  │   Rice   │    │
│  │  Tadka   │  │  Butter  │  │  Pulao   │    │
│  │  🕐 35m  │  │  🕐 45m   │  │  🕐 40m  │    │
│  │  ★★★★☆   │  │  ★★★★★   │  │  ★★★☆☆   │    │
│  └──────────┘  └──────────┘  └──────────┘    │
│                                              │
│  ┌──────────┐                                │
│  │  Aloo    │                                 │
│  │  Gobi    │   Recently Cooked:              │
│  │  🕐 30m  │   Dal Tadka - Yesterday        │
│  │  ★★★★☆   │   Paneer Butter - 2 days ago    │
│  └──────────┘                                │
│                                              │
│        [    Browse All Recipes    ]          │
│                                              │
├──────────────────────────────────────────────┤
│  Device Ready  │  Pot: Not Detected  │ 25°C  │
└──────────────────────────────────────────────┘
```

**Elements:**
- Status bar: hamburger menu, brand name, time, settings gear, WiFi indicator
- Greeting with user name (from preferences)
- 3-4 quick recipe cards (favorites or suggestions)
- Recent cooking history
- "Browse All Recipes" prominent button
- Bottom status bar: device state, pot detection, ambient temperature

---

### 2. Recipe Selection

```
┌──────────────────────────────────────────────┐
│ ◄ Back         Browse Recipes        🔍      │
├──────────────────────────────────────────────┤
│                                              │
│ [All] [Vegan] [Healthy] [Vegetarian] [Pro..] │
│ [Indian] [Italian] [American] [Chinese] [..] │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │ ┌────────┐  Dal Tadka               │    │
│  │ │ (food  │  35 min · Easy ●○○       │    │
│  │ │  bowl) │  P:18g C:42g F:8g 320cal │    │
│  │ └────────┘                           │    │
│  └──────────────────────────────────────┘    │
│  ┌──────────────────────────────────────┐    │
│  │ ┌────────┐  Dal Makhni              │    │
│  │ │ (food  │  40 min · Med ●●○        │    │
│  │ │  bowl) │  P:14g C:38g F:12g 350cal│    │
│  │ └────────┘                           │    │
│  └──────────────────────────────────────┘    │
│  ┌──────────────────────────────────────┐    │
│  │ ┌────────┐  Sambar                  │    │
│  │ │ (food  │  45 min · Med ●●○        │    │
│  │ │  bowl) │  P:12g C:48g F:6g 290cal │    │
│  │ └────────┘                           │    │
│  └──────────────────────────────────────┘    │
│                                              │
│         [ Load More... ]                     │
└──────────────────────────────────────────────┘
```

**Elements:**
- **Filter chips (top row):** All Recipes, Vegan, Healthy, Vegetarian, Protein Rich, Stir Fry, Gluten Free, Quick Recipe (horizontally scrollable)
- **Cuisine tabs (second row):** Indian, Italian, American, Chinese, Mexican, Korean, Thai, Asian, Global
- Search bar with text input
- Recipe cards in list layout:
  - Food image in bowl on the **left side** of the card
  - Recipe name, time, difficulty on the right
  - **Nutrition per serving** displayed below: Protein (g), Carbs (g), Fats (g), Calories (kcal)
- Difficulty indicator: Easy/Medium/Hard with dots
- Scrollable list, "Load More" or infinite scroll

---

### 3. Recipe Detail

```
┌──────────────────────────────────────────────┐
│ ◄ Back          Dal Tadka            ♡       │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │                                      │    │
│  │        [ Recipe Photo ]              │    │
│  │                                      │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  🕐 35 min  │  Serves 4  │  Easy ●○○         │
│                                              │
│  Spice Level: [──────●────────] Medium       │
│                                              │
│  ⚠ Allergens: Contains mustard seeds         │
│                                              │
│  Ingredients:                                │
│  ├─ SLD-OIL:  Oil (30 g)                     │
│  ├─ ASD-1:    Turmeric powder (3 g)          │
│  ├─ ASD-2:    Chili powder (5 g)             │
│  ├─ ASD-3:    Salt + Garam masala (5 g)      │
│  ├─ CID-1:    Onions + Tomatoes (150 g)      │
│  ├─ CID-2:    Toor dal (200 g)               │
│  └─ SLD-WATER: Water (400 g)                 │
│                                              │
│  Pre-loaded in pot: Cooked toor dal (400 g)  │
│                                              │
│       [     Start Cooking     ]              │
│                                              │
└──────────────────────────────────────────────┘
```

**Elements:**
- Recipe photo (from local storage or placeholder)
- Time estimate, servings, difficulty badge
- Spice level slider (adjustable, saved to preferences)
- Allergen warnings (highlighted, configurable in settings)
- Ingredient list mapped to subsystem IDs (ASD/CID/SLD)
- Any pre-loading instructions (items placed directly in pot)
- Prominent "Start Cooking" button

---

### 4. Ingredient Loading

```
┌──────────────────────────────────────────────┐
│          Load Ingredients: Dal Tadka         │
├──────────────────────────────────────────────┤
│                                              │
│   Step 3 of 7                                │
│   [████████████░░░░░░░░░░░░░] 43%            │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │   ASD        CID        SLD          │    │
│  │  ┌───┐┌───┐┌───┐ ┌───┐┌───┐ ┌───┐┌───┐    │
│  │  │A1 ││A2 ││A3 │ │C1 ││███│ │OIL││H2O│    │
│  │  │ ✓ ││ ✓ ││   │ │ ✓ ││►  │ │ ✓ ││   │    │
│  │  └───┘└───┘└───┘ └───┘└───┘ └───┘└───┘    │
│  │   Subsystem Diagram (top view)      │     │
│  └──────────────────────────────────────┘    │
│                                              │
│   ► Load CID-2:                              │
│     Toor dal — 200 g                         │
│                                              │
│   Weight sensor: [████████████░░] 142 g      │
│   Target: 150 g (± 10 g)                     │
│                                              │
│   [ ◄ Previous ]        [ Next ► ]           │
│                                              │
├──────────────────────────────────────────────┤
│   [ Cancel ]     [ All Loaded — Start ]      │
└──────────────────────────────────────────────┘
```

**Elements:**
- Step counter and progress bar
- Top-view subsystem diagram with current slot highlighted
- Checkmarks on loaded subsystem slots
- Ingredient name, amount, and subsystem ID (ASD-1, CID-2, SLD-OIL, etc.)
- Live weight sensor reading with progress bar toward target (ASD/SLD)
- Acceptable range indication (e.g., ±10 g)
- Previous/Next navigation
- "All Loaded - Start" button (enabled when all subsystems confirmed)

---

### 5. Cooking Progress

```
┌──────────────────────────────────────────────┐
│  Cooking: Dal Tadka          Stage 3 of 6    │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │                                      │    │
│  │                                      │    │
│  │         [ Live Camera Feed ]         │    │
│  │           640 x 480                  │    │
│  │                                      │    │
│  │                                      │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  Current Stage: Saute Onions                 │
│  [████████████████░░░░░░░░░░░] 62%           │
│                                              │
│  ┌────────────┐  ┌────────────┐              │
│  │ Temp       │  │ Time Left  │              │
│  │ 148°C      │  │ 3:12       │              │
│  │ Target:150 │  │ of 5:00    │              │
│  └────────────┘  └────────────┘              │
│                                              │
│  Stir: ● Active (Continuous, 60 RPM)         │
│  CV:   ● Monitoring (golden_brown: 0.42)     │
│                                              │
│  [ ⏸ Pause ]              [ ⏹ Emergency Stop ]│
│                                              │
└──────────────────────────────────────────────┘
```

**Elements:**
- Stage counter in header
- Live camera feed (large, central area)
- Current stage name and overall progress bar
- Temperature gauge (current vs target)
- Time remaining countdown
- Stir status indicator (pattern, speed)
- CV monitoring status (what it is looking for, current confidence)
- Pause button (holds current state, maintains safe temperature)
- Emergency Stop button (prominent, red, always accessible)

---

### 6. Cooking Complete

```
┌──────────────────────────────────────────────┐
│              Cooking Complete!               │
├──────────────────────────────────────────────┤
│                                              │
│              ✓                               │
│                                              │
│         Dal Tadka is Ready!                  │
│                                              │
│  ┌──────────────────────────────────────┐    │
│  │  Summary:                            │    │
│  │                                      │    │
│  │  Total Time:     34 min 22 sec       │    │
│  │  Stages:         6 of 6 completed    │    │
│  │  Peak Temp:      182°C               │    │
│  │  CV Transitions: 5 auto, 1 timer     │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  Rate This Cook:                             │
│  [ ★ ] [ ★ ] [ ★ ] [ ★ ] [ ☆ ]               │
│                                              │
│  Notes: [________________________]           │
│                                              │
│  [ Cook Again ]        [ Home ]              │
│                                              │
└──────────────────────────────────────────────┘
```

**Elements:**
- Success checkmark and message
- Cooking summary: total time, stages completed, peak temperature, CV vs timer transitions
- Star rating (1-5, saved to cooking_logs)
- Optional notes text field
- "Cook Again" button (same recipe) and "Home" button

---

### 7. Settings

```
┌──────────────────────────────────────────────┐
│ ◄ Back              Settings                 │
├──────────────────────────────────────────────┤
│                                              │
│  Language              [ English       ▼ ]   │
│                                              │
│  WiFi Network          [ EpicuraHome   ▼ ]   │
│                                              │
│  ──── Cooking Preferences ────               │
│  Default Spice Level   [────●──────] Med     │
│  Default Servings      [ 4          ▼ ]      │
│                                              │
│  ──── Allergen Profile ────                  │
│  [ ] Nuts     [ ] Dairy    [✓] Mustard       │
│  [ ] Gluten   [ ] Soy      [ ] Sesame        │
│                                              │
│  ──── Display ────                           │
│  Brightness            [──────────●] 80%     │
│  Theme                 [ Light     ▼ ]       │
│                                              │
│  ──── System ────                            │
│  Firmware Version      CM5: 1.0.0            │
│                        STM32: 1.0.0          │
│  [ Check for Updates ]                       │
│  [ Factory Reset ]                           │
│                                              │
│  ──── About ────                             │
│  Device ID: EPIC-001                         │
│  Serial: SN2026020001                        │
│                                              │
└──────────────────────────────────────────────┘
```

**Elements:**
- Language dropdown (see Multi-Language Support below)
- WiFi network selection and connection status
- Cooking preferences: default spice level, default servings
- Allergen profile checkboxes (flagged recipes show warnings)
- Display: brightness slider, light/dark theme
- System: firmware versions for both processors, update check, factory reset
- Device identification

---

## Multi-Language Support

### Supported Languages

| Language | Script | Locale Code | Priority |
|----------|--------|-------------|----------|
| English | Latin | en_IN | Primary |
| Hindi | Devanagari (हिन्दी) | hi_IN | Primary |
| Tamil | Tamil (தமிழ்) | ta_IN | Secondary |
| Telugu | Telugu (తెలుగు) | te_IN | Secondary |
| Kannada | Kannada (ಕನ್ನಡ) | kn_IN | Secondary |
| Malayalam | Malayalam (മലയാളം) | ml_IN | Secondary |
| Bengali | Bengali (বাংলা) | bn_IN | Secondary |
| Marathi | Devanagari (मराठी) | mr_IN | Secondary |

### Implementation

**Python i18n Workflow:**
1. Mark all UI strings with gettext `_()` function
2. Run `xgettext` to extract strings into `.po` translation files
3. Translate `.po` files using Poedit or Python Babel tools
4. Compile `.po` to binary `.mo` files with `msgfmt`
5. Load appropriate `.mo` at runtime based on user preference

```python
# In Python files
import gettext
_ = gettext.gettext

from kivy.uix.label import Label
from kivy.uix.button import Button

label = Label(text=_("Cooking in Progress..."))
greeting = Label(text=_("Good Afternoon!"))
start_btn = Button(text=_("Start Cooking"))
temp_label = Label(text=_("Temperature: %d°C") % current_temp)
```

**Font Requirements:**
- Noto Sans family covers all target scripts
- Embedded in Kivy resources
- Fallback font chain for missing glyphs
- Estimated font storage: ~15-20 MB for all scripts

---

## UX Goals

### Five Core Principles

1. **Easy Recipe Selection (< 3 taps to start)**
   - Home screen shows favorites and recent recipes
   - One tap on recipe card → recipe detail
   - One tap "Start Cooking" → ingredient loading
   - Maximum 3 taps from power-on to cooking

2. **Clear Ingredient Loading Instructions**
   - Visual subsystem diagram with highlighting
   - Live weight feedback from load cells
   - Step-by-step guided flow
   - Confirmation before proceeding

3. **Transparent Cooking Progress**
   - Live camera feed always visible during cooking
   - Real-time temperature, time, and stir status
   - CV confidence indicator (user can see what the system "sees")
   - Stage-by-stage progress with estimated completion

4. **Safety First**
   - Emergency Stop button visible on every cooking screen
   - Red color, large touch target, no confirmation dialog
   - Clear warning messages for high temperatures
   - Pot detection prevents cooking without pot

5. **Offline-Capable**
   - All UI assets stored locally
   - Full recipe library cached on device
   - No internet required for any cooking operation
   - Cloud features (sync, OTA) are optional enhancements

---

## Accessibility

### Touch Targets
- Minimum size: 48 x 48 pixels for all interactive elements
- Emergency Stop: 96 x 48 pixels minimum (oversized for safety)
- Spacing between targets: minimum 8 pixels

### Visual Accessibility
- **High contrast mode:** Dark backgrounds with bright text (toggle in settings)
- **Adjustable font size:** Small / Medium / Large / Extra-Large
- **Color-blind safe palette:** Avoid red/green only indicators; use shape + color
- **Status indicators:** Use both color and icon (e.g., green checkmark, red X)

### Audio Feedback
- **Stage transitions:** Distinct beep pattern when moving to next cooking stage
- **Completion:** Musical chime when cooking is done
- **Warnings:** Rapid beeping for temperature warnings
- **Emergency:** Continuous alarm tone for E-stop or critical errors
- **Touch:** Subtle click sound on button press (configurable)

### Text & Typography
- Primary font: Noto Sans (covers all Indian scripts)
- Minimum body text: 16px (on 10" 1280x800 display)
- Headings: 24-32px
- Temperature/time numbers: 36-48px (large, at-a-glance readable)

---

## Kivy Implementation Notes

### Application Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      main.kv                            │
│  ┌─────────────────┐  ┌──────────────────────────────┐  │
│  │   HeaderBar     │  │        StatusBar             │  │
│  └─────────────────┘  └──────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐   │
│  │              StackView (Navigation)              │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │ HomePage │ RecipePage │ CookingPage │ ...  │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │          CameraView (GStreamer → VideoOutput)    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Key Kivy Screens and Widgets

| Component | File | Purpose |
|-----------|------|---------|
| HomePage | `home_screen.py` | Greeting, quick recipes, recent history |
| RecipeBrowser | `recipe_browser_screen.py` | Category filters, grid view, search |
| RecipeDetail | `recipe_detail_screen.py` | Ingredients, spice slider, allergens |
| IngredientLoader | `ingredient_loader_screen.py` | Step-by-step subsystem loading (ASD/CID/SLD) |
| CookingProgress | `cooking_progress_screen.py` | Camera feed, gauges, progress, E-stop |
| CookingComplete | `cooking_complete_screen.py` | Summary, rating, notes |
| SettingsPage | `settings_screen.py` | Language, WiFi, preferences, firmware |
| CameraWidget | `camera_widget.py` | Kivy Camera widget with CSI-2 feed |
| TempGauge | `temp_gauge.py` | Circular temperature gauge (custom widget) |
| RecipeCard | `recipe_card.py` | Reusable card with photo, name, time |

### Camera Widget

```python
# camera_widget.py
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout

class CameraWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Kivy Camera widget with CSI-2 device
        self.camera = Camera(
            resolution=(1280, 800),
            play=True,
            index=0  # CSI-2 camera device
        )
        self.camera.size_hint = (1, 1)
        self.add_widget(self.camera)

    def capture_frame(self):
        """Capture current frame for CV inference"""
        return self.camera.texture
```

**GStreamer Pipeline (for CSI-2 camera on CM5):**
```
Kivy Camera widget (index=0, resolution=(640, 480), play=True) with CSI-2 V4L2 backend
```

### Styling

**Design Language:** Material Design inspired, warm food-friendly palette

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Warm Orange | #E65100 |
| Secondary | Deep Green | #2E7D32 |
| Background | Cream White | #FFF8E1 |
| Surface | White | #FFFFFF |
| Text Primary | Dark Brown | #3E2723 |
| Text Secondary | Medium Brown | #6D4C41 |
| Emergency Stop | Bright Red | #D50000 |
| Success | Green | #43A047 |
| Warning | Amber | #FFB300 |

```python
# theme.py - App-wide styling constants
class Theme:
    PRIMARY = "#E65100"
    SECONDARY = "#2E7D32"
    BACKGROUND = "#FFF8E1"
    SURFACE = "#FFFFFF"
    TEXT_PRIMARY = "#3E2723"
    TEXT_SECONDARY = "#6D4C41"
    EMERGENCY = "#D50000"
    SUCCESS = "#43A047"
    WARNING = "#FFB300"

    FONT_SIZE_BODY = 16
    FONT_SIZE_HEADING = 24
    FONT_SIZE_DISPLAY = 36
    TOUCH_TARGET_MIN = 48
```

---

## Companion App Design

### Native Mobile Architecture

Epicura uses native mobile development: **SwiftUI** (iOS) and **Jetpack Compose** (Android), following the MVVM pattern. For complete architecture details, project structure, and platform-specific implementation guides, see:

- [[../12-MobileApps/01-Mobile-Architecture|Mobile Architecture]] - MVVM layers, networking, BLE manager, design system
- [[../12-MobileApps/02-iOS-App|iOS App]] - Swift/SwiftUI project structure, Core Bluetooth, APNs
- [[../12-MobileApps/03-Android-App|Android App]] - Kotlin/Compose project structure, CompanionDeviceManager, FCM

### Key Screens

1. **Recipe Browse** - List layout with food bowl image on left, tag filters (Vegan/Healthy/Vegetarian/Protein Rich/Stir Fry/Gluten Free/Quick), cuisine filters (Indian/Italian/American/Chinese/Mexican/Korean/Thai/Asian/Global), nutrition per serving (Protein/Carbs/Fats/Calories)
2. **Recipe Detail** - Ingredients, spice customization, allergen flags, nutrition breakdown, remote start
3. **Live Cook View** - MJPEG camera stream, temperature gauge, stage progress, notifications
4. **History** - List of past cooks with date, rating, duration, recipe name
5. **Profile / Settings** - Food preferences, device pairing, allergen profile, notifications
6. **Food Preferences** (within Profile tab) — Dedicated section for dietary and taste customization:

```
┌──────────────────────────────────────────────┐
│ ◄ Back            Profile                    │
├──────────────────────────────────────────────┤
│                                              │
│  ──── Food Preferences ────                 │
│                                              │
│  Diet                                        │
│  [ Vegetarian | Vegan | Pescatarian | ●None ]│
│                                              │
│  Preferred Cuisines                          │
│  [●Indian] [●Italian] [●Thai] [Chinese]     │
│  [American] [●Mexican] [Korean] [Global]    │
│                                              │
│  Seasoning Levels                            │
│  Spice  [─────────●─────────] 3             │
│  Salt   [─────────●─────────] 3             │
│  Oil    [─────────●─────────] 3             │
│                                              │
│  Typical Servings     [ − ]  2  [ + ]       │
│                                              │
│  ──── Allergen Profile ────                 │
│  [ ] Nuts     [ ] Dairy    [✓] Mustard      │
│  [ ] Gluten   [ ] Soy      [ ] Sesame       │
│                                              │
│  ──── Device & Account ────                 │
│  Paired Device        EPIC-001 (Online)     │
│  Notifications        [  ON  ]              │
│  Theme                [ Light     ▼ ]       │
│                                              │
└──────────────────────────────────────────────┘
```

**Food Preferences Fields:**

| Control | Type | Options / Range | Default |
|---------|------|-----------------|---------|
| Diet | Single-select segmented | Vegetarian, Vegan, Pescatarian, No Restrictions | No Restrictions |
| Preferred Cuisines | Multi-select chip group | Indian, Italian, Thai, Chinese, American, Mexican, Korean, Global | Indian, Italian, Thai, Mexican |
| Spice Level | 5-point discrete slider | 1 (Mild) – 5 (Hot) | 3 |
| Salt Level | 5-point discrete slider | 1 (Low) – 5 (High) | 3 |
| Oil Level | 5-point discrete slider | 1 (Light) – 5 (Rich) | 3 |
| Typical Servings | Stepper (spinner) | 1 – 4 | 2 |
6. **Device Pairing** - BLE scan, WiFi provisioning, cloud account linking
7. **Device Status** - Firmware versions, connection status, sensor health

### Communication

| Channel | Protocol | Data |
|---------|----------|------|
| Recipe browsing | REST (HTTP GET) | JSON recipe list and details |
| Start cooking | REST (HTTP POST) | Recipe ID, customization params |
| Live camera | MJPEG over HTTP or WebSocket | Video frames at 10-15 fps |
| Cooking status | WebSocket | Real-time temp, stage, progress |
| Settings sync | REST (HTTP GET/PUT) | User preferences JSON |
| Push notifications | FCM (Android) / APNs (iOS) | Cooking complete, errors |
| Device pairing | BLE GATT services | WiFi provisioning, device identification |

### Offline Recipe Cache

- iOS: Recipes cached locally using SwiftData; images cached using Nuke
- Android: Recipes cached locally using Room; images cached using Coil
- Offline mode: browse and select recipes, queue for when device is reachable
- Last sync timestamp displayed in app

---

## Related Documentation

- [[../01-Overview/01-Project-Overview|Project Overview]]
- [[../03-Software/04-Controller-Software-Architecture|Controller & Software Architecture]]
- [[../03-Software/08-Tech-Stack|Tech Stack]]

#epicura #ui-ux #user-interface #touchscreen #mobile-app #kivy #swift #kotlin #native-mobile #accessibility #multi-language

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Manas Pradhan | Initial document creation |