 #!/bin/sh

# Overall run script for 2018. Now that we have normtags available, this is basically identical to the 2017
# script.

echo Starting script at `date`

# Update the normtag repository. Since the cvmfs version only updates once a week, we instead keep our own
# copy of the git repository which we can pull now! Note: this now has to be done before setting up the
# environment since the git version in CMSSW_7_4_0 is now no longer compatible.
cd ~/public/Normtags
git pull

# Set up the environment. First we need to set up brilconda.
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH

# Make the plots!
mkdir -p  /eos/user/l/lumipro/www/publicplots/2018
cd ~/PublicPlots

 1a) create the plots for this year, online luminosity, and copy them to plot area
# No online plots for 2018 anymore
#python create_public_lumi_plots.py public_brilcalc_plots_pp_2018_online.cfg
#cp plots/2018/online/*2018*OnlineLumi*png plots/2018/online/*2018*OnlineLumi*pdf /eos/user/l/lumipro/www/publicplots/2018

# 1b) same, with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_pp_2018_normtag.cfg
cp plots/2018/normtag/*2018*Normtag*png plots/2018/normtag/*2018*Normtag*pdf /eos/user/l/lumipro/www/publicplots/2018

# 2) Copy the cache into the cache for the all years plots. Note: uses normtag now!
cp public_lumi_plots_cache/pp_2018_normtag/* public_lumi_plots_cache/pp_all/

# 3) Copy cache to public location
#cp -R -u public_lumi_plots_cache/pp_2018_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_2018_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_all /afs/cern.ch/user/l/lumipro/public/lumiCache/

# 4) create the plots for all years and Run 2 only. Do the Run 2 first because that way we get the lumiByDay.csv file correct.
mkdir -p /eos/user/l/lumipro/www/publicplots/multiYear
python create_public_lumi_plots.py public_lumi_plots_pp_run2.cfg
python create_public_lumi_plots.py public_lumi_plots_pp_allyears.cfg
cp plots/allYears/peak_lumi_pp* plots/allYears/int_lumi_cumulative_pp* plots/allYears/int_lumi_allcumulative_pp* plots/allYears/lumiByDay.csv /eos/user/l/lumipro/www/publicplots/multiYear/
 
