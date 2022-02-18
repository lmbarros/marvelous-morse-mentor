#
# Marvelous Morse Mentor
# Copyright 2021-2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

import random

to_morse = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}


# These are all symbols MMM knows, sorted by the learning priority: symbols
# first on the list are assumed to be more important to learn than those that
# appear later. This is based on the frequency of occurrence in the English
# language, with some tweaks.
symbols_by_learning_order = [
    # First the vowels
    "A", "E", "I", "O", "U",

    # Then the numbers
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",

    # Then the consonants, by frequency of occurrence in English
    "R", "T", "N", "S", "L", "C", "D", "P", "M", "H", "G",
    "B", "F", "Y", "W", "K", "V", "X", "Z", "J", "Q",
]

def random_symbol():
    """ Returns a tuple like ("V", "...-").
    """
    symbol = random.choice(list(to_morse.keys()))
    return (symbol, to_morse[symbol])


def grade(morse_code, inputs):
    """Grades how well the `inputs` represents the expected `morse_code`.
    Returns a tuple with three elements. The first is a Boolean telling if we
    consider the input good enough (this is the pass/fail evaluation). The next
    two elements are strings to be show, respectively, in the top and bottom
    lines of the display to give as feedback.
    """
    # Did we get the right number of dits and dahs?
    expected_inputs = len(morse_code) * 2 - 1
    if len(inputs) > expected_inputs:
        return (False, "   Not good!    ", " Extra dit-dahs ")

    if len(inputs) < expected_inputs:
        return (False, "   Not good!    ", "Too few dit-dahs")

    # Check the sequence of dits and dahs. Don't be too critical about timing
    # for now: simply require that every dit is shorter than every dah.
    dit_lengths = [ ]
    longest_dit = 0.0
    dah_lengths = [ ]
    shortest_dah = float("inf")

    i = 0
    for c in morse_code:
        press_length = inputs[i*2]
        if c == ".":
            if press_length > longest_dit:
                longest_dit = press_length
            dit_lengths.append(inputs[i*2])
        else:
            if press_length < shortest_dah:
                shortest_dah = press_length
            dah_lengths.append(inputs[i*2])

        if len(dit_lengths) > 0 and len(dah_lengths) > 0 and  shortest_dah <= longest_dit:
            return (False, "Not Good! Wrong", "dit-dah sequence")

        # For the purposes of timing, spaces count as dits
        if i < len(morse_code)-1:
            dit_lengths.append(inputs[i*2 + 1])

        i += 1

    # Now check the dits and dahs lengths more carefully
    time_unit = (sum(dit_lengths) + sum(dah_lengths)) / (len(dit_lengths) + 3*len(dah_lengths))

    i = 0
    worst_prec = 1.0
    while i < len(inputs):
        prec = 0.0

        # Check the character
        if morse_code[i//2] == ".":
            prec = inputs[i] / time_unit
        else:
            prec = inputs[i] / (3 * time_unit)

        if prec > 1.0:
            prec = 1.0 / prec
        if prec < worst_prec:
            worst_prec = prec

        # Check the space
        if i+1 >= len(inputs):
            break

        prec = inputs[i+1] / time_unit
        if prec > 1.0:
            prec = 1.0 / prec
        if prec < worst_prec:
            worst_prec = prec

        i += 2

    if worst_prec < 0.35:
        return (False, "Not good! Bad", "dit-dahs timing.")
    elif worst_prec < 0.55:
        return (True, "Good! Can better", "dit-dahs timing.")
    elif worst_prec < 0.75:
        return (True, "Good!", "Almost perfect!")
    else:
        return (True, "Great!", "Nailed it!")
