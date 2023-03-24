#!/usr/bin/env python3

import  sys
from    subprocess  import Popen
from    gpiozero    import Button
from    time        import sleep
import  threading


#################
BOTON = Button(3)
LED   = 'rojo'
#################


def _bucle_led():
    """ BUCLE infinito que gobierna un led de la placa, en función
        del evento 'ev_blink' lo hace parpadar o lo mantiene apagado
    """

    # Por defecto usamos el LED 'rojo' de la placa
    led = {'verde': 'led0', 'rojo': 'led1'}.get(LED, 'led1')

    # BUCLE de parpadeo
    onoff = 0
    while True:

        if ev_blink.is_set():
            Popen(f"sudo sh -c 'echo {onoff} > /sys/class/leds/{led}/brightness'", shell=True)
        else:
            Popen(f"sudo sh -c 'echo {0}     > /sys/class/leds/{led}/brightness'", shell=True)

        sleep(.5)

        onoff = {0:1, 1:0}.get(onoff)


def _bucle_boton(tg=3):
    """ BUCLE INFINITO que lee las pulsaciones del botón de control,
        con un tiempo de guarda tg (por defecto 3 segundos) hasta empezar
        a leer de nuevo.
    """

    def espera_pulsacion(t=3):
        """ Comprueba que el botón esté pulsado de forma sostenida
            durante t segundos
        """
        BOTON.wait_for_press()

    grabar = False
    while True:
        espera_pulsacion()
        grabar = {True:False, False:True}.get(grabar)
        if grabar:
            iniciar_grabacion()
        else:
            detener_grabacion()
        sleep(tg)


def iniciar_grabacion():

    print('GRABANDO')
    # Inicia el parpadeo del LED
    ev_blink.set()
    # Ejecuta script de incio de la grabadora
    # Popen(...)


def detener_grabacion():

    print('PARANDO')
    # Detiene el parpadeo del LED
    ev_blink.clear()
    # Ejecuta script de detención de la grabadora
    # Popen(...)


if __name__ == "__main__":

    # Inicia la gestión del LED
    ev_blink = threading.Event()
    th_led = threading.Thread(target=_bucle_led)
    th_led.start()


    # Inicia la lectura del botón de control
    print('PULSAR BOTON PARA INICIAR/PARAR')
    th_boton = threading.Thread(target=_bucle_boton)
    th_boton.start()

