//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Jun 14 20:22:35 2021 by ROOT version 6.20/06
// from TTree tree_NOMINAL/output tree
// found on file: mc16_13TeV.364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6.deriv.DAOD_STDM3.e5887_s3126_r10201_p4252.root
//////////////////////////////////////////////////////////

#ifndef ana_base_h
#define ana_base_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <vector>
#include "TLorentzVector.h"
// Header file for the classes stored in the TTree if any.
#include "vector"
#include "vector"
#include "vector"
using namespace std;
class ana_base {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         mu;
   Int_t           run;
   Bool_t          passTrig;
   ULong64_t       event;
   Double_t        weight;
   Float_t         w_sf_jvt;
   Float_t         w_prw;
   vector<float>   *v_mcGenWgt;
   vector<TLorentzVector> *v_e_tlv;
   vector<int>     *v_e_pid;
   vector<bool>    *v_e_LHTight;
   vector<bool>    *v_e_LHMedium;
   vector<bool>    *v_e_ambiguous;
   vector<bool>    *v_e_fwd;
   vector<float>   *v_e_wgtLoose;
   vector<float>   *v_e_wgtTight;
   vector<float>   *v_e_wgtIso;
   vector<TLorentzVector> *v_m_tlv;
   vector<int>     *v_m_pid;
   vector<float>   *v_m_d0;
   vector<bool>    *v_m_medium;
   vector<bool>    *v_m_tight;
   vector<bool>    *v_m_lowpt;
   vector<bool>    *v_m_CtSaSa;
   vector<float>   *v_m_wgtLoose;
   vector<float>   *v_m_wgtIso;
   vector<float>   *v_m_wgtIsoVarRad;
   vector<TLorentzVector> *v_m_tlv_fsr;
   vector<int>     *v_m_pid_fsr;
   vector<float>   *v_m_d0_fsr;
   vector<bool>    *v_m_medium_fsr;
   vector<bool>    *v_m_tight_fsr;
   vector<bool>    *v_m_lowpt_fsr;
   vector<bool>    *v_m_CtSaSa_fsr;
   vector<float>   *v_m_wgtLoose_fsr;
   vector<float>   *v_m_wgtIso_fsr;
   vector<float>   *v_m_wgtIsoVarRad_fsr;
   Double_t        MET;
   Double_t        METPhi;
   Double_t        METSig;
   vector<TLorentzVector> *v_j_tlv;
   vector<bool>    *v_j_btag60;
   vector<bool>    *v_j_btag70;
   vector<bool>    *v_j_btag77;
   vector<bool>    *v_j_btag85;
   vector<float>   *v_j_wgt_btag60;
   vector<float>   *v_j_wgt_btag70;
   vector<float>   *v_j_wgt_btag77;
   vector<float>   *v_j_wgt_btag85;
   vector<int>     *v_j_btagCont;
   vector<float>   *v_j_wgt_btagCont;
   vector<float>   *v_m_ptvarcone30_TightTTVA_pt1000;
   vector<float>   *v_m_ptvarcone30_TightTTVA_pt1000_fsr;
   vector<float>   *v_m_ptvarcone30_TightTTVA_pt500;
   vector<float>   *v_m_ptvarcone30_TightTTVA_pt500_fsr;
   vector<float>   *v_m_ptcone20_TightTTVA_pt1000;
   vector<float>   *v_m_ptcone20_TightTTVA_pt1000_fsr;
   vector<float>   *v_m_ptcone20_TightTTVA_pt500;
   vector<float>   *v_m_ptcone20_TightTTVA_pt500_fsr;
   vector<float>   *v_m_topoetcone20;
   vector<float>   *v_m_topoetcone20_fsr;
   vector<float>   *v_m_neflowisol20;
   vector<float>   *v_m_neflowisol20_fsr;
   vector<float>   *v_e_ptvarcone30_TightTTVALooseCone_pt1000;
   vector<float>   *v_e_ptcone20_TightTTVALooseCone_pt1000;
   vector<float>   *v_e_topoetcone20;
   vector<bool>    *v_m_passIso_PflowTight_VarRad;
   vector<bool>    *v_m_passIso_PflowTight_VarRad_fsr;
   vector<bool>    *v_m_passIso_PflowTight_FixedRad;
   vector<bool>    *v_m_passIso_PflowTight_FixedRad_fsr;
   vector<bool>    *v_m_passIso_PflowLoose_VarRad;
   vector<bool>    *v_m_passIso_PflowLoose_VarRad_fsr;
   vector<bool>    *v_m_passIso_PflowLoose_FixedRad;
   vector<bool>    *v_m_passIso_PflowLoose_FixedRad_fsr;
   vector<bool>    *v_m_passIso_HighPtTrackOnly;
   vector<bool>    *v_m_passIso_HighPtTrackOnly_fsr;
   vector<bool>    *v_m_passIso_TightTrackOnly_VarRad;
   vector<bool>    *v_m_passIso_TightTrackOnly_VarRad_fsr;
   vector<bool>    *v_m_passIso_TightTrackOnly_FixedRad;
   vector<bool>    *v_m_passIso_TightTrackOnly_FixedRad_fsr;
   vector<bool>    *v_m_passIso_Tight_VarRad;
   vector<bool>    *v_m_passIso_Tight_VarRad_fsr;
   vector<bool>    *v_m_passIso_Tight_FixedRad;
   vector<bool>    *v_m_passIso_Tight_FixedRad_fsr;
   vector<bool>    *v_m_passIso_Loose_VarRad;
   vector<bool>    *v_m_passIso_Loose_VarRad_fsr;
   vector<bool>    *v_m_passIso_Loose_FixedRad;
   vector<bool>    *v_m_passIso_Loose_FixedRad_fsr;
   vector<bool>    *v_e_passIso_HighPtCaloOnly;
   vector<bool>    *v_e_passIso_TightTrackOnly_VarRad;
   vector<bool>    *v_e_passIso_TightTrackOnly_FixedRad;
   vector<bool>    *v_e_passIso_Tight_VarRad;
   vector<bool>    *v_e_passIso_Loose_VarRad;
   vector<TLorentzVector> *v_truth_l_tlv;
   vector<int>     *v_truth_l_pdgId;
   vector<bool>    *v_truth_l_fromTau;
   vector<TLorentzVector> *v_truth_j_tlv;
   Bool_t          tauEvent;

   // List of branches
   TBranch        *b_mu;   //!
   TBranch        *b_run;   //!
   TBranch        *b_passTrig;   //!
   TBranch        *b_event;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_w_sf_jvt;   //!
   TBranch        *b_w_prw;   //!
   TBranch        *b_v_mcGenWgt;   //!
   TBranch        *b_v_e_tlv;   //!
   TBranch        *b_v_e_pid;   //!
   TBranch        *b_v_e_LHTight;   //!
   TBranch        *b_v_e_LHMedium;   //!
   TBranch        *b_v_e_ambiguous;   //!
   TBranch        *b_v_e_fwd;   //!
   TBranch        *b_v_e_wgtLoose;   //!
   TBranch        *b_v_e_wgtTight;   //!
   TBranch        *b_v_e_wgtIso;   //!
   TBranch        *b_v_m_tlv;   //!
   TBranch        *b_v_m_pid;   //!
   TBranch        *b_v_m_d0;   //!
   TBranch        *b_v_m_medium;   //!
   TBranch        *b_v_m_tight;   //!
   TBranch        *b_v_m_lowpt;   //!
   TBranch        *b_v_m_CtSaSa;   //!
   TBranch        *b_v_m_wgtLoose;   //!
   TBranch        *b_v_m_wgtIso;   //!
   TBranch        *b_v_m_wgtIsoVarRad;   //!
   TBranch        *b_v_m_tlv_fsr;   //!
   TBranch        *b_v_m_pid_fsr;   //!
   TBranch        *b_v_m_d0_fsr;   //!
   TBranch        *b_v_m_medium_fsr;   //!
   TBranch        *b_v_m_tight_fsr;   //!
   TBranch        *b_v_m_lowpt_fsr;   //!
   TBranch        *b_v_m_CtSaSa_fsr;   //!
   TBranch        *b_v_m_wgtLoose_fsr;   //!
   TBranch        *b_v_m_wgtIso_fsr;   //!
   TBranch        *b_v_m_wgtIsoVarRad_fsr;   //!
   TBranch        *b_MET;   //!
   TBranch        *b_METPhi;   //!
   TBranch        *b_METSig;   //!
   TBranch        *b_v_j_tlv;   //!
   TBranch        *b_v_j_btag60;   //!
   TBranch        *b_v_j_btag70;   //!
   TBranch        *b_v_j_btag77;   //!
   TBranch        *b_v_j_btag85;   //!
   TBranch        *b_v_j_wgt_btag60;   //!
   TBranch        *b_v_j_wgt_btag70;   //!
   TBranch        *b_v_j_wgt_btag77;   //!
   TBranch        *b_v_j_wgt_btag85;   //!
   TBranch        *b_v_j_btagCont;   //!
   TBranch        *b_v_j_wgt_btagCont;   //!
   TBranch        *b_v_m_ptvarcone30_TightTTVA_pt1000;   //!
   TBranch        *b_v_m_ptvarcone30_TightTTVA_pt1000_fsr;   //!
   TBranch        *b_v_m_ptvarcone30_TightTTVA_pt500;   //!
   TBranch        *b_v_m_ptvarcone30_TightTTVA_pt500_fsr;   //!
   TBranch        *b_v_m_ptcone20_TightTTVA_pt1000;   //!
   TBranch        *b_v_m_ptcone20_TightTTVA_pt1000_fsr;   //!
   TBranch        *b_v_m_ptcone20_TightTTVA_pt500;   //!
   TBranch        *b_v_m_ptcone20_TightTTVA_pt500_fsr;   //!
   TBranch        *b_v_m_topoetcone20;   //!
   TBranch        *b_v_m_topoetcone20_fsr;   //!
   TBranch        *b_v_m_neflowisol20;   //!
   TBranch        *b_v_m_neflowisol20_fsr;   //!
   TBranch        *b_v_e_ptvarcone30_TightTTVALooseCone_pt1000;   //!
   TBranch        *b_v_e_ptcone20_TightTTVALooseCone_pt1000;   //!
   TBranch        *b_v_e_topoetcone20;   //!
   TBranch        *b_v_m_passIso_PflowTight_VarRad;   //!
   TBranch        *b_v_m_passIso_PflowTight_VarRad_fsr;   //!
   TBranch        *b_v_m_passIso_PflowTight_FixedRad;   //!
   TBranch        *b_v_m_passIso_PflowTight_FixedRad_fsr;   //!
   TBranch        *b_v_m_passIso_PflowLoose_VarRad;   //!
   TBranch        *b_v_m_passIso_PflowLoose_VarRad_fsr;   //!
   TBranch        *b_v_m_passIso_PflowLoose_FixedRad;   //!
   TBranch        *b_v_m_passIso_PflowLoose_FixedRad_fsr;   //!
   TBranch        *b_v_m_passIso_HighPtTrackOnly;   //!
   TBranch        *b_v_m_passIso_HighPtTrackOnly_fsr;   //!
   TBranch        *b_v_m_passIso_TightTrackOnly_VarRad;   //!
   TBranch        *b_v_m_passIso_TightTrackOnly_VarRad_fsr;   //!
   TBranch        *b_v_m_passIso_TightTrackOnly_FixedRad;   //!
   TBranch        *b_v_m_passIso_TightTrackOnly_FixedRad_fsr;   //!
   TBranch        *b_v_m_passIso_Tight_VarRad;   //!
   TBranch        *b_v_m_passIso_Tight_VarRad_fsr;   //!
   TBranch        *b_v_m_passIso_Tight_FixedRad;   //!
   TBranch        *b_v_m_passIso_Tight_FixedRad_fsr;   //!
   TBranch        *b_v_m_passIso_Loose_VarRad;   //!
   TBranch        *b_v_m_passIso_Loose_VarRad_fsr;   //!
   TBranch        *b_v_m_passIso_Loose_FixedRad;   //!
   TBranch        *b_v_m_passIso_Loose_FixedRad_fsr;   //!
   TBranch        *b_v_e_passIso_HighPtCaloOnly;   //!
   TBranch        *b_v_e_passIso_TightTrackOnly_VarRad;   //!
   TBranch        *b_v_e_passIso_TightTrackOnly_FixedRad;   //!
   TBranch        *b_v_e_passIso_Tight_VarRad;   //!
   TBranch        *b_v_e_passIso_Loose_VarRad;   //!
   TBranch        *b_v_truth_l_tlv;   //!
   TBranch        *b_v_truth_l_pdgId;   //!
   TBranch        *b_v_truth_l_fromTau;   //!
   TBranch        *b_v_truth_j_tlv;   //!
   TBranch        *b_tauEvent;   //!

   ana_base(TTree *tree=0);
   virtual ~ana_base();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef ana_base_cxx
ana_base::ana_base(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("mc16_13TeV.364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6.deriv.DAOD_STDM3.e5887_s3126_r10201_p4252.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("mc16_13TeV.364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6.deriv.DAOD_STDM3.e5887_s3126_r10201_p4252.root");
      }
      f->GetObject("tree_NOMINAL",tree);

   }
   Init(tree);
}

ana_base::~ana_base()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t ana_base::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t ana_base::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void ana_base::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   v_mcGenWgt = 0;
   v_e_tlv = 0;
   v_e_pid = 0;
   v_e_LHTight = 0;
   v_e_LHMedium = 0;
   v_e_ambiguous = 0;
   v_e_fwd = 0;
   v_e_wgtLoose = 0;
   v_e_wgtTight = 0;
   v_e_wgtIso = 0;
   v_m_tlv = 0;
   v_m_pid = 0;
   v_m_d0 = 0;
   v_m_medium = 0;
   v_m_tight = 0;
   v_m_lowpt = 0;
   v_m_CtSaSa = 0;
   v_m_wgtLoose = 0;
   v_m_wgtIso = 0;
   v_m_wgtIsoVarRad = 0;
   v_m_tlv_fsr = 0;
   v_m_pid_fsr = 0;
   v_m_d0_fsr = 0;
   v_m_medium_fsr = 0;
   v_m_tight_fsr = 0;
   v_m_lowpt_fsr = 0;
   v_m_CtSaSa_fsr = 0;
   v_m_wgtLoose_fsr = 0;
   v_m_wgtIso_fsr = 0;
   v_m_wgtIsoVarRad_fsr = 0;
   v_j_tlv = 0;
   v_j_btag60 = 0;
   v_j_btag70 = 0;
   v_j_btag77 = 0;
   v_j_btag85 = 0;
   v_j_wgt_btag60 = 0;
   v_j_wgt_btag70 = 0;
   v_j_wgt_btag77 = 0;
   v_j_wgt_btag85 = 0;
   v_j_btagCont = 0;
   v_j_wgt_btagCont = 0;
   v_m_ptvarcone30_TightTTVA_pt1000 = 0;
   v_m_ptvarcone30_TightTTVA_pt1000_fsr = 0;
   v_m_ptvarcone30_TightTTVA_pt500 = 0;
   v_m_ptvarcone30_TightTTVA_pt500_fsr = 0;
   v_m_ptcone20_TightTTVA_pt1000 = 0;
   v_m_ptcone20_TightTTVA_pt1000_fsr = 0;
   v_m_ptcone20_TightTTVA_pt500 = 0;
   v_m_ptcone20_TightTTVA_pt500_fsr = 0;
   v_m_topoetcone20 = 0;
   v_m_topoetcone20_fsr = 0;
   v_m_neflowisol20 = 0;
   v_m_neflowisol20_fsr = 0;
   v_e_ptvarcone30_TightTTVALooseCone_pt1000 = 0;
   v_e_ptcone20_TightTTVALooseCone_pt1000 = 0;
   v_e_topoetcone20 = 0;
   v_m_passIso_PflowTight_VarRad = 0;
   v_m_passIso_PflowTight_VarRad_fsr = 0;
   v_m_passIso_PflowTight_FixedRad = 0;
   v_m_passIso_PflowTight_FixedRad_fsr = 0;
   v_m_passIso_PflowLoose_VarRad = 0;
   v_m_passIso_PflowLoose_VarRad_fsr = 0;
   v_m_passIso_PflowLoose_FixedRad = 0;
   v_m_passIso_PflowLoose_FixedRad_fsr = 0;
   v_m_passIso_HighPtTrackOnly = 0;
   v_m_passIso_HighPtTrackOnly_fsr = 0;
   v_m_passIso_TightTrackOnly_VarRad = 0;
   v_m_passIso_TightTrackOnly_VarRad_fsr = 0;
   v_m_passIso_TightTrackOnly_FixedRad = 0;
   v_m_passIso_TightTrackOnly_FixedRad_fsr = 0;
   v_m_passIso_Tight_VarRad = 0;
   v_m_passIso_Tight_VarRad_fsr = 0;
   v_m_passIso_Tight_FixedRad = 0;
   v_m_passIso_Tight_FixedRad_fsr = 0;
   v_m_passIso_Loose_VarRad = 0;
   v_m_passIso_Loose_VarRad_fsr = 0;
   v_m_passIso_Loose_FixedRad = 0;
   v_m_passIso_Loose_FixedRad_fsr = 0;
   v_e_passIso_HighPtCaloOnly = 0;
   v_e_passIso_TightTrackOnly_VarRad = 0;
   v_e_passIso_TightTrackOnly_FixedRad = 0;
   v_e_passIso_Tight_VarRad = 0;
   v_e_passIso_Loose_VarRad = 0;
   v_truth_l_tlv = 0;
   v_truth_l_pdgId = 0;
   v_truth_l_fromTau = 0;
   v_truth_j_tlv = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("mu", &mu, &b_mu);
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("passTrig", &passTrig, &b_passTrig);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("w_sf_jvt", &w_sf_jvt, &b_w_sf_jvt);
   fChain->SetBranchAddress("w_prw", &w_prw, &b_w_prw);
   fChain->SetBranchAddress("v_mcGenWgt", &v_mcGenWgt, &b_v_mcGenWgt);
   fChain->SetBranchAddress("v_e_tlv", &v_e_tlv, &b_v_e_tlv);
   fChain->SetBranchAddress("v_e_pid", &v_e_pid, &b_v_e_pid);
   fChain->SetBranchAddress("v_e_LHTight", &v_e_LHTight, &b_v_e_LHTight);
   fChain->SetBranchAddress("v_e_LHMedium", &v_e_LHMedium, &b_v_e_LHMedium);
   fChain->SetBranchAddress("v_e_ambiguous", &v_e_ambiguous, &b_v_e_ambiguous);
   fChain->SetBranchAddress("v_e_fwd", &v_e_fwd, &b_v_e_fwd);
   fChain->SetBranchAddress("v_e_wgtLoose", &v_e_wgtLoose, &b_v_e_wgtLoose);
   fChain->SetBranchAddress("v_e_wgtTight", &v_e_wgtTight, &b_v_e_wgtTight);
   fChain->SetBranchAddress("v_e_wgtIso", &v_e_wgtIso, &b_v_e_wgtIso);
   fChain->SetBranchAddress("v_m_tlv", &v_m_tlv, &b_v_m_tlv);
   fChain->SetBranchAddress("v_m_pid", &v_m_pid, &b_v_m_pid);
   fChain->SetBranchAddress("v_m_d0", &v_m_d0, &b_v_m_d0);
   fChain->SetBranchAddress("v_m_medium", &v_m_medium, &b_v_m_medium);
   fChain->SetBranchAddress("v_m_tight", &v_m_tight, &b_v_m_tight);
   fChain->SetBranchAddress("v_m_lowpt", &v_m_lowpt, &b_v_m_lowpt);
   fChain->SetBranchAddress("v_m_CtSaSa", &v_m_CtSaSa, &b_v_m_CtSaSa);
   fChain->SetBranchAddress("v_m_wgtLoose", &v_m_wgtLoose, &b_v_m_wgtLoose);
   fChain->SetBranchAddress("v_m_wgtIso", &v_m_wgtIso, &b_v_m_wgtIso);
   fChain->SetBranchAddress("v_m_wgtIsoVarRad", &v_m_wgtIsoVarRad, &b_v_m_wgtIsoVarRad);
   fChain->SetBranchAddress("v_m_tlv_fsr", &v_m_tlv_fsr, &b_v_m_tlv_fsr);
   fChain->SetBranchAddress("v_m_pid_fsr", &v_m_pid_fsr, &b_v_m_pid_fsr);
   fChain->SetBranchAddress("v_m_d0_fsr", &v_m_d0_fsr, &b_v_m_d0_fsr);
   fChain->SetBranchAddress("v_m_medium_fsr", &v_m_medium_fsr, &b_v_m_medium_fsr);
   fChain->SetBranchAddress("v_m_tight_fsr", &v_m_tight_fsr, &b_v_m_tight_fsr);
   fChain->SetBranchAddress("v_m_lowpt_fsr", &v_m_lowpt_fsr, &b_v_m_lowpt_fsr);
   fChain->SetBranchAddress("v_m_CtSaSa_fsr", &v_m_CtSaSa_fsr, &b_v_m_CtSaSa_fsr);
   fChain->SetBranchAddress("v_m_wgtLoose_fsr", &v_m_wgtLoose_fsr, &b_v_m_wgtLoose_fsr);
   fChain->SetBranchAddress("v_m_wgtIso_fsr", &v_m_wgtIso_fsr, &b_v_m_wgtIso_fsr);
   fChain->SetBranchAddress("v_m_wgtIsoVarRad_fsr", &v_m_wgtIsoVarRad_fsr, &b_v_m_wgtIsoVarRad_fsr);
   fChain->SetBranchAddress("MET", &MET, &b_MET);
   fChain->SetBranchAddress("METPhi", &METPhi, &b_METPhi);
   fChain->SetBranchAddress("METSig", &METSig, &b_METSig);
   fChain->SetBranchAddress("v_j_tlv", &v_j_tlv, &b_v_j_tlv);
   fChain->SetBranchAddress("v_j_btag60", &v_j_btag60, &b_v_j_btag60);
   fChain->SetBranchAddress("v_j_btag70", &v_j_btag70, &b_v_j_btag70);
   fChain->SetBranchAddress("v_j_btag77", &v_j_btag77, &b_v_j_btag77);
   fChain->SetBranchAddress("v_j_btag85", &v_j_btag85, &b_v_j_btag85);
   fChain->SetBranchAddress("v_j_wgt_btag60", &v_j_wgt_btag60, &b_v_j_wgt_btag60);
   fChain->SetBranchAddress("v_j_wgt_btag70", &v_j_wgt_btag70, &b_v_j_wgt_btag70);
   fChain->SetBranchAddress("v_j_wgt_btag77", &v_j_wgt_btag77, &b_v_j_wgt_btag77);
   fChain->SetBranchAddress("v_j_wgt_btag85", &v_j_wgt_btag85, &b_v_j_wgt_btag85);
   fChain->SetBranchAddress("v_j_btagCont", &v_j_btagCont, &b_v_j_btagCont);
   fChain->SetBranchAddress("v_j_wgt_btagCont", &v_j_wgt_btagCont, &b_v_j_wgt_btagCont);
   fChain->SetBranchAddress("v_m_ptvarcone30_TightTTVA_pt1000", &v_m_ptvarcone30_TightTTVA_pt1000, &b_v_m_ptvarcone30_TightTTVA_pt1000);
   fChain->SetBranchAddress("v_m_ptvarcone30_TightTTVA_pt1000_fsr", &v_m_ptvarcone30_TightTTVA_pt1000_fsr, &b_v_m_ptvarcone30_TightTTVA_pt1000_fsr);
   fChain->SetBranchAddress("v_m_ptvarcone30_TightTTVA_pt500", &v_m_ptvarcone30_TightTTVA_pt500, &b_v_m_ptvarcone30_TightTTVA_pt500);
   fChain->SetBranchAddress("v_m_ptvarcone30_TightTTVA_pt500_fsr", &v_m_ptvarcone30_TightTTVA_pt500_fsr, &b_v_m_ptvarcone30_TightTTVA_pt500_fsr);
   fChain->SetBranchAddress("v_m_ptcone20_TightTTVA_pt1000", &v_m_ptcone20_TightTTVA_pt1000, &b_v_m_ptcone20_TightTTVA_pt1000);
   fChain->SetBranchAddress("v_m_ptcone20_TightTTVA_pt1000_fsr", &v_m_ptcone20_TightTTVA_pt1000_fsr, &b_v_m_ptcone20_TightTTVA_pt1000_fsr);
   fChain->SetBranchAddress("v_m_ptcone20_TightTTVA_pt500", &v_m_ptcone20_TightTTVA_pt500, &b_v_m_ptcone20_TightTTVA_pt500);
   fChain->SetBranchAddress("v_m_ptcone20_TightTTVA_pt500_fsr", &v_m_ptcone20_TightTTVA_pt500_fsr, &b_v_m_ptcone20_TightTTVA_pt500_fsr);
   fChain->SetBranchAddress("v_m_topoetcone20", &v_m_topoetcone20, &b_v_m_topoetcone20);
   fChain->SetBranchAddress("v_m_topoetcone20_fsr", &v_m_topoetcone20_fsr, &b_v_m_topoetcone20_fsr);
   fChain->SetBranchAddress("v_m_neflowisol20", &v_m_neflowisol20, &b_v_m_neflowisol20);
   fChain->SetBranchAddress("v_m_neflowisol20_fsr", &v_m_neflowisol20_fsr, &b_v_m_neflowisol20_fsr);
   fChain->SetBranchAddress("v_e_ptvarcone30_TightTTVALooseCone_pt1000", &v_e_ptvarcone30_TightTTVALooseCone_pt1000, &b_v_e_ptvarcone30_TightTTVALooseCone_pt1000);
   fChain->SetBranchAddress("v_e_ptcone20_TightTTVALooseCone_pt1000", &v_e_ptcone20_TightTTVALooseCone_pt1000, &b_v_e_ptcone20_TightTTVALooseCone_pt1000);
   fChain->SetBranchAddress("v_e_topoetcone20", &v_e_topoetcone20, &b_v_e_topoetcone20);
   fChain->SetBranchAddress("v_m_passIso_PflowTight_VarRad", &v_m_passIso_PflowTight_VarRad, &b_v_m_passIso_PflowTight_VarRad);
   fChain->SetBranchAddress("v_m_passIso_PflowTight_VarRad_fsr", &v_m_passIso_PflowTight_VarRad_fsr, &b_v_m_passIso_PflowTight_VarRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_PflowTight_FixedRad", &v_m_passIso_PflowTight_FixedRad, &b_v_m_passIso_PflowTight_FixedRad);
   fChain->SetBranchAddress("v_m_passIso_PflowTight_FixedRad_fsr", &v_m_passIso_PflowTight_FixedRad_fsr, &b_v_m_passIso_PflowTight_FixedRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_PflowLoose_VarRad", &v_m_passIso_PflowLoose_VarRad, &b_v_m_passIso_PflowLoose_VarRad);
   fChain->SetBranchAddress("v_m_passIso_PflowLoose_VarRad_fsr", &v_m_passIso_PflowLoose_VarRad_fsr, &b_v_m_passIso_PflowLoose_VarRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_PflowLoose_FixedRad", &v_m_passIso_PflowLoose_FixedRad, &b_v_m_passIso_PflowLoose_FixedRad);
   fChain->SetBranchAddress("v_m_passIso_PflowLoose_FixedRad_fsr", &v_m_passIso_PflowLoose_FixedRad_fsr, &b_v_m_passIso_PflowLoose_FixedRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_HighPtTrackOnly", &v_m_passIso_HighPtTrackOnly, &b_v_m_passIso_HighPtTrackOnly);
   fChain->SetBranchAddress("v_m_passIso_HighPtTrackOnly_fsr", &v_m_passIso_HighPtTrackOnly_fsr, &b_v_m_passIso_HighPtTrackOnly_fsr);
   fChain->SetBranchAddress("v_m_passIso_TightTrackOnly_VarRad", &v_m_passIso_TightTrackOnly_VarRad, &b_v_m_passIso_TightTrackOnly_VarRad);
   fChain->SetBranchAddress("v_m_passIso_TightTrackOnly_VarRad_fsr", &v_m_passIso_TightTrackOnly_VarRad_fsr, &b_v_m_passIso_TightTrackOnly_VarRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_TightTrackOnly_FixedRad", &v_m_passIso_TightTrackOnly_FixedRad, &b_v_m_passIso_TightTrackOnly_FixedRad);
   fChain->SetBranchAddress("v_m_passIso_TightTrackOnly_FixedRad_fsr", &v_m_passIso_TightTrackOnly_FixedRad_fsr, &b_v_m_passIso_TightTrackOnly_FixedRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_Tight_VarRad", &v_m_passIso_Tight_VarRad, &b_v_m_passIso_Tight_VarRad);
   fChain->SetBranchAddress("v_m_passIso_Tight_VarRad_fsr", &v_m_passIso_Tight_VarRad_fsr, &b_v_m_passIso_Tight_VarRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_Tight_FixedRad", &v_m_passIso_Tight_FixedRad, &b_v_m_passIso_Tight_FixedRad);
   fChain->SetBranchAddress("v_m_passIso_Tight_FixedRad_fsr", &v_m_passIso_Tight_FixedRad_fsr, &b_v_m_passIso_Tight_FixedRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_Loose_VarRad", &v_m_passIso_Loose_VarRad, &b_v_m_passIso_Loose_VarRad);
   fChain->SetBranchAddress("v_m_passIso_Loose_VarRad_fsr", &v_m_passIso_Loose_VarRad_fsr, &b_v_m_passIso_Loose_VarRad_fsr);
   fChain->SetBranchAddress("v_m_passIso_Loose_FixedRad", &v_m_passIso_Loose_FixedRad, &b_v_m_passIso_Loose_FixedRad);
   fChain->SetBranchAddress("v_m_passIso_Loose_FixedRad_fsr", &v_m_passIso_Loose_FixedRad_fsr, &b_v_m_passIso_Loose_FixedRad_fsr);
   fChain->SetBranchAddress("v_e_passIso_HighPtCaloOnly", &v_e_passIso_HighPtCaloOnly, &b_v_e_passIso_HighPtCaloOnly);
   fChain->SetBranchAddress("v_e_passIso_TightTrackOnly_VarRad", &v_e_passIso_TightTrackOnly_VarRad, &b_v_e_passIso_TightTrackOnly_VarRad);
   fChain->SetBranchAddress("v_e_passIso_TightTrackOnly_FixedRad", &v_e_passIso_TightTrackOnly_FixedRad, &b_v_e_passIso_TightTrackOnly_FixedRad);
   fChain->SetBranchAddress("v_e_passIso_Tight_VarRad", &v_e_passIso_Tight_VarRad, &b_v_e_passIso_Tight_VarRad);
   fChain->SetBranchAddress("v_e_passIso_Loose_VarRad", &v_e_passIso_Loose_VarRad, &b_v_e_passIso_Loose_VarRad);
   fChain->SetBranchAddress("v_truth_l_tlv", &v_truth_l_tlv, &b_v_truth_l_tlv);
   fChain->SetBranchAddress("v_truth_l_pdgId", &v_truth_l_pdgId, &b_v_truth_l_pdgId);
   fChain->SetBranchAddress("v_truth_l_fromTau", &v_truth_l_fromTau, &b_v_truth_l_fromTau);
   fChain->SetBranchAddress("v_truth_j_tlv", &v_truth_j_tlv, &b_v_truth_j_tlv);
   fChain->SetBranchAddress("tauEvent", &tauEvent, &b_tauEvent);
   Notify();
}

Bool_t ana_base::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void ana_base::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t ana_base::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef ana_base_cxx
