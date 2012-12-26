import socket as sck
import logging
import uuid
from identity import *
from constants import *


logging.root.setLevel(logging.INFO)
#random

class ConnectingError(Exception):
	def __init__(self,value,mesg):
		self.val=value
		self.mesg=mesg

	def __str__(self):
		return repr(self.mesg)

class multicast(sck.socket):
    def __init__(self,timeout):
        
        super(multicast,self).__init__(sck.AF_INET,sck.SOCK_DGRAM,sck.IPPROTO_UDP)
        self.setsockopt(sck.IPPROTO_IP,sck.IP_MULTICAST_TTL,2)
        self.setsockopt(sck.SOL_SOCKET,sck.SO_REUSEADDR,1)
        self.setsockopt(sck.SOL_IP, sck.IP_MULTICAST_LOOP, 1)
        self.bind(('',port))
        ip=raw_input("whats ur ip:")
        self.setsockopt(sck.SOL_IP,sck.IP_MULTICAST_IF,sck.inet_aton(ip))
        self.setsockopt(sck.SOL_IP,sck.IP_ADD_MEMBERSHIP,sck.inet_aton(mcast_ip)+sck.inet_aton(ip))
        self.settimeout(timeout)
	self.players_uids={}
	self.uid_id_obj=Identification(ip) #calling the identification object
	self.uid=str(self.uid_id_obj.uid) # coverting the uuid of the player into string format
        logging.info("socket initialised and UUID of player generated:{0}".format(self.uid))
        
    def send_mes(self,mesg):
        self.sendto(mesg,(mcast_ip,port))
        logging.info("BROADCASTING \n")

    def add_peers(self,mesg,conn):
    	
	self.players_uids[(mesg.split()[0])]=conn[0] #adding only the ip
	logging.info("{0} . successfully added to the list".format(mesg.split()[0]))
    
    def listen(self):
    	d=ConnectingError(1,"no response")
        try:
            (data,conn)=self.recvfrom(buff_size)
            print 'got connection from {0}'.format(conn)
            logging.info("connection received")
        
	except sck.timeout:
		raise d
                logging.info("SOCKET TIMED OUT ! therefore no response\n")
      	
	if data.split()[0]==self.uid or data.split()[0] in self.players_uids: #extracting the uuid from the messag
		logging.info("SAME UUID's TRYING TO COMMUNICATE \n")
		raise d
		
	else : 
		self.add_peers(data,conn) 


    def listen2(self):
    	l=ConnectingError(3,"Didnot recieve encoded data")
    	try:
    		data,conn=self.recvfrom(buff_size)
		logging.info("\nGame initialisation! New data")
	except sck.timeout:
		raise l
	return data


    def discover_bcast_mesg(self):
    	a=ConnectingError(2,"exceeded no of tries")
	n=0 #no of attempts
        tries=3
        while 1:
		self.send_mes("{0} . Broadcasting message".format(self.uid))
		if(n>tries):
			raise a
			self.close()
			break
			
		else:
			try:
				self.listen()
				self.close()
				break
			except ConnectingError as c:
				if c.val==1:
					logging.warning("FAILED {0}".format(n+1))
					n+=1
					pass
				else:
					raise c
     
