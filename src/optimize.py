###############################################################################
#  file -- optimize.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Implements functions for the optimization routine.
#  Optimization layers:
#  I)   minimize Sum (dim_i), prioritize write dims over read dims.
#  II)  minimize Sum (Prod (ranges_i + 2)).
#  III) minimize Sum (Strides_i).
#  IV)  minimize Sum (Starting_addr_i).
#
###############################################################################

from solve import *

def propagate_partial_ass_for_opt (u, m, dim_names, min_sum, optimize_bit_width, optimize_depth, r_is_sat, ass_to_opt, min_loop_ass, partial_assignment, group_names_i, obj_term_keys_i, interval_low, interval_high, total_latest_solution_to_opt_next, symbols, solver):

    if (optimize_depth > 1):
        if r_is_sat:
            partial_assignment = {}
            names = []
            for id in m.group_ids:
                for key in group_names_i[id].keys():
                    names.append(key)
            partial_assignment = extract_assignment(names, u, symbols, solver)
        elif not (optimize_bit_width and first_solution_found):
            partial_assignment = {}
        else:
            partial_assignment = total_latest_solution_to_opt_next
            
        optimize_fun_update(r_is_sat, m, dim_names, min_sum, optimize_bit_width, ass_to_opt, min_loop_ass, partial_assignment, group_names_i, obj_term_keys_i, interval_low, interval_high, symbols, solver)

    


# Updates the necessary current values after each optimization call.
# obj_term_keys collects names for all current values of the objective term components as well as updates the interval [low, high) for the objective term value.
def optimize_fun_update (r_is_sat, m, dim_names, min_sum, optimize_bit_width, ass_to_opt, min_loop_ass, partial_assignment, group_names_i, obj_term_keys_i, interval_low, interval_high, symbols, solver):

    if r_is_sat or ((not r_is_sat) and optimize_bit_width and len(partial_assignment)):
        term_low = obj_term_keys_i[-2]
        term_high = obj_term_keys_i[-1]

        for id in m.group_ids:
            for signal in list(group_names_i[id].keys()):
                ass_to_opt[signal] = partial_assignment[symbols[signal]]
        build_obj_term_comps = {}

        for id in m.group_ids:
            if len(group_names_i[id]) > 0:
                keys = list(group_names_i[id].keys())
                if "starting_addr" in keys[0] or "strides" in keys[0]:
                    build_obj_term_comps[id] = solver.make_term(0, symbols[keys[0]].get_sort())
                else:
                    build_obj_term_comps[id] = solver.make_term(1, symbols[keys[0]].get_sort())
                for key in group_names_i[id].keys():

                    s_key = symbols[key]

                    if ("[" in key and int(key[key.find('[')+1:key.find(']')],0) < min_loop_ass[dim_names[id]]) or "[" not in key:
                        if "starting_addr" in key or "strides" in key:
                            build_obj_term_comps[id] = BVAdde(build_obj_term_comps[id], partial_assignment[s_key], solver)
                        else:
                            build_obj_term_comps[id] = BVMule(build_obj_term_comps[id], partial_assignment[s_key], solver)
                for key in obj_term_keys_i:
                    if id in key:
                        ass_to_opt[key] = build_obj_term_comps[id]
                        break
            else:
                for key in obj_term_keys_i:
                    if id in key:
                        keys = list(group_names_i[id].keys())
                        ass_to_opt[key] = None
                        break
        
        if len(build_obj_term_comps) > 0:
            values = list(build_obj_term_comps.values())
            sum_groups = values[0]
            for i in range(1,len(values)):
                sum_groups = BVAdde(sum_groups, values[i], solver)
            ass_to_opt[term_high] = sum_groups
        else:
            assert (False) #no dim without other group members

        if interval_high:
            ass_to_opt[term_low] =  solver.make_term(po.BVUdiv, min_loop_ass[term_high], solver.make_term(2, min_loop_ass[term_high].get_sort()))
                
        else:
            keys = list(group_names_i[m.group_ids[0]])
            ass_to_opt[term_low] = solver.make_term(min_sum, symbols[keys[0]].get_sort())

#        print("interval: (",int(ass_to_opt[obj_term_keys_i[-2]]),int(ass_to_opt[obj_term_keys_i[-1]]),"), interval_low",interval_low, "interval_high",interval_high)

    else:
        ass_to_opt = {}

    return r_is_sat

def gen_dim_vals (slv, strm, u, m, fout, output_file_first, optimize_bit_width, binary_search, partial_assignment, unrolled_ts, optimize_depth, sum_left, dim_names, dim_max_val, min_sum, dims_left, list_keys, ass_to_opt, min_loop_ass, opt_steps, group_names, obj_term_keys, indicators, prnt, tm, sys_argv, symbols, solver):
    
    partial_latest_solution_to_fix = {}
    total_latest_solution_to_opt_next = {}
    
    assert (optimize_depth >= 1)
    
    cur_key_ind = len(dim_names) - dims_left
    item = dim_names[list_keys[cur_key_ind]]


    if dims_left == 1 and sum_left <= dim_max_val:
 
        if optimize_bit_width:
            bw = {}
            bw_last_sat = {}
            
            for id in m.group_ids:
                for addr in m.groups_data["starting_addr"][id].keys():
                    st_addr = symbols[addr]
                    bw[addr] = 2
                    bw_last_sat[addr] = 2
            
    
        min_loop_ass[item] = sum_left

        first_solution_found = (len(min_loop_ass) > len(dim_names))
        iter_optim_depth = optimize_depth

        is_unsat = True
        increase_bound = True

        while is_unsat and increase_bound:
            if optimize_bit_width:
                solver.push()
                
                for id in group_ids:
                    for addr in groups_data["starting_addr"][id].keys():
                        st_addr = symbols[addr]
                        if bw[addr] < pow(2, st_addr.get_sort().get_width()):
                            solver.assert_formula(solver.make_term(po.BVUlt, unrolled_ts.at_time(st_addr,0), solver.make_term(bw[addr], st_addr.get_sort())))
                            solver.assert_formula(solver.make_term(po.Implies, indicators[addr], solver.make_term(po.BVUlt, unrolled_ts.at_time(st_addr,0), solver.make_term(bw[addr], st_addr.get_sort()))))
                core = []
            else: increase_bound = False

            first_solution_found = (len(min_loop_ass) > len(dim_names))
            res_is_sat = solve_lake(slv, strm, optimize_bit_width, binary_search, min_loop_ass,unrolled_ts, first_solution_found, group_names[optimize_depth-iter_optim_depth], obj_term_keys[optimize_depth-iter_optim_depth], indicators.values(), dim_names, m, fout, prnt, symbols, solver)
            
            sys.stdout = prnt.old_stdout
            
            propagate_partial_ass_for_opt (u, m, dim_names, min_sum, optimize_bit_width, optimize_depth, res_is_sat, ass_to_opt, min_loop_ass, partial_assignment, group_names[optimize_depth-iter_optim_depth], obj_term_keys[optimize_depth-iter_optim_depth], slv.interval_low, slv.interval_high, total_latest_solution_to_opt_next, symbols, solver)
            
            
            if optimize_bit_width:
                solver.pop()

            if res_is_sat:
                first_solution_found = True
                print("first solution found!")
                opt_steps += 1
                is_unsat = False
                
                if optimize_bit_width:
                    for indc in indicators.keys():
                        bw_last_sat[indc] = bw[indc]

                
                for id in m.group_ids:
                    for conf_name in group_names[optimize_depth-iter_optim_depth][id]:
                        conf_term = symbols[conf_name]
                        partial_latest_solution_to_fix[conf_term] = solver.get_value(unrolled_ts.at_time(conf_term, 0))
                                                                    
                if iter_optim_depth >= 2:
                    for conf_name in strm.config_names:
                        conf_term = symbols[conf_name]
                        total_latest_solution_to_opt_next[conf_term] = solver.get_value(unrolled_ts.at_time(conf_term, 0))


                sub_res_is_sat = True
                new_opt_layer = False
                at_least_one_layer_sat = False
                while res_is_sat:
                    while sub_res_is_sat or increase_bound:
                        print("OPT STEP", opt_steps)
                        if opt_steps == 1 and sub_res_is_sat:
                            end = time.perf_counter()

                            prnt.print_first_solution (fout, tm, slv, sys.argv, output_file_first)

                            if optimize_depth < 2:
                                break

                        if new_opt_layer and len(total_latest_solution_to_opt_next):
                            at_least_one_layer_sat = True

                            end = time.perf_counter()
                            
                            prnt.print_opt_layer (fout, tm, slv, sys_argv, optimize_depth, iter_optim_depth)
                            
                            optimize_fun_update(True, m, dim_names, min_sum, optimize_bit_width, ass_to_opt, min_loop_ass, total_latest_solution_to_opt_next, group_names[optimize_depth-iter_optim_depth], obj_term_keys[optimize_depth-iter_optim_depth], False, False, symbols, solver)
                            
                            if optimize_bit_width:
                                for indc in indicators.keys():
                                    bw[indc] = bw_last_sat[indc]
                            
                        new_opt_layer = False
                        current_opt_ass = {}

                        for key in min_loop_ass:
                            current_opt_ass[key] = min_loop_ass[key]
                        for key in ass_to_opt:
                            current_opt_ass[key] = ass_to_opt[key]

                        if optimize_bit_width:
                            solver.push()
                            
                            for id in m.group_ids:
                                for addr in m.groups_data["starting_addr"][id].keys():
                                    st_addr = symbols[addr]
                                    if bw[addr] <= st_addr.get_sort().get_width():
                                        solver.assert_formula(solver.make_term(po.BVUlt, unrolled_ts.at_time(st_addr,0), solver.make_term(bw[addr], st_addr.get_sort())))
                                        solver.assert_formula(solver.make_term(po.Implies, indicators[addr], solver.make_term(po.BVUlt, unrolled_ts.at_time(st_addr,0), solver.make_term(bw[addr], st_addr.get_sort()))))
                        
                        sub_res_is_sat = solve_lake(slv, strm, optimize_bit_width, binary_search, current_opt_ass, unrolled_ts, first_solution_found, group_names[optimize_depth-iter_optim_depth], obj_term_keys[optimize_depth-iter_optim_depth], indicators.values(), dim_names, m, fout, prnt, symbols, solver)
                        
                        sys.stdout = prnt.old_stdout

                        propagate_partial_ass_for_opt(u, m, dim_names, min_sum, optimize_bit_width, optimize_depth, sub_res_is_sat, ass_to_opt, current_opt_ass, partial_assignment, group_names[optimize_depth-iter_optim_depth], obj_term_keys[optimize_depth-iter_optim_depth], slv.interval_low, slv.interval_high, total_latest_solution_to_opt_next, symbols, solver)

                        if optimize_bit_width:
                            solver.pop()
                        
                        if sub_res_is_sat:
                            if optimize_bit_width:
                                for indc in indicators.keys():
                                    bw_last_sat[indc] = bw[indc]

                            opt_steps += 1
                            
                            for id in m.group_ids:
                                for conf_name in group_names[optimize_depth-iter_optim_depth][id]:
                                    conf_term = symbols[conf_name]
                                    partial_latest_solution_to_fix[conf_term] = solver.get_value(unrolled_ts.at_time(conf_term, 0))
                                                                                
                            if iter_optim_depth >= 2:
                                for conf_name in strm.config_names:
                                    conf_term = symbols[conf_name]
                                    total_latest_solution_to_opt_next[conf_term] = solver.get_value(unrolled_ts.at_time(conf_term, 0))
                                
                        elif optimize_bit_width:
                            core = []

                            core = solver.get_unsat_core()
                            increase_bound = False
                            if len(core) == 0:
                                for indc in indicators.keys():
                                    if bw[indc] < pow(2, symbols[indc].get_sort().get_width()):
                                        bw[indc] = 2*bw[indc]
                                        increase_bound = True
                            else:
                                for indc in indicators.keys():
                                    if indicators[indc] in core and bw[indc] < pow(2, symbols[indc].get_sort().get_width()):
                                        increase_bound = True
                                        bw[indc] = 2*bw[indc]
                            print ("increase_bound ------------",increase_bound)

                            
                    if iter_optim_depth <= 2:
                        #opt_steps -= 1
                        res_is_sat = False
                        if at_least_one_layer_sat:
                            solver.pop()
                    else:
                        new_opt_layer = True
                        if at_least_one_layer_sat:
                            solver.pop()
                        solver.push()
                        
                        for conf_term in partial_latest_solution_to_fix.keys():
                            solver.assert_formula(solver.make_term(po.Equal, unrolled_ts.at_time(conf_term, 0), partial_latest_solution_to_fix[conf_term]))
                                                    
                        iter_optim_depth -= 1
                    sub_res_is_sat = True
                
            elif optimize_bit_width: # not res_is_sat
                core = solver.get_unsat_core()
                increase_bound = False
                if len(core) == 0:
                    for indc in indicators.keys():
                        if bw[indc] < pow(2, symbols[indc].get_sort().get_width()):
                            bw[indc] = 2*bw[indc]
                            increase_bound = True
                else:
                    for indc in indicators.keys():
                        if indicators[indc] in core and bw[indc] < pow(2, symbols[indc].get_sort().get_width()):
                            increase_bound = True
                            bw[indc] = 2*bw[indc]

        return opt_steps
    
    i = 0

    while i <= sum_left and i <= dim_max_val and dims_left > 1:
        min_loop_ass[item] = i
        opt_steps = gen_dim_vals (slv, strm, u, m, fout, output_file_first, optimize_bit_width, binary_search, partial_assignment, unrolled_ts, optimize_depth, sum_left-i, dim_names, dim_max_val, min_sum, dims_left-1, list_keys, ass_to_opt, min_loop_ass, opt_steps, group_names, obj_term_keys, indicators, prnt, tm, sys_argv, symbols, solver)
        i += 1
        if opt_steps:
            return opt_steps
    return opt_steps

