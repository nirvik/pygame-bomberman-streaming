#!/usr/bin/python
import socket as sck
from struct import pack
import sys
mcast_grp=('224.4.28.87',500) # tupule consisting of multicast ip and port no
message='hey ... waiting for response....'#the message to be sent
x=sck.socket(sck.AF_INET,sck.SOCK_DGRAM) #creating socket AF_INET family :- socket datagram
sck.settimeout(0.1)
time=pack('b',1) #pack 1 in the given format and control no of networks which will recieve the packet
x.setsockopt(sck.IPPROTO_IP,sck.IP_MULTICAST_TTL,ttl)# setting up socket options..
try:
	print 'sending message  ',message
	sent=x.sendto(message,mcast_grp) #send message to the multicast ip
	while 1:
		print 'waiting for responses'
		try:
			data,server=x.recvfrom(16)
			#print 'connection received from ',server
		except sck.timeout:
			print 'time exceeded..closing socket'
			x.close()
			sys.exit(0)
		else :
			print 'received a message : {0} from {1}'.format(data,server) 
finally:
	print 'closing socket!'
	x.close()

