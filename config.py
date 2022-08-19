#Sprites and global variables

import pygame as pg
from pygame.locals import *


WINDOW = (1920, 1080)
SURFACE = (480, 270)

SCALE_RATIO = int(WINDOW[0] / SURFACE[0])
game_surface = pg.Surface(SURFACE)


WIN = pg.display.set_mode((WINDOW), HWSURFACE | DOUBLEBUF | RESIZABLE)

pg.display.set_caption("Mörköpeli")
FPS = 60

TILE_SIZE = 8
CHUNK_SIZE = 16
G_CONST = 32
RENDER_DISTANCE = 4
#Paths
WORLD_DIR = 'world'

#load sprites
GRASS = pg.transform.scale(pg.image.load('lib/tiles/grass.png'), (TILE_SIZE,TILE_SIZE)).convert()
DIRT = pg.transform.scale(pg.image.load('lib/tiles/dirt.png'), (TILE_SIZE,TILE_SIZE)).convert()
STONE = pg.transform.scale(pg.image.load('lib/tiles/stone.png'), (TILE_SIZE,TILE_SIZE)).convert()


#BACK_GROUND = pg.transform.scale(pg.image.load('lib/bg.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2)).convert()

BG_1 = pg.image.load('lib/bg/L_1.png')
BG_2 = pg.image.load('lib/bg/L_2.png')
BG_3 = pg.image.load('lib/bg/L_3.png')
BG_4 = pg.image.load('lib/bg/L_4.png')
BG_5 = pg.image.load('lib/bg/L_5.png')

BACK_GROUND = [BG_1, BG_2, BG_3, BG_4,BG_5]

#Animations:
PLAYER_RUN_R = [
pg.transform.scale(pg.image.load('lib/player/run_R_1.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_2.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_3.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_4.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_5.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_6.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_7.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_8.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_R_9.png'), (24, 24))
]


PLAYER_RUN_L = [
pg.transform.scale(pg.image.load('lib/player/run_L_1.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_2.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_3.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_4.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_5.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_6.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_7.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_8.png'), (24, 24)),
pg.transform.scale(pg.image.load('lib/player/run_L_9.png'), (24, 24))
]


scroll = [0,0]
loaded_chunks = {}