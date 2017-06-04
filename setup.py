#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from croncoat import __version__

#following PyPI guide: https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(name='croncoat',
    version = __version__,
    author="Matthias Kauer",
    author_email="mk.software@zuez.org",
    url="https://github.com/MatthiasKauer/croncoat",
    classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: BSD License",
    "Operating System :: Unix",
    "Programming Language :: Python",
    ],

    install_requires=[
      'argparse>=1.1',
      'subprocess32>=3.2.7',
    ],
    packages = find_packages(),

    entry_points={'console_scripts': ['croncoat=croncoat.scripts.ccscript:main']},
    platforms=["Unix"],
    license="BSD",
    keywords='cron wrapper crontab cronjob email',
    description="croncoat extends cronwrap, a cron job wrapper that wraps jobs and enables better error reporting and command timeouts.",
    long_description=read('README.md'),
)
