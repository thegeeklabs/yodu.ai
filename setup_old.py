import site
import sys
import time
from os import environ
from pathlib import Path

import setuptools
from setuptools import setup, find_packages

# workround for enabling editable user pip installs
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

# version
here = Path(__file__).absolute().parent
version_data = {}
with open(here.joinpath("yodu", "__init__.py"), "r") as f:
    exec(f.read(), version_data)
version = version_data.get("__version__", "0.0")
print("Here")
print(version)

# Get the long description from the README file
with open(here.joinpath("README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

HASH = environ.get("HASH", None)
if HASH is not None:
    version += ".post" + str(int(time.time()))

install_requires = [
    "pydantic",
    "typing",
    "requests",
    "pytest",
    "elasticsearch",
    "influxdb-client",
    "python-dotenv",
    "ijson==3.1.4",
]

setup(
    name="yodu",
    version="0.0.1",
    author="Shashank Agarwal",
    author_email="shashank@thegeeklabs.com",
    description="Generic Purpose Open Source Recommender System",
    license="Apache 2.0",
    keywords="recommendations recommendation recommenders recommender system engine "
    "machine learning python spark gpu",
    url="https://github.com/thegeeklabs/yodu.ai",
    package_data={"": ["*.py", "*.json", "*.pk", "*.js", "*.zip"]},
    python_requires=">=3.0, <3.10",
    packages=setuptools.find_packages(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://github.com/thegeeklabs/yodu.ai/tree/dev/docs/",
        "Wiki": "https://github.com/thegeeklabs/yodu.ai/tree/dev/docs/",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)
