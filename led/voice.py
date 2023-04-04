#import json
#import requests

#sess = requests.get('https://api.ownthink.com/bot?spoken=为什么')

#answer = sess.text

#answer = json.loads(answer)

#print(answer)
from machine import Pin, SPI
import socket
import time
import network
import machine
import urequests


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('HiWiFi_B5CCD4','88888888')
        while not wlan.isconnected():
            print("connecting...")
            time.sleep(0.75)
    print('network config:', wlan.ifconfig())
do_connect()
response0 = urequests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=天气好！')
parsed0 = response0.json()
print(parsed0["content"])

response1 = urequests.get('https://api.ownthink.com/bot?spoken=不行')
parsed1 = response1.json()
print(parsed1["data"]["info"]["text"])

