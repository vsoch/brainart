'''
BrainArt Mosaic

Example for complete database generation

'''

from brainart.db import get_data, save_lookup
from brainart.utils import get_color_lookup
from brainart.mosaic import generate
import shutil
import os
import re

# If you use the command line tool, a mosaic will be generated using
# the database of online images. This script will show how that
# database was generated, and how you can make your own set

download_folder = "/home/vanessa/Documents/Work/NEUROVAULT/mosaic"
png_folder = "%s/png" %(download_folder)
if not os.path.exists(png_folder):
    os.mkdir(png_folder)

# Download NeuroVault collections, non thresholded, MNI, with DOI, group maps
brainmaps = get_data(download_folder)

# For each of the below, images with black backgrounds and white bgs are produced

# brains with multiple colors from matplotlib color maps
png_colormaps = make_colormap_brains(brainmaps,png_folder)

# Single brains (using 500+ hex colors) - this function returns the table
lookup_table_hex = make_hexcolor_brains(brainmaps,png_folder)

# Split into black and white
lookups = dict()
exp = re.compile("white")
white_index = [x for x in lookup_table_hex.index.tolist() if exp.search(x)]
black_index = [x for x in lookup_table_hex.index.tolist() if not exp.search(x)]
lookups["white"] = lookup_table_hex.loc[white_index]
lookups["black"] = lookup_table_hex.loc[black_index]

# For each, we will save a color lookup table to package
output_folder = "/home/vanessa/Documents/Dropbox/Code/Python/mosaic"
for bgcolor,lookup_table in lookups.iteritems():

    # We already have single colors, just need to add colormap versions
    png_images = [x for x in png_colormaps if re.search(bgcolor,x)]
    lookup_table_spectrum = get_color_lookup(png_images)    

    # Add the tables
    merged_lookup = lookup_table_spectrum.append(lookup_table)
    output_file = "%s/brainart/data/%s_lookup.pkl" %(output_folder,bgcolor)
    save_lookup(merged_lookup,output_file)

# Finally, we want to include these images in the package, so copy them to package
png_folder = "%s/png"%output_folder
shutil.copytree("%s/png"%download_folder,png_folder)

# Make an image from template
template = "/home/vanessa/Desktop/roman.jpg"
generate(template,color_lookup="black")
