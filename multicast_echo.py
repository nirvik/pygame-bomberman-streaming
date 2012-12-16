import socket as sck
import logging
mcast_ip='224.23.23.29'
port=9878
timeout=5
buff_size=1024
logging.root.setLevel(logging.INFO)

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
        logging.info("socket initialised ")

    def send_mes(self):
        self.sendto("Broadcasting! looking for peers\n",(mcast_ip,port))
        logging.info("BROADCASTING \n")
    def listen(self):
        d=ConnectingError(1,"no response")
        try:
            (data,conn)=self.recvfrom(buff_size)
            print 'got connection from {0}'.format(conn)
            logging.info("connection received")
        except sck.timeout:
                raise d
                logging.info("SOCKET TIMED OUT ! therefore no response\n")

    def discover_bcast_mesg(self):
        a=ConnectingError(2,"exceeded no of tries")

        n=0 #no of attempts
        tries=3
        while 1:
                self.send_mes()
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
