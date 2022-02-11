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
#cd /afs/cern.ch/user/l/lumipro/CMSSW_7_4_16/src/
#source /cvmfs/cms.cern.ch/cmsset_default.sh
#eval `scramv1 runtime -sh`

# Make the plots!
#cd ~/PublicPlots
cd ~/scratch0/testdir/ChristophLearn/PublicPlots

# 1a) create the plots for this year, online luminosity, and copy them to plot area
python create_public_lumi_plots.py public_brilcalc_plots_pp_2018_online.cfg
#cp *2018*OnlineLumi*png *2018*OnlineLumi*pdf /eos/user/l/lumipro/www/publicplots/

# 1b) same, with normtag luminosity
python create_public_lumi_plots.py public_brilcalc_plots_pp_2018_normtag.cfg
#cp *2018*NormtagLumi*png *2018*NormtagLumi*pdf /eos/user/l/lumipro/www/publicplots/

# 2) Copy the cache into the cache for the all years plots. Note: uses normtag now!
cp public_lumi_plots_cache/pp_2018_normtag/* public_lumi_plots_cache/pp_all/

# # 3) Copy cache to public location
# cp -R -u public_lumi_plots_cache/pp_2018_online /afs/cern.ch/user/l/lumipro/public/lumiCache/
# cp -R -u public_lumi_plots_cache/pp_2018_normtag /afs/cern.ch/user/l/lumipro/public/lumiCache/
# cp -R -u public_lumi_plots_cache/pp_all /afs/cern.ch/user/l/lumipro/public/lumiCache/
# 
# # 4) create the plots for all years and Run 2 only. Do the Run 2 first because that way we get the lumiByDay.csv file correct.
# python create_public_lumi_plots.py public_lumi_plots_pp_run2.cfg
# python create_public_lumi_plots.py public_lumi_plots_pp_allyears.cfg
#    cp peak_lumi_pp* int_lumi_cumulative_pp* int_lumi_allcumulative_pp* lumiByDay.csv /eos/user/l/lumipro/www/publicplots/
 
