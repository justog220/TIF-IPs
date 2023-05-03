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

class WatchdogSSH(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Evento {event.event_type} detectado en {event.src_path}")
        if '../pruebaTxt/datos.txt' == event.src_path:
            print(f"Archivo {event.src_path} modificado")
            
    def on_modified(self, event):
        print(f"Evento {event.event_type} detectado en {event.src_path}")
        if '../pruebaTxt/datos.txt' == event.src_path:
            subprocess.call(["./buscarLogs.sh"])
            print(f"Archivo {event.src_path} modificado")
            
if __name__ == "__main__":
    event_handler = WatchdogSSH()
    
    observer = Observer()
    
    observer.schedule(event_handler, path='../pruebaTxt/datos.txt', recursive=False)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        
        
    observer.join()
                
