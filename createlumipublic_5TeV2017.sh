#!/bin/sh

# Overall run script for the 2017 5TeV run. This is much simpler than the
# main 2017 script since we only need to do online luminosity, not normtag
# or year-by-year plots.

# Update the normtag repository. Since the cvmfs version only updates once a week,
# we instead keep our own copy of the git repository which we can pull now!
cd ~/public/Normtags
git pull 2>&1

# Set up the environment. First we need to set up brilconda and then CMSSW.
# I want to get rid of the CMSSW dependence but it doesn't quite work yet.

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH

# Make the plots!
mkdir -p  /eos/user/l/lumipro/www/publicplots/2017
cd ~/PublicPlots

# 1) create the plots for this year, online luminosity, and copy them to plot area

python create_public_lumi_plots.py public_brilcalc_plots_pp5TeV_2017_normtag.cfg
cp plots/2017/normtag/*2017*5TeV_Normtag*png plots/2017/normtag/*2017*5TeV_Normtag*pdf /eos/user/l/lumipro/www/publicplots/

# 2) Copy cache to public location
cp -R -u public_lumi_plots_cache/pp5TeV_2017_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
