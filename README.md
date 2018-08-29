# PublicPlots

This repository contains the tools for creating the public luminosity plots. This is initially imported from the Run 1 repository in https://github.com/cms-sw/RecoLuminosity-LumiDB/plotdata and is currently in the process of being cleaned up and documented.

The basic procedure is:
```python create_public_lumi_plots.py [cfg file]```
where the config file is hopefully self-explanatory (but see below for further documentation).

However, be aware that many of the config files are out of date. The following config files should work and reproduce the plots currently on the page:

* 2018 pp 13 TeV (online & normtag)
* 2017 pp 13 TeV (online & normtag)
* 2017 pp 5 TeV (online & normtag)
* 2016 pPb 5 TeV (online)
* 2016 pPb 8 TeV (online & normtag)
* 2015 pp 5 TeV (normtag)

The rest are in progress.

There are also various run scripts which perform the task of setting up the environment, running the actual script, copying the plots to the final plot location, etc. Check out createlumipublic_2017.sh for an example.

## Todo list
* Figure out disrepancies in 2016 pp run
* Update 2015 pp 13 TeV and 2015 PbPb runs
* Restore beamenergy and accelerator mode filters in brilcalc invocation
* Clean up other year-dependent hacks
* Remove dependence on CMSSW

## Config file

Here are the various variables you can set in the config file. All of these are in the "general" category:
* `file_suffix`: A suffix to be added to the name of all of the plots. This is useful to distinguish online/normtag lumi, or for special runs, or so forth.
* `plot_label`: The label to be added to the plots. Per agreement with Run Coordination, this should be "CMS Preliminary Online Luminosity" for online luminosity, "CMS Preliminary Offline Luminosity" for preliminary (not physics approved) offline luminosity, and "CMS Preliminary" for approved physics results.
* `normtag_file`: The name of the normtag file to use. If this argument is not included, no normtag file (i.e. online luminosity) will be used.
* `json_file`: A JSON file to define ranges of data that are certified as good for physics. This option is no longer used for the regular public plots any more, so use at your own risk.
* `beam_energy`: The beam energy (in GeV). This will be used both for display on the plots and for filtering the brilcalc results.
* `accel_mode`: The accelerator mode (PROTPHYS, IONPHYS, or PAPHYS). Like the beam energy this will both be used for display and for filtering the brilcalc output.
* `units`: If you want to override the default units with units more appropriate to a special run, they can be specified here. There are four different units, for the cumulative by day, cumulative by week, yearly, and maximum instantaneous luminosity. They should be specified as a dictionary, as for example `units = {"cum_day": "pb^{-1}", "cum_week": "pb^{-1}", "cum_year" : "pb^{-1}", "max_inst" : "Hz/nb"}`. You can also specify just some entries if you only want to override some units.
* `display_units`: This is a bit of a workaround necessary for the fact that the units are changed for PbPb running, so the units that need to be displayed are no longer the same as the units that brilcalc uses internally. See `public_brilcalc_plots_pbpb_2015.cfg` for an example of how this works.
* `date_begin`: First date to consider in this run.
* `date_end`: Last date to consider in this run (set this at the end of the year for runs which are still in progress).
* `cache_dir`: The cache directory where the brilcalc results will be stored (see below).
* `lumicalc_script`: The actual script to invoke for getting the luminosity information. This is mostly a legacy option from when we were still in the transition from other tools to brilcalc; now that brilcalc is established, this should always be `brilcalc lumi` (other tools are no longer supported).
* `lumicalc_flags`: Flags to pass to the script defined by `lumicalc_script`. Normally this should be `-b "STABLE BEAMS" --byls` and should not need to be changed (normally changes to the brilcalc invocation are handled by `normtag_file`, `beam_energy`, and `accel_mode`).
* `color_schemes`: Color schemes for the plots, as defined in `public_plots_tools.py`.
* `verbose`: Adds some extra messages for debugging.

## A note about the cache

Since running the script on a full year's data is a quite lengthy procedure, the script normally keeps the brilcalc output data in a cache directory (specified by the `cache_dir` argument above). By default, when the script is run, it will always regenerate the last 3 days of the cache if no normtag file is being used, or the last 7 days if a normtag file is being used, to make sure that it will always pick up the most recent data (the longer period if a normtag is being used is to account for the occasional case where the fill validation is not run promptly and so fills do not appear in the normtag for several days). However, if the data for older fills changes for whatever reason, the script will not automatically pick up these changes. In order to rebuild the cache, you have a few options:

* If you know which dates need to be updated, simply remove the output files for those dates from the cache directory and re-run; they will automatically be regenerated with the updated data.
* If you want to rebuild the whole cache, you can run the script with the option --ignore-cache, which will rebuild the cached data.
* You can also simply delete (or move) the cache directory, which accomplishes the same as above.

It is recommended to periodically rebuild the cache a few times throughout the year just to catch any unexpected changes that may have happened in the year's data.
