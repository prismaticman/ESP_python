import bluetooth
from machine import UART

# 初始化UART串口
uart = UART(0, baudrate=9600)

# 初始化蓝牙设备
bluetooth.start_scan(5)
while True:
    adv = bluetooth.get_adv()
    if adv and bluetooth.resolve_adv_data(adv.data, bluetooth.ADV_NAME_CMPL) == 'MyDevice':
        addr_type, addr = adv.addr_type, adv.addr
        break

# 连接蓝牙设备
bluetooth.connect(addr)

# 循环发送数据到蓝牙设备
while True:
    data = uart.readline()
    if data:
        bluetooth.send(data)