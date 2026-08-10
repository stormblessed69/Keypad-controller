# HARDWARE_INTEGRATION.md

# Broadlink RM Mini 3 / RM3 Mini

The project uses a Broadlink RM3 Mini already configured in Home Assistant.

The Broadlink is used to transmit learned IR commands.

---

# HOME ASSISTANT ENTITIES

## Broadlink remote

`remote.control_universal`

This is the primary entity used for learned IR commands.

Use:

`remote.send_command`

with:

```yaml
target:
  entity_id: remote.control_universal
data:
  device: <device>
  command: <command>

Example:

action: remote.send_command
target:
  entity_id: remote.control_universal
data:
  device: proyector
  command: power
IR emitter

infrared.control_universal_ir_emitter

This belongs to the same IR system.

Do not substitute it for remote.control_universal when sending the learned
remote commands documented below.

IMPORTANT: CHROMECAST

remote.sala_de_estar

is NOT the Broadlink RM3 Mini.

It belongs to the Chromecast 4 in the living room.

Do NOT use it for the IR projector or TV/monitor controls.

PROJECTOR

Broadlink virtual device name:

proyector

The following commands have already been learned physically with the
Broadlink RM3 Mini and tested successfully in Home Assistant.

Available commands
power
menu
up
down
left
right
ok
back
home
volume_up
volume_down
focus_up
focus_down

Do not invent additional projector commands.

Keypad mapping
Enter single press
action: remote.send_command
target:
  entity_id: remote.control_universal
data:
  device: proyector
  command: power
Enter double press
action: remote.send_command
target:
  entity_id: remote.control_universal
data:
  device: proyector
  command: ok
PROJECTOR NOTES

focus_up and focus_down control projector focus.

They are NOT color controls.

The physical projector remote contains a microphone-related button that was
initially mistaken for mute.

There is NO valid mute command in the current projector specification.

Do not implement mute.

TV / MONITOR

Broadlink virtual device name:

televisor_monitor

The following commands have already been learned physically and tested:

power
volume_up
volume_down

Do not invent additional commands.

Keypad mapping
Backspace single press
action: remote.send_command
target:
  entity_id: remote.control_universal
data:
  device: televisor_monitor
  command: power
Backspace double press

Does not send IR.

It enters the TV volume context.

TV volume context

+:

action: remote.send_command
target:
  entity_id: remote.control_universal
data:
  device: televisor_monitor
  command: volume_up

-:

action: remote.send_command
target:
  entity_id: remote.control_universal
data:
  device: televisor_monitor
  command: volume_down
IR LEARNING

IR learning was performed through Home Assistant using:

action: remote.learn_command
target:
  entity_id: remote.control_universal
data:
  device: <device>
  command: <command>
  command_type: ir

The learned commands are already stored in Home Assistant.

The Python keypad controller does NOT need to learn IR commands.

It only needs to call remote.send_command.

AIR CONDITIONER — DO NOT IMPLEMENT

The air conditioner is a Hyundai split AC.

Its IR behavior is different from a normal remote.

It appears to transmit the complete device state rather than independent
stateless button commands.

Observed behavior:

When the remote loses power and is powered again, transmitting can restore
a state resembling:

mode: COOL
temperature: 23°C
fan: AUTO

The currently learned AC commands are unreliable/mislabeled.

During learning, the physical buttons were shifted because some buttons were
not recognized correctly.

Therefore:

DO NOT use the current AC commands in the keypad controller.

DO NOT create a climate entity.

DO NOT create new AC IR commands.

DO NOT attempt to "fix" the AC as part of normal keypad development.

AC investigation is a separate future task.

BROADLINK RULES
Use remote.control_universal.
Use remote.send_command.
Use only documented device names.
Use only documented learned commands.
Do not invent IR commands.
Do not use remote.sala_de_estar.
Do not implement AC.
Do not re-learn commands from the Python controller.
Keep Broadlink-specific data separate from keypad event logic.
KNOWN-GOOD DEVICE NAMES
proyector
televisor_monitor

These names must remain unchanged.

KNOWN-GOOD REMOTE COMMANDS
proyector
power
menu
up
down
left
right
ok
back
home
volume_up
volume_down
focus_up
focus_down
televisor_monitor
power
volume_up
volume_down

Anything not listed here must be considered unknown until explicitly
confirmed.


---
