import setuptools
from setuptools import find_packages, setup
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'


def list_reqs(fname="requirements.txt"):
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().splitlines()

setuptools.setup(
    name="StocksMA",
    version="0.0.1",
    author="sovix",
    author_email="sed.labiad@gmail.com",
    description="Retrieve data related to moroccan stocks from diffrent sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s0v1x/StocksMA",
    project_urls={
        "Bug Tracker": "https://github.com/s0v1x/StocksMA/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "StocksMA"},
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.6",
    extras_require={},
    include_package_data=True,
    license='MIT',
    keywords="pandas, stocks, finance, morocco, ma, yahoo finance, marketwatch, wsj, data, timeseries",
    
)