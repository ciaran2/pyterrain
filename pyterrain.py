#!/usr/bin/python

import argparse
import sys

import noise
import pygame

SEA_COLOR = (0,0,255)
COAST_COLOR = (0,100,255)
SHORE_COLOR = (244,164,96)
LAND_COLOR = (183,123,72)
MOUNTAIN_COLOR = (122,102,78)

def main(width, height, sea_level, xoffset=0, yoffset=0):

  worldmap = pygame.Surface((width, height))
  worldmap.fill(SEA_COLOR)

  freq_mod = 3/float(width)

  for x in range(width):
    for y in range(height):
      nx = x * freq_mod + xoffset
      ny = y * freq_mod + yoffset
      land_level = 10000 * noise.snoise2(nx, ny, octaves=6)
      if land_level > sea_level:
        if land_level < 5000:
          if (land_level - sea_level) < 1000:
            worldmap.set_at((x, y), SHORE_COLOR)
          else:
            worldmap.set_at((x, y), LAND_COLOR)
        else:
          worldmap.set_at((x, y), MOUNTAIN_COLOR)
      elif (sea_level - land_level) < 1000:
        worldmap.set_at((x, y), COAST_COLOR)

  pygame.image.save(worldmap,"testmap.png")
 
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('width', type=int, help='Width of the final image')
  parser.add_argument('height', type=int, help='Height of the final image')
  parser.add_argument('sea_level', type=float, help="How high should the map's sea level be")
  parser.add_argument('-x', '--xoffset', type=float,
                      help='Offset to apply to the horizontal noise position', default=0)
  parser.add_argument('-y', '--yoffset', type=float,
                      help='Offset to apply to the vertical noise position', default=0)
  args = parser.parse_args()
  main(**vars(args))
