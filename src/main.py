import time
from grove.grove_led import GroveLed
from grove.factory import Factory

# Transform this into simple functions, maybe in a separate file, probably using
# a "start buzz/end buzz" interface ('cause that's what I'll need).
class Buzzer():
    def __init__(self):
        from mraa import getGpioLookup
        from upm import pyupm_buzzer as upmBuzzer

        mraa_pin = getGpioLookup("GPIO12") # PWM pin always 12 on Grove?
        self.buzzer = upmBuzzer.Buzzer(mraa_pin)

        self.buzzer.setVolume(1/50)

        print("Initialized buzzer '{}'".format(self.buzzer.name()))


    def play(self, note, time):
        self.buzzer.playSound(note, time)


def main():
    ledPin = 5
    buttonPin = 16
    joyPin = 0

    # LED
    theLED = GroveLed(ledPin)

    # Display
    lcd = Factory.getDisplay("JHD1802")
    rows, cols = lcd.size()
    print("LCD model: {}".format(lcd.name))
    print("LCD type : {} x {}".format(cols, rows))
    lcd.clear()

    # Buzzer
    buzzer = Buzzer()

    counter = 1
    while True:
        theLED.on()
        time.sleep(1.5)

        lcd.setCursor(0, 0)
        lcd.write("Arre!")
        lcd.setCursor(0, cols - 1)
        lcd.write('X')
        lcd.setCursor(rows - 1, 0)
        lcd.write(str(counter))
        counter += 1
        buzzer.play(2500, 500000)

        theLED.off()
        time.sleep(1.5)



if __name__ == '__main__':
    main()
