#!/bin/bash

minitrees="\
mc16_13TeV.364250.Sherpa_222_NNPDF30NNLO_llll.deriv.DAOD_STDM3.e5894_s3126_r10201_p4252.root \
mc16_13TeV.364250.Sherpa_222_NNPDF30NNLO_llll.deriv.DAOD_STDM3.e5894_s3126_r10724_p4252.root \
mc16_13TeV.364250.Sherpa_222_NNPDF30NNLO_llll.deriv.DAOD_STDM3.e5894_s3126_r9364_p4252.root \
mc16_13TeV.364288.Sherpa_222_NNPDF30NNLO_llll_lowMllPtComplement.deriv.DAOD_STDM3.e6096_s3126_r10201_p4097.root \
mc16_13TeV.364288.Sherpa_222_NNPDF30NNLO_llll_lowMllPtComplement.deriv.DAOD_STDM3.e6096_s3126_r10724_p4097.root \
mc16_13TeV.364288.Sherpa_222_NNPDF30NNLO_llll_lowMllPtComplement.deriv.DAOD_STDM3.e6096_s3126_r9364_p4097.root \
mc16_13TeV.345705.Sherpa_222_NNPDF30NNLO_ggllll_0M4l130.deriv.DAOD_STDM3.e6213_s3126_r10201_p4252.root \
mc16_13TeV.345705.Sherpa_222_NNPDF30NNLO_ggllll_0M4l130.deriv.DAOD_STDM3.e6213_s3126_r10724_p4252.root \
mc16_13TeV.345705.Sherpa_222_NNPDF30NNLO_ggllll_0M4l130.deriv.DAOD_STDM3.e6213_s3126_r9364_p4252.root \
mc16_13TeV.345706.Sherpa_222_NNPDF30NNLO_ggllll_130M4l.deriv.DAOD_STDM3.e6213_s3126_r10201_p4252.root \
mc16_13TeV.345706.Sherpa_222_NNPDF30NNLO_ggllll_130M4l.deriv.DAOD_STDM3.e6213_s3126_r10724_p4252.root \
mc16_13TeV.345706.Sherpa_222_NNPDF30NNLO_ggllll_130M4l.deriv.DAOD_STDM3.e6213_s3126_r9364_p4252.root \
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
