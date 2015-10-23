#!/usr/bin/python

from mosaic import get_avg_rgb, get_color_lookup, generate_matching_df
from glob import glob
import numpy as np
import pandas
import sys

input_folder = sys.argv[1]
template = sys.argv[2]
output_folder = sys.argv[3]
#input_folder = "/home/vanessa/Documents/Work/NEUROVAULT/mosaic"

# Read in png images
black_png_images = glob("%s/png/*_black.png" %(input_folder))
white_png_images = glob("%s/png/*_white.png" %(input_folder))

# Template image
#template = "%s/template/LectinFISH560.jpg" %(input_folder)

# Get color lookups for white and black images
print "Generating color lookup tables"
lookup_black = get_color_lookup(black_png_images)
lookup_white = get_color_lookup(white_png_images)

print "Generating black image..."
new_black = generate_matching_df(template,lookup_black)
print "Generating white image..."
new_white = generate_matching_df(template,lookup_white)

# Make paths relative to image folder, so we can move into output directory
new_white.png = ["%s/%s" %(x.split("/")[-2],x.split("/")[-1]) for x in new_white.png]
new_black.png = ["%s/%s" %(x.split("/")[-2],x.split("/")[-1]) for x in new_black.png]

# Save data to file
new_black.to_csv("%s/data_black.tsv" %(output_folder),sep="\t",index=None)
new_white.to_csv("%s/data_white.tsv" %(output_folder),sep="\t",index=None)
