import RPi.GPIO as GPIO
import json
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

data = "12345678,123,2,2025"

try:
    text = input('New data:')
    print("Now place your tag to write")
    reader.write(data)
    print("Written")
finally:
    GPIO.cleanup()


