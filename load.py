
from EDsend import *
import pygame
from pygame.locals import *
from multicasting import *



class start(multicast):

	def __init__(self):
		super(start,self).__init__(timeout)	
		self.stream_message=[]
		try:
			self.discover_bcast_mesg()
		except ConnectingError as c:
			logging.info("\n ConnectingError has occured ")
		print "Displaying the Player's uuid and ip "
		for keys in self.players_uids:
			print keys,':',self.players_uid[keys]
		print '****************************************'
		logging.info("Initialising Screen :D")
		pygame.init()
		self.scr=pygame.display.set_mode((700,700))
		pygame.display.set_caption('Project Tic-Tac toe')
		self.load=pygame.image.load('loading.png').convert()
		self.scr.blit(self.load,(0,0))
		pygame.display.flip()
		self.join_game()


	def join_game(self):
		which_player=raw_input('Choose Player name: ')#since all the comps are goint to be together,players can discuss amongst themselves and discuss which player no they want 
		id=which_player[-1]
		string=self.uid+' '+id
		self.players_ids[self.uid]=id
		try:
			self.communication(string)
		except ConnectingError as c:
			if c.val==2:
				print c.mesg
				pass
		self.load=pygame.Surface((700,300))
		self.load=self.load.convert()
		self.load.fill((250,250,250))
		
		#pygame.display.flip()
		self.coordinate1=350
		self.coordinate2=20
		#INITIALISING FONTS ---PYGAME 
		font=pygame.font.Font(None,24)
		
		print 'displaying the uids and player ids\n'
		for keys in self.players_ids:
			print keys,':',self.players_ids[keys]
			text=font.render("{0} is player {1}".format(keys,self.players_ids[keys]),1,(0,0,255))
			textpos=text.get_rect(center=(self.coordinate1,self.coordinate2))
			self.coordinate2+=50
			textpos.centerx=self.load.get_rect().centerx
			self.load.blit(text,textpos)
		
		self.scr.blit(self.load,(0,0))
		pygame.display.flip()
		time.sleep(2)
	
	def __del__(self):
		self.close()
		logging.info("Closing socket")

