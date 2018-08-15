#This plugin will read the temperature and humidity values from your sensor (dht11, dht22, 3202) and return it in readable format for tools like icinga oder nagios including perfdata for visualization.
#This check plugin needs the adafruit dht library available on: https://github.com/adafruit/Adafruit_Python_DHT.git

import sys
import argparse
import Adafruit_DHT

AUTHOR = "Frederic Werner"
VERSION = 1.0

parser = argparse.ArgumentParser()
parser.add_argument("model", help="the sensor model you use [11|22|3202]", type=int, choices=[11, 22, 3202])
parser.add_argument("gpio", help="the gpio pin number you are using", type=int)
parser.add_argument("-wt", help="warning value for temperature", type=int)
parser.add_argument("-ct", help="critical value for temperature", type=int)
parser.add_argument("-wh", help="warning value for humidity", type=int)
parser.add_argument("-ch", help="warning value for humidity", type=int)
args = parser.parse_args()

model = args.model
gpio = args.gpio
wt = args.wt
ct = args.ct
wh = args.wh
ch = args.ch

state = "OK"

humidity, temperature = Adafruit_DHT.read_retry(model, gpio)

if wt and wt < temperature:
    state = "WARNING"
if wh and wh < humidity:
    state = "WARNING"
if ct and ct < temperature:
    state = "CRITICAL"
if ch and ch < humidity:
    state = "CRITICAL"

print '%s - ' % state + 'Temperature: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity), '| temperature={0:0.1f}c'.format(temperature), 'humidity=%d' % humidity + '%'
