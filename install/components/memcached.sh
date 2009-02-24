#!/bin/bash

function die()
{
    echo $*
    exit 1
}

function checkRoot()
{
    if [ ! $( id -u ) -eq 0 ]; then
        die "Must have super-user rights to run this script.  Run with the command 'sudo $0'"
    fi
}

function installPackages()
{
    for package in "$@"; do
        if [ -z "`dpkg -l |grep $package`" ]; then
            packages="$packages $package"
        fi
    done
    if [ ! -z "$packages" ]; then
        apt-get install -y --force-yes $packages
        if [ ! $? -eq 0 ]; then
            die "Script encountered an error during package installation.  Check errors and retry."
        fi
    fi
}

# ----------
# Main script
# ----------

checkRoot

installPackages wget libevent1 libevent-dev

wget -c http://www.danga.com/memcached/dist/memcached-1.2.6.tar.gz

echo -n "Extracting memcached tar ball..."
tar xfz memcached-1.2.6.tar.gz
if [ ! $? -eq 0 ]; then
    die "Unable to extract memcached.  Check errors and retry."
fi
echo

chmod 755 memcached-1.2.6
cd memcached-1.2.6
./configure
if [ ! $? -eq 0 ]; then
    die "Configuration of memcached was not successful.  Check errors for additional packages not installed by the script and try again."
fi

make
if [ ! $? -eq 0 ]; then
    die "Make of memcached was not successful.  Cannot continue."
fi

make install

