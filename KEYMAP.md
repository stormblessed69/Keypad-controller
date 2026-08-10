````markdown
# KEYMAP — Numpad Home Assistant

## Dispositivo físico

```text
HS6209 2.4G Wireless Receiver
````

Linux:

```text
/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd
```

---

# Mapa físico

```text
┌────────┬────────┬────────┬────────┐
│ Num    │   /    │   *    │   -    │
│ Lock   │        │        │        │
├────────┼────────┼────────┼────────┤
│ 7      │ 8      │ 9      │   +    │
│ Home   │ ↑      │ PgUp   │        │
├────────┼────────┼────────┼────────┤
│ 4      │ 5      │ 6      │ Back   │
│ ←      │        │ →      │ Space  │
├────────┼────────┼────────┼────────┤
│ 1      │ 2      │ 3      │ Enter  │
│ End    │ ↓      │ PgDn   │   =    │
├─────────────────┼────────┼────────┤
│       0         │   .    │        │
│       Ins       │  Del   │        │
└─────────────────┴────────┴────────┘
```

---

# Teclas 1–6 — Luces

## Selección

| Tecla | Entidad                    | Función                |
| ----- | -------------------------- | ---------------------- |
| `1`   | `light.living_room_aurum`  | Seleccionar Aurum      |
| `2`   | `light.alacena`            | Seleccionar Alacena    |
| `3`   | Pendiente                  | Seleccionar futura luz |
| `4`   | `light.kitchen_cuprum`     | Seleccionar Cuprum     |
| `5`   | `light.living_room_espejo` | Seleccionar Espejo     |
| `6`   | Pendiente                  | Seleccionar futura luz |

---

## Pulsación simple

Una pulsación de `1`–`6` selecciona la luz.

Ejemplo:

```text
5
↓
selected_light = light.living_room_espejo
```

Una vez seleccionada una luz:

```text
+ → brillo +10%
- → brillo -10%
```

---

## Doble pulsación

Una doble pulsación de `1`–`6`:

```text
Luz ON/OFF
```

Cuando la luz está apagada, se utiliza el brillo predeterminado configurado actualmente:

```text
DEFAULT_BRIGHTNESS = 70
```

---

# `+` — Brillo / volumen contextual

La tecla `+` no tiene una única función fija.

Su comportamiento depende del dispositivo/modo seleccionado.

### Luz seleccionada

```text
+ → brillo +10%
```

### JBL seleccionado

```text
+ → volumen +
```

### TV/monitor en modo volumen

```text
+ → volumen +
```

### Todas las luces

Cuando se activa el modo global:

```text
+ → brillo de todas las luces +
```

---

# `-` — Brillo / volumen contextual

### Luz seleccionada

```text
- → brillo -10%
```

### JBL seleccionado

```text
- → volumen -
```

### TV/monitor en modo volumen

```text
- → volumen -
```

### Todas las luces

```text
- → brillo de todas las luces -
```

---

# `0` — Todas las luces

### Pulsación simple

```text
0
↓
Toggle general de todas las luces
```

### Doble pulsación

La doble pulsación de `0` debe activar el modo:

```text
CONTROL GLOBAL DE BRILLO
```

En ese estado:

```text
+ → todas las luces +10%
- → todas las luces -10%
```

Este comportamiento es una de las áreas que todavía requiere refinamiento.

---

# `.` — Temperatura / color

La tecla `.` modifica el tipo de iluminación de la luz seleccionada.

## Luces normales

```text
Blanco frío ↔ Blanco cálido
```

## Espejo

Entidad:

```text
light.living_room_espejo
```

Comportamiento:

```text
Blanco ↔ Naranja
```

## Alacena

Entidad:

```text
light.alacena
```

Comportamiento:

```text
Blanco ↔ Naranja
```

La diferencia existe porque Espejo y Alacena manejan el color de manera distinta a las otras luces.

---

# `/` — JBL

Dispositivo:

```text
JBL 300
```

Entidad:

```text
media_player.estudio
```

### Pulsación simple

Selecciona el JBL como dispositivo contextual.

Después:

```text
+ → volumen +
- → volumen -
```

### Doble pulsación

```text
/ / 
↓
button.estudio_bluetooth
```

Activa Bluetooth.

---

# `7` — Spotify anterior

Control mediante Spotcast.

```text
7 → pista anterior
```

---

# `8` — Play/Pause

Esta tecla tiene comportamiento diferente según el número de pulsaciones.

### Pulsación simple

Controla el reproductor nativo:

```text
media_player.estudio
```

Acción:

```text
Play/Pause
```

### Doble pulsación

Controla Spotify mediante Spotcast:

```text
Play/Pause
```

Esto permite diferenciar:

```text
8 simple
↓
JBL nativo
```

de:

```text
8 doble
↓
Spotify / Spotcast
```

---

# `9` — Spotify siguiente

Control mediante Spotcast.

```text
9 → siguiente pista
```

---

# `Backspace` — TV / Monitor

Dispositivo objetivo:

```text
TV / Monitor
```

### Pulsación simple

Función principal del dispositivo.

### Doble pulsación

Activa modo:

```text
CONTROL DE VOLUMEN
```

Entonces:

```text
+ → volumen +
- → volumen -
```

---

# `Enter` — Proyector

### Pulsación simple

```text
Enter → encender proyector
```

### Doble pulsación

```text
Enter Enter → OK
```

---

# `*` — Reservada

Actualmente:

```text
SIN FUNCIÓN DEFINITIVA
```

Reservada para:

* escenas
* automatizaciones
* funciones futuras

---

# `NumLock`

Ignorado por el controlador.

```text
KEY_NUMLOCK → ignore
```

---

# Sistema de pulsación doble

La detección utiliza:

```text
DOUBLE_PRESS_TIME
```

Actualmente:

```text
DOUBLE_PRESS_TIME = 0.4
```

Por lo tanto, dos pulsaciones de la misma tecla dentro de aproximadamente:

```text
400 ms
```

se interpretan como doble pulsación.

---

# Filosofía del layout

El objetivo es aprovechar el layout físico del numpad y utilizar:

```text
Pulsación simple
+
Doble pulsación
+
Estado seleccionado
+
Modo contextual
```

para obtener muchas funciones sin agregar teclas físicas.

El layout debe mantenerse estable una vez consolidado, porque el usuario está desarrollando memoria muscular para utilizar el numpad como controlador físico.

````

Guardá:

**Ctrl + O → Enter → Ctrl + X**

---

