# AI_CONTEXT.md

## Purpose

This repository controls an HS6209 USB numpad through `evdev` and the
Home Assistant REST API.

The controller is an existing working project. Extend it incrementally.

## AI DEVELOPMENT RULES

1. Preserve the existing `evdev + REST` architecture.
2. Modify the minimum necessary files.
3. Do not rewrite the controller unless strictly necessary.
4. Do not perform unrelated refactors.
5. Preserve working functionality.
6. Do not change the physical keypad layout.
7. Do not invent Home Assistant entities.
8. Do not invent IR commands.
9. Do not invent Spotcast entities.
10. Do not modify the structure or secrets in `config.py`.
11. Never implement the air conditioner unless explicitly requested.
12. Preserve existing timeout, rate-limit and error-handling behavior.
13. Single/double press handling must not block the `evdev` event loop.
14. Home Assistant failures must not terminate the keypad process.
15. Prefer existing helper functions over new duplicate implementations.
16. Before changing code, inspect the relevant existing implementation.
17. After changes, validate Python syntax and inspect `git diff`.
18. If requirements conflict with existing code or documentation, report
    the conflict instead of guessing.
19. Do not change unrelated behavior merely to make the code "cleaner".
20. Keep hardware-specific facts in documentation rather than hard-coding
    assumptions that are not documented.

## SOURCE OF TRUTH

Use these files in this order:

1. `AI_CONTEXT.md` — development rules
2. `KEYMAP.md` — authoritative keypad behavior
3. `ENTITIES.md` — authoritative Home Assistant entities
4. `HARDWARE_INTEGRATION.md` — Broadlink/IR hardware facts
5. `PROJECT_CONTEXT.md` — architecture/background
6. Python source code — current implementation

If source code conflicts with the documented desired behavior, report it
as `FIX` or `CONFLICT`; do not silently redefine the specification.

## IMPLEMENTATION PHILOSOPHY

The goal is reliable behavior, not a rewrite.

Prefer:

- small changes
- reusable helpers
- explicit state
- deterministic key handling
- short Home Assistant requests
- clear separation between keypad input and Home Assistant actions

Avoid:

- unnecessary abstractions
- large rewrites
- blocking sleeps
- duplicated API code
- guessed entity IDs
- guessed service calls
- guessed IR behavior

## TESTING REQUIREMENT

Every implemented key must be testable against `KEYMAP.md`.

A successful Python syntax check is NOT sufficient.

The implementation must be checked for:

- single press
- double press
- contextual `+` / `-`
- repeated presses
- Home Assistant timeout
- Home Assistant unavailable
- context switching
- no selected device
- accidental key autorepeat

## CURRENT PROJECT SCOPE

Currently supported domains:

- lights
- JBL/media
- Spotcast
- Broadlink IR projector
- Broadlink IR TV/monitor

Explicitly postponed:

- Hyundai air conditioner IR integration

Do not implement postponed functionality without explicit instruction.
