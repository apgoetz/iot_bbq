#!/bin/bash
export PYTHONPATH=/usr/lib/python3/dist-packages
BINDIR=/home/pi/iot_bbq

cd $BINDIR
source bin/activate
python hw.py
