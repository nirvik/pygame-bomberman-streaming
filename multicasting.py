import socket as sck
import logging
import uuid
from identity import *
from constants import *
import netifaces # A NEW CHANGE -- to get the ip


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
	self.players_uids={}# uuids and ip
	self.players_ids={} # uuids and player id -- ADDITIONAL CHANGES
	self.uid_id_obj=Identification(ip) #calling the identification object
	self.uid=str(self.uid_id_obj.uid) # coverting the uuid of the player into string format
	self.auth_uids=[] #for authenticating players to join the game
        logging.info("socket initialised and UUID of player generated:{0}".format(self.uid))
        
    def send_mes(self,mesg):
        self.sendto(mesg,(mcast_ip,port))
        logging.info("BROADCASTING .{0}".format(mesg))

    def add_players(self,mesg,conn):
    	
	self.players_uids[(mesg.split()[0])]=conn[0] #adding only the ip
	logging.info("{0} . successfully added to the list".format(mesg.split()[0]))
    
    def listen(self): #this listen is for adding players to the list with their uuid
    	d=ConnectingError(1,"no response")
        try:
            (data,conn)=self.recvfrom(buff_size)
            print 'got connection from {0}'.format(conn)
            logging.info("connection received")
        
	except sck.timeout:
		raise d
                logging.info("SOCKET TIMED OUT ! therefore no response\n")
      	
	if data.split()[0]==self.uid or data.split()[0] in self.players_uids: #extracting the uuid from the message
		logging.info("SAME UUID's TRYING TO COMMUNICATE \n")
		raise d
		
	else : 
		self.add_players(data,conn) 


    def listen_decoded_data(self): # listening to all the decoded pygame events...
    	l=ConnectingError(3,"Didnot recieve encoded data")
    	try:
    		data,conn=self.recvfrom(buff_size)
		logging.info("\nGame initialisation! New data")
	except sck.timeout:
		raise l
	return data
   
    def listen_player_id(self): # listening to the player id broadcasted by each player
    				#accordingly the position of the players will be decided
    	j=ConnectingError(5,"not a valid player uuid! cannot connect")
	try:
		data,conn=self.recvfrom(buff_size)
		if data.split()[0] in self.auth_uids: #if the uuid is present in the list
			logging.info("Successfull connection \n")
			mesg=data.split()[1] #extracting the id
			self.players_ids[data.split()[0]]=mesg
			self.auth_uids.remove(data.split()[0])
		else:
			raise j
	except sck.timeout:
		raise ConnectingError(1,"no response")


    def discover_bcast_mesg(self):
    	a=ConnectingError(2,"exceeded no of tries")
	n=0 #no of attempts
        tries=3
        while 1:
		self.send_mes("{0} . Broadcasting message".format(self.uid))
		if(n>tries):
			raise a
			#self.close()
			break
			
		else:
			try:
				self.listen()
				self.close()
			#	break  -------------------Just a test-----------------------
			except ConnectingError as c:
				if c.val==1:
					logging.warning("FAILED {0}".format(n+1))
					n+=1
					pass
				else:
					raise c
    def communication(self,data):
    	
	n=5
    	self.auth_uids=self.players_uids.keys()
	i=0
	while 1:
		self.send_mes(data)
		logging.info("{0} is broadcasting player id:{1} \n".format(self.uid,data.split()[1]))
		if(i>n):
			raise ConnectingError(2,"exceeded no of tries")
			logging.info("exceeded no of tries")
			break
		else:
			try:
				self.listen_player_id() #removing self.auth_uid as param
			except ConnectingError as c:
				if c.val==1:
					logging.warning("Socket timed out..failed attempt {0}".format(i+1))
					i+=1
				elif c.val==5:
					logging.warning("That ip doesnot belong to the ips list")
					i+=1
				
				else :
					raise c
			
    def __del__(self):
	self.close()
	logging.info("Closing sockets")
