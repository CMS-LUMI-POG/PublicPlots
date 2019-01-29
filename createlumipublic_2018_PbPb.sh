#!/bin/sh

# Run script for 2018 PbPb period. This is much simpler than the pp run script since we don't have a
# normtag and don't need to do the multiyear plots.

echo Starting script at `date`

# Update the normtag repository. Since the cvmfs version only updates once a week, we instead keep our own
# copy of the git repository which we can pull now! Note: this now has to be done before setting up the
# environment since the git version in CMSSW_7_4_0 is now no longer compatible.
cd ~/public/Normtags
git pull

# Set up the environment. First we need to set up brilconda and then CMSSW.
# I want to get rid of the CMSSW dependence but it doesn't quite work yet.

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
cd /afs/cern.ch/user/l/lumipro/CMSSW_7_4_16/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

# Make the plots!
cd ~/PublicPlots

python create_public_lumi_plots.py public_brilcalc_plots_PbPb_2018_online.cfg
cp *pbpb_2018*OnlineLumi*png *pbpb_2018*OnlineLumi*pdf /eos/user/l/lumipro/www/publicplots/
cp -R -u public_lumi_plots_cache/PbPb_2018_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
