# GRABADORA "CAJA NEGRA"

Grabadora caja negra, ideada para grabar un evento sonorizado con una mesa de mezclas con interfaz de audio USB.

También se puede usar por ejemplo conectándole cualquier interfaz de audio (tarjeta de sonido) USB y algún micrófono.

La interfaz de usuario consiste en un sencillo pulsador y un LED indicador del estado de la grabadora.

Las pistas de audio quedan almacenadas en un PINCHO USB de memoria, con un nombre de archivo secuencial con la fecha y hora de inicio.

El script `grabadora_control.py` permite usar un LED de los integrados en una placa Raspberry Pi o bien un LED dedicado en las conexiones GPIO.

## FUNCIONAMIENTO

Basta conectar a la Raspberry Pi por este orden:

- Un PINCHO USB de memoria.
- El cable USB de la mesa de mezclas.
- Conectar la fuente de alimentación de la Raspberry Pi (cargador recomendado >= 2 A)

Esperamos al arranque de la Raspberry Pi (unos 30 segundos).

Si usamos el LED rojo integrado en la placa Raspberry Pi, al conectarle alimentación se pone en rojo, y se apaga cuando el programa de control de la grabación está listo.

Si usamos un LED dedicado no lucirá, basta con esperar los 30 segundos referidos.

**PULSAR el BOTÓN (durante > 3 segundos)** para **INICIAR** o **DETENER** la grabación sucesivamente. Normalmente la detendremos al final del evento a la par que la cámara deja de grabar.

### Indicaciones LED:

- PARPADEO RÁPIDO >> PREPARANDO GRABACION ... (\*)
- PARPADEO LENTO >> GRABACION EN CURSO
- APAGADO >> GRABACION DETENIDA

(\*) Si la grabadora NO pudiera acceder al PINCHO, seguirá el PARPADEO RÁPIDO

### Extracción del PINCHO USB de memoria:

Podremos extraer el PINCHO USB cuando el LED esté apagado, o lógicamente cuando la Raspberry Pi esté sin alimentación.

## INSTALACION:

### Paquetes Linux

```
sudo apt install jackd2 jack-capture sox libsox-fmt-all ipython3
```

### Archivos

Copiar el contenido de `bin/` de este repositorio en `/home/upcm/bin/`


### Ajustes para el usuario `upcm`

```
sudo adduser upcm
sudo usermod -a -G audio,plugdev,gpio upcm
```

```
sudo nano /etc/dbus-1/system-local.conf
```

```
    <busconfig>
        <policy user="upcm">
            <allow own="org.freedesktop.ReserveDevice1.Audio0"/>
            <allow own="org.freedesktop.ReserveDevice1.Audio1"/>
            <allow own="org.freedesktop.ReserveDevice1.Audio2"/>
            <allow own="org.freedesktop.ReserveDevice1.Audio3"/>
        </policy>
    </busconfig>
```
    
```
sudo service dbus restart
```

### Autoarranque al encendido

```
sudo nano /etc/rc.local
```
```
...
...
...

# Grabadora controlada por un boton
su -l upcm -c "grabadora_control.py &"

exit 0
```
