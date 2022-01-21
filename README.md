# Marvelous Morse Mentor

*Learn some morse code!*

This is a toy project I am creating to learn and explore the features of
[balena](https://balena.io) (disclaimer: I work for balena -- we are encouraged
to have projects like this to experience the platform as an end user).

For the **hardware**, I am using a Raspberry Pi Zero and beginner-friendly Grove
components connected via a [Grove Base Hat for Raspberry Pi
Zero](https://www.seeedstudio.com/Grove-Base-Hat-for-Raspberry-Pi-Zero.html).

The **software** is written in Python using
[grove.py](https://github.com/Seeed-Studio/grove.py), because it seemed to be
the best-supported language for my choice of hardware.

## Hardware connections

This is what I have connected to the Grove Base Hat:

* *I2C port:* a [16x2
  display](https://www.seeedstudio.com/Grove-16x2-LCD-White-on-Blue.html).
* *D16 port:* a [button](https://www.seeedstudio.com/buttons-c-928/Grove-Button.html).
* *D5 port:* a [red LED](https://www.seeedstudio.com/Grove-Red-LED.html).
* *A0 port:* a [thumb
  joystick](https://www.seeedstudio.com/Grove-Thumb-Joystick.html) (admittedly
  not the perfect UI choice, but I wanted to use an analog input to enrich my
  learning experience).
* *PWM port*: a [buzzer](https://www.seeedstudio.com/Grove-Buzzer.html).

## Interesting commits

Here are some commits that show how to use certain balena features.

* [9b53ffb4feb4d053b7ac79a2faf5f39011da1a5d](https://github.com/lmbarros/marvelous-morse-mentor/commit/9b53ffb4feb4d053b7ac79a2faf5f39011da1a5d):
  Convert from a single-container app to a multi-container app. In fact, the app
  remains as a single container, but this shows, *e.g.*, how to configure a
  multi-container app container such that it can access the GPIO.
