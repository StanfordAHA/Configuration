###############################################################################
#  file -- sts.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Builds the symbolic transition system.
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
from bounds import *
#import timeit

def build_sts(u, args, strm, fout, agg_set, tb_set, sram_set, add_bounds, dim_max_val, fts, m, symbols, solver):
    
    
    # Open a file with a sequence
    fo = open(args.sequence, "r+")
    lines = fo.readlines()
    fo.close()

    CLK_CYCLES=len(lines)-1
   
    
    data_in = ''
    valid_in = ''
    data_out = ''
    valid_out = ''
    
    

    
             
    # look up the rstn by name
    rst_n = symbols[strm.rst_n_name]
#    print('rst_n',rst_n)


#-----------------------------------------------------

#    # look up the clock by name
#    clk = symbols[strm.clk_name]
##    print('CLK',clk)
#
#    # Start clock at 0 and toggle it every transition
#    # -- this is a bit complicated because clk is an input
#    # -- and initial states can only be over *states*
#
#    # Make a boolean clock state variable
#    # Note: by default the BTOR2Encoder makes all variables bitvectors
#    #       so clk is a bitvector of size 1
#    clk_state = fts.make_statevar("clk_state", solver.make_sort(sk.BOOL))
#
#    # Force clk_state and clk to be equivalent
#    fts.constrain_inputs(solver.make_term(po.Equal, clk_state, solver.make_term(po.Equal, clk, solver.make_term(1, clk.get_sort()))))
#
#    # Start the clock at 0
#    fts.constrain_init(solver.make_term(po.Not, clk_state))
#
#    # Toggle the clock in every transition
#    fts.assign_next(clk_state, solver.make_term(po.Not, clk_state))
    
    #       clk_0=0 --> clk-0=1 |                        |                clk_1=0      clk-1=1     clk_2=0 clk-2=1     clk-3 clk_3
    # state  x@0                |      x@1               |    x@1
    # input               y@0   |                   y@1  |
    
    #        x@0                |      x@1               |    x@2            x@3         x@4
    
    
    # clkstate_init0=F          |  clkstate-1=T          | clkstate_2=F              clkstate-3  clkstate_4 --> clkstate = (clk == 1)
    

    
    #set all set0 variables to 0 and set1 to 1
    for s in strm.set0:
        s_s = symbols[s]
        fts.constrain_inputs(solver.make_term(po.Equal, s_s, solver.make_term(0, s_s.get_sort())))
    for s in strm.set1:
        s_s = symbols[s]
        fts.constrain_inputs(solver.make_term(po.Equal, s_s, solver.make_term(1, s_s.get_sort())))

    
    # Now require that the configuration state is held constant
    # with the same trick using a new state variable
    # (because they're inputs also)

    for name in strm.config_names:
        cfg_term = symbols[name]
        # let's just double-check. if it's a state, don't need a new state
        if cfg_term in fts.statevars:
            cfg_state = cfg_term
        else:
            cfg_state = fts.make_statevar(name + '_state', cfg_term.get_sort())
            fts.constrain_inputs(solver.make_term(po.Equal, cfg_term, cfg_state))
            
        # keep it constant, e.g. cfg_state' = cfg_state
        fts.assign_next(cfg_state, cfg_state)

#----------------------------------------------------------------------------------------------------------------
    
    
    # unroll up to CLK_CYCLES and add init/trans to solver assertions
    solver.assert_formula(u.at_time(fts.init, 0))

    for i in range(CLK_CYCLES):
        solver.assert_formula(u.at_time(fts.trans, i))
        
    # proceess constraints for parameters
    for v in list(symbols.keys()):
        v_name = v[:v.find('[')]
        v_ind = v[v.find('[')+1:v.find(']')]
        if v_name in strm.var_array_inds and v_ind not in strm.var_array_inds[v_name]:
            assert v in strm.config_names
            solver.assert_formula(solver.make_term(po.Equal, u.at_time(symbols[v],0), solver.make_term(0, symbols[v].get_sort())))

    # add any constraints provided in the annotation file
    for t in strm.constr2terms:
        if 'if' !=  t[0] and 'SOLVE' !=  t[1]:
            signal = t[0]
            if ':' in signal:
                bounded_var_name = signal[:signal.find('[')]
                ind_start = signal[signal.find('[')+1:signal.find(':')]
                symb_start = False
                if ind_start in strm.vars:
                    ind_start = int(strm.vars[ind_start],0)
                    #symb_start = True
                elif ind_start.isdigit():
                    ind_start = int(ind_start,0)
                else: symb_start = True
                ind_end = signal[signal.find(':')+1:signal.find(']')]
                symb_end = False
                if ind_end in strm.vars:
                    ind_end = int(strm.vars[ind_end],0)
                    symb_end = True
                elif ind_end.isdigit():
                    ind_end = int(ind_end,0)
                else: symb_end = True
                if not symb_start and not symb_end:
                    if signal[:signal.find('[')] not in strm.var_array_inds:
                        for i in range(ind_start,ind_end+1):
                            bounded_var = symbols[bounded_var_name+'['+str(i)+']']
                            assert bounded_var_name+'['+str(i)+']' in strm.config_names
                            if  t[1] == '<=':
                                solver.assert_formula(solver.make_term(po.BVUle, u.at_time(bounded_var,0), solver.make_term(int(strm.vars[ t[2]],0), bounded_var.get_sort())))
                            elif  t[1] == '<':
                                solver.assert_formula(solver.make_term(po.BVUlt, u.at_time(bounded_var,0), solver.make_term(int(strm.vars[ t[2]],0), bounded_var.get_sort())))
                            else:
                                assert t[1] == '='
                                solver.assert_formula(solver.make_term(po.Equal, u.at_time(bounded_var,0), solver.make_term(int(t[2],0), bounded_var.get_sort())))
                            
                else: #implement later when suport for universal quantifiers is added
                    print (t,'not supported yet')
            else:
                bounded_var_name = t[0]
                assert bounded_var_name in list(symbols.keys())
                bounded_var = symbols[bounded_var_name]
                assert bounded_var_name in strm.config_names
                if  t[1] == '<=':
                    solver.assert_formula(solver.make_term(po.BVUle, u.at_time(bounded_var,0), solver.make_term(int(strm.vars[ t[2]],0), bounded_var.get_sort())))
                    
                elif  t[1] == '<':
                    solver.assert_formula(solver.make_term(po.BVUlt, u.at_time(bounded_var,0), solver.make_term(int(strm.vars[ t[2]],0), bounded_var.get_sort())))
                else:
                    assert t[1] == '='
                    solver.assert_formula(solver.make_term(po.Equal, u.at_time(bounded_var,0), solver.make_term(int(t[2],0), bounded_var.get_sort())))
        
        elif 'if' ==  t[0]:
            assert  t[6] == '='
            if_var_name = t[1]
            if_var = symbols[if_var_name]
            signal = t[5]
            if ':' in signal:
                then_var_name = signal[:signal.find('[')]
                ind_start = signal[signal.find('[')+1:signal.find(':')]
                symb_start = False
                if ind_start in strm.vars:
                    ind_start = int(strm.vars[ind_start],0)
                elif ind_start.isdigit():
                    ind_start = int(ind_start,0)
                else: symb_start = True
                ind_end = signal[signal.find(':')+1:signal.find(']')]
                symb_end = False
                if ind_end in strm.vars:
                    ind_end = int(strm.vars[ind_end],0)
                    symb_end = True
                elif ind_end.isdigit():
                    ind_end = int(ind_end,0)
                else: symb_end = True
                
                if not symb_start and not symb_end:
                    if signal[:signal.find('[')] not in strm.var_array_inds:
                        for i in range(ind_start,ind_end+1):
                            bounded_var = symbols[bounded_var_name+'['+str(i)+']']
                            if  t[2] == '<=':
                                solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.BVUle,u.at_time(if_var,0),
                                solver.make_term(int( t[3],0), if_var.get_sort())),
                                solver.make_term(po.Equal,u.at_time(then_var,0), solver.make_term(int( t[7],0), then_var.get_sort()))))
                            if  t[2] == '<':
                                solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.BVUlt,u.at_time(if_var,0) ,solver.make_term(int( t[3],0), if_var.get_sort())), solver.make_term(po.Equal,u.at_time(then_var,0) ,solver.make_term(int( t[7],0), then_var.get_sort()))))
                            if  t[2] == '=':
                                solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.Equal,u.at_time(if_var,0) ,
                                solver.make_term(int( t[3],0), if_var.get_sort())), solver.make_term(po.Equal,u.at_time(then_var,0) ,
                                solver.make_term(int( t[7],0), then_var.get_sort()))))
                else: #implement later when suport for universal quantifiers is added
                    print (t,'not supported yet')
            else:
                then_var_name = t[5]
                then_var = symbols[then_var_name]

                assert if_var_name in strm.config_names
                assert then_var_name in strm.config_names
                if  t[2] == '<=':
                    bounded_var = symbols[bounded_var_name+'['+str(i)+']']
                    solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.BVUle,u.at_time(if_var,0),
                    solver.make_term(int( t[3],0), if_var.get_sort())),
                    solver.make_term(po.Equal,u.at_time(then_var,0), solver.make_term(int( t[7],0), then_var.get_sort()))))
                
                if  t[2] == '<':
                    solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.BVUlt,u.at_time(if_var,0) ,solver.make_term(int( t[3],0), if_var.get_sort())), solver.make_term(po.Equal,u.at_time(then_var,0) ,solver.make_term(int( t[7],0), then_var.get_sort()))))
                if  t[2] == '=':
                    solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.Equal,u.at_time(if_var,0) ,
                    solver.make_term(int( t[3],0), if_var.get_sort())), solver.make_term(po.Equal,u.at_time(then_var,0) ,
                    solver.make_term(int( t[7],0), then_var.get_sort()))))
                    
                
        else:
            signal = t[0]
            signal_name = signal[:signal.find('[')]
            assert ind_start == int(0)
            signal_size = 0
            for s in list(symbols.keys()):
                if signal_name in s:
                    signal_size += 1
            for i in range(signal_size):
                for j in range(i,signal_size):
                    entry_name = signal_name+'['+str(j)+']'
                    entry = symbols[entry_name]
                    assert entry_name in strm.config_names
                    ind_end = signal[signal.find(':')+1:signal.find(']')]
                    solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.Equal,u.at_time(symbols[ind_end],0),
                    solver.make_term(i, symbols[ind_end].get_sort())),
                    solver.make_term(po.Equal,u.at_time(entry,0), solver.make_term(0, entry.get_sort()))))
    
   # Set sequence processing
    new_sequence_format = True
    sequence_property = True

    incomplete_sequence_in = True #for tb only it is False
    incomplete_sequence_out = True #for sram only it is False

    if tb_set:
        incomplete_sequence_in = False
    elif sram_set:
        incomplete_sequence_out = False

    if args.agg_solved != None or args.tb_solved != None or args.caggtbfirst or args.caggtbmin:
        modular = True
    else:
        modular = False

##############################  Modular plug in agg/tb ##############################

    if modular:
        solution = []
        mod_lines = []
        modules_solved = []
        if args.agg_solved != None:
            modules_solved.append(args.agg_solved)
        if args.tb_solved != None:
            modules_solved.append(args.tb_solved)
        if args.caggtbfirst or args.caggtbmin:
            assert sram_set
            assert not (args.caggtbfirst and args.caggtbmin)
            if args.optimize == 0:
               agg_file = output_file_min
               tb_file = output_file_min
            else:
                if args.caggtbfirst:
                    agg_file = output_file_first
                    tb_file = output_file_first
                else:
                    agg_file = output_file_min
                    tb_file = output_file_min
            agg_file = agg_file.replace("_modular_","_")
            tb_file = tb_file.replace("_modular_","_")
            agg_file = agg_file.replace("_first_print","_print")
            tb_file = tb_file.replace("_first_print","_print")
            agg_file = agg_file.replace("_min_print","_print")
            tb_file = tb_file.replace("_min_print","_print")
            agg_file = agg_file.replace("sram_opt","agg_opt")
            tb_file = tb_file.replace("sram_opt","tb_opt")
            agg_file = agg_file.replace("sram_","agg_")
            tb_file = tb_file.replace("sram_","tb_")
            agg_file = agg_file.replace("_sram/","_agg/")
            tb_file = tb_file.replace("_sram/","_tb/")

            modules_solved.append(agg_file)
            modules_solved.append(tb_file)
        #if args.caggtbmin:
        #    assert sram_set
        #    agg_file = output_file_min
        #    tb_file = output_file_min
        #    agg_file = agg_file.replace("sram_opt","agg_opt")
        #    tb_file = tb_file.replace("sram_opt","tb_opt")
        #    modules_solved.append(agg_file)
        #    modules_solved.append(tb_file)

        print("modules_solved",modules_solved)
#        for mod_file in sys.argv[3:]:
        for mod_file in modules_solved:
            # Open a file with one of the two an agg or tb solution
            fo = open(mod_file, "r+")
            mod_lines = fo.readlines()
            for mod_line in mod_lines:
                solution.append(mod_line)
            # Close opend file
            fo.close()
        module_confs = []
        for conf_val in solution:
            conf_val = conf_val.strip()
            conf_val = conf_val.split()
            print (conf_val)
            fout.write(str(conf_val))
            fout.write("\n")
            if 'config' not in conf_val[0]: continue

            suffix = conf_val[0][conf_val[0].rfind('_')+1:-2]

            if suffix.isdigit():
                conf = conf_val[0][8:conf_val[0].rfind('_')]+'['+suffix+']'
            else:
                conf = conf_val[0][8:-2]
            val = int(conf_val[2],0) #fix sequence later

            if conf in m.shared_agg_sram_tb and m.shared_agg_sram_tb[conf] in strm.config_names:
                module_conf = symbols[m.shared_agg_sram_tb[conf]]
                solver.assert_formula(solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(val, module_conf.get_sort())))
                module_confs.append("    config[\""+m.shared_agg_sram_tb[conf]+"\"] = "+str(val))
        for each in module_confs:
            print (each)
            fout.write(str(each))
            fout.write("\n")

    #  add bounds on ranges, strides, starting addresses, dimensionalities
    if new_sequence_format:
        ln0 = lines[0]
        ln0 = ln0.strip()
        ln0 = ln0.replace(' ', '')
        ln0 = ln0.replace('valid_in,', m.valids['valid_in']+",")
        ln0 = ln0.replace('valid_out', m.valids['valid_out'])
        ln0 = ln0.replace('data_in,', m.data['data_in']+",")
        ln0 = ln0.replace('data_out,', m.data['data_out']+",")
        seq_names = ln0.split(',')

        for j in range(len(seq_names)):
            seq_names[j] = seq_names[j].strip()
        if sequence_property:
            assert (len(seq_names) == 4)
            data_in = seq_names[0]
            valid_in = seq_names[1]
            data_out = seq_names[2]
            valid_out = seq_names[3]
            if valid_in not in strm.seq_in: strm.seq_in.append(valid_in)
            if valid_out not in strm.seq_out: strm.seq_out.append(valid_out)

        else:
            data_in = seq_names[0]
            data_out = seq_names[1]

    else:
        ln0 = lines[0]
        ln0 = ln0.strip()
        ln0 = ln0.replace(',', '')
        ln0 = ln0.replace('valid_in', m.valids['valid_in'])
        ln0 = ln0.replace('valid_out', m.valids['valid_out'])
        ln0 = ln0.replace('data_in', m.data['data_in'])
        ln0 = ln0.replace('data_out', m.data['data_out'])
        seq_names = ln0.split(' ')
    
    seq_vals_all_lines = []
    
    for i in range(CLK_CYCLES):
        if new_sequence_format:
            ln = lines[i+1]
            ln = ln.strip()
            seq_vals = ln.split(',')
            for j in range(len(seq_vals)):
                seq_vals[j] = seq_vals[j].strip()
        else:
            ln = lines[i+1]
            ln = ln.strip()
            ln = ln.replace('], [','],[')
            ln = ln.replace(',', '')
            seq_vals = ln.split(' ')
        seq_vals_all_lines.append(seq_vals)


    valid_in_cycle = 0
    valid_out_cycle = 0

    if add_bounds:

        i = 0
        valid_in_col = None
        if sequence_property:
            valid_in_col = 1
        else:
            valid_in_col = 0
        while (i < CLK_CYCLES and seq_vals_all_lines[i][valid_in_col] == "0"):
            valid_in_cycle += 1
            i += 1
        i = 0
        while (i < CLK_CYCLES and seq_vals_all_lines[i][-1] == "0"):
            valid_out_cycle += 1
            i += 1
        
        
        #write_ids = None
        #if agg_set: write_ids = agg_write_ids
        #elif tb_set: write_ids = tb_write_ids
        
        bound_ranges_strides_st_addr_dim (u, add_bounds, agg_set, tb_set, sram_set, valid_in_cycle, CLK_CYCLES, dim_max_val, m, symbols, m.group_ids, strm.config_names, m.stride_start_addr_ids, solver)


    for i in range(CLK_CYCLES):
        seq_vals = seq_vals_all_lines[i]
        seq_vals_prev = seq_vals
        seq_vals_next = seq_vals
        #use this if valids need to be shifted either up or down.
#        if i > 0: seq_vals_prev = seq_vals_all_lines[i-1]
#        if i < CLK_CYCLES-1: seq_vals_next = seq_vals_all_lines[i+1]
        
        solver.assert_formula(solver.make_term(po.Equal, u.at_time(rst_n,i), solver.make_term(1, rst_n.get_sort())))

        if args.verbose:
            print (seq_vals)
            fout.write(seq_vals)
            fout.write("\n")
        for s_in in strm.seq_in:
            ss_in = symbols[s_in]
            dims = []
            if s_in[-1:] != ']': #not multi-dimensional
                ind_s_in = seq_names.index(s_in)
                assert seq_vals[ind_s_in][-1:] != ']'
                val = int(seq_vals[ind_s_in],0)#fix sequence later
                if s_in == data_in: val += 1
                dim_val = None
            else:
                s_in_name = s_in[:s_in.find('[')]
                ind_s_in = seq_names.index(s_in_name)
                s_in_val = seq_vals[ind_s_in].replace('[', ' ')
                s_in_val = s_in_val.replace(']', ' ')
                s_in_val = s_in_val.split()
                
                rem_dims = s_in[s_in.find('['):]
                while (rem_dims != ''):
                    dims.append(int(rem_dims[1:rem_dims.find(']')],0))
                    rem_dims = rem_dims[rem_dims.find(']')+1:]
                assert len(dims) <= 3
                assert len(dims) == len(strm.data_in_size)
                dim_val = None
                if len(dims) == 3:
                    assert (dims[0] == 0 and dims[1] == 0)
                    dim_val = dims[0]*(strm.data_in_size[1]+1)*(strm.data_in_size[2]+1)+dims[1]*(strm.data_in_size[2]+1)+dims[2]
                elif len(dims) == 2:
                    dim_val = dims[0]*(strm.data_in_size[1]+1)+dims[1]
                else:
                    dim_val = dims[0]
                if s_in_val[dim_val] == 'X':
                    val = 'X'
                else:
                    val = int(s_in_val[dim_val],0)#fix sequence later
                if s_in_name == data_in and val != 'X': val += 1
            if incomplete_sequence_in:
                if len(dims) > 0 and strm.data_in_size[0] > 0:
#                if agg_set:
                    # to support 2 port valids
                    if seq_vals[1] != "0" or s_in == valid_in:#in current design valid_in is an output, redundant s_in here, UPDATE: changed this valid_in is input
                        if (dims[0] == 0 and seq_vals[1] == "1") or (dims[0] == 1 and seq_vals[1] == "2") or (seq_vals[1] == "3") or s_in == valid_in:
                            solver.assert_formula(solver.make_term(po.Equal, u.at_time(ss_in, i), solver.make_term(val, ss_in.get_sort())))
                            if args.verbose:
                                print("IN-2-port:",s_in,"=", val)#, solver.make_term(po.Equal, u.at_time(ss_in, i), solver.make_term(val, ss_in.get_sort())))
                                fout.write("IN-2-port: "+s_in+" = "+val)
                                fout.write("\n")
                else: #if tb_set or sram_set:
                    # to support 1 port valids
                    if seq_vals_prev[1] != "0" or s_in == valid_in:#in current design valid_in is an output, redundant s_in here
                        solver.assert_formula(solver.make_term(po.Equal, u.at_time(ss_in, i), solver.make_term(val, ss_in.get_sort())))
                        if args.verbose:
                            print("IN-1-port:",s_in,"=", val)#, solver.make_term(po.Equal, u.at_time(ss_in, i), solver.make_term(val, ss_in.get_sort())))
                            fout.write("IN-1-port: "+s_in+" = "+val)
                            fout.write("\n")
            else:
                if val != 'X':
                    solver.assert_formula(solver.make_term(po.Equal, u.at_time(ss_in, i), solver.make_term(val, ss_in.get_sort())))
                    if args.verbose:
                        print("IN-all:",s_in,"=", val)#, solver.make_term(po.Equal, u.at_time(ss_in, i), solver.make_term(val, ss_in.get_sort())))
                        fout.write("IN-all: "+s_in+" = "+val)
                        fout.write("\n")
        
        for s_out in strm.seq_out:
            ss_out = symbols[s_out]
            dims = []
            if s_out[-1:] != ']': #not multi-dimensional
                ind_s_out = seq_names.index(s_out)
                assert seq_vals[ind_s_out][-1:] != ']'
                val = int(seq_vals[ind_s_out],0)#fix sequence later
                if s_out == data_out: val += 1
                dim_val = None
            else:
                s_out_name = s_out[:s_out.find('[')]
                ind_s_out = seq_names.index(s_out_name)
                s_out_val = seq_vals[ind_s_out].replace('[', ' ')
                s_out_val = s_out_val.replace(']', ' ')
                s_out_val = s_out_val.split()
                
                rem_dims = s_out[s_out.find('['):]
                while (rem_dims != ''):
                    dims.append(int(rem_dims[1:rem_dims.find(']')],0))
                    rem_dims = rem_dims[rem_dims.find(']')+1:]
                assert len(dims) <= 3
                assert len(dims) == len(strm.data_out_size)
                if len(dims) == 3:
                    assert (dims[0] == 0 and dims[1] == 0)
                    dim_val = dims[0]*(strm.data_out_size[1]+1)*(strm.data_out_size[2]+1)+dims[1]*(strm.data_out_size[2]+1)+dims[2]
                elif len(dims) == 2:
                    dim_val = dims[0]*(strm.data_out_size[1]+1)+dims[1]
                else:
                    dim_val = dims[0]
                if s_out_val[dim_val] == 'X':
                    val = 'X'
                else:
                    val = int(s_out_val[dim_val],0)#fix sequence later
                if s_out_name == data_out and val != 'X': val += 1
            if incomplete_sequence_out:
                if len(dims) > 0 and strm.data_out_size[0] > 0:#if tb_set: #this needs to be changed in general for SRAM to strm.data_out_size[1]*strm.data_out_size[0]
                    #to support 2 port valids
                    if seq_vals_prev[-1] != "0" or s_out == valid_out:# or s_out == valid_in:
                        if (dims[0] == 0 and seq_vals_prev[-1] == "1") or (dims[0] == 1 and seq_vals_prev[-1] == "2") or seq_vals_prev[-1] == "3" or s_out == valid_out:# or s_out == valid_in:
                            solver.assert_formula(solver.make_term(po.Equal, u.at_time(ss_out, i), solver.make_term(val, ss_out.get_sort())))
                            if args.verbose:
                                print("OUT-2-port:",s_out, val)#, dim_val, solver.make_term(po.Equal, u.at_time(ss_out, i), solver.make_term(val, ss_out.get_sort())))
                                fout.write("OUT-2-port: "+s_out+" = "+val)
                                fout.write("\n")
                else:#if agg_set or sram_set:
                    #to support 1 port valids
                    if seq_vals[-1] != "0" or s_out == valid_out:
#                        print("added out:",s_out, val)
                        solver.assert_formula(solver.make_term(po.Equal, u.at_time(ss_out, i), solver.make_term(val, ss_out.get_sort())))
                        if args.verbose:
                            print("OUT-1-port: "+s_out+" = "+val)
                            fout.write("OUT-1-port: "+s_out+" = "+val)
                            fout.write("\n")
            else:
                if val != 'X':
                    solver.assert_formula(solver.make_term(po.Equal, u.at_time(ss_out, i), solver.make_term(val, ss_out.get_sort())))
                    if args.verbose:
                        print("OUT-all:",s_out,"=", val)
                        fout.write("OUT-all: "+s_out+" = "+val)
                        fout.write("\n")
    return u
