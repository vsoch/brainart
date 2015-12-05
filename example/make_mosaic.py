'''
BrainArt Mosaic

Example for complete database generation

'''

from brainart.db import get_data, save_lookup
from brainart.mosaic import generate
import shutil
import os

# If you use the command line tool, a mosaic will be generated using
# the database of online images. This script will show how that
# database was generated, and how you can make your own set

download_folder = "/home/vanessa/Documents/Work/NEUROVAULT/mosaic"

# black, white, greywhite, greyblack images go into [download_folder]/png
get_data(download_folder)

# For each, we will save a color lookup table to package
output_folder = "/home/vanessa/Documents/Dropbox/Code/Python/mosaic"
for bgcolor in ["black","white"]:
    png_images = glob("%s/png/*_%s.png" %(download_folder,bgcolor))
    output_file = "%s/brainart/data/%s_lookup.pkl" %(output_folder,bgcolor)
    save_lookup(png_images,output_file)

# Finally, we want to include these images in the package, so copy them to package
png_folder = "%s/png"%output_folder
shutil.copytree("%s/png"%download_folder,png_folder)

# Make an image from template
template = "/home/vanessa/Desktop/roman.jpg"
generate(template,color_lookup="black")
