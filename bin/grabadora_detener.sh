#!/bin/bash

CARDNAME="CODEC"
tmp=$(grep -Ev "^#|^$" ~/bin/grabadora_config.txt)
if [[ $tmp ]]; then
    CARDNAME=$tmp
fi

# Paramos la grabación
pkill -f jack_capture

# Paramos el servidor de audio
pkill -f "$CARDNAME"
sleep 1

# Desmontamos el pincho USB
sudo umount /mnt/pinchousb 1>/dev/null 2>&1
sync
