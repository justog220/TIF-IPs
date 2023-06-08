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
import os

class WatchdogSSH(FileSystemEventHandler):
    def __init__(self):
        """
        Constructor de la clase responsable de monitorear el archivo
        donde se registran las conexiones por protocolo SSH y ante un cambio
        llevar a cabo cierto proceso.

        Returns
        -------
        None.

        """
        self._ipsAnalizadas = []
        self._diccionariosInfos = []
        self._url = self.setUrl()

    def setUrl(self):
        ruta_html = '../web/index.html'

        # Obtener la ruta absoluta del archivo HTML
        ruta_absoluta = os.path.abspath(ruta_html)

        return ('file:///' + ruta_absoluta)
        
    def on_created(self, event):
        """
        Establece que es lo que se realiza si se crea el archivo de
        registros

        Parameters
        ----------
        event : Watchdog event
            evento ante la creación del archivo.

        Returns
        -------
        None.

        """
        subprocess.call(["./buscarLogs.sh"])
        
    def on_modified(self, event):
        """
        Establece que es lo que se realiza si se modifica el archivo de
        registros

        Parameters
        ----------
        event : Watchdog event
            evento ante la creación del archivo.

        Returns
        -------
        None.

        """
        subprocess.call(["./buscarLogs.sh"])
        self.checkearReputacion()
        
    def checkearReputacion(self):
        """
        Método que permite hacer una consulta a la API para
        conocer informacion de una ip.

        Returns
        -------
        None.

        """
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
        """
        Permite llevar a cabo un registro de la información de las 
        distintas IP de las cuales se han ido pidiendo información.

        Returns
        -------
        None.

        """
        ips = []
        esPublica = []
        estaEnWhitelist = []
        scoreAbuso = []
        codigoPais = []
        isps = []
        usos = []
        reportes = []
        
        columnas = [ips, esPublica, estaEnWhitelist, scoreAbuso, codigoPais, isps, usos, reportes]
        for dic in self._diccionariosInfos:
            keys = dic.keys()
            
            for columna, key in zip(columnas, keys):
                columna.append(dic[key])
        
        
        df = pd.DataFrame(data={
            'IP' : ips,
            'Es pública' : esPublica,
            'Está en whitelist' : estaEnWhitelist,
            'Score de abuso' : scoreAbuso,
            'Codigo país' : codigoPais,
            'ISP' : isps,
            'Uso' : usos,
            'Último reporte' : reportes
            })
        
        df.to_csv("dataFrame.csv")
        
        html = df.to_html(classes='table table-stripped')
        
        md = df.to_markdown()
        os.system("clear")
        print(md)
        
        with open("../web/estilo.html", "r") as estilos:
            estilo = estilos.read()

        with open("../web/tabla.html", "w") as pagHtml:
            pagHtml.write("")
            pagHtml.write(estilo + html)
    
            
                
                
            
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
                
