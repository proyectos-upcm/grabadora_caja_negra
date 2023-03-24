# GRABADORA "CAJA NEGRA" PARA MESA DE MEZCLAS

Grabadora para mesa de mezclas con interfaz de audio USB.

Las pistas de audio quedan almacenadas en un PINCHO USB de memoria.

## FUNCIONAMIENTO

Basta conectar a la Raspberry Pi por este orden:

- Un PINCHO USB de memoria.
- El cable USB de la mesa de mezclas.
- Conectar la fuente de alimentación de la Raspberry Pi.

Esperamos al arranque de la Raspberry Pi (unos 30 segundos).

En el momento en que el LED ROJO de la máquina se apague, estará en disposición de **ser pulsado el BOTÓN (durante 3 segundos)** para **INICIAR** o **DETENER** la grabación sucesivamente.

INDICACIONES:

- LED ROJO PARPADEANDO >> GRABACION EN CURSO
- LED ROJO APAGADO >> GRABACION DETENIDA

## INSTALACION:

### Paquetes Linux

```
sudo apt install jackd2 alsa-utils libasound2-dev libasound2-plugins  \
                 libjack-jackd2-dev libsamplerate0 libsamplerate0-dev  \
                 mc jq anacron netcat source-highlight jack-capture \
                 sox libsox-fmt-all ipython3

```

### Usuario Linux

```
sudo adduser upcm
sudo usermod -a -G audio,plugdev,gpio upcm
```

```
sudo nano /etc/dbus-1/system-local.conf
```

```
    <busconfig>
        <policy user="YourUserHere">
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
