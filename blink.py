from machine import Pin
import time
led = Pin(2, Pin.OUT)  # LED integrado en muchas DevKit V1
for _ in range(10):
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
print("Blink ok")
