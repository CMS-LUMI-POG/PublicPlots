#!/bin/sh

# Update the normtag repository. Since the cvmfs version only updates once a week,
# we instead keep our own copy of the git repository which we can pull now!
#cd ~/Normtags
#git pull

# Set up the environment. First we need to set up brilconda and then CMSSW.
# I want to get rid of the CMSSW dependence but it doesn't quite work yet.

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
cd /afs/cern.ch/user/l/lumipro/CMSSW_7_4_16/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

# Make the plots!
cd ~/PublicPlots/

python create_public_pileup_plots_allYears.py public_pileup_plots_pp_allyears.cfg

cp pileup_allYears* /afs/cern.ch/cms/lumi/www/publicplots/