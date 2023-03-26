#!/bin/bash

# tarjeta de sonido
CARDNAME=$(aplay -l | grep USB | cut -d' ' -f3)
if [[ ! $CARDNAME ]]; then
    CARDNAME="CODEC"
fi

# Paramos la grabación
pkill -f jack_capture

# Paramos el servidor de audio
pkill -f "$CARDNAME"
sleep 1

# Desmontamos el pincho USB
sudo umount /mnt/pinchousb 1>/dev/null 2>&1
sync
