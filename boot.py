try:
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import esp

esp.osdebug(None) 

import gc as garbageCollector
garbageCollector.collect()

print('Insira suas credenciais de rede Wi-Fi')
ssid = input('SSID (Nome da rede): ')
password = input('Senha: ')

station = network.WLAN(network.STA_IF)
station.active(True)

while not station.isconnected():
  pass

print('Conexão estabelecida com sucesso!')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
button = Pin(4, Pin.IN)