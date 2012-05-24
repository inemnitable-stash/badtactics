import sys, pygame, gameobjects
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)

class gameState:
    def __init__(self):
        self.stack = [topMenu()]
    
    def pushState(self, state, displayprev = False):
        self.stack[-1].display = displayprev
        self.stack.append(state)
    
    def popState(self):
        self.stack.pop()
        self.stack[-1].display = True
    
    def top(self):
        return self.stack[-1]
        
class topMenu:
    def __init__(self):
        self.display = True
        self.font = pygame.font.SysFont("sans", 15)
        self.options = ["New Game", "Continue", "Quit"]
        self.cursor = gameobjects.menuCursor(len(self.options))
        
    def processInput(self, event, state): #only keypresses
        if event.key in (K_UP, K_DOWN):
            self.cursor.move(event.key)
        elif event.key == K_z:
            self.selectOption(state)
    
    def selectOption(self, state):
        if self.cursor.location == 0:
            state.pushState(newGame())
        elif self.cursor.location == 1:
            print("Under Construction")
        elif self.cursor.location == 2:
            pygame.quit()
            sys.exit()
            
    def draw(self, gameWindow):
        if self.display:
            gameWindow.fill(black)
            gameWindow.blit(self.cursor.image, (335, 294 + 18 * self.cursor.location))
            for index, option in enumerate(self.options):
                gameWindow.blit(self.font.render(option, False, white, black), (350, 293 + 18 * index))
            
class newGame:
    def __init__(self):
        self.display = True
        self.font = pygame.font.SysFont("sans", 70)
    
    def draw(self, gameWindow):
        if self.display:
            size1 = self.font.size("Epic")
            size2 = self.font.size("Maneuvers")
            gameWindow.fill((0,0,0))
            gameWindow.blit(self.font.render("Epic", True, white, black), (400 - size1[0]/2, 300 - size1[1]))
            gameWindow.blit(self.font.render("Maneuvers", True, white, black), (400 - size2[0]/2, 300))
        
    def processInput(self, event, state):
        if event.key == K_z:
            state.popState()
            state.pushState(gameMap(9, 9))
            
class gameMap:
    def __init__(self, x, y):
        self.display = True
        self.terrain = gameobjects.terrainObj()
        self.size = (x, y)
        self.currdisp = [0, 0]
        self.cursor = gameobjects.gameCursor(self.size, self)
        self.terrain.occupant[(9, 7)] = gameobjects.characterObj("suddenblades", "player", 0)
        self.terrain.occupant[(0, 3)] = gameobjects.characterObj("XmasAgain", "enemy", 1)
        self.terrain.occupant[(0, 5)] = gameobjects.characterObj("slashdown", "enemy", 0)
        self.faction = "player"
    
    def draw(self, gameWindow):
        if self.display:
            gameWindow.fill((0,0,0))
            for x in xrange(0,702,100):
                pygame.draw.line(gameWindow, (255,255,255), (x,0), (x,600))
            for y in xrange(0,502,100):
                pygame.draw.line(gameWindow, (255,255,255), (0,y), (800,y))
            for location, occupant in self.terrain.occupant.iteritems():
                if occupant and 0 <= location[0] - self.currdisp[0] < 8 and 0 <= location[1] - self.currdisp[1] < 6:
                    gameWindow.blit(occupant.image, tuple(100 * (loc - self.currdisp[i]) + 2 for i, loc in enumerate(location)))
            gameWindow.blit(self.cursor.image, tuple(100 * (loc - self.currdisp[i]) for i, loc in enumerate(self.cursor.location)))
    
    def processInput(self, event, state):
        if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
            self.cursor.move(event.key)
        if event.key == K_z:
            character = self.terrain.occupant[self.cursor.location]
            if character:
                if character.faction == self.faction and character.active:
                    state.pushState(moveChar(self.cursor), True)
                else:
                    # show some character info
                    pass
        if event.key == K_x:
            state.pushState(mapMenu(self.cursor, self.terrain.occupant), True)

class windowedMenu:
    def draw(self, gameWindow):
        dim = self.menuWindow.get_size()
        self.menuWindow.fill(black)
        for start, end in (((1,1), (dim[0]-1, 1)), ((1,1), (1, dim[1]-1)), ((dim[0]-1,1), (dim[0]-1, dim[1]-1)), ((1, dim[1]-1), (dim[0]-1,dim[1]-1))):
            pygame.draw.line(self.menuWindow, white, start, end)
        self.menuWindow.blit(self.menuCursor.image, (3, 4 + 18*self.menuCursor.location))
        for index, option in enumerate(self.options):
            self.menuWindow.blit(self.font.render(option, False, white, black), (20, 3 + 18*index))
        if self.cursor.location[0] - self.cursor.origin.currdisp[0] < 5:
            gameWindow.blit(self.menuWindow, (600,0))
        #print(self.menuWindow)
        else:
            gameWindow.blit(self.menuWindow, (0,0))
                    
class moveChar:
    def __init__(self, cursor):
        self.display = True
        self.cursor = cursor
        self.initloc = cursor.location
        self.character = cursor.origin.terrain.occupant[self.initloc]
    
    def draw(self, gameWindow):
        pass
    
    def processInput(self, event, state):
        if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
            self.cursor.restrictedMove(event.key, self.initloc, self.character.move)
        if event.key == K_z:
        #    self.cursor.origin.terrain.occupant[self.initloc] = None
         #   self.cursor.origin.terrain.occupant[self.cursor.location] = self.character
          #  state.popState()
            if not self.cursor.origin.terrain.occupant[self.cursor.location]:
                state.pushState(moveMenu(self.cursor, self.character, self.initloc), True)
        if event.key == K_x:
            self.cursor.location = self.initloc
            if self.cursor.origin.currdisp:
                pass
            state.popState()

class moveMenu(windowedMenu):
    def __init__(self, cursor, character, initloc):
        self.display = True
        self.cursor = cursor
        self.character = character
        self.initloc = initloc
        self.options = character.actions
        cursor.origin.terrain.occupant[initloc] = None
        cursor.origin.terrain.occupant[cursor.location] = character
        self.font = pygame.font.SysFont("sans", 15)
        self.menuWindow = pygame.Surface((200, 18 * len(self.options) + 6))
        self.menuCursor = gameobjects.menuCursor(len(self.options))
    
    # def draw(self, gameWindow):
    #     if self.display:
    #         dim = self.menuWindow.get_size()
    #         self.menuWindow.fill((0,0,0))
    #         for start, end in (((1,1), (dim[0]-1, 1)), ((1,1), (1, dim[1]-1)), ((dim[0]-1,1), (dim[0]-1, dim[1]-1)), ((1, dim[1]-1), (dim[0]-1,dim[1]-1))):
    #             pygame.draw.line(self.menuWindow, (255,255,255), start, end)
    #         self.menuWindow.blit(self.menuCursor.image, (3, 4 + 18*self.menuCursor.location))
    #         for index, option in enumerate(self.character.actions):
    #             self.menuWindow.blit(self.font.render(option, False, (255,255,255), (0,0,0)), (20, 3 + 18*index))
    #         if self.cursor.location[0] - self.cursor.origin.currdisp[0] < 5:
    #             gameWindow.blit(self.menuWindow, (600,0))
    #         #print(self.menuWindow)
    #         else:
    #            gameWindow.blit(self.menuWindow, (0,0))
    
    def processInput(self, event, state):
        if event.key in (K_UP, K_DOWN):
            self.menuCursor.move(event.key)
        if event.key == K_x:
            self.cursor.origin.terrain.occupant[self.cursor.location] = None
            self.cursor.origin.terrain.occupant[self.initloc] = self.character
            state.popState()
        if event.key == K_z:
            if self.options[self.menuCursor.location] == "Attack":
                state.pushState(attackMenu())
            elif self.options[self.menuCursor.location] == "Wait":
                self.character.active = False
                state.popState()
                state.popState()

class mapMenu(windowedMenu):
    def __init__(self, cursor, characters):
        self.display = True
        self.cursor = cursor
        self.characters = characters
        self.origin = cursor.origin
        self.options = ("End Turn",)
        self.font = pygame.font.SysFont("sans", 15)
        self.menuWindow = pygame.Surface((200, 18 * len(self.options) + 6))
        self.menuCursor = gameobjects.menuCursor(len(self.options))
        
    def processInput(self, event, state):
        if event.key in (K_UP, K_DOWN):
            self.menuCursor.move(event.key)
        if event.key == K_x:
            state.popState()
        if event.key == K_z:
            if self.options[self.menuCursor.location] == "End Turn":
                for character in self.cursor.origin.terrain.occupant.itervalues():
                    if character and not character.active:
                        character.active = True
                if self.origin.faction == "player":
                    self.origin.faction = "enemy"
                elif self.origin.faction == "enemy":
                    self.origin.faction = "player"
            state.popState()