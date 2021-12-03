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
