#!/bin/bash

if [ "`whoami`" != "root" ]; then
    echo You need to be root in order to install required dependencies
    exit
fi

if [ ! "`whereis pip`" ]; then
    echo You need "pip" to install requirements. On Ubuntu you can type: sudo apt-get install python-pip
else
    pip install -r requirements.txt $1
fi
