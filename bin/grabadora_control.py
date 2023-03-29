#!/usr/bin/env python3
""" Control de la grabación mediante un BOTON PULSADOR
    en RASPBERRY PI >= 2
"""

import  subprocess  as sp
import  gpiozero
from    time        import sleep
import  threading

#################    OPCIONES DE CONFIGURACION    ######################
# GPIO-03_pin-05 <---> GND_pin-06 (tercera pareja de pines)
BOTON = gpiozero.Button(3)  # GPIO-03

# Opción usando uno de los LED integrados en placa (rojo o verde)
#LED   = 'rojo'

# Opción usando un LED dedicado en un pin GPIO
LED   = gpiozero.LED(15)    # GPIO-15 (quinta pareja de pines)
########################################################################


def loop_boton_gpio(tp=3):
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


def loop_detecta_jack_capture():
    """ BUCLE INFINITO para la detección del proceso 'jack_capture',
        activando entonces el flag JACK_CAPTURE, y gestionando en
        consecuencia las indicaciones de estado (LED y consola)
    """

    global JACK_CAPTURE

    def display_update(estado):
        """ maneja LED y consola
        """
        modo_led = {'PARADO':'off', 'GRABANDO':'normal', 'PREPARANDO':'rapido'}.get(estado, 'off')
        if TIPO_DE_LED == 'gpio':
            led_gpio_blink(modo_led)
        else:
            # el led integrado tiene un loop propio en threading
            pass

        print(f'---> {estado}')


    st = st_prev = 'PARADO'
    while True:

        if GRABACION_INICIADA:

            try:
                sp.check_output('pgrep -f jack_capture'.split())
                JACK_CAPTURE = True
            except:
                JACK_CAPTURE = False


            if JACK_CAPTURE:

                st = 'GRABANDO'
                if st != st_prev:
                    display_update(st)
                st_prev = st

            else:

                st = 'PREPARANDO'
                if st != st_prev:
                    display_update(st)
                st_prev = st

        else:

            st = 'PARADO'
            if st != st_prev:
                display_update(st)
            st_prev = st

        sleep(1)


def loop_led_integrado():
    """ BUCLE INFINITO que gobierna un led integrado en la placa, en función
        del las variables GRABACION_INICIADA y JACK_CAPTURE lo hace parpadar
        o lo mantiene apagado.

        NOTA: los led de placa no están gestionados por la libreria 'gpiozero',
              por tanto necesitamos este LOOP para hacerlo parpadear.
    """

    def blink(frec='normal'):
        t = {'normal': 1.0, 'rapido': 0.1, 'off': 0}.get(frec)
        if t:
            sp.Popen(f"sudo sh -c 'echo {onoff} > /sys/class/leds/{ledX}/brightness'", shell=True)
            sleep(t)
        else:
            sp.Popen(f"sudo sh -c 'echo 0       > /sys/class/leds/{ledX}/brightness'", shell=True)
            sleep(1)


    # Por defecto .get resolverá el LED 'rojo' de la placa 'led1'
    ledX = {'verde': 'led0', 'rojo': 'led1'}.get(LED, 'led1')

    # BUCLE del parpadeo (OjO el sleep está implementado en la subfunción blink)
    onoff = 0
    while True:

        if GRABACION_INICIADA:
            # Parpadeo normal cuando se detecte jack_capture funcionando
            if JACK_CAPTURE:
                blink('normal')
            else:
                blink('rapido')
        else:
            blink('off')

        onoff = {0:1, 1:0}.get(onoff)


def led_gpio_blink(mode='normal'):
    """ Usado para gestionar un LED dedicado en un pin GPIO
        usando la librería gpiozero
    """

    if mode == 'normal':
        ton = 1.5; toff = 1.0
    elif mode == 'rapido':
        ton = 0.15; toff = 0.15
    else:
        LED.off()
        return

    LED.blink(on_time=ton, off_time=toff)


def iniciar_grabacion():

    global GRABACION_INICIADA

    # Ejecuta script de incio de la grabadora
    sp.Popen("~/bin/grabadora_iniciar.sh", shell=True)
    GRABACION_INICIADA = True


def detener_grabacion():

    global GRABACION_INICIADA

    # Ejecuta script de detención de la grabadora
    sp.Popen("~/bin/grabadora_detener.sh", shell=True)
    GRABACION_INICIADA = False


if __name__ == "__main__":

    # Indicativo del tipo de LED en uso
    TIPO_DE_LED = 'integrado' if (type(LED) == str) else 'gpio'

    # Flags indicativos del estado de la grabadora
    GRABACION_INICIADA = False
    JACK_CAPTURE       = False

    # LOOP de lectura del botón de control
    th_boton = threading.Thread(target = loop_boton_gpio)
    th_boton.start()

    # LOOP que detecta si 'jack_capture' está en ejecución y maneja
    # la visualización al usuario en consecuencia.
    th_jack_capture = threading.Thread(target = loop_detecta_jack_capture)
    th_jack_capture.start()

    # LOOP auxiliar para hacer parpadear un LED integrado en placa
    if TIPO_DE_LED == 'integrado':
        th_led = threading.Thread(target = loop_led_integrado)
        th_led.start()
