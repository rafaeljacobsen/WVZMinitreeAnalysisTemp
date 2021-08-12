#!/usr/bin/env python3
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

parser.add_argument('-f', '--five_only',
        action = 'store_true',
        help = "look at 5 lepton channel only")

# parser.add_argument('-n','--nowgt',
#         action = 'store_true',
#         help = 'yield without wgt'
#         )

args = parser.parse_args()

d_sample_lv2 = collections.OrderedDict({
        # WWW
        "WVZ":[
            "WWW_3l",
            "WWZ_4l",
            "WWZ_2l",
            "WZZ_5l",
            "WZZ_3l",
            "ZZZ_6l",
            "ZZZ_4l",
            "ZZZ_2l",
            "WWZ_3l2j",
            "WZZ_4l2j",
            "WZZ_3l2j",
            ],
        "ZZ":["VBSZZ", "qqZZ", "ggZZ", "ZZqqll", "llvvjj"],
        "top": ["tt", "singleTop", "4top"],
        "ttV": ["tty", "tZ", "ttZ", "ttW", "ttWW"],
        "other": ["WZ", "WW", "Zjets", "Zgamma"],
        "VH":["VH"]
        # VH, ttH
    })


d_sample_5l = collections.OrderedDict({
        #For 5l analysis
        "5l_signal1":[
            "WZZ_5l"
            ],
        "5l_signal2":[
            "ZZZ_4l", "WWZ_4l", "WZZ_4l2j", "WWW_3l",
            "WWZ_2l","WZZ_3l","ZZZ_6l","ZZZ_2l","WWZ_3l2j","WZZ_3l2j",
            ],
        "5l_background":[
            "VBSZZ","qqZZ","ggZZ","ZZqqll","llvvjj",
            "Zjets",
            "tt","singleTop",
            "tty","tZ","ttZ","ttW","ttWW",
            "WZ","WW","Zjets","Zgamma",
            ],
        "5l_VH":["VH"]
    })


dir_name='./cutflowinfo/allresults/'+args.input+'/'
input_name=args.input

def get_cutflow_info(data_sample):

    # initial variables
    time_list=['_1516.csv','_17.csv','_18.csv']
    data=dict()
    flag = True
    started = 1
    length = 17

    for _time in time_list:
        file_name=dir_name+input_name+_time
        with open(file_name,'r') as csvfile:
            csvdata=csv.reader(csvfile, delimiter=',')
            line=0
            for row in csvdata:
                if line==0:
                    if flag:
                        if args.five_only:
                            started = row.index('>=5l')
                            end = row.index('>=4l')
                            length = started - end - 1
                        else:
                            length = len(row) - 1
                        data['header']=['Yield'] + row[started:(started+length)]
                        print('start column is ' + str(started))
                        for key in data_sample:
                            data[key]=[key]
                        for i in range(started, started+length):
                            for key in data_sample:
                                data[key].append(float(0))
                        flag=False
                else:
                    for sb, channel in data_sample.items():
                        if row[0] in channel:
                            for i in range(started, started+length):
                                data[sb][i-started+1]+=float(row[i])
                line+=1

    return data

if __name__=="__main__":        
    if not args.phys:
        with open(dir_name+input_name+'_5l_all.csv','w') as csvfile:
            csvdata=csv.writer(csvfile, delimiter=',')
            data = get_cutflow_info(d_sample_5l)
            for key in data:
                csvdata.writerow(data[key])
    else:
        with open(dir_name+input_name+'_5l_physics.csv','w') as csvfile:
            csvdata=csv.writer(csvfile, delimiter=',')
            data = get_cutflow_info(d_sample_lv2)
            for key in data:
                csvdata.writerow(data[key])

