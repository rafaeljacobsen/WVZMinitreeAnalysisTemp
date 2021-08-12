#!/usr/bin/env python2

"""
the most general merging
specify output name, input collections, it will merge over mc16a and mc16d
"""

from __future__ import print_function

import argparse
parser = argparse.ArgumentParser(description='merge condor outputs')
parser.add_argument('-o', '--output', 
        type=str, 
        required = True,
        help = "the output dir that lives in the ../output")
parser.add_argument('-p', '--phys',
        action = 'store_true',
        help = "merge with physical names")
parser.add_argument('-t', '--test',
        action = 'store_true',
        help = "do not merge, check cmd instead") 
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
        # "VBSZZ":[364283, 364284],
        "VBSZZ":[366086, 366087, 366088, 366089],
        "llvvjj":[364285, 364287],

        # new since v1.2
        "tt":[410472],
        "singleTop":[410658, 410659] + range(410644, 410648),
        # "4top":[412043], # NLO, currently not available
        "4top":[410080], # LO

        "tty":[410389],
        "ttZ":[410156, 410157, 410218, 410219, 410220],
        "tZ":[410560],
        # old
        #  "tt":[410503],
        #  "singleTop":range(410011, 410015) + [410025, 410026],
        #  "4top":[410080],
        #  "tZ":[410560],
        #  "ttZ":[410218, 410219, 410220],

        "ttW":[410155],
        "ttWW":[410081],


        # "VH":[342284, 342285],
        "VH":[346646, 346647, 345066, 346645],
        "ttH":[343365],

        "WZ":[364253, 364289, 363358],
        "WW":[364254, 364290],

        "Zjets":range(364100, 364142), 
        # "Zjets":range(364120, 364142), 
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
        # with tty
        #  "ttV": ["tty", "tZ", "ttZ", "ttW", "ttWW"],
        # without tty
        "ttV": ["tZ", "ttZ", "ttW", "ttWW"],
        "other": ["WZ", "WW", "Zjets", "Zgamma"]
        # VH, ttH
    })

d_sample_lv3 = collections.OrderedDict({ 
        # WWW
        "WVZ4l":[
            "ZZZ_4l",
            "WWZ_4l", 
            "WZZ_4l2j",
            ],
        "WVZ5l":["WZZ_5l"],
        "WVZ6l":["ZZZ_6l"],
        "WVZothers":[
            "WWW_3l",
            "WWZ_2l",
            "WZZ_3l",
            "ZZZ_2l",
            "WWZ_3l2j",
            "WZZ_3l2j",
            ],
        "ZZ":["VBSZZ", "qqZZ", "ggZZ", "ZZqqll", "llvvjj"],
    })

d_sample_5l = collections.OrderedDict({
        #For 5l analysis
        "WZZ5l":["WZZ_5l"],        
        "WVZelse":["ZZZ_4l","WWZ_2l","WWZ_4l","WZZ_3l","ZZZ_6l","ZZZ_2l","WWZ_3l2j","WZZ_3l2j","WZZ_4l2j","WWW_3l"],
        "WVZ":["WZZ_5l","ZZZ_4l","WWZ_2l","WWZ_4l","WZZ_3l","ZZZ_6l","ZZZ_2l","WWZ_3l2j","WZZ_3l2j","WZZ_4l2j","WWW_3l"],
        "background":[
            "VBSZZ","qqZZ","ggZZ","ZZqqll","llvvjj",
            "tt","singleTop", "4top",
            "tty","tZ","ttZ","ttW","ttWW",
            "WZ","WW","Zjets","Zgamma",
            "ttH",
            ],
        "ZZ":["VBSZZ", "qqZZ", "ggZZ", "ZZqqll", "llvvjj"],
        "others":[
            "tt","singleTop", "4top",
            "tty","tZ","ttZ","ttW","ttWW",
            "WZ","WW","Zjets","Zgamma",
            "ttH",
            ]
    })

def expand(dic_in, dicbase):
    dic_out = collections.OrderedDict()
    for key, l_base in dic_in.items():
        dic_out[key] = [dsid for basekey in l_base for dsid in dicbase[basekey]]
        pass
    return dic_out

#  print(expand(d_sample_lv2, d_sample_lv1))
#  exit(0)

def merge(outdir, l_variation, d_sample = d_sample_lv1):
    for variation in l_variation:
        dir = os.path.join(outdir, variation)
        # make the target dir
        os.system("mkdir -p " + dir)
        cmd_glob_tmplate = "hadd -f " + dir + "{0}/{1}.root "
        cmd_oneprocess_tmplate = dir + "_{0}/{1}.root "
        for process, l_mc in d_sample.items():
            cmd_merge_period = cmd_glob_tmplate.format("", process)

            cmd_one_period = "("
            for year in [1516, 17, 18]:
                cmd_merge_period += cmd_oneprocess_tmplate.format(year, process)

                cmd_str = cmd_glob_tmplate.format("_" + str(year), process) 
                for dsid in l_mc:
                    cmd_str += cmd_oneprocess_tmplate.format(year, dsid)
                #  print(cmd_str)
                cmd_one_period += "nohup " + cmd_str + "; " 
                pass


            cmd_final = cmd_one_period + " nohup " + cmd_merge_period + ") &"
            if args.test:
                print(cmd_final)
            else:
                os.system(cmd_final)



    pass


#  d_sample_lv1.update(expand(d_sample_lv2, d_sample_lv1))

#  merge(os.path.join("../output", args.output), ["NOMINAL"], d_sample_lv1)
if not args.phys:
    merge(os.path.join("../output", args.output), ["NOMINAL"], d_sample_lv1)
else:
    # merge(os.path.join("../output", args.output), ["NOMINAL"], d_sample_lv3)
    merge(os.path.join("../output", args.output), ["NOMINAL"], d_sample_5l)
