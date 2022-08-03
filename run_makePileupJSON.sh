#!/bin/bash
   
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
cd ~/CMSSW/CMSSW_12_4_3/src
cmsenv

cd ~/Pileup

echo "running makePileupJSON.py $1 $2"
makePileupJSON.py $1 $2

mv $2 ~/public/pileupJSON/$3
