from visci.app import generate_vis_index
from glob import glob
import os

base = os.path.abspath("../")
template_files = glob("%s/gallery/*.html" %base)
generate_vis_index(template_files,base)
