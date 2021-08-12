ROOTLIBS = `root-config --libs`
OPTCOMP = `root-config --cflags`
SRC_DIR = ../source
WRK_DIR = ../run
SPECIALFLAGS= --exceptions
CFLAGS = -I.
LFLAGS =

RCXX = $(CFLAGS) $(ROOTCFLAGS) -std=c++14
DBG = -g -L -O -m32
CC = g++ ${DBG} $(RCXX) $(OPTCOMP) -std=c++14
F77 = f77

all: run

run: run.o ana.o ana_base.o ZZZ_ana.o WZZ_ana.o WWZ_ana.o CutFlowTool.o
	$(CC) $^ $(ROOTLIBS) -o $(WRK_DIR)/$@

run.o: $(SRC_DIR)/run.cpp
	$(CC) -c $< -o $@

ana.o: $(SRC_DIR)/ana.cpp $(SRC_DIR)/ana.h
	$(CC) -c $< -o ana.o

ana_base.o: $(SRC_DIR)/ana_base.C $(SRC_DIR)/ana_base.h
	$(CC) -c $< -o ana_base.o

ZZZ_ana.o: $(SRC_DIR)/ZZZ_ana.cpp $(SRC_DIR)/ana.h
	$(CC) -c $< -o ZZZ_ana.o

WZZ_ana.o: $(SRC_DIR)/WZZ_ana.cpp $(SRC_DIR)/ana.h
	$(CC) -c $< -o WZZ_ana.o

WWZ_ana.o: $(SRC_DIR)/WWZ_ana.cpp $(SRC_DIR)/ana.h
	$(CC) -c $< -o WWZ_ana.o

CutFlowTool.o: $(SRC_DIR)/CutFlowTool.cxx $(SRC_DIR)/CutFlowTool.h
	$(CC) -c $< -o CutFlowTool.o

clean: 
	\rm -rf *.o
