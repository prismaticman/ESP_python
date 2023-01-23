#无法在vscode打开使用
#请使用Thonny打开并添加ssd1306.py

from machine import Pin, I2C

#OLED=....
i2c = I2C(scl=Pin(5), sda=Pin(4))
from ssd1306 import SSD1306_I2C 
OLED= SSD1306_I2C(128, 64, i2c)

#fonts=....
fonts= {
    0xe9a1b9:
    [0x00,0x01,0x00,0x00,0x3D,0x09,0x09,0x09,0x3D,0x01,0x00,0x00,0x01,0x03,0x00,0x00,
    0x00,0xF8,0x60,0xC0,0xF8,0x08,0x08,0x68,0x68,0x68,0x60,0xD8,0x8C,0x06,0x00,0x00],  # 项
    
    0xe79bae:
    [0x00,0x00,0x0F,0x08,0x08,0x0B,0x08,0x08,0x0B,0x08,0x08,0x08,0x08,0x0F,0x00,0x00,
    0x00,0x00,0xF0,0x10,0x10,0xD0,0x10,0x10,0xD0,0x10,0x10,0x10,0x10,0xF0,0x00,0x00],  # 目
    
    0xe7bd91:
    [0x00,0x00,0x3F,0x20,0x20,0x28,0x25,0x22,0x25,0x28,0x20,0x20,0x20,0x20,0x00,0x00,
    0x00,0x00,0xFC,0x04,0x04,0x8C,0x54,0x24,0x54,0x8C,0x04,0x14,0x1C,0x0C,0x00,0x00],  # 网
}


#函数部分
def chinese(ch_str, x_axis, y_axis): 
   offset_ = 0 
   for k in ch_str: 
       code = 0x00  # 将中文转成16进制编码 
       data_code = k.encode("utf-8")
       code |= data_code[0] << 16
       code |= data_code[1] << 8
       code |= data_code[2]
       byte_data = fonts[code]
       for y in range(0, 16):
           a_ = bin(byte_data[y]).replace('0b', '')
           while len(a_) < 8:
               a_ = '0'+ a_
           b_ = bin(byte_data[y+16]).replace('0b', '')
           while len(b_) < 8:
               b_ = '0'+ b_
           for x in range(0, 8):
               OLED.pixel(x_axis + offset_ + x,    y+y_axis, int(a_[x]))   
               OLED.pixel(x_axis + offset_ + x +8, y+y_axis, int(b_[x]))   
       offset_ += 16

chinese('项目网',16,4) 
OLED.show()
OLED.text('itprojects.cn',0,32)
OLED.show()