#!/usr/bin/env python

"""
setuptools install script.
"""
from setuptools import setup, find_packages

from datacoco_secretsmanager import VERSION

requires = ["boto3==1.10.14"]

setup(
    name="datacoco-secretsmanager",
    version=VERSION,
    author="Equinox Fitness",
    description="AWS boto3 Secrets Manager wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
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
