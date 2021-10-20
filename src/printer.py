###############################################################################
#  file -- printer.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Handles printing.
###############################################################################

import sys
import io
import time
from timer import *

class printer:
    
    old_stdout = sys.stdout
    
    new_stdout = io.StringIO()
    
    output = "No solution found"
    
    def __init__(self,fout):
        self.fout = fout
    
    def set_output (self):
        self.output = self.new_stdout.getvalue()


    def print_opt_objective (self, optimize_dims, optimize_ranges, optimize_strides, optimize_start_addrs, optimize_bit_width, binary_search, add_bounds):
    
        print ("optimize_dims = ",optimize_dims,", optimize_ranges = ",optimize_ranges,", optimize_strides = ",optimize_strides,", optimize_start_addrs = ",optimize_start_addrs,", optimize_bit_width = ",optimize_bit_width, ", binary_search = ",binary_search,", add_bounds = ",add_bounds)

        self.fout.write("optimize_dims = "+str(optimize_dims)+", optimize_ranges = "+str(optimize_ranges)+", optimize_strides = "+str(optimize_strides)+", optimize_start_addrs = "+str(optimize_start_addrs)+", optimize_bit_width = "+str(optimize_bit_width)+", binary_search = "+str(binary_search)+", add_bounds = "+str(add_bounds))
        self.fout.write("\n")

    def print_final (self, fout, tm, slv, sys_argv):
            print ("input:",*sys_argv)
            print (time.strftime("-- MIN -- dump_time: %H:%M:%S",time.gmtime(tm.dump_time-tm.start)),time.strftime("; solve_time: %H:%M:%S",time.gmtime(slv.solve_time-tm.dump_time)),time.strftime("; total_time: %H:%M:%S",time.gmtime(tm.end-tm.start)))
            print ("-- MIN -- dump_time:",tm.dump_time-tm.start,"; solve_time:", slv.solve_time-tm.dump_time,"; total_time:",tm.end-tm.start)

            fout.write("input:"+str(sys_argv))
            fout.write("\n")
            fout.write(time.strftime("-- MIN -- dump_time: %H:%M:%S ",time.gmtime(tm.dump_time-tm.start))+" "+time.strftime("; solve_time: %H:%M:%S ",time.gmtime(slv.solve_time-tm.dump_time))+" "+time.strftime("; total_time: %H:%M:%S ",time.gmtime(tm.end-tm.start)))
            fout.write("\n")
            fout.write("-- MIN -- dump_time: "+str(tm.dump_time-tm.start)+"; solve_time: "+str(slv.solve_time-tm.dump_time)+"; total_time: "+str(tm.end-tm.start))
            fout.write("\n")

    def print_first_solution (self, fout, tm, slv, sys_argv, output_file_first):
            print ("input:",*sys_argv)
            print(self.output,flush = True)
            print (time.strftime("-- FIRST -- dump_time: %H:%M:%S",time.gmtime(tm.dump_time-tm.start)),time.strftime("; solve_time: %H:%M:%S",time.gmtime(slv.solve_time-tm.dump_time)),time.strftime("; total_time: %H:%M:%S",time.gmtime(tm.end-tm.start)), flush = True)
            print ("-- FIRST -- dump_time:",tm.dump_time-tm.start,"; solve_time:",slv.solve_time-tm.dump_time,"; total_time:",tm.end-tm.start, flush = True)

            fout.write("input: "+str(sys_argv))
            fout.write("\n")
            fout.write(self.output)
            fout.write("\n")
            fout.write(time.strftime("-- FIRST -- dump_time: %H:%M:%S ",time.gmtime(tm.dump_time-tm.start))+" "+time.strftime("; solve_time: %H:%M:%S ",time.gmtime(slv.solve_time-tm.dump_time))+time.strftime("; total_time: %H:%M:%S",time.gmtime(tm.end-tm.start)))
            fout.write("\n")
            fout.write("-- FIRST -- dump_time: "+str(tm.dump_time-tm.start)+"; solve_time: "+str(slv.solve_time-tm.dump_time)+"; total_time: "+str(tm.end-tm.start))
            fout.write("\n")
            
            
            with open(output_file_first, "w") as fout_first:
                print("fout_first",output_file_first)
                #print("start",fout_first.closed)
                #print ("get_min_solution", slv.get_min_solution)
                for line in slv.get_min_solution:
                    print (line)
                    fout_first.write(line)
                    fout_first.write("\n")
            #print("finish",fout_first.closed)

#           fout_first.close()

    def print_opt_layer (self, fout, tm, slv, sys_argv, optimize_depth, iter_optim_depth):
    
        print ("input:",*sys_argv)
        print(self.output,flush = True)
        print ("-- OPTIMIZATION LAYER ", optimize_depth-iter_optim_depth,time.strftime(" -- dump_time: %H:%M:%S",time.gmtime(tm.dump_time-tm.start)),time.strftime("; solve_time: %H:%M:%S",time.gmtime(slv.solve_time-tm.dump_time)),time.strftime("; total_time: %H:%M:%S",time.gmtime(tm.end-tm.start)), flush = True)
        print ("-- OPTIMIZATION LAYER ", optimize_depth-iter_optim_depth," -- dump_time:",tm.dump_time-tm.start,"; solve_time:",slv.solve_time-tm.dump_time,"; total_time:",tm.end-tm.start, flush = True)

        fout.write("input:"+str(sys_argv))
        fout.write("\n")
        fout.write(self.output)
        fout.write("\n")
        fout.write("-- OPTIMIZATION LAYER "+str(optimize_depth-iter_optim_depth)+time.strftime(" -- dump_time: %H:%M:%S ",time.gmtime(tm.dump_time-tm.start))+time.strftime("; solve_time: %H:%M:%S ",time.gmtime(slv.solve_time-tm.dump_time))+time.strftime("; total_time: %H:%M:%S ",time.gmtime(tm.end-tm.start)))
        fout.write("\n")
        fout.write("-- OPTIMIZATION LAYER "+str(optimize_depth-iter_optim_depth)+" -- dump_time: "+str(tm.dump_time-tm.start)+"; solve_time: "+str(slv.solve_time-tm.dump_time)+"; total_time: "+str(tm.end-tm.start))
        fout.write("\n")

