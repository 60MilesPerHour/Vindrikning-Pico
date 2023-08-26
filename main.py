import network
import socket
import time
from machine import Pin
from machine import UART

measurements = [0, 0, 0, 0, 0]
measurement_idx = 0

def valid_header(d):
    headerValid = (d[0] == 0x16 and d[1] == 0x11 and d[2] == 0x0B)
    return headerValid

led = Pin(2, Pin.OUT)  # ESP32 usually has a built-in LED on GPIO 2
led.on()

# Configure UART
uart0 = UART(1, baudrate=9600, tx=17, rx=16)  # tx/rx pins can change based on your connection

ssid = 'Your_SSID'
password = 'Your_Password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError('Network connection failed.')
else:
    print('ESP32 IP address:', wlan.ifconfig()[0])

json = """{
"sensor":"vindriktning",
"pm25":%s
}
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

led.off()

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)

        request = str(request)
        reading = request.find('/reading')
        stateis = "ERROR"

        if reading == 6:
            led.on()

            v = False
            while not v:
                data = uart0.read(32)
                if data:
                    v = valid_header(data)

            pm25 = (data[5] << 8) | data[6]
            measurements[measurement_idx] = pm25
            measurement_idx = (measurement_idx + 1) % 5

        stateis = str(sum(measurements) / len(measurements))  # Calculate the average
        response = json % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        cl.send(response)
        cl.close()
        led.off()

    except OSError as e:
        cl.close()
