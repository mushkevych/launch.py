#!/bin/sh

if [ -z "$1" ]; then
    echo "Need path to project root"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Need path to virtual environment to install virtualenv"
    exit 1
fi

if [ `uname` == "Darwin" ]; then
    export ARCHFLAGS="-arch i386 -arch x86_64"
fi
which ccache > /dev/null 2>&1
if [ $? == 0 ]; then
    export CC='ccache gcc'
fi

. $2/bin/activate

vendor=$1/vendors
cd $vendor
easy_install $vendor/virtualenv-1.6.4.tar.gz
easy_install $vendor/ipython-0.10.1.tar.gz
easy_install $vendor/setproctitle-1.1.3.tar.gz

# pylint section start
easy_install $vendor/logilab-common-0.59.0.tar.gz
easy_install $vendor/logilab-astng-0.24.2.tar.gz
easy_install $vendor/pylint-0.27.0.tar.gz
# pylint section end

easy_install $vendor/unittest2-0.5.1.tar.gz
easy_install $vendor/coverage-3.4.tar.gz
easy_install $vendor/unittest-xml-reporting-1.0.3.tar.gz
easy_install $vendor/psutil-0.4.0.tar.gz
easy_install $vendor/python_rest_client2.tar.gz
