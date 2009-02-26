#!/bin/bash
virtualenv dolomite-env
source dolomite-env/bin/activate
easy_install web.py
easy_install python-memcached
deactivate

wget -c http://cloud.github.com/downloads/cccarey/dolomite/tools-ubuntu-8.10.tgz

tar xvf tools-ubuntu-8.10.tgz

