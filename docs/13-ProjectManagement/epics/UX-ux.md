---
tags: [epicura, project-management, epic, ux, mobile, design]
created: 2026-02-17
aliases: [UX Epic, User Experience Epic]
---

> [!info] Review History
> | Date | Author | Change |
> |------|--------|--------|
> | 2026-02-17 | Manas Pradhan | Initial version — 7 stories for JSX mock screens |

# Epic: UX — User Experience Design

JSX mock screens (Vite + React) for rapid prototyping of mobile app flows. Covers phone+OTP auth, tab navigation (Recipe, Favourite, Session, Profile), and all primary screens. Visual style: iOS Liquid Glass aesthetic as default, Material 3 notes in comments. Mocks will be converted to native SwiftUI and Kotlin/Compose.

## Story Summary

| Module | Stories | Points | Sprints |
|--------|:-------:|:------:|---------|
| AUTH — Phone+OTP Auth | 1 | 3 | — |
| TAB — Tab Navigation | 1 | 2 | — |
| RCP — Recipe Browsing | 1 | 3 | — |
| FAV — Favourites | 1 | 2 | — |
| SES — Session / History | 1 | 3 | — |
| PRO — Profile | 1 | 3 | — |
| LIVE — Mini Progress | 1 | 2 | — |
| **Total** | **7** | **~18** | |

---

## UX-AUTH.01: Phone+OTP login/register screens (JSX mock)

- **Priority:** P0
- **Points:** 3
- **Blocked by:** None
- **Blocks:** [[UX-ux#UX-TAB.01|UX-TAB.01]]

**Acceptance Criteria:**
- [ ] Phone number entry screen with country code picker (+91 default)
- [ ] 6-digit OTP input screen with auto-focus advance
- [ ] Auto-verify simulation (fills OTP after 3s delay)
- [ ] Register-on-first-login: no separate registration flow
- [ ] Error states: invalid phone, wrong OTP, expired OTP
- [ ] Liquid Glass frosted card styling

**Tasks:**
- [ ] `UX-AUTH.01a` — Implement LoginScreen.jsx with phone input and "Send OTP" button
- [ ] `UX-AUTH.01b` — Implement OTPScreen.jsx with 6-digit input and auto-verify
- [ ] `UX-AUTH.01c` — Implement OTPInput.jsx reusable component

---

## UX-TAB.01: Tab bar layout (JSX mock)

- **Priority:** P0
- **Points:** 2
- **Blocked by:** [[UX-ux#UX-AUTH.01|UX-AUTH.01]]
- **Blocks:** All screen stories

**Acceptance Criteria:**
- [ ] Bottom tab bar with 4 tabs: Recipe, Favourite, Session, Profile
- [ ] Icons and labels for each tab
- [ ] Active tab highlight with Warm Orange accent
- [ ] Tab switching renders correct screen
- [ ] Frosted glass tab bar background

**Tasks:**
- [ ] `UX-TAB.01a` — Implement TabBar.jsx with 4 tabs and active state
- [ ] `UX-TAB.01b` — Implement App.jsx tab navigation wrapper

---

## UX-RCP.01: Recipe browsing screen (JSX mock)

- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[UX-ux#UX-TAB.01|UX-TAB.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] List layout of recipe cards (horizontal card: food bowl image on left, details on right)
- [ ] Each card: food image in bowl (left), name, time, difficulty badge, nutrition per serving (Protein g, Carbs g, Fats g, Calories kcal)
- [ ] Search bar with placeholder text
- [ ] Tag filter chips (horizontally scrollable): All Recipes, Vegan, Healthy, Vegetarian, Protein Rich, Stir Fry, Gluten Free, Quick Recipe
- [ ] Cuisine filter chips (second row): Indian, Italian, American, Chinese, Mexican, Korean, Thai, Asian, Global
- [ ] Pull-down refresh animation (simulated)

**Tasks:**
- [ ] `UX-RCP.01a` — Implement RecipeScreen.jsx with list layout, tag filters, and cuisine filters
- [ ] `UX-RCP.01b` — Implement RecipeCard.jsx with horizontal layout (bowl image left, details + nutrition right)

---

## UX-FAV.01: Favourites screen (JSX mock)

- **Priority:** P1
- **Points:** 2
- **Blocked by:** [[UX-ux#UX-TAB.01|UX-TAB.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] List of favourited recipes (subset of mock data)
- [ ] Heart icon toggle to unfavourite
- [ ] Empty state: "No favourites yet" with illustration
- [ ] Tap card navigates to recipe detail (simulated)

**Tasks:**
- [ ] `UX-FAV.01a` — Implement FavouriteScreen.jsx with favourited recipe list

---

## UX-SES.01: Session screen (JSX mock)

- **Priority:** P0
- **Points:** 3
- **Blocked by:** [[UX-ux#UX-TAB.01|UX-TAB.01]], [[UX-ux#UX-LIVE.01|UX-LIVE.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Cooking history list: recipe name, date, duration, status badge
- [ ] Mini live progress card at top when cooking is active
- [ ] Empty state: "No cooking sessions yet"
- [ ] Status badges: completed (green), failed (red), in-progress (orange)

**Tasks:**
- [ ] `UX-SES.01a` — Implement SessionScreen.jsx with history list and mini progress

---

## UX-PRO.01: Profile screen (JSX mock)

- **Priority:** P1
- **Points:** 3
- **Blocked by:** [[UX-ux#UX-TAB.01|UX-TAB.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] User info section: avatar, name, phone number
- [ ] Preferences: spice level, default servings, dietary tags
- [ ] Device management: paired device card with status
- [ ] Settings: notifications toggle, language, logout button

**Tasks:**
- [ ] `UX-PRO.01a` — Implement ProfileScreen.jsx with user info, preferences, and settings

---

## UX-LIVE.01: Mini cooking progress view (JSX mock)

- **Priority:** P0
- **Points:** 2
- **Blocked by:** None
- **Blocks:** [[UX-ux#UX-SES.01|UX-SES.01]]

**Acceptance Criteria:**
- [ ] Compact card showing: recipe name, current stage, temperature, time remaining
- [ ] Animated progress bar
- [ ] Pulsing dot indicator for "live" status
- [ ] Fits at top of Session screen

**Tasks:**
- [ ] `UX-LIVE.01a` — Implement MiniProgress.jsx compact card component

---

## UX-GLANCE.01: Live Activity / Glance Widget mock (JSX)

- **Priority:** P1
- **Points:** 3
- **Blocked by:** [[UX-ux#UX-LIVE.01|UX-LIVE.01]]
- **Blocks:** None

**Acceptance Criteria:**
- [ ] Mock of iOS Lock Screen Live Activity: recipe name, stage, temp gauge, progress bar, time remaining
- [ ] Mock of Dynamic Island compact view (pill shape): recipe name + timer
- [ ] Mock of Dynamic Island expanded view: full cooking info
- [ ] Mock of Android Glance widget small (2x1) and medium (3x2) variants
- [ ] Pulsing live indicator on all variants
- [ ] Completed/failed end states shown
- [ ] Liquid Glass styling for iOS; Material 3 styling for Android variant

**Tasks:**
- [ ] `UX-GLANCE.01a` — Implement iOS Live Activity mock (Lock Screen + Dynamic Island views)
- [ ] `UX-GLANCE.01b` — Implement Android Glance widget mock (small + medium sizes)

---

## Dependencies

### What UX blocks

| UX Story | Blocks | Reason |
|----------|--------|--------|
| UX screens | IOS, AND native implementation | Mocks define screen layout and flow |

### What blocks UX

None — UX is independent; can be built in parallel with other epics.

---

## References

- [[__Workspaces/Epicura/docs/12-MobileApps/01-Mobile-Architecture|Mobile Architecture]]
- [[__Workspaces/Epicura/docs/04-UserInterface/03-UI-UX-Design|UI/UX Design]]
- [[__Workspaces/Epicura/docs/13-ProjectManagement/epics/__init|Epic Index]]
