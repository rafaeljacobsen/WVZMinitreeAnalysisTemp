#!/usr/bin/env python
import ROOT
import sys,os
import pandas as pd
import argparse
parser = argparse.ArgumentParser(description="input and output names")
parser.add_argument("-i", "--input", type=str, help="Input dir lives in ../output/ ??")
parser.add_argument("-test", "--testflag", action="store_true", help="test mode")
args = parser.parse_args()
# names
dir_in = "../output/"
dir_out = "./data/"

tree_name = "WWZ"

file_in = args.input
file_suffix1 = "/NOMINAL/4l_signal.root"
file_suffix2 = "/NOMINAL/4l_background.root"

# read tree from input file and convert it to dataframe, save it to csv file
def convert(file_name, is_signal):
    # file_name example: 4l_signal ---> to open 4l_signal.root
    # will generate 4l_signal.csv in ./data/
    # is_signal should be: 0 ---- background, 1 ---- signal
    print("conversion of {0} start".format(file_name))
    fi = ROOT.TFile.Open(dir_in+file_in+"/NOMINAL/"+file_name+".root","READ")
    tree = fi.Get(tree_name)
    data, column = tree.AsMatrix(return_labels=True)
    df = pd.DataFrame(data=data, columns=column)
    df['signal'] = is_signal
    df.to_csv(dir_out+file_name+".csv")
    print("conversion complete")

convert("4l_signal", 1)
convert("4l_background", 0)
#convert("ZZ",0)
#convert("WZ",0)
#convert("ttZ",0)
#convert("tWZ",0)
#convert("other",0)
