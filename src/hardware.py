#
# Marvelous Morse Menthor
# Copyright 2021 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

from grove.grove_led import GroveLed
from grove.grove_thumb_joystick import GroveThumbJoystick
from grove.factory import Factory


# Pins where hardware is connected.
LED_PIN = 5
BUTTON_PIN = 16
JOYSTICK_PIN = 0

# Other tweakable constants (turn them into environment variables?)
BUZZER_VOLUME=1/50
BUZZER_NOTE=2500


class Hardware:
    """Abstracts everything hardware-related. Makes things simpler to use for
    our needs.
    """

    def __init__(self):
        # LED
        self.led = GroveLed(LED_PIN)

        # Button
        self.button = Factory.getButton("GPIO-HIGH", BUTTON_PIN)
        self.is_button_pressed = self.button.is_pressed()

        # Buzzer
        from mraa import getGpioLookup
        from upm import pyupm_buzzer as upmBuzzer
        mraa_pin = getGpioLookup("GPIO12") # PWM pin always 12 on GrovePi?
        self.buzzer = upmBuzzer.Buzzer(mraa_pin)
        self.buzzer.setVolume(BUZZER_VOLUME)

        # Display
        self.lcd = Factory.getDisplay("JHD1802")

        # Joystick
        self.joystick = GroveThumbJoystick(JOYSTICK_PIN)
        self.joystick_direction = self.get_joystick_direction()


    def process_input(self, sm):
        """Call this periodically to process hardware state and generate input
        events to the `StateManager` passed as `sm`.
        """
        # Button
        new_is_button_pressed = self.button.is_pressed()
        if self.is_button_pressed != new_is_button_pressed:
            if new_is_button_pressed:
                sm.button_pressed()
            else:
                sm.button_released()
        self.is_button_pressed = new_is_button_pressed

        # Joystick
        new_joystick_direction = self.get_joystick_direction()
        if self.joystick_direction == 0 and new_joystick_direction != 0:
            if new_joystick_direction == -1:
                sm.left()
            else:
                sm.right()
        self.joystick_direction = new_joystick_direction


    def start_buzzing(self):
        # Docs say to pass 0 to play forever, but didn't work for me. Tried -1
        # and worked.
        self.buzzer.playSound(BUZZER_NOTE, -1)


    def stop_buzzing(self):
        self.buzzer.stopSound()


    def led_on(self):
        self.led.on()


    def led_off(self):
        self.led.off()


    def clearDisplay(self):
        self.lcd.clear()


    def display(self, top=None, bottom=None):
        """Displays strings top and bottom. If either is None, the correspoding
        line will remain untouched (not erased).
        """
        if top != None:
            self.lcd.setCursor(0, 0)
            self.lcd.write(top + "                ")

        if bottom != None:
            self.lcd.setCursor(1, 0)
            self.lcd.write(bottom + "                ")


    def get_joystick_direction(self):
        """Returns -1 if the joystick is moved to left; +1 if turned to the
        right; and 0 if it is on a neutral position."""
        x, _ = self.joystick.value
        if x < 325:
            return -1
        elif x > 725:
            return 1
        else:
            return 0
