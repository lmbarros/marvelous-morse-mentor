import time
from grove.grove_led import GroveLed

def main():
    bluePin = 5
    greenPin = 16

    blueLED = GroveLed(bluePin)
    greenLED = GroveLed(greenPin)

    while True:
        blueLED.on()
        greenLED.off()
        time.sleep(1.5)
        blueLED.off()
        greenLED.on()
        time.sleep(0.15)


if __name__ == '__main__':
    main()
