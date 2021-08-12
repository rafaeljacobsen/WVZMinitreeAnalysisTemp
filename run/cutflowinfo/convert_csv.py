#!/usr/bin/env python

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


import sys, os, collections

d_sample_lv1 = collections.OrderedDict({
        "WWW_3l":[364242],

        "WWZ_4l":[364243],
        "WWZ_2l":[364244],
        "WZZ_5l":[364245],
        "WZZ_3l":[364246],
        "ZZZ_6l":[364247],
        "ZZZ_4l":[364248],
        "ZZZ_2l":[364249],

        "WWZ_3l2j":[363507],
        "WZZ_4l2j":[363508],
        "WZZ_3l2j":[363509],

        "qqZZ":[364250, 364288],
        "ggZZ":["345705", "345706"],
        "ZZqqll":[363356],
        "VBSZZ":[364283, 364284],
        "llvvjj":[364285, 364287],

        # new since v1.2
        "tt":[410472],
        "singleTop":[410658, 410659] + range(410644, 410648),
        "4top":[412043],
        "tty":[410389],
        "ttZ":[410156, 410157, 410218, 410219, 410220],

        # old
        #  "tt":[410503],
        #  "singleTop":range(410011, 410015) + [410025, 410026],
        #  "4top":[410080],
        #  "tZ":[410560],
        #  "ttZ":[410218, 410219, 410220],

        "ttW":[410155],
        "ttWW":[410081],


        "VH":[342284, 342285],
        "ttH":[343365],

        "WZ":[364253, 364289, 363358],
        "WW":[364254, 364290],

        #  "Zjets":range(364100, 364142),
        "Zjets":range(364120, 364142),
        "Zgamma":range(364500, 364510),
        })

d_sample_lv2 = collections.OrderedDict({
        # WWW
        "WVZ":[
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
        "other": ["WZ", "WW", "Zjets", "Zgamma"]
        # VH, ttH
    })


def _list_read(dir_name,d_sample):
    _output_dic={}
    for process,l_mc in d_sample.items():
        for dsid in l_mc:
            if(os.path.isfile(dir_name+str(dsid)+".txt")):
                with open(dir_name+str(dsid)+".txt","r") as f_in:
                    temp_lst=[]
                    for line in f_in.readlines():
                        if 'START' in line or ':' not in line:
                            continue
                        lst_line=line.split(':')
                        lst_event=lst_line[1].split("+")[0].split("(")
                        temp_lst.append([lst_line[0],lst_event[0],lst_event[1]])
                    _output_dic[dsid]=temp_lst
    return _output_dic


def _write_csv(dir_name,d_sample,output_file_name="yield.csv",no_wgt=True):

    output_dir='./cutflowinfo/'

    yield_dic=_list_read(dir_name,d_sample)

    if(no_wgt):
        index = 1
    else:
        index = 2
    with open(output_dir+output_file_name,"w") as f_out:

        flag =True;#flag of writing table head 

        f_out.write("{}".format("Yield"))
        
        d_merge={}        

        len_lst=0

        for process,l_mc in d_sample.items():
            if flag:
                for lst in yield_dic[l_mc[0]]:
                    f_out.write(",{}".format(lst[0]))
                f_out.write('\n')
                flag = False
                len_lst = len(yield_dic[l_mc[0]])
            f_out.write("{}".format(process))

            for i in range(len_lst):
                temp=0
                for dsid in l_mc:
                    if dsid in yield_dic:
                        temp += float(yield_dic[dsid][i][index])
                    
                f_out.write(",{}".format(str(temp)))
            f_out.write('\n')

        
if __name__=="__main__":        
    path="../output/"+args.input+"/NOMINAL"

    if not args.phys:
        d_sample=d_sample_lv1
    else:
        d_sample=d_sample_lv2
    _write_csv(path+"_1516/",d_sample,args.input+"_1516.csv",args.nowgt)
    _write_csv(path+"_17/",d_sample,args.input+"_17.csv",args.nowgt)
    _write_csv(path+"_18/",d_sample,args.input+"_18.csv",args.nowgt)		
