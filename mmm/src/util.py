#
# Marvelous Morse Mentor
# Copyright 2022 Leandro Motta Barros
# Licensed under the Apache License 2.0 (see the LICENSE file for details)
#

# Yes, we have the dreaded "util" module!

import os

DEFAULT_INPUT_TIMEOUT_SECS = 10.0

cached_input_timeout_secs = None

def input_timeout_secs():
    """Returns the timeout, in seconds, after which we give up on receiving user
    input.
    """
    global cached_input_timeout_secs
    if cached_input_timeout_secs is None:
        try:
            cached_input_timeout_secs = float(os.environ['MMM_INPUT_TIMEOUT_SECS'])
            print("Using input timeout from the environment:", cached_input_timeout_secs)
        except Exception as err:
            cached_input_timeout_secs = DEFAULT_INPUT_TIMEOUT_SECS
            print("Using default input timeout because:", repr(err))

    return cached_input_timeout_secs
