#
# Marvelous Morse Menthor
# Copyright 2021 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import time
import state_manager
import menu_state


class WelcomeState(state_manager.State):
    def on_enter(self, hw):
        hw.display("Marvelous Morse",
                   "     Mentor")
        self.start_time = time.time()


    def on_tick(self, hw):
        if time.time() - self.start_time >= 2.5:
            self.push(menu_state.MenuState())
