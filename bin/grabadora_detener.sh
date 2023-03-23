#!/bin/bash

CARDNAME="CODEC"
tmp=$(grep -Ev "^#|^$" ~/bin/grabadora_config.txt)
if [[ $tmp ]]; then
    CARDNAME=$tmp
fi

pkill -f jack_capture
pkill -f "$CARDNAME"
sleep 1

sudo umount /mnt/pinchousb 1>/dev/null 2>&1
sync
