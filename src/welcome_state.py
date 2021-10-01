#
# Marvelous Morse Menthor
# Copyright 2021 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import state_manager

class WelcomeState(state_manager.State):
    def on_enter(self, hw):
        hw.display("Marvelous Morse",
                   "     Mentor")


    def on_button_pressed(self, hw):
        hw.startBuzzing()
        hw.ledOn()


    def on_button_released(self, hw):
        hw.stopBuzzing()
        hw.led.off()


    def on_left(self, hw):
        hw.display("<")


    def on_right(self, hw):
        hw.display(">")
