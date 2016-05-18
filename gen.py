#!/usr/bin/python

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta
from subprocess import call

# GitHub uses Sunday-starting weeks, so add 1
offset = (date.today().weekday() + 1) % 7
rows = 7
cols = 52
size = (cols,rows)
numdays = rows * cols

def commit(days_ago, msg):
  d = date.today() - timedelta(days = days_ago)
  t = str(d) + " 00:00:00"
  os.system("echo " + msg + " > .tmpfile")
  os.system("git add .tmpfile")
  os.system('GIT_COMMITTER_DATE="'+t+'"' + ' GIT_AUTHOR_DATE="'+t+'"' + ' git commit -m "' +msg+'" 2>&1 >/dev/null')

def rgb2gray(rgb):
    r,g,b = rgb[0:3] # ignore alpha for now
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def write_px(x, y, intensity, prefix=""):
  days_ago = numdays+offset - (x*rows+y)
  d = date.today() - timedelta(days = days_ago)
  t = str(d) + " 00:00:00"
  print "val=",intensity, "x",x,"y",y,"date:",d
  for i in range(0, intensity):
    msg = prefix + os.urandom(8).encode("hex")
    commit(days_ago, msg)

# Use this function to process a 52x7 image as grayscale
def process_image(path):
  img = Image.open(path)
  px = img.load()
  size = img.size
  if (52,7) != size:
    raise Exception("Image should be 52x7, got " + size)
  for x in range(size[0]):
    print "processed line",x
    for y in range(size[1]):
      val = 255-int(rgb2gray(px[x,y]))
      val /= 16
      write_px(x,y, val, prefix="ign-")

def process_text(txt, offset=2):
  f = 1
  image = Image.new("RGB", [x*f for x in size], (255,255,255))
  draw = ImageDraw.Draw(image)
# see https://mail.python.org/pipermail/image-sig/2005-August/003497.html
  draw.fontmode = "1"
  font = ImageFont.truetype("font/5x5_pixel.ttf", 8)
  draw.text((offset,1), txt, (0,0,0), font=font)

  image.save(txt+".bmp")

def main():
  if sys.argv[1] == "--text":
    process_text(sys.argv[2])
  else:
    process_image(sys.argv[1])


if __name__ == "__main__": main()

