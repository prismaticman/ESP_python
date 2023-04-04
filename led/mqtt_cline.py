import time
from machine import Pin  # ---- 添加 --------
import network
from umqttsimple import MQTTClient


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('HiWiFi_B5CCD4','88888888')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())


def sub_cb(topic, msg): # 回调函数，收到服务器消息后会调用这个函数
    print(topic, msg)
    # ---- 添加 --------
    if topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "on":
        led_pin.value(1)
    elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "off":
        led_pin.value(0)
    # ---- 添加 --------


# 1. 联网
do_connect()

# 2. 创建mqt
c = MQTTClient("umqtt_client", "192.168.199.124")  # 建立一个MQTT客户端
c.set_callback(sub_cb)  # 设置回调函数
c.connect()  # 建立连接
c.subscribe(b"ledctl")  # 监控ledctl这个通道，接收控制命令

# ---- 添加 --------
# 3. 创建LED对应Pin对象
led_pin = Pin(2, Pin.OUT)
# ---- 添加 --------

while True:
    c.check_msg()
    time.sleep(1)
