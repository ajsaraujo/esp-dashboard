def home_page():
	return 'Some nice, well made web page' 

mySocket = socket.socket(socket.AF_IFNET, socket.SOCK_STREAM)
mySocket.bind(('', 80)) 
# Accept up to 5 queued connections 
mySocket.listen(5)

print('O servidor está aguardando requisições...')

while True:
	connection, address = s.accept() 
	print('Obtivemos uma conexão vinda de %s' % str(address)) 
	
	# Receive up to 1024 bytes from the socket
	request = connection.recv(1024) 
	
	led_on = request.find('led=on') 
	led_off = request.find('led=off') 
	poll = request.find('poll') 
	
	content_type = 'Content-Type: application/json' 
	
	response = '' 
	
	if led_on != -1:
		print('LED aceso pelo Dashboard Web!') 
		led.value(1) 
	else if led_off != -1:
		print('LED apagado pelo Dashboard Web!') 
		led.value(0)
	else if poll != -1:
		print('Informações sobre o button requisitadas pelo Client-side...')
		response = '{"led_value": ' + led.value() + '}' 
	else:
		content_type = 'Content-Type: text/html'
		response = home_page() 
	
	connection.send('HTTP/1.1 200 OK\n') 
	connection.send(content_type) 
	connection.send('Connection: close\n\n') 
	connection.sendall(response)
	connection.close() 
		