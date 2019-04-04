'''
This script reads in the lumiByDay.csv file
and generates a png for each day. These pngs are 
then stitched together with ffmpeg to create videos 
and animated gifs.

to-do:

* This script started as a stand-alone; it should use styling code already included in
  PublicPlots
* Changes to the styling to conform to static plot style
* Generalize so that any range of dates can be specified 
* Add CMS logo
* Why is xaxis style different for first two images?
* Perhaps use matplotlib plot directly rather than via pandas dataframe?
  This might be the source of some of the plotting problems above.

thomas.mccauley@cern.ch
'''

import sys
import os

import pandas as pd
import matplotlib

from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import matplotlib.pyplot as plt

# Make images and videos dirs
try:
    print('Creating directory ./images')
    os.mkdir('./images')
except FileExistsError:
    print('The directory ./images already exists. Continuing.')

try:
    print('Creating directory ./animations')
    os.mkdir('./animations')
except FileExistsError:
    print('The directory ./animations already exists. Continuing.')

# Read in the lumiByDay csv into a pandas DataFrame and
# add a Date column for manipulation
try:
    lumi = pd.read_csv('lumiByDay.csv') # https://cern.ch/cmslumi/publicplots/lumiByDay.csv
except FileNotFoundError:
    print('Please download lumiByDay.csv from here: https://cern.ch/cmslumi/publicplots/lumiByDay.csv')
    sys.exit()

lumi['Date'] = pd.to_datetime(lumi.Date)

min_date = pd.Timestamp(year=2015, month=6, day=3)
max_date = pd.Timestamp(year=2018, month=10, day=26)

# Select our DataFrame over the data range
lumi = lumi[(lumi.Date <= max_date) & (lumi.Date >= min_date)]

# Add columns for cumulative luminosity
lumi['CMS recorded'] = lumi['Recorded(/ub)'].cumsum() / 1e9
lumi['LHC delivered'] = lumi['Delivered(/ub)'].cumsum() / 1e9
#print(lumi.head())

# The styling below should come from a PublicPlots library
cms_orange= (0.945, 0.76, 0.157)
cms_blue = (0.0, 0.596, 0.831)

FONT_PROPS_SUPTITLE = FontProperties(size="x-large", weight="bold", stretch="condensed")
FONT_PROPS_TITLE = FontProperties(size="large", weight="regular")
FONT_PROPS_AX_TITLE = FontProperties(size="x-large", weight="bold")
FONT_PROPS_TICK_LABEL = FontProperties(size="large", weight="bold")
DATE_FMT_STR_AXES = "%-d %b"

matplotlib.rcParams["font.size"] = 10.8 
matplotlib.rcParams["axes.labelweight"] = "bold"

# Now interate through the days over our range and make a plot for each entry in ./images
print('Creating', len(lumi)-2, 'images in ./images')

for i in range(2,len(lumi)):
    
    axes = lumi[1:i].plot(x='Date', y=['LHC delivered', 'CMS recorded'], 
                          kind='area', stacked=False, figsize=(12*0.75,9*0.75), 
                          color=[cms_blue, cms_orange], alpha=1.0)
    
    axes.tick_params(axis='y', which='both', labelright=True)
    
    '''
    The styling here seems to change over the production of pngs so 
    do not use for now.

    ylocs, ylabels = plt.yticks() 
    for label in ylabels:
        label.set_font_properties(FONT_PROPS_TICK_LABEL)
        
    xlocs, xlabels = plt.xticks() 
    for label in xlabels:
        label.set_font_properties(FONT_PROPS_TICK_LABEL)
    '''
    
    lumi_delivered = '{0:.2f}'.format(lumi[1:i]['LHC delivered'].values[-1])
    lumi_recorded = '{0:.2f}'.format(lumi[1:i]['CMS recorded'].values[-1])
    
    plt.suptitle('CMS Integrated Luminosity, pp, $\mathrm{\sqrt{s} =}$ 13 TeV', fontproperties=FONT_PROPS_SUPTITLE)
    plt.title('Data included from 2015-06-03 to 2018-10-26', fontproperties=FONT_PROPS_TITLE)

    plt.ylim(0, 180)
    plt.ylabel('Total Integrated Luminosity ($\mathrm{{fb}^{-1}}$)', fontproperties=FONT_PROPS_AX_TITLE)

    plt.xlim(min_date, max_date)
    plt.xlabel('Date', fontproperties=FONT_PROPS_AX_TITLE)
    
    cms_square = mlines.Line2D([], [], color=cms_orange, 
                               label='CMS Recorded: '+lumi_recorded+' ($\mathrm{{fb}^{-1}}$)',
                               marker='s', linestyle='None', markersize=10)
    
    lhc_square = mlines.Line2D([], [], color=cms_blue, 
                               label='LHC Delivered: '+lumi_delivered+' ($\mathrm{{fb}^{-1}}$)',
                               marker='s', linestyle='None', markersize=10)
    
    plt.legend(handles=[lhc_square, cms_square],
               loc=2, frameon=False, 
               prop={'weight':'bold', 'size':'large'})
    
    if (i-1) % 10 == 0:
        print((i-1), 'images created')

    plt.savefig('./images/lumi'+str(i-1)+'.png')
    plt.close()

print('Done. Now run make_animations.sh')

