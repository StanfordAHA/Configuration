###############################################################################
#  file -- parse.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Handles parsing of all input files.
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
#import timeit

class stream:

    set0 = []
    set1 = []
    seq_in = []
    seq_out = []
    vars = {}
    var_array_inds = {}
    constr2terms = []
    
    data_in_size = []
    data_out_size = []
    
    clk_name = None
    rst_n_name = None
    
    config_names = []
        

    def read_stream(self, args, fout, agg_set, tb_set, sram_set, symbols, solver):
        
        global dim_names
        
        # open an annotation file
        if args.annotation == None:
            if agg_set:
                annot_file = args.hwpath+"agg_lake_top_annotation.txt"
            elif tb_set:
                annot_file = args.hwpath+"tb_lake_top_annotation.txt"
            elif sram_set:
                annot_file = args.hwpath+"sram_lake_top_annotation.txt"
            else:
                annot_file = args.hwpath+"lake_top_annotation.txt"
        else:
            annot_file = args.annotation
            
        cfo = open(annot_file, "r+")
        
        clines = cfo.readlines()
        
        # Close opend file
        cfo.close()

        # Collect the Set0, Set1, I/O sequence, and config_name variables as they appear in btor2
        
        for cln in clines:
            cln = cln.strip()
            cln = cln.replace(',', '')
            cvars = cln.split()
            
            if 'var'  == cvars[0]:
                self.vars[cvars[1]] = cvars[3]
            elif 'input' != cvars[0] and 'output' != cvars[0] and 'var' != cvars[0] and 'if' != cvars[0] and 'SOLVE' != cvars[1]:
                self.constr2terms.append(cvars)
            elif 'if' == cvars[0]:
               self.constr2terms.append(cvars)
               
            elif 'SOLVE' == cvars[1]:#specific bits are set only to be solved. Others can be anything, e.g. 0
                signal = cvars[0]
                
                if ':' in signal:
                    signal_name = signal[:signal.find('[')]
                    ind_start = signal[signal.find('[')+1:signal.find(':')]
                    symb_start = False
                    if ind_start in self.vars:
                        ind_start = int(self.vars[ind_start],0)
                    elif ind_start.isdigit():
                        ind_start = int(ind_start,0)
                    else: symb_start = True
                    ind_end = signal[signal.find(':')+1:signal.find(']')]
                    symb_end = False
                    if ind_end in self.vars:
                        ind_end = int(self.vars[ind_end],0)
                    elif ind_end.isdigit():
                        ind_end = int(ind_end,0)
                    else: #case of symbolic
                        symb_end = True
                    if not symb_start and not symb_end:
                        if signal[:signal.find('[')] not in self.var_array_inds:
                            self.var_array_inds[signal[:signal.find('[')]] = []
                            for i in range(ind_start,ind_end+1):
                                self.var_array_inds[signal_name].append(i)
                    else: #implement later when suport for universal quantifiers is added
                        self.constr2terms.append(cvars)
                        
                else:
                    if signal[:signal.find('[')] not in self.var_array_inds:
                        self.var_array_inds[signal[:signal.find('[')]] = []
                    self.var_array_inds[signal[:signal.find('[')]].append(signal[signal.find('[')+1:signal.find(']')])
                
                
            elif 'SET' == cvars[-1][:-1]:
                if len(cvars) == 6:
                    rem_dims = cvars[2]
                    dims = []
                    while (rem_dims != ''):
                        dims.append(int(rem_dims[1:rem_dims.find(':')],0))
                        rem_dims = rem_dims[rem_dims.find(']')+1:]

                    gen = [0]*len(dims)
                    j = len(dims)-1
                    while j >= 0:
                        if gen[j] <= dims[j]:
                            build_dims = cvars[-2]
                            for i in gen:
                                build_dims = build_dims + '['+str(i)+']'
                            if cvars[-1][-1:] == '0':
                                self.set0.append(build_dims)
                            else:
                                self.set1.append(build_dims)
                            while (j < len(dims)-1 and gen[j+1] == 0):
                                j += 1
                        else:
                            gen[j] = 0
                            j -= 1
                        gen[j] += 1
                else:
                    if cvars[-1][-1:] == '0':
                        self.set0.append(cvars[-2])
                    else:
                        self.set1.append(cvars[-2])
                        
            elif 'SEQUENCE' == cvars[-1]:
                if len(cvars) == 6:
                    rem_dims = cvars[2]
                    dims = []
                    while (rem_dims != ''):
                        dims.append(int(rem_dims[1:rem_dims.find(':')],0))
                        rem_dims = rem_dims[rem_dims.find(']')+1:]
                    if cvars[0] == 'input':
                        self.data_in_size = dims
                    else:
                        self.data_out_size = dims

                    assert len(self.data_in_size) <= 3
                    assert len(self.data_out_size) <= 3
                    gen = [0]*len(dims)
                    j = len(dims)-1
                    while j >= 0:
                        if gen[j] <= dims[j]:
                            build_dims = cvars[-2]
                            for i in gen:
                                build_dims = build_dims + '['+str(i)+']'
                            if cvars[0] == 'input':
                                self.seq_in.append(build_dims)
                            else:
                                self.seq_out.append(build_dims)
                            while (j < len(dims)-1 and gen[j+1] == 0):
                                j += 1
                        else:
                            gen[j] = 0
                            j -= 1
                        gen[j] += 1
                else:
                    if cvars[0] == 'input':
                        self.seq_in.append(cvars[-2])
                    else:
                        self.seq_out.append(cvars[-2])
            elif 'SOLVE' == cvars[-1] and ('input' == cvars[0] or 'output' == cvars[0]):
                #if cvars[3] == 'strg_ub_pre_fetch_0_input_latency':
                #    continue
                if len(cvars) == 6:
                    dim = int(cvars[2][1:cvars[2].find(':')],0)
                    for i in range(dim+1):
                        self.config_names.append(cvars[-2]+'['+str(i)+']')
                else:
                    self.config_names.append(cvars[-2])
            elif 'CLK' == cvars[-1]: self.clk_name = cvars[-2]
            elif 'RSTN' == cvars[-1]: self.rst_n_name = cvars[-2]
            else:
                assert 'X' == cvars[-1]
                
