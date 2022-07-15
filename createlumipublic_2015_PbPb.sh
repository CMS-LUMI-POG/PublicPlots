#!/bin/sh

# Run script for 2015 PbPb period. This is much simpler than the pp run script since we don't have a
# normtag and don't need to do the multiyear plots.

echo Starting script at `date`

# Update the normtag repository. Since the cvmfs version only updates once a week, we instead keep our own
# copy of the git repository which we can pull now! Note: this now has to be done before setting up the
# environment since the git version in CMSSW_7_4_0 is now no longer compatible.
cd ~/public/Normtags
git pull 2>&1

# Set up the environment. First we need to set up brilconda.
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH

# Make the plots!
mkdir -p  /eos/user/l/lumipro/www/publicplots/2015
cd ~/PublicPlots


# with normtag
python create_public_lumi_plots.py public_brilcalc_plots_PbPb_2015_normtag.cfg
cp plots/2015/normtag/*pbpb_2015*Normtag*png plots/2015/normtag/*pbpb_2015*Normtag*pdf /eos/user/l/lumipro/www/publicplots/2015/
cp -R -u public_lumi_plots_cache/PbPb_2015_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/
