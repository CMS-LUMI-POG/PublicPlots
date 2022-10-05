#!/usr/bin/python3
import os
import pathlib
import re
from datetime import datetime
import subprocess
import shlex
import sys

##################################################################################
# This script is steering the process of generating pileup-plots based on the 
# latest data-certification files. It is regularly launched during a running 
# period via a cron-job. It handles the running of brilcalc to produce the lumi
# per bunch-crossing for the certified lumi-sections, the production fo the
# summary file "pileup-latest.json" which finally is used to generate the pileup
# plots in the last step.
# The script relies on a set of filepaths and names which need to be edited 
# according ot the actual running period. These names are summarised in the 
# following section.
##################################################################################

# Directory where intermediate files and log files are stored
WORKDIR = "/afs/cern.ch/user/l/lumipro/Pileup"

# Will be used for the destination directory of the the intermediate pileup_latest.json
YEARSTR = "2022"

# Directory where the scripts are located (a git area)
SCRIPTDIR = "/afs/cern.ch/user/l/lumipro/PublicPlots"

# The directory containing the certification json files to be processed
CERTIFICATION_BASE = "/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/DCSOnly_JSONS"

# A regular expression for the file name of the certificatoin json. 
# The filename with the largest number for the last processed run will be 
# chosen (the second sub-pattern)
# This pattern needs to be changed every year (at least)
JSON_PATTERN = "Cert_Collisions2022_(\d+)_(\d+)_13p6TeV_DCSOnly_TkPx.json"

NORMTAG = "/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json"

LOGFILE = os.path.join( WORKDIR, "pileup.log")

# cachefile for last successfully processed json to avoid double processing
# of the same data over and over again with the cron-job:
certification_cachefile = os.path.join( WORKDIR, "_lastProcessedCertification.txt")

# intermediate output product from brilcalc (a very large file)
LUMICSV = os.path.join( WORKDIR, "lumi_DCSONLY.csv")

# output product from makePileupJSON.py (needed for the pileup plots)
PILEUP_JSON = os.path.join( WORKDIR, "pileup_latest.json")

# A link to the lastest DCS Json certifiction file in the eos DQM area
# This link will be updated when new certification files are found with 
# the above mentioned file pattern.
DCSJsonLink = os.path.join( WORKDIR, "DCSOnly.json")

###################################################################################

# The print function is re-defined here in order to be able to easily switch
# the print-out to a log file)
def print( *args ):

    pstr = str(datetime.now()) + " : "
    for arg in args:
        pstr += str(arg)
    pstr += "\n"

    fd = open(LOGFILE,"a+")
    fd.write(pstr)
    fd.close()

    
# Given a directory (CERTIFICATION_BASE) and a regular expression for 
# the json filename (JSON_PATTERN) this function finds the latest certification
# json in the DQM certification directory tree on eos. It assumes that the 
# filename contains the first run certified and the last run certified and that
# looks for the filename with the largest last processed run number. It does not
# do any checks on the first certified run number.
def findLatestJson():
    dir_contents = os.listdir( CERTIFICATION_BASE )
    latestPath = None
    runcmp = 0
    for entry in dir_contents:
        epath = os.path.join( CERTIFICATION_BASE, entry )
        if not os.path.isfile(epath):
            continue
        mo = re.match( JSON_PATTERN, entry )
        if not mo:
            continue
        start_run = int(mo.group(1))
        last_run = int(mo.group(2))
        if last_run > runcmp:
            runcmp = last_run
            latestPath = epath
    if latestPath:
        mtime = pathlib.Path(latestPath).stat().st_mtime
    return( latestPath, mtime )



# The script maintains a small cache file with the name of the latest 
# processed certification JSON file. This avoids re-processing over and over
# again the same certification file without that anything changed.
def checkIfNew( path ):
    if not os.path.isfile(certification_cachefile):
        print( "Make symlink DCSOnly.json to ", path )
        if os.path.isfile( DCSJsonLink ):
            os.remove(DCSJsonLink)
        os.symlink( path, DCSJsonLink )
        return True
    
    fd = open(certification_cachefile, 'r')
    lastfile = fd.read()
    fd.close()
    if lastfile == path:
        print( "The certification file ", path, " has already been processed.")
        return False
    
    print( "Make symlink DCSOnly.json to ", path )
    if os.path.isfile( DCSJsonLink ):
        os.remove(DCSJsonLink)
    os.symlink( path, DCSJsonLink )

    return True

def updateCertificationCache( path ):
    fd = open(certification_cachefile, 'w+')
    fd.write( path )
    fd.close()

# Brilcalc is launched with a certification json file as input in order to create a 
# csv file containing for all lumi sections the lumi per bunch. This is a large file but
# it is needed in the next processing step.
def launchBrilcalc( certificationJson ):

    # Only process if the certification file was not yet processed:
    if not checkIfNew( certificationJson ):
        return False

    # adjust the environment to run brilcalc
    my_env = os.environ.copy()
    print( "env : ", my_env )
    my_env['PATH'] = my_env['HOME'] + '/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/bin:' + my_env['PATH']
    my_env['LD_LIBRARY_PATH'] = '/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/root/lib:'
    my_env['PYTHONPATH'] = '/afs/cern.ch/cms/lumi/brilconda-1.1.7-cc7/root/lib:'

    # Now run brilcalc
    cmd = 'brilcalc lumi --xing -i ' + certificationJson + ' -b "STABLE BEAMS" --normtag ' +  NORMTAG + ' --xingTr 0.1 -o ' + LUMICSV
    args = shlex.split(cmd)
    print (cmd)

    try:
        cproc = subprocess.run( args, env = my_env, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                check = True, encoding='ascii' )
    except subprocess.CalledProcessError as e :
        print( "Error encountered when launching the command : ", e.args)
        print( "Error code: ", e.returncode)
        print( "stdout : \n\n" + e.stdout )
        print( "stderr : \n\n" + e.stderr )
        return
    print( "Output of command ", cproc.args )
    print( "stdout : \n" + cproc.stdout )
    print( "stderr : \n" + cproc.stderr )

    updateCertificationCache( certificationJson )

    return True
    

# This function launches a script ot produce the "pileup_latest.json" file which 
# is the base for the production of the pileup plots. The file is transfered to the 
# public area of the lumipro account. Since the production of this file is done with
# help of a script in CMSSW, a sub-script is used which sets up the correct CMSSW 
# environment to run that tool.
def makePileupJson():

    args = [ os.path.join(SCRIPTDIR, "run_makePileupJSON.sh"), LUMICSV, PILEUP_JSON, YEARSTR ]

    try:
        cproc = subprocess.run( args, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                check = True, encoding='ascii' )
    except subprocess.CalledProcessError as e :
        print( "Error encountered when launching the command : ", e.args)
        print( "Error code: ", e.returncode)
        print( "stdout : \n\n" + e.stdout )
        print( "stderr : \n\n" + e.stderr )
        return
    print( "Output of command ", cproc.args )
    print( "stdout : \n" + cproc.stdout )
    print( "stderr : \n" + cproc.stderr )
    

# This function launches the script to produce the pileup plots.
def makePileupPlots():

    args = [os.path.join(SCRIPTDIR, "createpileuppublic_" + YEARSTR + ".sh")]
    try:
        cproc = subprocess.run( args, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                check = True, encoding='ascii' )
    except subprocess.CalledProcessError as e :
        print( "Error encountered when launching the command : ", e.args)
        print( "Error code: ", e.returncode)
        print( "stdout : \n\n" + e.stdout )
        print( "stderr : \n\n" + e.stderr )
        return
    print( "Output of command ", cproc.args )
    print( "stdout : \n" + cproc.stdout )
    print( "stderr : \n" + cproc.stderr )
    
    
def processPileupFiles():
    certifile_path,mtime = findLatestJson()
    print(certifile_path," with timestamp: ", datetime.fromtimestamp(mtime))
    if launchBrilcalc( certifile_path ):
        print("Launching makePileupJson")
        makePileupJson()
        print("Launching the plot job")
        makePileupPlots()

try:
    processPileupFiles()
except Exception as e:
    print("Something in this script went wrong: ", sys.exc_info()[0])

