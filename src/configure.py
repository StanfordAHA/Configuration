###############################################################################
#  file -- configure.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#    Makai Mann
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  The main file of the configuration finder.
###############################################################################

import smt_switch as ss
import smt_switch.primops as po
import smt_switch.sortkinds as sk
import argparse
import pono as c
import sys
import re
import time
import copy
import io
from parse import *
from operators import *
from groups import *
from sts import *
from solve import *
from printer import *
from optimize import *
from timer import *

if __name__ == "__main__":

    
    parser = argparse.ArgumentParser()
    parser.add_argument('--agg', action="store_true")
    parser.add_argument('--tb', action="store_true")
    parser.add_argument('--sram', action="store_true")
    #parser.add_argument('--verbose', action="store_true")
    parser.add_argument('-l','--linear', action="store_true")
    parser.add_argument('--bounds', action="store_true")
    parser.add_argument('--optbw', action="store_true")
    parser.add_argument('-n','--annote', dest="annotation", default = None)
    parser.add_argument('-sv','--verilog', dest="verilog", default = None)
    parser.add_argument('-csv','--seq', dest="sequence")
    parser.add_argument('--cagg', dest="agg_solved", default = None)
    parser.add_argument('--ctb', dest="tb_solved", default = None)
    parser.add_argument('--hwpath', dest="hwpath", type = str, default =".")
    parser.add_argument('-v','--verify', dest="verify", default = None)
    parser.add_argument('-opt','--optimize', dest="optimize", type = int, default = 1)
    parser.add_argument('-out','--output', dest="out_path", default = "")
    parser.add_argument('--caggtbfirst', action="store_true")
    parser.add_argument('--caggtbmin', action="store_true")

    args = parser.parse_args()

    c.set_global_logger_verbosity(1)
    
    tm = timer()

    tm.set_start()
  
    csv_file = args.sequence
    csv_path = csv_file
    csv_path = csv_path[csv_path.find("aha_garnet_smt/")+15:]


    if args.agg:
        module_name = "agg"
    if args.tb:
        module_name = "tb"
    if args.sram:
        module_name = "sram"
    if not (args.agg or args.sram or args.tb):
        module_name = "top"

    output_file = csv_path+"/"+module_name+"_opt_"+str(args.optimize)

    if args.optbw:
        output_file = output_file+"_bw"
    
    output_file_first = args.out_path+output_file+"_first.out"
    output_file_min = args.out_path+output_file+"_min.out"
    output_file = args.out_path+output_file+".out"
    file_dump = csv_path+"_dump.smt2"
    file_dump = file_dump.replace('/', '_')
    print("file_dump:",file_dump)
    print("output_file:",output_file)
    print("output_file_first:",output_file_first)
    print("output_file_min:",output_file_min)

    fout = open(output_file,"w")


    print ("input:",*sys.argv)
    fout.write("input:"+str(sys.argv))
    fout.write("\n")

    symbols = {}
    group_ranges = {}
    dim_names = {}

    

############################################################################################################
# Set the module to solve
############################################################################################################

    agg_set = False
    tb_set = False
    sram_set = False
    top_set = False

    if args.agg:
        agg_set = args.agg
        print("Solving an Aggregator module")
        fout.write("Solving an Aggregator module")
        fout.write("\n")
    elif args.tb:
        tb_set = args.tb
        print("Solving a TB module")
        fout.write("Solving a TB module")
        fout.write("\n")
    elif args.sram:
        sram_set = args.sram
        print("Solving an SRAM module")
        fout.write("Solving an SRAM module")
        fout.write("\n")
    else:
        top_set = True
        print("Solving an top module")
        fout.write("Solving an top module")
        fout.write("\n")

############################################################################################################
# Set an SMT solver.
# Create STS
############################################################################################################
    # instantiate an smt solver
    #option False is for simplifying terms, True for no term simplification
    solver = ss.create_btor_solver(False)
    #solver = ss.create_bitwuzla_solver(False)
    #solver = ss.create_cvc4_solver()
    #solver = ss.create_msat_solver()
    
    # set options
    #solver.set_opt('BTOR_OPT_REWRITE_LEVEL', '0')
    solver.set_opt('produce-models', 'true')
    solver.set_opt('incremental', 'true')
    solver.set_opt('produce-unsat-cores', 'true')
    
    # create a transition system
    fts = c.FunctionalTransitionSystem(solver)
    
    # instantiate an unroller
    u = c.Unroller(fts, solver)
    
    if args.verilog == None:
        if agg_set:
            mod_sv = args.hwpath+'agg_lake_top_no_arrays.btor2'
        elif tb_set:
            mod_sv = args.hwpath+'tb_lake_top_no_arrays.btor2'
        elif sram_set:
            mod_sv = args.hwpath+'sram_lake_top_no_arrays.btor2'
        else:
            mod_sv = args.hwpath+'lake_top_no_arrays.btor2'
    else:
        mod_sv = args.verilog

    # read in a filename and populate the transition system
    encoder = c.BTOR2Encoder(mod_sv, fts)
    
    # create a dictionary to look up symbols by name
    # start with named terms
    symbols = {k:v for k,v in fts.named_terms.items()}

    for sym_set in [fts.statevars, fts.inputvars]:
        for s in sym_set:
            symbols[str(s).replace('|', '')] = s

############################################################################################################
# Generate stream
############################################################################################################
    #dump_time = 0
    
    strm = stream()
    strm.read_stream(args, fout, agg_set, tb_set, sram_set, symbols, solver)

############################################################################################################
# Set group IDs for the module
############################################################################################################
    
    m = module()
    m.set_group_ids(agg_set, tb_set, sram_set, top_set, strm.config_names, symbols)
    m.set_shared_interface()
    
    print("VALID MAP:", m.valids)
    print("DATA MAP:", m.data)
    fout.write("VALID MAP:"+str(m.valids))
    fout.write("\n")
    fout.write("DATA MAP:"+str(m.data))
    fout.write("\n")
    
    for conf_name in strm.config_names:
        if "dimensionality" in conf_name:
            for id in m.group_ids:
                if id in conf_name:
                    dim_names[id] = conf_name

############################################################################################################
# Set adding extra info on bounds
############################################################################################################

    if args.bounds:
        add_bounds = True
    else:
        add_bounds = False

############################################################################################################
# Binary vs Linear search
############################################################################################################

    if args.linear:
        binary_search = False
    else:
        binary_search = True
        
############################################################################################################
# To verify solution
############################################################################################################

    if args.verify != None:
        verify_solution = True
    else:
        verify_solution = False

############################################################################################################
# For Optimization
############################################################################################################

    optimize_bit_width = args.optbw

    optimize_depth = args.optimize
    if args.optimize > 4: optimize_depth = 4

    optimize_start_addrs = False
    optimize_strides = False
    optimize_ranges = False
    optimize_dims = False

    if optimize_depth == 1:
        optimize_dims = True
    if optimize_depth == 2:
        optimize_dims = True
        optimize_ranges = True
    if optimize_depth == 3:
        optimize_dims = True
        optimize_ranges = True
        optimize_strides = True
    if optimize_depth == 4:
        optimize_dims = True
        optimize_ranges = True
        optimize_strides = True
        optimize_start_addrs = True

    if (optimize_depth > 1): optimize_dims = True
    
    ass_to_opt = {}
    current_ass = {}
    bw_last_sat = {}
    partial_assignment = {}

    min_sum = 0#len(m.group_ids)
    dim_max_val = 6
    max_sum = len(m.group_ids) * dim_max_val + 1
 
    obj_term_keys = []

    build_keys = []
    for id in m.group_ids:
        key = "obj_term_comp_"+id+"_ranges"
        build_keys.append(key)
    build_keys.append("obj_term_ranges_low")
    build_keys.append("obj_term_ranges_high")
    obj_term_keys.append(build_keys)
    
    build_keys = []
    for id in m.group_ids:
        key = "obj_term_comp_"+id+"_strides"
        build_keys.append(key)
    build_keys.append("obj_term_strides_low")
    build_keys.append("obj_term_strides_high")
    obj_term_keys.append(build_keys)
    
    build_keys = []
    for id in m.group_ids:
        key = "obj_term_comp_"+id+"_starting_addr"
        build_keys.append(key)
    build_keys.append("obj_term_starting_addr_low")
    build_keys.append("obj_term_starting_addr_high")
    obj_term_keys.append(build_keys)


############################################################################################################
    
    slv = solution()

    prnt = printer(fout)

    prnt.print_opt_objective (optimize_dims, optimize_ranges, optimize_strides, optimize_start_addrs, optimize_bit_width, binary_search, add_bounds)

############################################################################################################
    
    unrolled_ts = build_sts(u, args, strm, fout, agg_set, tb_set, sram_set, add_bounds, dim_max_val, fts, m, symbols, solver)

    solver.dump_smt2(file_dump)
    print('dump done!')
    fout.write('dump done!')
    fout.write("\n")
    
    tm.set_dump_time()
    #assert(False)


    group_names = []
    group_names.append(m.groups_data["ranges"])
    group_names.append(m.groups_data["strides"])
    group_names.append(m.groups_data["starting_addr"])

    decide = "unsat"
    indicators = {}
    for id in m.group_ids:
        for addr in m.groups_data["starting_addr"][id].keys():
            st_addr = symbols[addr]
            #if "sched" not in addr:
            indicator = solver.make_symbol("indicator_"+str(addr), solver.make_sort(sk.BOOL))
            indicators[addr] = indicator
    
    
    if optimize_dims:
        opt_steps = 0
        
        res = 0
        
        for i in range(min_sum,max_sum):#(2,13)
            min_loop_ass = {}

            list_keys_temp = list(dim_names)
            list_keys = []

            write_names_temp = m.write_ids


            for d in list_keys_temp:
                if d in write_names_temp:
                    list_keys.append(d)
            
            for d in list_keys_temp:
                if d not in list_keys:
                    list_keys.append(d)

            dims_left = len(dim_names)
            
            if dims_left:
                res = gen_dim_vals(slv, strm, u, m, fout, output_file_first, optimize_bit_width, binary_search, partial_assignment, unrolled_ts, optimize_depth, i, dim_names, dim_max_val, min_sum, dims_left, list_keys, ass_to_opt, min_loop_ass, opt_steps, group_names, obj_term_keys, indicators, prnt, tm, sys.argv, symbols, solver)
            if res:
                decide = "sat"
                print (res,"optimization steps")
                fout.write(str(res)+" optimization steps")
                fout.write("\n")
                break
    else: #not optimize dims
        min_loop_ass = {}
        empty_data = [[]]
        if verify_solution:
            decide = verify_config(unrolled_ts, args.verify, symbols, strm.config_names, solver)
        if solve_lake(slv, strm, optimize_bit_width, binary_search, min_loop_ass, unrolled_ts, False, empty_data, empty_data, indicators.values(), dim_names, m, fout, prnt, symbols, solver):
            sys.stdout = prnt.old_stdout
            decide = "sat"
        
    print (decide)
    print (prnt.output)
    fout.write(decide)
    fout.write("\n")
    fout.write(prnt.output)
    fout.write("\n")
    
    tm.set_end()
    prnt.print_final (fout, tm, slv, sys.argv)
    
    fout.close()
    
    with open(output_file_min, "w") as fout_min:
        for line in slv.get_min_solution:
            fout_min.write(line)
            fout_min.write("\n")

