import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BORD)

GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)

p.start(2.5)

try:
    while True:
        time.sleep(30)
        p.ChangeDutyCycle(7.5)
        time.sleep(10)
        p.ChangeDutyCycle(2.5)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup
