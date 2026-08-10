# AI_CONTEXT — Numpad Home Assistant Controller

## INSTRUCCIÓN PRINCIPAL

Este repositorio contiene un proyecto funcional de un numpad inalámbrico convertido en controlador físico para Home Assistant.

Antes de modificar cualquier código:

1. Leer `README.md`.
2. Leer `PROJECT_CONTEXT.md`.
3. Leer `KEYMAP.md`.
4. Revisar `numpad_controller.py`.
5. Revisar `config.py` si está disponible localmente.
6. No eliminar funcionalidades existentes sin indicarlo explícitamente.
7. Mantener compatibilidad con el hardware y las entidades documentadas.
8. Probar cada modificación antes de reemplazar una versión funcional.

El objetivo es evolucionar el proyecto incrementalmente, no reescribirlo desde cero.

---

# HARDWARE

Dispositivo:

```text
HS6209 2.4G Wireless Receiver

Dispositivo Linux:

/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd

El controlador utiliza Python + evdev para leer directamente los eventos del teclado.

El programa se ejecuta en un servidor Linux y controla Home Assistant mediante REST API.

HOME ASSISTANT

URL:

http://localhost:8123

Comunicación:

Home Assistant REST API

Autenticación:

Bearer Token

El token está únicamente en:

config.py

config.py NO debe subirse a GitHub.

ARCHIVO PRINCIPAL

Controlador actual:

numpad_controller.py

Versiones anteriores:

numpad_controller_v2.py
numpad_controller.WORKING_BACKUP.py

No reemplazar el controlador actual por una versión anterior salvo que se solicite explícitamente.

MAPA ACTUAL
LUces
1 → Aurum
2 → Alacena
3 → futura luz
4 → Cuprum
5 → Espejo
6 → futura luz

Entidades:

1 → light.living_room_aurum
2 → light.alacena
4 → light.kitchen_cuprum
5 → light.living_room_espejo

Una pulsación:

1–6 → seleccionar luz

Una vez seleccionada:

+ → brillo +10%
- → brillo -10%

Doble pulsación:

1–6 → encender/apagar luz

Si estaba apagada:

DEFAULT_BRIGHTNESS = 70
0 — TODAS LAS LUCES

Una pulsación:

0 → toggle de todas las luces

Doble pulsación:

0 → activar modo de brillo global

En modo global:

+ → brillo de todas las luces +
- → brillo de todas las luces -

IMPORTANTE:

El toggle general ya funciona.

El modo de brillo global requiere especial cuidado porque fue una de las partes que presentó problemas durante las pruebas.

. — COLOR / TEMPERATURA

La tecla . cambia el tipo de iluminación de la luz seleccionada.

Luces normales:

Blanco frío ↔ Blanco cálido

Espejo:

Blanco ↔ Naranja

Alacena:

Blanco ↔ Naranja

Espejo y Alacena manejan el color de forma diferente al resto.

/ — JBL

JBL físico:

JBL 300

Entidad principal:

media_player.estudio

Una pulsación:

/ → seleccionar JBL

Después:

+ → volumen +
- → volumen -

Doble pulsación:

/ / → button.estudio_bluetooth
7 — SPOTIFY ANTERIOR
7 → pista anterior

Debe utilizar Spotcast.

8 — PLAY/PAUSE

Una pulsación:

8 → Play/Pause del dispositivo nativo

Dispositivo nativo:

media_player.estudio

Doble pulsación:

8 8 → Play/Pause de Spotify mediante Spotcast

IMPORTANTE:

Estas dos funciones deben permanecer separadas.

9 — SPOTIFY SIGUIENTE
9 → siguiente pista

Debe utilizar Spotcast.

BACKSPACE — TV / MONITOR

Dispositivo objetivo:

media_player.philips_google_tv_ta6_lt

Actualmente figura como:

unavailable

Diseño:

Backspace → función principal TV/monitor
Backspace doble → activar modo volumen

En modo volumen:

+ → volumen +
- → volumen -

Esta integración todavía puede necesitar desarrollo.

ENTER — PROYECTOR

Una pulsación:

Enter → encender proyector

Doble pulsación:

Enter Enter → OK

La entidad específica del proyector todavía debe identificarse si no está documentada.

* — RESERVADA

Actualmente no tiene función.

Reservada para futuras escenas o automatizaciones.

No asignarla sin autorización explícita.

NUMLOCK

Debe ignorarse:

KEY_NUMLOCK
DOBLE PULSACIÓN

Configuración actual:

DOUBLE_PRESS_TIME = 0.4

Dos pulsaciones de la misma tecla dentro de aproximadamente 400 ms se consideran doble pulsación.

No eliminar este sistema.

CONTROL CONTEXTUAL

El diseño depende de un concepto importante:

TECLA
+
ESTADO SELECCIONADO
+
MODO ACTIVO
+
TIPO DE PULSACIÓN

Ejemplo:

/ → JBL seleccionado
+ → volumen JBL

Pero:

5 → Espejo seleccionado
+ → brillo Espejo

Y:

Backspace doble
→ modo volumen TV
+ → volumen TV

Por lo tanto + y - NO deben convertirse en funciones globales rígidas.

ENTIDADES IMPORTANTES

Luces:

light.living_room_aurum
light.kitchen_cuprum
light.living_room_espejo
light.alacena

JBL:

media_player.estudio

Controles JBL:

button.estudio_bluetooth
button.estudio_mute
button.estudio_play_pause
number.estudio_volume

Spotify / Spotcast:

media_player.25040rp0ag_striker_boom_convidado2_spotcast
media_player.37030f42f92b34e00f9f503a367226cbf242f8bd_striker_boom_convidado2_spotcast
media_player.desktop_tf04l4g_striker_boom_convidado2_spotcast
media_player.sala_de_estar_striker_boom_convidado2_spotcast

TV:

media_player.philips_google_tv_ta6_lt

IR:

infrared.control_universal_ir_emitter
remote.control_universal
remote.sala_de_estar
PROBLEMA CONOCIDO — BRILLO

Durante las primeras pruebas, mantener + o - presionado generó muchos eventos consecutivos.

Esto provocó demasiadas solicitudes REST simultáneas/secuenciales a Home Assistant.

Resultado observado:

requests.exceptions.ReadTimeout

Ejemplo:

HTTPConnectionPool(host='localhost', port=8123)
Read timed out. (read timeout=5)

Cualquier solución futura debe considerar:

rate limiting
debounce
acumulación de cambios
evitar solicitudes innecesarias
no bloquear el loop principal
manejo de excepciones de red

Pero NO sacrificar la respuesta normal de las teclas.

FILOSOFÍA DEL PROYECTO

Este es un controlador físico pensado para uso diario.

La memoria muscular importa.

No cambiar arbitrariamente el layout.

No mover funciones existentes sin autorización.

No eliminar funciones para simplificar el código.

Preferir:

pequeñas modificaciones
+
pruebas
+
commit

en lugar de reescrituras completas.

PROCEDIMIENTO PARA MODIFICAR

Antes:

leer documentación
↓
entender estado actual
↓
identificar función afectada

Modificar:

hacer el cambio mínimo necesario

Probar:

tecla normal
tecla mantenida
doble pulsación
cambio de contexto
errores de Home Assistant

Después:

git status
git diff
git add .
git commit
git push

Cada versión funcional debe quedar respaldada en Git.

REGLA DE ORO

Si una función actualmente funciona:

NO ROMPERLA

Si una nueva función requiere modificarla:

explicar primero qué cambia

Si aparece un error:

diagnosticar el error
↓
corregir específicamente el problema
↓
volver a probar

No hacer una reescritura completa solamente porque apareció un bug puntual.

OBJETIVO FINAL

Convertir el numpad en un controlador físico completo para:

Home Assistant
Luces
JBL
Spotify
TV/Monitor
Proyector
Escenas
Automatizaciones

manteniendo una interfaz física consistente, rápida y fácil de memorizar.

