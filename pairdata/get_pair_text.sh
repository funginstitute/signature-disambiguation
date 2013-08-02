#!/bin/bash

# USAGE: ./get_pair_text.sh <application number> <number of cores>
# downloads the PAIR data if it exists, then converts all the image file wrapper
# data to text if it exists

appnum=$1
numcores=$2

wget "http://storage.googleapis.com/uspto-pair/applications/$1.zip"

unzip "$1.zip"

cd $1/$1-image_file_wrapper

find . -name '*.pdf' | parallel -j$2 gs -q -dNO_PAUSE -sDEVICE=tiffg4 -sOutputFile={}.tif {} -c quit
find . -name '*.tif' | parallel -j$2 tesseract -l eng {} {}
