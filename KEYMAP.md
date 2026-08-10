# KEYMAP.md

# HS6209 Numpad — Authoritative Keymap

This file defines the required behavior of every physical keypad key.

The physical keypad layout must not be changed.

---

## 1 — Living Room Aurum

Entity:

`light.living_room_aurum`

### Single press

Select Aurum as the active light/context.

### Double press

Toggle Aurum.

When turning it ON, use `DEFAULT_BRIGHTNESS`.

### `+` / `-`

When Aurum is selected:

- `+` = increase brightness
- `-` = decrease brightness

### `.`

Toggle Aurum between:

- cold white
- warm white

Use normal color-temperature handling.

---

## 2 — Alacena

Entity:

`light.alacena`

### Single press

Select Alacena as the active light/context.

### Double press

Toggle Alacena.

When turning it ON, use `DEFAULT_BRIGHTNESS`.

### `+` / `-`

When Alacena is selected:

- `+` = increase brightness
- `-` = decrease brightness

### `.`

Toggle between:

- WHITE
- ORANGE

IMPORTANT:

Alacena must NOT be treated as a normal cold-white/warm-white
color-temperature light.

Use RGB color handling.

---

## 3

Reserved / future.

Do not invent functionality.

---

## 4 — Kitchen Cuprum

Entity:

`light.kitchen_cuprum`

### Single press

Select Cuprum as the active light/context.

### Double press

Toggle Cuprum.

When turning it ON, use `DEFAULT_BRIGHTNESS`.

### `+` / `-`

When Cuprum is selected:

- `+` = increase brightness
- `-` = decrease brightness

### `.`

Toggle Cuprum between:

- cold white
- warm white

Use normal color-temperature handling.

---

## 5 — Living Room Espejo

Entity:

`light.living_room_espejo`

### Single press

Select Espejo as the active light/context.

### Double press

Toggle Espejo.

When turning it ON, use `DEFAULT_BRIGHTNESS`.

### `+` / `-`

When Espejo is selected:

- `+` = increase brightness
- `-` = decrease brightness

### `.`

Toggle between:

- WHITE
- ORANGE

IMPORTANT:

Espejo must NOT be treated as a normal cold-white/warm-white
color-temperature light.

Use RGB color handling.

---

## 6

Reserved / future.

Do not invent functionality.

---

# MULTIMEDIA

## 7 — Spotcast Previous

Spotcast action:

`previous_track`

Use the authoritative Spotcast entity from `ENTITIES.md`.

Do not use a guessed media player.

---

## 8 — JBL Native Play/Pause

Entity:

`media_player.estudio`

### Single press

Use native media play/pause on:

`media_player.estudio`

This is NOT the Spotcast action.

---

## 88 — Spotify / Spotcast

Double press of `8`.

Start/resume Spotify playback on the `estudio` Spotcast device.

This is separate from native JBL play/pause.

Use the exact Spotcast entity/action documented in `ENTITIES.md`.

---

## 9 — Spotcast Next

Spotcast action:

`next_track`

Use the authoritative Spotcast entity from `ENTITIES.md`.

Do not use a guessed media player.

---

# JBL CONTEXT

## `/` — JBL Selection

Single press:

Select JBL/media context.

When JBL is selected:

- `+` = increase JBL volume
- `-` = decrease JBL volume

JBL entity:

`media_player.estudio`

---

## `//` — JBL Bluetooth

Double press of `/`.

Press:

`button.estudio_bluetooth`

---

# GLOBAL LIGHT CONTEXT

## 0

Preserve the existing global-light behavior unless it directly conflicts
with the requirements in this file.

Do not invent a new behavior.

If the current implementation and documentation disagree about `0`,
report the discrepancy before changing it.

---

## GLOBAL BRIGHTNESS

If the existing project exposes a global-light brightness context,
`+` and `-` must control all relevant lights while that context is active.

Do not remove an existing working global-light feature.

---

# COLOR KEY

## `.`

Controls the currently selected light.

### Aurum / Cuprum

Use normal color-temperature handling:

`cold white <-> warm white`

### Alacena / Espejo

Use RGB handling:

`white <-> orange`

Do NOT send `color_temp` to Alacena or Espejo for this function.

---

# INFRARED

## Enter — Projector

Broadlink remote:

`remote.control_universal`

Broadlink device:

`proyector`

### Single press

Send:

`power`

### Double press

Send:

`ok`

---

## Backspace — TV / Monitor

Broadlink remote:

`remote.control_universal`

Broadlink device:

`televisor_monitor`

### Single press

Send:

`power`

### Double press

Enter TV volume context.

While TV volume context is active:

- `+` = `volume_up`
- `-` = `volume_down`

---

# RESERVED KEYS

## 3

Reserved.

## 6

Reserved.

## *

Reserved.

Do not assign functionality without explicit instruction.

## NumLock

Ignored.

---

# INPUT RULES

Double press uses the existing:

`DOUBLE_PRESS_TIME`

Do not increase the double-press delay unnecessarily.

The event listener must remain responsive while waiting to determine whether
a second press occurred.

Held/repeated keypad events must not flood Home Assistant.

---

# CONTEXT PRIORITY

`+` and `-` are contextual.

Priority must be deterministic.

Possible contexts include:

1. TV volume
2. JBL volume
3. selected-light brightness
4. global-light brightness

Do not invent additional contexts.

If the existing project already has an explicit context-state mechanism,
reuse it.

---

# IMPORTANT

This file describes DESIRED FUNCTIONAL BEHAVIOR.

The fact that a function is listed here does not mean the current code already
implements it.

If code differs from this file, report the difference and implement the
minimum necessary fix.
