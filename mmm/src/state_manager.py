#
# Marvelous Morse Mentor
# Copyright 2021-2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

class State:
    def push(self, state):
        self.state_manager.push(state)

    def pop(self):
        self.state_manager.pop()

    def on_tick(self, hw):
        pass

    def on_enter(self, hw):
        pass

    def on_left(self, hw):
        pass

    def on_right(self, hw):
        pass

    def on_button_pressed(self, hw):
        pass

    def on_button_released(self, hw):
        pass


class StateManager:
    def __init__(self, hw, initialState):
        self.hw = hw
        self.stack = [initialState]
        initialState.state_manager = self
        initialState.on_enter(self.hw)

    def push(self, state):
        state.state_manager = self
        self.stack.append(state)
        state.on_enter(self.hw)

    def pop(self):
        self.stack.pop()
        self.top().on_enter(self.hw)

    def top(self):
        return self.stack[len(self.stack)-1]

    def tick(self):
        self.top().on_tick(self.hw)

    def left(self):
        self.top().on_left(self.hw)

    def right(self):
        self.top().on_right(self.hw)

    def button_pressed(self):
        self.top().on_button_pressed(self.hw)

    def button_released(self):
        self.top().on_button_released(self.hw)
