#!/bin/sh

echo Starting script at `date`

# Update the normtag repo and set up the environment as in the regular public plots script.
cd ~/public/Normtags
git pull

export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/bin:$PATH
export LD_LIBRARY_PATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/root/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/root/lib:$PYTHONPATH


# The above is sufficient if we have the output of pileupCalc cached. But if we have to run
# pileupCalc.py we need to configure CMSSW since pileupCalc IS a CMSSW tool.
# We run pileupCalc in a subshell since the environment of CMSSW is not compatible with the
# python and matplotlib we are useing to produce the plots later.
# The separation of running pileupCalc and the creation of the plots nicely factors out
# the dependency on CMSSW and makes it easier to move to a new release if necessary. 
(
    cd /afs/cern.ch/user/l/lumipro/CMSSW_7_4_16/src/
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    eval `scramv1 runtime -sh`
    cd ~/PublicPlots
    #cd ~/scratch0/testdir/ChristophLearn/PublicPlots
    
    # you can specify --ignore-cache here to force the re-sun of pileupCalc:
    python run_pileupCalc.py public_pileup_plots_pp_2018_80000.cfg 
    python run_pileupCalc.py public_pileup_plots_pp_2018_69200.cfg 
)

cd ~/PublicPlots
#cd ~/scratch0/testdir/ChristophLearn/PublicPlots
    

# Create and copy the pileup plots for this year.
# The following commands requires the pileupCalc results to be in the cache.
python create_public_pileup_plots.py public_pileup_plots_pp_2018_80000.cfg 
python create_public_pileup_plots.py public_pileup_plots_pp_2018_69200.cfg 

#cp plots/2018/normtag/pileup_pp_2018* /eos/user/l/lumipro/www/publicplots/

# Now make sure that the same rootfile is in both cache directories.
cp /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_2018/pileup_calc_80000_tmp.root /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_all/PileupHistogram-goldenJSON-13tev-2018.root

# Create and copy the all-year pileup plots.
python create_public_pileup_plots_allYears.py public_pileup_plots_pp_allyears.cfg
#cp pileup_allYears* /eos/user/l/lumipro/www/publicplots/
