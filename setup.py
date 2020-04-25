# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(name="kafka-python",
      version="0.0.1",
      description="A package that demonstrates kafka producer and consumer",
      license="MIT",
      author="Sahil Kabra",
      packages=find_packages(),
      install_requires=[],
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.8",
      ])
