#!/usr/bin/python

import numpy as np
from numpy.random import choice
from PIL import Image
import pandas
import os
import brainart.hello as hello

def get_packagedir():
    return os.path.dirname(hello.__file__)

def get_avg_rgb(png_image):
    """
    get_avg_rgb:
        returns a tuple with (True/False,R,G,B)
        True/False indicates if the image is not empty
        the R G B are red, green, blue values, respectively
    """

    img = Image.open(png_image)
    width, height = img.size

    # make a list of all pixels in the image
    pixels = img.load()
    data = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            data.append(cpixel)

    r = 0
    g = 0
    b = 0
    counter = 0

    # loop through all pixels
    # if alpha value is greater than 200/255, add it to the average
    for x in range(len(data)):
        if (data[x][3] > 200):
            if not (data[x][0] == 0 and data[x][1] == 0 and data[x][2] == 0):
                # Don't count white, black is 0 so we don't care
                if not (data[x][0] == 255 and data[x][1] == 255 and data[x][2] == 255):
                    r+=data[x][0]
                    g+=data[x][1]
                    b+=data[x][2]
                    counter+=1;

    # compute average RGB values
    if counter != 0:
        rAvg = r/counter
        gAvg = g/counter
        bAvg = b/counter
        return (True,rAvg, gAvg, bAvg)
    else:
        return (False,0,0,0)


def get_color_lookup(png_images,remove_path=True):
    '''get_color_lookup
    returns pandas data frame with average color of an image. Columns are "R" "G" "B" and rows are image paths
    :param png_images: full paths to png images to include
    :param remove_path: if True, will return table with image names only (default is True)
    '''
    color_lookup = pandas.DataFrame(columns=["R","G","B"])
    for png_image in png_images:
        valid,R,G,B = get_avg_rgb(png_image)
        if valid:
            if remove_path == True:
                png_image = os.path.basename(png_image)
            color_lookup.loc[png_image] = [R,G,B]
    return color_lookup


def generate_matching_df(template,color_lookup,top=20,sample=15):
    '''generate_matching_df (worst function name ever)
    this will generate a dataframe with x,y, corr, and png file path for images that most highly match each sampled pixel. The df gets parsed to json that plugs into d3 grid 
    '''
    # Now read in our actual image
    base = Image.open(template)
    width, height = base.size
    pixels = base.load()
    data = []

    count=0
    new_image = pandas.DataFrame(columns=["x","y","corr","png"])

    for x in range(width):
        for y in range(height):
            # And take only every [sample]th pixel
            if np.remainder(x,sample)==0 and np.remainder(y,sample)==0:
                cpixel = pixels[x, y]
                tmp = color_lookup.copy()
                tmp = (tmp-cpixel).abs().sum(axis=1)
                tmp.sort()
                png = choice(tmp.loc[tmp.index[0:top]].index.tolist(),1)[0]
                new_image.loc[count] = [x,y,0,png]
                count+=1

    new_image["x"] = [int(x) for x in (new_image["x"] / sample) * 10]
    new_image["y"] = [int(x) for x in (new_image["y"] / sample) * 10]
    
    return new_image
