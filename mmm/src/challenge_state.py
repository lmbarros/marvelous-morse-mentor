#
# Marvelous Morse Mentor
# Copyright 2021-2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import state_manager


class ChallengeState(state_manager.State):
    def on_enter(self, hw):
        hw.display(" Challenge Mode ",
                   "Not implemented!")


    def on_left(self, hw):
        self.pop()


    def on_right(self, hw):
        self.pop()
