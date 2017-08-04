#!/usr/bin/python

from brainart.utils import get_avg_rgb, get_color_lookup, generate_matching_df, get_packagedir
from brainart.template import get_template, sub_template, save_template
from glob import glob
import numpy as np
import webbrowser
import tempfile
import pandas
import json
import sys
import os

base = get_packagedir() 

def generate(template,output_folder=None,color_lookup="white",image_base_path=None,bgcolor="black",top=20,sample=10):
    '''generate
    create a brainart image using a particular color lookup table
    :param template: the template image to generate brainart for! Only jpg has been tested.
    :param output_folder: output folder for the final file. If not specified, will use TMP
    :param color_lookup: one of "white" "black" "greywhite" or "greyblack" will default to using brainart database, and you do not need to worry about setting image_base_path. If you set this to a custom lookup table (should be a pandas dataframe) then you also need to set image_base_path to be the directory with images defined in your lookup table index. Default color lookup is white.
    :param image_base_path: Only specify if you provide a custom color lookup pandas. Default is None, as the base path is the github repo images. 
    :param top: The number of top matches to sample from. Smaller values mean less variation in brains and color. Higher values means possibly more variation in color, and more brains.
    :param bgcolor: background color (string or hex) for the output html page. Default is black, and will be matched to color lookup if one is provided.
    :param sample: how many pixels to sample from. Default is every 5th pixel (5). Larger numbers mean generating images faster.
    '''
    if output_folder == None:
        output_folder = tempfile.mkdtemp()

    if isinstance(color_lookup,pandas.DataFrame):
        print("Custom color lookup found!")
        if image_base_path == None:
            print("Error: color lookup is set to custom file but image_base_path is set to 'None.' If you want to use images for a custom table you have created, you need to provide a base path to those images.")
            sys.exit()
    elif color_lookup not in ["white","black"]:
        print("Error: package color lookup tables include 'white','black','greywhite' and 'greyblack'")
        sys.exit()
    else:
        # Background color of html page should be black in all cases except for white lookup
        if color_lookup == "white":
            bgcolor = "white"        
        color_lookup = pandas.read_pickle("%s/data/%s_lookup.pkl" %(base,color_lookup))
        image_base_path = "https://rawgithub.com/vsoch/brainart/master/png"

    print("Generating image... this can take a few minutes.")
    new_image = generate_matching_df(template,color_lookup,top=top,sample=sample)

    # Make paths relative to image_base_path
    new_image.png = ["%s/%s" %(image_base_path,x) for x in new_image.png]

    # Get image template
    html_template = get_template("index")
    image_name = os.path.splitext(os.path.basename(template))[0]

    # Save output to file
    new_image_dict = new_image.to_dict(orient="records")
    result = {"image":new_image_dict,"bgcolor":bgcolor}
    html_template = sub_template(html_template,"DATA",str(result))
    output_html = "%s/index.html" %output_folder
    save_template(output_html,html_template)
        
    print("Result files being saved to %s" %output_folder)
    webbrowser.open_new_tab(output_html)

