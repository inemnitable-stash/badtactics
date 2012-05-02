import pygame
from pygame.locals import *
from collections import defaultdict

class menuCursor:
	def __init__(self, numOptions):
		self.image = pygame.image.load('menucursor.png').convert_alpha()
		self.location = 0
		self.maxloc = numOptions - 1
		
	def move(self, direc):
		if direc == K_UP and self.location > 0:
			self.location -= 1
		if direc == K_DOWN and self.location < self.maxloc:
			self.location += 1
				

class gameCursor:
	def __init__(self, size, origin):
		self.image = pygame.image.load('gamecursor.png').convert_alpha()
		self.location = (0, 0)
		self.size = size
		self.origin = origin
	
	def move(self, arrow):
		if arrow == K_UP and self.location[1] > 0:
			self.location = (self.location[0], self.location[1] - 1)
		elif arrow == K_DOWN and self.location[1] < self.size[1]:
			self.location = (self.location[0], self.location[1] + 1)
		elif arrow == K_RIGHT and self.location[0] < self.size[0]:
			self.location = (self.location[0] + 1, self.location[1])
		elif arrow == K_LEFT and self.location[0] > 0:
			self.location = (self.location[0] - 1, self.location[1])
		if self.location[0] > self.origin.currdisp[0] + 7:
			self.origin.currdisp[0] += 1
		elif self.location[0] < self.origin.currdisp[0]:
			self.origin.currdisp[0] -= 1
		elif self.location[1] > self.origin.currdisp[1] + 5:
			self.origin.currdisp[1] += 1
		elif self.location[1] < self.origin.currdisp[1]:
			self.origin.currdisp[1] -= 1
	
	def restrictedMove(self, arrow, start, distance): 
		xdisp = self.location[0] - start[0]
		ydisp = self.location[1] - start[1]
		if arrow == K_UP and self.location[1] > 0 and ydisp > -distance + abs(xdisp):
			self.location = (self.location[0], self.location[1] - 1)
		elif arrow == K_DOWN and self.location[1] < self.size[1] and ydisp < distance - abs(xdisp):
			self.location = (self.location[0], self.location[1] + 1)
		elif arrow == K_RIGHT and self.location[0] < self.size[0] and xdisp < distance - abs(ydisp):
			self.location = (self.location[0] + 1, self.location[1])
		elif arrow == K_LEFT and self.location[0] > 0 and xdisp > -distance + abs(ydisp):
			self.location = (self.location[0] - 1, self.location[1])
		if self.location[0] > self.origin.currdisp[0] + 7:
			self.origin.currdisp[0] += 1
		elif self.location[0] < self.origin.currdisp[0]:
			self.origin.currdisp[0] -= 1
		elif self.location[1] > self.origin.currdisp[1] + 5:
			self.origin.currdisp[1] += 1
		elif self.location[1] < self.origin.currdisp[1]:
			self.origin.currdisp[1] -= 1

class characterObj:
	def __init__(self, name, faction, job):
		#eventually implement something more extensible here
		self.name = name
		self.image = pygame.image.load('.'.join((name, 'gif'))).convert_alpha()
		self.faction = faction
		self.jobID = job
		self.move = (6, 4, 3)[job]
		self.hp = (100, 60, 50)[job]
		self.str = (40, 30, 30)[job]
		self.defense = (20, 20, 20)[job]
		self.actions = ("Attack", "Wait")
	
class terrainObj:
	def __init__(self):
		self.occupant = defaultdict(lambda: None)
	
	def select(self, location):
		self.selection = location
	
	def deselect(self):
		self.selection = None