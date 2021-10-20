###############################################################################
#  file -- solve.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Impliments the main configuration solving routine.
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
#import timeit

    
class solution:
    get_min_solution = None
        
    solve_time = 0
    
    interval_high = False
    interval_low = False
    
def extract_assignment (names, u, symbols, solver):
    assignment = {}
    for conf_name in names:
        conf_term = symbols[conf_name]
        assignment[conf_term] = solver.get_value(u.at_time(conf_term, 0))
    return assignment


def solve_lake(self, strm, optimize_bit_width, binary_search, current_opt_ass, u, first_solution_found, group_names_i, obj_term_keys_i, indicators, dim_names, m, fout, prnt, symbols, solver):

    self.interval_high = False
    self.interval_low = False
    
    #print ("======================== Solve lake start ===============================")
    solver.push()

    if first_solution_found:
        build_obj_term_comps = {}
        for id in m.group_ids:
            if len(group_names_i[id]) > 0:
                values = list(group_names_i[id].values())
                keys = list(group_names_i[id].keys())
                if "starting_addr" in keys[0] or "strides" in keys[0]:
                    build_obj_term_comps[id] = solver.make_term(0, values[0].get_sort())
                else:
                    build_obj_term_comps[id] = solver.make_term(1, values[0].get_sort())

    for key in current_opt_ass:
        if "obj_term" in key: continue
        conf = symbols[key]
        if "dimensionality" in key:
            solver.assert_formula(solver.make_term(po.Equal, u.at_time(conf,0), solver.make_term(current_opt_ass[key], conf.get_sort())))

    solver.push()
    for key in current_opt_ass:
        if "obj_term" in key: continue
        conf = symbols[key]
        if "dimensionality" not in key:
            for id in m.group_ids:
                if len(group_names_i[id]) > 0:
                    if key in group_names_i[id].keys() and (("[" in key and int(key[key.find('[')+1:key.find(']')],0) < current_opt_ass[dim_names[id]]) or "[" not in key):

                        sum = BVAdde(build_obj_term_comps[id], u.at_time(conf,0), solver)
                        prod = BVMule(build_obj_term_comps[id], u.at_time(conf,0), solver)
                        
                        keys = list(group_names_i[id].keys())
                        if "starting_addr" in keys[0] or "strides" in keys[0]:
                            build_obj_term_comps[id] = sum
                        else:
                            build_obj_term_comps[id] = prod
    r_is_sat = False
        
    if first_solution_found:
        term_low = obj_term_keys_i[-2]
        term_high = obj_term_keys_i[-1]

        if binary_search:
            if len(build_obj_term_comps) > 0:
                values = list(build_obj_term_comps.values())
                sum_groups = values[0]
                for i in range(1,len(values)):
                    sum_groups = BVAdde(sum_groups, values[i], solver)
                term = BVUgee(sum_groups, current_opt_ass[term_low], solver)
                solver.assert_formula(term)
                solver.assert_formula(BVUlte(sum_groups, solver.make_term(po.BVUdiv, current_opt_ass[term_high], solver.make_term(2, current_opt_ass[term_high].get_sort())), solver))
            
                if optimize_bit_width:
                    r = solver.check_sat_assuming(indicators)
                else:
                    r = solver.check_sat()
                if r.is_sat():
                    self.interval_low = True
                    r_is_sat = True
                    solver.pop()
                    solver.pop()
                else:
                    self.interval_high = True
                    solver.pop()
                    solver.push()
                    term = solver.make_term(po.BVUdiv, current_opt_ass[term_high], solver.make_term(2, current_opt_ass[term_high].get_sort()))
                    if int(current_opt_ass[term_high])/2 < int(current_opt_ass[term_low]):
                        term = current_opt_ass[term_low]
                        
                    solver.assert_formula(BVUgee(sum_groups, term, solver))
                    solver.assert_formula(BVUlte(sum_groups, current_opt_ass[term_high], solver))

                    if optimize_bit_width:
                        r = solver.check_sat_assuming(indicators)
                    else:
                        r = solver.check_sat()
                    if r.is_sat():
                        r_is_sat = True

                    solver.pop()
                    solver.pop()

            else:
                assert (False) #no dim without other group members
        else: #linear search
        
            if len(build_obj_term_comps) > 0:
                values = list(build_obj_term_comps.values())
                sum_groups = values[0]
                for i in range(1,len(values)):
                    sum_groups = BVAdde(sum_groups, values[i], solver)
                
                sum_current_opt_ass = current_opt_ass[obj_term_keys_i[0]]
                for i in range(1,len(obj_term_keys_i)-2):
                    sum_current_opt_ass = BVAdde(sum_current_opt_ass, current_opt_ass[obj_term_keys_i[i]], solver)
                    
                solver.assert_formula(BVUlte(sum_groups, sum_current_opt_ass, solver))
 
                if optimize_bit_width:
                    r = solver.check_sat_assuming(indicators)
                else:
                    r = solver.check_sat()
                if r.is_sat(): r_is_sat = True
                solver.pop()
                solver.pop()
            else:
                assert (False) #no dim without other group members
    else: # no first_solution_found yet
        if optimize_bit_width:
            r = solver.check_sat_assuming(indicators)
        else:
            #print("check sat start")
            r = solver.check_sat()
            #print("check sat end")
        if r.is_sat(): r_is_sat = True
    
    if not first_solution_found:
        solver.pop()
        solver.pop()
    
    self.solve_time = time.perf_counter()
    
    # now you can get model values
    # for example
    
#
#    if r.is_sat():
#        print("_________________intermediate solution:____________________")
#        configuration = {}
#        for name in strm.config_names:
#            cfg_term = symbols[name]
#            # don't forget to use the timed symbol
#            val = solver.get_value(u.at_time(cfg_term, 0))
#            val_dec = int (val)
#            #print('{} := {}'.format(name, val))
#            current_ass[name]=val_dec
#            if name[-1:] != ']':
#                print('    config["{}"] = {}'.format(name, val_dec))
#            else:
#                name_modif = name[:name.find('[')]+'_'+name[name.find('[')+1:name.find(']')]
#                print('    config["{}"] = {}'.format(name_modif, val_dec))
#            configuration[symbols[name]] = val
#        print("____________________________________________________________")
    
    if r_is_sat:

        sys.stdout = prnt.new_stdout
        self.get_min_solution = []
        print("____________________________________________________________")
        fout.write("____________________________________________________________")
        fout.write("\n")
        configuration = {}
        for conf_name in strm.config_names:
            cfg_term = symbols[conf_name]
            # don't forget to use the timed symbol
            val = solver.get_value(u.at_time(cfg_term, 0))
            #print('val',val,cfg_term)
            val_dec = int (val)
            #print('{} := {}'.format(conf_name, val))
            #current_ass[conf_name]=val_dec
            if conf_name[-1:] != ']':
                print('    config["{}"] = {}'.format(conf_name, val_dec))
                fout.write('    config["{}"] = {}'.format(conf_name, val_dec))
                fout.write("\n")
                self.get_min_solution.append('    config["{}"] = {}'.format(conf_name, val_dec))
            else:
                conf_name_modif = conf_name[:conf_name.find('[')]+'_'+conf_name[conf_name.find('[')+1:conf_name.find(']')]
                print('    config["{}"] = {}'.format(conf_name_modif, val_dec))
                fout.write('    config["{}"] = {}'.format(conf_name_modif, val_dec))
                fout.write("\n")
                self.get_min_solution.append('    config["{}"] = {}'.format(conf_name_modif, val_dec))
            configuration[symbols[conf_name]] = val
        
        prnt.set_output()
   # print ("======================== Solve lake end ===============================")
    return r_is_sat



