 #!/bin/sh

# Overall run script for 2022. Now that we have normtags available, this is basically identical to the 2017
# script.

echo Starting script at `date`

# Update the normtag repository. Since the cvmfs version only updates once a week, we instead keep our own
# copy of the git repository which we can pull now! Note: this now has to be done before setting up the
# environment since the git version in CMSSW_7_4_0 is now no longer compatible.
cd ~/public/Normtags
git pull 2>&1

# Set up the environment. First we need to set up brilconda.
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH

# Make the plots!
cd ~/PublicPlots

# 1a) create the plots for this year, online luminosity, and copy them to plot area
# We directly produce Normtag plots, no online plots anymore. The certification is fast enough
#python create_public_lumi_plots.py public_brilcalc_plots_pp_2022_online.cfg
#mkdir -p /eos/user/l/lumipro/www/publicplots/2022
#cp plots/2022/online/*2022*Online*png plots/2022/online/*2022*Online*pdf /eos/user/l/lumipro/www/publicplots/2022
#
# 1b) same, with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_pp_2022_normtag.cfg
cp plots/2022/normtag/*2022*Normtag*png plots/2022/normtag/*2022*Normtag*pdf /eos/user/l/lumipro/www/publicplots/2022
#
# 2) Copy the cache into the cache for the all years plots. Note: uses normtag now!
cp public_lumi_plots_cache/pp_2022_normtag/* public_lumi_plots_cache/pp_all/
#
# 3) Copy cache to public location
#cp -R -u public_lumi_plots_cache/pp_2022_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_2022_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/
cp -R -u public_lumi_plots_cache/pp_all /afs/cern.ch/user/l/lumipro/public/lumiCache/
#
# # 4) create the plots for all years and Run 3 only. Do the Run 3 first because that way we get the lumiByDay.csv file correct.
mkdir -p /eos/user/l/lumipro/www/publicplots/multiYear
#python create_public_lumi_plots.py public_lumi_plots_pp_run3.cfg
python create_public_lumi_plots.py public_lumi_plots_pp_run2and3.cfg
python create_public_lumi_plots.py public_lumi_plots_pp_allyears.cfg
cp plots/allYears/peak_lumi_pp* plots/allYears/int_lumi_cumulative_pp* plots/allYears/int_lumi_allcumulative_pp* plots/allYears/lumiByDay.csv /eos/user/l/lumipro/www/publicplots/multiYear/
#
