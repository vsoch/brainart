# Brainart

Generate a rendering (made with brains) of an image of your choice.

### Installation

      pip install brainart


This will place an executable, 'brainart' in your system folder.


### Generate an image

      brainart --input /home/vanessa/Desktop/roman.jpg


It will open in your browser, and tell you the location of the output file, if you want to save it. 


### Color Lookup Tables
The default package comes with four color lookup tables, which are somewhat limited as they are generated from matplotlib color maps. (Contributions of skin tones would be greatly appreciated!) For an example of how to generate a set of image data for the package, see [examples/make_mosaic.py](examples/make_mosaic.py). The way to specify a color lookup table:

     brainart --input /home/vanessa/Desktop/roman.jpg --background-color greyblack

Where the options are `black` `white` `greyblack` and `greywhite`. For the last two, these are sets of grey images with black and white backgrounds, best suited for black and white.

### Similarity Threshold
By default, the similarity threshold is 0.9, meaning that a random image is selected from the lookup with average color of the brain above the threshold in that similarity (pearson's R). If you want to adjust that value:

      brainart --input /home/vanessa/Desktop/roman.jpg --threshold 0.8

as in the case that the result set is empty (meaning the lookup does not have a good color match) a random image is selected, and this can reduce the quality of your result.


### Under Development
Currently, works best for colorful images (unfortunately this does not include faces) as the color maps are pulled directly from matplotlib. And we know what can be found there! We need to add color maps for skin tones, etc, and faces will be better rendered.

Image generation is very slow, based on sampling every 5th pixel. Not yet streamlined or converted to some kind of app, but the functions will work! :)
