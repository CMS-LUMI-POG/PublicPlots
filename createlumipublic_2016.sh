#!/bin/sh

# Update the normtag repository. Since the cvmfs version only updates once a week,
# we instead keep our own copy of the git repository which we can pull now!
cd ~/public/Normtags
git pull

# Set up the environment. First we need to set up brilconda.
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH

# Make the plots!
cd ~/PublicPlots

# 1a) create the plots for this year, online luminosity, and copy them to plot area
python create_public_lumi_plots.py public_brilcalc_plots_pp_2016_online.cfg
cp plots/2016/online/*2016*OnlineLumi*png plots/2016/online/*2016*OnlineLumi*pdf /eos/user/l/lumipro/www/publicplots/

# 1b) same, with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_pp_2016_normtag.cfg
cp plots/2016/normtag/*2016*NormtagLumi*png plots/2016/normtag/*2016*NormtagLumi*pdf /eos/user/l/lumipro/www/publicplots/

# 2) Copy the cache into the cache for the all years plots. Note: uses normtag now!
cp public_lumi_plots_cache/pp_2016_normtag/* public_lumi_plots_cache/pp_all/

# 3) Copy cache to public location
cp -R -u public_lumi_plots_cache/pp_2016_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_2016_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_all /afs/cern.ch/user/l/lumipro/public/lumiCache/

#  ===> done in the 2016 script
#
# 4) create the plots for all years 
#python create_public_lumi_plots.py public_lumi_plots_pp_allyears.cfg
#cp plots/allYears/peak_lumi_pp.* plots/allYears/peak_lumi_pp_* plots/allYears/int_lumi_cumulative_pp_2* plots/allYears/int_lumi_cumulative_pp_1* /eos/user/l/lumipro/www/publicplots/
