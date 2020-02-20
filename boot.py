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

print('Insira suas credenciais de rede Wi-Fi:') 
ssid = input('SSID (nome da rede): ') 
password = intpu('Senha: ') 

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

print('Tentando conectar à rede...') 
while station.isconnected() == False:
  pass

print('Conexão estabelecida!')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
button = Pin(4, Pin.IN) 