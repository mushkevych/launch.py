#!/bin/bash

# List of packages to install
python2list=(
    "linecache2-1.0.0.tar.gz"
    "traceback2-1.4.0.tar.gz"
    "six-1.10.0.tar.gz"
    "virtualenv-13.1.2.tar.gz" 
    "setuptools-18.3.2.tar.gz" 
    "distribute-0.7.3.zip"
    "unittest2-1.1.0.tar.gz" 
    "pbr-1.8.1.tar.gz"
    "funcsigs-0.4.tar.gz"
    "mock-1.3.0.tar.gz" 
    "nose-1.3.7.tar.gz"
)

python3list=(
    "six-1.10.0.tar.gz"
)

commonlist=(
    "pip-7.1.2.tar.gz"

    # ipython
    "path.py-8.1.2.tar.gz"
    "ipython_genutils-0.1.0.tar.gz"
    "ptyprocess-0.5.tar.gz"
    "decorator-4.0.4.tar.gz"
    "pickleshare-0.5.tar.gz"
    "simplegeneric-0.8.1.zip"
    "traitlets-4.0.0.tar.gz"
    "pexpect-4.0.1.tar.gz"
    "ipython-4.0.0.tar.gz"

    # pylint section start
    "logilab-common-1.0.2.tar.gz"
    "logilab-astng-0.24.3.tar.gz"
    "astroid-1.3.8.tar.gz"
    "pylint-1.4.4.tar.gz"

    "coverage-4.0.tar.gz"
    "unittest-xml-reporting-1.12.0.tar.gz"
    "setproctitle-1.1.9.tar.gz"
    "psutil-3.2.2.tar.gz"
)

if [ -z "$1" ]; then
    echo "Parameter #1 is missing: path to project root"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Parameter #2 is missing: path to target virtual environment"
    exit 1
fi

if [ -z "$3" ]; then
    echo "Parameter #3 is missing: Python major version"
    exit 1
fi

if [[ $3 == 2* ]]; then
    easy_install_bin="easy_install-$3"
    packagelist=("${python2list[@]}" "${commonlist[@]}")
elif [[ $3 == 3* ]]; then
    export PYTHONPATH="$2/lib/python$3/site-packages/"
    easy_install_bin="easy_install-$3 --prefix=$2"
    packagelist=("${python3list[@]}" "${commonlist[@]}")
else
    echo "Python version $3 is not yet supported"
    exit 1
fi

echo "DEBUG: PYTHONPATH=${PYTHONPATH}"
echo "DEBUG: easy_install_bin=${easy_install_bin}"

# ccache speeds up recompilation by caching previous compilations
which ccache > /dev/null 2>&1
if [ $? == 0 ]; then
    export CC="ccache gcc"
    export CXX="ccache g++"    
fi

# Ignore some CLANG errors on OSX else install will fail
if [ `uname` == "Darwin" ]; then
    export ARCHFLAGS="-arch i386 -arch x86_64"
    export CFLAGS=-Qunused-arguments
    export CPPFLAGS=-Qunused-arguments
fi

. $2/bin/activate

vendor=$1/vendors
cd ${vendor}

for package in "${packagelist[@]}"; do   # The quotes are necessary here
    ${easy_install_bin} ${vendor}/${package}
done
