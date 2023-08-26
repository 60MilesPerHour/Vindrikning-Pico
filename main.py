import network
import socket
import time
from machine import Pin
from machine import UART

def valid_header(d):
    return d[0] == 0x16 and d[1] == 0x11 and d[2] == 0x0B

def get_pm25_reading():
    uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    while True:
        data = uart0.read(32)
        if data and valid_header(data):
            pm25 = (data[5] << 8) | data[6]
            return pm25
        time.sleep(5)

ssid = 'Your_SSID'
password = 'Your_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print('Pico IP address:', wlan.ifconfig()[0])

json_template = """{
    "sensor":"vindriktning",
    "pm25":%s
}"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

while True:
    cl, addr = s.accept()
    request = str(cl.recv(1024))
    
    if '/reading' in request:
        pm25_value = get_pm25_reading()
        response = json_template % pm25_value
        cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        cl.send(response)
    cl.close()
