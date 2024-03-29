#!/usr/bin/env python
# coding: utf-8

######################################################################
## File: create_public_pileup_plots.py
######################################################################

# NOTE: Typical way to create the pileup ROOT file from the cached txt
# files (maintained by Mike Hildreth):
# pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/DCSOnly/json_DCSONLY.txt \
# --inputLumiJSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_latest.txt \
# --calcMode true --maxPileupBin=40 pu2012DCSONLY.root

from __future__ import print_function
import sys
import os
import commands
import math
import optparse
import ConfigParser

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True
from ROOT import TFile

from public_plots_tools import ColorScheme
from public_plots_tools import LatexifyUnits
from public_plots_tools import AddLogo
from public_plots_tools import InitMatplotlib
from public_plots_tools import RoundAwayFromZero
from public_plots_tools import SavePlot
from public_plots_tools import FONT_PROPS_SUPTITLE
from public_plots_tools import FONT_PROPS_TITLE
from public_plots_tools import FONT_PROPS_AX_TITLE
from public_plots_tools import FONT_PROPS_TICK_LABEL
from public_plots_tools import FONT_PROPS_PLOT_LABEL

try:
    import debug_hook
    import pdb
except ImportError:
    pass

######################################################################

def TweakPlot(fig, ax, add_extra_head_room=False):

    # Fiddle with axes ranges etc.
    ax.relim()
    ax.autoscale_view(False, True, True)
    for label in ax.get_xticklabels():
        label.set_ha("right")
        label.set_rotation(30.)

    # Bit of magic here: increase vertical scale by one tick to make
    # room for the legend.
    if add_extra_head_room:
        y_ticks = ax.get_yticks()
        (y_min, y_max) = ax.get_ylim()
        is_log = (ax.get_yscale() == "log")
        y_max_new = y_max
        if is_log:
            tmp = y_ticks[-1] / y_ticks[-2]
            y_max_new = y_max * math.pow(tmp, add_extra_head_room)
            # Try to convince matplotlib to fill the space up to the bottom
            # of the plots
            y_min = y_min * 10
        else:
            tmp = y_ticks[-1] - y_ticks[-2]
            y_max_new = y_max + add_extra_head_room * tmp
        ax.set_ylim(y_min, y_max_new)

    # Add a second vertical axis on the right-hand side.
    ax_sec = ax.twinx()
    ax_sec.set_ylim(ax.get_ylim())
    ax_sec.set_yscale(ax.get_yscale())

    for ax_tmp in fig.axes:
        for sub_ax in [ax_tmp.xaxis, ax_tmp.yaxis]:
            for label in sub_ax.get_ticklabels():
                label.set_font_properties(FONT_PROPS_TICK_LABEL)

    if is_log:
        fig.subplots_adjust(top=.89, bottom=.125, left=.11, right=.925)
    else:
        fig.subplots_adjust(top=.89, bottom=.125, left=.1, right=.925)

    # End of TweakPlot().

######################################################################

if __name__ == "__main__":

    desc_str = "This script creates the official CMS pileup plots " \
               "based on the output from the pileupCalc.py script."
    arg_parser = optparse.OptionParser(description=desc_str)
    (options, args) = arg_parser.parse_args()
    if len(args) != 1:
        print("ERROR Need exactly one argument: a config file name", file=sys.stderr)
        sys.exit(1)
    config_file_name = args[0]

    cfg_defaults = {
        "color_schemes" : "Joe, Greg",
        "verbose" : False,
        "plot_label" : "",
        "file_suffix" : ""
    }
    cfg_parser = ConfigParser.SafeConfigParser(cfg_defaults)
    if not os.path.exists(config_file_name):
        print("ERROR Config file '%s' does not exist" % config_file_name, file=sys.stderr)
        sys.exit(1)
    cfg_parser.read(config_file_name)

    # Location of the cached ROOT file.
    cache_file_dir = cfg_parser.get("general", "cache_dir")

    # Which color scheme to use for drawing the plots.
    color_scheme_names_tmp = cfg_parser.get("general", "color_schemes")
    color_scheme_names = [i.strip() for i in color_scheme_names_tmp.split(",")]
    # Flag to turn on verbose output.
    verbose = cfg_parser.getboolean("general", "verbose")
    # Suffix to append to all file names.
    file_suffix2 = cfg_parser.get("general", "file_suffix")

    # Some things needed for titles etc.
    particle_type_str = cfg_parser.get("general", "particle_type_str")
    year = int(cfg_parser.get("general", "year"))
    cms_energy_str = cfg_parser.get("general", "cms_energy_str")

    # get the directory where to put the plots
    plot_directory_tmp = cfg_parser.get("general", "plot_directory")
    if not plot_directory_tmp:
        plot_directory = "plots"
        print("No plot directory specified --> using default value '%s'" % plot_directory)
    else:
        plot_directory = plot_directory_tmp
        print("Plots will be stored in directory '%s'." % plot_directory)

    xsection = float(cfg_parser.get("general", "xsection"))/1000
    print("Inelastic x-section:", xsection, "mb at", cms_energy_str)

    ##########

    # Tell the user what's going to happen.
    print("Using configuration from file '%s'" % config_file_name)
    print("Using color schemes '%s'" % ", ".join(color_scheme_names))

    ##########

    InitMatplotlib()

    ##########

    # read the results of pileupCalc which should be in the cache:
    xsec_suffix = cfg_parser.get("general", "xsection")
    tmp_file_name = os.path.join(cache_file_dir,"pileup_calc_" + xsec_suffix + "_tmp.root")

    in_file = TFile.Open(tmp_file_name, "READ")
    if not in_file or in_file.IsZombie():
        print("ERROR Could not read back pileupCalc results", file=sys.stderr)
        sys.exit(1)
    pileup_hist = in_file.Get("pileup")
    pileup_hist.SetDirectory(0)
    in_file.Close()

    ##########

    # And this is where the plotting starts.
    print("Drawing things...")
    ColorScheme.InitColors()

    # Turn the ROOT histogram into a Matplotlib one.
    bin_edges = [pileup_hist.GetBinLowEdge(i) \
                 for i in range(1, pileup_hist.GetNbinsX() + 1)]
    vals = [pileup_hist.GetBinCenter(i) \
            for i in range(1, pileup_hist.GetNbinsX() + 1)]
    weights = [pileup_hist.GetBinContent(i) \
               for i in range(1, pileup_hist.GetNbinsX() + 1)]
    # NOTE: Convert units to /pb!
    weights = [1.e-6 * i for i in weights]

    # Loop over all color schemes.
    for color_scheme_name in color_scheme_names:

        print("    color scheme '%s'" % color_scheme_name)

        color_scheme = ColorScheme(color_scheme_name)
        color_line_pileup = color_scheme.color_line_pileup
        color_fill_pileup = color_scheme.color_fill_pileup
        logo_name = color_scheme.logo_name
        file_suffix = color_scheme.file_suffix

        fig = plt.figure()

        for type in ["lin", "log"]:
            is_log = (type == "log")
            log_setting = False
            if is_log:
                min_val = min(weights)
                if min_val == 0.:
                    exp = 0.
                else:
                    exp = RoundAwayFromZero(math.log10(min_val))
                log_setting = math.pow(10., exp)

            fig.clear()
            ax = fig.add_subplot(111)

            ax.hist(vals, bins=bin_edges, weights=weights, log=log_setting,
                    histtype="stepfilled",
                    edgecolor=color_line_pileup,
                    facecolor=color_fill_pileup)

            # No title according to CMS plot guidelines
            # Set titles and labels.
            # Due to a bug in matplotlib 1.5.3 we cannot directly set the
            # fontproperties in the call but need to use the method
            # set_fontproperties. This might disapear with a new version of
            # matplotlib
            # fig.suptitle(r"CMS Average Pileup, " \
            #              "%s, %d, $\mathbf{\sqrt{s} =}$ %s" % \
            #              (particle_type_str, year, cms_energy_str)) \
            #    .set_fontproperties(FONT_PROPS_SUPTITLE)
            ax.set_xlabel(r"Mean number of interactions per crossing",
                          fontproperties=FONT_PROPS_AX_TITLE)
            # The labelpad is necessary since otherwise the label goes
            # out of the picture frame and is cut.
            ax.set_ylabel(r"Recorded luminosity (%s/%.1f)" % \
                          (LatexifyUnits("pb^{-1}"),
                           pileup_hist.GetBinWidth(1)),
                          labelpad = 0,
                          fontproperties=FONT_PROPS_AX_TITLE)

            # Add the average pileup number to the top right.
            ax.text(.95, .925, u"<μ> = %.0f" % \
                    round(pileup_hist.GetMean()),
                    transform = ax.transAxes,
                    horizontalalignment="right",
                    fontproperties=FONT_PROPS_AX_TITLE)

            # Add the inelastic pp cross section employed
            ax.text(.95, .7, u"σ"+r"$\mathregular{{}_{in}^{pp}}$ = "+str(xsection)+" mb",
                     transform = ax.transAxes,
                     horizontalalignment="right",
                     fontproperties=FONT_PROPS_AX_TITLE,
                     fontsize=9)

            if cfg_parser.get("general", "plot_label"):
                ax.text(0.02, 0.85, cfg_parser.get("general", "plot_label"),
                        verticalalignment="center", horizontalalignment="left",
                        transform = ax.transAxes, fontproperties=FONT_PROPS_PLOT_LABEL)

            # Add the logo.
            AddLogo(logo_name, ax)
            TweakPlot(fig, ax, True)

            xsec_suffix = "_" + cfg_parser.get("general", "xsection")
            log_suffix = ""
            if is_log:
                log_suffix = "_log"
            fn_particle_type_str = particle_type_str.replace(' ','_')
            SavePlot(fig, "pileup_%s_%d%s%s%s%s" % \
                     (fn_particle_type_str, year,
                      log_suffix, file_suffix, xsec_suffix,file_suffix2),
                     direc = plot_directory)

        plt.close()

    ##########

    print("Done")

######################################################################
