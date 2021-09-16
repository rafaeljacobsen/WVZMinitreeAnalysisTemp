#define ana_cxx
#include "ana.h"
#include <iostream>
#include <time.h>
#include <fstream>
#include <TLorentzVector.h>
#include <fstream>
#include <iostream>
#include <numeric>
#include "TString.h"
using namespace std;
///////////////////////////////////////////////////below is universal functions for help////////////////////////////////////////////////
void ana::Find_Z_pair()
{
   int i,j;
   vector<int>::iterator iter;
   pair<int, int> Z_pair_temp(-1,-1);
   for(i=0; i<v_l_pid.size(); i++)
   {
      if(find(v_ignore.begin(),v_ignore.end(),i)!= v_ignore.end()) continue;
      for(j=i+1; j<v_l_pid.size(); j++)
      {
         if(find(v_ignore.begin(),v_ignore.end(),j)!= v_ignore.end())    continue;
         if(v_l_pid[i]+v_l_pid[j]!=0) continue;
         if(Z_pair_temp.first<0 || Z_pair_temp.second<0){ Z_pair_temp= make_pair(i,j); continue;}
         if(abs((v_l_tlv[i]+v_l_tlv[j]).M()-Z_mass) < abs((v_l_tlv[Z_pair_temp.first]+v_l_tlv[Z_pair_temp.second]).M()-Z_mass))
            Z_pair_temp= make_pair(i,j);
      }
   }
   if(v_l_tlv[Z_pair_temp.first].Pt()<v_l_tlv[Z_pair_temp.second].Pt()) Z_pair_temp= make_pair(Z_pair_temp.second,Z_pair_temp.first);
   if(Z_pair_temp!= make_pair(-1,-1))
   {
      v_ignore.insert(v_ignore.end(),Z_pair_temp.first);
      v_ignore.insert(v_ignore.end(),Z_pair_temp.second);
      v_Z_pair.insert(v_Z_pair.end(),Z_pair_temp);
      float Z_wgt= v_l_wgt[Z_pair_temp.first] * v_l_wgt[Z_pair_temp.second];
      v_Z_wgt.insert(v_Z_wgt.end(),Z_wgt);
   }
};

bool ana::initial_Cut()
{
   wgt= weight/v_sumofwgt[fCurrent];
   cutflow("initial").pass("initial","All",wgt);
   // lepton number > 3
   if(v_l_pid.size()<=3) return false;
   cutflow("initial").pass("initial",">3l",wgt);
   // at least one SFOS pair
   Find_Z_pair();
   Find_Z_pair();
   Find_Z_pair();
   if(v_Z_pair.size()==0) return false;
   cutflow("initial").pass("initial","1_SFOS",wgt*v_Z_wgt[0]);
   // fill Z_mass_first Z_mass_second Z_mass_third
   TString s_number[3]={"first","second","third"};
   for(int i=0;i<v_Z_pair.size();i++)
   {
      TLorentzVector Z_tlv=v_l_tlv[v_Z_pair[i].first]+v_l_tlv[v_Z_pair[i].second];
      makehist("Z_mass_"+s_number[i])->Fill(Z_tlv.M()/1000,wgt);
   }

   // Z window 20 GeV
   if(abs((v_l_tlv[v_Z_pair[0].first]+v_l_tlv[v_Z_pair[0].second]).M()-Z_mass)>20e3) return false;
   cutflow("initial").pass("initial","Z_window",wgt*v_Z_wgt[0]);
   if(passTrig) cutflow("initial").pass("initial","passTrig",wgt*v_Z_wgt[0]);
   // find m4l
   Find_m4l();
   // forward electron
   n_e_fwd=0;
   for(int i=0;i<v_e_fwd->size();i++)
   {
      if((*v_e_fwd)[i]){n_e_fwd++;} 
   }
   if(n_e_fwd>0) cutflow("initial").pass("initial","e_fwd",wgt*v_Z_wgt[0]);
   if(n_e_fwd==1) cutflow("initial").pass("initial","e_fwd_1",wgt*v_Z_wgt[0]);
   // low pt muon
   n_m_lowpt=0;
   for(int i=0;i<v_m_lowpt->size();i++)
   {
      if((*v_m_lowpt)[i]){ n_m_lowpt++;}
   }
   if(n_m_lowpt>0) cutflow("initial").pass("initial","m_lowpt",wgt*v_Z_wgt[0]);
   if(n_m_lowpt==1) cutflow("initial").pass("initial","m_lowpt_1",wgt*v_Z_wgt[0]);
   if(n_e_fwd==0 && n_m_lowpt==0) cutflow("initial").pass("initial","no_fwde_lowptm",wgt*v_Z_wgt[0]);
   // lepton number information
   int nlepton=v_l_pid.size();
   if(nlepton>6) cutflow("initial").pass("initial",">6l",wgt*v_Z_wgt[0]);
   if(nlepton==6) cutflow("initial").pass("initial","6l",wgt*v_Z_wgt[0]);
   if(nlepton==5) cutflow("initial").pass("initial","5l",wgt*v_Z_wgt[0]);
   if(nlepton==4) cutflow("initial").pass("initial","4l",wgt*v_Z_wgt[0]);
   return true;
}

void ana::Bjet_Cut(string s_flow, string s_cut, float wgt_base)
{
   bool btag_veto;
   float btag_wgt;
   int njet=v_j_tlv->size();

   btag_wgt=1;
   btag_veto=true;
   for(int i=0;i<njet;i++)
   {
      if(v_j_btag60->at(i)) btag_veto=false;
      btag_wgt*=v_j_wgt_btag60->at(i);
   }
   if(btag_veto) cutflow(s_flow).pass(s_cut,"B_veto60",wgt_base*btag_wgt);
   b_wgt[0]=btag_wgt;

   btag_wgt=1;
   btag_veto=true;
   for(int i=0;i<njet;i++)
   {
      if(v_j_btag70->at(i)) btag_veto=false;
      btag_wgt*=v_j_wgt_btag70->at(i);
   }
   if(btag_veto) cutflow(s_flow).pass(s_cut,"B_veto70",wgt_base*btag_wgt);
   b_wgt[1]=btag_wgt;

   btag_wgt=1;
   btag_veto=true;
   for(int i=0;i<njet;i++)
   {
      if(v_j_btag77->at(i)) btag_veto=false;
      btag_wgt*=v_j_wgt_btag77->at(i);
   }
   if(btag_veto) cutflow(s_flow).pass(s_cut,"B_veto77",wgt_base*btag_wgt);
   b_wgt[2]=btag_wgt;

   btag_wgt=1;
   btag_veto=true;
   for(int i=0;i<njet;i++)
   {
      if(v_j_btag85->at(i)) btag_veto=false;
      btag_wgt*=v_j_wgt_btag85->at(i);
   }
   if(btag_veto) cutflow(s_flow).pass(s_cut,"B_veto85",wgt_base*btag_wgt);
   b_wgt[3]=btag_wgt;
}

void ana::pt_sort(vector<TLorentzVector> v_tlv,vector<int>& v_order)
{
   int temp;
   int nparticle=v_tlv.size();
   for(int i=0;i<nparticle;i++)
      v_order.insert(v_order.end(),i);
   for(int i=0;i<nparticle;i++)   
      for(int j=i+1;j<nparticle;j++)      
         if(v_tlv[v_order[i]].Pt()<v_tlv[v_order[j]].Pt())
         {
            temp=v_order[i];
            v_order[i]=v_order[j];
            v_order[j]=temp;
         }  
}

void ana::Find_m4l_best()
{
   int nlepton=v_l_pid.size();
   int iter[4];
   TLorentzVector m4l_tlv = v_l_tlv[v_l_order[0]];
   for(int i=1;i<4;i++)
      m4l_tlv += v_l_tlv[v_l_order[i]];
   for(int i=0;i<4;i++)
      m4l[i]=v_l_order[i];
   for(iter[0]=0;iter[0]<nlepton;iter[0]++)
      for(iter[1]=iter[0]+1;iter[1]<nlepton;iter[1]++)
         for(iter[2]=iter[1]+1;iter[2]<nlepton;iter[2]++)
            for(iter[3]=iter[2]+1;iter[3]<nlepton;iter[3]++)
            {
               TLorentzVector temp_tlv=v_l_tlv[iter[0]];
               for(int i=1;i<4;i++)
                  temp_tlv += v_l_tlv[iter[i]];
               if(abs(temp_tlv.M()-Z_mass)<abs(m4l_tlv.M()-Z_mass))
               {
                  for(int i=0;i<4;i++)
                     m4l[i]=iter[i];
                  m4l_tlv=temp_tlv;
               }
            }   
   
}
bool ana::Find_m4l()
{
   m4l[0]=v_Z_pair[0].first;
   m4l[1]=v_Z_pair[0].second;
   int j=2;
   for(int i=0;i<v_l_pid.size() && j<4;i++)
   {
      if(v_l_order[i]==m4l[0] || v_l_order[i]==m4l[1]) continue;
      if(j==2) m4l[j]=v_l_order[i];
      if(j==3) {
        // TODO: For emu channel, can never find such m4l
        // if((v_l_pid[v_l_order[i]]+v_l_pid[m4l[2]])==0) m4l[j]=v_l_order[i];
        // else continue;
        m4l[j] = v_l_order[i];
      }
      j++;
   }
   // require 2SFOS
   if (j < 4) {
     mass_4l = -9999.;
     return false;
   }

   TLorentzVector tlv_4l;
   for(int i=0;i<4;i++) tlv_4l+=v_l_tlv[m4l[i]];
   mass_4l=tlv_4l.M();
   return true;
}
void ana::WWZ_chi2()
{
   // to reduce ZZ event
   TLorentzVector WWZ_tlv[4];
   WWZ_tlv[0]=v_l_tlv[v_Z_pair[0].first];
   WWZ_tlv[1]=v_l_tlv[v_Z_pair[0].second];
   WWZ_tlv[2]=v_l_tlv[W_id[0]];
   WWZ_tlv[3]=v_l_tlv[W_id[1]];
   chi2=999999;
   float temp;
   TLorentzVector Z1_tlv,Z2_tlv;
   for(int i=1; i<4; i++)
   {
      Z1_tlv=WWZ_tlv[0]+WWZ_tlv[i];
      for(int j=1; j<4; j++)
      {
         if(j==i) continue;
         Z2_tlv+=WWZ_tlv[j];
      }
      temp=((Z1_tlv.M()-Z_mass)*(Z1_tlv.M()-Z_mass)+(Z2_tlv.M()-Z_mass)*(Z2_tlv.M()-Z_mass))/(2495.2*2495.2);
      if(temp<chi2) chi2= temp;
   }
}
////////////////////////////////////////////////below is major part of ana///////////////////////////////////////////////////////////
////////////////////////////////////////////////////constructors/////////////////////////////////////////////////////////////////////
ana::ana(TTree* tree): ana_base(tree){}

ana::ana(TTree* tree, TString output_file, vector<float> iv_sumofwgt):
   ana_base(tree),
   _output_dir("../output/"),
   _output_file(output_file),
   v_sumofwgt(iv_sumofwgt){}

ana::ana(TTree* tree, TString output_dir, TString output_file, vector<float> iv_sumofwgt): 
   ana_base(tree),
   _output_dir(output_dir),
   _output_file(output_file),
   v_sumofwgt(iv_sumofwgt){}
//////////////////////////////////////////////////////cutflow///////////////////////////////////////////////////////////////////////
CutFlowTool& ana::cutflow(string s, bool ini)
{
   if(ini) m_CutFlowTool.emplace(s,s);
   return m_CutFlowTool.at(s);
}
/////////////////////////////////////////////////////histogram//////////////////////////////////////////////////////////////////////
TH1F* ana::makehist(TString s, bool ini, int nbin, float start, float end)
{
   if(ini) m_hist.emplace(s,new TH1F(s,s,nbin,start,end));
   return m_hist.at(s);
}
TH2F* ana::makehist2d(TString s, bool ini, int xbin, float xstart, float xend, int ybin, float ystart, float yend)
{
   if(ini) m_hist2d.emplace(s, new TH2F(s,s,xbin,xstart,xend,ybin,ystart,yend));
   m_hist2d.at(s)->SetOption("colz");
   return m_hist2d.at(s);
}

void ana::channel_makehist(TString channel_name, int nZ)
{
    
   //makehist(channel_name+"_m4l",true,100,0,1000);
   
   if(nZ>3) return;
   /**
   TString s_number[3]={"first","second","third"};
   for(int i=0;i<nZ;i++)
   {
      makehist(channel_name+"_Z_mass_"+s_number[i],true,60,0,300);
      makehist(channel_name+"_Z_pt_"+s_number[i],true,60,0,300);
   }
   makehist(channel_name+"_MET",true,80,0,400);
   makehist(channel_name+"_METSig",true,80,0,40);
   makehist(channel_name+"_jet_number",true,20,0,20);
   for(int i=0;i<7;i++)
   {
      makehist(channel_name+"_lepton_pt_"+TString::Format("%d",i+1),true, 200, 0, 400);
      makehist(channel_name+"_lepton_eta_"+TString::Format("%d",i+1),true,30,-3,3);
   }
    makehist(channel_name+"_fwdele_pt", true, 200, 0, 400);
    makehist(channel_name+"_fwdele_eta", true,30,-3,3);

   for(int i=0;i<10;i++)
   {
      makehist(channel_name+"_jet_pt_"+TString::Format("%d",i+1),true);
      makehist(channel_name+"_jet_eta_"+TString::Format("%d",i+1),true,30,-3,3);
   }**/
   
}


void ana::channel_fillhist(TString channel_name, int nZ, float fill_wgt)
{
   if(nZ>3) {
     std::cerr << "got 4 Z?" << std::endl;
     return;
   }
   /**
   TString s_number[3]={"first","second","third"};
   TLorentzVector Z_tlv;
   int nlepton=v_l_tlv.size();
   int njet=v_j_tlv->size();
   makehist(channel_name+"_MET")->Fill(MET/1000,fill_wgt);
   makehist(channel_name+"_METSig")->Fill(METSig,fill_wgt);
   makehist(channel_name+"_m4l")->Fill(mass_4l/1000,fill_wgt);
   for(int i=0;i<nZ;i++)
   {
      Z_tlv=v_l_tlv[v_Z_pair[i].first]+v_l_tlv[v_Z_pair[i].second];
      makehist(channel_name+"_Z_mass_"+s_number[i])->Fill(Z_tlv.M()/1000,fill_wgt);
      makehist(channel_name+"_Z_pt_"+s_number[i])->Fill(Z_tlv.Pt()/1000,fill_wgt);
   }
   makehist(channel_name+"_jet_number")->Fill(njet,fill_wgt);
   for(int i=0;i<nlepton && i<7;i++)
   {
      makehist(channel_name+"_lepton_pt_"+TString::Format("%d",i+1))->Fill(v_l_tlv[v_l_order[i]].Pt()/1000,fill_wgt);
      makehist(channel_name+"_lepton_eta_"+TString::Format("%d",i+1))->Fill(v_l_tlv[v_l_order[i]].Eta(),fill_wgt);
   }
   for(int i=0;i<v_e_tlv->size() && i < 7; ++i) {
    if (!v_e_fwd->at(i)) continue;
      makehist(channel_name+"_fwdele_pt")->Fill(v_e_tlv->at(i).Pt()/1000,fill_wgt);
      makehist(channel_name+"_fwdele_eta")->Fill(v_e_tlv->at(i).Eta(),fill_wgt);
   }
   for(int i=0;i<njet && i<10;i++)
   {
      makehist(channel_name+"_jet_pt_"+TString::Format("%d",i+1))->Fill((*v_j_tlv)[v_j_order[i]].Pt()/1000,fill_wgt);
      makehist(channel_name+"_jet_eta_"+TString::Format("%d",i+1))->Fill((*v_j_tlv)[v_j_order[i]].Eta(),fill_wgt);
   }**/
}

void ana::WWZ_makehist(TString channel_name){
   //makes quality electron histos
   /**makehist(channel_name+"_elec_qual_eta_less_1p3",true,3,0,3);
   makehist(channel_name+"_elec_qual_eta_more_1p3",true,3,0,3);
   makehist(channel_name+"_muon_qual_eta_less_1p3",true,3,0,3);
   makehist(channel_name+"_muon_qual_eta_more_1p3",true,3,0,3);
   makehist(channel_name+"_W_elec_qual_eta_less_1p3",true,3,0,3);
   makehist(channel_name+"_W_elec_qual_eta_more_1p3",true,3,0,3);
   makehist(channel_name+"_W_muon_qual_eta_less_1p3",true,3,0,3);
   makehist(channel_name+"_W_muon_qual_eta_more_1p3",true,3,0,3);
   makehist(channel_name+"_Z_elec_qual_eta_less_1p3",true,3,0,3);
   makehist(channel_name+"_Z_elec_qual_eta_more_1p3",true,3,0,3);
   makehist(channel_name+"_Z_muon_qual_eta_less_1p3",true,3,0,3);
   makehist(channel_name+"_Z_muon_qual_eta_more_1p3",true,3,0,3);**/
   //makehist(channel_name+"_Z_event_eta_more",true,3,0,3);
   //makehist(channel_name+"_W_event_eta_more",true,3,0,3);
   //makehist(channel_name+"_elec_event_eta_more",true,3,0,3);
   //makehist(channel_name+"_muon_event_eta_more",true,3,0,3);
   //makehist(channel_name+"_Z_event_eta_less",true,3,0,3);
   //makehist(channel_name+"_W_event_eta_less",true,3,0,3);
   //makehist(channel_name+"_elec_event_eta_less",true,3,0,3);
   //makehist(channel_name+"_muon_event_eta_less",true,3,0,3);
   //makehist(channel_name+"_elec_event_numTight_4",true,5,0,5);
   //makehist(channel_name+"_muon_event_numTight_4",true,5,0,5);
   //makehist(channel_name+"_elec_event_numTight_2",true,5,0,5);
   //makehist(channel_name+"_muon_event_numTight_2",true,5,0,5);
   //makehist(channel_name+"_all_muon_tight",true,3,0,3);
   //makehist(channel_name+"_all_elec_tight",true,3,0,3);
   //makehist(channel_name+"_all_muon_eta_less",true,3,0,3);
   //makehist(channel_name+"_all_elec_eta_less",true,3,0,3);

   //makehist(channel_name+"_Z_event_qual_first",true,3,0,3);
   //makehist(channel_name+"_W_event_qual_first",true,3,0,3);
   //makehist(channel_name+"_Z_event_eta_first",true,2,0,2);
   //makehist(channel_name+"_W_event_eta_first",true,2,0,2);
   //makehist(channel_name+"_Z_event_qual_second",true,3,0,3);
   //makehist(channel_name+"_W_event_qual_second",true,3,0,3);
   //makehist(channel_name+"_Z_event_eta_second",true,2,0,2);
   //makehist(channel_name+"_W_event_eta_second",true,2,0,2);

   //makehist2d(channel_name+"_Z_event_qual",true,3,0,3,3,0,3);
   //makehist2d(channel_name+"_W_event_qual",true,3,0,3,3,0,3);
   //makehist2d(channel_name+"_Z_event_eta",true,2,0,2,2,0,2);
   //makehist2d(channel_name+"_W_event_eta",true,2,0,2,2,0,2);

   //makehist2d(channel_name+"_event_qual",true,5,0,5,5,0,5);
   //makehist2d(channel_name+"_event_eta",true,3,0,3,3,0,3);

   makehist2d(channel_name+"_event_eta_more",true,5,0,5,17,0,3.4);
   /**
   makehist(channel_name+"_event_eta_more_0.0",true,5,0,5);
   makehist(channel_name+"_event_eta_more_0.2",true,5,0,5);
   makehist(channel_name+"_event_eta_more_0.4",true,5,0,5);
   makehist(channel_name+"_event_eta_more_2.4",true,5,0,5);
   makehist(channel_name+"_event_eta_more_2.6",true,5,0,5);
   makehist(channel_name+"_event_eta_more_2.8",true,5,0,5);
   makehist(channel_name+"_event_eta_more_3.0",true,5,0,5);
   makehist(channel_name+"_event_eta_more_3.2",true,5,0,5);**/


   //makehist(channel_name+"_event_eta_more",true,5,0,5);
   //makehist(channel_name+"_event_eta_less",true,5,0,5);
   //makehist(channel_name+"_event_tightness",true,16,0,4);
   makehist(channel_name+"_event_numTight",true,5,0,5);

   makehist2d(channel_name+"_event_eta_more_4tight",true,5,0,5,17,0,3.4);
   makehist2d(channel_name+"_event_eta_more_3tight",true,5,0,5,17,0,3.4);
   makehist2d(channel_name+"_event_eta_more_2tight",true,5,0,5,17,0,3.4);
   makehist2d(channel_name+"_event_eta_more_1tight",true,5,0,5,17,0,3.4);
   makehist2d(channel_name+"_event_eta_more_0tight",true,5,0,5,17,0,3.4);

   makehist2d(channel_name+"_elec_eta_more",true,34,0,3.4,3,0,3);
   makehist2d(channel_name+"_muon_eta_more",true,34,0,3.4,3,0,3);
   //makehist(channel_name+"_event_numMedium",true,5,0,5);
   //makehist(channel_name+"_event_numLoose",true,5,0,5);
   //makehist2d(channel_name+"_event_numTight_eta_less",true,5,0,5,5,0,5);
   //makehist2d(channel_name+"_event_numTight_eta_more",true,5,0,5,5,0,5);
   //makehist(channel_name+"_v_l_pid",true,40,-20,20);


}
void ana::WWZ_fillhist(TString channel_name, float fill_wgt){
   //fill electron quality eta cut histogram
   //initializes variables to be used to fill the histograms
   //8-24-2021
   
   //initializes variables
   int Z_num_eta_more = 0;
   int W_num_eta_more = 0;
   int elec_num_eta_more = 0;
   int muon_num_eta_more = 0;

   int Z_num_eta_first = 0;
   int W_num_eta_first = 0;
   int Z_num_qual_first = 0;
   int W_num_qual_first = 0;
   int Z_num_eta_second = 0;
   int W_num_eta_second = 0;
   int Z_num_qual_second = 0;
   int W_num_qual_second = 0;

   int elec_num_eta_less = 0;
   int muon_num_eta_less = 0;
   int numTight = 0;
   int numMedium = 0;
   int numLoose = 0;
   int numEtaMore = 0;
   int zero = 0;

   for (int i=0; i<4;i++){
      if (v_l_qual[i] == 2){
         numTight += 1;
      }
   }
   makehist(channel_name+"_event_numTight")->Fill(numTight, fill_wgt);

   for (int i=0; i < 17; ++i){
      numEtaMore = 0;
      for (int j=0; j < 4; ++j){
         if (v_l_tlv[j].Eta() > 0.2*i || v_l_tlv[j].Eta() < (-1)*(0.2*i)){
            numEtaMore += 1;
         }
      }

      makehist2d(channel_name+"_event_eta_more")->Fill(numEtaMore, 0.2*i+0.05, fill_wgt);
      if (numTight == 0){
         makehist2d(channel_name+"_event_eta_more_0tight")->Fill(numEtaMore, 0.2*i+0.05, fill_wgt);
      } else if (numTight == 1){
         makehist2d(channel_name+"_event_eta_more_1tight")->Fill(numEtaMore, 0.2*i+0.05, fill_wgt);
      } else if (numTight == 2){
         makehist2d(channel_name+"_event_eta_more_2tight")->Fill(numEtaMore, 0.2*i+0.05, fill_wgt);
      } else if (numTight == 3){
         makehist2d(channel_name+"_event_eta_more_3tight")->Fill(numEtaMore, 0.2*i+0.05, fill_wgt);
      } else {
         makehist2d(channel_name+"_event_eta_more_4tight")->Fill(numEtaMore, 0.2*i+0.05, fill_wgt);
      }
   }

   for (int j=0; j < 4; ++j){
      if (v_l_pid[j] == 11 || v_l_pid[j] == -11) {
         makehist2d(channel_name+"_elec_eta_more")->Fill(v_l_tlv[j].Eta(), v_l_qual[j], fill_wgt);
      } else {
         makehist2d(channel_name+"_muon_eta_more")->Fill(v_l_tlv[j].Eta(), v_l_qual[j], fill_wgt);
      }
   }
   /**
   int numEtaMore00 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 0.0 || v_l_tlv[j].Eta() < -0.0){
         numEtaMore00 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_0.0")->Fill(numEtaMore00, fill_wgt);


   int umEtaMore02 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 0.2 || v_l_tlv[j].Eta() < -0.2){
         numEtaMore02 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_0.2")->Fill(numEtaMore02, fill_wgt);


   int numEtaMore04 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 0.4 || v_l_tlv[j].Eta() < -0.4){
         numEtaMore04 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_0.4")->Fill(numEtaMore04, fill_wgt);


   int numEtaMore24 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 2.4 || v_l_tlv[j].Eta() < -2.4){
         numEtaMore24 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_2.4")->Fill(numEtaMore24, fill_wgt);


   int numEtaMore26 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 2.6 || v_l_tlv[j].Eta() < -2.6){
         numEtaMore26 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_2.6")->Fill(numEtaMore26, fill_wgt);


   int numEtaMore = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 2.8 || v_l_tlv[j].Eta() < -2.8){
         numEtaMore += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_2.8")->Fill(numEtaMore, fill_wgt);

   int numEtaMore30 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 3.0 || v_l_tlv[j].Eta() < -3.0){
         numEtaMore30 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_3.0")->Fill(numEtaMore30, fill_wgt);

   int numEtaMore32 = 0;
   for (int j=0; j < 4; ++j){
      if (v_l_tlv[j].Eta() > 3.2 || v_l_tlv[j].Eta() < -3.2){
         numEtaMore32 += 1;
      }
   }
   makehist(channel_name+"_event_eta_more_3.2")->Fill(numEtaMore32, fill_wgt);
   **/
   /**
   //8-18-2021 -> 9-6-2021
   //fill eta variables
   //first Z lep
   if (v_l_tlv[v_Z_pair[0].first].Eta() > 1.3 || v_l_tlv[v_Z_pair[0].first].Eta() < -1.3) {
      Z_num_eta_first = 1;
      c
   } else {
      if (v_l_pid[v_Z_pair[0].first] == 11 || v_l_pid[v_Z_pair[0].first] == -11) {
         elec_num_eta_less += 1;
      } else {
         muon_num_eta_less += 1;
      }
   }
   //second Z lep
   if (v_l_tlv[v_Z_pair[0].second].Eta() > 1.3 || v_l_tlv[v_Z_pair[0].second].Eta() < -1.3) {
      Z_num_eta_second = 1;
      if (v_l_pid[v_Z_pair[0].second] == 11 || v_l_pid[v_Z_pair[0].second] == -11) {
         elec_num_eta_more += 1;
      } else {
         muon_num_eta_more += 1;
      }
   } else {
      if (v_l_pid[v_Z_pair[0].second] == 11 || v_l_pid[v_Z_pair[0].second] == -11) {
         elec_num_eta_more += 1;
      } else {
         muon_num_eta_more += 1;
      }
   }

   //first W
   if (v_l_tlv[W_id[0]].Eta() > 1.3 || v_l_tlv[W_id[0]].Eta() < -1.3) {
      W_num_eta_first = 1;
      if (v_l_pid[W_id[0]] == 11 || v_l_pid[W_id[0]] == -11) {
         elec_num_eta_more += 1;
      } else {
         muon_num_eta_more += 1;
      }
   } else {
      if (v_l_pid[W_id[0]] == 11 || v_l_pid[W_id[0]] == -11) {
         elec_num_eta_less += 1;
      } else {
         muon_num_eta_less += 1;
      }
   }

   //second W
   if (v_l_tlv[W_id[1]].Eta() > 1.3 || v_l_tlv[W_id[1]].Eta() < -1.3) {
      W_num_eta_second = 1;
      if (v_l_pid[W_id[1]] == 11 || v_l_pid[W_id[1]] == -11) {
         elec_num_eta_more += 1;
      } else {
         muon_num_eta_more += 1;
      }
   } else {
      if (v_l_pid[W_id[1]] == 11 || v_l_pid[W_id[1]] == -11) {
         elec_num_eta_less += 1;
      } else {
         muon_num_eta_less += 1;
      }
   }
   **/
   //fills Z & W qual variables
   if (v_l_qual[v_Z_pair[0].first] == 2) Z_num_qual_first = 2;
   if (v_l_qual[v_Z_pair[0].second] == 2) Z_num_qual_second = 2;
   if (v_l_qual[W_id[0]] == 2) W_num_qual_first = 2;
   if (v_l_qual[W_id[1]] == 2) W_num_qual_second = 2;
   if (v_l_qual[v_Z_pair[0].first] == 1) Z_num_qual_first = 1;
   if (v_l_qual[v_Z_pair[0].second] == 1) Z_num_qual_second = 1;
   if (v_l_qual[W_id[0]] == 1) W_num_qual_first = 1;
   if (v_l_qual[W_id[1]] == 1) W_num_qual_second = 1;
   if (v_l_qual[v_Z_pair[0].first] == 0) Z_num_qual_first = 0;
   if (v_l_qual[v_Z_pair[0].second] == 0) Z_num_qual_second = 0;
   if (v_l_qual[W_id[0]] == 0) W_num_qual_first = 0;
   if (v_l_qual[W_id[1]] == 0) W_num_qual_second = 0;

   /**
   tightnessVect.push_back(v_l_qual[v_Z_pair[0].first]);
   tightnessVect.push_back(v_l_qual[v_Z_pair[0].second]);
   tightnessVect.push_back(v_l_qual[W_id[0]]);
   tightnessVect.push_back(v_l_qual[W_id[1]]);

   for(int i=0; i < tightnessVect.size(); ++i){
      tightness += tightnessVect[i];
   }
   tightness = tightness/tightnessVect.size(); //tightness is the average tightness level**/
   //makehist(channel_name+"_Z_event_eta_more")->Fill(Z_num_eta_more, fill_wgt);
   //makehist(channel_name+"_W_event_eta_more")->Fill(W_num_eta_more, fill_wgt);
   //makehist(channel_name+"_elec_event_eta_more")->Fill(elec_num_eta_more, fill_wgt);
   //makehist(channel_name+"_muon_event_eta_more")->Fill(muon_num_eta_more, fill_wgt);
   
   /**
   //9-6-2021
   makehist(channel_name+"_Z_event_eta_first")->Fill(Z_num_eta_first, fill_wgt);
   makehist(channel_name+"_W_event_eta_first")->Fill(W_num_eta_first, fill_wgt);
   makehist(channel_name+"_Z_event_qual_first")->Fill(Z_num_qual_first, fill_wgt);
   makehist(channel_name+"_W_event_qual_first")->Fill(W_num_qual_first, fill_wgt);

   makehist(channel_name+"_Z_event_eta_second")->Fill(Z_num_eta_second, fill_wgt);
   makehist(channel_name+"_W_event_eta_second")->Fill(W_num_eta_second, fill_wgt);
   makehist(channel_name+"_Z_event_qual_second")->Fill(Z_num_qual_second, fill_wgt);
   makehist(channel_name+"_W_event_qual_second")->Fill(W_num_qual_second, fill_wgt);

   makehist2d(channel_name+"_Z_event_eta")->Fill(Z_num_eta_first, Z_num_eta_second, fill_wgt);
   makehist2d(channel_name+"_W_event_eta")->Fill(W_num_eta_first, W_num_eta_second, fill_wgt);
   makehist2d(channel_name+"_Z_event_qual")->Fill(Z_num_qual_first, Z_num_qual_second, fill_wgt);
   makehist2d(channel_name+"_W_event_qual")->Fill(W_num_qual_first, W_num_qual_second, fill_wgt);

   makehist2d(channel_name+"_event_eta")->Fill(Z_num_eta_first + Z_num_eta_second, W_num_eta_first + W_num_eta_second, fill_wgt);
   makehist2d(channel_name+"_event_qual")->Fill(Z_num_qual_first + Z_num_qual_second, W_num_qual_first + W_num_qual_second, fill_wgt);
   **/

   //makehist(channel_name+"_elec_event_eta_less")->Fill(elec_num_eta_less, fill_wgt);
   //makehist(channel_name+"_muon_event_eta_less")->Fill(muon_num_eta_less, fill_wgt);
   //makehist(channel_name+"_event_eta_more")->Fill(W_num_eta_more+Z_num_eta_more, fill_wgt);
   //makehist(channel_name+"_event_eta_less")->Fill(W_num_eta_less+Z_num_eta_less, fill_wgt);
   
   //makehist(channel_name+"_event_tightness")->Fill(tightness, fill_wgt);
   /**
   //commented 9/3/21
   vector<int> elecTight;
   vector<int> muonTight;
   vector<int> elecEtaLess;
   vector<int> muonEtaLess;

   //fills tight variables
   for (int i=0; i<4;i++){
      makehist(channel_name+"_v_l_pid")->Fill(v_l_pid[i], fill_wgt);
      if (abs(v_l_pid[i]) == 11){
         if (v_l_qual[i] == 2){
            numTight += 1;
            elecTight.push_back(1);
         } else if (v_l_qual[i] == 1){
            numMedium += 1;
            elecTight.push_back(0);
         } else {
            numLoose += 1;
            elecTight.push_back(0);
         }
         if (v_l_tlv[i].Eta() > 1.3 || v_l_tlv[i].Eta() < -1.3){
            elecEtaLess.push_back(0);
         } else {
            elecEtaLess.push_back(1);
         }
      } else if (abs(v_l_pid[i]) == 13){
         if (v_l_qual[i] == 2){
            numTight += 1;
            muonTight.push_back(1);
         } else if (v_l_qual[i] == 1){
            numMedium += 1;
            muonTight.push_back(0);
         } else {
            numLoose += 1;
            muonTight.push_back(0);
         }
         if (v_l_tlv[i].Eta() > 1.3 || v_l_tlv[i].Eta() < -1.3){
            muonEtaLess.push_back(0);
         } else {
            muonEtaLess.push_back(1);
         }
      }

   }
   if (elecTight.size() == accumulate(elecTight.begin(),elecTight.end(),0) && elecTight.size() > 0){
      makehist(channel_name+"_all_elec_tight")->Fill(2, fill_wgt);
   } else if (elecTight.size() > 0){
      makehist(channel_name+"_all_elec_tight")->Fill(1, fill_wgt);
   } else {
      makehist(channel_name+"_all_elec_tight")->Fill(zero, fill_wgt);
   }
   if (muonTight.size() == accumulate(muonTight.begin(),muonTight.end(),0) && muonTight.size() > 0){
      makehist(channel_name+"_all_muon_tight")->Fill(2, fill_wgt);
   } else if (muonTight.size() > 0){
      makehist(channel_name+"_all_muon_tight")->Fill(1, fill_wgt);
   } else {
      makehist(channel_name+"_all_muon_tight")->Fill(zero, fill_wgt);
   }

   if (elecEtaLess.size() == accumulate(elecEtaLess.begin(),elecEtaLess.end(),0) && elecEtaLess.size() > 0){
      makehist(channel_name+"_all_elec_eta_less")->Fill(2, fill_wgt);
   } else if (elecEtaLess.size() > 0){
      makehist(channel_name+"_all_elec_eta_less")->Fill(1, fill_wgt);
   } else {
      makehist(channel_name+"_all_elec_eta_less")->Fill(zero, fill_wgt);
   }

   if (muonEtaLess.size() == accumulate(muonEtaLess.begin(),muonEtaLess.end(),0) && muonEtaLess.size() > 0){
      makehist(channel_name+"_all_muon_eta_less")->Fill(2, fill_wgt);
   } else if (muonEtaLess.size() > 0){
      makehist(channel_name+"_all_muon_eta_less")->Fill(1, fill_wgt);
   } else {
      makehist(channel_name+"_all_muon_eta_less")->Fill(zero, fill_wgt);
   }
   makehist(channel_name+"_event_numTight")->Fill(numTight, fill_wgt);
   makehist(channel_name+"_event_numMedium")->Fill(numMedium, fill_wgt);
   makehist(channel_name+"_event_numLoose")->Fill(numLoose+Z_num_eta_more, fill_wgt);
   //makehist2d(channel_name+"_event_numTight_eta_less")->Fill(numTight, W_num_eta_less+Z_num_eta_less, fill_wgt);
   //makehist2d(channel_name+"_event_numTight_eta_more")->Fill(numTight, W_num_eta_more+Z_num_eta_more, fill_wgt);
   **/
   //8-17-2021
   /**
   int x = 0;
   //Z
   if (v_l_pid[v_Z_pair[0].first] == 11 || v_l_pid[v_Z_pair[0].first] == -11) {
      if (v_l_pid[v_Z_pair[0].second] == 11 || v_l_pid[v_Z_pair[0].second] == -11) {
         makehist(channel_name+"_Z_type")->Fill(x, fill_wgt);
      } else {
         makehist(channel_name+"_Z_type")->Fill(1, fill_wgt);
      }
   } else {
      if (v_l_pid[v_Z_pair[0].second] == 11 || v_l_pid[v_Z_pair[0].second] == -11) {
         makehist(channel_name+"_Z_type")->Fill(2, fill_wgt);
      } else {
         makehist(channel_name+"_Z_type")->Fill(3, fill_wgt);
      }
   }


   //W
   if (v_l_pid[W_id[0]] == 11 || v_l_pid[W_id[0]] == -11) {
      makehist(channel_name+"_W_type_1")->Fill(x, fill_wgt);
      if (v_l_pid[W_id[1]] == 11 || v_l_pid[W_id[1]] == -11) {
         makehist(channel_name+"_W_type")->Fill(x, fill_wgt);
         makehist(channel_name+"_W_type_2")->Fill(x, fill_wgt);
      } else {
         makehist(channel_name+"_W_type")->Fill(1, fill_wgt);
         makehist(channel_name+"_W_type_2")->Fill(1, fill_wgt);
      }
   } else {
      makehist(channel_name+"_W_type_1")->Fill(1, fill_wgt);
      if (v_l_pid[W_id[1]] == 11 || v_l_pid[W_id[1]] == -11) {
         makehist(channel_name+"_W_type")->Fill(2, fill_wgt);
         makehist(channel_name+"_W_type_2")->Fill(x, fill_wgt);
      } else {
         makehist(channel_name+"_W_type")->Fill(3, fill_wgt);
         makehist(channel_name+"_W_type_2")->Fill(1, fill_wgt);
      }
   }**/

   //8-17-2021
   
   //first Z
   /**
   if (v_l_tlv[v_Z_pair[0].first].Eta() > 1.3 || v_l_tlv[v_Z_pair[0].first].Eta() < -1.3) {
      if (v_l_pid[v_Z_pair[0].first] == 11 || v_l_pid[v_Z_pair[0].first] == -11) {
         makehist(channel_name+"_Z_elec_qual_eta_more_1p3")->Fill(v_l_qual[v_Z_pair[0].first], fill_wgt);
      } else {
         makehist(channel_name+"_Z_muon_qual_eta_more_1p3")->Fill(v_l_qual[v_Z_pair[0].first], fill_wgt);
      }
   } else {
      if (v_l_pid[v_Z_pair[0].first] == 11 || v_l_pid[v_Z_pair[0].first] == -11) {
         makehist(channel_name+"_Z_elec_qual_eta_less_1p3")->Fill(v_l_qual[v_Z_pair[0].first], fill_wgt);
      } else {
         makehist(channel_name+"_Z_muon_qual_eta_less_1p3")->Fill(v_l_qual[v_Z_pair[0].first], fill_wgt);
      }
   }
   //second Z
   if (v_l_tlv[v_Z_pair[0].second].Eta() > 1.3 || v_l_tlv[v_Z_pair[0].second].Eta() < -1.3) {
      if (v_l_pid[v_Z_pair[0].second] == 11 || v_l_pid[v_Z_pair[0].second] == -11) {
         makehist(channel_name+"_Z_elec_qual_eta_more_1p3")->Fill(v_l_qual[v_Z_pair[0].second], fill_wgt);
      } else {
         makehist(channel_name+"_Z_muon_qual_eta_more_1p3")->Fill(v_l_qual[v_Z_pair[0].second], fill_wgt);
      }
   } else {
      if (v_l_pid[v_Z_pair[0].second] == 11 || v_l_pid[v_Z_pair[0].second] == -11) {
         makehist(channel_name+"_Z_elec_qual_eta_less_1p3")->Fill(v_l_qual[v_Z_pair[0].second], fill_wgt);
      } else {
         makehist(channel_name+"_Z_muon_qual_eta_less_1p3")->Fill(v_l_qual[v_Z_pair[0].second], fill_wgt);
      }
   }
   //first W
   if (v_l_tlv[W_id[0]].Eta() > 1.3 || v_l_tlv[W_id[0]].Eta() < -1.3) {
      if (v_l_pid[W_id[0]] == 11 || v_l_pid[W_id[0]] == -11) {
         makehist(channel_name+"_W_elec_qual_eta_more_1p3")->Fill(v_l_qual[W_id[0]], fill_wgt);
      } else {
         makehist(channel_name+"_W_muon_qual_eta_more_1p3")->Fill(v_l_qual[W_id[0]], fill_wgt);
      }
   } else {
      if (v_l_pid[W_id[0]] == 11 || v_l_pid[W_id[0]] == -11) {
         makehist(channel_name+"_W_elec_qual_eta_less_1p3")->Fill(v_l_qual[W_id[0]], fill_wgt);
      } else {
         makehist(channel_name+"_W_muon_qual_eta_less_1p3")->Fill(v_l_qual[W_id[0]], fill_wgt);
      }
   }
   //second W
   if (v_l_tlv[W_id[1]].Eta() > 1.3 || v_l_tlv[W_id[1]].Eta() < -1.3) {
      if (v_l_pid[W_id[1]] == 11 || v_l_pid[W_id[1]] == -11) {
         makehist(channel_name+"_W_elec_qual_eta_more_1p3")->Fill(v_l_qual[W_id[1]], fill_wgt);
      } else {
         makehist(channel_name+"_W_muon_qual_eta_more_1p3")->Fill(v_l_qual[W_id[1]], fill_wgt);
      }
   } else {
      if (v_l_pid[W_id[1]] == 11 || v_l_pid[W_id[1]] == -11) {
         makehist(channel_name+"_W_elec_qual_eta_less_1p3")->Fill(v_l_qual[W_id[1]], fill_wgt);
      } else {
         makehist(channel_name+"_W_muon_qual_eta_less_1p3")->Fill(v_l_qual[W_id[1]], fill_wgt);
      }
   }**/
}
float ana::deltaphi(TLorentzVector tlv1, TLorentzVector tlv2){
   float dphi = abs(tlv1.Phi()-tlv2.Phi());
   if(dphi > 3.14159){
      dphi = 2*3.14159 - dphi;
   }
   return dphi;
}
/////////////////////////////////////////////////////////////////Loop///////////////////////////////////////////////////
void ana::Loop()
{
   if (fChain == 0) return;
   Initialize();

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;

      Loop_initialize();

      if(ientry%100000==0) std::cout<<"processing event: "<<ientry<<'\n';
//      if(ientry>100000) break;
      if(ientry==0)
      { 
         std::cout<<"#####################begin of file##################"<<'\n';
         std::cout<<"#sum of weight: "<<v_sumofwgt[fCurrent]<<'\n';
         std::cout<<"#####################end of file####################"<<'\n';
      }
      if(initial_Cut()){ 
         if(ZZZ_Cut())
         {
            ZZZ_operation();
         }
         else if(WZZ_Cut())
         {
            WZZ_operation();
         }
         else if(WWZ_Cut())
         {
            WWZ_operation();
         }
      }
      Loop_terminate();
   }    
   Terminate();

} 

void ana::Loop_initialize()
{
   for (int i=0; i < v_e_tlv->size(); ++i) {
      // do not consider it temporarily
      //if (v_e_fwd->at(i)) continue; //commented it out to resolve a really annoying bug
      v_l_tlv.push_back(v_e_tlv->at(i));
      v_l_pid.push_back(v_e_pid->at(i));
      v_l_wgt.push_back(v_e_wgtLoose->at(i));
      if (v_e_LHTight->at(i)) {
         //v_e_qual.push_back(2);
         v_l_qual.push_back(2);
      } else if (v_e_LHMedium->at(i)) {
         //v_e_qual.push_back(1);
         v_l_qual.push_back(1);
      } else {
         //v_e_qual.push_back(0);
         v_l_qual.push_back(0);
      }
   }
   for (int i=0; i < v_m_tlv->size(); ++i) {
      // do not consider it temporarily
      //if (v_m_lowpt->at(i)) continue;
      v_l_tlv.push_back(v_m_tlv->at(i));
      v_l_pid.push_back(v_m_pid->at(i));
      v_l_wgt.push_back(v_m_wgtLoose->at(i));
      if (v_m_tight->at(i)) {
         //v_m_qual.push_back(2);
         v_l_qual.push_back(2);
      } else if (v_m_medium->at(i)) {
         //v_m_qual.push_back(1);
         v_l_qual.push_back(1);
      } else {
         //v_m_qual.push_back(0);
         v_l_qual.push_back(0);
      }
   }
   pt_sort(v_l_tlv,v_l_order);
   pt_sort(*v_j_tlv,v_j_order);
}

void ana::Loop_terminate()
{
   v_l_tlv.clear();
   WWZ_tlv.clear();
   v_l_pid.clear();
   v_l_wgt.clear();
   v_l_order.clear();
   if(v_Z_pair.size()!=0)
   {
      v_Z_pair.clear();
      v_ignore.clear();
      v_Z_wgt.clear();
   }
   //v_m_qual.clear();
   //v_e_qual.clear();
   v_l_qual.clear();

}


void ana::Initialize()
{
   _output= new TFile(_output_dir+_output_file+".root","recreate");
   _WWZ_tree = new TTree("WWZ","WWZ");
   _WWZ_tree->Branch("WWZ_Z_mass",&WWZ_Z_mass,"WWZ_Z_mass/F");
   _WWZ_tree->Branch("WWZ_dilepton_mass",&WWZ_dilepton_mass,"WWZ_dilepton_mass/F");
 
   cutflow("initial",true)
      .regFlow("initial","initial selection")
      .regCut("All")
      .regCut(">3l")
      .regCut("1_SFOS")
      .regCut("Z_window")
      .regCut("passTrig","",true)
      .regCut("no_fwde_lowptm","",true)
      .regCut("e_fwd","",true)
      .regCut("e_fwd_1","",true)
      .regCut("m_lowpt","",true)
      .regCut("m_lowpt_1","",true)
      .regCut(">6l","",true)
      .regCut("6l","",true)
      .regCut("5l","",true)
      .regCut("4l","",true);   
   cutflow("ZZZ",true)
      .regFlow("ZZZ","cutflow of ZZZ channel")
      .regCut("All")
      .regCut("1_SFOS","",true)
      .regCut("2_SFOS_>6l","",true)
      .regCut("2_SFOS_=6l","",true)
      .regCut("ee_before","",true)
      .regCut("mm_before","",true)
      .regCut("em_before","",true)
      .regCut("3_SFOS_before","",true)
      .regCut("Z3_40GeV")
      .regCut("3_SFOS_after","",true)
      .regCut("passTrig","",true)
      .regCut("no_fwde_lowptm","",true)
      .regCut("e_fwd","",true)
      .regCut("e_fwd_1","",true)
      .regCut("m_lowpt","",true)
      .regCut("m_lowpt_1","",true)
      .regCut("ee_after","",true)
      .regCut("mm_after","",true)
      .regCut("em_after","",true)
      .regCut("ZZZ_>6l","",true)
      .regCut("ZZZ_6l","",true);
   cutflow("WZZ",true)
      .regFlow("WZZ","cutflow of WZZ channel")
      .regCut(">=5l")
      .regCut("2_SFOS")
      .regCut("Z_window")
      .regCut("LeptonPt")
      .regCut("B_veto60","",true)
      .regCut("B_veto70","",true)
      .regCut("B_veto77","",true)
      .regCut("B_veto85","",true)
      .regCut("passTrig","",true)
      .regCut("no_fwde_lowptm","",true)
      .regCut("e_fwd","",true)
      .regCut("e_fwd_1","",true)
      .regCut("m_lowpt","",true)
      .regCut("m_lowpt_1","",true)
      .regCut("WZZ_>6l","",true)
      .regCut("WZZ_6l","",true)
      .regCut("WZZ_5l","",true);
   cutflow("WWZ",true)
      .regFlow("WWZ","cutflow of WWZ channel")
      .regCut(">=4l")
      .regCut("Dilepton")
      .regCut("LeptonPt")
      .regCut("dR>0.1")
      .regCut("B_veto60","",true)
      .regCut("B_veto70","",true)
      .regCut("B_veto77","",true)
      .regCut("B_veto85","",true)
      .regCut("passTrig","",true)
      .regCut("WWZ_>6l","",true)
      .regCut("WWZ_6l","",true)
      .regCut("WWZ_5l","",true)
      .regCut("WWZ_4l","",true)
      .regCut("chargesum=0","",true)
      .regCut("WWZ_SF_noZ","",true)
      .regCut("WWZ_SF_inZ","",true)
      .regCut("WWZ_em","",true);
   // make your own hist
   makehist("Z_mass_first",true);
   makehist("Z_mass_second",true);
   makehist("Z_mass_third",true);
   channel_makehist("ZZZ",3);
   channel_makehist("WZZ",2);
   channel_makehist("WWZ",1);
   channel_makehist("WWZ_SF_noZ",1);
   channel_makehist("WWZ_SF_inZ",1);
   channel_makehist("WWZ_em",1);
   // WWZ channel
   WWZ_makehist("WWZ");
   WWZ_makehist("WWZ_SF_noZ");
   WWZ_makehist("WWZ_SF_inZ");
   WWZ_makehist("WWZ_em");
}

void ana::Terminate()
{
   std::ofstream _ofs_cutflow(_output_dir+_output_file+".txt",std::ofstream::out);   
   cutflow("initial").print(_ofs_cutflow);
   //cutflow("ZZZ").print(_ofs_cutflow);
   //cutflow("WZZ").print(_ofs_cutflow);
   cutflow("WWZ").print(_ofs_cutflow);
   _ofs_cutflow.close();
   _output->Write("All");
   _output->Close();
   delete _output;
}
