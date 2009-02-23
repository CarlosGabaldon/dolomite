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

installPackages wget db4.7-util libdb4.7-dev libevent1 libevent-dev

wget -c http://memcachedb.googlecode.com/files/memcachedb-1.2.0.tar.gz

echo -n "Extracting memcachedb tar ball..."
tar xfz memcachedb-1.2.0.tar.gz
if [ ! $? -eq 0 ]; then
    die "Unable to extract memcachedb.  Check errors and retry."
fi
echo

cd memcachedb
./configure --enable-threads
if [ ! $? -eq 0 ]; then
    die "Configuration of memcachedb was not successful.  Check errors for additional packages not installed by the script and try again."
fi

make
if [ ! $? -eq 0 ]; then
    die "Make of memcachedb was not successful.  Cannot continue."
fi

make install

