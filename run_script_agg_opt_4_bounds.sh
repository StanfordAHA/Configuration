#!/bin/bash
source "/barrett/scratch/nestan/lake/CAV/.env/bin/activate"
export PYTHONPATH=/barrett/scratch/makaim/repos/pono/build/python:/barrett/scratch/makaim/repos/pono/deps/smt-switch/build/python:$PYTHONPATH
export CADICAL_PHASE=false

python3 /barrett/scratch/nestan/Configure/configure.py --seq $1  --hwpath /barrett/scratch/nestan/Configure/modular/ --agg --bounds -opt 4 -out /barrett/scratch/nestan/Configure/output_agg_opt_4_bounds_print/sq_identity_conv_cascade_harris_agg/
