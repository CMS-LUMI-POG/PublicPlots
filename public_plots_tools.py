# coding: utf-8

######################################################################
## File: public_plots_tools.py
######################################################################

import os
import math
from colorsys import hls_to_rgb, rgb_to_hls

import matplotlib
from matplotlib.font_manager import FontProperties
from matplotlib._png import read_png
from matplotlib.offsetbox import OffsetImage
from matplotlib.offsetbox import AnnotationBbox

import numpy as np

######################################################################

FONT_PATH = '/usr/share/fonts/gnu-free/FreeSans.ttf'
FONT_PATH_BOLD = '/usr/share/fonts/gnu-free/FreeSansBold.ttf'
FONT_PATH_ITALIC = '/usr/share/fonts/gnu-free/FreeSansOblique.ttf'
FONT_PROPS_SUPTITLE = FontProperties(fname=FONT_PATH_BOLD, size="16", stretch="condensed")
FONT_PROPS_TITLE = FontProperties(fname=FONT_PATH, size="14", weight="regular")
FONT_PROPS_AX_TITLE = FontProperties(fname=FONT_PATH, size="16", weight="regular")
FONT_PROPS_TICK_LABEL = FontProperties(fname=FONT_PATH, size="14", weight="regular")
FONT_PROPS_CMS_LABEL = FontProperties(fname=FONT_PATH_BOLD, size=24)
FONT_PROPS_PLOT_LABEL = FontProperties(fname=FONT_PATH_ITALIC, size=17)

######################################################################

def InitMatplotlib():
    """Just some Matplotlib settings."""
    matplotlib.rcParams["text.usetex"] = False
    matplotlib.rcParams["legend.numpoints"] = 1
    matplotlib.rcParams["figure.figsize"] = (8., 6.)
    matplotlib.rcParams["figure.dpi"] = 300
    matplotlib.rcParams["savefig.dpi"] = matplotlib.rcParams["figure.dpi"]
    matplotlib.rcParams["font.size"] = 10.8
    matplotlib.rcParams["pdf.fonttype"] = 42
    # End of InitMatplotlib().

######################################################################

#def AddLogo(logo_name, ax, zoom=1.2, xy_offset=(2., -3.)):
def AddLogo(logo_name, ax, zoom=1.2, xy_offset=(0., 0.)):
    """Read logo from PNG file and add it to axes."""
    ax.text( 0.02,0.91 + xy_offset[1], "CMS",
             transform = ax.transAxes,
             horizontalalignment="left",
             fontproperties=FONT_PROPS_CMS_LABEL )

    #
    #
    # logo_data = read_png(logo_name)
    # fig_dpi = ax.get_figure().dpi
    # fig_size = ax.get_figure().get_size_inches()
    # # NOTE: This scaling is kinda ad hoc...
    # zoom_factor = .1 / 1.2 * fig_dpi * fig_size[0] / np.shape(logo_data)[0]
    # zoom_factor *= zoom
    # logo_box = OffsetImage(logo_data, zoom=zoom_factor)
    # ann_box = AnnotationBbox(logo_box, [0., 1.],
    #                          xybox=xy_offset,
    #                          xycoords="axes fraction",
    #                          boxcoords="offset points",
    #                          box_alignment=(0., 1.),
    #                          pad=0., frameon=False)
    # ax.add_artist(ann_box)
    # # End of AddLogo().

######################################################################

def RoundAwayFromZero(val):

    res = None
    if val < 0.:
        res = math.floor(val)
    else:
        res = math.ceil(val)

    # End of RoundAwayFromZero().
    return res

######################################################################

def LatexifyUnits(units_in):

    latex_units = {
        "b^{-1}" : u"b⁻¹",
        "mb^{-1}" : u"mb⁻¹",
        "ub^{-1}" : u"μb⁻¹",
        "nb^{-1}" : u"nb⁻¹",
        "pb^{-1}" : u"pb⁻¹",
        "fb^{-1}" : u"fb⁻¹",
        "Hz/b" : "Hz/b",
        "Hz/mb" : "Hz/mb",
        "Hz/ub" : u"Hz/μb",
        "Hz/nb" : "Hz/nb",
        "Hz/pb" : "Hz/pb",
        "Hz/fb" : "Hz/fb"
        }

    res = latex_units[units_in]

    # End of LatexifyUnits().
    return res

######################################################################

def DarkenColor(color_in):
    """Takes a tuple (r, g, b) as input."""

    color_tmp = matplotlib.colors.colorConverter.to_rgb(color_in)

    tmp = rgb_to_hls(*color_tmp)
    color_out = hls_to_rgb(tmp[0], .7 * tmp[1], tmp[2])

    # End of DarkenColor().
    return color_out

######################################################################

class ColorScheme(object):
    """A bit of a cludge, but a simple way to store color choices."""

    @classmethod
    def InitColors(cls):

        #------------------------------
        # For color scheme 'Greg'.
        #------------------------------

        # This is the light blue of the CMS logo.
        ColorScheme.cms_blue = (0./255., 152./255., 212./255.)

        # This is the orange from the CMS logo.
        ColorScheme.cms_orange = (241./255., 194./255., 40./255.)

        # Slightly darker versions of the above colors for the lines.
        ColorScheme.cms_blue_dark = (102./255., 153./255., 204./255.)
        ColorScheme.cms_orange_dark = (255./255., 153./255., 0./255.)

        #------------------------------
        # For color scheme 'Joe'.
        #------------------------------

        # Several colors from the alternative CMS logo, with their
        # darker line variants.

        ColorScheme.cms_red = (208./255., 0./255., 37./255.)
        ColorScheme.cms_yellow = (255./255., 248./255., 0./255.)
        ColorScheme.cms_purple = (125./255., 16./255., 123./255.)
        ColorScheme.cms_green = (60./255., 177./255., 110./255.)
        ColorScheme.cms_orange2 = (227./255., 136./255., 36./255.)
        ColorScheme.cms_lighttblue = (30./255., 144./255., 255./255.)
        ColorScheme.cms_lightyellow = (255./255., 235./255., 215./255.)

        # End of InitColors().

    def __init__(self, name):

        self.name = name

        # Some defaults.
        self.color_fill_del = "black"
        self.color_fill_rec = "white"
        self.color_fill_cert = "red"
        self.color_fill_peak = "black"
        self.color_line_del = DarkenColor(self.color_fill_del)
        self.color_line_rec = DarkenColor(self.color_fill_rec)
        self.color_line_cert = DarkenColor(self.color_fill_cert)
        self.color_line_peak = DarkenColor(self.color_fill_peak)
        self.color_by_year = {
            2010 : "green",
            2011 : "red",
            2012 : "blue",
	        2013 : "orange",
	        2014 : "orange",
	        2015 : "purple",
            2016 : "orange",
            2017 : "deepskyblue",
            2018 : "navy",
            2022 : "brown",
            2023 : "mediumorchid"
            }
        self.color_line_pileup = "black"
        self.color_fill_pileup = "blue"
        self.logo_name = "cms_logo.png"
        self.file_suffix = "_%s" % self.name.lower()

        tmp_name = self.name.lower()
        if tmp_name == "greg":
            # Color scheme 'Greg'.
            self.color_fill_del = ColorScheme.cms_blue
            self.color_fill_rec = ColorScheme.cms_orange
            self.color_fill_cert = ColorScheme.cms_lightyellow
            self.color_fill_peak = ColorScheme.cms_blue
            self.color_line_del = DarkenColor(self.color_fill_del)
            self.color_line_rec = DarkenColor(self.color_fill_rec)
            self.color_line_cert = DarkenColor(self.color_fill_cert)
            self.color_line_peak = DarkenColor(self.color_fill_peak)
            self.color_line_pileup = "black"
            self.color_fill_pileup = ColorScheme.cms_blue
            self.logo_name = "cms_logo.png"
            self.file_suffix = ""
        elif tmp_name == "joe":
            # Color scheme 'Joe'.
            self.color_fill_del = ColorScheme.cms_yellow
            self.color_fill_rec = ColorScheme.cms_red
            self.color_fill_cert = ColorScheme.cms_orange
            self.color_fill_peak = ColorScheme.cms_yellow
            self.color_line_del = DarkenColor(self.color_fill_del)
            self.color_line_rec = DarkenColor(self.color_fill_rec)
            self.color_line_cert = DarkenColor(self.color_fill_cert)
            self.color_line_peak = DarkenColor(self.color_fill_peak)
            self.color_line_pileup = "black"
            self.color_fill_pileup = ColorScheme.cms_yellow
            self.logo_name = "cms_logo_alt.png"
            self.file_suffix = "_alt"
        else:
            print >> sys.stderr, \
                  "ERROR Unknown color scheme '%s'" % self.name
            sys.exit(1)

        # Find the full path to the logo PNG file.
        # NOTE: This is a little fragile, I think.
        logo_path = os.path.realpath(os.path.dirname(__file__))
        self.logo_name = os.path.join(logo_path,
                                      "./%s" % self.logo_name)

        # End of __init__().

    # End of class ColorScheme.

######################################################################

def SavePlot(fig, file_name_base, ax=None, direc="plots", yamldict={}):
    """Little helper to save plots in various formats."""

    if not ax:
        ax = fig.axes[0]
    # Check some assumptions.
    # assert len(fig.axes) == 2 # this is a little excessively paranoid --
    # just be sure that if it's not fig.axes[0] that you pass the correct axis
    # assert len(ax.artists) == 1

    assert file_name_base.find(".") < 0

    # CS : added the direc option to have the results in a sub-directory
    #      and not mixed with scripts and config files.
    if direc != None and direc != "":
        if not os.path.isdir(direc):
            os.makedirs(direc)
    else:
        direc = ""

    file_name_path = os.path.join( direc, file_name_base )


    # First save as PNG.
    fig.savefig("%s.png" % file_name_path)

    #Conditional in case we do not use the logo but plain text as requested
    #in CMS plot guidelines.
    if len(ax.artists) == 1:
        # Then rescale and reposition the logo (which is assumed to be the
        # only artist in the first pair of axes) and save as PDF.
        tmp_annbox = ax.artists[0]
        tmp_offsetbox = tmp_annbox.offsetbox
        fig_dpi = fig.dpi
        tmp_offsetbox.set_zoom(tmp_offsetbox.get_zoom() * 72. / fig_dpi)
        # CS: tmp = tmp_annbox.xytext ==> The api seems to have changed:
        tmp = tmp_annbox.xyann
        # CS tmp_annbox.xytext = (tmp[0] + 1., tmp[1] - 1.)
        #                             ==> The api seems to have changed:
        tmp_annbox.xyann = (tmp[0] + 1., tmp[1] - 1.)

    fig.savefig("%s.pdf" % file_name_path, dpi=600)

    if yamldict == {} :
        return

    # Yamldict contains all we need to crete an unique directory and file name.
    # year, date, particle, run (run 1,2,3 ... ), energystring, log_suffix,
    # category(Online, Normtag), title caption

    run = yamldict['run']
    particle = yamldict['particle']
    year = yamldict['year']
    energystr = yamldict['energystr']
    log_suffix = yamldict['log_suffix']

    dirname = os.path.join( direc, run, file_name_base )

    yamlstr = ""
    yamlstr += "title: '" + yamldict['title'] + "'\n"
    yamlstr += "date: '" + str(yamldict['date']) + "'\n"
    yamlstr += "caption: '" + yamldict['caption'] + "'\n"
    yamlstr += "tags: ["
    for tag in ['run','particle','year','energystr']:
        yamlstr += '"' + str(yamldict[tag]) + '",'
    yamlstr = yamlstr[:-1]
    yamlstr += "]\n"

    if not os.path.exists( dirname ):
        os.makedirs( dirname )

    pathname = os.path.join( dirname, file_name_base)
    fd = open(pathname + ".yaml", 'w+')
    fd.write( yamlstr )
    fd.close()

    fig.savefig("%s.png" % pathname)

    # End of SavePlot().

######################################################################
