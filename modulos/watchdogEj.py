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
    def __init__(self):
        ipsAnalizadas = []
        
    def on_created(self, event):
        subprocess.call(["./buscarLogs.sh"])
        
    def on_modified(self, event):
        subprocess.call(["./buscarLogs.sh"])
        self.checkearReputacion()
        
    def checkearReputacion(self):
        with open("data/hora_ip.txt", "r") as registro:
            print(registro.read())
            
if __name__ == "__main__":
    event_handler = WatchdogSSH()
    
    observer = Observer()
    observer.schedule(event_handler, path='rand.txt', recursive=False)
    #observer.schedule(event_handler, path='/var/log/auth.log', recursive=False)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        
        
    observer.join()
                
