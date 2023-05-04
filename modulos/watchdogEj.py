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
    def __init__(self):
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
                mes, dia, ip = split[0], split[1], split[2]
                if not ip in self._ipsAnalizadas:
                    abuseIPDB = AbuseIPDB()
                    info = abuseIPDB.getInfo(ip)
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
        
        columnas = [ips, esPublica, estaEnWhitelist, scoreAbuso, pais, codigoPais]
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
            'Codigo pais' : codigoPais
            })
        
        df.to_csv("dataFrame.csv")
                
                
            
if __name__ == "__main__":
    event_handler = WatchdogSSH()
    
    observer = Observer()
    #observer.schedule(event_handler, path='rand.txt', recursive=False)
    observer.schedule(event_handler, path='/var/log/auth.log', recursive=False)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        
        
    observer.join()
                
