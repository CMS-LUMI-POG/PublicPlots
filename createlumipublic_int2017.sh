#!/bin/sh
echo "Hi I am running this script"
cd /afs/cern.ch/user/l/lumipro/lumiplotmachinery/internal/CMSSW_7_4_0_pre9/src/RecoLuminosity/LumiDB/plotdata
echo "made cd into the relevant directory"
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH
echo "did the brilcalc link"
##eval `source /afs/cern.ch/cms/sw/cmsset_default.sh`
source /cvmfs/cms.cern.ch/cmsset_default.sh;
echo "sourced the cmssw setup"
eval `scramv1 runtime -sh`
######rm -rf public_lumi_plots_cache/pp_2016/*
echo "and I set up the cms environment"
python create_public_lumi_plots.py public_brilcalc_plots_pp_2017_internal.cfg
#python create_public_lumi_plots_ppb16.py public_lumi_plots_ppb8TeV_2016.cfg
#cp int_lumi_per_day_cumulative*2017*OnlineLumi*png int_lumi_per_day_cumulative*2017*OnlineLumi*pdf /afs/cern.ch/cms/lumi/www/publicplots/
cp *2017*OnlineLumi*png *2017*OnlineLumi*pdf /afs/cern.ch/cms/lumi/www/publicplots/
#cp *_lumi_per_day_*ppb_2016*OnlineLumi8TeVPPb.p* /afs/cern.ch/cms/lumi/www/publicplots/
cp public_lumi_plots_cache/pp_2017/* public_lumi_plots_cache/pp_all/
cp -R /afs/cern.ch/user/l/lumipro/lumiplotmachinery/internal/CMSSW_7_4_0_pre9/src/RecoLuminosity/LumiDB/plotdata/public_lumi_plots_cache/pp_2017 /afs/cern.ch/user/l/lumipro/public/lumiCache/
python create_public_lumi_plots_allYears.py public_lumi_plots_pp_allyears.cfg
cp peak_lumi_pp.* peak_lumi_pp_* int_lumi_cumulative_pp_2* int_lumi_cumulative_pp_1* /afs/cern.ch/cms/lumi/www/publicplots/





