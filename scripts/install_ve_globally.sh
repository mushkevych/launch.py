#!/bin/bash

if [ -z "$1" ]; then
    echo "Parameter #1 is missing: path to project root"
    exit 1
fi

vendor=$1/vendors
cd ${vendor}
sudo easy_install ${vendor}/virtualenv-15.0.3.tar.gz
