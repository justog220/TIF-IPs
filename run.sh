carpeta=$(basename $(pwd))
if [[ $carpeta == "TIF-IPs"]]
then
    cd app/modulos
fi

python3 watchdogEj.py
