
from multicasting import *
import msgpack

def encoder(data):
	encoded_data=msgpack.packb(data)
	return encoded_data

def decoder(data):
	decoded_data=msgpack.unpackb(data,use_list=True)
	return decoded_data

def send(data):
	mes=encoder(data)
	multicast(timeout).send_mes(mes)
	logging.info("Message successfully sent from EDsend")

def receive_data():
	try:
		recv_data=multicast(timeout).listen2()
		logging.info("encoded data received \n")
	except ConnectingError as c:
		if c.val==3:
			print c.mesg
	
	return decoder(recv_data)


