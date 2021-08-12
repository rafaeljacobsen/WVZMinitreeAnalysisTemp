#!/usr/bin/env python
import csv
import sys, os, collections
import argparse

parser = argparse.ArgumentParser(description="csv converter")
parser.add_argument('-i','--input',
        type=str,
        required = True,
        help = "for example :allSample, indicate the input directory name"
        )
parser.add_argument('-p', '--phys',
        action = 'store_true',
        help = "merge with physical names")
parser.add_argument('-n','--nowgt',
        action = 'store_true',
        help = 'yield without wgt'
        )
args = parser.parse_args()


d_sample_4l = collections.OrderedDict({
        #For 4l analysis
        "4l_signal":[
            "WWZ_4l",
            "WZZ_4l2j",
            "ZZZ_4l"
            ],
        "4l_background":[
            "WWZ_2l","WZZ_5l","WZZ_3l","ZZZ_6l","ZZZ_2l","WWZ_3l2j","WZZ_3l2j",
            "VBSZZ","qqZZ","ggZZ","ZZqqll","llvvjj",
            "tt","ttZ","ttW","ttWW",
            "tZ","ttZ","ttW","ttWW",
            "WZ","WW","Zjets","Zgamma"
            ]
    })
dir_name="./cutflowinfo/"
input_name=args.input
time_list=['_1516.csv','_17.csv','_18.csv']
data={}
flag = True
for _time in time_list:
    file_name=dir_name+input_name+_time
    with open(file_name,'r') as csvfile:
        csvdata=csv.reader(csvfile, delimiter=',')
        line=0
        for row in csvdata:
            if line==0:
                if flag:
                    data['header']=row
                    signal=['4l_signal']
                    background=['4l_background']
                    for i in range(len(row)-1):
                        signal.append(float(0))
                        background.append(float(0))
                    data['4l_signal']=signal
                    data['4l_background']=background
                    flag=False
            else:
                for sb,channel in d_sample_4l.items():
                    if row[0] in channel:
                        for i in range(len(row)-1):
                            data[sb][i+1]+=float(row[i+1])
            line+=1
with open(dir_name+input_name+'_4l.csv','w') as csvfile:
    csvdata=csv.writer(csvfile, delimiter=',')
    csvdata.writerow(data['header'])
    csvdata.writerow(data["4l_signal"])
    csvdata.writerow(data["4l_background"])
