from setuptools import setup

with open("veptools/_version.py") as f:
    version = f.read().split('"')[1]

setup(
    version=version,
)
