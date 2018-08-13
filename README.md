# monitoring-plugins
In this repository i will get together all check plugins i wrote by myself or i found usefull which are not included in the default ```monitoring-plugins``` you can install via ```apt```.

Keep in mind that i am working on, improving and developing new plugins within this repopsitory so check out the [release section](https://github.com/wernerfred/monitoring-plugins/releases) to use only working versions of my plugins

## Table of contents
- [check_dht.py](#check_dht.py)
- [check_synology.py](#check_synology.py)

### check_dht.py
This plugin will read the temperature and humidity values from your sensor (dht11, dht22, 3202) and return it in readable format for tools like icinga oder nagios including perfdata for visualization.

This check plugin needs the adafruit dht library available on: https://github.com/adafruit/Adafruit_Python_DHT.git

Example ```CheckCommand``` for use with ```icinga2```:
```
object CheckCommand "check_dht" {
  command = ["/usr/bin/sudo", "/usr/bin/python", PluginDir + "/check_dht.py" ]
  arguments = {
    "--model" = {
       skip_key = true
       order = 0
       value = "$dht_model$"
    }
    "--gpio" = {
       skip_key = true
       order = 1
       value = "$dht_gpio$"
    }
    "--wt" = "$dht_warning_temperature$"
    "--wh" = "$dht_warning_humidity$"
    "--ct" = "$dht_critical_temperatur$"
    "--ch" = "$dht_critical_humidity$"
  }
}
```
### check_synology.py
Keep in mind: This plugin is not released yet.

This check plugin needs ```pysnmp``` to be installed on your system. You can install it with: ```pip install pysnmp```

Example ```CheckCommand``` for use with ```icinga2```:
```
object CheckCommand "check_synology" {
  command = ["/usr/bin/python", PluginDir + "/check_synology.py" ]

  arguments = {
    "--host" = {
       skip_key = true
       order = 0
       value = "$synology_host$"
    }
    "--username" = {
       skip_key = true
       order = 1
       value = "$synology_snmp_user$"
    }
    "--authkey" = {
       skip_key = true
       order = 2
       value = "$synology_snmp_authkey$"
    }
    "--privkey" = {
       skip_key = true
       order = 3
       value = "$synology_snmp_privkey$"
    }
    "--mode" = {
       skip_key = true
       order = 4
       value = "$synology_mode$"
    }
    "-w" = "$synology_warning$"
    "-c" = "$synology_critical$"
  }
}
```
