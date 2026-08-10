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

## 2. Crear `ENTITIES.md`

Ahora:

```bash
nano ~/numpad-ha/ENTITIES.md
````

Pegá:

````markdown
# ENTITIES — Home Assistant

Listado de entidades relevantes para el proyecto Numpad Home Assistant.

---

# Luces

## Aurum

```text
light.living_room_aurum
````

Uso:

```text
Tecla 1
```

---

## Cuprum

```text
light.kitchen_cuprum
```

Uso:

```text
Tecla 4
```

---

## Espejo

```text
light.living_room_espejo
```

Uso:

```text
Tecla 5
```

Características especiales:

```text
Blanco ↔ Naranja
```

También existe:

```text
number.living_room_espejo_effect_speed
sensor.living_room_espejo_paired_remotes
select.living_room_espejo_remote_config
select.living_room_espejo_wiring
switch.living_room_espejo_remote_access
button.living_room_espejo_restart
button.living_room_espejo_unpair_remotes
```

---

## Alacena

```text
light.alacena
```

Uso:

```text
Tecla 2
```

Características especiales:

```text
Blanco ↔ Naranja
```

---

# JBL / Estudio

## Reproductor principal

```text
media_player.estudio
```

Nombre físico:

```text
JBL 300
```

---

## Segundo reproductor

```text
media_player.estudio_2
```

---

## Controles

```text
button.estudio_bluetooth
button.estudio_mute
button.estudio_play_pause
```

---

## Volumen

```text
number.estudio_volume
```

Estado observado durante el desarrollo:

```text
39
```

---

## Otros controles

```text
number.estudio_125hz
number.estudio_250hz
number.estudio_500hz
number.estudio_1000hz
number.estudio_2000hz
number.estudio_4000hz
number.estudio_8000hz
select.estudio_eq_preset
switch.estudio_nightmode
switch.estudio_power
switch.estudio_pure_voice
```

---

# Spotify / Spotcast

Entidades detectadas:

```text
media_player.25040rp0ag_striker_boom_convidado2_spotcast
media_player.37030f42f92b34e00f9f503a367226cbf242f8bd_striker_boom_convidado2_spotcast
media_player.desktop_tf04l4g_striker_boom_convidado2_spotcast
media_player.sala_de_estar_striker_boom_convidado2_spotcast
```

Sensores relacionados:

```text
binary_sensor.spotcast_striker_boom_convidado2_is_default_account
binary_sensor.spotcast_striker_boom_convidado2_spotify_profile_malfunction
sensor.spotcast_striker_boom_convidado2_spotify_account_type
sensor.spotcast_striker_boom_convidado2_spotify_current_playlist
sensor.spotcast_striker_boom_convidado2_spotify_devices
sensor.spotcast_striker_boom_convidado2_spotify_followers
sensor.spotcast_striker_boom_convidado2_spotify_liked_songs
sensor.spotcast_striker_boom_convidado2_spotify_playlists
sensor.spotcast_striker_boom_convidado2_spotify_product
sensor.spotcast_striker_boom_convidado2_spotify_profile
```

---

# TV / Monitor

Entidad detectada:

```text
media_player.philips_google_tv_ta6_lt
```

Estado observado:

```text
unavailable
```

La integración física/lógica todavía necesita ser completada.

---

# Home Assistant

URL local:

```text
http://localhost:8123
```

La comunicación se realiza mediante:

```text
Home Assistant REST API
```

Autenticación:

```text
Bearer Token
```

El token se almacena únicamente en:

```text
config.py
```

y no debe subirse al repositorio.

---

# Otras entidades relevantes

## Proyector

Todavía no se ha identificado/documentado definitivamente la entidad Home Assistant correspondiente.

## Control IR

```text
infrared.control_universal_ir_emitter
remote.control_universal
remote.sala_de_estar
```

Estas entidades pueden utilizarse posteriormente para integrar dispositivos controlados por infrarrojos.

---

# Entidades no relacionadas directamente

El sistema Home Assistant contiene muchas otras entidades, pero no deben incorporarse al controlador hasta que exista una función concreta para ellas.

````

Guardá igual:

**Ctrl + O → Enter → Ctrl + X**

---

## 3. Crear `CHANGELOG.md`

Finalmente:

```bash
nano ~/numpad-ha/CHANGELOG.md
````

Pegá:

````markdown
# CHANGELOG

Historial del desarrollo del Numpad Home Assistant Controller.

---

# 2026-08-09 — Prototipo funcional

## Estado

El proyecto alcanzó un estado de:

```text
PROTOTIPO FUNCIONAL
````

El numpad puede controlar diferentes dispositivos de Home Assistant mediante un único programa Python.

---

# Etapa 1 — Lectura del numpad

Se identificó el dispositivo:

```text
HS6209 2.4G Wireless Receiver
```

Linux lo expone mediante:

```text
/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd
```

Se utilizó:

```python
evdev
```

para leer los eventos de teclado directamente.

---

# Etapa 2 — Comunicación con Home Assistant

Se implementó comunicación mediante:

```text
Home Assistant REST API
```

utilizando:

```python
requests
```

La autenticación se realiza mediante:

```text
Authorization: Bearer <HA_TOKEN>
```

El token se separó del código principal y se almacenó en:

```text
config.py
```

---

# Etapa 3 — Selección de luces

Se implementó la selección mediante:

```text
1–6
```

Cada tecla representa una luz.

La variable:

```python
selected_light
```

mantiene la luz actualmente seleccionada.

---

# Etapa 4 — Control de brillo

Se implementaron:

```text
+ → brillo +
- → brillo -
```

El paso configurado inicialmente fue:

```text
10%
```

mediante:

```python
BRIGHTNESS_STEP = 10
```

---

# Etapa 5 — Doble pulsación

Se agregó detección de doble pulsación utilizando:

```python
DOUBLE_PRESS_TIME = 0.4
```

Esto permitió utilizar la misma tecla para dos funciones.

Ejemplo:

```text
1 simple
→ seleccionar Aurum

1 doble
→ encender/apagar Aurum
```

---

# Etapa 6 — Encendido con brillo predeterminado

Cuando una luz estaba apagada y se solicitaba encenderla, se implementó:

```python
DEFAULT_BRIGHTNESS = 70
```

Esto evita que una luz vuelva a encenderse con un nivel de brillo inesperado.

---

# Etapa 7 — Problema de saturación

Durante las pruebas se mantuvo presionada la tecla `+`.

El numpad generó muchos eventos consecutivos.

El controlador realizó numerosas solicitudes HTTP a Home Assistant.

Finalmente apareció:

```text
requests.exceptions.ReadTimeout
```

con:

```text
HTTPConnectionPool(host='localhost', port=8123)
```

Conclusión:

El problema no estaba relacionado con el numpad sino con la cantidad de solicitudes REST consecutivas.

Este comportamiento debe seguir optimizándose.

---

# Etapa 8 — Reorganización completa del layout

Se decidió abandonar progresivamente el primer layout experimental para evitar desarrollar memoria muscular sobre una distribución que posteriormente sería modificada.

Se estableció el nuevo diseño:

```text
1–6 → luces
0 → todas las luces
. → temperatura/color
/ → JBL
7–9 → Spotify
Backspace → TV/monitor
Enter → proyector
* → reservado
+/- → control contextual
```

---

# Etapa 9 — JBL / Estudio

Se identificó:

```text
media_player.estudio
```

como el JBL 300.

Se agregó:

```text
/ → seleccionar JBL
+ → volumen +
- → volumen -
```

También:

```text
doble / → Bluetooth
```

utilizando:

```text
button.estudio_bluetooth
```

---

# Etapa 10 — Spotify / Spotcast

Se decidió separar el control nativo del JBL del control de Spotify.

La tecla:

```text
8
```

tiene dos comportamientos.

Simple:

```text
8 → Play/Pause nativo
```

Doble:

```text
8 → Play/Pause Spotcast
```

Las teclas:

```text
7 → anterior
9 → siguiente
```

quedan asociadas al control de Spotify mediante Spotcast.

---

# Etapa 11 — Temperatura de color

Se reasignó:

```text
.
```

para cambiar la temperatura/color de la luz seleccionada.

Luces normales:

```text
Blanco frío ↔ Blanco cálido
```

Espejo y Alacena:

```text
Blanco ↔ Naranja
```

---

# Etapa 12 — Control global

Se estableció:

```text
0 → toggle general
```

y se diseñó:

```text
0 doble
→ modo de brillo global
```

En este modo:

```text
+ → todas las luces +
- → todas las luces -
```

Durante las pruebas se detectó que el toggle general funcionaba, pero el modo de brillo global necesitaba refinamiento.

---

# Etapa 13 — Proyector

Se asignó:

```text
Enter
```

para el proyector.

Diseño:

```text
Enter simple → encender
Enter doble → OK
```

---

# Etapa 14 — TV / Monitor

Se asignó:

```text
Backspace
```

al TV/monitor.

Diseño:

```text
Backspace simple → función principal
Backspace doble → modo volumen
```

En modo volumen:

```text
+ → volumen +
- → volumen -
```

---

# Estado actual

El sistema es funcional como prototipo.

Las próximas modificaciones deben realizarse de manera incremental.

Antes de cambiar el controlador se debe:

1. Leer `README.md`.
2. Leer `PROJECT_CONTEXT.md`.
3. Leer `KEYMAP.md`.
4. Leer `ENTITIES.md`.
5. Revisar `CHANGELOG.md`.
6. Revisar el código actual.
7. Probar la modificación sin eliminar funcionalidades existentes.

---

# Regla de desarrollo

No reemplazar una versión funcional por una implementación simplificada sin conservar explícitamente las funciones existentes.

El proyecto utiliza estados contextuales y pulsaciones dobles deliberadamente.

La prioridad es:

```text
FUNCIONALIDAD
↓
ESTABILIDAD
↓
ROBUSTEZ
↓
NUEVAS FUNCIONES
```

````
