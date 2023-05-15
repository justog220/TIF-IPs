#!/bin/bash

carpeta=$(basename $(pwd))
if [[ $carpeta == "TIF-IPs" ]]
then
    if [ "$UID" -eq 0 ]; then
        sudo sh -c 'cd app/modulos; python3 watchdogEj.py'
    else
        cd app/modulos
        python3 watchdogEj.py
    fi
fi


