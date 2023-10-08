#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='ina229',
    version='0.0.0.dev0',
    description='A Python driver for Texas Instruments INA229 85-V, 20-Bit, '
                'Ultra-Precise Power/Energy/Charge Monitor With SPI Interface',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/blueskysolarracing/ina229',
    author='Blue Sky Solar Racing',
    author_email='blueskysolar@studentorg.utoronto.ca',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords=['python', 'ina229', 'ti', 'texas instruments'],
    project_urls={
        'Documentation': 'https://ina229.readthedocs.io/en/latest/',
        'Source': 'https://github.com/blueskysolarracing/ina229',
        'Tracker': 'https://github.com/blueskysolarracing/ina229/issues',
    },
    packages=find_packages(),
    install_requires=['python-periphery>=2.4.0,<3']
    python_requires='>=3.11',
    package_data={'ina229': ['py.typed']},
)
