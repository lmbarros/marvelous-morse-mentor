#
# Marvelous Morse Mentor
# Copyright 2021-2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import time
import state_manager
import morse

# The possible substates
STATE_HELLOING="HELLOING"
STATE_LISTENING="LISTENING"
STATE_GOODBYING="GOODBYING"
STATE_FEEDBACKING="FEEDBACKING"


class LearnState(state_manager.State):
    state = STATE_HELLOING
    last_input_time = 0.0
    last_tick_time = 0.0
    secs_till_timeout = 0.0
    secs_since_last_input = 0.0
    inputs = []
    morse_code = "" # what the user is expected to send


    def on_enter(self, hw):
        self.last_tick_time = self.last_input_time = time.time()
        self.transition_to_helloing(hw)


    def on_left(self, hw):
        self.transition_to_goodbying(hw, " Moved Joystick ", "   Leaving...   ")


    def on_right(self, hw):
        self.transition_to_goodbying(hw, " Moved Joystick ", "   Leaving...   ")


    def on_button_pressed(self, hw):
        self.on_button_pressed_or_released(hw, True)


    def on_button_released(self, hw):
        self.on_button_pressed_or_released(hw, False)


    def on_button_pressed_or_released(self, hw, pressed):
        prev_input_time = self.last_input_time
        self.last_input_time = time.time()
        dt = self.last_input_time - prev_input_time

        if self.state != STATE_LISTENING:
            return

        # First interesting time is the length of the first pressed interval
        if len(self.inputs) > 0 or not pressed:
            self.inputs.append(dt)

        if pressed:
            hw.start_buzzing()
            hw.led_on()
        else:
            hw.stop_buzzing()
            hw.led_off()


    def on_tick(self, hw):
        now = time.time()
        dt = now - self.last_tick_time
        self.last_tick_time = now
        self.secs_till_timeout -= dt
        self.secs_since_last_input = time.time() - self.last_input_time

        if self.state == STATE_HELLOING:
            if self.secs_till_timeout <= 0.0:
                self.transition_to_listening(hw)
        elif self.state == STATE_LISTENING:
            if len(self.inputs) > 0 and self.secs_since_last_input > 5.0:
                self.transition_to_feedbacking(hw)
            elif self.secs_since_last_input > 10.0:
                self.transition_to_goodbying(hw, "   Time out!    ", "   Leaving...   ")
                return
        elif self.state == STATE_GOODBYING:
            if self.secs_till_timeout <= 0.0:
                self.pop()
        elif self.state == STATE_FEEDBACKING:
            if self.secs_till_timeout <= 0.0:
                self.transition_to_listening(hw)


    def transition_to_listening(self, hw):
        self.state = STATE_LISTENING
        self.inputs = [ ]
        self.last_input_time = time.time() # fake input
        s, m = morse.random_symbol()
        hw.display("[%s]   %s"  % (s, m), "    Send it!    ")
        self.morse_code = m


    def transition_to_feedbacking(self, hw):
        self.state = STATE_FEEDBACKING
        self.secs_till_timeout = 3.5
        ok, top, bottom = morse.grade(self.morse_code, self.inputs)
        hw.display(top, bottom)


    def transition_to_helloing(self, hw):
        self.state = STATE_HELLOING
        self.secs_till_timeout = 2.5
        hw.display("    Learning    ", "      Mode      ")


    def transition_to_goodbying(self, hw, top, bottom):
        self.state = STATE_GOODBYING
        self.secs_till_timeout = 4.0
        hw.display(top, bottom)
