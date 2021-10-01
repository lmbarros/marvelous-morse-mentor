#
# Marvelous Morse Menthor
# Copyright 2021 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import state_manager


class LearnState(state_manager.State):
    def on_enter(self, hw):
        hw.display("   Learn Mode   ",
                   "Not implemented!")


    def on_left(self, hw):
        self.pop()


    def on_right(self, hw):
        self.pop()
