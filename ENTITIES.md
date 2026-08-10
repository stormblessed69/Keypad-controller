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
