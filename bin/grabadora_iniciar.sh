#!/bin/bash

# tarjeta de sonido
CARDNAME="CODEC"
tmp=$(grep -Ev "^#|^$" ~/bin/grabadora_config.txt)
if [[ $tmp ]]; then
    CARDNAME=$tmp
fi

# disco USB
PINCHO="/dev/sda1"
tmp=$(lsblk -f -r | grep "sd" | grep fat | cut -d' ' -f1)
if [[ $tmp ]]; then
    PINCHO="/dev/"$tmp
fi


# paramos lo que hubiera en marcha
~/bin/grabadora_detener.sh 1>/dev/null 2>&1

# montamos el disco USB
sudo mkdir -p /mnt/pinchousb
sudo mount -o umask=000 "$PINCHO" /mnt/pinchousb

# servidor de audio
jackd -d alsa -d hw:"$CARDNAME" -C -r 48000 &
sleep 3

# prefijo del archivo de audio
ahora=$(date +%Y%m%d-%H%M)
fprefix="audio_""$ahora""_"

# Grabación:
# El archivo de salida se nombra automáticamente por 'jack_capture',
# si existiera no se sobreecriberá, se incrementará el contador del sufijo.
jack_capture    -b 16 \
                -p system:capture* \
                --filename-prefix /mnt/pinchousb/"$fprefix" \
                --daemon &
