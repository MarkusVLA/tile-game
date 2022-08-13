from random import seed
from timeit import repeat
import noise
import numpy as np


CHUNK_SIZE = 32
TILE_SIZE = 16
TERRAIN_HEIGHT  = 32

WORLD_DIR = 'world'

def generate_chunk(id):
    chunk = []
    for x in range(CHUNK_SIZE):
        height = noise.pnoise1(x + id * CHUNK_SIZE, repeat = 1000000, octaves = 1)
        y = int(height * 16) + TERRAIN_HEIGHT
        chunk.append(y)

    return chunk


def write_chunk(data, id):
    with open(WORLD_DIR + '\c{}.csv'.format(str(id)), 'w') as f:
        for i in range(len(data)):

            format = '{},{},{}\n'.format(i, data[i], 1)

            #print(format)

            f.write(format)

    print('Generated new chunk: {}'.format(str(id)))



def make_a_chunk(id):
    data = generate_chunk(id)
    write_chunk(data, id)
            

if __name__ == "__main__":
    print("You not supposer to run this file")