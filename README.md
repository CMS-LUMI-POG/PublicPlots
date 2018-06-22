# PublicPlots

This repository contains the tools for creating the public luminosity plots. This is initially imported from the Run 1 repository
in https://github.com/cms-sw/RecoLuminosity-LumiDB/plotdata and is currently in the process of being cleaned up and documented.

The basic procedure is:
python create_public_lumi_plots.py [cfg file]
where the config file is hopefully self-explanatory.

However, be aware that many of the config files are out of date. The following config files should work and
reproduce the plots currently on the page:

* 2018 pp 13 TeV (online)
* 2017 pp 13 TeV (online & normtag)
* 2017 pp 5 TeV (online & normtag)
* 2016 pPb 5 TeV (online)
* 2016 pPb 8 TeV (online & normtag)
* 2015 pp 5 TeV (normtag)

The rest are in progress.

There are also various run scripts which perform the task of setting up the environment, running the actual
script, copying the plots to the final plot location, etc. Check out createlumipublic_2017.sh for an example.

## Todo list
* Figure out disrepancies in 2016 pp run
* Update 2015 pp 13 TeV and 2015 PbPb runs
* Restore beamenergy and accelerator mode filters in brilcalc invocation
* Clean up other year-dependent hacks
* Remove dependence on CMSSW
