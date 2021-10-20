###############################################################################
#  file -- bounds.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Defines optional bound constraints imposed on a configuration.
#  These are design specific constraints.
###############################################################################

import smt_switch as ss
import smt_switch.primops as po
from operators import *

#for each type of range read/write: (range_0 + 2) * (range_1 + 2) * …. * (range_i + 2) <= sequence_length for i < dimensionality.
def bound_range_prod_term (u, module_conf, write_ranges, CLK_CYCLES, symbols, solver):

    solver.assert_formula(
    solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(1, module_conf.get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUge, solver.make_term(CLK_CYCLES, write_ranges[0].get_sort()),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort()))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle, solver.make_term(1, write_ranges[0].get_sort()),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort()))),
    uaddo(u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort()),solver)
    ))))
    solver.assert_formula(
    solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(2, module_conf.get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUge, solver.make_term(CLK_CYCLES, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle, solver.make_term(1, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[1].get_sort())),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[0],0),solver.make_term(2,write_ranges[0].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[1],0),solver.make_term(2,write_ranges[1].get_sort()),solver),
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),solver)
    )))
    )))))
    
    solver.assert_formula(
    solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(3, module_conf.get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUge, solver.make_term(CLK_CYCLES, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort()))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle, solver.make_term(1, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort()))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[1].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[2].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort()))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[0],0),solver.make_term(2,write_ranges[0].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[1],0),solver.make_term(2,write_ranges[1].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[2],0),solver.make_term(2,write_ranges[2].get_sort()),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),solver),
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort()))),solver)
    )))))
    )))))))
        
    solver.assert_formula(
    solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(4, module_conf.get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUge, solver.make_term(CLK_CYCLES, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle, solver.make_term(1, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[1].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[2].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[3].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort()))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[0],0),solver.make_term(2,write_ranges[0].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[1],0),solver.make_term(2,write_ranges[1].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[2],0),solver.make_term(2,write_ranges[2].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[3],0),solver.make_term(2,write_ranges[3].get_sort()),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort()))),solver),
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())))),solver)
    )))))))
    )))))))))
    
    solver.assert_formula(
    solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(5, module_conf.get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUge, solver.make_term(CLK_CYCLES, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort()))))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle, solver.make_term(1, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort()))))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[1].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[2].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[3].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[4].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort()))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort()))))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[0],0),solver.make_term(2,write_ranges[0].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[1],0),solver.make_term(2,write_ranges[1].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[2],0),solver.make_term(2,write_ranges[2].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[3],0),solver.make_term(2,write_ranges[3].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[4],0),solver.make_term(2,write_ranges[4].get_sort()),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort()))),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())))),solver),
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort()))))),solver)
    ))))))))
    ))))))))))))
       
    solver.assert_formula(
    solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(6, module_conf.get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUge, solver.make_term(CLK_CYCLES, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort())))))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle, solver.make_term(1, write_ranges[0].get_sort()),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort())))))))),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[1].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[2].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[3].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[4].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(CLK_CYCLES, write_ranges[4].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort()))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort())))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort()))))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    solver.make_term(po.BVUle,
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort())))))),
    solver.make_term(CLK_CYCLES, write_ranges[0].get_sort())),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[0],0),solver.make_term(2,write_ranges[0].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[1],0),solver.make_term(2,write_ranges[1].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[2],0),solver.make_term(2,write_ranges[2].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[3],0),solver.make_term(2,write_ranges[3].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[4],0),solver.make_term(2,write_ranges[4].get_sort()),solver),
    solver.make_term(po.And,
    uaddo(u.at_time(write_ranges[5],0),solver.make_term(2,write_ranges[5].get_sort()),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort()))),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())))),solver),
    solver.make_term(po.And,
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort()))))),solver),
    umulo(solver.make_term(po.BVAdd, u.at_time(write_ranges[0],0), solver.make_term(2,write_ranges[0].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[1],0), solver.make_term(2,write_ranges[1].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[2],0), solver.make_term(2,write_ranges[2].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[3],0), solver.make_term(2,write_ranges[3].get_sort())),
    solver.make_term(po.BVMul, solver.make_term(po.BVAdd, u.at_time(write_ranges[4],0), solver.make_term(2,write_ranges[4].get_sort())),
    solver.make_term(po.BVAdd, u.at_time(write_ranges[5],0), solver.make_term(2,write_ranges[5].get_sort())))))),solver)
    )))))))))))
    )))))))))))))

# Set 0 on values (of ranges and strides) indexed beyond dimensionality.
def set_zero_beyond_dimensionality (u, dim, dim_val, confs, symbols, solver):
    for i in range(dim_val,len(confs)):
        if "[" not in confs[i]:
            conf = symbols[confs[i]]
            solver.assert_formula(
            solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(dim,0), solver.make_term(dim_val, dim.get_sort())),
            solver.make_term(po.BVUle, u.at_time(conf,0), solver.make_term(2**dim_val-1, conf.get_sort()))))
        elif int(confs[i][confs[i].find('[')+1:confs[i].find(']')],0) >= dim_val:
            conf = symbols[confs[i]]
            solver.assert_formula(
            solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(dim,0), solver.make_term(dim_val, dim.get_sort())),
            solver.make_term(po.Equal, u.at_time(conf,0), solver.make_term(0, conf.get_sort()))))
            #print(solver.make_term(po.Implies, solver.make_term(po.Equal, u.at_time(dim,0), solver.make_term(dim_val, dim.get_sort())), solver.make_term(po.Equal, u.at_time(conf,0), solver.make_term(0, conf.get_sort()))))





# Add bounds on ranges, strides, starting addresses, dimensionalities (design specific).
def bound_ranges_strides_st_addr_dim (u, add_bounds, agg_set, tb_set, sram_set, valid_in_cycle, CLK_CYCLES, dim_max_val, m, symbols, group_ids, config_names, stride_start_addr_ids, solver):
    
    assert(add_bounds)

    
    for id in group_ids:
        for addr in m.groups_data["starting_addr"][id].keys():
            if "sched" in addr:
                st_addr = symbols[addr]
                dim = list(m.groups_data["dimensionality"][id].values())
                assert len(dim) == 1
                solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.BVUgt, u.at_time(dim[0], 0), solver.make_term(0, dim[0].get_sort())), solver.make_term(po.BVUlt, u.at_time(st_addr,0), solver.make_term(CLK_CYCLES, st_addr.get_sort()))))

    for conf in config_names:

        if "ranges" in conf:
            module_conf = symbols[conf]
            solver.assert_formula(solver.make_term(po.BVUle, u.at_time(module_conf,0), solver.make_term(CLK_CYCLES, module_conf.get_sort())))
            
        if "dimensionality" in conf:
            #each dimensionality <= 6
            module_conf = symbols[conf]
            solver.assert_formula(solver.make_term(po.BVUle, u.at_time(module_conf,0), solver.make_term(dim_max_val, module_conf.get_sort())))
            

            for id in m.groups_data["ranges"].keys():
                if id in conf:
                    ranges = m.groups_data["ranges"][id]
                    for i in range(0,dim_max_val+1):
                        set_zero_beyond_dimensionality(u, module_conf, i, list(m.groups_data["ranges"][id].keys()), symbols, solver)
            
            for id in m.groups_data["strides"].keys():
                if id in conf:
                    for i in range(0,dim_max_val+1):
                        strides = m.groups_data["strides"][id]
                        set_zero_beyond_dimensionality(u, module_conf, i, list(m.groups_data["strides"][id].keys()), symbols, solver)
                #i >= dimensionality --> range_i = 0
            
            for id in m.groups_data["ranges"].keys():
                if id in conf:
                    confs = list(m.groups_data["ranges"][id].values())
                    bound_range_prod_term (u, module_conf, confs, CLK_CYCLES, symbols, solver)

            for id in m.groups_data["starting_addr"].keys():
                if id in conf:
                    for addr in m.groups_data["starting_addr"][id].keys():
                        st_addr = symbols[addr]
                        solver.assert_formula(solver.make_term(po.Implies,  solver.make_term(po.Equal, u.at_time(module_conf,0), solver.make_term(0, module_conf.get_sort())), solver.make_term(po.Equal, u.at_time(st_addr,0), solver.make_term(0, st_addr.get_sort()))))


    if agg_set or tb_set or sram_set:
        for keyword in stride_start_addr_ids.keys():
            bw_val = None
            if agg_set:
                #     stride_start_addr_ids = {
                #        "in2buf_autovec_write": ["port_sel_addr", "agg_read_addr_gen_1", "input_addr_gen", "agg_read_addr_gen_0", "input_sched_gen"], #read 2
                #        "in2buf_0": ["agg_write_addr_gen_0", "agg_write_sched_gen_0"], #write 3
                #        "in2buf_1": ["agg_write_addr_gen_1", "agg_write_sched_gen_1"], #write 3

                bw_val = 2**2-1
                if keyword in m.write_ids:
                    bw_val = 2**4-1#3

            if tb_set:
                #    stride_start_addr_ids = {
                ##    "buf2out_autovec_read": ["output_sched_gen", "output_addr_gen"], #write 2
                #    "buf2out_read_0": ["tb_read_addr_gen_0", "tb_read_sched_gen_0"], #read 3
                #    "buf2out_read_1": ["tb_read_sched_gen_1", "tb_read_addr_gen_1"] #read 3
                #    }

                bw_val = 2**3-1
                if keyword in m.write_ids:
                    bw_val = 2**1-1# since we separate both for writes and reads we don't need 2

            if sram_set:
                #    stride_start_addr_ids = {
                #    "in2buf_autovec_write": ["port_sel_addr", "agg_read_addr_gen_1", "input_addr_gen", "agg_read_addr_gen_0", "input_sched_gen"], $write 9
                #    "buf2out_autovec_read": ["output_sched_gen", "output_addr_gen"] #read 9
                #    }
                
                bw_val = 2**9-1

            for id in stride_start_addr_ids[keyword]:
                for addr in m.groups_data["starting_addr"][keyword].keys():
                    if "sched" not in addr:
                        st_addr = symbols[addr]
                        solver.assert_formula(solver.make_term(po.BVUle, u.at_time(st_addr,0), solver.make_term(bw_val, st_addr.get_sort())))

#        if "strides" in conf:
#            for id in group_ids:
#                for id_stride in stride_start_addr_ids[id]:
#                    if id_stride in conf:
#                        m.groups_data["strides"][id][conf] = module_conf
#                        break

            for id in stride_start_addr_ids[keyword]:
                for strd in m.groups_data["strides"][keyword].keys():
                    if "sched" not in strd:
                        st_strd = symbols[strd]
                        solver.assert_formula(solver.make_term(po.BVUle, u.at_time(st_strd,0), solver.make_term(bw_val, st_strd.get_sort())))


    

    #add a constraint: sched_starting_addr cannot be less than the first cycle the valid = 1
    for id in group_ids:
        dim_module = set(m.groups_data["dimensionality"][id].values())
        assert len(dim_module) == 1
        dim = dim_module.pop()
        for addr in m.groups_data["starting_addr"][id].keys():
            if "sched" in addr:
                st_addr = symbols[addr]
                solver.assert_formula(solver.make_term(po.Implies, solver.make_term(po.BVUgt, u.at_time(dim, 0), solver.make_term(0, dim.get_sort())), solver.make_term(po.BVUge, u.at_time(st_addr,0), solver.make_term(valid_in_cycle, st_addr.get_sort()))))

