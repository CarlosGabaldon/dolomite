#!/usr/bin/env python
import os, sys, tarfile, shutil
import subprocess as proc
import warnings

warnings.filterwarnings('ignore','.*apt API not stable yet.*')

import apt

def create_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)
        
def dependenciesMet(packages):
    met = True
    cache = apt.Cache()
    for package in packages:
        pkg = cache[package]
        if not pkg.isInstalled:
            print("%s package is not installed." % package)
            met = False
    return met

def copy_built_files(files, build_dir):
    if type(files) is list:
        for f in files:
            shutil.copy('tmp/%s/%s' % (build_dir, f), 'tools/dolomite-env/bin')
    else:
        shutil.copy('tmp/%s/%s' % (build_dir, files), 'tools/dolomite-env/bin')
        
def usage():
    print("Usage: %s component_name" % sys.argv[0])
    
def get_config(component):
    config_file = open("%s-conf" % component)
    config = { }
    for setting in config_file:
        if len(setting.split('=')) > 1:
            if (len(setting.split(' '))) > 1:
                config[setting.split('=')[0]] = setting.rstrip('\n').split('=')[1].split(' ')
            else:
                config[setting.split('=')[0]] = setting.rstrip('\n').split('=')[1]
    return config

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    component = sys.argv[1]
    
    print("building %s" % component)

    config = get_config(component)
    
    create_dir('tmp')
    create_dir('tools')
    create_dir('tools/dolomite-env')
    create_dir('tools/dolomite-env/bin')

    os.chdir('tmp')

    print("checking build depedencies...")
    if not dependenciesMet(config['BUILDDEP']):
        print("install dependencies using the following command and try again")
        print("sudo apt-get install %s" % " ".join(config['BUILDDEP']))
        sys.exit(1)
        
    print("downloading source...")
    try:
        proc.check_call(['wget','-c', '%s/%s' % (config['SOURCEPATH'], config['SOURCETARFILE'])])
    except proc.CalledProcessError:
        sys.exit(1)

    print("extracting tar ball...")    
    memcached = tarfile.open(name=config['SOURCETARFILE'], mode='r:gz')
    memcached.extractall()
    
    print("configuring...")
    os.chdir(config['BUILDDIR'])
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
    copy_built_files(config['INSTALLFILES'], config['BUILDDIR'])
    
if __name__ == "__main__":
    main()
