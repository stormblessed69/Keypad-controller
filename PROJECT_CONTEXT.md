# Numpad Home Assistant Controller — Project Context

## 1. Propósito del proyecto

Este proyecto convierte un numpad inalámbrico USB en un controlador físico personalizado para Home Assistant.

El objetivo es disponer de un único dispositivo físico para controlar:

- luces
- brillo
- temperatura/color de las luces
- JBL / Spotify
- volumen
- reproducción
- proyector
- TV / monitor
- escenas futuras

El proyecto está pensado para evolucionar progresivamente. No modificar funciones existentes sin comprobar primero que no se rompa el comportamiento actual.

---

# 2. Hardware

## Numpad

Dispositivo:

HS6209 2.4G Wireless Receiver

El sistema Linux lo identifica como:

HS6209 2.4G Wireless Receiver

Input device:

/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd

Se utiliza Python + evdev para leer directamente los eventos del teclado.

El dispositivo es inalámbrico y permanece encendido.

No existe una función de encendido/apagado del numpad que deba controlarse mediante software.

---

# 3. Entorno

## Sistema

Servidor Linux.

Usuario:

server

Proyecto:

~/numpad-ha

## Python

El controlador utiliza Python.

Bibliotecas principales:

- evdev
- requests
- time

## Home Assistant

Home Assistant corre localmente en:

http://localhost:8123

La comunicación se realiza mediante la API REST de Home Assistant.

La autenticación utiliza un Long-Lived Access Token.

IMPORTANTE:

El token NO debe aparecer nunca en GitHub.

Está almacenado en:

config.py

Este archivo está excluido mediante .gitignore.

---

# 4. Arquitectura actual

El numpad genera eventos Linux EV_KEY.

Python recibe los eventos mediante:

evdev.InputDevice

El controlador identifica:

- tecla
- pulsación
- tiempo entre pulsaciones

Luego ejecuta acciones mediante la API REST de Home Assistant.

Flujo:

Numpad
    ↓
Linux evdev
    ↓
numpad_controller.py
    ↓
Home Assistant REST API
    ↓
Entidades de Home Assistant
    ↓
Luces / JBL / Spotify / TV / proyector

---

# 5. Archivos actuales

## numpad_controller.py

Controlador principal actual.

Es el archivo que debe considerarse como referencia principal del sistema.

## numpad_controller_v2.py

Versión anterior / experimental.

Debe conservarse como referencia histórica hasta decidir si todavía es necesaria.

## test_numpad.py

Archivo utilizado para pruebas.

## config.py

Configuración local y secretos.

NO subir a GitHub.

Contiene:

- HA_URL
- HA_TOKEN
- LIGHTS
- JBL
- BRIGHTNESS_STEP
- DEFAULT_BRIGHTNESS
- DOUBLE_PRESS_TIME

## .gitignore

Evita subir:

- config.py
- backups
- secretos
- __pycache__
- archivos compilados
- configuraciones locales

---

# 6. Entidades de Home Assistant utilizadas

## Luces

### Aurum

light.living_room_aurum

### Cuprum

light.kitchen_cuprum

### Espejo

light.living_room_espejo

### Alacena

light.alacena

Actualmente existen otras posiciones reservadas para futuras luces.

---

# 7. JBL

El dispositivo JBL utilizado en el proyecto es conocido en Home Assistant como:

Estudio

Entidad principal:

media_player.estudio

También existe:

media_player.estudio_2

Actualmente el dispositivo que debe considerarse como JBL / Estudio es:

media_player.estudio

---

# 8. Entidades adicionales relevantes

Botón Bluetooth:

button.estudio_bluetooth

Botón Play/Pause:

button.estudio_play_pause

Botón Mute:

button.estudio_mute

Volumen:

number.estudio_volume

Power:

switch.estudio_power

Night Mode:

switch.estudio_nightmode

Pure Voice:

switch.estudio_pure_voice

Spotify / Spotcast:

binary_sensor.spotcast_striker_boom_convidado2_is_default_account

binary_sensor.spotcast_striker_boom_convidado2_spotify_profile_malfunction

media_player.37030f42f92b34e00f9f503a367226cbf242f8bd_striker_boom_convidado2_spotcast

media_player.25040rp0ag_striker_boom_convidado2_spotcast

media_player.desktop_tf04l4g_striker_boom_convidado2_spotcast

media_player.sala_de_estar_striker_boom_convidado2_spotcast

sensor.spotcast_striker_boom_convidado2_spotify_account_type

sensor.spotcast_striker_boom_convidado2_spotify_current_playlist

sensor.spotcast_striker_boom_convidado2_spotify_devices

sensor.spotcast_striker_boom_convidado2_spotify_followers

sensor.spotcast_striker_boom_convidado2_spotify_liked_songs

sensor.spotcast_striker_boom_convidado2_spotify_playlists

sensor.spotcast_striker_boom_convidado2_spotify_product

sensor.spotcast_striker_boom_convidado2_spotify_profile

---

# 9. Filosofía del layout

El objetivo es acostumbrarse desde el principio al layout definitivo.

No se debe reutilizar una tecla simplemente porque anteriormente tenía otra función.

El mapa actual debe considerarse la especificación funcional.

---

# 10. Mapa físico del numpad

Distribución:

┌─────┬─────┬─────┬─────┐
│ Num │  /  │  *  │  -  │
├─────┼─────┼─────┼─────┤
│  7  │  8  │  9  │  +  │
├─────┼─────┼─────┼─────┤
│  4  │  5  │  6  │Back │
├─────┼─────┼─────┼─────┤
│  1  │  2  │  3  │     │
├─────┴─────┼─────┼─────┤
│     0     │  .  │Enter│
└───────────┴─────┴─────┘

Enter ocupa dos unidades verticales.

0 ocupa dos unidades horizontales.

---

# 11. Luces — teclas 1 a 6

Las teclas 1–6 seleccionan luces.

La primera pulsación selecciona una luz.

Una segunda pulsación rápida de la misma tecla hace toggle:

- si está encendida → OFF
- si está apagada → ON

Cuando una luz está seleccionada:

+ aumenta el brillo
- disminuye el brillo

Esto debe funcionar con cualquier luz seleccionada.

## Asignación

1 → Aurum

light.living_room_aurum

4 → Cuprum

light.kitchen_cuprum

2 → Alacena

light.alacena

5 → Espejo

light.living_room_espejo

3 → futura luz

6 → futura luz

El sistema debe permitir agregar las luces 3 y 6 posteriormente sin rediseñar toda la arquitectura.

---

# 12. Brillo

Tecla:

+

Aumenta el brillo de la luz seleccionada.

Tecla:

-

Disminuye el brillo de la luz seleccionada.

Paso actual:

10%

BRIGHTNESS_STEP = 10

El controlador utiliza:

brightness_step_pct

de Home Assistant.

---

# 13. Control global de luces

Tecla:

0

Una pulsación:

Toggle general de todas las luces configuradas.

Doble pulsación:

Activa un modo de control global de brillo.

En este modo:

+ → aumenta brillo de todas las luces

- → disminuye brillo de todas las luces

Este comportamiento todavía requiere refinamiento.

IMPORTANTE:

Existe un problema conocido con el ciclo de brillo global donde el valor puede aparentar quedarse en 59% y luego actualizarse de forma irregular.

No considerar este comportamiento como definitivo.

---

# 14. Temperatura / color

Tecla:

.

Una pulsación cambia la luz seleccionada entre dos estados de iluminación.

Para:

Aurum / Cuprum:

blanco frío ↔ blanco cálido

Para:

Espejo / Alacena:

blanco ↔ naranja

La razón de la diferencia es que Espejo y Alacena procesan el color de forma diferente.

Esta función debe utilizar las capacidades de color de cada entidad y no asumir que todas las luces utilizan exactamente el mismo modelo de color.

---

# 15. JBL / Spotify

El JBL se identifica como:

media_player.estudio

La tecla:

/

selecciona/controla el JBL.

La función principal es permitir controlar el volumen mediante:

+ → volumen +

- → volumen -

Doble pulsación de:

/

activa Bluetooth mediante:

button.estudio_bluetooth

---

# 16. Spotify / Spotcast

Las teclas:

7
8
9

están destinadas al control de Spotify mediante Spotcast.

Funciones:

7 → Back / Previous

8 → Play / Pause

9 → Next

IMPORTANTE:

La doble pulsación de 8 debe ejecutar Play/Pause de Spotify mediante Spotcast.

Una sola pulsación de 8 debe ejecutar Play/Pause del dispositivo nativo JBL:

media_player.estudio

Esta diferencia es intencional.

---

# 17. TV / monitor

Backspace está reservado para:

TV / monitor

Una pulsación:

control de TV/monitor

Doble pulsación:

entra en modo de volumen.

El comportamiento exacto debe terminar de implementarse/refinarse.

---

# 18. Proyector

Enter:

Una pulsación → encender proyector

Doble pulsación → OK / confirmar

La implementación exacta depende de la integración/control IR disponible.

---

# 19. Tecla *

La tecla:

*

Está reservada para futuras escenas.

No asignar una función permanente todavía.

---

# 20. Tecla /

Actualmente:

/ → JBL

Doble / → Bluetooth

No debe confundirse con la antigua función de esta tecla.

---

# 21. Teclas no utilizadas / funciones futuras

*

Escenas futuras.

3

Futura luz.

6

Futura luz.

Estas posiciones deben permanecer preparadas para expansión.

---

# 22. Doble pulsación

El sistema utiliza una ventana configurable:

DOUBLE_PRESS_TIME = 0.4

La doble pulsación debe detectarse solamente cuando la misma tecla se pulsa dos veces dentro de esa ventana.

No cambiar esta lógica global sin comprobar todos los controles.

---

# 23. Problema histórico: repetición de teclas

Durante las primeras pruebas se detectó que mantener presionada + o - genera repetición automática de teclas desde Linux.

Esto provocaba múltiples llamadas REST consecutivas a Home Assistant.

Ejemplo:

+ + + + + + + + + ...

El problema llegó a provocar:

requests.exceptions.ReadTimeout

con:

HTTPConnectionPool(host='localhost', port=8123): Read timed out.

La causa no fue Home Assistant en sí, sino la cantidad de requests consecutivos generados por la repetición de teclas.

La arquitectura debe considerar este problema antes de implementar funciones que hagan muchas llamadas REST.

---

# 24. Eventos Linux observados

Algunas teclas generan códigos como:

KEY_KPASTERISK
KEY_KPPLUS
KEY_KPMINUS
KEY_KP7
KEY_KP8
KEY_KP9
KEY_KP0
KEY_KPENTER
KEY_BACKSPACE

También se observaron secuencias ANSI en consola debido a ciertas teclas de navegación.

No asumir que la leyenda física de la tecla coincide siempre con el keycode Linux.

Siempre comprobar mediante evdev cuando se agregue una nueva tecla.

---

# 25. API de Home Assistant

Las llamadas se realizan mediante:

POST /api/services/{domain}/{service}

Las consultas de estado utilizan:

GET /api/states/{entity}

Headers:

Authorization: Bearer <HA_TOKEN>

Content-Type: application/json

El token real debe permanecer únicamente en config.py.

---

# 26. Configuración actual conocida

BRIGHTNESS_STEP = 10

DEFAULT_BRIGHTNESS = 70

DOUBLE_PRESS_TIME = 0.4

JBL:

media_player.estudio

Home Assistant:

http://localhost:8123

---

# 27. Regla fundamental para futuras IAs

Antes de modificar numpad_controller.py:

1. Leer PROJECT_CONTEXT.md.
2. Leer README.md.
3. Leer numpad_controller.py completo.
4. Leer config.py solamente si existe localmente.
5. No asumir que las funciones antiguas siguen siendo correctas.
6. Respetar el mapa de teclas de este documento.
7. No eliminar funciones existentes sin indicarlo.
8. Crear un backup antes de cambios importantes.
9. Probar una función a la vez.
10. Registrar cambios en CHANGELOG.md.

---

# 28. Estado actual

El proyecto funciona como prototipo.

Las funciones principales de luces y JBL ya fueron probadas.

La prioridad actual es:

1. estabilizar el controlador
2. corregir el control global de brillo
3. terminar Spotify / Spotcast
4. terminar TV/monitor
5. terminar proyector
6. implementar temperatura/color
7. agregar escenas
8. mejorar manejo de errores
9. evitar saturación de Home Assistant
10. documentar cada nueva función

No realizar grandes refactorizaciones hasta tener una versión funcional estable.

---

# 29. Filosofía del proyecto

Este proyecto comenzó como un controlador simple de luces y fue evolucionando hacia un controlador físico universal para Home Assistant.

La prioridad es:

FUNCIONA → PROBAR → DOCUMENTAR → REFINAR

No:

REESCRIBIR TODO → AGREGAR COMPLEJIDAD → ROMPER FUNCIONES EXISTENTES

Las nuevas funciones deben agregarse de forma incremental.

---

# 30. Información para futuras IAs

Si una IA recibe este repositorio sin acceso a conversaciones anteriores, debe asumir que:

- este documento contiene la especificación funcional actual
- numpad_controller.py es el código principal
- config.py contiene secretos y no está disponible en GitHub
- Home Assistant está en localhost:8123 desde el servidor
- el dispositivo físico es el HS6209
- evdev es utilizado para detectar teclas
- las funciones de doble pulsación son deliberadas
- el layout actual debe respetarse
- el proyecto está en fase de prototipo
- los bugs conocidos deben corregirse sin romper funciones existentes

Antes de proponer código nuevo, comparar la propuesta con este documento.
