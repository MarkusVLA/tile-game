
import pygame as pg
import numpy as np

from generator import make_a_chunk

#Globall stuff
WINDOW = (1600, 800)
WIN = pg.display.set_mode(WINDOW)
pg.display.set_caption("Mörköpeli")
FPS = 60


#load sprites
PLAYER = pg.transform.scale(pg.image.load('lib\player.png'), (32, 32)).convert()
GRASS = pg.transform.scale(pg.image.load('lib/grass.png'), (16,16)).convert()
BACK_GROUND = pg.transform.scale(pg.image.load('lib/bg.png'), (WINDOW[0] * 1.2, WINDOW[1] * 1.2)).convert()


#Config
TILE_SIZE = 16
CHUNK_SIZE = 128
G_CONST = 24
RENDER_DISTANCE = 3

#Paths
WORLD_DIR = 'world'

#scroll on x and y axies
scroll = [0,0]

loaded_chunks = []
     


#Maybe make more general
def collision_test(rect, loaded_chunks):
    
    for c in range(len(loaded_chunks)):

        chunk = loaded_chunks[c]

        for i in range(len(chunk.blocks)):
            block = chunk.blocks[i]
        
            #Make a rect from the tile
            block_rect = block.rect
            if rect.colliderect(block_rect):
                return True


class chunk(object):

    #chunk object that is 32 blocks long
    def __init__(self, data, index):
        self.index = index
        self.data = data

        #dictionary
        self.blocks = self.init_blocks()


    def init_blocks(self):
        blocks = []
        for key, value in self.data.items():

            #Append block object to block list
            block = Block(pos = key, id = value)
    
            blocks.append(block)

        return blocks


    def render(self):
        for n in range(len(self.blocks)):
            block = self.blocks[n]
            block.render()



class Block(object):
    def __init__(self, pos, id):
        self.id = id
        self.sprite = GRASS
        self.rect = pg.Rect((pos[0] * TILE_SIZE, pos[1] * TILE_SIZE),(TILE_SIZE, TILE_SIZE))
        

    def render(self):
        WIN.blit(GRASS, (self.rect.x - scroll[0], self.rect.y - scroll[1]))




#Player object
class player(object):

    def __init__(self, speed):

        self.rect = PLAYER.get_rect()

        self.sprite = PLAYER
        self.speed = speed
        self.scale = (32, 32)
        self.vel = 0
        self.air_time = 0
        self.is_jumping = True
        self.rect = PLAYER.get_rect()
        

    #move player with wasd-keys
    def move(self, loaded_chunks):
        #Get pressed keys
        keys = pg.key.get_pressed()
        #Check what keys are pressed and save them in move_vector
        move_vector = [0,0]
        #left and right
        if keys[ord('a')]:
            move_vector[0] -= 1
        if keys[ord('d')]:
            move_vector[0] += 1


        #Jump
        if keys[pg.K_SPACE]:
            if self.is_jumping == False:
                self.is_jumping = True
                self.vel += 8

###########################################################################################

        y_move = self.vel- G_CONST * self.air_time
        if y_move > -16:

            move_vector[1] -= y_move

        else:
            move_vector[1] -= -16

        #check if movement creates a collision
        new_pos_x = self.rect.move([move_vector[0] * 4, 0])
        new_pos_y = self.rect.move([0, move_vector[1]])

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
        WIN.blit(self.sprite, (self.rect.x - scroll[0] , self.rect.y - scroll[1] ))

    

#Render player on screen.
def player_events(player, loaded_chunks):
    player.move(loaded_chunks)
    player.render()

###########################################################################################

def read_chunk(chunk_id):
    #1
    chunk = {}
    #index: -2, -1, 0, 1, 2, 3, etc
    try:
        with open('world\c{}.csv'.format(chunk_id)) as f:
            for line in f:
                lis = list(line.split(','))

                x = int(int(lis[0]) + (chunk_id -1) * CHUNK_SIZE/4);  y = int(lis[1]);  id = (int(lis[2]))

                chunk[(x,y)] = id

        #Chunk in memory
        return chunk

    #Chunk doesn't exist yet ----> Make the chunk
    except:
        make_a_chunk(chunk_id)

        with open('world\c{}.csv'.format(chunk_id)) as f:
            for line in f:
                lis = list(line.split(','))

                x = int(int(lis[0]) + (chunk_id -1) * CHUNK_SIZE/4);  y = int(lis[1]);  id = (int(lis[2]))

                chunk[(x,y)] = id

        #Chunk in memory
        return chunk

##############################################################################################


def load_chunks(in_chunk):
    load = []
    chunk_data = {}
    load_range = RENDER_DISTANCE
    #Load chunks base on players x coordinate
    #chunks to loadddddd
            
    for c in range(0, load_range):
        load.append(in_chunk + c)         
        load.append(in_chunk - c - 1)
        #1 and 2


    #Load chunks that arent loaded that need to be loaded
    for c in range(len(load)):
        #if load[c] not in loaded_chunks:
        chunk_data[in_chunk + c] = read_chunk(load[c])
        loaded_chunks.append(load[c])

    
    return chunk_data
 
###############################################################################################
    



#Main rendering function
def events(player):
    #Initialize new frame:
    WIN.fill((10, 150, 240))
    WIN.blit(BACK_GROUND, (-100 - scroll[0] / 50, -100 - scroll[1] / 50))

    
    
    #in_chunk = int((player.rect.x // TILE_SIZE) / CHUNK_SIZE * 4) + 1
    in_chunk = int((player.rect.x // TILE_SIZE) / CHUNK_SIZE * 4) + 1
    
    

    #chunk data in a dict
    chunk_data = load_chunks(in_chunk)
    
    #Chunk the player is in
    #player_chunk = chunk(data = chunk_data.get(in_chunk), index=in_chunk)
    
    #Other chunks:
    loaded_chunks = []
    for key, value in chunk_data.items():
        id = key
        data = value
        a_chunk = chunk(data=data, index=id)
        a_chunk.render()
        loaded_chunks.append(a_chunk)


    #player_chunk.render()

    #############################
    player_events(player, loaded_chunks)
    
    scroll[0] += (player.rect.x - scroll[0] - (WINDOW[0] / 2 - player.scale[0] / 2)) / 16
    scroll[1] += (player.rect.y - scroll[1] - (WINDOW[1] / 2 - player.scale[1] / 2)) / 16

    
    pg.display.update()


#main game loop
def main():
   
    #player object
    player_1 = player(speed = 5)
    
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

