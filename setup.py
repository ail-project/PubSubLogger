#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='PubSubLogger',
    version='0.1',
    author='Raphaël Vinot',
    author_email='raphael.vinot@gmail.com',
    url='https://github.com/Rafiot/PubSubLogger.git',
    packages=['pubsublogger'],
    scripts = ['log_subscriber'],
    license='Do What The Fuck You Want To Public License',
    long_description=open('README.md').read(),
    )
