# Brainart

[gallery](http://vsoch.github.io/brainart)

What do you get when you combine open source brainmaps with art? Why, BrainArt of course! Generate a rendering (made with brains) of an image of your choice using images from the [NeuroVault](http://www.neurovault.org) database! After generation of your image, clicking on any of the tiny brains will take you to the brain statistical map. Current image lookup tables are optimized for highly colorful images, either with black or white background. You can generate your own brain images on your computer, and contribute to our gallery!

### Installation

      pip install brainart


This will place an executable, 'brainart' in your system folder.


      usage: brainart [-h] --input IMAGE [--db DB] [--threshold THRESHOLD]
                      [--update] [--background-color BGCOLOR]
                      [--color-lookup LOOKUP] [--output-folder OUTPUT]

      make images out of brain imaging data

      optional arguments:
         -h, --help            show this help message and exit
         --input IMAGE         full path to jpg image
         --db DB               path to folder for png images for database
         --threshold THRESHOLD
                               threshold value to match pixels to brain images
         --update              regenerate png database
         --background-color BGCOLOR
                               background color
         --color-lookup LOOKUP
                               color lookup (white, black, greyblack, greywhite)
         --output-folder OUTPUT
                               output folder for html file


### Generate an image

      brainart --input /home/vanessa/Desktop/flower.jpg

It will open in your browser, and tell you the location of the output file, if you want to save it. 


### Color Lookup Tables
The default package comes with two lookup tables, each of which are somewhat limited as they are generated from matplotlib color maps. (Contributions of skin tones would be greatly appreciated!) For an example of how to generate a set of image data for the package, see [example/make_mosaic.py](example/make_mosaic.py). Currently, choice of a color lookup table just means choosing a black or white background. The way to specify this:


     brainart --input /home/vanessa/Desktop/roman.jpg --color-lookup black

Where the options are `black` `white`. I should probably make an option for black and white images, but I haven't done that yet.


### Similarity Threshold
By default, the similarity threshold is 0.9, meaning that a random image is selected from the lookup with average color of the brain above the threshold in that similarity (pearson's R). If you want to adjust that value:


      brainart --input /home/vanessa/Desktop/roman.jpg --threshold 0.8


as in the case that the result set is empty (meaning the lookup does not have a good color match) a random image is selected, and this can reduce the quality of your result.


### Gallery
The [gallery](http://vsoch.github.io/brainart) is the index file hosted on the github pages for this repo. To submit a file to it, you can clone this repo:

      git clone https://www.github.com/vsoch/brainart

Check out the gh-pages branch

      git checkout -b gh-pages
      git pull origin gh-pages

Add your file to the folder called "gallery" and then regenerate the static index.html like so. You will need to install my visci package to quickly generate the template:


      cd scripts  #!important
      pip install visci
      python generate_gallery.py


This will update the `index.html` in the main folder, which renders on github pages. Now just submit the PR, and you're done! You can also email directly to me, if you are not comfortable with github. Submissions are greatly appreciated, and fun :)


### Under Development
Currently, works best for colorful images (unfortunately this does not include faces) as the color maps are pulled directly from matplotlib. And we know what can be found there! We need to add color maps for skin tones, etc, and faces will be better rendered.

Image generation is slow, based on sampling every 10th pixel. If you change the sample rate, you may need to alter the d3 to change the spacing between the brains. It would be optimal to generate the x,y coordinates in the python to best render for the sampling rate. It would also be desired to have a faster generation of the image. Please contribute! :_)
