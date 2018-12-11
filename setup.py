#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pardal",
    version="0.1.0",
    author="Ana Paula Gomes",
    author_email="apgomes88@gmail.com",
    maintainer="Ana Paula Gomes",
    maintainer_email="apgomes88@gmail.com",
    license="MIT",
    url="https://github.com/anapaulagomes/pardal",
    description="An accessible and customizable Twitter client",
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.7",
    install_requires=[""],  # FIXME
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Adaptive Technologies",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={},
)
