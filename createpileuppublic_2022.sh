#!/bin/sh

echo Starting script at `date`

# Update the normtag repository. Since the cvmfs version only updates once a week,
# we instead keep our own copy of the git repository which we can pull now!

cd ~/public/Normtags
git pull 2>&1

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/bin:$PATH
export LD_LIBRARY_PATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/root/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/root/lib:$PYTHONPATH


# The above is sufficient if we have the output of pileupCalc cached. But if we have to run
# pileupCalc.py we need to configure CMSSW since pileupCalc IS a CMSSW tool.
# We run pileupCalc in a subshell since the environment of CMSSW is not compatible with the
# python and matplotlib we are useing to produce the plots later.
# The separation of running pileupCalc and the creation of the plots nicely factors out
# the dependency on CMSSW and makes it easier to move to a new release if necessary. 
CMSSWPATH=~/CMSSW/CMSSW_7_4_16
(
    cd $CMSSWPATH
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    # equivalent to `cmsenv`:
    eval `scramv1 runtime -sh`
    cd ~/PublicPlots
    
    # you can specify --ignore-cache here to force the re-sun of pileupCalc:
    python run_pileupCalc.py public_pileup_plots_pp_2022_80000.cfg 
)


cd ~/PublicPlots


# Create and copy the pileup plots for this year.
# The following commands requires the pileupCalc results to be in the cache.
python create_public_pileup_plots.py public_pileup_plots_pp_2022_80000.cfg 

cp plots/2022/normtag/pileup_pp_2022* /eos/user/l/lumipro/www/publicplots/2022

# Now make sure that the same rootfile is in both cache directories.
cp /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_2022/pileup_calc_80000_tmp.root /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_all/PileupHistogram-Online-136tev-2022.root

# Create and copy the all-year pileup plots.
# python create_public_pileup_plots_allYears.py public_pileup_plots_pp_allyears.cfg
#cp plots/allYears/pileup_allYears* /eos/user/l/lumipro/www/publicplots/
