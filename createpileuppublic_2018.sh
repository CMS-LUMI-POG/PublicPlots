#!/bin/sh

echo Starting script at `date`

# Update the normtag repo and set up the environment as in the regular public plots script.
cd ~/public/Normtags
git pull

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
cd /afs/cern.ch/user/l/lumipro/CMSSW_7_4_16/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

cd ~/PublicPlots

# Create and copy the pileup plots for this year.
python create_public_pileup_plots.py public_pileup_plots_pp_2018.cfg --ignore-cache
cp pileup_pp_2018* /afs/cern.ch/cms/lumi/www/publicplots/

# Now make sure that the same rootfile is in both cache directories.
cp /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_2018/pileup_calc_tmp.root /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_all/PileupHistogram-goldenJSON-13tev-2018.root

# Create and copy the all-year pileup plots.
python create_public_pileup_plots_allYears.py public_pileup_plots_pp_allyears.cfg
cp pileup_allYears* /afs/cern.ch/cms/lumi/www/publicplots/
