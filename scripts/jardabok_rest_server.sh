#!/bin/bash
PROGRAM_PATH=/var/www/jardabok.com/server/icelandic_farms_as_network/server/src
PROGRAM_NAME=icelandic_farms_rest_server.py
LOG_FILE=/var/log/icelandic_farms_rest_server.log

while [  true ]; do
    cd $PROGRAM_PATH
    /usr/bin/python3.4  ./$PROGRAM_NAME >> $LOG_FILE 2>&1
done
