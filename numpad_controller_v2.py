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

dev = InputDevice(DEVICE)

selected_light = None
last_number = None
last_number_time = 0

# ---------------------------------------
# CONTROL DE REPETICIÓN DEL BRILLO
# ---------------------------------------

BRIGHTNESS_INTERVAL = 0.15
last_brightness_time = 0


# ---------------------------------------
# HOME ASSISTANT
# ---------------------------------------

def call_service(domain, service, data=None):
    url = f"{HA_URL}/api/services/{domain}/{service}"

    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json=data or {},
            timeout=2,
        )

        if response.status_code >= 300:
            print(f"❌ Error HA: {response.status_code}")
            print(response.text)
            return False

        return True

    except requests.exceptions.Timeout:
        print("⚠️ Home Assistant tardó demasiado en responder.")
        return False

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error de conexión con Home Assistant: {e}")
        return False


# ---------------------------------------
# SELECCIÓN DE LUZ
# ---------------------------------------

def select_light(key):
    global selected_light

    entity = LIGHTS.get(key)

    if not entity:
        print("⚠️ Esa luz todavía no está configurada.")
        return

    selected_light = entity

    print(f"💡 Luz seleccionada: {entity}")


# ---------------------------------------
# TOGGLE SIMPLE
# ---------------------------------------

def toggle_light(entity):
    if call_service(
        "light",
        "toggle",
        {"entity_id": entity},
    ):
        print(f"🔄 Toggle: {entity}")


# ---------------------------------------
# CAMBIO DE BRILLO
# ---------------------------------------

def change_brightness(amount):
    global last_brightness_time

    if not selected_light:
        print("⚠️ Primero seleccioná una luz con 1–6.")
        return

    now = time.monotonic()

    # Evita bombardear Home Assistant
    if now - last_brightness_time < BRIGHTNESS_INTERVAL:
        return

    last_brightness_time = now

    if call_service(
        "light",
        "turn_on",
        {
            "entity_id": selected_light,
            "brightness_step_pct": amount,
        },
    ):
        print(
            f"☀️ Brillo {'+' if amount > 0 else ''}{amount}% "
            f"→ {selected_light}"
        )


# ---------------------------------------
# TOGGLE / BRILLO POR DEFECTO
# ---------------------------------------

def toggle_or_default(entity):

    url = f"{HA_URL}/api/states/{entity}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=2,
        )

    except requests.exceptions.Timeout:
        print("⚠️ Home Assistant tardó demasiado en responder.")
        return

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error consultando Home Assistant: {e}")
        return

    if response.status_code != 200:
        print(
            f"❌ No pude consultar el estado. "
            f"HTTP {response.status_code}"
        )
        return

    try:
        state = response.json()["state"]
    except (KeyError, ValueError):
        print("❌ Respuesta inválida de Home Assistant.")
        return

    if state == "on":

        if call_service(
            "light",
            "turn_off",
            {"entity_id": entity},
        ):
            print(f"🌑 OFF → {entity}")

    else:

        if call_service(
            "light",
            "turn_on",
            {
                "entity_id": entity,
                "brightness_pct": DEFAULT_BRIGHTNESS,
            },
        ):
            print(
                f"💡 ON → {entity} "
                f"({DEFAULT_BRIGHTNESS}%)"
            )


# ---------------------------------------
# INICIO
# ---------------------------------------

print()
print("======================================")
print("      NUMPAD HOME ASSISTANT")
print("======================================")
print(f"Dispositivo: {dev.name}")
print("Controlador iniciado.")
print()


# ---------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------

for event in dev.read_loop():

    if event.type != ecodes.EV_KEY:
        continue

    key = categorize(event)

    # Solo detectar pulsación inicial.
    # Ignora key-up y repeticiones generadas
    # automáticamente por el teclado.
    if key.keystate != key.key_down:
        continue

    keycode = key.keycode

    # Algunas teclas pueden devolver una lista
    # de códigos en evdev.
    if isinstance(keycode, list):
        keycode = keycode[0]

    # ---------------------------------------
    # NUM LOCK
    # ---------------------------------------

    if keycode == "KEY_NUMLOCK":
        continue


    # ---------------------------------------
    # LUCES 1–6
    # ---------------------------------------

    if keycode in LIGHTS:

        now = time.monotonic()

        # Doble pulsación
        if (
            last_number == keycode
            and now - last_number_time <= DOUBLE_PRESS_TIME
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


    # ---------------------------------------
    # BRILLO
    # ---------------------------------------

    if keycode == "KEY_KPPLUS":

        change_brightness(BRIGHTNESS_STEP)

        continue


    if keycode == "KEY_KPMINUS":

        change_brightness(-BRIGHTNESS_STEP)

        continue


    # ---------------------------------------
    # JBL
    # ---------------------------------------

    if keycode == "KEY_KP7":

        if call_service(
            "media_player",
            "volume_down",
            {"entity_id": JBL},
        ):
            print("🔊 Volumen -")

        continue


    if keycode == "KEY_KP8":

        if call_service(
            "media_player",
            "volume_up",
            {"entity_id": JBL},
        ):
            print("🔊 Volumen +")

        continue


    if keycode == "KEY_KP9":

        if call_service(
            "media_player",
            "media_play_pause",
            {"entity_id": JBL},
        ):
            print("▶️ Play/Pause")

        continue


    # ---------------------------------------
    # TODAS LAS LUCES
    # ---------------------------------------

    if keycode == "KEY_KP0":

        entities = [
            entity
            for entity in LIGHTS.values()
            if entity
        ]

        if entities:

            if call_service(
                "light",
                "toggle",
                {
                    "entity_id": entities
                },
            ):
                print("💡 Toggle todas las luces")

        else:
            print("⚠️ No hay luces configuradas.")

        continue


    # ---------------------------------------
    # DEBUG
    # ---------------------------------------

    print(f"Tecla no asignada: {keycode}")
