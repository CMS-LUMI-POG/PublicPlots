# PublicPlots

This repository contains the tools for creating the public luminosity plots. This is initially imported from the Run 1 repository in https://github.com/cms-sw/RecoLuminosity-LumiDB/plotdata and is currently in the process of being cleaned up and documented.

The basic procedure is:
```
python create_public_lumi_plots.py [cfg file]
```
where the config file is hopefully self-explanatory (but see below for further documentation).

Be aware there are many special config files which might be out of date. 
However all runs and data taking periods of run 2 and the ongoing run 3 period are up to date and reproduce the plots on the page. The results should be consistent with the Twiki results page and the values in that page:

* 2018 pp 13 TeV (online & normtag)
* 2018 PbPb 5TeV (normtag)
* 2017 pp 13 TeV (online & normtag)
* 2017 pp 5 TeV (online & normtag)
* 2016 pPb 5 TeV (online)
* 2016 pPb 8 TeV (online & normtag)
* 2015 pp 5 TeV (normtag)
* 2015 PbPb 5TeV (normtag)
* 2015 pp 13TeV (normtag)

There are also various run scripts which perform the task of setting up the environment, running the actual script, copying the plots to the final plot location, etc. Check out createlumipublic_2017.sh for an example.

A new addition is `public_animated_lumi_plot_run2.py`, which will create an animated plot from the `lumiByDay.csv` file created when the multi-year plots are created. See the script for some documentation; it is designed to be run to create the individual frames and then `make_animations.sh` will create the final animation (requires installation of `ffmpeg`).

**IMPORTANT NOTE**: In order to produce the all-years cumulative plots with broken axes, the `brokenaxes` package needs to be installed. You can install it with `pip install --user brokenaxes`. If not installed, the script will still work; it will just skip making those plots.

## Todo list
* Restore beamenergy and accelerator mode filters in brilcalc invocation
* Clean up other year-dependent hacks if possible
## Config file

Here are the various variables you can set in the config file. All of these are in the "general" category.

* `plot_multiple_years`: If False (or omitted), this will just make the plots for a single year, calling brilcalc as necessary. If True, this will make the plots for multiple years, but brilcalc will not be invoked -- only existing data in the cache will be used. In principle the script could be updated to make the single year and multiple year plots in one pass, but this is a little tricky because of the different configuration necessary for different years, so for now you'll just have to run it twice with the appropriate configuration. Some of the options below apply only in one case or the other, so I've separated them below.

**Options for both single-year and multiple-year plots**

* `file_suffix`: A suffix to be added to the name of all of the plots. This is useful to distinguish online/normtag lumi, or for special runs, or so forth.
* `plot_label`: The label to be added to the plots. Per agreement with Run Coordination, this should be "CMS Preliminary Online Luminosity" for online luminosity, "CMS Preliminary Offline Luminosity" for preliminary (not physics approved) offline luminosity, and "CMS Preliminary" for approved physics results.
* `json_file`: A JSON file to define ranges of data that are certified as good for physics.
* `accel_mode`: The accelerator mode (PROTPHYS, IONPHYS, or PAPHYS). This is used for display (and naming) of the plots. For single-year plots it can also be used to filter the brilcalc output (see below). For multi-year plots you can also specify the special mode ALLIONS which combines PbPb and pPb running. In this case you will also need to specify the actual accelerator mode for each year in `accel_mode_by_year`. See `public_lumi_plots_ions_run2.cfg` for an example of how this works.
* `date_begin`: First date to consider in this run.
* `date_end`: Last date to consider in this run (set this at the end of the year for runs which are still in progress).
* `cache_dir`: The cache directory where the brilcalc results will be stored (if brilcalc is invoked) and read from. See below for more details.
* `units`: If you want to override the default units with units more appropriate to a special run, they can be specified here. There are four different units, for the cumulative by day, cumulative by week, yearly, and maximum instantaneous luminosity. They should be specified as a dictionary, as for example `units = {"cum_day": "pb^{-1}", "cum_week": "pb^{-1}", "cum_year" : "pb^{-1}", "max_inst" : "Hz/nb"}`. You can also specify just some entries if you only want to override some units. Note that only `cum_year` and `max_inst` are applicable for multi-year plots.
* `data_scale_factor`: If the output from brilcalc needs to be scaled by a factor in order to get the correct value, you can specify the factor here. This is necessary for ion runs for 2015 and before, since the luminosity output for these runs was scaled. This can be either a flat factor (in which case all data is scaled by that factor) or a dictionary of years specifying the factor for each year you need to scale. If you just want to change the display (not the actual luminosity), don't use this; see `display_scale_factor` below.
* `color_schemes`: Color schemes for the plots, as defined in `public_plots_tools.py`.
* `verbose`: Adds some extra messages for debugging.
* `plot_directory` : The sub-directory tree to put the plots. If this option is not specified, plots will be put in the subdirectory 'plots'. Make sure that the shell scripts which copy the plots to the web-server space on eos, contain the corresponding directory path.

**Options for single-year plots only**

* `display_units`: This is a bit of a workaround necessary for the fact that the units are changed for PbPb running, so the units that need to be displayed are no longer the same as the units that brilcalc uses internally. See `public_brilcalc_plots_pbpb_2015.cfg` for an example of how this works.
* `normtag_file`: The name of the normtag file to use. If this argument is not included, no normtag file will be used (i.e., the results will use online luminosity).
* `beam_energy`: The beam energy (in GeV). This will be used to display on the plots and (if enabled) for filtering the brilcalc results.
* `filter_brilcalc_results`: If True, only fills matching the beam energy and accelerator mode selected by `beam_energy` and `accel_mode` will be included in the output. If False, all fills in the specified dates will be used. Use this flag carefully: normally you will need to set it to True to exclude various special runs (e.g., the XeXe run in 2017 or the 450 GeV runs in 2018). However it occasionally happens that an otherwise normal fill will have an incorrect beam energy stored, and in the special runs the accelerator mode is also sometimes not correct, so using this filter will incorrectly exclude these runs. Either way, I recommend that you periodically check what happens when you flip this flag and make sure that you understand the resulting differences.
* `lumicalc_script`: The actual script to invoke for getting the luminosity information. This is mostly a legacy option from when we were still in the transition from other tools to brilcalc; now that brilcalc is established, this should always be `brilcalc lumi` (other tools are no longer supported).
* `lumicalc_flags`: Flags to pass to the script defined by `lumicalc_script`. Normally this should be `-b "STABLE BEAMS" --byls` and should not need to be changed (normally changes to the brilcalc invocation are handled by `normtag_file`, `beam_energy`, and `accel_mode`).

**Options for multi-year plots only**

* `display_scale_factor`: If some years have a very small luminosity, you can use this option to scale them by a factor to make them visible. It should be in the format `display_scale_factor = {"2010": {"integrated": 50.0, "peak": 10.0}}`. This is different from `data_scale_factor` above in that it only affects the drawing of the line, not the actual luminosity shown in the totals. Also a label is added to show that the scaling has been applied.

Note that for multi-year plots, `beam_energy` is not used; rather, the per-year defaults defined in the script are used to define the beam energy.

## A note about the cache

Since running the script on a full year's data is a quite lengthy procedure, the script normally keeps the brilcalc output data in a cache directory (specified by the `cache_dir` argument above). By default, when the script is run, it will always regenerate the last 3 days of the cache if no normtag file is being used, or the last 7 days if a normtag file is being used, to make sure that it will always pick up the most recent data (the longer period if a normtag is being used is to account for the occasional case where the fill validation is not run promptly and so fills do not appear in the normtag for several days). However, if the data for older fills changes for whatever reason, the script will not automatically pick up these changes. In order to rebuild the cache, you have a few options:

* If you know which dates need to be updated, simply remove the output files for those dates from the cache directory and re-run; they will automatically be regenerated with the updated data.
* If you want to rebuild the whole cache, you can run the script with the option --ignore-cache, which will rebuild the cached data.
* You can also simply delete (or move) the cache directory, which accomplishes the same as above.

It is recommended to periodically rebuild the cache a few times throughout the year just to catch any unexpected changes that may have happened in the year's data.

## Current setup on lxplus

For the ongoing run3 an acron job on the lumipro account as been set up to run 4 times a day. The corresponding acrontab entry is 

00 0,6,12,18 * * * lxplus.cern.ch /afs/cern.ch/user/l/lumipro/run_public_plots.sh >> /afs/cern.ch/user/l/lumipro/cron_logs/PublicPlots_2022.log

To see the current acron setup use `acrontab -l` and to edit it you can use `acrontab -e`.

The crontab is configured so that it invokes the scripts `~lumipro/run_public_plots.sh`. This is set up as symlink to the actual scripts which should be run (for 2022, `~lumipro/PublicPlots/createlumipublic_2022.sh`), so that if you need to change the script when entering a different run period, you can just alter the symlink to point to the desired script.
