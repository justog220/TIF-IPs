#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:42:15 2023

@author: justo
"""

import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from abuseIPDB import AbuseIPDB
import pandas as pd

class WatchdogSSH(FileSystemEventHandler):
    def __init__(self, rutaTabla):
        self._ipsAnalizadas = []
        self._diccionariosInfos = []
        
    def on_created(self, event):
        subprocess.call(["./buscarLogs.sh"])
        
    def on_modified(self, event):
        subprocess.call(["./buscarLogs.sh"])
        self.checkearReputacion()
        
    def checkearReputacion(self):
        with open("data/hora_ip.txt", "r") as registro:
            info = registro.readlines()
            for data in info:
                split = data.split()
                mes, dia, hora, ip = split[0], split[1], split[2], split[3]
                if not ip in self._ipsAnalizadas:
                    self._ipsAnalizadas.append(ip)
                    
                    abuseIPDB = AbuseIPDB()
                    info = abuseIPDB.getInfo(ip)
                    
                    info["mes"] = mes
                    info["dia"] = dia
                    info["hora"] = hora
                    
                    print(info)
                    self._diccionariosInfos.append(info)
                    self.actualizarDB()
                    
                    
    def actualizarDB(self):
        ips = []
        esPublica = []
        estaEnWhitelist = []
        scoreAbuso = []
        pais = []
        codigoPais = []
        meses = []
        dias = []
        horas = []
        
        columnas = [ips, esPublica, estaEnWhitelist, scoreAbuso, pais, codigoPais, meses, dias, horas]
        for dic in self._diccionariosInfos:
            keys = dic.keys()
            
            for columna, key in zip(columnas, keys):
                columna.append(dic[key])
        
        
        df = pd.DataFrame(data={
            'IP' : ips,
            'Es publica' : esPublica,
            'Esta en whitelist' : estaEnWhitelist,
            'Score de abuso' : scoreAbuso,
            'Pais' : pais,
            'Codigo pais' : codigoPais,
            'Mes' : meses,
            'Dia' : dias,
            'Hora' : horas
            })
        
        df.to_csv("dataFrame.csv")
        
        html = df.to_html(classes='table table-stripped')
        
        with open("../web/tabla.html", "w") as pagHtml:
            pagHtml.write(html)
            
            
    
            
                
                
            
if __name__ == "__main__":
    event_handler = WatchdogSSH()
    
    observer = Observer()
    observer.schedule(event_handler, path='/var/log/auth.log', recursive=False)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        
        
    observer.join()
                
