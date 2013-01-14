import pygame
from pygame.locals import *

import threading
from load import *
import time
import socket as sck
import sys

port=8767
grid=[[None,None,None],[None,None,None],[None,None,None]]
XO='X'
OX='X'
winner=None
coordinate1=600
coordinate2=20
begin=0
address=('localhost',port)

class TTTError(Exception):
	def __init__(self,value,mesg):
		self.val=value
		self.mesg=mesg
	
	def __str__(self):
		return repr(self.mesg)

class tic_tac_toe(sck.socket):
	def __init__(self):#,condition):
		super(tic_tac_toe,self).__init__(sck.AF_INET,sck.SOCK_DGRAM)
		logging.info("\nSOCKET DATAGRAM ESTABLISHED\n")
		self.bind(address)
		self.settimeout(10) #setting the timeout
		self.loading=start()
		pygame.init()
		self.send_ip=str(self.loading.players_uids.values()[0])
		print ' HEY WAIT ! THE SENDING IP IS :{0}'.format(self.send_ip)
		self.loading.load=pygame.display.set_mode((700,700))
		pygame.display.set_caption("tic-tac")
		self.board=self.init_board()
		self.showboard(self.loading.load,self.board)
	def init_board(self):
		board=pygame.Surface((300,300))
		board=board.convert()
		board.fill((250,250,250))
		pygame.draw.line(board,(0,0,0),(100,0),(100,300),2)
	        pygame.draw.line(board,(0,0,0),(200,0),(200,300),2)
	        pygame.draw.line(board,(0,0,0),(0,100),(300,100),2)
	        pygame.draw.line(board,(0,0,0),(0,200),(300,200),2)
	        return board
	def showboard(self,tt,board):

	        global XO,winner,coordinate1,coordinate2,OX
	        if (winner is None):
	                message=OX +"'s turn"
	        else:
	                message=winner + " WON!"
	        print message
	        font=pygame.font.Font(None,24)
	        text=font.render(message,1,(0,0,250))
		textpos=text.get_rect(center=(coordinate1,coordinate2))
		coordinate2+=50
       		self.board.fill((250,250,250),(0,300,300,25))
	        textpos.centerx=self.board.get_rect().centerx
	        self.board.blit(text,textpos)
	        tt.blit(board,(0,0))
	        pygame.display.flip()
	       	time.sleep(1)

	def boardpos(self,mouseX,mouseY):
	        if (mouseY<100):
	                self.row=0
	        elif mouseY<200:
	                self.row=1
	        else: self.row=2
	
	        if mouseX < 100:
	                self.col=0
	        elif mouseX < 200:
       		        self.col=1
       	 	else: self.col=2

        	return (self.col,self.row)
	def draw_piece(self,board,row,col,piece):
	        centerX=(row*100)+50
	        centerY=(col*100)+50
	        if piece=='X':
	                pygame.draw.line(self.board,(0,0,0),(centerX-22,centerY-22),(centerX+22,centerY+22),2)
	                pygame.draw.line(self.board,(0,0,0),(centerX-22,centerY+22),(centerX+22,centerY-22),2)
	        else:
	                pygame.draw.circle(self.board,(0,0,0),(centerX,centerY),44,2)
	
	        grid[col][row]=piece

	def clickboard(self,board):
	        global grid,XO,OX
		d=TTTError(1,"SPACE OCCUPIED ALREADY")
       		(mouseX,mouseY)=pygame.mouse.get_pos()
        	(self.col,self.row)=self.boardpos(mouseY,mouseX)
		try:
        		if (grid[self.row][self.col]=='X' or grid[self.row][self.col]=='O'):
        	        	raise d
		except TTTError as t:
			if t.val==1:
				print t.mesg
				self.clickboard(self.board)
        	self.draw_piece(self.board,self.row,self.col,XO)
		if OX=='X':
			OX='O'
		else : OX='X'
		return self.col,self.row


	def gamewon(self,board):
	        global grid,winner
	        val=0
	        for row in range(0,3):
	                if((grid[row][0]==grid[row][1]==grid[row][2]) and grid[row][0] is not None):
	                        logging.info("ROW no. {0} wins".format(row))
	                        winner=grid[row][0]
	                        pygame.draw.line(board,(250,0,0),(0,(row+1)*100-50),(300,(row+1)*100-50),2)
	                        return True
	        for col in range(0,3):
	                if ((grid[0][col]==grid[1][col]==grid[2][col]) and grid[0][col] is not None):
	                        logging.info("COL no. {0} wins".format(col))
	                        winner=grid[0][col]
        	                pygame.draw.line(board,(250,0,0),((col+1)*100-50,0),((col+1)*100-50,300),2)
        	                return True

        	if ((grid[0][0]==grid[1][1]==grid[2][2]) and grid[0][0] is not None):
        	        winner = grid[0][0]
        	        pygame.draw.line (board, (250,0,0), (50, 50), (250, 250), 2)
        	        return True
        	elif ((grid[0][2]==grid[1][1]==grid[2][0]) and grid[0][2] is not None):
        	        winner = grid[0][2]
        	        pygame.draw.line (board, (250,0,0), (250, 50), (50, 250), 2)
        	        return True
	def run(self):
		global begin,XO,port,OX
		XO=self.loading.players_ids[self.loading.uid]
		OX=XO
		running=1
		eve=1
		iterator=1
		while running==1:	#for receiving purpose
			if (XO=='X' and begin!=0) or XO=='O':
				try:
					logging.info("waiting for response!")
					data,conn=self.recvfrom(2048)
					print data
					logging.info("Encoded data received")
					data=decoder(''.join(data.split(':')[1:]))
					if data[0]==1: # 1 stands for the function drawpiece
						self.draw_piece(self.board,data[1],data[2],data[3])
				except sck.timeout as se:
					print '{0} has won the game as oponent couldnt think of a move'.format(XO)
					sys.exit()
					break
			elif XO=='X' and begin==0:
				pass
			self.showboard(self.loading.load,self.board) #showing the opponents move
			#running=1
			iterator=1	
			while eve==1:
				for event in pygame.event.get():
					if event.type is QUIT:
						eve=0
					elif event.type is MOUSEBUTTONDOWN:
						col,row=self.clickboard(self.board)
						data=[1,col,row,XO]
						data=encoder(data)
						data='1:'+data
						print data
						#self.loading.transfer_data('1:'+data)
						self.sendto(data,(self.send_ip,port))

						logging.info("Encoded Info transfered")
						self.showboard(self.loading.load,self.board)
						iterator=0
						break
				if iterator==0:
					break
				
			self.showboard(self.loading.load,self.board)
			begin+=1
			
	def __del__(self):
		self.close()
		logging.info("CLOSING ALL SOCKETS ! Thanks for playing")

