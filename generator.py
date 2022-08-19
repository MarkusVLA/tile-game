
from random import randint
import noise
import numpy as np

GRASS = 1
DIRT = 2
STONE = 3
 
SEED = randint(0, 10000)

CHUNK_SIZE = 16
TILE_SIZE = 8
TERRAIN_HEIGHT = 16

WORLD_DEPTH = 128

WORLD_DIR = 'world'

def make_terrain(id):
    chunk = {}

    for x in range(CHUNK_SIZE):
        

        height = noise.pnoise1((x) / CHUNK_SIZE + id + SEED, repeat = 1000000, octaves = 2)
        real_height = (height * 16) + TERRAIN_HEIGHT

        #Top layer
        chunk[(x, int(real_height))] = GRASS

        #Stone layer:
        stone_H = noise.pnoise1((x) / CHUNK_SIZE + id, repeat = 1000000, octaves = 4)
        real_stone_H = (stone_H * 16) + TERRAIN_HEIGHT + 16

        random = randint(0,3)
        for i in range(WORLD_DEPTH):
            
            if i > real_height:
                if i < real_stone_H + random:
                    chunk[(x, i)] = DIRT

                else:
                    chunk[(x, i)] = STONE


        #Cut caves in the terrain
        
        for x in range(CHUNK_SIZE):
            for y in range(WORLD_DEPTH):

                cave_pattern = noise.pnoise2(x / CHUNK_SIZE + id, y / WORLD_DEPTH * 20, octaves = 1)
                if (cave_pattern * 4) > 1:
                    if y > 30:
                        if (x, y) in chunk.keys():
                            chunk.pop((x,y))

        
    
    return chunk

        


def write_chunk(data, id):
    with open(WORLD_DIR + '\c{}.csv'.format(str(id)), 'w') as f:
        for key,value in data.items():
            #(x , y): id

            format = '{},{},{}\n'.format(key[0], key[1], value)

            #print(format)

            f.write(format)

    print('Generated new chunk: {}'.format(str(id)))



def make_a_chunk(id):
    data = make_terrain(id)
    write_chunk(data, id)
            

if __name__ == "__main__":
    print(make_terrain(3))