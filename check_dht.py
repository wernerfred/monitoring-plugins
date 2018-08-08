#!/usr/bin/python
import sys
import Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(22, 4)
print 'Temperature: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity), '| temperature={0:0.1f}c'.format(temperature), 'humidity=%d' % humidity + '%'
