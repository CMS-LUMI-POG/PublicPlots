#!/bin/sh

# Overall run script for 2018. Now that we have normtags available, this is basically identical to the 2017
# script except for the addition of the pileup script.

# Update the normtag repository. Since the cvmfs version only updates once a week, we instead keep our own
# copy of the git repository which we can pull now! Note: this now has to be done before setting up the
# environment since the git version in CMSSW_7_4_0 is now no longer compatible.
cd ~/Normtags
git pull

# Set up the environment. First we need to set up brilconda and then CMSSW.
# I want to get rid of the CMSSW dependence but it doesn't quite work yet.

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH
cd /afs/cern.ch/user/l/lumipro/CMSSW_7_4_16/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

# Make the plots!
cd ~/PublicPlots

# 1a) create the plots for this year, online luminosity, and copy them to plot area
python create_public_lumi_plots.py public_brilcalc_plots_pp_2018_online.cfg
cp *2018*OnlineLumi*png *2018*OnlineLumi*pdf /afs/cern.ch/cms/lumi/www/publicplots/

# 1b) same, with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_pp_2018_normtag.cfg
cp *2018*NormtagLumi*png *2018*NormtagLumi*pdf /afs/cern.ch/cms/lumi/www/publicplots/

# 2) Copy the cache into the cache for the all years plots. Note: uses normtag now!
cp public_lumi_plots_cache/pp_2018_normtag/* public_lumi_plots_cache/pp_all/

# 3) Copy cache to public location
cp -R public_lumi_plots_cache/pp_2018_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R public_lumi_plots_cache/pp_2018_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/

# 4) Run the all years plotting script
python create_public_lumi_plots_allYears.py public_lumi_plots_pp_allyears.cfg
cp peak_lumi_pp.* peak_lumi_pp_* int_lumi_cumulative_pp_2* int_lumi_cumulative_pp_1* /afs/cern.ch/cms/lumi/www/publicplots/

# 5) Run the pileup plots script
python create_public_pileup_plots.py public_pileup_plots_pp_2018.cfg
cp pileup_pp_2018* /afs/cern.ch/cms/lumi/www/publicplots/