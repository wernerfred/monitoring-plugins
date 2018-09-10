# monitoring-plugins [![CodeFactor](https://www.codefactor.io/repository/github/wernerfred/monitoring-plugins/badge)](https://www.codefactor.io/repository/github/wernerfred/monitoring-plugins)
In this repository i will get together all check plugins i wrote by myself or i found usefull which are not included in the default ```monitoring-plugins``` you can install via ```apt```. All check plugins will return their results in a readable format for tools like nagios or icinga including perfdata for visualization with tools like grafana or pnp. Feel free to modify the scripts to add more functionality but please keep the [Guidelines](https://blog.netways.de/2015/08/07/monitoring-plug-ins-selbst-gemacht/) in mind. If you don't mind please start a pull request once you have finished so others can profit from your work. 

Keep in mind that i am working on, improving and developing new plugins within this repopsitory so check out the [release section](https://github.com/wernerfred/monitoring-plugins/releases) to use only working versions of my plugins.

## Table of contents
- [![check_dht](https://img.shields.io/badge/check__dht-v.02-green.svg)](#check_dhtpy) 
- [![check_synology](https://img.shields.io/badge/check__synology-v0.2-green.svg)](#check_synologypy)

### check_dht.py
This plugin will read the temperature and humidity values from your sensor (dht11, dht22, 3202).

This check plugin needs the adafruit dht library available on: https://github.com/adafruit/Adafruit_Python_DHT.git

Usage:
```
> python check_dht.py -h
usage: check_dht.py [-h] [-wt WT] [-ct CT] [-wh WH] [-ch CH] {11,22,3202} gpio
```
Example check:
```
> python check_dht.py 22 4 -wt 40 -ch 99
OK - Temperature: 24.6 C  Humidity: 47.7 % | temperature=24.6c humidity=47%
```

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

This plugin uses ```snmpv3``` with ```MD5``` + ```AES``` to check a lot of different values on your Synology DiskStation.

This check plugin needs ```pysnmp``` to be installed on your system. You can install it with: ```pip install pysnmp```

Usage:
```
> python check_synology.py -h
usage: check_synology.py hostname username authkey privkey {mode} [-h] [-w W] [-c C]
```

Example check:
```
> python check_synology.py hostname snmp_user auth_key priv_key load
OK - load average: 1.48, 1.71, 1.74 | load1=1.48c load5=1.71c load15=1.74c
```

Available modes:

| mode    | description                                                                | warning/critical                    |
| :-----: | -------------------------------------------------------------------------- | ----------------------------------- |
| load    | Checks the load1, load5 and load15 values                                  | if more than w/c in int (only load1)|
| memory  | Checks the physical installed memory (free and total)                      | if less free than w/c in %          |
| disk    | Detects and checks all disks (name, status, temperature)                   | if temp higher than w/c in °C <br> if c is set it will also trigger if status <br> is Failure or Crashed                                                             |
| storage | Detects and checks all disks (free, total, %)                              | if more used than w/c in %          |
| update  | Shows the current DSM version and if DSM update is available               | set w/c to any int this triggers: <br> warning if available and critical <br> if other than un-/available                                                           |
| status  | Shows model, s/n, temp and status of system, fan, cpu fan and power supply | if temp higher than w/c in °C       |

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
If you want to add a missing check or another value to be added than you can use the [official Synology MIB Guide](https://global.download.synology.com/download/Document/MIBGuide/Synology_DiskStation_MIB_Guide.pdf) as a hint for the right MIBs / OIDs.
