#!/usr/bin/env python3
""" Control de la grabación mediante un BOTON PULSADOR
    en RASPBERRY PI >= 2
"""

import  subprocess  as sp
import  gpiozero
from    time        import sleep
import  threading


########################################################################
# GPIO-03_pin-05 <---> GND_pin-06 (tercera pareja de pines)
BOTON = gpiozero.Button(3)  # GPIO-03

# Opción con LED integrado en placa (rojo o verde)
#LED   = 'rojo'

# Opción con LED dedidcado en un pin GPIO
LED   = gpiozero.LED(15)    # GPIO-15 (quinta pareja de pines)
########################################################################


def detecta_jack_capture():

    detectado = False

    c = 10  # límite de intentos
    n = 0   # veces detectado jack_capture
    while c:
        try:
            sp.check_output('pgrep -f jack_capture'.split())
            n += 1
        except:
            pass
        if n == 3:
            detectado = True
            break
        c -= 1
        sleep(1)

    print('jack_capture en ejecución:', detectado)

    return detectado


def _bucle_led_placa():
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
            # Parpadeo normal cuando se detecte jack_capture funcionando
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


def led_blink(mode='normal'):
    """ Usado para gestionar un LED dedicado en un pin GPIO
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

    print('GRABANDO')
    # Ejecuta script de incio de la grabadora
    sp.Popen("~/bin/grabadora_iniciar.sh", shell=True)

    # Inicia el parpadeo del LED integrado o dedicado
    if led_integrado:

        ev_blink.set()

    else:

        led_blink('rapido')
        if detecta_jack_capture():
            led_blink('normal')


def detener_grabacion():

    print('PARANDO')
    # Ejecuta script de detención de la grabadora
    sp.Popen("~/bin/grabadora_detener.sh", shell=True)
    # Detiene el parpadeo del LED
    if led_integrado:
        ev_blink.clear()
    else:
        led_blink('off')


if __name__ == "__main__":

    # Inicia la lectura del botón de control
    th_boton = threading.Thread(target=_bucle_boton)
    th_boton.start()

    # Inicia la gestión del LED integrado en placa si es el elegido
    led_integrado = True if (type(LED) == str) else False
    if led_integrado:
        ev_blink = threading.Event()
        th_led = threading.Thread(target=_bucle_led_placa)
        th_led.start()
