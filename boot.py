import micropython
# Auxilia no debugging ao trabalhar com interrupções
micropython.alloc_emergency_exception_buf(100)

try:
    import usocket as socket
except:
    import socket

from machine import Pin, Signal
from time import sleep 
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
print('Aguardando requisições em', station.ifconfig())


led = Pin(2, Pin.OUT)
button = Pin(4, Pin.IN)

def toggleLed(pin):
    print('Interrupção gerada! O valor do botão é', button.value()) 
    if button.value() == 1:
        led.value(not led.value())
        
# Interrupt Request 
button.irq(toggleLed)

def home_page():
    if led.value() == 1:
         led_state = 'On'
    else:
        led_state = 'Off'
    html = """<!DOCTYPE html> <html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css?family=Roboto+Condensed&display=swap" rel="stylesheet"> <title>ESP8266 Dashboard</title><style>html {font-family: 'Roboto Condensed', sans-serif; text-align: center; }h1 {color: indigo;}button {border-radius: 25%;margin-right: 10px;background-color: indigo; color: whitesmoke;border-color: indigo; width: 70px; }.main-card {border: 1px solid grey; border-radius: 25px;padding-top: 2%;padding-bottom: 25px; }p {margin-right: 5px;}.events {display: flex;text-align: left;max-width: device-width; }</style></head><script>async function toggleLed(value) {let url = `led=${value}`; let response = await fetch(url);console.log(await response.message);document.getElementById('led-state').innerHTML = `Led State = ${value.toUpperCase()}`; addEventToHtml('DASHBOARD', document.getElementById('led-state').innerHTML); }async function poll() {let response = await fetch('/poll'); if (response.status == 502) {console.log('Timeout de conexão... :('); await poll(); } else if (response.status != 200) {console.log('Alguma coisa deu errado... -_-'); console.log(response.statustext); } else {let message = await response.json(); console.log('Estado Atual: ' + document.getElementById('led-state').innerHTML); console.log('Estado recebido: ' + message['led_state']); if (message['led_state'] == 0) {if (document.getElementById('led-state').innerHTML == 'Led State = OFF') {addEventToHtml('BOTÃO', 'Led State = ON'); }document.getElementById('led-state').innerHTML = 'Led State = ON'; } else {if (document.getElementById('led-state').innerHTML == 'Led State = ON') {addEventToHtml('BOTÃO', 'Led State = OFF'); }document.getElementById('led-state').innerHTML = 'Led State = OFF'; }await poll(); }}poll(); async function addEventToHtml(source, behaviour) {let p = document.createElement('p'); p.innerHTML = `[${source}] ${behaviour}`; document.getElementById('events-div').appendChild(p); }function clearEventDiv() {document.getElementById('events-div').innerHTML = ''; }</script><body><div class="main-card"><h1>ESP8266 Dashboard</h1><h2 id="led-state">Led State = OFF</h2><button onclick="toggleLed('on')">Ligar</button><button onclick="toggleLed('off')">Desligar</button><button onclick="clearEventDiv()">Limpar</button></div><div class="events" id="events-div"></div></body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

i = 0

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_on = request.find('/led=on')
    led_off = request.find('/led=off')
    poll = request.find('/poll') 
    if led_on != -1:
        print('LED ON')
        response = 'ON'
        led.off()
        conn.send('{"led_state": ' + str(led.value()) + '}') 
    elif led_off != -1:
        print('LED OFF')
        response = 'OFF'
        led.on()
        conn.send('{"led_state": ' + str(led.value()) + '}')
    elif poll != -1:
        conn.send('{"led_state": ' + str(led.value()) + '}')
    else:
        response = home_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
    conn.close()


