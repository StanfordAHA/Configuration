###############################################################################
#  file -- time.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#
#  Handles timing.
###############################################################################

import time

class timer:
    
    dump_time = 0
    
    start = 0
    
    end = 0
        
    def set_dump_time (self):
        self.dump_time = time.perf_counter()

    def set_start (self):
        self.start = time.perf_counter()
        
    def set_end (self):
        self.end = time.perf_counter()
