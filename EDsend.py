
import msgpack
import logging

logging.root.setLevel(logging.INFO)
def encoder(data):
	encoded_data=msgpack.packb(data)
	return encoded_data

def decoder(data):
	decoded_data=msgpack.unpackb(data,use_list=True)
	return decoded_data

def encode_data(data):
	mes=encoder(data)
	
	logging.info("Message successfully Encoded")
	return msg
def decode_data():
	#try:
	#	recv_data=multicast(timeout).listen2()
	#	logging.info("encoded data received \n")
	#except ConnectingError as c:
	#	if c.val==3:
	#		print c.mesg
	logging.info("returning Decoded data\n")
	return decoder(recv_data)


