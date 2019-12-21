#!/bin/usr/python3
# -*- coding:utf-8 -*-

__version__ = "0.0.1"

import os,warnings,sys
import pygame
from pygame.locals import *

def initialize(screen_l,screen_h):
	#returns pygame object (weird stuff)
	screen_l=pygame.display.Info().current_w
	screen_h=pygame.display.Info().current_h

	if len(sys.argv)>=3:
		screen = pygame.display.set_mode(int(sys.argv[1]),int(sys.argv[2]))
		sys.argv.pop(2);sys.argv.pop(1)
	else:
		screen = pygame.display.set_mode(screen_l,screen_h)
	if len(sys.argv)==2:
		pygame.display.set_caption(sys.argv[1])
	pygame.display.flip()
	return screen


class Graphics():

	"""Graphic handler for all pygame graphicEvents"""

	screen = ()

	def __init__(self):
		
		graphicsAttributes(screen_h = screen_h, screen_l = screen_l , self)

	def __del__(self):
		pygame.quit()
		del self

	#DISPLAY METHODS
	
	def displaySquare(self,coordinates):
		self.screen.blit(self.square, [ int(x*(self.screen)) for x in coordinates])

	def displayActivatable(self,element,displaySet=True):
		elif element.image == None:
			img = pygame.image.load(element.imageAdress).convert()
			img = pygame.transform.scale(img, [ int(x*self.screen_h/60) for x in element.size] )
			element.image = img
		else :
			img = element.image
		if displaySet :
			self.screen.blit(img, [ int(x*self.screen_h/60) for x in element.position])
	
	#background handler
	@property
	def bckg(self):
		return self._bckg

	@bckg.setter
	def bckg(self, adress):
		self._bckg = pygame.image.load(adress).convert()
		self._bckg = pygame.transform.scale(self._bckg, (self.screen_l,self.screen_h))
	
	def displayBackgroundUpdate(self,imageAdress=None,displaySet=True):
		if not imageAdress==None:
			self.bckg = pygame.image.load(imageAdress).convert()
			self.bckg = pygame.transform.scale(self.bckg, (self.screen_l,self.screen_h))
		if displaySet :
			self.screen.blit(self.bckg,(0,0))	

	def generalDisplayUpdate(self):
		pygame.display.flip()

	def __call__(self):
		self.generalDisplayUpdate()

	@property
	def cursor(self):
		return self._cursor

	@cursor.setter
	def cursor(self, ref):
		try : pygame.mouse.set_cursor(*ref)
		except: print("couldn't set cursor : "+str(ref))
		else : print("new cursor set !")

	@cursor.deleter
	def cursor(self):
		pygame.mouse.set_cursor(*self._cursor)

	#GETKEYS/MOUSE

	def getKeys(self):
		#no parameters
		#gives a "quit = true" if the player presses Alt+F4, otherwise gives the pressed keys

		keys_input = []

		all_keys = pygame.key.get_pressed()
		if all_keys[pygame.K_F4] and (all_keys[pygame.K_LALT] or all_keys[pygame.K_RALT]):
			return(True)
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				return(True)
		for k in self.keys_nb:
			if all_keys[k] :
				keys_input.append(self.keys_name[self.keys_nb.index(k)])
		#print(all_keys.index(1))
		
		return keys_input

	def getMouse(self):
		self.leftClick = pygame.mouse.get_pressed()[0]
		self.rightClick = pygame.mouse.get_pressed()[2]
		return pygame.mouse.get_pos()

	def load_image(self,Adr,size):
		img = pygame.image.load(Adr).convert()
		img = pygame.transform.scale(img, [ int(x*self.screen_h/60) for x in size] )
		return img

	def graphicsAttributes():

		if os.name == "posix" :
			self.keys_nb = [273,276,274,275,13,271,27,38,233,34,39]
		elif os.name == "nt" :
			self.keys_nb = [273,276,274,275,13,271,27,49,50,51,52]
		else :
			warnings.warn("{} OS ins't supported for pygame kernel {}".format(os.name, __version__),Warning)
			self.keys_nb = []
		self.keys_name = ["UpARR","LeftARR","DownARR","RightARR","Enter","ENTER","esc","1","2","3","4"]

		self.leftClick = 0
		self.rightClick = 0

		self._cursor = pygame.mouse.get_cursor()
	##### obsolete

	"""
	def drawGrid(self):  #for level_editor.py
		for x in range(1,61):
			pygame.draw.line(self.screen,[125,125,125],(x*self.screen_l/60,0),(x*self.screen_l/60,self.screen_h))
		for y in range(1,61):
			pygame.draw.line(self.screen,[125,125,125],(0,y*self.screen_h/60),(self.screen_l,y*self.screen_h/60))"""


if __name__ == '__main__':
	pygame.init()