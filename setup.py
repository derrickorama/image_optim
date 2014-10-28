# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ImageOptim',
    version='0.3.0',
    description='Python bindings for image_optim (https://github.com/toy/image_optim)',
    long_description=readme,
    author='Derrick Gall',
    author_email='derrickorama@gmail.com',
    url='http://derrickorama.com',
    license=license,
    packages=find_packages(exclude=('tests'))
)
