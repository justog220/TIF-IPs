#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:32:41 2023

@author: justo
"""

from watchdog.observers import Observer
from modulos.watchdogEj import WatchdogSSH
import time

event_handler = WatchdogSSH("web/tabla.html")

observer = Observer()

observer.schedule(event_handler, path='/var/log/auth.log', recursive=False)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    
    
observer.join()