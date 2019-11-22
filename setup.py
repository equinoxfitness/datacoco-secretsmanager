#!/usr/bin/env python

"""
setuptools install script.
"""
import os
import re
from setuptools import setup, find_packages

requires = ["boto3==1.10.14"]


def get_version():
    version_file = open(
        os.path.join("datacoco_secretsmanager", "__version__.py")
    )
    version_contents = version_file.read()
    return re.search('__version__ = "(.*?)"', version_contents).group(1)


setup(
    name="datacoco-secretsmanager",
    version=get_version(),
    author="Equinox Fitness",
    description="AWS boto3 Secrets Manager wrapper",
    long_description=open("README.rst").read(),
    url="https://github.com/equinoxfitness/datacoco-secretsmanager",
    scripts=[],
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
