# Configuration Finder: an automated configuration finder built on an SMT-based model checker built on [Pono](https://github.com/upscale-project/pono)

## Setup

Install Pono with Boolector and Python bindings. 

 ```
 git clone https://github.com/upscale-project/pono
 
 # Optional recommended step: start a python virtualenv
 # If you install in the virtualenv, you will need to activate it each time before using pono
 # and deactivate the virtualenv with: deactivate
 # From pono folder: 
 python3.8 -m venv ./env
 source ./env/bin/activate

 # To build the `Pono` python bindings, first make sure that you have [Cython]
 # (https://cython.org/) version >= 0.29 installed. 
 pip install pytest Cython==0.29.15

 # Install all dipendencies -- assuming none are globally installed.
 ./contrib/setup-bison.sh
 ./contrib/setup-flex.sh
 ./contrib/setup-btor2tools.sh

 # Then ensure that `smt-switch` and its python bindings are installed.
 # Build smt-switch with Python bindings. It will build smt-switch with `Boolector`. 
 ./contrib/setup-smt-switch.sh --python
 
 # Install the Python bindings in this virtualenv.
 pip install -e ./deps/smt-switch/build/python/
 
 # Finally, you can configure and then build `Pono` normally.
  ./configure.sh --python
  cd build
  make -j4
  make -j2 test
  pip install -e ./python

  python -X faulthandler -c "import smt_switch"
  python -X faulthandler -c "import pono"      

 # Optional you can set `CaDiCaL` SAT solver's phase to false: 
 # (we found this more efficient in our experiments):
 export CADICAL_PHASE=false
```


## Options

To run the `Configuration Finder` from a command line use `./src/configure.py` with your choice of argument options:

```
--agg, --tb, or --sram --- to specify the module in the modular configuration.
--cagg [config_of_agg] --- to propagate agg configuration when solving sram.
--ctb [config_of_tb] --- to propagate tb configuration when solving sram.
--caggtbfirst --- used with .sh scripts to feed corresponding first configurations of both agg and tb.
--caggtbmin --- used with .sh scripts to feed corresponding min configurations of both agg and tb.
-out or --output [out_path] --- to provide the output destination.
-sv or --verilog [design.sv] --- for System Verilog source of a design.
-csv or --seq [i-o_stream] --- for the input-output stream.
-n or --annote [annotation_file] --- for the annotation files.
-opt or --optimize [number] --- to provide optimization depth.
-v or --verify [config_to_verify] --- to verify a configuration is correct.
--bounds --- to add auxiliary, design-specific, bound constraints.
--optbw --- to activate bit-width optimization during configuration finding. This options tries to find a solution with the lowest bit-width for several large bit-vector variables (starting_address variables).
-l or --linear --- to activate a linear search for the optimal solution. Default is a binarysearch.
--hwpath [hwpath] --- used with .sh to provide a top-level folder where the designs/annotations are stored. Default is ".".
```

For, example:

`python3 ./src/configure.py --seq ./aha_garnet_smt/app/agg_stream.csv  --hwpath ./modular/ --agg --bounds -opt 4 -out ./results/` 

configures an agg module in `./modular/` for the sequence in `./app/agg_stream.csv` with auxiliary bound constraints and complete optimization. The output consists of three files -- first solution, min solution, and general output -- stored in the `./results/app/agg_stream.csv/` folder. In addition, the current version is bound to specific module file names.  

If you like to submit a slurm job you can use a script similar to `run_script_agg_opt_4_bounds.sh`. 

## Generating BTOR2 from Verilog

The best tool for creating BTOR2 from Verilog is [Yosys](https://github.com/YosysHQ/yosys). Yosys has an excellent manual [here](http://www.clifford.at/yosys/files/yosys_manual.pdf). You can find a detailed description on how to generate BTOR2 from Verilog at Pono webpage.

Once you have `yosys` installed, you can use our `gen-btor.ys` in the top-level of this repository and run `yosys -s gen-btor.ys` to produce the BTOR2 file.

## Benchmarks

* Modules

All design modules used in our experiments are in the folder `modular`. This folder also contains all required annotation files, configuration variable mappings for the modular approach, and information about the size of each module.

* Input-Output streams

The input-output specifications are provided in the `aha_garnet_smt` folder. There are four different image processing applications: identity-stream, convolution 3x3, cascade, and harris.

To reproduce the experiments use:

Pono commit a667066363f0d67789acc044b4b976d40e6e6f1b.
smt-switch commit 9d8b1ebe5a06c3f7a2f924efcdcaa978f503232a.
Boolector Version 3.2.1 HEAD-95859db82fe5b08d063a16d6a7ffe4a941cb0f7d.

