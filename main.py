import sys, pygame, gameobjects, stateEngine
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
gameWindow = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Epic Maneuvers!")
state = stateEngine.gameState()

while True:
    for st in state.stack:
        st.draw(gameWindow)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            state.top().processInput(event, state)
    pygame.display.update()
    fpsClock.tick(30)