carpeta=$(basename $(pwd))
if [[ $carpeta == "TIF-IPs"]]
then
    cd app
    cd modulos
fi

python3 watchdogEj.py
