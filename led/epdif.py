##
 #  @filename   :   epdif.py
 #  @brief      :   EPD hardware interface implements (GPIO, SPI)
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 10 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 #

from machine import Pin, SPI
import time

# Pin definition
reset_pin         = Pin(2,Pin.OUT)
dc_pin          = Pin(4,Pin.OUT)
cs_pin          = Pin(5,Pin.OUT)
busy_pin        = Pin(0,Pin.IN)

gpio_sck = Pin(18)
gpio_mosi = Pin(23)
gpio_miso = Pin(19)
	
spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=gpio_sck, mosi=gpio_mosi, miso=gpio_miso)

def epd_digital_write(pin, val):
    pin.value(val)

def epd_digital_read(pin):
    return pin.value()

def epd_delay_ms(delaytime):
    time.sleep_ms(delaytime)

def spi_transfer(data):
    spi.write(data)

def epd_init():
	epd_digital_write(cs_pin, 0)
	spi.init(baudrate=200000)
	return 0





