#!/usr/bin/env python

import sys
import time
import scrollphat


scrollphat.set_brightness(2)

if len(sys.argv) != 2:
    print("\nusage: python simple-text-scroll-rotated.py \"message\" \npress CTRL-C to exit\n")
    sys.exit(0)

#The screen is rotated on my robot case.
scrollphat.rotate(180)


scrollphat.write_string(sys.argv[1], 11)

while True:
    try:
    	scrollphat.show()
        scrollphat.scroll(1)
        time.sleep(0.05)
    except KeyboardInterrupt:
        scrollphat.clear()
sys.exit(-1)