################################################################################
## author:xiao
## date:2023/1/18
################################################################################

import network
from socket import *

wlan = network.WLAN(network.STA_IF)#创建工作站界面 STA传输模式
wlan.active(True)                  #激活界面
wlan.scan()                        #扫描接入点
wlan.isconnected()                 #检查工作站是否已连接到 AP
wlan.connect('HUAWEI-004OB1','1q2w3e4r5t6y7u8i9o0p')#连接到接入点
wlan.config('mac')                 #获取接口的 MAC 地址
wlan.ifconfig()                    #获取接口的 IP/网络掩码/GW/DNS 地址

# 网络连接函数
# def do_connect():
#     import network
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     if not wlan.isconnected():
#         print('connecting to network...')
#         wlan.connect('HUAWEI-004OB1', '1q2w3e4r5t6y7u8i9o0p')
#         while not wlan.isconnected():
#             pass
#     print('network config:', wlan.ifconfig())


# # 1. 创建udp套接字
# udp_socket = socket(AF_INET, SOCK_DGRAM)

# # 2. 准备接收方的地址
# dest_addr = ('192.168.3.56', 8000)

# # 3. 从键盘获取数据
# send_data = "hello world to pc"

# # 4. 发送数据到指定的电脑上
# udp_socket.sendto(send_data.encode('utf-8'), dest_addr)

# # 5. 从指定的电脑上接收数据
# recv_data = udp_socket.recvfrom(1024)

# # 6. 打印数据
# print(recv_data)

# # 7. 关闭套接字
# udp_socket.close()

