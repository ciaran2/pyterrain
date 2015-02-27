#!/usr/bin/python

import sys
import noise
import pygame

SEA_COLOR = (0,0,255)
COAST_COLOR = (0,100,255)
SHORE_COLOR = (244,164,96)
LAND_COLOR = (183,123,72)
MOUNTAIN_COLOR = (122,102,78)

def print_usage():
  print("usage: procedural-map.py width height sea_level xoffset yoffset")
  sys.exit()

def verify_args():
  if len(sys.argv) != 6:
    print_usage()

  try:
    return int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
  except ValueError:
    print_usage()

def main():
  width, height, sea_level, xoffset, yoffset = verify_args()

  worldmap = pygame.Surface((width,height))
  worldmap.fill(SEA_COLOR)

  freq_mod = 3/float(width)

  for x in range(width):
    for y in range(height):
      nx = x * freq_mod + xoffset
      ny = y * freq_mod + yoffset
      land_level = 10000 * noise.snoise2(nx,ny,octaves=6)
      if land_level > sea_level:
        if land_level < 5000:
          if (land_level - sea_level) < 1000:
            worldmap.set_at((x,y),SHORE_COLOR)
          else:
            worldmap.set_at((x,y),LAND_COLOR)
        else:
          worldmap.set_at((x,y),MOUNTAIN_COLOR)
      elif (sea_level - land_level) < 1000:
        worldmap.set_at((x,y),COAST_COLOR)

  pygame.image.save(worldmap,"testmap.png")

main()
