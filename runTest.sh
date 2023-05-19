#!/bin/bash

carpeta=$(basename $(pwd))
if [[ $carpeta == "TIF-IPs" ]]
then
    if [ "$UID" -eq 0 ]; then
        sudo sh -c 'cd appTest/modulos; python3 watchdogEj.py'
    else
        cd appTest/modulos
        python3 watchdogEj.py
    fi
fi


