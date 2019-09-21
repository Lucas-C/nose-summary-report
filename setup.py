# -*- encoding: utf-8 -*-
import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


with open(join(dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='nose-summary-report',
    version='1.0.3',
    license = 'GNU LGPL',
    description='Nose plugin that generates a final summary of tests status as a table',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lucas Cimon',
    author_email='lucas.cimon+nose-summary-report@gmail.com',
    url='https://github.com/Lucas-C/nose-summary-report',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob.glob('src/*.py')],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    install_requires=[
        'nose',
    ],
    entry_points = {
        'nose.plugins.0.10': [
            'html = nose_summary_report:SummaryReporter'
        ]
    }
)
