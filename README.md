# grabadora_mesa_mezclas
Grabadora para mesa de mezclas con interfaz de audio USB


## Paquetes Linux

```
sudo apt install jackd2 alsa-utils libasound2-dev libasound2-plugins  \
                 libjack-jackd2-dev libsamplerate0 libsamplerate0-dev  \
                 mc jq anacron netcat source-highlight jack-capture sox \
                 ipython3

```

## Usuario Linux

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
