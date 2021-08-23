#define WWZ_ana_cxx
#include <iostream>
#include "ana.h"
#include <time.h>
bool ana::WWZ_Cut()
{
   //All
   cutflow("WWZ").pass("WWZ",">=4l",wgt*v_Z_wgt[0]);
   //lepton numbers
   int nlepton=v_l_pid.size();
   //define weight
   WWZ_wgt= wgt*v_Z_wgt[0];
   int nW=0;
   //define W lepton ID and modify weight
   for(int i=0;i<nlepton;i++)
   {
      if(nW>=2) break;
      if(v_l_order[i]==v_Z_pair[0].first || v_l_order[i]==v_Z_pair[0].second) continue;
      WWZ_wgt*= v_l_wgt[v_l_order[i]];
      W_id[nW]=v_l_order[i];
      nW++;
   }
   WWZ_chi2();
   //dilepton
   for(int i=0;i<v_l_tlv.size();i++)
      for(int j=i+1;j<v_l_tlv.size();j++)
      {
         if(v_l_pid[i]+v_l_pid[j]!=0) continue;
         WWZ_dilepton_mass = (v_l_tlv[i]+v_l_tlv[j]).M()/1000;
         if(WWZ_dilepton_mass<12) return false;
      }
   cutflow("WWZ").pass("WWZ","Dilepton",WWZ_wgt);
   //lepton pt cut
   if (v_l_tlv[v_l_order[0]].Pt() < 30e3) return false;
   if (v_l_tlv[v_l_order[1]].Pt() < 15e3) return false;
   if (v_l_tlv[v_l_order[2]].Pt() < 8e3) return false;
   if (v_l_tlv[v_l_order[3]].Pt() < 6e3) return false;
   cutflow("WWZ").pass("WWZ","LeptonPt",WWZ_wgt);
   // selected lepton min dR 
   dR = 999;
   for (int i=0;i<4;i++){
      for (int j=i+1;j<4;j++){
         float temp = v_l_tlv[v_l_order[i]].DeltaR(v_l_tlv[v_l_order[j]]);
         if(temp < dR){
            dR = temp;
         }
      }
   }
   if(dR < 0.1) return false;
   cutflow("WWZ").pass("WWZ","dR>0.1",WWZ_wgt);
   // bveto
   Bjet_Cut("WWZ","WWZ",WWZ_wgt);

   // choose 77 as our work point
   WWZ_wgt*=b_wgt[2];
   if(cutflow("WWZ").isPass("WWZ","B_veto77"))
   {
      if(passTrig) cutflow("WWZ").pass("WWZ","passTrig",WWZ_wgt);
      else return false;
   }
   else
   {  
      return false;
   }
   //lepton number infomation
   if(nlepton>6) cutflow("WWZ").pass("WWZ","WWZ_>6l",WWZ_wgt);
   if(nlepton==6) cutflow("WWZ").pass("WWZ","WWZ_6l",WWZ_wgt);
   if(nlepton==5) cutflow("WWZ").pass("WWZ","WWZ_5l",WWZ_wgt);
   if(nlepton==4) cutflow("WWZ").pass("WWZ","WWZ_4l",WWZ_wgt);
   
   // total charge requirement
   int chargesum=0;
   for (int i=0;i<4;i++) {
       if (v_l_pid[i]>0) {
           chargesum++;
       } else {
           chargesum--;
       }
   }
   if (chargesum!= 0) return false;
   cutflow("WWZ").pass("WWZ","chargesum=0",WWZ_wgt);
   /**
   // divide WWZ channel
   if(cutflow("WWZ").isPass("WWZ","B_veto77"))
   {
      // SF_noZ and SF_inZ
      if( abs(v_l_pid[W_id[0]])==abs(v_l_pid[W_id[1]]))
      {

         if(abs((v_l_tlv[W_id[0]]+v_l_tlv[W_id[1]]).M()-Z_mass)<20e3)
         {
            n_channel=0;
            cutflow("WWZ").pass("WWZ","WWZ_SF_inZ",WWZ_wgt);
         }
         else
         {
            n_channel=1;
            cutflow("WWZ").pass("WWZ","WWZ_SF_noZ",WWZ_wgt);
         }
      }
      //em

      else
      {
         n_channel=2;
         cutflow("WWZ").pass("WWZ","WWZ_em",WWZ_wgt);
      }
   }
   **/

   WWZ_Z_mass = (v_l_tlv[v_Z_pair[0].first]+v_l_tlv[v_Z_pair[0].second]).M();
   _WWZ_tree->Fill();
   return true;
}


void ana::WWZ_operation()
{
   if(cutflow("WWZ").isPass("WWZ","B_veto77"))
   {
      channel_fillhist("WWZ",1,WWZ_wgt);
      WWZ_fillhist("WWZ",WWZ_wgt);
      /**
      if(cutflow("WWZ").isPass("WWZ","WWZ_SF_noZ")){
         channel_fillhist("WWZ_SF_noZ",1,WWZ_wgt);
         WWZ_fillhist("WWZ_SF_noZ",WWZ_wgt);
      }
      if(cutflow("WWZ").isPass("WWZ","WWZ_SF_inZ")){  
         channel_fillhist("WWZ_SF_inZ",1,WWZ_wgt);
         WWZ_fillhist("WWZ_SF_inZ",WWZ_wgt);
      }
      if(cutflow("WWZ").isPass("WWZ","WWZ_em")){
         channel_fillhist("WWZ_em",1,WWZ_wgt);
         WWZ_fillhist("WWZ_em",WWZ_wgt);
      }
      **/
   }
}
