#!/bin/bash

ruta_actual=$(pwd)
cat /var/log/auth.log | grep sshd | grep -Eo ' [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | grep -v '0.0.0.0' | grep -v '127.0.0.1'  > $ruta_actual/data/ips.txt
cat /var/log/auth.log | grep sshd | grep -E ' [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | grep -v '0.0.0.0' | grep -v '127.0.0.1' | awk '{print $1" "$2" "$3}' > $ruta_actual/data/hora.txt
paste $ruta_actual/data/hora.txt $ruta_actual/app/modulos/data/ips.txt > $ruta_actual/data/hora_ip.txt
rm $ruta_actual/data/ips.txt $ruta_actual/app/modulos/data/hora.txt
