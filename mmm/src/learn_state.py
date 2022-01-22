#
# Marvelous Morse Mentor
# Copyright 2021-2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import pickle
import time
import random

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
    current_symbol = "" # the symbol currently being learned
    morse_code = "" # what the user is expected to send
    learn_state = None

    def on_enter(self, hw):
        self.last_tick_time = self.last_input_time = time.time()
        self.transition_to_helloing(hw)
        self.learn_state = load_learn_state()


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
        s, m = next_symbol_to_learn(self.learn_state)
        hw.display("       %s       " % s, "    Send it!    ")
        self.morse_code = m
        self.current_symbol = s


    def transition_to_feedbacking(self, hw):
        self.state = STATE_FEEDBACKING
        self.secs_till_timeout = 3.5
        ok, top, bottom = morse.grade(self.morse_code, self.inputs)
        if ok:
            hw.display("Good job! '%s' is" % self.current_symbol,
                       "  %s" % self.morse_code)
            self.learn_state[self.current_symbol] *= 2
            if self.learn_state[self.current_symbol] >= 64:
                add_symbol_to_learning_set(self.learn_state)
                clean_up_learning_set(self.learn_state)
        else:
            hw.display("No! '%s' is " % self.current_symbol,
                       "  %s" % self.morse_code)
            self.learn_state[self.current_symbol] = 1

        save_learn_state(self.learn_state)


    def transition_to_helloing(self, hw):
        self.state = STATE_HELLOING
        self.secs_till_timeout = 2.5
        hw.display("     Learn      ", "      Mode      ")


    def transition_to_goodbying(self, hw, top, bottom):
        self.state = STATE_GOODBYING
        self.secs_till_timeout = 4.0
        hw.display(top, bottom)



def next_symbol_to_learn(ls):
    """Returns the next symbol to learn. This always returns characters from the
    training set, within those, gives higher probability to symbols the user
    doesn't know very well yet. `ls` is the learn state. Returns a tuple like
    ("V", "...-")
    """
    total = 0.0
    candidates = [ ]
    for k in ls["learning_set"]:
        weight = 1.0/ls[k]
        total += weight
        candidates.append((k, weight))

    r = random.uniform(0.0, total)
    sum = 0.0
    for c in candidates:
        symbol = c[0]
        weight = c[1]
        sum += weight
        if r <= sum:
            return (symbol, morse.to_morse[symbol])
    print("Ooops, should have selected a candidate symbol")


def add_symbol_to_learning_set(ls):
    """Adds a new random symbol to the learning set.
    """
    for s in morse.symbols_by_learning_order:
        if not is_in_learning_set(s, ls):
            ls["learning_set"][s] = True
            return


def is_in_learning_set(symbol, ls):
    return symbol in ls["learning_set"]


def clean_up_learning_set(ls):
    """Removes from the learning set symbols that have a too low score -- but
    only if we have too many symbols with a low score.
    """
    removable_symbols = [ ]
    for s in ls["learning_set"]:
        if ls[s] == 1.0:
            removable_symbols.append(s)

    while len(removable_symbols) > 5:
        s = removable_symbols.pop()
        del(ls["learning_set"][s])


def blank_learn_state():
    """Creates a blank learn state, usable when there isn't one saved already.
    It's a dictionary mapping each possible character to a number telling how
    well that character is known. Minimum is 1.
    """
    state = { }
    for k in morse.to_morse:
        state[k] = 1.0

    # We'll always take characters from this set. New characters are added to
    # the learning set as the user masters the old ones.]
    state["learning_set"] = { "A": True, "E": True, "I": True, "O": True, "U": True }
    return state


def save_learn_state(ls):
    """Saves the learn state.
    """
    with open("/data/learn-state.pkl", "wb") as f:
        pickle.dump(ls, f)


def load_learn_state():
    """Loads the learn state, create a brand new one if not create yet.
    """
    try:
        with open("/data/learn-state.pkl", "rb") as f:
            return pickle.load(f)
    except IOError:
        print("Creating new learn state")
        return blank_learn_state()
    except EOFError:
        print("Error reading learn state, creating new one")
        return blank_learn_state()
