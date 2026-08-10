# 🎛️ Numpad Home Assistant Controller

Controlador personalizado para utilizar un **numpad inalámbrico HS6209 2.4G Wireless Receiver** como panel físico de control para **Home Assistant**.

El proyecto convierte las teclas del numpad en controles físicos para:

- 💡 Luces
- ☀️ Brillo
- 🎨 Temperatura/color de las luces
- 🔊 JBL / Estudio
- 🎵 Spotify mediante Spotcast
- 📺 TV / monitor
- 📽️ Proyector
- 🌐 Home Assistant
- 🧩 Funciones futuras y escenas

El controlador está escrito en **Python** y funciona directamente sobre Linux utilizando `evdev` para leer las pulsaciones del dispositivo.

---

## 🖥️ Hardware

### Numpad

**Dispositivo detectado por Linux:**

```text
HS6209 2.4G Wireless Receiver
Ruta utilizada por el controlador:

/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd

El numpad posee:

18 teclas físicas
4 columnas
5 filas
Teclas low-profile
Conectividad inalámbrica 2.4 GHz
Teclas numéricas con funciones secundarias
Tecla +
Tecla -
/
*
.
Enter
Backspace
🏠 Entorno

El sistema funciona con:

Linux
Python 3
evdev
requests
Home Assistant
Spotcast
Git
GitHub

Home Assistant está disponible localmente mediante:

http://localhost:8123

El controlador se ejecuta directamente en el servidor Linux y se comunica con Home Assistant mediante su API REST.

🎹 Mapa actual del teclado
💡 Luces

Las teclas 1 a 6 seleccionan una luz.

Teclas
Tecla	Luz
1	Aurum
2	Alacena
3	Luz futura
4	Cuprum
5	Espejo
6	Luz futura

La selección funciona con una pulsación simple.

Una vez seleccionada una luz:

+ → aumenta brillo
- → disminuye brillo

El incremento actual es de:

10%
Doble pulsación

Una doble pulsación de 1–6:

ON/OFF

La lógica de encendido utiliza un brillo predeterminado cuando la luz estaba apagada.

☀️ Brillo global

La tecla:

0

realiza un toggle general de las luces.

La intención del diseño es que una doble pulsación de 0 active el modo de control global de brillo.

En ese modo:

+ → aumenta brillo de todas las luces
- → disminuye brillo de todas las luces

Este comportamiento todavía se encuentra en fase de refinamiento.

🎨 Temperatura / color

La tecla:

.

cambia el tipo de iluminación de la luz seleccionada.

Para las luces normales:

Blanco frío ↔ Blanco cálido

Para:

light.living_room_espejo
light.alacena

el comportamiento debe ser:

Blanco ↔ Naranja

Esto se debe a que esas luminarias procesan el color de manera diferente.

🔊 JBL / Estudio

El JBL utilizado en el proyecto aparece en Home Assistant como:

media_player.estudio

y se conoce físicamente como:

JBL 300

La tecla:

/

selecciona/controla el JBL.

Una vez seleccionado:

+ → volumen +
- → volumen -

Una doble pulsación de:

/

activa Bluetooth mediante:

button.estudio_bluetooth
🎵 Spotify / Spotcast

Las teclas:

7
8
9

están destinadas al control de Spotify mediante Spotcast.

Su función es:

Tecla	Spotify / Spotcast
7	Anterior
8	Play / Pause
9	Siguiente

Existe una distinción importante:

8 pulsación simple

Controla:

Play/Pause del dispositivo nativo JBL/Estudio
8 doble pulsación

Controla:

Play/Pause de Spotify mediante Spotcast

Esto permite diferenciar el reproductor nativo de la reproducción controlada por Spotify.

📺 TV / Monitor

La tecla:

Backspace

está reservada para el dispositivo:

TV / Monitor

Una pulsación controla la función principal.

Una doble pulsación de Backspace cambia al modo:

+ → volumen +
- → volumen -
📽️ Proyector

La tecla:

Enter

controla el proyector.

Pulsación simple
Encender proyector
Doble pulsación
OK

La función está pensada para utilizar el Enter como botón físico principal del proyector.

⭐ Tecla *

La tecla:

*

queda reservada para futuras escenas y automatizaciones.

No tiene una función definitiva todavía.

🔢 NumLock

La tecla NumLock se ignora deliberadamente.

Esto evita que el estado de NumLock interfiera con el funcionamiento del controlador.

🧠 Concepto de funcionamiento

El controlador mantiene internamente un estado de selección.

Por ejemplo:

1
↓
Selecciona Aurum
↓
+
↓
Aumenta brillo de Aurum

Otro ejemplo:

5
↓
Selecciona Espejo
↓
.
↓
Cambia Blanco ↔ Naranja

Y:

/
↓
Selecciona JBL
↓
+
↓
Aumenta volumen

El sistema utiliza pulsaciones dobles para acceder a funciones secundarias sin necesidad de agregar más teclas físicas.

🏠 Entidades Home Assistant

Las principales entidades utilizadas actualmente son:

Luces
light.alacena
light.kitchen_cuprum
light.living_room_aurum
light.living_room_espejo
JBL / Estudio
media_player.estudio
media_player.estudio_2

Controles auxiliares:

button.estudio_bluetooth
button.estudio_mute
button.estudio_play_pause
number.estudio_volume
switch.estudio_power
switch.estudio_nightmode
switch.estudio_pure_voice
Spotcast
media_player.25040rp0ag_striker_boom_convidado2_spotcast
media_player.37030f42f92b34e00f9f503a367226cbf242f8bd_striker_boom_convidado2_spotcast
media_player.desktop_tf04l4g_striker_boom_convidado2_spotcast
media_player.sala_de_estar_striker_boom_convidado2_spotcast
TV
media_player.philips_google_tv_ta6_lt

Actualmente aparece como:

unavailable

por lo que su integración continúa pendiente.

🐍 Código

El controlador principal es:

numpad_controller.py

También existe:

numpad_controller_v2.py

que corresponde a una versión anterior del desarrollo.

El archivo:

test_numpad.py

contiene pruebas utilizadas durante el desarrollo inicial.

⚙️ Configuración

La configuración privada se encuentra en:

config.py

Este archivo contiene información sensible, incluyendo el token de Home Assistant.

NO debe subirse a GitHub.

El .gitignore evita que sea incluido en commits.

La configuración incluye:

HA_URL
HA_TOKEN
LIGHTS
JBL
BRIGHTNESS_STEP
DEFAULT_BRIGHTNESS
DOUBLE_PRESS_TIME
🔐 Seguridad

Nunca publicar:

HA_TOKEN

ni:

config.py

El repositorio está configurado para ignorarlos.

Si el token alguna vez queda expuesto públicamente:

Revocar el token en Home Assistant.
Crear uno nuevo.
Actualizar config.py.
🛠️ Arquitectura

El flujo general es:

Numpad
   │
   ▼
Linux evdev
   │
   ▼
numpad_controller.py
   │
   ├── Detecta tecla
   │
   ├── Detecta pulsación simple/doble
   │
   ├── Mantiene estado seleccionado
   │
   ▼
Home Assistant REST API
   │
   ├── Light
   ├── Media Player
   ├── Button
   ├── Switch
   └── Spotcast
🐛 Problemas encontrados durante el desarrollo
Saturación de Home Assistant

Durante pruebas de mantener + o - presionado se generaron muchas solicitudes consecutivas.

Esto provocó:

requests.exceptions.ReadTimeout

con:

HTTPConnectionPool(host='localhost', port=8123)

El problema no era una falla física del numpad.

La causa era que el controlador podía generar solicitudes HTTP demasiado rápidamente.

Esto deberá seguir siendo refinado para hacer el sistema más robusto frente a pulsaciones prolongadas.

Teclas no asignadas

Durante las primeras pruebas aparecieron códigos como:

KEY_KPASTERISK
KEY_BACKSPACE
KEY_KPENTER

Esto permitió identificar cómo Linux estaba interpretando algunas teclas físicas y adaptar el mapeo.

Diferencias entre dispositivos de audio

Se descubrió que:

media_player.estudio

representa el dispositivo JBL nativo.

Mientras que Spotcast utiliza entidades media_player diferentes.

Por eso se decidió separar:

8 simple

de:

8 doble

para permitir controlar ambos sistemas.

📈 Evolución del proyecto

El proyecto comenzó como un controlador sencillo:

Tecla → acción Home Assistant

Después se incorporaron:

Selección de luces
       ↓
Control de brillo
       ↓
Doble pulsación
       ↓
Estados diferentes
       ↓
Control multimedia
       ↓
Spotify / Spotcast
       ↓
Modos secundarios

La filosofía actual es mantener un teclado físico pequeño pero conseguir múltiples funciones mediante:

pulsaciones simples
dobles pulsaciones
selección de dispositivos
estados internos
funciones contextuales
🤖 Contexto para IA / Copilot

Si una IA continúa este proyecto, debe leer primero:

README.md
PROJECT_CONTEXT.md

Antes de modificar:

numpad_controller.py

Es especialmente importante conservar:

El layout físico del numpad.
Las funciones asignadas a cada tecla.
Las entidades reales de Home Assistant.
La diferencia entre JBL nativo y Spotcast.
La lógica de pulsación simple/doble.
La selección contextual de dispositivos.
El tratamiento especial de Espejo y Alacena.
La protección del token de Home Assistant.

No reemplazar código funcional por una versión simplificada sin analizar primero el código existente.

El objetivo del proyecto es evolucionar progresivamente desde un prototipo funcional hacia un controlador físico completo para Home Assistant.

🚧 Estado actual

El proyecto se encuentra en estado:

PROTOTIPO FUNCIONAL

Las funciones básicas ya están operativas.

Las próximas mejoras deberían realizarse de forma incremental, evitando romper las funciones que actualmente funcionan correctamente.

📚 Documentación adicional

Documentación técnica detallada:

PROJECT_CONTEXT.md

Mapa completo de teclas:

KEYMAP.md

Entidades utilizadas:

ENTITIES.md

Historial de cambios:

CHANGELOG.md
