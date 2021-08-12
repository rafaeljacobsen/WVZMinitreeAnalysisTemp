#!/usr/bin/env python
import ROOT as R
import sys,os
plot_dir=os.path.dirname(__file__)
sys.path.append(os.path.join(plot_dir,"libs"))
import AtlasStyle
import MyPyRootPlot1d as plt

# set color
# 0--red  1--blue  2--green  3--purple  4--orange  5--brown  6--pink  7--yellow  8--dark blue  9--dark green  10--grey  11--black  12--white
color_dic={}
color_dic["llll"]=0
color_dic["ggllll_130M4l"]=1
color_dic["WWZ_4l2v"]=2

def shape_compare(file_name_list, var_name_list, extra_name="shape"):
        s_dic={}
        for var_name in var_name_list:
                s_dic[var_name]=plt.FlatPlot(var_name+"_"+extra_name,var_name+"_"+extra_name)

        for file_name in file_name_list:
                input_file= R.TFile.Open(os.path.join(plot_dir,"root",file_name+".root"))
                for var_name in var_name_list:
                        input_hist= input_file.Get(var_name)

                        s_dic[var_name].SetDoShape()
                        s_dic[var_name].add(input_hist, lco=color_dic[file_name], lab_name=file_name, drawop="E", lab_op="fl",is_fill_color=False, falpha=0.1)
        for var_name in var_name_list:
                if 'number' in var_name:
                        s_dic[var_name].set_frame(xtitle=var_name,ytitle="a.u.")
                if 'pt' in var_name:
                        s_dic[var_name].set_frame(xtitle=var_name+"[GeV]",ytitle="a.u.")
                elif 'mass' in var_name:
                        s_dic[var_name].set_frame(xtitle=var_name+"[GeV]",ytitle="a.u.")
                elif 'eta' in var_name:
                        s_dic[var_name].set_frame(xtitle=var_name,ytitle="a.u.")

                s_dic[var_name].draw()
                s_dic[var_name].Print("./PDFs/"+var_name+"_"+extra_name+".png")
        input_file.Close()

if __name__=="__main__":
    var_name_list=[]
    file_name_list=["llll","ggllll_130M4l","WWZ_4l2v"]
    channel_name_list=["WWZ_SF_inZ","WWZ_SF_noZ","WWZ_em"]
    para_name_list=["base","fwde","lowptm"]
        for channel_name in channel_name_list:
        for para_name in para_name_list:
            for i in range(1,8):
                var_name_list.append(channel_name+'_'+para_name+'_'+'lepton_pt'+str(i))
                var_name_list.append(channel_name+'_'+para_name+'_'+'lepton_eta'+str(i))
    shape_compare(file_name_list,var_name_list)
