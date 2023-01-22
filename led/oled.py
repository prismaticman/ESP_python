################################################################################
## author :xiao
## date   :2023/1/22
## version:1.0
################################################################################

from machine import Pin, I2C
import ssd1306
import framebuf

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.fill(0)
display.text('MicroPython', 40, 0, 1)
display.text('SSD1306', 40, 12, 1)
display.text('OLED 128x64', 40, 24, 1)
display.show()
display.show()