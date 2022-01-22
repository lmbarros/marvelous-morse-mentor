#
# Marvelous Morse Mentor
# Copyright 2021-2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import state_manager
import challenge_state
import learn_state
import practice_state

class MenuState(state_manager.State):
    def __init__(self):
        self.modes = [ "<     Learn    >", "<   Practice   >", "<   Challenge  >" ]
        self.selected_mode = 0


    def on_enter(self, hw):
        hw.display("   Select mode  ",
                   "")
        self.display_selected_mode(hw)


    def on_button_released(self, hw):
        if self.selected_mode == 0:
            self.push(learn_state.LearnState())
        if self.selected_mode == 1:
            self.push(practice_state.PracticeState())
        elif self.selected_mode == 2:
            self.push(challenge_state.ChallengeState())


    def on_left(self, hw):
        self.selected_mode = (self.selected_mode - 1) % len(self.modes)
        self.display_selected_mode(hw)


    def on_right(self, hw):
        self.selected_mode = (self.selected_mode + 1) % len(self.modes)
        self.display_selected_mode(hw)


    def display_selected_mode(self, hw):
        hw.display(None, self.modes[self.selected_mode])
