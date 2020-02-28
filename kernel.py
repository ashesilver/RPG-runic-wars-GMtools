#!/bin/usr/python3
# -*- coding:utf-8 -*-

__version__ = "0.0.2"

import os,warnings,sys
import pygame
from pygame.locals import *

__file__ = sys.argv[0]
__system_args__ = sys.argv[1:]
	
class Resolutions():
	"""Main class for all resolutions"""
	screen_h,screen_l = None,None

	def ratio(self, other):
		return [other.screen_l/self.screen_l,other.screen_h/self.screen_h]

	def resize(self, other, currentSize):
		ratios = self.ratio(other)
		return [int(currentSize[0]*ratios[0]),int(currentSize[1]*ratios[1])]

class Customres(Resolutions):
	"""docstring for Customres"""
	def __init__(self, screen_l, screen_h):
		self.screen_h = screen_h
		self.screen_l = screen_l

	def windowDownsize(self):
		self.screen_l = int(self.screen_l - self.screen_l*0.1)
		self.screen_h = int(self.screen_h - self.screen_h*0.1)	


class Graphics(Resolutions):

	"""Graphic handler for all pygame graphicEvents"""
	pygame.init()
	screen = ()
	screen_l = int(pygame.display.Info().current_w*90/100)
	screen_h = int(pygame.display.Info().current_h*90/100)
	clock = pygame.time.Clock()

	def inputSystemTreatment(self):
		self.options = {
			"caption" : "Pygame kernel v"+__version__,
			"resolution" : [Graphics.screen_l,Graphics.screen_h],
			"helper" : "Pygame kernel v{v}\n".format(v=__version__) +
				"options :\n\n-c / --caption : << (use) -c caption >>\n sets a custom name for your pygame window\n" +
				"-r / --resolution : << (use) -r width height >>\n sets a custom resolutions for your pygame window\n" +
				"-i / --icon : << (use) -i filepath >>\n sets a custom icon for your pygame window\n",
			"icon" : None 
		}

		for x in __system_args__:
			if "-c" in x or "--caption" in x :
				self.options["caption"] = __system_args__[__system_args__.index(x)+1]
			if "-r" in x or "--resolution" in x :
				self.options["resolution"] = [int(__system_args__[__system_args__.index(x)+1]),int(__system_args__[__system_args__.index(x)+2])]
			if "-i" in x or "--icon" in x :
				self.options["icon"] = __system_args__[__system_args__.index(x)+1]


	def __init__(self,size=(None,None)):

		#print(sys.argv)

		if size!=(None,None):
			(Graphics.screen_l,Graphics.screen_h) = size
		self.inputSystemTreatment()
		Graphics.screen = pygame.display.set_mode(self.options["resolution"])
		if [Graphics.screen_l,Graphics.screen_h] != self.options["resolution"] :
			Graphics.screen_l = self.options["resolution"][0]
			Graphics.screen_h = self.options["resolution"][1]
		
		"""
		elif len(sys.argv)>=3:
			Graphics.screen_l,Graphics.screen_h=int(sys.argv[2]),int(sys.argv[3])
		
		Graphics.screen = pygame.display.set_mode((self.screen_l,self.screen_h))
		if len(sys.argv)==2:
			pygame.display.set_caption(sys.argv[1])"""

		#pygame.display.flip()

		#print(pygame.display.get_caption())

	def __del__(self):
		pygame.quit()
		del self

	def loadAllAttributes(self):

		if os.name == "posix" :
			self.keys_nb = [273,276,274,275,13,271,27,
				38,233,34,39]
		elif os.name == "nt" :
			self.keys_nb = [273,276,274,275,13,271,27,
				49,50,51,52
			]
		else :
			warnings.warn("{} OS ins't supported for pygame kernel {}".format(os.name, __version__),Warning)
			self.keys_nb = []
		self.keys_name = ["UpARR","LeftARR","DownARR","RightARR","Enter","ENTER","esc",
			"1","2","3","4",
			"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

		self.leftClick = 0
		self.rightClick = 0

		self._cursor = pygame.mouse.get_cursor()

		self.square = pygame.image.load("./img/whitesquare.png").convert()

		self._bckg = None

		self._caption = "pygame kernel" if pygame.display.get_caption()[0]=="pygame window" else sys.argv[1]

	#DISPLAY METHODS
	
	def displaySquare(self,coordinates):
		self.screen.blit(self.square, [ int(x*[self.screen_l,self.screen_h][coordinates.index(x)]) for x in coordinates])

	def displayActivatable(self,element,displaySet=True):
		if element["image"] == None:
			img = pygame.image.load(element["imageAdress"]).convert()
			img = pygame.transform.scale(img, element["size"] )
			element["image"] = img
		else :
			img = element["image"]
		if displaySet :
			self.screen.blit(img, element["position"])
		return element

	def load_image(self,Adr,size):
		return self.displayActivatable({"image":None,"imageAdress":Adr,"size":size},False)["image"]
	
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
		

	def __call__(self, max_framerate=90):
		"""default max FPS set to 90, custom can be passed as arg[0]"""
		self.generalDisplayUpdate()
		Graphics.clock.tick(max_framerate)
		return self.mainloop()

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

	@property
	def caption(self):
		return pygame.display.get_caption()[0]

	@caption.setter
	def caption(self,new):
		pygame.display.set_caption(new)

	@caption.deleter
	def caption(self):
		pygame.display.set_caption(self.options["caption"])

	#GETKEYS/MOUSE

	def mainloop(self):
		all_keys = pygame.key.get_pressed()
		if all_keys[pygame.K_F4] and (all_keys[pygame.K_LALT] or all_keys[pygame.K_RALT]):
			return(True)
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				return(True)

		return False

	def getKeys(self):
		keys_input = []
		all_keys = pygame.key.get_pressed()

		for k in self.keys_nb:
			if all_keys[k] :
				keys_input.append(self.keys_name[self.keys_nb.index(k)])
		print(all_keys.index(1))
		
		return keys_input

	def getMouse(self):
		self.leftClick = pygame.mouse.get_pressed()[0]
		self.rightClick = pygame.mouse.get_pressed()[2]
		return pygame.mouse.get_pos()

	##### obsolete

	"""
	def drawGrid(self):  #for level_editor.py
		for x in range(1,61):
			pygame.draw.line(self.screen,[125,125,125],(x*self.screen_l/60,0),(x*self.screen_l/60,self.screen_h))
		for y in range(1,61):
			pygame.draw.line(self.screen,[125,125,125],(0,y*self.screen_h/60),(self.screen_l,y*self.screen_h/60))"""

class Button(Graphics):
	"""UI clickable elements """
	def __init__(self,pos,size,*imgadr):
		self.zone =[pos,size]
		self.clicked= False
		self.hover=False
		self.imgdata = {
			"base":None,
			"hov":None,
			"onclick":None
		}
		(self.base, self.onclick, self.hov) = imgadr

	@property
	def base(self):
		return self._base

	@base.setter
	def base(self,adress):
		self.imgdata["base"]=self.load_image(adress,self.zone[1])

	@property
	def onclick(self):
		return self._onclick

	@onclick.setter
	def onclick(self,adress):
		self.imgdata["onclick"]=self.load_image(adress,self.zone[1])

	@property
	def hov(self):
		return self._hov
	
	@hov.setter
	def hov(self,adress):
		self.imgdata["hov"]=self.load_image(adress,self.zone[1])
	
	def mouseover(self):
		mp = self.getMouse()
		if (( self.zone[0][0] <= mp[0] and self.zone[0][0]+self.zone[1][0] >= mp[0] ) and ( self.zone[0][1] <= mp[1] and self.zone[0][1]+self.zone[1][1] >= mp[1] )):
			if self.leftClick :
				self.clicked = True
			elif self.clicked and not self.leftClick :
				return True
			else :
				self.hover = True
		else :
			self.hover = False
			self.clicked = False
		return False

	def graphicUpdate(self):
		if self.clicked:
			self.displayActivatable({"image":self.imgdata["onclick"],"position":self.zone[0]})
		elif self.hover:
			self.displayActivatable({"image":self.imgdata["hov"],"position":self.zone[0]})
		else :
			self.displayActivatable({"image":self.imgdata["base"],"position":self.zone[0]})

	def __call__(self):
		self.graphicUpdate()
		return self.mouseover()

class Textzone(Graphics):
	"""docstring for Textzone"""
	def __init__(self, fontsize, coordinates, maxlength = 100, text = "Enter your text here"):
		
		self.fontsize = fontsize
		self.coordinates = coordinates
		self.maxlength = maxlength
		self.textfont = pygame.font.Font(None, self.fontsize)
		self.focused = False
		self.hover = False
		self.text = text

	def write(self, text = None):
		if text == None :
			self.display = self.textfont.render(self.text, True, (0,0,0))
		self.screen.blit(self.display, [self.coordinates[0],self.coordinates[1]+0.1*self.fontsize])

	def input(self):
		pass

	def mouseover(self):
		mp = self.getMouse()
		if (( self.coordinates[0] <= mp[0] and self.coordinates[0]+(self.fontsize+1)*self.maxlength >= mp[0] ) and ( self.coordinates[1] <= mp[1] and self.coordinates[1]+self.fontsize*2 >= mp[1] )):
			if self.leftClick :
				self.focused = True
			else :
				self.hover = True
		elif self.hover :
			self.hover = False
			if self.leftClick :
				self.focused = False

	def graphicUpdate(self):
		pygame.draw.rect(self.screen, (255,255,255),[self.coordinates[0],self.coordinates[1],(self.fontsize+1)*self.maxlength,self.fontsize*1.2])
		self.write()

	def __call__(self):
		self.graphicUpdate()
		self.mouseover()
		#print("focus : {}, hov : {}".format(self.focused,self.hover))
		return self.text
		


if __name__ == '__main__':
	print("kernel can't be launched\nNow searching for exe/bat/main files")
	files = [];path ="./"
	for file in os.listdir(path):
		if ".py" in file :
			print("found {} in {}".format(file,path))
			files.append(path+file)
	for x in files:
		if "main" in x.lower():
			print("Now starting {}".format(x))
			os.system("python {}".format(x))