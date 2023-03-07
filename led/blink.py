################################################################################
## author :xiao
## date   :2023/1/18
## version:1.0
## 实现led灯的闪烁
################################################################################


import time
from machine import Pin
led = Pin(2, Pin.OUT)
while True:
    led.value(1)
    time.sleep(.5)
    led.value(0)
    time.sleep(.5)