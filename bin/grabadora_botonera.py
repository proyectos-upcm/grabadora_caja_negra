#/usr/bin/env python3

import sys
from subprocess import Popen
from gpiozero import LED, Button
from time import sleep

#######################
B_VERDE     = Button(2)
B_ROJO      = Button(3)
LED_VERDE   = LED(17)
LED_ROJO    = LED(18)
#######################

def iniciar_grabacion():

    print('GRABANDO')
    # Popen(...)

    B_ROJO.wait_for_press()
    detener_grabacion()
    sleep(1)                # debounce


def detener_grabacion():

    print('PARANDO')
    # Popen(...)


def main():
    print('PULSAR VERDE PARA INICIAR')
    while True:
        B_VERDE.wait_for_press()
        iniciar_grabacion() # esto ya tarda unos segundos


if __name__ == "__main__":

    main()
