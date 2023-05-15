carpeta=$(basename $(pwd))
if [[ $carpeta == "TIF-IPs" ]]
then
    if [ "$UID" -eq 0 ]; then
        sudo sh -c 'cd app/modulos'
    else
        cd app/modulos
    fi
fi

python3 watchdogEj.py
