###############################################################################
#  file -- verify.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Verifies if a given configuration is correct.
###############################################################################

def verify_config (u, file, symbols, config_names, solver):

#   file is in args.verify of the input configuration problem

    focheck = open(file, "r+")
    lines_chk = focheck.readlines()
    focheck.close()

    test_conf = {}
    configuration = {}
    for cln in lines_chk:
        cln = cln.strip()
        cln = cln.replace(',', '')
        confs = cln.split()
        print(confs)
        fout.write(confs)
        fout.write("\n")

        start = confs[0].find('["')+2
        end = confs[0].find('"]')
        end_name = confs[0].rfind('_')
        if end_name == -1 or confs[0][end_name+1:end].isdigit() == False:
            fsym = confs[0][start:end]
        else:
            index = int(confs[0][end_name+1:end],0)
            fsym = confs[0][start:end_name]+'['+str(index)+']'
        print('fsym',fsym)
        fout.write('fsym '+fsym)
        fout.write("\n")

        fval = int(confs[2],0)
        print('fval',fval)
        fout.write('fval '+fval)
        fout.write("\n")
        test_conf[fsym] = fval
        configuration[symbols[fsym]] = solver.make_term(fval,symbols[fsym].get_sort())

        solver.assert_formula(solver.make_term(po.Equal, u.at_time(symbols[fsym], 0), solver.make_term(fval,symbols[fsym].get_sort())))
    for sym in config_names:
        if sym not in list(test_conf.keys()):
            configuration[symbols[sym]] = solver.make_term(0,symbols[fsym].get_sort())
            solver.assert_formula(solver.make_term(po.Equal, u.at_time(symbols[sym], 0), solver.make_term(0, symbols[sym].get_sort())))
    for i in list(configuration.keys()):
        print (i,int(configuration[i]))
        fout.write(str(i)+" "+str(int(configuration[i])))
        fout.write("\n")
#        --------------------------------------

    solver.push()
#   solver.dump_smt2("./dump_verify.smt2")
#   print('dump done!')

#   constrain configuration
#   only need to constrain at one time, because they're required to not change

    for sym, val in configuration.items():
        solver.assert_formula(solver.make_term(po.Equal, u.at_time(sym, 0), val))

    print('validate inputs:')
    fout.write('validate inputs:')
    fout.write("\n")

    print('\n=================== try simulating in Pono ==================\n')
    fout.write('\n=================== try simulating in Pono ==================\n')
    fout.write("\n")

    r = solver.check_sat()

    #assert r.is_sat()
    if not r.is_sat():
        print ("config verification FAILED")
        fout.write("config verification FAILED")
        fout.write("\n")
        return r

    print ("config verification SUCCESS")
    fout.write("config verification SUCCESS")
    fout.write("\n")
#---------------------------------- non determinism start --------------------
#    for i in range(CLK_CYCLES):
#        # check outputs
#        ln = lines[i+1]
#        ln = ln.strip()
#        ln = ln.replace('], [','],[')
#        ln = ln.replace(',', '')
#        seq_vals = ln.split(' ')
#
#        timed_data_out = {}
#        expected_data_out = {}
#
#        for s_out in seq_out:
#            ss_out = symbols[s_out]
#            if s_out[-1:] != ']': #not multi-dimensional
#                ind_s_out = seq_names.index(s_out)
#                assert seq_vals[ind_s_out][-1:] != ']'
#                val = int(seq_vals[ind_s_out],0)
#            else:
#                s_out_name = s_out[:s_out.find('[')]
#                dim_val = int(s_out[s_out.find('[')+1:s_out.find(']')],0)
#
#                ind_s_out = seq_names.index(s_out_name)
#                assert seq_vals[ind_s_out][-1:] == ']'
#                s_out_val = seq_vals[ind_s_out].replace('[', ' ')
#                s_out_val = s_out_val.replace(']', ' ')
#                s_out_val = s_out_val.split()
#                val = int(s_out_val[dim_val],0)
#
#            timed_data_out_s = u.at_time(ss_out, i)
#            timed_data_out[ss_out] = solver.get_value(timed_data_out_s)
#            print(s_out,'@{} :='.format(i), timed_data_out[ss_out])
#            expected_data_out[ss_out] = solver.make_term(val, timed_data_out[ss_out].get_sort())
#            print('expected ',s_out,'@{} :='.format(i), expected_data_out[ss_out])
#
#            if timed_data_out[ss_out] != expected_data_out[ss_out]:
#                print('\tIncorrect value for {}@{}. Should be {}'.format(s_out,i, expected_data_out[ss_out]))
#                # see if it's possible to change the value
#                solver.push()
#                solver.assert_formula(solver.make_term(po.Equal, timed_data_out_s, expected_data_out[ss_out]))
#                r = solver.check_sat()
#                if r.is_sat():
#                    print('\tPossible to correct value (nondeterminism!)')
#                solver.pop()
#---------------------------------- non determinism end --------------------
#    for i in range(CLK_CYCLES):
#        test = symbols['strg_ub.tb_only.tb_read_addr_gen_0.addr_out']
#        print('strg_ub.tb_only.tb_read_addr_gen_0.addr_out@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.cycle_count']
#        print('strg_ub.tb_only.cycle_count@',i,int(solver.get_value(u.at_time(test, i))))
##        test = symbols['strg_ub.tb_only.tb']
##        print('strg_ub.tb_only.tb@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.tb_read']
#        print('strg_ub.tb_only.tb_read@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.tb_read_sched_gen_0.valid_output']
#        print('strg_ub.tb_only.tb_read_sched_gen_0.valid_output@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.sram_read_data[0]']
#        print('strg_ub.tb_only.sram_read_data[0]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.sram_read_data[1]']
#        print('strg_ub.tb_only.sram_read_data[1]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.sram_read_data[2]']
#        print('strg_ub.tb_only.sram_read_data[2]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.sram_read_data[3]']
#        print('strg_ub.tb_only.sram_read_data[3]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.t_read_d1']
#        print('strg_ub.tb_only.t_read_d1@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['formal_mem_data[0][0][0]']
#        print('formal_mem_data[0][0][0]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['formal_mem_data[0][0][1]']
#        print('formal_mem_data[0][0][1]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['formal_mem_data[0][0][2]']
#        print('formal_mem_data[0][0][2]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['formal_mem_data[0][0][3]']
#        print('formal_mem_data[0][0][3]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['data_out[0]']
#        print('data_out[0]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['data_out[1]']
#        print('data_out[1]@',i,int(solver.get_value(u.at_time(test, i))))
#        test = symbols['strg_ub.tb_only.t_read']
#        print('strg_ub.tb_only.t_read@',i,int(solver.get_value(u.at_time(test, i))))
#

    #strg_ub.tb_only.cycle_count
    #strg_ub.tb_only.tb
    #strg_ub.tb_only.tb_read
    #strg_ub.tb_only.tb_read_sched_gen_0.valid_output
    #strg_ub.tb_only.sram_read_data
    #strg_ub.tb_only.t_read_d1

#        test = symbols['strg_ub.agg_in_0.write_act']
#        print('strg_ub.agg_in_0.write_act','@{} :='.format(i),solver.get_value(u.at_time(test, i)))
#        test = symbols['rst_n']
#        print('rst_n','@{} :='.format(i),solver.get_value(u.at_time(test, i)))
#        test = symbols['strg_ub.agg_in_0.rst_n']
#        print('strg_ub.agg_in_0.rst_n','@{} :='.format(i),solver.get_value(u.at_time(test, i)))
#        test = symbols['strg_ub.agg_in_0.clk']
#        print('strg_ub.agg_in_0.clk','@{} :='.format(i),solver.get_value(u.at_time(test, i)))

#---nondeterminism check
#        # check that configuration was set correctly
#        for name in config_names:
#            sym = symbols[name]
#            val = solver.get_value(u.at_time(sym, i))
#            assert val == configuration[sym], \
#                "Expected {}@{} := {} but got {}".format(sym, i, configuration[sym], val)
#---nondeterminism check end
    return r

