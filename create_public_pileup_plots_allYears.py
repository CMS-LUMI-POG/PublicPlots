#!/usr/bin/env python
# coding: utf-8

######################################################################
## File: create_public_pileup_plots_allYears.py
######################################################################

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
        fig.subplots_adjust(top=.95, bottom=.125, left=.12, right=.925)
    else:
        fig.subplots_adjust(top=.95, bottom=.125, left=.11, right=.925)

    # End of TweakPlot().

######################################################################

def MakePlot(xvalues, yvalues, labels, is_stacked=False, has_run1=False, has_run2=False, has_run3=False):

    print "Selected is_stacked = ", is_stacked
    print "Selected has_run1 = ", has_run1
    print "Selected has_run2 = ", has_run2
    print "Selected has_run3 = ", has_run3

    print "Drawing things..."

    fig = plt.figure()
    log_setting = False
    fig.clear()

    ax = fig.add_subplot(111)

    histo_type="step"
    stack_suffix = ""
    run_suffix = ""
    transparency = 1
    add_extra_head_room = True
    if is_stacked:
        histo_type="stepfilled"
        stack_suffix = "_stack"
    if has_run1 and has_run2 and has_run3:
        add_extra_head_room = 2
    elif (not has_run1) and has_run2 and has_run3:
        run_suffix = "_run2and3"
    elif (not has_run1) and has_run2 and (not has_run3):
        run_suffix = "_run2"
    elif (not has_run1) and (not has_run2) and has_run3:
        run_suffix = "_run3"

    ax.hist(xvalues, bins=bin_edges,
            weights=yvalues,
            log=log_setting,
            histtype=histo_type, stacked=is_stacked,
            color=color_fill_histos,
            alpha=transparency,
            label=labels
            )
    ax.legend(prop=FONT_PROPS_AX_TITLE, frameon=False)

    ax.set_xlabel(r"Mean number of interactions per crossing",
                  fontproperties=FONT_PROPS_AX_TITLE)
    ax.set_ylabel(r"Recorded luminosity (%s/%.1f)" % \
                      (LatexifyUnits("fb^{-1}"),
                       pileup_hist2023.GetBinWidth(1)),
                  fontproperties=FONT_PROPS_AX_TITLE)

    # Add the inelastic pp cross section employed
    if (not has_run1) and has_run2 and (not has_run3):
        ax.text(.97, .35, u"σ"+r"$\mathregular{{}_{in}^{pp}}$ = "+str(xsection13)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
    elif (not has_run1) and (not has_run2) and has_run3:
        ax.text(.97, .35, u"σ"+r"$\mathregular{{}_{in}^{pp}}$ = "+str(xsection13p6)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
    elif (not has_run1) and has_run2 and has_run3:
        ax.text(.97, .35, u"σ"+r"$\mathregular{{}_{in}^{pp}}$(13.6 TeV) = "+str(xsection13p6)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
        ax.text(.97, .28, u"σ"+r"$\mathregular{{}_{in}^{pp}}$(13 TeV) = "+str(xsection13)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
    else:
        ax.text(.97, .38, u"σ"+r"$\mathregular{{}_{in}^{pp}}$(13.6 TeV) = "+str(xsection13p6)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
        ax.text(.97, .31, u"σ"+r"$\mathregular{{}_{in}^{pp}}$(13 TeV) = "+str(xsection13)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
        ax.text(.97, .24, u"σ"+r"$\mathregular{{}_{in}^{pp}}$(8 TeV) = "+str(xsection8)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)
        ax.text(.97, .17, u"σ"+r"$\mathregular{{}_{in}^{pp}}$(7 TeV) = "+str(xsection7)+" mb",
                 transform = ax.transAxes,
                 horizontalalignment="right",
                 fontproperties=FONT_PROPS_AX_TITLE,
                 fontsize=9)

    # Add the logo.
    AddLogo(logo_name, ax)
    TweakPlot(fig, ax, add_extra_head_room)

    SavePlot(fig, "pileup_allYears%s%s" % (stack_suffix,run_suffix), direc=plot_directory)

    plt.close()

    return
    # End of MakePlot().


######################################################################

def ConvertROOTtoMatplotlib(pileup_hist):
    # Dump the ROOT histogram bins into a vector
    weights = [pileup_hist.GetBinContent(i) \
               for i in xrange(1, pileup_hist.GetNbinsX() + 1)]
    # NOTE: Convert units to /fb!
    weights = [1.e-9 * i for i in weights]
    return weights

######################################################################

def LoadHistogram(directory,filename):

    # load ROOT histogram
    print "Loading histogram", filename, "from", directory
    tmp_file_name = os.path.join(directory,filename)
    in_file = TFile.Open(tmp_file_name, "READ")
    if not in_file or in_file.IsZombie():
        print >> sys.stderr, \
              "ERROR Could not read back pileupCalc results"
        sys.exit(1)
    pileup_hist = in_file.Get("pileup")
    pileup_hist.SetDirectory(0)
    in_file.Close()

    weights = ConvertROOTtoMatplotlib(pileup_hist)

    return (pileup_hist,weights)

######################################################################

if __name__ == "__main__":

    # Load and parse config file
    desc_str = "This script creates the official CMS pileup plots " \
               "based on the output from the pileupCalc.py script."
    arg_parser = optparse.OptionParser(description=desc_str)
    (options, args) = arg_parser.parse_args()
    if len(args) != 1:
        print >> sys.stderr, \
              "ERROR Need exactly one argument: a config file name"
        sys.exit(1)
    config_file_name = args[0]

    cfg_defaults = {
        "stacked" : False
        }
    cfg_parser = ConfigParser.SafeConfigParser(cfg_defaults)
    if not os.path.exists(config_file_name):
        print >> sys.stderr, \
              "ERROR Config file '%s' does not exist" % config_file_name
        sys.exit(1)
    cfg_parser.read(config_file_name)

    # Location of the cached ROOT file.
    cachedir = cfg_parser.get("general", "cache_dir")
    rootfile2023 = cfg_parser.get("general", "rootfile2023")
    rootfile2022 = cfg_parser.get("general", "rootfile2022")
    rootfile2018 = cfg_parser.get("general", "rootfile2018")
    rootfile2017 = cfg_parser.get("general", "rootfile2017")
    rootfile2016 = cfg_parser.get("general", "rootfile2016")
    rootfile2015 = cfg_parser.get("general", "rootfile2015")
    rootfile2012 = cfg_parser.get("general", "rootfile2012")
    rootfile2011 = cfg_parser.get("general", "rootfile2011")

    xsection13p6 = float(cfg_parser.get("general", "xsection13p6"))/1000
    xsection13 = float(cfg_parser.get("general", "xsection13"))/1000
    xsection8 = float(cfg_parser.get("general", "xsection8"))/1000
    xsection7 = float(cfg_parser.get("general", "xsection7"))/1000
    print "Inelastic x-sections:", xsection13p6, "mb at 13.6 TeV,", xsection13, "mb at 13 TeV,", xsection8, "mb at 8 TeV, and", xsection7, "mb at 7 TeV"

    # get the directory where to put the plots
    plot_directory_tmp = cfg_parser.get("general", "plot_directory")
    if not plot_directory_tmp:
        plot_directory = "plots"
        print("No plot directory specified --> using default value '%s'" % plot_directory)
    else:
        plot_directory = plot_directory_tmp
        print("Plots will be stored in directory '%s'." % plot_directory)


    ##########

    # Tell the user what's going to happen.
    print "Using configuration from file '%s'" % config_file_name

    InitMatplotlib()

    ##########

    # open pileup files
    (pileup_hist2023,weights2023) = LoadHistogram(cachedir,rootfile2023)
    (pileup_hist2022,weights2022) = LoadHistogram(cachedir,rootfile2022)
    (pileup_hist2018,weights2018) = LoadHistogram(cachedir,rootfile2018)
    (pileup_hist2017,weights2017) = LoadHistogram(cachedir,rootfile2017)
    (pileup_hist2016,weights2016) = LoadHistogram(cachedir,rootfile2016)
    (pileup_hist2015,weights2015) = LoadHistogram(cachedir,rootfile2015)
    (pileup_hist2012,weights2012) = LoadHistogram(cachedir,rootfile2012)
    (pileup_hist2011,weights2011) = LoadHistogram(cachedir,rootfile2011)

    # take the bins from the most recent histogram
    bin_edges = [pileup_hist2023.GetBinLowEdge(i) \
                     for i in xrange(1, pileup_hist2023.GetNbinsX() + 1)]
    vals = [pileup_hist2023.GetBinCenter(i) \
                for i in xrange(1, pileup_hist2023.GetNbinsX() + 1)]


    # And this is where the plotting starts.
    ColorScheme.InitColors()
    color_scheme = ColorScheme("Greg") # note by Andrea G.: in other LUM POG scripts there is an option to choose color scheme, and two are selected simultaneously and executed in a loop; but in my opinion that's unnecessary and cumbersome, and I prefer the "Greg" scheme anyway!
    color_line_pileup = color_scheme.color_line_pileup
    logo_name = color_scheme.logo_name

    # Plot all years in the same plot, first stacked and then superimposed:
    xvalues=[vals,vals,vals,vals,vals,vals,vals,vals]
    yvalues=[weights2011,weights2012,weights2015,weights2016,weights2017,weights2018,weights2022,weights2023]
    color_fill_histos = [color_scheme.color_by_year[2011], color_scheme.color_by_year[2012], color_scheme.color_by_year[2015], color_scheme.color_by_year[2016], color_scheme.color_by_year[2017], color_scheme.color_by_year[2018], color_scheme.color_by_year[2022], color_scheme.color_by_year[2023]]
    labels = [u"2011 (7 TeV): <μ> = %.0f" % round(pileup_hist2011.GetMean()),
              u"2012 (8 TeV): <μ> = %.0f" % round(pileup_hist2012.GetMean()),
              u"2015 (13 TeV): <μ> = %.0f" % round(pileup_hist2015.GetMean()),
              u"2016 (13 TeV): <μ> = %.0f" % round(pileup_hist2016.GetMean()),
              u"2017 (13 TeV): <μ> = %.0f" % round(pileup_hist2017.GetMean()),
              u"2018 (13 TeV): <μ> = %.0f" % round(pileup_hist2018.GetMean()),
              u"2022 (13.6 TeV): <μ> = %.0f" % round(pileup_hist2022.GetMean()),
              u"2023 (13.6 TeV): <μ> = %.0f" % round(pileup_hist2023.GetMean())]
    MakePlot(xvalues,yvalues,labels,is_stacked=True,has_run1=True,has_run2=True,has_run3=True)
    MakePlot(xvalues,yvalues,labels,has_run1=True,has_run2=True,has_run3=True)

    # Now make a Run-2 + Run-3 plot:
    xvalues=[vals,vals,vals,vals,vals,vals]
    yvalues=[weights2015,weights2016,weights2017,weights2018,weights2022,weights2023]
    color_fill_histos = [color_scheme.color_by_year[2015], color_scheme.color_by_year[2016], color_scheme.color_by_year[2017], color_scheme.color_by_year[2018], color_scheme.color_by_year[2022], color_scheme.color_by_year[2023]]
    labels = [u"2015: <μ> = %.0f" % round(pileup_hist2015.GetMean()),
              u"2016: <μ> = %.0f" % round(pileup_hist2016.GetMean()),
              u"2017: <μ> = %.0f" % round(pileup_hist2017.GetMean()),
              u"2018: <μ> = %.0f" % round(pileup_hist2018.GetMean()),
              u"2022: <μ> = %.0f" % round(pileup_hist2022.GetMean()),
              u"2023: <μ> = %.0f" % round(pileup_hist2023.GetMean())]
    MakePlot(xvalues,yvalues,labels,is_stacked=True,has_run2=True,has_run3=True)
    MakePlot(xvalues,yvalues,labels,has_run2=True,has_run3=True)

    # Now make a Run-3 only plot:
    pileup_histRun3 = pileup_hist2023.Clone()
    pileup_histRun3.Add(pileup_hist2022)
    weightsRun3 = ConvertROOTtoMatplotlib(pileup_histRun3)
    xvalues=[vals,vals,vals]
    yvalues=[weights2022,weights2023,weightsRun3]
    color_fill_histos = [color_scheme.color_by_year[2022], color_scheme.color_by_year[2023], "black"]
    labels = [u"2022: <μ> = %.0f" % round(pileup_hist2022.GetMean()),
              u"2023: <μ> = %.0f" % round(pileup_hist2023.GetMean()),
              u"Run 3: <μ> = %.0f" % round(pileup_histRun3.GetMean())]
    MakePlot(xvalues,yvalues,labels,has_run3=True)
    color_fill_histos=color_fill_histos[:-1]
    MakePlot(xvalues[:-1],yvalues[:-1],labels[:-1],is_stacked=True,has_run3=True)

    # Now make a Run-2 only plot:
    # pileup_histRun2 = pileup_hist2018.Clone()
    # pileup_histRun2.Add(pileup_hist2017)
    # pileup_histRun2.Add(pileup_hist2016)
    # pileup_histRun2.Add(pileup_hist2015)
    # weightsRun2 = ConvertROOTtoMatplotlib(pileup_histRun2)
    # xvalues=[vals,vals,vals,vals,vals]
    # yvalues=[weights2015,weights2016,weights2017,weights2018,weightsRun2]
    # color_fill_histos = [color_scheme.color_by_year[2015], color_scheme.color_by_year[2016], color_scheme.color_by_year[2017], color_scheme.color_by_year[2018], "black"]
    # labels = [u"2015: <μ> = %.0f" % round(pileup_hist2015.GetMean()),
    #           u"2016: <μ> = %.0f" % round(pileup_hist2016.GetMean()),
    #           u"2017: <μ> = %.0f" % round(pileup_hist2017.GetMean()),
    #           u"2018: <μ> = %.0f" % round(pileup_hist2018.GetMean()),
    #           u"Run 2: <μ> = %.0f" % round(pileup_histRun2.GetMean())]
    # MakePlot(xvalues,yvalues,labels,has_run2=True)
    # color_fill_histos=color_fill_histos[:-1]
    # MakePlot(xvalues[:-1],yvalues[:-1],labels[:-1],is_stacked=True,has_run2=True)

    ##########


    print "Done"

######################################################################

# USEFUL EXAMPLES:

# https://matplotlib.org/examples/statistics/histogram_demo_multihist.html
# https://stackoverflow.com/questions/18449602/matplotlib-creating-stacked-histogram-from-three-unequal-length-arrays
# https://matplotlib.org/examples/pylab_examples/stackplot_demo.html
# https://matplotlib.org/gallery/lines_bars_and_markers/bar_stacked.html

# this one is for legends:
# https://jakevdp.github.io/PythonDataScienceHandbook/04.06-customizing-legends.html

# MANUAL:

# https://matplotlib.org/api/pyplot_api.html
