#!/bin/bash

if [ -z "$1" ]; then
    echo "Need path to project root"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Need path to virtual environment to install virtualenv"
    exit 1
fi

. $2/bin/activate

vendor=$1/vendors
cd $vendor
easy_install $vendor/virtualenv-1.10.1.tar.gz
easy_install $vendor/setuptools-1.4.tar.gz
easy_install $vendor/pip-1.4.1.tar.gz
easy_install $vendor/ipython-1.1.0.tar.gz

easy_install $vendor/unittest2-0.5.1.tar.gz
easy_install $vendor/nose-1.3.0.tar.gz
easy_install $vendor/distribute-0.7.3.zip

# pylint section start
easy_install $vendor/logilab-common-0.60.0.tar.gz
easy_install $vendor/logilab-astng-0.24.3.tar.gz
easy_install $vendor/astroid-1.0.1.tar.gz
easy_install $vendor/pylint-1.0.0.tar.gz
# pylint section end

easy_install $vendor/coverage-3.7.tar.gz
easy_install $vendor/unittest-xml-reporting-1.7.0.tar.gz

easy_install $vendor/setproctitle-1.1.8.tar.gz
easy_install $vendor/python_rest_client2.tar.gz
easy_install $vendor/psutil-1.2.0.tar.gz
