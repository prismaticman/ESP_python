################################################################################
## author :xiao
## date   :2023/1/19
## version:1.0
## 远程控制esp8266的led灯
## 将网络调试助手远程主机端口设置为7788字符编码设置为utf-8
################################################################################


import socket
import time
import network
import machine

# 网络连接函数
def do_connect():
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('HUAWEI-004OB1', '1q2w3e4r5t6y7u8i9o0p')
        while not wlan.isconnected():
            print("connecting...")
            time.sleep(0.75)
    print('network config:', wlan.ifconfig())

#启动网络功能（UDP）连接准备
def creat_udp_soket():
    #创建套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #绑定一个端口
    udp_socket.bind(("0.0.0.0",7788))
    #返回套接字
    return udp_socket



def main():
    # 1. 链接wifi
    do_connect()
    # 2. 创建UDP
    udp_socket = creat_udp_soket()
    # 3. 创建灯对象
    led = machine.Pin(2,machine.Pin.OUT)

    
    while True:
        #等待接收
        recv_data,sender_info = udp_socket.recvfrom(1024)
        #pc发送的数据是
        print("{}send data is:{}".format(sender_info,recv_data))
        #指定的编码格式解码字符串
        recv_data_str = recv_data.decode("utf-8")
        #解码的字符串是
        print("decode data is:{}".format(recv_data_str))
        #异常检测，并打印
        try:
            print(recv_data_str)
        except Exception as ret:
            print("error:", ret)
        #判断灯的亮灭
        if recv_data_str == "off":
            led.value(1)

        elif recv_data_str == "on":
            led.value(0)
        

#这相当于主函数
if __name__ == "__main__":
    main()

