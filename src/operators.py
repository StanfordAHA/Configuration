###############################################################################
#  file -- operators.py --
#  Top contributors (to current version):
#    Nestan Tsiskaridze
#  This file is part of the configuration finder for the Stanford AHA project.
#  Copyright (c) 2021 by the authors listed in the file AUTHORS
#  in the top-level source directory) and their institutional affiliations.
#  All rights reserved.  See the file LICENSE in the top-level source
#  directory for licensing information.
#
#  Defines auxiliary bit-vector operators.
###############################################################################

import smt_switch as ss
import smt_switch.primops as po

# BVAdd for different bit-width.

def BVAdde(t0,t1,solver):
    orig_width_t0 = t0.get_sort().get_width()
    orig_width_t1 = t1.get_sort().get_width()
    orig_width = max(orig_width_t0,orig_width_t1)

    t0e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t0), t0)
    t1e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t1), t1)

    sum = solver.make_term(po.BVAdd, t0e, t1e)
    return sum

# BVMul for different bit-width.

def BVMule(t0,t1,solver):
    orig_width_t0 = t0.get_sort().get_width()
    orig_width_t1 = t1.get_sort().get_width()
    orig_width = max(orig_width_t0,orig_width_t1)

    t0e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t0), t0)
    t1e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t1), t1)
    
    prod = solver.make_term(po.BVMul, t0e, solver.make_term(po.BVAdd, t1e, solver.make_term(2, t1e.get_sort())))
    return prod

# BVUge for different bit-width.

def BVUgee(t0,t1,solver):

    orig_width_t0 = t0.get_sort().get_width()
    orig_width_t1 = t1.get_sort().get_width()

    orig_width = max(orig_width_t0,orig_width_t1)

    t0e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t0), t0)
    t1e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t1), t1)

    uge = solver.make_term(po.BVUge, t0e, t1e)

    return uge

# BVUlt for different bit-width.

def BVUlte(t0,t1,solver):
    orig_width_t0 = t0.get_sort().get_width()
    orig_width_t1 = t1.get_sort().get_width()
    orig_width = max(orig_width_t0,orig_width_t1)

    t0e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t0), t0)
    t1e = solver.make_term(ss.Op(po.Zero_Extend, orig_width-orig_width_t1), t1)
    
    ulte = solver.make_term(po.BVUlt, t0e, t1e)
    
    return ulte

# Constraint to avoid overflow during multiplication.

def umulo(t0,t1,solver):
    #overflow if hi(x*y) != 0
    orig_width = t0.get_sort().get_width()

    t0e = solver.make_term(ss.Op(po.Zero_Extend, orig_width), t0)
    t1e = solver.make_term(ss.Op(po.Zero_Extend, orig_width), t1)

    prod = solver.make_term(po.BVMul, t0e, t1e)
    #overflow occurs if the upper bits are non-zero
    result = solver.make_term(po.Not, solver.make_term(
        po.Distinct,
        solver.make_term(ss.Op(po.Extract, 2 * orig_width - 1, orig_width), prod),
        solver.make_term(0, t0.get_sort())))
        
    return result

# Constraint to avoid overflow during addition.

def uaddo(t0,t1,solver):
    orig_width = t0.get_sort().get_width()

    t0 = solver.make_term(ss.Op(po.Zero_Extend, 1), t0)
    t1 = solver.make_term(ss.Op(po.Zero_Extend, 1), t1)

    sum = solver.make_term(po.BVAdd, t0, t1)
    #overflow occurs if there's a carry out bit
    result = solver.make_term(po.Not, solver.make_term(ss.Op(po.Extract, orig_width, orig_width), sum))
    #result = solver.make_term(po.Equal, solver.make_term(ss.Op(po.Extract, orig_width, orig_width), solver.make_term(0, solver.make_sort(ss.sortkinds.BV, 1)))
    
    return result
