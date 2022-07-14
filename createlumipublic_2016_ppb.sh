#!/bin/sh

# Update the normtag repository. Since the cvmfs version only updates once a week,
# we instead keep our own copy of the git repository which we can pull now!
cd ~/public/Normtags
git pull 2>&1

# Set up the environment. First we need to set up brilconda.
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH

# Make the plots!
mkdir -p  /eos/user/l/lumipro/www/publicplots/2016
cd ~/PublicPlots

# 1a) 5TeV with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_ppb5TeV_2016_online.cfg

# 1b) 8TeV with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_ppb8TeV_2016_normtag.cfg


# 2) Copy the cache into the cache for the all years plots. Note: uses normtag now!
cp public_lumi_plots_cache/ppb5TeV_2016_online/* public_lumi_plots_cache/pp_all/
cp public_lumi_plots_cache/ppb8TeV_2016_normtag/* public_lumi_plots_cache/pp_all/

# 3) Copy cache to public location
#    the plots:
cp plots/2016/normtag/*2016*Normtag*png plots/2016/normtag/*2016*Normtag*pdf /eos/user/l/lumipro/www/publicplots/
cp plots/2016/online/*2016*Online*png plots/2016/online/*2016*Online*pdf /eos/user/l/lumipro/www/publicplots/


cp -R -u public_lumi_plots_cache/ppb5TeV_2016_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/ppb8TeV_2016_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_all /afs/cern.ch/user/l/lumipro/public/lumiCache/

