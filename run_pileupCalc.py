#!/usr/bin/env python

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

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True
from ROOT import TFile

try:
    import debug_hook
    import pdb
except ImportError:
    pass


if __name__ == "__main__":

    desc_str = "This script creates the official CMS pileup plots " \
               "based on the output from the pileupCalc.py script."
    arg_parser = optparse.OptionParser(description=desc_str)
    arg_parser.add_option("--ignore-cache", action="store_true",
                          help="Ignore all cached PU results " \
                          "and run pileupCalc. " \
                          "(Rebuilds the cache as well.)")
    (options, args) = arg_parser.parse_args()
    if len(args) != 1:
        print("ERROR Need exactly one argument: a config file name", file=sys.stderr)
        sys.exit(1)
    config_file_name = args[0]
    ignore_cache = options.ignore_cache

    cfg_defaults = {
        "pileupcalc_flags" : "",
        "color_schemes" : "Joe, Greg",
        "verbose" : False
        }
    cfg_parser = ConfigParser.SafeConfigParser(cfg_defaults)
    if not os.path.exists(config_file_name):
        print("ERROR Config file '%s' does not exist" % config_file_name, file=sys.stderr)
        sys.exit(1)
    cfg_parser.read(config_file_name)

    # Location of the cached ROOT file.
    cache_file_dir = cfg_parser.get("general", "cache_dir")
    verbose = cfg_parser.getboolean("general", "verbose")

    # Some details on how to invoke pileupCalc.
    pileupcalc_flags_from_cfg = cfg_parser.get("general", "pileupcalc_flags")
    input_json = cfg_parser.get("general", "input_json")
    input_lumi_json = cfg_parser.get("general", "input_lumi_json")

    # Some things needed for the print-out.
    cms_energy_str = cfg_parser.get("general", "cms_energy_str")

    xsection = float(cfg_parser.get("general", "xsection"))/1000
    print("Inelastic x-section:", xsection, "mb at", cms_energy_str)

    ##########

    # Tell the user what's going to happen.
    print("Using configuration from file '%s'" % config_file_name)
    #print("Using color schemes '%s'" % ", ".join(color_scheme_names))
    print("Using additional pileupCalc flags from configuration: '%s'" % \
          pileupcalc_flags_from_cfg)
    print("Using input JSON filter: %s" % input_json)
    print("Using input lumi JSON filter: %s" % input_lumi_json)

    ##########

    # Run pileupCalc if necessary (either no cache f0ile
    #              or we are forced to ignore the cache).
    xsec_suffix = cfg_parser.get("general", "xsection")
    tmp_file_name = os.path.join(cache_file_dir,"pileup_calc_" + xsec_suffix + "_tmp.root")

    # run pileupCalc if the cache file does not exist or if we should ignore it
    if not os.path.isfile(tmp_file_name) or ignore_cache:
        if not os.path.isdir(cache_file_dir): 
            os.makedirs( cache_file_dir )
            print("Created directory for pileup cache file: ", cache_file_dir ) 
        cmd = "pileupCalc.py -i %s --inputLumiJSON=%s %s %s" % \
              (input_json, input_lumi_json,
               pileupcalc_flags_from_cfg, tmp_file_name)
        print("Running pileupCalc (this may take a while)")
        if verbose:
            print("  pileupCalc cmd: '%s'" % cmd)
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            print("ERROR Problem running pileupCalc: %s" % output, file=sys.stderr)
            sys.exit(1)
        
        print( "pileupCalc run finished" )
    else:
        print( "Not necessary to run pileupCalc since cached results exist. (If you want to ") 
        print( "            force a new run specify the ignore_cache option in the cfg file.")
        
######################################################################
