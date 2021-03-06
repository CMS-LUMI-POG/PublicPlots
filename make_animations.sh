# Script for making animations from static images
# using ffmpeg: https://ffmpeg.org/
# thomas.mccauley@cern.ch

# For some reason the first two images have a different xaxis format
# which I actually would like to keep but it doesn't persist.
# For now, remove the first two images
rm -f images/lumi1.png
rm -f images/lumi2.png

# Make a webm video
ffmpeg -i $PWD/images/lumi%d.png -vb 20M $PWD/animations/lumi.webm

# Make an mp4
ffmpeg -r 20 -i $PWD/images/lumi%d.png -f mp4 -q:v 0 -vcodec mpeg4 -r 20 $PWD/animations/lumi.mp4

# Make a sped-up version (here, 4X faster)
ffmpeg -i $PWD/animations/lumi.mp4 -f mp4 -q:v 0 -vcodec mpeg4 -filter:v "setpts=0.25*PTS" $PWD/animations/lumi_4X.mp4

# Make an animated gif
ffmpeg -i $PWD/animations/lumi_4X.mp4  $PWD/animations/lumi_4X.gif
