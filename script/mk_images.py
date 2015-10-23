#!/usr/bin/python

from nilearn.plotting import plot_stat_map
from numpy.random import choice
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import nibabel
import os

input_folder = "/home/vanessa/Documents/Work/NEUROVAULT/mosaic"

# Read in each brain map
brainmaps = glob("%s/original/*.nii.gz" %(input_folder))
output_folder = "%s/png" %(input_folder)

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Let's use a crapton of colormaps
cmaps = [('Sequential',     ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
         ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool', 'copper',
                             'gist_heat', 'gray', 'hot', 'pink',
                             'spring', 'summer', 'winter']),
         ('Diverging',      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic']),
         ('Qualitative',    ['Accent', 'Dark2', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3']),
         ('Miscellaneous',  ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                             'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'gist_ncar',
                             'nipy_spectral', 'jet', 'rainbow',
                             'gist_rainbow', 'hsv', 'flag', 'prism'])]

# Flatten into a single vector
colormaps = []
for category in cmaps:
    colormaps = colormaps + category[1]

# We want an axial slice with different renderings (all the colors!)
for brainmap in brainmaps:
    image_id = os.path.basename(brainmap).replace(".nii.gz","")
    mr = nibabel.load(brainmap)
    # Randomly choose a color
    color = choice(colormaps,size=1)[0]
    # Save a black and a white version
    plot_stat_map(mr,display_mode="z",colorbar=False,annotate=False,draw_cross=False,cmap=color,cut_coords=1)
    plt.savefig("%s/%s_white.png" %(output_folder,image_id))
    plt.close()
    plot_stat_map(mr,display_mode="z",colorbar=False,annotate=False,draw_cross=False,cmap=color,cut_coords=1,black_bg=True)
    plt.savefig("%s/%s_black.png" %(output_folder,image_id),facecolor="k", edgecolor="k")
    plt.close()
