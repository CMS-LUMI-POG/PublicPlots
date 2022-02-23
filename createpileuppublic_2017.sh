#!/bin/sh

echo Starting script at `date`

# Update the normtag repository. Since the cvmfs version only updates once a week,
# we instead keep our own copy of the git repository which we can pull now!

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
    
    # you can specify --ignore-cache here to force the re-sun of pileupCalc:
    python run_pileupCalc.py public_pileup_plots_pp_2017_80000.cfg 
    python run_pileupCalc.py public_pileup_plots_pp_2017_69200.cfg
    python run_pileupCalc.py public_pileup_plots_pplowpu_2017_H_69200.cfg
    python run_pileupCalc.py public_pileup_plots_pplowpu_2017_H_80000.cfg
    python run_pileupCalc.py public_pileup_plots_pplowpu_2017_G_65000.cfg
)


cd ~/PublicPlots


# Create and copy the pileup plots for this year.
# The following commands requires the pileupCalc results to be in the cache.
python create_public_pileup_plots.py public_pileup_plots_pp_2017_80000.cfg 
python create_public_pileup_plots.py public_pileup_plots_pp_2017_69200.cfg 
python create_public_pileup_plots.py public_pileup_plots_pplowpu_2017_H_69200.cfg
python create_public_pileup_plots.py public_pileup_plots_pplowpu_2017_H_80000.cfg
python create_public_pileup_plots.py public_pileup_plots_pplowpu_2017_G_65000.cfg 

cp plots/2017/normtag/pileup_pp_2017* /eos/user/l/lumipro/www/publicplots/
cp plots/2017/normtag_lowPU/pileup_pp* /eos/user/l/lumipro/www/publicplots/

# Now make sure that the same rootfile is in both cache directories.
cp /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_2017/pileup_calc_80000_tmp.root /afs/cern.ch/user/l/lumipro/PublicPlots/public_lumi_plots_cache/pileup_all/PileupHistogram-goldenJSON-13tev-2017.root

# The all year pileup plots are created when running the script for 2018
