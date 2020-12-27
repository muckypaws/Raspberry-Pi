#!/usr/bin/env python
#
# Update to Raspberry Pi RGB XMas Tree
# Adapted from the Pimorini Plasma Buttons Script: https://github.com/pimoroni/plasma
# Adapted from the Original RGB Xmas Tree Script: https://github.com/ThePiHut/rgbxmastree#rgbxmastree
#
# Created by Jason Brooks: www.muckypaws.com and www.wonkypix.com
#            27th December 2020
#
# Add a PNG of colours to set the tree to cycle through that list.
# rainbow-cycle.png is provided as an example.
#

import png
import time
import signal
import os
import sys
import threading
from datetime import datetime
from tree import RGBXmasTree
# Application Defaults

PATTERNS = "./"
#How fast should the lights update? Anything above 30FPS
#Won't give you an advantage due to SPI Transfer Clock Speed
FPS = 25

#Changing this value will create differing effects cycling through
#Your PNG of colours
DELTA_OFFSET = 20

# Pattern List of the order of LED Light on the RGB Xmas Tree
# Starting from Front Left, working around the tree anti-clockwise
# Be Creative, create light chasers!
XMASLEDLIST = [7, 20, 25, 1, 8, 16, 17, 13,     # Bottom Row
               6, 21, 24, 2, 9, 15, 18, 12,     # Middle Row
               5, 22, 23, 3, 10, 14, 19, 11,    # Top Row
               4]                               # Star

stopped = threading.Event()
tree = RGBXmasTree()

def main():
        r, g, b = 0, 0, 0
        pattern, pattern_w, pattern_h, pattern_meta = load_pattern("rainbow-cycle")
             
        while not stopped.wait(1.0 / FPS):
            delta = time.time() * 60
            
            if pattern is not None:
                alpha = pattern_meta['alpha']
                channels = 4 if alpha else 3

                offset_y = int(delta % pattern_h)
                row = pattern[offset_y]
                x = 0
                for index in XMASLEDLIST:
                    offset_x = (x * channels) % (pattern_w * channels)
                    r, g, b = row[offset_x:offset_x + 3]
                    tree[index-1].color = r/255.0, g/255.0, b/255.0
                    delta+=DELTA_OFFSET
                    offset_y = int(delta % pattern_h)
                    row = pattern[offset_y]
            else:
                for pixel in tree:
                    pixel.color = r/255.0, g/255.0, b/255.0
                    
            tree.update()

def log(msg):
    sys.stdout.write(str(datetime.now()))
    sys.stdout.write(": ")
    sys.stdout.write(msg)
    sys.stdout.write("\n")
    sys.stdout.flush()

def load_pattern(pattern_name):
    pattern_file = os.path.join(PATTERNS, "{}.png".format(pattern_name))
    if os.path.isfile(pattern_file):
        r = png.Reader(file=open(pattern_file, 'rb'))
        pattern_w, pattern_h, pattern, pattern_meta = r.read()
        pattern = list(pattern)
        log("Loaded pattern file: {}".format(pattern_file))
        return pattern, pattern_w, pattern_h, pattern_meta
    else:
        log("Invalid pattern file: {}".format(pattern_file))
        return None, 0, 0, None

if __name__ == "__main__":
    main()
