#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/08/04 12:49
Desc: Yodu.ai  A General purpose Open Source Recommendation Engine
"""
import ast
import re

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_version_string() -> str:
    """
    Get Yodu.ai version number
    :return: version number
    :rtype: str, e.g. '0.6.24'
    """
    with open("yodu/__init__.py", "rb") as _f:
        version_line = re.search(
            r"__version__\s+=\s+(.*)", _f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


setuptools.setup(
    name="yodu",
    version=get_version_string(),
    author="Shashank Agarwal",
    author_email="shashank@thegeeklabs.com",
    description="Generic Purpose Open Source Recommender System",
    license="Apache 2.0",
    keywords=[
        "recommendations",
        "recommendation",
        "recommenders",
        "recommender",
        "system",
        "engine",
        "machine learning",
        "python",
        "AI",
        "ML",
    ],
    url="https://github.com/thegeeklabs/yodu.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydantic",
        "typing",
        "requests",
        "elasticsearch",
        "python-dotenv",
        "ijson",
    ],
    package_data={"": ["*.py", "*.json", "*.pk", "*.js", "*.zip"]},
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
    python_requires=">=3.7",
)
