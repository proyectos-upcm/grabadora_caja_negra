#!/usr/bin/env python3
""" Control de la grabación mediante un BOTON PULSADOR
    en RASPBERRY PI > 2
"""

import  subprocess  as sp
from    gpiozero    import Button
from    time        import sleep
import  threading


########################################################################
# GPIO-03_pin-05 <---> GND_pin-06 (tercera pareja de pines)
BOTON = Button(3) # GPIO-03
LED   = 'rojo'
########################################################################


def _bucle_led():
    """ BUCLE INFINITO que gobierna un led de la placa, en función
        del evento 'ev_blink' lo hace parpadar o lo mantiene apagado
    """

    def blink(frec='normal'):
        t = {'normal': 1.0, 'rapido': 0.1, 'off': 0}.get(frec)
        if t:
            sp.Popen(f"sudo sh -c 'echo {onoff} > /sys/class/leds/{led}/brightness'", shell=True)
            sleep(t)
        else:
            sp.Popen(f"sudo sh -c 'echo 0       > /sys/class/leds/{led}/brightness'", shell=True)
            sleep(1)


    # Por defecto usamos el LED 'rojo' de la placa
    led = {'verde': 'led0', 'rojo': 'led1'}.get(LED, 'led1')

    # BUCLE de parpadeo
    onoff = 0
    jack_capture = None
    while True:

        if ev_blink.is_set():
            if not jack_capture:
                blink('rapido')
                try:
                    jack_capture = sp.check_output('pgrep -f jack_capture'.split())
                except:
                    pass
            else:
                blink('normal')
        else:
            blink('off')

        onoff = {0:1, 1:0}.get(onoff)


def _bucle_boton(tp=3):
    """ BUCLE INFINITO que lee las pulsaciones del botón de control,
        con un tiempo de persistencia tp por defecto 3 segundos.
    """

    def espera_pulsacion():
        """ Comprueba que el botón esté pulsado durante tp segundos
        """
        c = 0
        while True:
            BOTON.wait_for_press()
            c += 1
            sleep(.5)
            if c >= 2 * tp:
                break


    print('PULSAR BOTON PARA INICIAR/PARAR')

    # BUCLE de lectura
    grabar = False
    while True:
        espera_pulsacion()
        grabar = {True:False, False:True}.get(grabar)
        if grabar:
            iniciar_grabacion()
        else:
            detener_grabacion()


def iniciar_grabacion():

    print('GRABANDO')
    # Inicia el parpadeo del LED
    ev_blink.set()
    # Ejecuta script de incio de la grabadora
    sp.Popen("~/bin/grabadora_iniciar.sh", shell=True)


def detener_grabacion():

    print('PARANDO')
    # Detiene el parpadeo del LED
    ev_blink.clear()
    # Ejecuta script de detención de la grabadora
    sp.Popen("~/bin/grabadora_detener.sh", shell=True)


if __name__ == "__main__":

    # Inicia la gestión del LED
    ev_blink = threading.Event()
    th_led = threading.Thread(target=_bucle_led)
    th_led.start()

    # Inicia la lectura del botón de control
    th_boton = threading.Thread(target=_bucle_boton)
    th_boton.start()

