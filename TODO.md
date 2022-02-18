# TODO

* Save learn state in JSON: easier to check and tweak manually.
* Env var to configure how long MMM waits before accepting an input.
* Second container with an HTTP server showing the learn state. Allow to clear
  the learn state. Enable the device public URL.
* Challenge mode: MMM asks for something in morse, user replies in morse.
    * Antonym of words (yes/no, up/down, left/right, etc)
    * Color of things (sky, coal, snow... though colors are almost always
      ambiguous).
    * The speed MMM plays the morse is adjustable with an env var.
