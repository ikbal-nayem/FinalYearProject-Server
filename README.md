# Smart home security server script

python --version ```3.10.4```

## Access to Raspberry pi zero w (ssh, vnc)
```ssh
user = pi
pass = password0
```

## Connect to Wifi
Add wpa_supplicant.conf file to the boot directory.

wpa_supplicant.conf
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
 ssid="Xiaomi"
 psk="ikbr2932"
 id_str="home"
}

network={
 ssid="ikbal.webx"
 psk="12345678"
 id_str="laptop"
}

network={
 ssid="CSE LAB 1"
 psk="12345678"
 id_str="laptop"
}
```

## Migrate DB table after change table column
```flask db init```
```flask db migrate -m "Adding column x."```
```flask db upgrade```