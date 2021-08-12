#include<iostream>
#include<fstream>
#include<memory>
#include<vector>
#include<TH1.h>
#include"TChain.h"
#include"TFile.h"
#include"ana.h"
using namespace std;

int main(int argc, char** argv)
{
   TString input_file_list="file.list";
   TString input_file_name;
   TString input_tree_name="tree_NOMINAL";
   TString input_hist_name="sumWeight";
   TString output_dir_name="../output";
   TString output_file_name="test";
   if(argc==2) 
   {
      output_file_name= argv[1];
   }
   if(argc==3)
   {
      input_file_list= argv[1];
      output_file_name= argv[2];
   }
   if(argc==4)
   {
      input_file_list= argv[1];
      output_dir_name= argv[2];
      output_file_name= argv[3];
   }
   std::cout<<"output file name is: "<<output_file_name+".root"<<'\n';
   // sumofwgt, lumi, xs_eff inputdata
   vector<float>       iv_sumofwgt;
   // read file.list   
   auto ch = std::make_unique<TChain>(input_tree_name);
   ifstream ifs;
   ifs.open(input_file_list.Data());
   std::string line;
   while(std::getline(ifs, line))
   { 
     input_file_name = line; 
     if(input_file_name.BeginsWith("#")) continue; //file name begins with # will pass.      

     cout<<"input file: "<<input_file_name<<'\n';
     std::unique_ptr<TFile> file( TFile::Open(input_file_name) );
     // TFile* file= TFile::Open(input_file_name);
     TTree* tree= (TTree*) file->Get(input_tree_name);
     TH1D*  hist= (TH1D *) file->Get(input_hist_name);

     if(!tree || !hist) 
       cout<<"can't open: "<<input_file_name<<'\n';
     else
     {
       // add sum of weight
       // iv_sumofwgt.insert(iv_sumofwgt.end(),hist->GetBinContent(2));
       iv_sumofwgt.push_back(hist->GetBinContent(2));
       // ch->Add(input_file_name);
     }


     //delete tree; // do not delete tree from TFile!
     //delete file;
     auto myanalysis = std::make_unique<ana>(tree, output_dir_name + "/",output_file_name,iv_sumofwgt);
     myanalysis->Loop();
     file->Close();
     break;
   }


   //delete ch;
   //delete myanalysis;
}
