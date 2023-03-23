#!/bin/bash

CARDNAME="CODEC"
tmp=$(grep -Ev "^#|^$" ~/bin/grabacion_config.txt)
if [[ $tmp ]]; then
    CARDNAME=$tmp
fi

~/bin/grabacion_detener.sh 1>/dev/null 2>&1

sudo mkdir -p /mnt/pinchousb
sudo mount -o umask=000 /dev/sda1 /mnt/pinchousb

jackd -d alsa -d hw:"$CARDNAME" -C -r 48000 &
sleep 3

ahora=$(date +%Y%m%d-%H%M)
fprefix="audio_""$ahora""_"

# El archivo de salida se nombra automáticamente por 'jack_capture',
# si existiera no se sobreecriberá, se incrementará el contador del sufijo.
jack_capture    -b 16 \
                -p system:capture* \
                --filename-prefix /mnt/pinchousb/"$fprefix" \
                --daemon &
