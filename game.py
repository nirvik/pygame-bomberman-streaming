import pygame
from pygame.locals import *

import threading
from load import *
import time

grid=[[None,None,None],[None,None,None],[None,None,None]]
XO='X'
winner=None
class tic_tac_toe(threading.Thread):
	def __init__(self):#,condition):
		super(tic_tac_toe,self).__init__()
		self.loading=start()
		#self.condition=condition
		pygame.init()
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

	        global XO,winner
	        if (winner is None):
	                message=XO +"'s turn"
	        else:
	                message=winner + " WON!"
	        print message
	        font=pygame.font.Font(None,24)
	        text=font.render(message,1,(0,0,0))
	        textpos=text.get_rect()
	        self.board.fill((250,250,250),(0,300,300,25))
	        textpos.centerx=self.board.get_rect().centerx
	        self.board.blit(text,textpos)
	        tt.blit(board,(0,0))
	        pygame.display.flip()
	       	time.sleep(1)

	def boardpos(mouseX,mouseY):
	        if (mouseY<100):
	                row=0
	        elif mouseY<200:
	                row=1
	        else: row=2
	
	        if mouseX < 100:
	                col=0
	        elif mouseX < 200:
       		        col=1
       	 	else: col=2

        	return (col,row)
	def draw_piece(board,row,col,piece):
	        centerX=(row*100)+50
	        centerY=(col*100)+50
	        if piece=='X':
	                pygame.draw.line(board,(0,0,0),(centerX-22,centerY-22),(centerX+22,centerY+22),2)
	                pygame.draw.line(board,(0,0,0),(centerX-22,centerY+22),(centerX+22,centerY-22),2)
	        else:
	                pygame.draw.circle(board,(0,0,0),(centerX,centerY),44,2)
	
	        grid[col][row]=piece

	def clickboard(board):
	        global grid,XO
       		(mouseX,mouseY)=pygame.mouse.get_pos()
        	(col,row)=boardpos(mouseY,mouseX)
        	if (grid[row][col]=='X' or grid[row][col]=='O'):
        	        print 'fuck this error ! create an exception'
        	draw_piece(board,row,col,XO)
        	if XO=='X':
        	        XO='O'
        	else: XO='X'


	def gamewon(board):
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


