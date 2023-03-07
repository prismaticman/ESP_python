################################################################################
## author :xiao
## date   :2023/1/18
## version:1.0
##实现led呼吸灯
################################################################################

from machine import Pin, PWM
import time


led2 = PWM(Pin(2))
led2.freq(1000)



while True:
    for i in range(0, 1024):
        led2.duty(i)
        time.sleep_ms(1)
        
    for i in range(1023, -1, -1):
        led2.duty(i)
        time.sleep_ms(1)
        