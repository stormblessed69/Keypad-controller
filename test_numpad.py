from evdev import InputDevice, categorize, ecodes

DEVICE = "/dev/input/by-id/usb-HS6209_2.4G_Wireless_Receiver-event-kbd"

dev = InputDevice(DEVICE)

print("===================================")
print("   NUMPAD HOME ASSISTANT - TEST")
print("===================================")
print(f"Dispositivo: {dev.name}")
print("Esperando teclas...")
print("Ctrl+C para salir")
print()

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key = categorize(event)

        # Solo reaccionamos al momento de PRESIONAR
        if key.keystate == key.key_down:
            print(f"Tecla: {key.keycode}")
