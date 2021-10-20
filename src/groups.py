###############################################################################
#  file -- groups.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Sets modules interface by setting group IDs, and valid and data signals for the design.
#  These are design and module specific.
###############################################################################

class module:

    group_ids = []
    
    stride_start_addr_ids = {}

    write_ids = {}
    
    shared_agg_sram_tb = {}
    
    valids = {'valid_in': 'valid_in', 'valid_out': 'valid_out'}
    data = {'data_in': 'data_in', 'data_out': 'data_out'}

    groups_data = {}
    
    def set_group_ids(self, agg_set, tb_set, sram_set, top_set, config_names, symbols):

        if top_set:
            
            self.group_ids = ['strg_ub_agg_only_loops_in2buf_0_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_', 'strg_ub_agg_only_loops_in2buf_1_', 'strg_ub_tb_only_loops_buf2out_read_0_', 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_', 'strg_ub_tb_only_loops_buf2out_read_1_', 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_']

            self.stride_start_addr_ids = {
                    'strg_ub_agg_only_loops_in2buf_0_': ['strg_ub_agg_only_agg_write_addr_gen_0_starting_addr', 'strg_ub_agg_only_agg_write_addr_gen_0_strides', 'strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_strides'],
                'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_': ['strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides', 'strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_agg_only_agg_read_addr_gen_0_starting_addr', 'strg_ub_agg_only_agg_read_addr_gen_0_strides', 'strg_ub_sram_only_input_addr_gen_0_strides', 'strg_ub_sram_only_input_addr_gen_0_starting_addr'],
                'strg_ub_agg_only_loops_in2buf_1_': ['strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_strides', 'strg_ub_agg_only_agg_write_addr_gen_1_starting_addr', 'strg_ub_agg_only_agg_write_addr_gen_1_strides', 'strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr'],
                'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_': ['strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides', 'strg_ub_agg_only_agg_read_addr_gen_1_strides', 'strg_ub_agg_only_agg_read_addr_gen_1_starting_addr', 'strg_ub_sram_only_input_addr_gen_1_starting_addr', 'strg_ub_sram_only_input_addr_gen_1_strides'],
                'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_': ['strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_strides', 'strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_write_addr_gen_0_strides', 'strg_ub_tb_only_tb_write_addr_gen_0_starting_addr', 'strg_ub_sram_only_output_addr_gen_0_starting_addr', 'strg_ub_sram_only_output_addr_gen_0_strides'],
                'strg_ub_tb_only_loops_buf2out_read_1_': ['strg_ub_tb_only_tb_read_sched_gen_1_sched_addr_gen_strides', 'strg_ub_tb_only_tb_read_addr_gen_1_strides', 'strg_ub_tb_only_tb_read_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_read_addr_gen_1_starting_addr'],
                'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_': ['strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_strides', 'strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_write_addr_gen_1_starting_addr', 'strg_ub_tb_only_tb_write_addr_gen_1_strides', 'strg_ub_sram_only_output_addr_gen_1_starting_addr', 'strg_ub_sram_only_output_addr_gen_1_strides', 'strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_starting_addr'],
                'strg_ub_tb_only_loops_buf2out_read_0_': ['strg_ub_tb_only_tb_read_sched_gen_0_sched_addr_gen_strides', 'strg_ub_tb_only_tb_read_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_read_addr_gen_0_strides', 'strg_ub_tb_only_tb_read_addr_gen_0_starting_addr'],
            }

            self.write_ids = {'strg_ub_agg_only_loops_in2buf_1_', 'strg_ub_agg_only_loops_in2buf_0_'}

            self.valids = {'valid_in': 'strg_ub.agg_only.agg_write', 'valid_out': 'strg_ub.tb_only.accessor_output'}
            self.data = {'data_in': 'data_in', 'data_out': 'data_out'}

    ###############################################################################################

        if agg_set:

            self.group_ids = ['strg_ub_agg_only_loops_in2buf_0_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_', 'strg_ub_agg_only_loops_in2buf_1_']

            self.stride_start_addr_ids = {'strg_ub_agg_only_loops_in2buf_0_': ['strg_ub_agg_only_agg_write_addr_gen_0_starting_addr', 'strg_ub_agg_only_agg_write_addr_gen_0_strides', 'strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_strides'],
            'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_': ['strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides', 'strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_agg_only_agg_read_addr_gen_0_starting_addr', 'strg_ub_agg_only_agg_read_addr_gen_0_strides'],
            'strg_ub_agg_only_loops_in2buf_1_': ['strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_strides', 'strg_ub_agg_only_agg_write_addr_gen_1_starting_addr', 'strg_ub_agg_only_agg_write_addr_gen_1_strides', 'strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr'],
            'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_': ['strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides', 'strg_ub_agg_only_agg_read_addr_gen_1_strides', 'strg_ub_agg_only_agg_read_addr_gen_1_starting_addr']}


            self.write_ids = {'strg_ub_agg_only_loops_in2buf_1_', 'strg_ub_agg_only_loops_in2buf_0_'}

            self.valids = {'valid_in': 'strg_ub.agg_only.agg_write', 'valid_out': 'strg_ub.agg_sram_shared.agg_read'}
            self.data = {'data_in' : 'data_in', 'data_out' : 'formal_agg_data_out'}
            
    ###############################################################################################

        if tb_set:

            self.group_ids = ['strg_ub_tb_only_loops_buf2out_read_0_', 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_', 'strg_ub_tb_only_loops_buf2out_read_1_', 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_']
            
            self.stride_start_addr_ids = {'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_': ['strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_strides', 'strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_write_addr_gen_0_strides', 'strg_ub_tb_only_tb_write_addr_gen_0_starting_addr'],
            'strg_ub_tb_only_loops_buf2out_read_1_': ['strg_ub_tb_only_tb_read_sched_gen_1_sched_addr_gen_strides', 'strg_ub_tb_only_tb_read_addr_gen_1_strides', 'strg_ub_tb_only_tb_read_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_read_addr_gen_1_starting_addr'],
            'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_': ['strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_strides', 'strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_write_addr_gen_1_starting_addr', 'strg_ub_tb_only_tb_write_addr_gen_1_strides'],
            'strg_ub_tb_only_loops_buf2out_read_0_': ['strg_ub_tb_only_tb_read_sched_gen_0_sched_addr_gen_strides', 'strg_ub_tb_only_tb_read_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_tb_only_tb_read_addr_gen_0_strides', 'strg_ub_tb_only_tb_read_addr_gen_0_starting_addr']}

            self.write_ids = {'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_', 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_'}
            
            self.valids = {'valid_in': 'strg_ub.sram_tb_shared.t_read_out', 'valid_out': 'strg_ub.tb_only.accessor_output'}
            self.data = {'data_in' : 'formal_mem_data', 'data_out' : 'data_out'}

    ###############################################################################################

        if sram_set:

            self.group_ids = ['strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_', 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_']
            
            self.stride_start_addr_ids = {'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_': ['strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_sram_only_input_addr_gen_0_strides', 'strg_ub_sram_only_input_addr_gen_0_starting_addr', 'strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides'],
             'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_': ['strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_strides', 'strg_ub_sram_only_output_addr_gen_0_starting_addr', 'strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_starting_addr', 'strg_ub_sram_only_output_addr_gen_0_strides'],
              'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_': ['strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_strides', 'strg_ub_sram_only_output_addr_gen_1_starting_addr', 'strg_ub_sram_only_output_addr_gen_1_strides', 'strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_starting_addr'],
               'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_': ['strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr', 'strg_ub_sram_only_input_addr_gen_1_starting_addr', 'strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides', 'strg_ub_sram_only_input_addr_gen_1_strides']}

            self.write_ids = ['strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_', 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_']
            

            self.valids = {'valid_in': 'strg_ub.agg_sram_shared.agg_read', 'valid_out': 'strg_ub.sram_only.read'}
            self.data = {'data_in' : 'agg_data_out_top', 'data_out' : 'formal_mem_data'}


        self.groups_data["ranges"] = {}
        self.groups_data["strides"] = {}
        self.groups_data["starting_addr"] = {}
        self.groups_data["dimensionality"] = {}
                
        for id in self.group_ids:
            self.groups_data["ranges"][id] = {}
            self.groups_data["strides"][id] = {}
            self.groups_data["starting_addr"][id] = {}
            self.groups_data["dimensionality"][id] = {}
        
        for conf in config_names:
            module_conf = symbols[conf]
            if "ranges" in conf:
                for id in self.group_ids:
                    if id in conf:
                        self.groups_data["ranges"][id][conf] = module_conf
                        break

            if "strides" in conf:
                for id in self.group_ids:
                    for id_stride in self.stride_start_addr_ids[id]:
                        if id_stride in conf:
                            self.groups_data["strides"][id][conf] = module_conf
                            break
                        

            if "starting_addr" in conf:
                for id in self.group_ids:
                    for id_st_addr in self.stride_start_addr_ids[id]:
                        if id_st_addr in conf:
                            self.groups_data["starting_addr"][id][conf] = module_conf
                            break


            if "dimensionality" in conf:
                for id in self.group_ids:
                    if id in conf:
                        self.groups_data["dimensionality"][id][conf] = module_conf
                        break



        #strides should be the same bw as corresponding starting addresses that don't have "sched" in it

#  Set shared signals agg-sram/sram-tb

    def set_shared_interface(self):

        for ind in range(6):
    #agg-sram
            self.shared_agg_sram_tb['strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides['+str(ind)+']'] = 'strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides['+str(ind)+']'
            self.shared_agg_sram_tb['strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_ranges['+str(ind)+']'] = 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_ranges['+str(ind)+']'
            self.shared_agg_sram_tb['strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides['+str(ind)+']'] = 'strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides['+str(ind)+']'
            self.shared_agg_sram_tb['strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_ranges['+str(ind)+']'] = 'sstrg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_ranges['+str(ind)+']'
    #sram-tb
            self.shared_agg_sram_tb['strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_ranges'] = 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_ranges'
            self.shared_agg_sram_tb['strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_strides'] = 'strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_strides'
            self.shared_agg_sram_tb['strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_ranges'] = 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_ranges'
            self.shared_agg_sram_tb['strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_strides'] = 'strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_strides'
            
    #agg-sram
        self.shared_agg_sram_tb['strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr'] = 'strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr'
        self.shared_agg_sram_tb['strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality'] = 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality'
        self.shared_agg_sram_tb['strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr'] = 'strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr'
        self.shared_agg_sram_tb['strg_ub_agg_sram_shared_agg_read_sched_gen_1_enable'] = 'strg_ub_agg_sram_shared_agg_read_sched_gen_1_enable'
        self.shared_agg_sram_tb['strg_ub_agg_sram_shared_agg_read_sched_gen_0_enable'] = 'strg_ub_agg_sram_shared_agg_read_sched_gen_0_enable'
        self.shared_agg_sram_tb['strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality'] = 'strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality'

    #sram-tb

        self.shared_agg_sram_tb['strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_starting_addr'] = 'strg_ub_sram_tb_shared_output_sched_gen_1_sched_addr_gen_starting_addr'
        self.shared_agg_sram_tb['strg_ub_sram_tb_shared_output_sched_gen_0_enable'] = 'strg_ub_sram_tb_shared_output_sched_gen_0_enable'
        self.shared_agg_sram_tb['strg_ub_sram_tb_shared_output_sched_gen_1_enable'] = 'strg_ub_sram_tb_shared_output_sched_gen_1_enable'
        self.shared_agg_sram_tb['strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_dimensionality'] = 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_1_dimensionality'
        self.shared_agg_sram_tb['strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_starting_addr'] = 'strg_ub_sram_tb_shared_output_sched_gen_0_sched_addr_gen_starting_addr'
        self.shared_agg_sram_tb['strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_dimensionality'] = 'strg_ub_sram_tb_shared_loops_buf2out_autovec_read_0_dimensionality'
