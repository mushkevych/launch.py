#!/bin/sh

if [ -z "$1" ]; then
    echo "Need path to project root"
    exit 1
fi

vendor=$1/vendors
cd $vendor
sudo easy_install $vendor/virtualenv-1.6.4.tar.gz
