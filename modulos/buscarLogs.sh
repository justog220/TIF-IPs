#!/bin/bash

ruta_actual=$(pwd)
cat /var/log/auth.log | grep sshd | grep -Eo ' [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} ' | grep -v '0.0.0.0' > $ruta_actual/data/ips.txt

