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

