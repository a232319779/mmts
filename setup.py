# -*- coding: utf-8 -*-
# @Time    :   2021/01/08 11:10:58
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   setup.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
import setuptools


def do_setup(**kwargs):
    try:
        setuptools.setup(**kwargs)
    except (SystemExit, Exception) as e:
        exit(1)

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md"), 'r', encoding='utf8') as f:
    long_description = f.read()

do_setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    author=about["__author__"],
    author_email=about["__email__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__uri__"],
    packages=setuptools.find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "mmts-decmd = mmts:deDos_main",
            "mmts-parselnk = mmts:parse_lnk_main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3',
    keywords=[],
    license="MIT",
    include_package_data=True,
    install_requires=[
    ],
)
