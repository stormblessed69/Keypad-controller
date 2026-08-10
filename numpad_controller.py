import time
import requests

from evdev import InputDevice, categorize, ecodes

from config import (
    HA_URL,
    HA_TOKEN,
    LIGHTS,
    JBL,
    BRIGHTNESS_STEP,
    DEFAULT_BRIGHTNESS,
    DOUBLE_PRESS_TIME,
)

DEVICE = "/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# ============================================================
# AJUSTES DE SEGURIDAD / AUTOREPEAT
# ============================================================

# Tiempo mínimo entre acciones repetidas de + y -
REPEAT_INTERVAL = 0.18

# Tiempo máximo para considerar dos pulsaciones como doble pulsación
DOUBLE_TIME = DOUBLE_PRESS_TIME

# Timeout corto para que HA nunca congele el controlador
REQUEST_TIMEOUT = 2


# ============================================================
# DISPOSITIVO
# ============================================================

dev = InputDevice(DEVICE)


# ============================================================
# ESTADO
# ============================================================

selected_light = None
selected_all = False
selected_jbl = False
selected_tv = False

last_number = None
last_number_time = 0

last_action = {}
pending_zero_time = 0


# ============================================================
# UTILIDADES
# ============================================================

def can_repeat(keycode):
    """
    Evita que mantener una tecla presionada
    genere cientos de peticiones a Home Assistant.
    """

    now = time.monotonic()

    last = last_action.get(keycode, 0)

    if now - last < REPEAT_INTERVAL:
        return False

    last_action[keycode] = now
    return True


def call_service(domain, service, data=None):
    """
    Ejecuta un servicio de Home Assistant sin permitir
    que un timeout mate el programa.
    """

    url = f"{HA_URL}/api/services/{domain}/{service}"

    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json=data or {},
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.Timeout:
        print("⚠️ Timeout de Home Assistant. Continuando...")
        return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con Home Assistant: {e}")
        return False

    if response.status_code >= 300:
        print(f"❌ Error HA {response.status_code}:")
        print(response.text)
        return False

    return True


def get_state(entity):
    """
    Obtiene el estado actual de una entidad.
    """

    url = f"{HA_URL}/api/states/{entity}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.Timeout:
        print("⚠️ Timeout consultando Home Assistant.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error consultando HA: {e}")
        return None

    if response.status_code != 200:
        print(f"❌ Error HA {response.status_code}")
        return None

    try:
        return response.json()["state"]

    except Exception:
        return None


def get_attributes(entity):
    """
    Obtiene los atributos de una entidad.
    """

    url = f"{HA_URL}/api/states/{entity}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.Timeout:
        print("⚠️ Timeout consultando Home Assistant.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error consultando HA: {e}")
        return None

    if response.status_code != 200:
        print(f"❌ Error HA {response.status_code}")
        return None

    try:
        return response.json().get("attributes", {})

    except Exception:
        return None


# ============================================================
# SELECCIÓN DE LUCES
# ============================================================

def select_light(key):
    global selected_light
    global selected_all
    global selected_jbl
    global selected_tv

    entity = LIGHTS.get(key)

    if not entity:
        print("⚠️ Esa luz todavía no está configurada.")
        return

    selected_light = entity
    selected_all = False
    selected_jbl = False
    selected_tv = False

    print(f"💡 Luz seleccionada: {entity}")


def select_all_lights():
    global selected_light
    global selected_all
    global selected_jbl
    global selected_tv

    selected_light = None
    selected_all = True
    selected_jbl = False
    selected_tv = False

    print("💡 TODAS LAS LUCES SELECCIONADAS")
    print("+/- → brillo de todas las luces")


def select_jbl():
    global selected_light
    global selected_all
    global selected_jbl
    global selected_tv

    selected_light = None
    selected_all = False
    selected_jbl = True
    selected_tv = False

    print("🔊 JBL/ESTUDIO SELECCIONADO")
    print("+/- → volumen")


def select_tv():
    global selected_light
    global selected_all
    global selected_jbl
    global selected_tv

    selected_light = None
    selected_all = False
    selected_jbl = False
    selected_tv = True

    print("📺 TV/MONITOR SELECCIONADO")
    print("+/- → volumen de TV")


# ============================================================
# LISTA DE LUCES REALES
# ============================================================

def get_all_lights():
    return [
        entity
        for entity in LIGHTS.values()
        if entity
    ]


# ============================================================
# BRILLO / VOLUMEN
# ============================================================

def change_brightness(amount):

    if selected_all:

        lights = get_all_lights()

        if not lights:
            print("⚠️ No hay luces configuradas.")
            return

        for entity in lights:

            call_service(
                "light",
                "turn_on",
                {
                    "entity_id": entity,
                    "brightness_step_pct": amount,
                },
            )

        print(
            f"☀️ Brillo "
            f"{'+' if amount > 0 else ''}"
            f"{amount}% → TODAS LAS LUCES"
        )

        return

    if selected_jbl:

        if amount > 0:
            call_service(
                "button",
                "press",
                {
                    "entity_id": "button.estudio_increase_volume",
                },
            )
            print("🔊 Volumen +")

        else:
            call_service(
                "button",
                "press",
                {
                    "entity_id": "button.estudio_lower_volume",
                },
            )
            print("🔊 Volumen -")

        return

    if selected_tv:

        if amount > 0:
            call_service(
                "remote",
                "send_command",
                {
                    "entity_id": "remote.control_universal",
                    "device": "televisor_monitor",
                    "command": "volume_up",
                },
            )

            print("📺 Volumen UP")

        else:
            call_service(
                "remote",
                "send_command",
                {
                    "entity_id": "remote.control_universal",
                    "device": "televisor_monitor",
                    "command": "volume_down",
                },
            )

            print("📺 Volumen DOWN")

        return

    if not selected_light:

        print(
            "⚠️ Primero seleccioná una luz con 1–6 "
            "o todas con 0."
        )

        return

    call_service(
        "light",
        "turn_on",
        {
            "entity_id": selected_light,
            "brightness_step_pct": amount,
        },
    )

    print(
        f"☀️ Brillo "
        f"{'+' if amount > 0 else ''}"
        f"{amount}% → {selected_light}"
    )


# ============================================================
# TOGGLE DE UNA LUZ
# ============================================================

def toggle_or_default(entity):

    state = get_state(entity)

    if state is None:
        return

    if state == "on":

        call_service(
            "light",
            "turn_off",
            {
                "entity_id": entity,
            },
        )

        print(f"🌑 OFF → {entity}")

    else:

        call_service(
            "light",
            "turn_on",
            {
                "entity_id": entity,
                "brightness_pct": DEFAULT_BRIGHTNESS,
            },
        )

        print(
            f"💡 ON → {entity} "
            f"({DEFAULT_BRIGHTNESS}%)"
        )


# ============================================================
# TOGGLE DE TODAS LAS LUCES
# ============================================================

def toggle_all_lights():

    lights = get_all_lights()

    if not lights:
        print("⚠️ No hay luces configuradas.")
        return

    # Consultamos los estados.
    states = []

    for entity in lights:

        state = get_state(entity)

        if state is not None:
            states.append(state)

    if not states:
        print("⚠️ No pude consultar las luces.")
        return

    # Si TODAS están encendidas → apagar todas.
    # En cualquier otro caso → encender todas.
    all_on = all(state == "on" for state in states)

    if all_on:

        call_service(
            "light",
            "turn_off",
            {
                "entity_id": lights,
            },
        )

        print("🌑 OFF → TODAS LAS LUCES")

    else:

        call_service(
            "light",
            "turn_on",
            {
                "entity_id": lights,
                "brightness_pct": DEFAULT_BRIGHTNESS,
            },
        )

        print(
            f"💡 ON → TODAS LAS LUCES "
            f"({DEFAULT_BRIGHTNESS}%)"
        )


# ============================================================
# CAMBIO DE COLOR / TEMPERATURA
# ============================================================

def change_light_mode():

    if selected_all:

        lights = get_all_lights()

        for entity in lights:

            change_entity_mode(entity)

        print("🎨 Cambio de modo → TODAS LAS LUCES")

        return

    if not selected_light:

        print(
            "⚠️ Primero seleccioná una luz con 1–6 "
            "o todas con 0."
        )

        return

    change_entity_mode(selected_light)


def change_entity_mode(entity):

    # --------------------------------------------------------
    # ESPEJO Y ALACENA
    # Blanco ↔ Naranja
    # --------------------------------------------------------

    if entity in (
        "light.living_room_espejo",
        "light.alacena",
    ):

        state = get_state(entity)

        # Si está apagada, arrancamos en blanco.
        if state != "on":

            call_service(
                "light",
                "turn_on",
                {
                    "entity_id": entity,
                    "brightness_pct": DEFAULT_BRIGHTNESS,
                    "rgb_color": [255, 255, 255],
                },
            )

            print(f"⚪ BLANCO → {entity}")
            return

        # Consultamos atributos para determinar el color.
        attributes = get_attributes(entity)

        if attributes is None:
            return

        rgb = attributes.get("rgb_color")

        # Si está aproximadamente naranja → blanco
        if rgb and rgb[0] > 180 and rgb[1] < 180:

            call_service(
                "light",
                "turn_on",
                {
                    "entity_id": entity,
                    "rgb_color": [255, 255, 255],
                },
            )

            print(f"⚪ BLANCO → {entity}")

        else:

            call_service(
                "light",
                "turn_on",
                {
                    "entity_id": entity,
                    "rgb_color": [255, 100, 0],
                },
            )

            print(f"🎨 NARANJA → {entity}")

        return

    # --------------------------------------------------------
    # AURUM / CUPRUM
    # Blanco frío ↔ Blanco cálido
    # --------------------------------------------------------

    if entity in (
        "light.living_room_aurum",
        "light.kitchen_cuprum",
    ):

        attributes = get_attributes(entity)

        if attributes is None:
            return

        color_temp_kelvin = attributes.get(
            "color_temp_kelvin"
        )

        min_temp = attributes.get(
            "min_color_temp_kelvin"
        )

        max_temp = attributes.get(
            "max_color_temp_kelvin"
        )

        # Valores aproximados.
        # Se adaptan automáticamente si HA informa
        # los límites de temperatura.

        if min_temp is not None and max_temp is not None:

            cold_kelvin = max_temp
            warm_kelvin = min_temp

        else:

            cold_kelvin = 6500
            warm_kelvin = 2700

        # Si no sabemos el estado actual,
        # empezamos en frío.
        if color_temp_kelvin is None:

            target = cold_kelvin
            mode = "❄️ BLANCO FRÍO"

        else:

            # Calculamos el punto medio en Kelvin.
            midpoint = (
                min_temp + max_temp
            ) / 2 if (
                min_temp is not None
                and max_temp is not None
            ) else (cold_kelvin + warm_kelvin) / 2

            if color_temp_kelvin > midpoint:

                target = warm_kelvin
                mode = "🔥 BLANCO CÁLIDO"

            else:

                target = cold_kelvin
                mode = "❄️ BLANCO FRÍO"

        call_service(
            "light",
            "turn_on",
            {
                "entity_id": entity,
                "color_temp_kelvin": target,
            },
        )

        print(f"{mode} → {entity}")

        return

    print(f"⚠️ Modo de color no configurado para {entity}")


# ============================================================
# JBL / MULTIMEDIA
# ============================================================

def jbl_play_pause():
    """
    Native JBL play/pause via button.
    """

    call_service(
        "button",
        "press",
        {
            "entity_id": "button.estudio_play_pause",
        },
    )

    print("⏯️ Play/Pause (JBL nativo)")


def spotcast_transfer():
    """
    Transfer Spotify playback to media_player.estudio
    via spotcast.transfer_playback.
    """

    call_service(
        "spotcast",
        "transfer_playback",
        {
            "entity_id": "media_player.estudio",
        },
    )

    print("🎵 Spotcast Transfer to Estudio")


def jbl_bluetooth():
    """
    Toggle JBL Bluetooth via button.
    """

    call_service(
        "button",
        "press",
        {
            "entity_id": "button.estudio_bluetooth",
        },
    )

    print("📱 JBL Bluetooth")


def media_previous():
    """
    Previous track on media_player.estudio.
    """

    call_service(
        "media_player",
        "media_previous_track",
        {
            "entity_id": "media_player.estudio",
        },
    )

    print("⏮️ Previous Track")


def media_next():
    """
    Next track on media_player.estudio.
    """

    call_service(
        "media_player",
        "media_next_track",
        {
            "entity_id": "media_player.estudio",
        },
    )

    print("⏭️ Next Track")


# ============================================================
# INFRARED / BROADLINK
# ============================================================

def broadlink_send(device, command):
    """
    Send IR command via Broadlink remote.
    """

    call_service(
        "remote",
        "send_command",
        {
            "entity_id": "remote.control_universal",
            "device": device,
            "command": command,
        },
    )

    print(f"📡 IR {device}: {command}")


def projector_power():
    """
    Projector power toggle (single press Enter).
    """

    broadlink_send("proyector", "power")


def projector_ok():
    """
    Projector OK button (double press Enter).
    """

    broadlink_send("proyector", "ok")


def tv_power():
    """
    TV power toggle (single press Backspace).
    """

    broadlink_send("televisor_monitor", "power")


# ============================================================
# INICIO
# ============================================================

print()
print("======================================")
print("      NUMPAD HOME ASSISTANT")
print("======================================")
print(f"Dispositivo: {dev.name}")
print("Controlador iniciado.")
print()
print("1-6 → seleccionar luces")
print("00 → toggle todas")
print("0 → seleccionar todas")
print("+/- → brillo")
print(". → color / temperatura")
print("/ → JBL/Estudio")
print("// → JBL Bluetooth")
print("7 → Previous Track")
print("8 → JBL Play/Pause")
print("88 → Spotcast Transfer")
print("9 → Next Track")
print("Enter → Proyector Power")
print("Enter (double) → Proyector OK")
print("Backspace → TV Power")
print("Backspace (double) → TV Volume Mode")
print()


# ============================================================
# LOOP PRINCIPAL
# ============================================================

for event in dev.read_loop():

    if event.type != ecodes.EV_KEY:
        continue

    key = categorize(event)

    # --------------------------------------------------------
    # SOLO KEY DOWN
    # --------------------------------------------------------

    if key.keystate != key.key_down:
        continue

    keycode = key.keycode

    # --------------------------------------------------------
    # IGNORAR NUMLOCK
    # --------------------------------------------------------

    if keycode == "KEY_NUMLOCK":
        continue

    # --------------------------------------------------------
    # 0
    # --------------------------------------------------------

    if keycode == "KEY_KP0":

        now = time.monotonic()

        # Segundo 0 dentro de la ventana
        if (
            last_number == "KEY_KP0"
            and now - last_number_time <= DOUBLE_TIME
        ):

            last_number = None
            last_number_time = 0

            toggle_all_lights()

            continue

        # Primer 0
        select_all_lights()

        last_number = "KEY_KP0"
        last_number_time = now

        continue

    # --------------------------------------------------------
    # LUCES 1-6
    # --------------------------------------------------------

    if keycode in LIGHTS:

        now = time.monotonic()

        # Doble pulsación
        if (
            last_number == keycode
            and now - last_number_time <= DOUBLE_TIME
        ):

            entity = LIGHTS.get(keycode)

            if entity:
                toggle_or_default(entity)

            last_number = None
            last_number_time = 0

            continue

        # Primera pulsación
        select_light(keycode)

        last_number = keycode
        last_number_time = now

        continue

    # --------------------------------------------------------
    # BRILLO +
    # --------------------------------------------------------

    if keycode == "KEY_KPPLUS":

        if can_repeat(keycode):
            change_brightness(BRIGHTNESS_STEP)

        continue

    # --------------------------------------------------------
    # BRILLO -
    # --------------------------------------------------------

    if keycode == "KEY_KPMINUS":

        if can_repeat(keycode):
            change_brightness(-BRIGHTNESS_STEP)

        continue

    # --------------------------------------------------------
    # .
    # CAMBIO DE COLOR / TEMPERATURA
    # --------------------------------------------------------

    if keycode == "KEY_KPDOT":

        if can_repeat(keycode):
            change_light_mode()

        continue

    # --------------------------------------------------------
    # 7 — Previous Track
    # --------------------------------------------------------

    if keycode == "KEY_KP7":

        if can_repeat(keycode):
            media_previous()

        continue

    # --------------------------------------------------------
    # 8 — JBL Play/Pause or Spotcast Transfer
    # --------------------------------------------------------

    if keycode == "KEY_KP8":

        now = time.monotonic()

        # Doble pulsación: Spotcast Transfer
        if (
            last_number == keycode
            and now - last_number_time <= DOUBLE_TIME
        ):

            last_number = None
            last_number_time = 0

            spotcast_transfer()

            continue

        # Primera pulsación: JBL native play/pause
        jbl_play_pause()

        last_number = keycode
        last_number_time = now

        continue

    # --------------------------------------------------------
    # 9 — Next Track
    # --------------------------------------------------------

    if keycode == "KEY_KP9":

        if can_repeat(keycode):
            media_next()

        continue

    # --------------------------------------------------------
    # / — JBL Selection or Bluetooth
    # --------------------------------------------------------

    if keycode == "KEY_KPSLASH":

        now = time.monotonic()

        # Doble pulsación: JBL Bluetooth
        if (
            last_number == keycode
            and now - last_number_time <= DOUBLE_TIME
        ):

            last_number = None
            last_number_time = 0

            jbl_bluetooth()

            continue

        # Primera pulsación: Select JBL
        select_jbl()

        last_number = keycode
        last_number_time = now

        continue

    # --------------------------------------------------------
    # Backspace — TV Power or TV Volume Context
    # --------------------------------------------------------

    if keycode == "KEY_BACKSPACE":

        now = time.monotonic()

        # Doble pulsación: TV Volume Context
        if (
            last_number == keycode
            and now - last_number_time <= DOUBLE_TIME
        ):

            last_number = None
            last_number_time = 0

            select_tv()

            continue

        # Primera pulsación: TV Power
        tv_power()

        last_number = keycode
        last_number_time = now

        continue

    # --------------------------------------------------------
    # Enter — Projector Power or OK
    # --------------------------------------------------------

    if keycode == "KEY_KPENTER":

        now = time.monotonic()

        # Doble pulsación: Projector OK
        if (
            last_number == keycode
            and now - last_number_time <= DOUBLE_TIME
        ):

            last_number = None
            last_number_time = 0

            projector_ok()

            continue

        # Primera pulsación: Projector Power
        projector_power()

        last_number = keycode
        last_number_time = now

        continue

    # --------------------------------------------------------
    # DEBUG
    # --------------------------------------------------------

    print(f"Tecla no asignada: {keycode}")
