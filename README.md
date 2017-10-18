# PublicPlots

This repository contains the tools for creating the public luminosity plots. This is initially imported from the Run 1 repository
in https://github.com/cms-sw/RecoLuminosity-LumiDB/plotdata and is currently in the process of being cleaned up and documented.

The basic procedure is:
python create_public_lumi_plots.py <cfg file>
where the config file is hopefully self-explanatory.

However be aware that most of the config files are out of date. I have updated the config files for:
* 2017 pp normtag
* 2017 pp online
* 2016 pPb 5 TeV (online)
* 2016 pPb 8 TeV (online)
* 2015 pp 5 TeV
and confirmed that they reproduce the results currently on the page. The others are in progress.

## Todo list
* Figure out disrepancies in 2016 pp run
* Update 2015 pp 13 TeV and 2015 PbPb runs
* Restore beamenergy and accelerator mode filters in brilcalc invocation
* Clean up other year-dependent hacks
* Remove dependence on CMSSW
