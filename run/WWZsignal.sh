#!/bin/bash

minitrees="\
mc16_13TeV.364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6.deriv.DAOD_STDM3.e5887_s3126_r9364_p4252.root \
mc16_13TeV.364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6.deriv.DAOD_STDM3.e5887_s3126_r10201_p4252.root \
mc16_13TeV.364243.Sherpa_222_NNPDF30NNLO_WWZ_4l2v_EW6.deriv.DAOD_STDM3.e5887_s3126_r10724_p4252.root \
"
rongkun_path="/eos/user/r/rowang/public/WVZ_minitrees/v1.3"

for minitree in $minitrees
do
  echo
  echo ${rongkun_path}/$minitree >> temporal.txt # make dummy txt with path of one ntuple
  ./run temporal.txt $minitree                   # run over the ntuple and throw output with name "$minitree".root
  rm -rf temporal.txt                            # remove dummy txt
  echo 
done

echo "Done!"
