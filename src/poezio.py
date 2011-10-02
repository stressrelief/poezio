# Copyright 2010-2011 Florent Le Coz <louiz@louiz.org>
#
# This file is part of Poezio.
#
# Poezio is free software: you can redistribute it and/or modify
# it under the terms of the zlib license. See the COPYING file.


"""
Starting point of poezio. Launches both the Connection and Gui
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import signal
import logging

from config import options
import singleton
import core

def main():
    """
    Enter point
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN) # ignore ctrl-c
    if options.debug:
        logging.basicConfig(filename=options.debug, level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)
    cocore = singleton.Singleton(core.Core)
    cocore.start()
    if not cocore.xmpp.start():  # Connect to remote server
        cocore.on_failed_connection()
    cocore.main_loop()    # Refresh the screen, wait for user events etc

if __name__ == '__main__':
    main()
