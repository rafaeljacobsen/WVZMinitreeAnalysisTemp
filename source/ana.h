#ifndef ana_h
#define ana_h
#include"ana_base.h"
#include"CutFlowTool.h"
#include<string.h>
#include"TFile.h"
#include"TH1F.h"
#include"TH2F.h"
#include<vector>
#include"TLorentzVector.h"
#include<time.h>
#include<fstream>
#define Z_mass 91187.6
using namespace std;

class ana:public ana_base
{
   public:
// variables
      int                          n_e_fwd  ;
      int                          n_m_lowpt;
      int                          m4l[4]   ;
      int                          n_channel;
      int                          n_recover;
      int                          W_id[2]  ;
      float                        mass_4l  ;
      float                        wgt      ;
      float                        ZZZ_wgt  ;
      float                        WZZ_wgt  ;
      float                        WWZ_wgt  ;
      float                        b_wgt[4] ;//0--60 1--70 2--77 3--85
      float                        dR       ;
      vector<TLorentzVector>       v_l_tlv  ;
      vector<TLorentzVector>       WWZ_tlv  ;
      vector<int>                  v_l_pid  ;
      vector<float>                v_l_wgt  ;
      vector<int>                  v_l_order;
      vector<int>                  v_j_order;
      vector<float>                v_Z_wgt  ; // weight for Z leptons, related to v_Z_pair
      vector<pair<int,int> >       v_Z_pair ;
      vector<int>                  v_ignore ;
      //vector<int>		           v_m_qual ;
      //vector<int>                  v_e_qual ;
      vector<int>                  v_l_qual ;



// initial cut
      bool initial_Cut();
// ZZZ
      bool ZZZ_Cut();
      void ZZZ_operation();
// WZZ
      bool WZZ_Cut();
      void WZZ_operation();
// WWZ machine learning variables
      float                                WWZ_Z_mass, WWZ_dilepton_mass;
      float                                chi2;
      float                                WWZ_m4l;
      float                                WWZ_phi[3],WWZ_eta[3];
// WWZ functions
      bool WWZ_Cut();
      void WWZ_operation();
//Loop  functions
      ana(TTree* tree);
      ana(TTree* tree, TString output_file, vector<float> iv_sumofwgt);
      ana(TTree* tree, TString output_dir, TString output_file, vector<float> iv_sumofwgt);
      void Loop()           ;
      void Initialize()     ;
      void Terminate()      ;
      void Loop_initialize();
      void Loop_terminate() ;
//universal functions
      CutFlowTool&  cutflow(string s="NOMINAL",bool ini=false)                                       ;
      TH1F*         makehist(TString s="NULL",bool ini=false,int nbin=20,float start=0,float end=200);
      TH2F*         makehist2d(TString s="NULL",bool ini=false, int xbin=20, float xstart=0, float xend=200, int ybin=20, float ystart=0,float yend=200);
      void          channel_makehist(TString channel_name, int nZ=0)                                 ;
      void          channel_fillhist(TString channel_name, int nZ=0, float fill_wgt=1)               ;
      void          WWZ_makehist(TString channel_name)                                               ;
      void          WWZ_fillhist(TString channel_name, float fill_wgt=1)                             ;
      void          WWZ_chi2()                                                                       ;
      float         deltaphi(TLorentzVector tlv1, TLorentzVector tlv2)                           ;
      void          Find_Z_pair()                                                                    ;
      void          Bjet_Cut(string s_flow, string s_cut, float wgt_base)                            ;
      void          pt_sort(vector<TLorentzVector> v_tlv, vector<int>& v_order)                      ;
      void          Find_m4l_best()                                                                  ;
      bool          Find_m4l()                                                                       ;
   private:
      TString                      _output_dir      ;
      TString                      _output_file     ;
      TFile*                       _output          ;
      TTree*                       _WWZ_tree        ;
      map<TString, TH1F*>          m_hist           ;
      map<TString, TH2F*>          m_hist2d         ;
      map<string,CutFlowTool>      m_CutFlowTool    ;
      vector<float>                v_sumofwgt       ;

};
#endif
