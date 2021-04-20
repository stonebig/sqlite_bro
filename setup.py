# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
from setuptools import find_packages, setup, Extension


def get_version():
    with open(os.path.join('sqlite_bro','sqlite_bro.py')) as f:
        for line in f:
            if line.strip().startswith('self.__version__'):
                return eval(line.split('=')[-1])

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='sqlite_bro',
    version=get_version(),
    description="a graphic SQLite Client in 1 Python file",

    long_description=(read('README.rst')),
    keywords=['sqlite', 'gui', 'ttk', 'sql'],
    author='stonebig',
    author_email='write_pull_requests_to_stonebig@github.com',
    url='https://github.com/stonebig/sqlite_bro',
    license='MIT license',
    #py_modules=['sqlite_bro'],
    packages=['sqlite_bro', 'sqlite_bro.tests'],
    # package_dir={"sqlite_bro": "sqlite_bro"},
    # namespace_packages=[],
    include_package_data=True,
    # zip_safe=False,
    # install_requires=[],
    entry_points={
        'console_scripts': [
            'sqlite_bro = sqlite_bro.sqlite_bro:_main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ]
)
