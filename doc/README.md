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

### Configuración:

**No se precisa**

Opcionalmente podemos EDITAR el script `grabadora_control.py` para usar un LED de los integrados en la placa Raspberry Pi (útil si usamos una caja transparente) o bien un LED externo en serie con 330 ohm conectado en un par de pines GPIO (en caso de ser una caja opaca).


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
    

### Autoarranque al encendido

```
sudo nano /etc/rc.local
```
```
...
...
...

# Grabadora controlada por un boton
su -l upcm -c "/home/upcm/bin/grabadora_control.py &"

exit 0
```

