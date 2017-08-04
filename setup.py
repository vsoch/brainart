from setuptools import setup, find_packages
import codecs
import os

setup(
    # Application name:
    name="brainart",

    # Version number (initial):
    version="1.0.9",

    # Application author details:
    author="vsoch",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Data files
    package_data = {'brainart.templates':['*.html'],
                    'brainart.data':['*.pkl']},

    include_package_data=True,
    zip_safe=False,

    # Details
    url="http://www.github.com/vsoch/brainart",

    license="LICENSE",
    description="make images out of brain imaging data",
    keywords='brain art neuroimaging',

    install_requires = ['numpy','pandas','pyneurovault','nilearn','matplotlib','Pillow'],

    entry_points = {
        'console_scripts': [
            'brainart=brainart.scripts:main',
        ],
    },

)
