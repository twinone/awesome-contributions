#!/usr/bin/python

import os
import sys
from PIL import Image
from datetime import date, timedelta
from subprocess import call

# GitHub uses Sunday-starting weeks, so add 1
offset = (date.today().weekday() + 1) % 7
rows = 7
cols = 52
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
  N=0
  days_ago = numdays+offset - (x*rows+y)
  d = date.today() - timedelta(days = days_ago)
  t = str(d) + " 00:00:00"
  print "val=",intensity, "x",x,"y",y,"date:",d
  for i in range(0, intensity):
    msg = prefix + os.urandom(8).encode("hex")
#    msg = prefix + str(N)
    N += 1
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

process_image(sys.argv[1])
