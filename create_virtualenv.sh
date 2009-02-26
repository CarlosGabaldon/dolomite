#!/bin/bash
virtualenv dolomite-env
source dolomite-env/bin/activate
easy_install web.py
easy_install python-memcached
deactivate

wget -c http://github.com/cccarey/dolomite/raw/master/tools-ubuntu-8.10.tgz

tar xvf tools-ubuntu-8.10.tgz

rm tools-ubuntu-8.10.tgz


