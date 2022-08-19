

import pygame as pg
import numpy as np
from pygame.locals import *
from generator import make_a_chunk

#Globall stuff
WINDOW = (600, 600)
WIN = pg.display.set_mode((WINDOW), HWSURFACE | DOUBLEBUF | RESIZABLE)
pg.display.set_caption("Mörköpeli")
FPS = 60


#load sprites
GRASS = pg.transform.scale(pg.image.load('lib/tiles/grass.png'), (16,16)).convert()
DIRT = pg.transform.scale(pg.image.load('lib/tiles/dirt.png'), (16,16)).convert()
STONE = pg.transform.scale(pg.image.load('lib/tiles/stone.png'), (16,16)).convert()


#BACK_GROUND = pg.transform.scale(pg.image.load('lib/bg.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2)).convert()

BG_1 = pg.transform.scale(pg.image.load('lib/bg/L_1.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2))
BG_2 = pg.transform.scale(pg.image.load('lib/bg/L_2.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2))
BG_3 = pg.transform.scale(pg.image.load('lib/bg/L_3.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2))
BG_4 = pg.transform.scale(pg.image.load('lib/bg/L_4.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2))
BG_5 = pg.transform.scale(pg.image.load('lib/bg/L_5.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2)).convert()

BACK_GROUND = [BG_1, BG_2, BG_3, BG_4,BG_5]

#Animations:
PLAYER_RUN_R = [
(pg.image.load('lib/player/run_R_1.png')),
(pg.image.load('lib/player/run_R_2.png')),
(pg.image.load('lib/player/run_R_3.png')),
(pg.image.load('lib/player/run_R_4.png')),
(pg.image.load('lib/player/run_R_5.png')),
(pg.image.load('lib/player/run_R_6.png')),
(pg.image.load('lib/player/run_R_7.png')),
(pg.image.load('lib/player/run_R_8.png')),
(pg.image.load('lib/player/run_R_9.png'))
]


PLAYER_RUN_L = [
(pg.image.load('lib/player/run_L_1.png')),
(pg.image.load('lib/player/run_L_2.png')),
(pg.image.load('lib/player/run_L_3.png')),
(pg.image.load('lib/player/run_L_4.png')),
(pg.image.load('lib/player/run_L_5.png')),
(pg.image.load('lib/player/run_L_6.png')),
(pg.image.load('lib/player/run_L_7.png')),
(pg.image.load('lib/player/run_L_8.png')),
(pg.image.load('lib/player/run_L_9.png'))
]


#Config
TILE_SIZE = 16
CHUNK_SIZE = 16
G_CONST = 32
RENDER_DISTANCE = 5

#Paths
WORLD_DIR = 'world'

#scroll on x and y axies
scroll = [0,0]

loaded_chunks = {}
     


def collision_test(rect, loaded_chunks):
    for key, val in loaded_chunks.items():
        chunk = val
        
        for block in chunk.blocks.values():

            #Make a rect from the tile
            block_rect = block.rect
                                                             
            if rect.colliderect(block_rect):
                return True



class chunk(object):

    #chunk object that is 16 blocks long
    def __init__(self, data, index):
        self.index = index
        self.data = data
        print 

        #dictionary
        self.blocks = self.init_blocks()


    def init_blocks(self):
        blocks = {}
        for key, value in self.data.items():
            #Append block object to block list
            
            block = Block(pos = key, id = value)
            
            blocks[key] = block

        return blocks


    def remove_block(self, pos):
        block_to_break = self.blocks.get((pos))
        if block_to_break != None:
            self.blocks.pop(pos)
    
    def add_block(self, pos):
        #check if a block exists
        block_to_break = self.blocks.get((pos))
        
        #Check if the spot is empty.
        if block_to_break == None:

            #Create block object:
            new_block = Block(pos=pos, id=3)

            #add new block to chunk
            self.blocks[pos] = new_block



    def render(self):
        for block in self.blocks.values():
            block.render()


class Block(object):
    def __init__(self, pos, id):

        self.id = id
        if self.id == 1:
            self.sprite = GRASS

        elif self.id == 2:
            self.sprite = DIRT

        elif self.id == 3:
            self.sprite = STONE
        
        else:
            self.sprite = GRASS

        self.rect = pg.Rect((pos[0] * TILE_SIZE, pos[1] * TILE_SIZE),(TILE_SIZE, TILE_SIZE))
        

    def render(self):
        WIN.blit(self.sprite, (self.rect.x - scroll[0], self.rect.y - scroll[1]))




#Player object
class player(object):

    def __init__(self, speed):

        self.sprites_run_left = PLAYER_RUN_L
        self.sprites_run_right = PLAYER_RUN_R
        self.speed = speed
        self.scale = (32, 36)
        self.vel = 0
        self.air_time = 0
        self.is_jumping = True
        self.rect = pg.Rect(-10, 0, 20, 33)
        self.facing = True
        self.run_count = 1


    def break_block(self, chunk):
        keys = pg.key.get_pressed()
        if keys[ord('r')]:
            pos = pg.mouse.get_pos()
            remove_pos = int((pos[0]) // TILE_SIZE + scroll[0] / TILE_SIZE), int(pos[1] / TILE_SIZE + scroll[1] / TILE_SIZE)
            chunk.remove_block(remove_pos)
            return

        if keys[ord('f')]:
            pos = pg.mouse.get_pos()
            place_pos = int(pos[0] // TILE_SIZE + scroll[0] / TILE_SIZE), int(pos[1] / TILE_SIZE + scroll[1] / TILE_SIZE)
            chunk.add_block(place_pos)
            return


    #move player with wasd-keys
    def move(self):
        #Get pressed keys
        keys = pg.key.get_pressed()
        #Check what keys are pressed and save them in move_vector
        move_vector = [0,0]
        #left and right
        if keys[ord('a')]:
            move_vector[0] -= 1
            self.facing = False
            #Running animation
            if self.run_count < 8 * 4:
                self.run_count += 1
            else:
                self.run_count = 1

        if keys[ord('d')]:
            move_vector[0] += 1
            self.facing = True
            #running animation
            if self.run_count < 8 * 4:
                self.run_count += 1
            else:
                self.run_count = 1

        #Jump
        if keys[pg.K_SPACE]:
            if self.is_jumping == False:
                self.is_jumping = True
                self.vel += 12

###########################################################################################

        y_move = self.vel- G_CONST * self.air_time
        if y_move > -16:

            move_vector[1] -= y_move

        else:
            move_vector[1] -= -16

        #check if movement creates a collision
        new_pos_x = self.rect.move([move_vector[0] * 6, 0])
        new_pos_y = self.rect.move([0, move_vector[1] + 1])

        if not collision_test(new_pos_x, loaded_chunks):
            self.rect.x += move_vector[0] * self.speed
        
        #fall collisions
        if not collision_test(new_pos_y, loaded_chunks):
            self.rect.y += move_vector[1]
            self.air_time += 1/FPS 
            self.is_jumping = True
    


        if collision_test(new_pos_y, loaded_chunks):
            self.is_jumping = False
            self.air_time = 0
            self.vel = 0



    def render(self):
        
        if self.facing == False:
            WIN.blit(PLAYER_RUN_L[self.run_count // 4], (self.rect.x - scroll[0] , self.rect.y - scroll[1] ))

        if self.facing == True:
            WIN.blit(PLAYER_RUN_R[self.run_count // 4], (self.rect.x - scroll[0] , self.rect.y - scroll[1] ))


###########################################################################################

def read_chunk(chunk_id):
    #1
    chunk = {}
    #index: -2, -1, 0, 1, 2, 3, etc
    try:
        with open('world\c{}.csv'.format(chunk_id)) as f:
            for line in f:
                lis = list(line.split(','))

                x = int(int(lis[0]) + (chunk_id) * CHUNK_SIZE);  y = int(lis[1]);  id = (int(lis[2]))
                chunk[(x,y)] = id

        #Chunk data in dictionary
        return chunk

    #Chunk doesn't exist yet ----> Make the chunk
    except:
        make_a_chunk(chunk_id)

        with open('world\c{}.csv'.format(chunk_id)) as f:
            for line in f:
                lis = list(line.split(','))

                x = int(int(lis[0]) + (chunk_id) * CHUNK_SIZE);  y = int(lis[1]);  id = (int(lis[2]))

                chunk[(x,y)] = id

        #Chunk data in dictionary
        return chunk

#Load chunks that are needed
def load_chunks(in_chunk):
    load = []


            
    for c in range(0, RENDER_DISTANCE):
        load.append(in_chunk + c)         
        load.append(in_chunk - c)


    #Load chunks that arent loaded that need to be loaded
    for c in range(len(load)):

        #Chunk index = load[cd]
        #print(load, loaded_chunks.keys())
        if load[c] not in loaded_chunks.keys():

            chunk_data = read_chunk(load[c]) #####
            #Should be (x,y) : id
            
            loaded_chunks[load[c]] = chunk(chunk_data, index=load[c])   




#Unload chunks that arent needed.
def unload_chunks(in_chunk):
    load = []
    
    #Load chunks base on players x coordinate
    #chunks to loadddddd
    for c in range(0, RENDER_DISTANCE):
        load.append(in_chunk + c)         
        load.append(in_chunk - c - 1)          ################

    flags = []
    for key, value in loaded_chunks.items():

        if key not in load:
            flags.append(key)

    for f in range(len(flags)):
        loaded_chunks.pop(flags[f])
    

###############################################################################################
    
def render_background():
    WIN.blit(BACK_GROUND[4], (-100 - scroll[0] / 50, -50 - scroll[1] / 50))
    #WIN.blit(BACK_GROUND[3], (-100 - scroll[0] / 40, -50 - scroll[1] / 40))
    WIN.blit(BACK_GROUND[2], (-100 - scroll[0] / 30, -50 - scroll[1] / 30))
    #WIN.blit(BACK_GROUND[1], (-100 - scroll[0] / 20, -50 - scroll[1] / 20))
    #WIN.blit(BACK_GROUND[0], (-100 - scroll[0] / 10, -50 - scroll[1] / 10))

def render_walls():
    pass
    



   
def player_events(player, player_chunk, mouse_chunk):
    player.move()
    player.break_block(mouse_chunk) #############
    player.render()



#Main rendering function
def events(player):
    #Initialize new frame:
    WIN.fill((10, 150, 240))
    render_background()

    
    
    in_chunk = int((player.rect.x // TILE_SIZE) // CHUNK_SIZE)
    mouse_pos = pg.mouse.get_pos()
    
    mouse_in_chunk = int(((mouse_pos[0] + scroll[0]) // TILE_SIZE) // CHUNK_SIZE)



    #update global chunk data
    load_chunks(in_chunk)
    unload_chunks(in_chunk)
    
    
    #Chunk the player is in
    player_chunk = loaded_chunks[in_chunk]

    mouse_chunk = loaded_chunks[mouse_in_chunk]



    #render all chunks
    for chunk_obj in loaded_chunks.values():
        chunk_obj.render()

    #############################
    player_events(player, player_chunk, mouse_chunk)


    
    scroll[0] += (player.rect.x - scroll[0] - (WINDOW[0] / 2 - player.scale[0] / 2)) / 16
    scroll[1] += (player.rect.y - scroll[1] - (WINDOW[1] / 2 - player.scale[1] / 2)) / 16

    
    pg.display.update()


#main game loop
def main():
   
    #player object
    player_1 = player(speed = 3)
    
    #chunk object
    #chunk_0 = chunk(data=read_chunk(chunk_id=0), index=0)
    

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            #closing window
            if event.type == pg.QUIT:
                run = False

        #main loop
        events(player_1)


if __name__ == "__main__":

    print("Starting game...")
    main()

