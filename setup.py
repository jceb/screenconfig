#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import screenconfig

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="screenconfig",
    version="2018.10",
    author="Jan Christoph Ebersbach",
    author_email="jceb@e-jc.de",
    description="Tool automate the configuration of connected monitors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jceb/screensconfig",
    packages=setuptools.find_packages(),
    scripts=['screenconfig'],
    install_requires=['toml'],
    package_data={
        '': ['screenconfig.toml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: X11 Applications",
        "Operating System :: POSIX",
    ],
)
