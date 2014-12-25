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

![Example layout](https://raw.githubusercontent.com/stdevel/check_gpio_pir/master/example_layout.jpg "Example layout")


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
OK: motion counter (0) beyond threshold (3)
```

Check the sensor with customized thresholds and GPIO pin:
```
# ./check_gpio_pir.py -c 2 -t 30 -i 15
WARNING: 5 motions detected!
```

Check the sensor with enabled debugging and LED flashing:
```
# ./check_gpio_pir.py -dl
DEBUG: {'motionThreshold': 3, 'seconds': 15, 'enableLED': True, 'debug': True, 'ledPIN': 11, 'sensorPIN': 7}
DEBUG: Motion detected!
DEBUG: checks done: 1  - motions: 1
DEBUG: checks done: 2  - motions: 1
DEBUG: checks done: 3  - motions: 1
DEBUG: Motion detected!
DEBUG: checks done: 4  - motions: 2
DEBUG: Motion detected!
DEBUG: checks done: 5  - motions: 3
DEBUG: checks done: 6  - motions: 3
DEBUG: checks done: 7  - motions: 3
DEBUG: Motion detected!
DEBUG: checks done: 8  - motions: 4
DEBUG: checks done: 9  - motions: 4
DEBUG: checks done: 10  - motions: 4
DEBUG: checks done: 11  - motions: 4
DEBUG: checks done: 12  - motions: 4
DEBUG: checks done: 13  - motions: 4
DEBUG: checks done: 14  - motions: 4
DEBUG: checks done: 15  - motions: 4
WARNING: 4 motions detected!
```

Sensor tuning
=============
The most PIR sensors have two potentiometer which control the behavior. The **first** potentiometer control the sensitivity, the **second** sets the time perioid the sensor is triggered in case of recognized motions.
Depending on the motions you want to trigger (*e.g. flashing LEDs*) you need to adjust the potentiometers.
