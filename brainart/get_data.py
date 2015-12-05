from pyneurovault import api
import numpy as np

all_collections = api.get_collections()
collections_with_dois = all_collections[np.logical_not(all_collections.DOI.isnull())]

images = api.get_images(collection_pks=list(collections_with_dois.collection_id))

# Remove images that are thresholded
images = api.filter(df=images,column_name="is_thresholded",field_value=False)

# Not in MNI
images = api.filter(df=images,column_name="not_mni",field_value=False)

# Just fMRI bold
images = api.filter(df=images,column_name="modality",field_value="fMRI-BOLD")

# Download all images to file, resample to target
outfolder = "/home/vanessa/Documents/Work/NEUROVAULT/mosaic"

# If you don't want to resample
api.download_images(dest_dir = outfolder,images_df=images,resample=False)
