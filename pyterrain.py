#!/usr/bin/python

import argparse
import sys

import noise
import pygame

def main(width=1024, height=1024, sea_level=5000, xoffset=0, yoffset=0, outfile='testmap.png',
         sea_color=(0,0,255), coast_color=(0,100,255), shore_color=(244,164,96), land_color=(183,123,72),
         mountain_color=(122,102,78)):
  worldmap = pygame.Surface((width, height))
  worldmap.fill(sea_color)

  freq_mod = 3/float(width)

  for x in range(width):
    for y in range(height):
      nx = x * freq_mod + xoffset
      ny = y * freq_mod + yoffset
      land_level = 10000 * noise.snoise2(nx, ny, octaves=6)
      if land_level > sea_level:
        if land_level < 5000:
          if (land_level - sea_level) < 1000:
            worldmap.set_at((x, y), shore_color)
          else:
            worldmap.set_at((x, y), land_color)
        else:
          worldmap.set_at((x, y), mountain_color)
      elif (sea_level - land_level) < 1000:
        worldmap.set_at((x, y), coast_color)

  pygame.image.save(worldmap, outfile)

def color(s):
  if s.startswith('#'):
    ss = s[1:]
    if len(ss) == 3:
      return tuple(int(c * 2, base=16) for c in ss)
    elif len(ss) == 6:
      return tuple(int(ss[i:i+2], base=16) for i in range(0, len(ss), 2))
    else:
      raise ValueError('Invalid literal "{}" for hexidecimal color'.format(s))
  else:
    r,g,b = tuple(min(max(int(i), 0), 255) for i in s.replace(':', ',').split(','))
    return r, g, b
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('width', type=int, help='Width of the final image')
  parser.add_argument('height', type=int, help='Height of the final image')
  parser.add_argument('sea_level', type=float, help="How high should the map's sea level be")
  parser.add_argument('-x', '--xoffset', type=float, help='Offset to apply to the horizontal noise position')
  parser.add_argument('-y', '--yoffset', type=float, help='Offset to apply to the vertical noise position')
  parser.add_argument('-o', '--outfile', type=str, help='File to write the map image to')

  parser.add_argument('--sea_color', type=color, help='Color for deep water')
  parser.add_argument('--coast_color', type=color, help='Color for water near land')
  parser.add_argument('--shore_color', type=color, help='Color for land near water')
  parser.add_argument('--land_color', type=color, help='Color for land')
  parser.add_argument('--mountain_color', type=color, help='Color for mountains')
  
  args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}
  main(**args)
