
from EDsend import *
import pygame
from pygame.locals import *
from multicasting import *


class start(multicast):

	def __init__(self):
		super(self,start).__init__(timeout)	
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
		pygame.display.set_caption('Project Bomberman')
		load=pygame.image.load('loading.png').convert()
		self.scr.blit(load,(0,0))
		pygame.display.flip()
		self.join_game()


	def join_game(self):
		print 'for the options input like this :p1 (if opt=P1) '
		which_player=raw_input('Choose Player \n p1 \n p2 \n p3 \n p4:')
		id=which_player[-1]
		string=self.uid+' '+id
		self.players_uids[self.uid]=id
		self.communication(string)
		print 'displaying the uids and player ids\n'
		for keys in self.players_ids:
			print keys,':',self.players_ids[keys]	
	
