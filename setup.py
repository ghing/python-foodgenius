import os.path
from setuptools import setup, find_packages

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="foodgenius",
    version="0.1",
    description="A simple library for consuming Food Genius' REST API",
    long_description=open(os.path.join(base_dir, "README.rst"), "r").read(),
    url="http://getfoodgenius.com/api/",
    packages=find_packages(),
    install_requires=['slumber']
)
