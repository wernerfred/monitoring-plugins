import sys
import argparse
import Adafruit_DHT

parser = argparse.ArgumentParser()
parser.add_argument("model", help="the model you use [11|22|3202]", type=int, choices=[11, 22, 3202])
parser.add_argument("gpio", help="the gpio pin number you are using", type=int)
parser.add_argument("-wt", help="warning for temperature", type=int)
parser.add_argument("-ct", help="critical for temperature", type=int)
parser.add_argument("-wh", help="warning for humidity", type=int)
parser.add_argument("-ch", help="warning for humidity", type=int)
args = parser.parse_args()

model = args.model
gpio = args.gpio
wt = args.wt
ct = args.ct
wh = args.wh
ch = args.ch

state = "OK"

humidity, temperature = Adafruit_DHT.read_retry(model, gpio)

if wt != None:
    if wt < temperature:
        state = "WARNING"
if wh != None:
    if wh < humidity:
        state = "WARNING"
if ct != None:
    if ct < temperature:
        state = "CRITICAL"
if ch != None:
    if ch < humidity:
        state = "CRITICAL"

print '%s - ' % state + 'Temperature: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity), '| temperature={0:0.1f}c'.format(temperature), 'humidity=%d' % humidity + '%'
