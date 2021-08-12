#!/usr/bin/env python
import ROOT as R
import sys,os
plot_dir=os.path.dirname(__file__)
sys.path.append(os.path.join(plot_dir,"libs"))
import AtlasStyle
import MyPyRootPlot1d as plt

dirname="data20210304_noem"
#  dirname="RemoveSFOSForZ2_WWZ"
#  dirname="WZZ_Z_window_20"
#  dirname="allSample"

outputdir="../output/"+dirname+"/NOMINAL"

# set color
# 0--red  1--blue  2--green  3--purple  4--orange  5--brown  6--pink  7--yellow  8--dark blue  9--dark green  10--grey  11--black  12--white

# define shape_compare function
def shape_compare(file_name_list, var_name_list, extra_name="shape"):
    s_dic={}
    for var_name in var_name_list:
        s_dic[var_name]=plt.FlatPlot(var_name+"_"+extra_name,var_name+"_"+extra_name)
        print var_name

    for file_name in file_name_list:
        input_file= R.TFile.Open(os.path.join(plot_dir, outputdir, file_name+".root"))
        print(os.path.join(plot_dir, outputdir, file_name+".root"))
        for var_name in var_name_list:
            input_hist= input_file.Get(var_name)

            s_dic[var_name].SetDoShape()
            try:
                lab_name = "{0}: {1:0.2f}".format(file_name, input_hist.Integral())
            except:
                raise Exception("hist name doesn't exist: " + var_name)
            s_dic[var_name].add(input_hist,  lab_name=lab_name, drawop="E", lab_op="fl",is_fill_color=False, falpha=0.1)
            if "lepton_eta_1" in var_name:
                print file_name, input_hist.Integral()
        input_file.Close()
    for var_name in var_name_list:
        if 'number' in var_name:
            s_dic[var_name].set_frame(xtitle=var_name,ytitle="a.u.")
        elif 'pt' in var_name:
                s_dic[var_name].set_frame(xtitle=var_name+"[GeV]",ytitle="a.u.")
        elif 'mass' in var_name:
                s_dic[var_name].set_frame(xtitle=var_name+"[GeV]",ytitle="a.u.")
        elif 'eta' in var_name:
                s_dic[var_name].set_frame(xtitle=var_name,ytitle="a.u.")
        elif 'phi' in var_name:
                s_dic[var_name].set_frame(xtitle=var_name,ytitle="a.u.")

        s_dic[var_name].draw()
        s_dic[var_name].Print("./PDFs/"+var_name+"_"+extra_name+".png")
# define 2d plot
def hist2d(file_name_list, var_name_list):
    for file_name in file_name_list:
        input_file=R.TFile.Open(os.path.join(plot_dir, outputdir, file_name+".root"))
        print(os.path.join(plot_dir, outputdir, file_name+'.root'))
        for varname in var_name_list:
            input_hist = input_file.Get(varname)
            c = R.TCanvas("c",varname, 1200,1000)
            input_hist.Draw("colz")
            c.SaveAs("./PDFs/"+varname+"_"+file_name+".pdf")
        input_file.Close()
    
# define stack function
def stack_hist_customize(file_name_list, var_name_list, extra_name="stack_ratio", bkg=True):
    s_dic={}
    for var_name in var_name_list:
        s_dic[var_name]=plt.StackPlotCustomize(var_name+"_"+extra_name,var_name+"_"+extra_name)
        #s_dic[var_name].remove_mc_stat=False
    for file_name in file_name_list:
        input_file= R.TFile.Open(os.path.join(plot_dir,"root",file_name+".root"))
        for var_name in var_name_list:
            input_hist= input_file.Get(var_name)
            lab_name = "{0}: {1:0.2f}".format(file_name, input_hist.Integral())
            #  if file_name in ["WWZ_4l2v","WZZ_5l1v","ZZZ_6l0v","ZZZ_4l2v"]: 
            if file_name in ["WVZ", "WWZ_4l2v", "WZZ_5l1v", "ZZZ_6l0v", "ZZZ_4l2v"]: 
                s_dic[var_name].add_sig(input_hist, lab_name=lab_name, drawop="",lab_op='F')
            else:
            #  if file_name in ["qq4l","gg4l"] and bkg:
                s_dic[var_name].add_bkg(input_hist, lab_name=lab_name, drawop="",lab_op='F')
    for var_name in var_name_list:
        if 'number' in var_name:
                s_dic[var_name].set_frame1(RightMargin=0.1,ytitle="Event")
                s_dic[var_name].set_frame2(RightMargin=0.1,xtitle=var_name)
        if 'pt' in var_name:
                s_dic[var_name].set_frame1(RightMargin=0.1,ytitle="Event/[10GeV]")
                s_dic[var_name].set_frame2(RightMargin=0.1,xtitle=var_name+"[GeV]")
        elif 'mass' in var_name:
                s_dic[var_name].set_frame1(RightMargin=0.1,ytitle="Event/[10GeV]")
                s_dic[var_name].set_frame2(RightMargin=0.1,xtitle=var_name+"[GeV]")
        elif 'eta' in var_name:
                s_dic[var_name].set_frame1(RightMargin=0.1,ytitle="Event/[0.5]")
                s_dic[var_name].set_frame2(RightMargin=0.1,xtitle=var_name)

        s_dic[var_name].draw()
        s_dic[var_name].Print("./PDFs/"+var_name+"_"+extra_name+".png")
    input_file.Close()
    
def stack_hist(file_name_list, var_name_list, extra_name="stack",bkg=True):
    s_dic={}
    for var_name in var_name_list:
        s_dic[var_name]=plt.StackPlot(var_name+"_"+extra_name,var_name+"_"+extra_name)
    for file_name in file_name_list:
        input_file=R.TFile.Open(os.path.join(plot_dir,"root",file_name+".root"))
        for var_name in var_name_list:
            input_hist=input_file.Get(var_name)
            s_dic[var_name].add_data(input_hist, lab_name=file_name, drawop="",lab_op='F')
                        #if 'pt' in var_name or 'mass' in var_name:
                        #        s_dic[var_name].set_frame(xtitle=var_name+"[GeV]",ytitle="Event")
                        #elif 'eta' in var_name:
                        #        s_dic[var_name].set_frame(xtitle="eta",ytitle="Event")
    for var_name in var_name_list:
        s_dic[var_name].draw()
        s_dic[var_name].Print("./PDFs/"+var_name+"_"+extra_name+".jpg")
    input_file.Close()
# main function
if __name__=="__main__":
    file_name_list=[
            "4l_signal",
            "4l_background"
            ]
    #  channel_name_lst=["ZZZ","WZZ","WWZ"]
    channel_name_lst=[
            "WWZ",
            "WWZ_SF_inZ",
            "WWZ_SF_noZ",
            "WWZ_em"
            #  "WWZ_SF_inZ_base",
            #  "WWZ_SF_noZ_base",
            #  "WWZ_em_base",

            #  "WWZ_SF_inZ_fwde",
            #  "WWZ_SF_noZ_fwde",
            #  "WWZ_em_fwde",

            #  "WWZ_SF_inZ_lowptm",
            #  "WWZ_SF_noZ_lowptm",
            #  "WWZ_em_lowptm",
            ]

    # variable dictionary
    var_dic={}
    var_list_2d=[]
    # Z_pt and mass
    var_dic['Z_pt']=["WZZ_Z_pt_first","WZZ_Z_pt_second"]
    #  var_dic['Z_mass']=["WZZ_Z_mass_first","WZZ_Z_mass_second"]
    #  var_dic['jet_number'] = [
            #  "ZZZ_jet_number", 
            #  "WWZ_jet_number",
            #  "WZZ_jet_number"]
    # lepton pt and eta
    var_dic['lepton_pt']=[]
    var_dic['lepton_eta']=[]
    var_dic['m4l']=[]
    var_dic['MET']=[]
    var_dic['METSig']=[]
    var_dic['Zl_pt']=[]
    var_dic['Wl_pt']=[]
    var_dic['chi2']=[]
    var_dic['eta']=[]
    var_dic['phi']=[]
    for channel_name in channel_name_lst:
        for i in range(1,8):    
            var_dic['lepton_pt'].append(channel_name+"_lepton_pt_"+str(i))
            var_dic['lepton_eta'].append(channel_name+"_lepton_eta_"+str(i))
        var_dic['m4l'].append(channel_name + "_m4l")
        var_dic['MET'].append(channel_name + "_MET")
        var_dic['METSig'].append(channel_name + "_METSig")
        var_dic['Zl_pt'].append(channel_name + "_Zl_pt_1")
        var_dic['Zl_pt'].append(channel_name + "_Zl_pt_2")
        var_dic['Wl_pt'].append(channel_name + "_Wl_pt_1")
        var_dic['Wl_pt'].append(channel_name + "_Wl_pt_2")
        var_dic['chi2'].append(channel_name + "_chi2")
        var_dic['eta'].append(channel_name + "_ZWl1_eta")
        var_dic['eta'].append(channel_name + "_ZWl2_eta")
        var_dic['eta'].append(channel_name + "_WW_eta")
        var_dic['phi'].append(channel_name + "_ZWl1_phi")
        var_dic['phi'].append(channel_name + "_ZWl2_phi")
        var_dic['phi'].append(channel_name + "_WW_phi")
        var_list_2d.append(channel_name+"_m4l_vs_mll2")
        var_list_2d.append(channel_name+"_WW_eta_vs_phi")
    # jet pt and eta
    var_dic['jet_pt']=[]
    var_dic['jet_eta']=[]
    for channel_name in channel_name_lst:
        for i in range(1,11):
            var_dic['jet_pt'].append(channel_name+"_jet_pt_"+str(i))
            var_dic['jet_eta'].append(channel_name+"_jet_eta_"+str(i))
    # fill var_name_list
    #  var_name_list=["WZZ_m4l"]
    var_name_list=[]
    for key in var_dic:
        var_name_list.extend(var_dic[key])
    # plot!!!!!!!!!!
    #shape_compare(file_name_list,var_name_list)
    hist2d(file_name_list,var_list_2d)
    #  stack_hist_customize(file_name_list,var_name_list)
    #  stack_hist_customize(file_name_list,var_name_list,"stack_nobkg",False)
