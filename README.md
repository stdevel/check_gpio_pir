check_gpio_pir
==============

``check_gpio_pir``is a Nagios / Icinga plugin written in Python for checking motions recognized by a PIR (passive infrared) sensor connected to a Raspberry Pi via GPIO.
Using this you can generate monitoring notifications for motions captured by the sensor.

Requirements
============
For this plugin you need:
- a Raspberry Pi :-)
- the Python module [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)
- a PIR sensor (*check [eBay](http://www.ebay.com) for this*)
- a breadboard
- a LED for displaying recognized motions (*optional*)

Usage
=====
By default the plugin checks for **15** seconds and returns a **WARNING** if **3** or more motions were detected.

You can use the following parameters to customize the plugin behavior:

| Parameter | Description |
|:----------|:------------|
| ``-d`` / ``--debug`` | enable debugging outputs |
| ``-l`` / ``--enable-led`` | enable LED blinking for motion detection (*default: no*) |
| ``-p`` / ``--led-pin`` | GPIO PIN of debug LED (*default: 11*) |
| ``-i`` / ``--sensor-pin`` | GPIO PIN of PIR sensor (*default: 7*) |
| ``-t`` / ``--seconds`` | threshold in seconds the sensor is read (*default: 15*) |
| ``-c`` / ``--motion-threshold`` | threshold of motions that trigger a warning event (*default: 3*) |

By default the GPIO pins **7** (*PIR sensor*) and **11** (*LED*) are used.

Examples
========
Check the sensor with default parameters (*GPIO PIN 7, 15 second check, motion threshold of 3*):
```
# ./check_gpio_pir.py
```
