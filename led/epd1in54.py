##
 #  @filename   :   epd1in54.py
 #  @brief      :   Implements for e-paper library
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     September 9 2017
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

import epdif
from machine import Pin, SPI
import ujson
import struct
# Display resolution
EPD_WIDTH       = 200
EPD_HEIGHT      = 200

# EPD1IN54 commands
DRIVER_OUTPUT_CONTROL                       = b'\x01'
BOOSTER_SOFT_START_CONTROL                  = b'\x0C'
GATE_SCAN_START_POSITION                    = b'\x0F'
DEEP_SLEEP_MODE                             = b'\x10'
DATA_ENTRY_MODE_SETTING                     = b'\x11'
SW_RESET                                    = b'\x12'
TEMPERATURE_SENSOR_CONTROL                  = b'\x1A'
MASTER_ACTIVATION                           = b'\x20'
DISPLAY_UPDATE_CONTROL_1                    = b'\x21'
DISPLAY_UPDATE_CONTROL_2                    = b'\x22'
WRITE_RAM                                   = b'\x24'
WRITE_VCOM_REGISTER                         = b'\x2C'
WRITE_LUT_REGISTER                          = b'\x32'
SET_DUMMY_LINE_PERIOD                       = b'\x3A'
SET_GATE_TIME                               = b'\x3B'
BORDER_WAVEFORM_CONTROL                     = b'\x3C'
SET_RAM_X_ADDRESS_START_END_POSITION        = b'\x44'
SET_RAM_Y_ADDRESS_START_END_POSITION        = b'\x45'
SET_RAM_X_ADDRESS_COUNTER                   = b'\x4E'
SET_RAM_Y_ADDRESS_COUNTER                   = b'\x4F'
TERMINATE_FRAME_READ_WRITE                  = b'\xFF'

class EPD :
    def __init__(self):
        self.reset_pin = epdif.reset_pin
        self.dc_pin = epdif.dc_pin
        self.busy_pin = epdif.busy_pin
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.lut = self.lut_full_update

    lut_full_update = [
        0x02, 0x02, 0x01, 0x11, 0x12, 0x12, 0x22, 0x22, 
        0x66, 0x69, 0x69, 0x59, 0x58, 0x99, 0x99, 0x88, 
        0x00, 0x00, 0x00, 0x00, 0xF8, 0xB4, 0x13, 0x51, 
        0x35, 0x51, 0x51, 0x19, 0x01, 0x00
    ]

    lut_partial_update  = [
        0x10, 0x18, 0x18, 0x08, 0x18, 0x18, 0x08, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x13, 0x14, 0x44, 0x12, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]

    def digital_write(self, pin, value):
        epdif.epd_digital_write(pin, value)

    def digital_read(self, pin):
        return epdif.epd_digital_read(pin)

    def delay_ms(self, delaytime):
        epdif.epd_delay_ms(delaytime)

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        # the parameter type is list but not int
        # so use [command] instead of command
        epdif.spi_transfer(command)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        # the parameter type is list but not int
        # so use [data] instead of data
        epdif.spi_transfer(data)

    def init(self, lut):
        if (epdif.epd_init() != 0):
            return -1
        # EPD hardware init start
        self.lut = lut
        self.reset()
        self.send_command(DRIVER_OUTPUT_CONTROL)
        self.send_data(struct.pack("B", (EPD_HEIGHT - 1) & 0xFF))
        self.send_data(struct.pack("B", ((EPD_HEIGHT - 1) >> 8) & 0xFF))
        self.send_data(b'\x00')                     # GD = 0 SM = 0 TB = 0
        self.send_command(BOOSTER_SOFT_START_CONTROL)
        self.send_data(b'\xD7')
        self.send_data(b'\xD6')
        self.send_data(b'\x9D')
        self.send_command(WRITE_VCOM_REGISTER)
        self.send_data(b'\xA8')                     # VCOM 7C
        self.send_command(SET_DUMMY_LINE_PERIOD)
        self.send_data(b'\x1A')                     # 4 dummy lines per gate
        self.send_command(SET_GATE_TIME)
        self.send_data(b'\x08')                     # 2us per line
        self.send_command(DATA_ENTRY_MODE_SETTING)
        self.send_data(b'\x03')                     # X increment Y increment
        self.set_lut(self.lut)		
        # EPD hardware init end
		
        return 0

    def wait_until_idle(self):
        while(self.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            self.delay_ms(100)
##
 #  @brief: module reset.
 #          often used to awaken the module in deep sleep,
 ##
    def reset(self):
        self.digital_write(self.reset_pin, 0)         # module reset
        self.delay_ms(300)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(300)    

##
 #  @brief: set the look-up table register
 ##
    def set_lut(self, lut):
        self.lut = lut
        self.send_command(WRITE_LUT_REGISTER)
        # the length of look-up table is 30 bytes
        for i in range(0, len(lut)):
            self.send_data(struct.pack("B", self.lut[i]))


##
 #  @brief: put an image to the frame memory.
 #          this won't update the display.
 ##
    def set_frame_memory(self, image, image_width,image_height,x, y):
        #if (image == None or x < 0 or y < 0):
        #    return
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        x = x & 0xF8
        image_width = image_width & 0xF8
        if (x + image_width >= self.width):
            x_end = self.width - 1
        else:
            x_end = x + image_width - 1
        if (y + image_height >= self.height):
            y_end = self.height - 1
        else:
            y_end = y + image_height - 1		
        self.set_memory_area(x, y, x_end, y_end)
        self.set_memory_pointer(x, y)
        self.send_command(WRITE_RAM)
        # send the image data
        #pixels = image_monocolor.load()
        byte_to_send = 0x00
        for j in range(0, y_end - y + 1):
            # 1 byte = 8 pixels, steps of i = 8
            for i in range(0, (x_end - x + 1)/8):
				self.send_data(struct.pack("B", image[i+j*(image_width >>3)]))
				#print(i+j*(image_width >>3),struct.pack("B", image[i+j*(image_width >>3)]),image[i+j*(image_width >>3)])
                # Set the bits for the column of pixels at the current position.
                #if pixels[i, j] != 0:
                #    byte_to_send |= 0x80 >> (i % 8)
                #if (i % 8 == 7):
                #    self.send_data(struct.pack("B", byte_to_send))
                #    byte_to_send = 0x00
##
 #  @brief: clear the frame memory with the specified color.
 #          this won't update the display.
 ##
    def clear_frame_memory(self, color):
        self.set_memory_area(0, 0, self.width - 1, self.height - 1)
        self.set_memory_pointer(0, 0)
        self.send_command(WRITE_RAM)
        # send the color data
        for i in range(0, self.width / 8 * self.height):
            self.send_data(struct.pack("B", color))

##
 #  @brief: update the display
 #          there are 2 memory areas embedded in the e-paper display
 #          but once this function is called,
 #          the the next action of SetFrameMemory or ClearFrame will 
 #          set the other memory area.
 ##
    def display_frame(self):
        self.send_command(DISPLAY_UPDATE_CONTROL_2)
        self.send_data(b'\xC4')
        self.send_command(MASTER_ACTIVATION)
        self.send_command(TERMINATE_FRAME_READ_WRITE)
        self.wait_until_idle()

##
 #  @brief: specify the memory area for data R/W
 ##
    def set_memory_area(self, x_start, y_start, x_end, y_end):
        self.send_command(SET_RAM_X_ADDRESS_START_END_POSITION)
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data(struct.pack("B", (x_start >> 3) & 0xFF))
        self.send_data(struct.pack("B", (x_end >> 3) & 0xFF))
        self.send_command(SET_RAM_Y_ADDRESS_START_END_POSITION)
        self.send_data(struct.pack("B", y_start & 0xFF))
        self.send_data(struct.pack("B", (y_start >> 8) & 0xFF))
        self.send_data(struct.pack("B", y_end & 0xFF))
        self.send_data(struct.pack("B", (y_end >> 8) & 0xFF))

##
 #  @brief: specify the start point for data R/W
 ##
    def set_memory_pointer(self, x, y):
        self.send_command(SET_RAM_X_ADDRESS_COUNTER)
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data(struct.pack("B", (x >> 3) & 0xFF))
        self.send_command(SET_RAM_Y_ADDRESS_COUNTER)
        self.send_data(struct.pack("B", y & 0xFF))
        self.send_data(struct.pack("B", (y >> 8) & 0xFF))
        self.wait_until_idle()

##
 #  @brief: After this command is transmitted, the chip would enter the
 #          deep-sleep mode to save power.
 #          The deep sleep mode would return to standby by hardware reset.
 #          You can use reset() to awaken or init() to initialize
 ##
    def sleep(self):
        self.send_command(DEEP_SLEEP_MODE)
        self.wait_until_idle()

### END OF FILE ###

