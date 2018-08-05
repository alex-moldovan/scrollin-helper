#!/usr/bin/env python

import sys
import time
import scrollphathd as sphd


sphd.set_brightness(1.0)

if len(sys.argv) != 2:
    print("\nusage: python simple-text-scroll-rotated.py \"message\" \npress CTRL-C to exit\n")
    sys.exit(0)

#The screen is rotated on my robot case.
sphd.rotate(180)


sphd.write_string(sys.argv[1], 11)

while True:
    try:
    	sphd.show()
        sphd.scroll(1)
        time.sleep(0.05)
    except KeyboardInterrupt:
        sphd.clear()
sys.exit()