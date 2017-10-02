# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ev3-controller',
    version='0.1.0',
    description='Controlling ev3 legos',
    long_description=readme,
    author='Jaakko Suutarla',
    author_email='jaakko@suutarla.com',
    url='https://github.com/jaakkos/ev3-controller',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

