#!/usr/bin/python

from nilearn.plotting import plot_stat_map
from brainart.utils import get_packagedir
from numpy.random import choice
import matplotlib.pyplot as plt
from pyneurovault import api
import numpy as np
from glob import glob
import pandas
import numpy as np
import nibabel
import os

base = get_packagedir()

def get_lookup(lookup_name):
    lookups = glob("%s/data/*.pkl" %base)
    lookup_names = [os.path.basename(x).split(".")[0].split("_")[0] for x in lookups]
    if lookup_name not in lookup_names:
        print "Invalid lookup name, choices are %s." %(",".join(lookup_names))
    else:
        return pandas.read_pickle("%s/data/%s_lookup.pkl" %(base,lookup_name))

def save_lookup(png_images,output_pkl):
    '''save_lookup
    save a color lookup table based on a set of images
    :param png_images: a list of full paths to png images to save
    :param output_pkl: the color lookup table will be saved to this pickle file
    '''
    lookup_table = get_color_lookup(png_images)
    lookup_table.to_pickle(output_pkl)


def get_data(download_folder):
    all_collections = api.get_collections()
    collections_with_dois = all_collections[np.logical_not(all_collections.DOI.isnull())]
    group_collections = collections_with_dois[collections_with_dois.group_comparison!=True]
    images = api.get_images(collection_pks=list(group_collections.collection_id))
    images = api.filter(df=images,column_name="is_thresholded",field_value=False)
    images = api.filter(df=images,column_name="not_mni",field_value=False)
    images = api.filter(df=images,column_name="modality",field_value="fMRI-BOLD")
    api.download_images(dest_dir = download_folder,images_df=images,resample=False)
    brainmaps = glob("%s/original/*.nii.gz" %(download_folder))
    output_folder = "%s/png" %(download_folder)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Let's use a crapton of colormaps
    colormaps = ["Spectral", "summer", "coolwarm", "Wistia_r", "pink_r", "Set1", "Set2", "Set3", "brg_r", "Dark2", "prism", "PuOr_r", "afmhot_r", "terrain_r", "PuBuGn_r", "RdPu", "gist_ncar_r", "gist_yarg_r", "Dark2_r", "YlGnBu", "RdYlBu", "hot_r", "gist_rainbow_r", "gist_stern", "PuBu_r", "cool_r", "cool", "gray", "copper_r", "Greens_r", "GnBu", "gist_ncar", "spring_r", "gist_rainbow", "gist_heat_r", "Wistia", "OrRd_r", "CMRmap", "bone", "gist_stern_r", "RdYlGn", "Pastel2_r", "spring", "terrain", "YlOrRd_r", "Set2_r", "winter_r", "PuBu", "RdGy_r", "spectral", "rainbow", "flag_r", "jet_r", "RdPu_r", "gist_yarg", "BuGn", "Paired_r", "hsv_r", "bwr", "cubehelix", "Greens", "PRGn", "gist_heat", "spectral_r", "Paired", "hsv", "Oranges_r", "prism_r", "Pastel2", "Pastel1_r", "Pastel1", "gray_r", "jet", "Spectral_r", "gnuplot2_r", "gist_earth", "YlGnBu_r", "copper", "gist_earth_r", "Set3_r", "OrRd", "gnuplot_r", "ocean_r", "brg", "gnuplot2", "PuRd_r", "bone_r", "BuPu", "Oranges", "RdYlGn_r", "PiYG", "CMRmap_r", "YlGn", "binary_r", "gist_gray_r", "Accent", "BuPu_r", "gist_gray", "flag", "bwr_r", "RdBu_r", "BrBG", "Reds", "Set1_r", "summer_r", "GnBu_r", "BrBG_r", "Reds_r", "RdGy", "PuRd", "Accent_r", "Blues", "autumn_r", "autumn", "cubehelix_r", "nipy_spectral_r", "ocean", "PRGn_r", "Greys_r", "pink", "binary", "winter", "gnuplot", "RdYlBu_r", "hot", "YlOrBr", "coolwarm_r", "rainbow_r", "Purples_r", "PiYG_r", "YlGn_r", "Blues_r", "YlOrBr_r", "seismic", "Purples", "seismic_r", "RdBu", "Greys", "BuGn_r", "YlOrRd", "PuOr", "PuBuGn", "nipy_spectral", "afmhot"]

    # We want an axial slice with different renderings (all the colors!)
    colormap_choices = colormaps[:]
    for brainmap in brainmaps:
        image_id = os.path.basename(brainmap).replace(".nii.gz","")
        mr = nibabel.load(brainmap)
        if len(colormap_choices)==0:
            colormap_choices = colormaps[:]
        color = colormap_choices.pop()
        # Save a black and a white version
        plot_stat_map(mr,display_mode="z",colorbar=False,annotate=False,draw_cross=False,cmap=color,cut_coords=1)
        plt.savefig("%s/%s_white.png" %(output_folder,image_id))
        plt.close()
        plot_stat_map(mr,display_mode="z",colorbar=False,annotate=False,draw_cross=False,cmap=color,cut_coords=1,black_bg=True)
        plt.savefig("%s/%s_black.png" %(output_folder,image_id),facecolor="k", edgecolor="k")
        plt.close()
        # Also generate for lots of grays
        image_id = os.path.basename(brainmap).replace(".nii.gz","")
        mr = nibabel.load(brainmap)
        plot_stat_map(mr,display_mode="z",colorbar=False,annotate=False,draw_cross=False,cmap="Greys",cut_coords=1)
        plt.savefig("%s/%s_greywhite.png" %(output_folder,image_id))
        plt.close()
        plot_stat_map(mr,display_mode="z",colorbar=False,annotate=False,draw_cross=False,cmap="Greys",cut_coords=1,black_bg=True)
        plt.savefig("%s/%s_greyblack.png" %(output_folder,image_id),facecolor="k", edgecolor="k")
        plt.close()
