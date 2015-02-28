#!/usr/bin/python
from __future__ import print_function, division, unicode_literals

import argparse
import itertools
import sys

import noise
import PIL.Image

def main(width=800, height=600, scale=3, mode='terrain', outfile='out.png', **kwargs):

  worldmap = [[(0,0,0) for i in range(width)] for i in range(height)]

  freq_mod = scale/width

  if mode == 'terrain':
    terrain(worldmap, width, height, freq_mod, **kwargs)
  elif mode == 'rgbheight':
    rgb_heightmap(worldmap, width, height, freq_mod, **kwargs)
  elif mode == 'height':
    heightmap(worldmap, width, height, freq_mod, **kwargs)
  else:
    raise ValueError('Invalid mode')
    
  im = PIL.Image.new('RGB',(width,height))
  im.putdata(list(itertools.chain(*worldmap)))
  im.save(outfile)

def terrain(worldmap, width, height,freq_mod, sea_level=1000, xoffset=0, yoffset=0,
         sea_color=(0,0,255), coast_color=(0,100,255), shore_color=(244,164,96), land_color=(183,123,72),
         mountain_color=(122,102,78)):
  for y in range(height):
    for x in range(width):
      nx = x * freq_mod + xoffset
      ny = y * freq_mod + yoffset
      land_level = 10000 * noise.snoise2(nx, ny, octaves=6)
      if land_level > sea_level:
        if land_level < 5000:
          if (land_level - sea_level) < 1000:
            worldmap[y][x] = shore_color
          else:
            worldmap[y][x] = land_color
        else:
          worldmap[y][x] = mountain_color
      elif (sea_level - land_level) < 1000:
        worldmap[y][x] = coast_color
      else:
        worldmap[y][x] = sea_color

def rgb_heightmap(worldmap, width, height,freq_mod, sea_level=1000, xoffset=0, yoffset=0):
  for y in range(height):
    for x in range(width):
      nx = x * freq_mod + xoffset
      ny = y * freq_mod + yoffset
      land_level = int((2**(8*3)-1) * ((noise.snoise2(nx, ny, octaves=6) + 1) / 2))
      b = land_level & 0xff
      land_level >>= 8
      g = land_level & 0xff
      land_level >>= 8
      r = land_level & 0xff
      worldmap[y][x] = r, g, b

def heightmap(worldmap, width, height,freq_mod, sea_level=1000, xoffset=0, yoffset=0):
  for y in range(height):
    for x in range(width):
      nx = x * freq_mod + xoffset
      ny = y * freq_mod + yoffset
      land_level = int((2**8 - 1) * ((noise.snoise2(nx, ny, octaves=6) + 1) / 2))
      worldmap[y][x] = land_level, land_level, land_level

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
  parser = argparse.ArgumentParser(add_help=False, description='Generate terrain maps')
  parser.add_argument('-H', '--help', action='store_true', help='Show this message and exit')

  parser.add_argument('-w', '--width', type=int, help='Width of the final image')
  parser.add_argument('-h', '--height', type=int, help='Height of the final image')
  parser.add_argument('-s', '--scale', type=float, help='Scale of the map')
  parser.add_argument('-x', '--xoffset', type=float, help='Offset to apply to the horizontal noise position')
  parser.add_argument('-y', '--yoffset', type=float, help='Offset to apply to the vertical noise position')
  parser.add_argument('-S', '--sea_level', type=float, help="How high should the map's sea level be")

  parser.add_argument('--sea_color', type=color, help='Color for deep water')
  parser.add_argument('--coast_color', type=color, help='Color for water near land')
  parser.add_argument('--shore_color', type=color, help='Color for land near water')
  parser.add_argument('--land_color', type=color, help='Color for land')
  parser.add_argument('--mountain_color', type=color, help='Color for mountains')

  parser.add_argument('-m', '--mode', type=str, choices=('terrain', 'height', 'rgbheight'),
                      help='Type of map to generate')

  parser.add_argument('-o', '--outfile', type=str, help='File to write the map image to')
  
  args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}

  if args['help']:
    parser.print_help()
    sys.exit(0)
  else:
    del args['help']
  
  main(**args)
