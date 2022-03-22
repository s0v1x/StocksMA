import configparser
from pathlib import Path
from typing import List

import setuptools

config = configparser.ConfigParser()
config.read("Pipfile")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / "requirements"

keywords = [
    "pandas",
    "stocks",
    "finance",
    "morocco",
    "ma",
    "yahoo finance",
    "marketwatch",
    "wsj",
    "data",
    "timeseries",
]


setuptools.setup(
    name="StocksMA",
    version="0.1.0",
    author="sovix",
    author_email="sed.labiad@gmail.com",
    description="Retrieve data related to Moroccan stocks from diffrent sources",
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
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires=">=3.6",
    install_requires=list(dict(config.items("packages")).keys()),
    extras_require={},
    include_package_data=True,
    license="MIT",
    keywords=", ".join(keywords),
)
