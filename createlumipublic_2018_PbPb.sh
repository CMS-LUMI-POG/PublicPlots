#!/bin/sh

# Run script for 2018 PbPb period. This is much simpler than the pp run script since we don't have a
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
mkdir -p  /eos/user/l/lumipro/www/publicplots/2018
cd ~/PublicPlots


#  # with normtag
#  python create_public_lumi_plots.py public_brilcalc_plots_PbPb_2018_normtag.cfg
#  cp plots/2018/normtag/*pbpb_2018*Normtag*png plots/2018/normtag/*pbpb_2018*Normtag*pdf /eos/user/l/lumipro/www/publicplots/2018/
#  cp -R -u public_lumi_plots_cache/PbPb_2018_normtag/* public_lumi_plots_cache/pbpb_all/
#  cp -R -u public_lumi_plots_cache/PbPb_2018_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/


# Now the plots for all Run 2 years
# It is important that the public_lumi_plots_cache/pbpb_all/ has been filled
# beforehand (by generating the 2015 and 2018 PbPb plots)
python create_public_lumi_plots.py public_lumi_plots_pbpb_run2.cfg

# plots with proton equivalent luminosity
python create_public_lumi_plots.py public_lumi_plots_ions_run2.cfg

cp plots/allYears/*pbpb*run2.png plots/allYears/*pbpb*run2.pdf /eos/user/l/lumipro/www/publicplots/multiYear/
