WVZ minitree analysis
==============================

1. Basic information

----------------------------------------------------

This code can:
 - generate cutflow
 - generate histograms of some variable

----------------------------------------------------

2. file structure

----------------------------------------------------

 - /source: contain source code
 - /build: use `make` to generate executable `run`
 - /run: contain `run`
   - cutflow information is in `/run/cutflowinfo`, with `convert_csv.py` convertion tool
 - /plot: contain `plot.py`, used to generate .png
   - generated root files are in `/plot/root`


----------------------------------------------------

3. Code structure

----------------------------------------------------
 - cut: applied in `ana.cpp`, `WWZ_ana.cpp`, `WZZ_ana.cpp` and `ZZZ_ana.cpp`
 - /build: Makefile, don't have to change except you want to add new source file
 - `run`: 
   1. `run: main exe`
   2. `file.list: include root file names`
   3. `test.root: include histograms`
   4. `test.txt: include cutflow information`
----------------------------------------------------

4. How to run this code

-----------------------------------------------------
 - `source setup.sh`
 - `cd build/`
 - `make`
 - `cd ../run`
 - `./run test`
if you are not working in UMATLAS server, you might need to change `file.list` first!!!

-----------------------------------------------------
5. Condor
-----------------------------------------------------
  1. to pass jobs to condor, you must have a valid proxy by `voms-proxy-init --voms atlas --valid 168:00`
