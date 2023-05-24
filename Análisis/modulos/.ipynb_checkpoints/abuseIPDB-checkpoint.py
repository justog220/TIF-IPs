#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:28:33 2023

@author: justo
"""

import requests
import json

class AbuseIPDB:
    def __init__(self):
        """
        Constructor de un objeto que permite hacer uso
        de la API de AbuseIPDB para acceder a diversa información sobre
        una IP.

        Returns
        -------
        None.

        """
        self._url = 'https://api.abuseipdb.com/api/v2/check'
        
        self._response = None
        
        self._ip = None
        
        self._ABUSE_KEY = 'd0e45eadb7b17c33ea3d7a42d02e8b46b4a5ef3338878bc99c956ca3a84f46c47d5e067024438046'
        
    def checkEndpoint(self, ip):
        """
        Utiliza el endpoint CHECK de la api de AbuseIPDB

        Parameters
        ----------
        ip : str
            Ip cuya información desea consultarse con la API.

        Returns
        -------
        None.

        """
        self._ip = ip
        
        querystring = {
            'ipAddress' : ip,
            'maxAgeInDays': '90'
        }
        
        headers = {
            'Accept': 'application/json',
            'Key': self._ABUSE_KEY
        }
        
        self._response = requests.request(method='GET', url=self._url, headers=headers, params=querystring)
        
        
    def getInfo(self, ip):
        """
        Método que permite obtener información sobre una cierta
        dirección IP.

        Parameters
        ----------
        ip : str
            Dirección IP de la cual se desea conocer la 
            información.

        Returns
        -------
        diccInfo : dict
            {
                'ip' : direccionIP,
                'esPublica' : si es una IP pública o no,
                'estaEnWhitelist' : si esta en una whitelist de AbuseIPDB,
                'scoreAbuso' : que tanta seguridad sobre que es usada con fines maliciosos,
                'pais' : de que pais es
            }.

        """
        if self._ip != ip or not self._ip:
            self.checkEndpoint(ip)
            
        decodedResponse = json.loads(self._response.text)
        
        data = decodedResponse['data']
        
        diccInfo = {
            'ip' : data['ipAddress']
            }
        
        keys = ['esPublica', 'estaEnWhitelist', 'scoreAbuso', 'pais', 'codigoPais', 'isp']
        keysOr = ['isPublic', 'isWhitelisted', 'abuseConfidenceScore', 'countryName', 'countryCode', 'isp']
        for key, keyOr in zip(keys, keysOr):
            if keyOr in data:
                diccInfo[key] = data[keyOr]
            else:
                diccInfo[key] = 'NaN'
                
        return diccInfo
        
if __name__ == '__main__':
    apiAbuse = AbuseIPDB()
    
    info = apiAbuse.getInfo('192.168.0.13')
    
    print(info)