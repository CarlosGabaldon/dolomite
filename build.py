#!/usr/bin/env python
import os, sys, tarfile, shutil
import subprocess as proc
import warnings

warnings.filterwarnings('ignore','.*apt API not stable yet.*')

import apt

def dependenciesMet(packages):
    met = True
    cache = apt.Cache()
    for package in packages:
        pkg = cache[package]
        if not pkg.isInstalled:
            print("%s package is not installed." % package)
            met = False
    return met
    
def main():
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('build'):
        os.mkdir('build')
    if not os.path.exists('build/bin'):
        os.mkdir('build/bin')
    os.chdir('tmp')

    print("checking build depedencies...")
    if not dependenciesMet(['libevent1','libevent-dev']):
        print("install dependencies and try again")
        sys.exit(1)
        
    print("downloading source...")
    try:
        proc.check_call(['wget','-c', 'http://www.danga.com/memcached/dist/memcached-1.2.6.tar.gz'])
    except proc.CalledProcessError:
        sys.exit(1)

    print("extracting tar ball...")    
    memcached = tarfile.open(name='memcached-1.2.6.tar.gz', mode='r:gz')
    memcached.extractall()
    
    print("configuring...")
    os.chdir('memcached-1.2.6')
    try:
        proc.check_call(['./configure'])
    except proc.CalledProcessError:
        sys.exit(1)
        
    print("building...")
    try:
        proc.check_call(['make'])
    except proc.CalledProcessError:
        sys.exit(1)

    print("copying built files...")
    os.chdir('../..')
    shutil.copy('tmp/memcached-1.2.6/memcached', 'build/bin')
    shutil.copy('tmp/memcached-1.2.6/memcached-debug', 'build/bin')
    
if __name__ == "__main__":
    main()
