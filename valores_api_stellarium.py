#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Mon Mar  4 16:04:04 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
##import re
class InformacoesStellarium:
    ##Essa função retira as informações da Api do Stellarium
    def obtem_informacoes(self):
        ## Esse é o endereço da Api do Stellarium
        html = urlopen("http://localhost:8090/api/objects/info")
        res = BeautifulSoup(html.read(),"html5lib");
        texto=res.get_text()
        texto_matriz=texto.split()
        return texto_matriz
    ## Essa função separa as coordenadas que serão enviadas ao telescópio    
    def coordenadas_horizontais(self): 
        texto_matriz=self.obtem_informacoes()
        a=0
        for item in texto_matriz:
            a+=1
            if "Azimute/Altura" in item:
                azimute=texto_matriz[a]
                return azimute              
    ## Essa função retorna o nome do Objeto       
    def nome_objeto(self):
        texto_matriz=self.obtem_informacoes()
        return texto_matriz[0]
    
    ## Essa função retorna a magnetude do objeto
    def magnitude_objeto(self):
        texto_matriz=self.obtem_informacoes()
        a=0
        for item in texto_matriz:
            a+=1
            if "Magnitude" in item:
                magnitude= texto_matriz[a]
                valor=magnitude[:4]           
                return valor        
    
        
    def main(self):
        a= self.coordenadas_horizontais()
        b=self.nome_objeto()
        c=self.magnitude_objeto()
        return a,b,c
        