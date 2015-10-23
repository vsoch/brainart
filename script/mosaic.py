#!/usr/bin/python

import numpy as np
from numpy.random import choice
from PIL import Image


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


def get_color_lookup(png_images):
    """
    get_color_lookup:
      returns pandas data frame with average color of an image
      columns are "R" "G" "B" and rows are image paths
    """
    color_lookup = pandas.DataFrame(columns=["R","G","B"])
    for png_image in png_images:
        valid,R,G,B = get_avg_rgb(png_image)
        if valid:
            color_lookup.loc[png_image] = [R,G,B]
    return color_lookup


def generate_matching_df(template,color_lookup,threshold=0.9):
    """
     generate_matching_df (worst function name ever)
        this will generate a dataframe with x,y, corr, and png file path
        for images that most highly  
    """
    # Now read in our actual image
    base = Image.open(template)
    width, height = base.size
    pixels = base.load()
    data = []

    count=0
    for x in range(width):
        for y in range(height):
            # And take only every 5th pixel
            if np.remainder(x,5)==0 and np.remainder(y,5)==0:
                cpixel = pixels[x, y]
                # Make a temporary data frame with cpixel appended
                tmp = color_lookup.copy()
                tmp.loc["lookup"] = cpixel[0:3]
                # Calculate pairwise correlations
                corrs = tmp.transpose().corr()
                scores = corrs.loc["lookup"]
                scores = scores.drop(["lookup"])
                scores = scores[scores.isnull()==False]
                scores.sort(ascending=False)
                # Randomly sample from anything > 0.9
                png = choice(scores[scores>threshold].index.tolist(),1)[0]
                new_image.loc[count] = [x,y,scores[png],png]
                count+=1
    return new_image

