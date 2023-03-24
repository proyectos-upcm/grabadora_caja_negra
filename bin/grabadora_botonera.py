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
    sleep(3)

    B_ROJO.wait_for_press()
    detener_grabacion()


def detener_grabacion():

    print('PARANDO')
    sleep(3)


def main():
    print('PULSAR VERDE PARA INICIAR')
    while True:
        B_VERDE.wait_for_press()
        iniciar_grabacion()


if __name__ == "__main__":

    main()
