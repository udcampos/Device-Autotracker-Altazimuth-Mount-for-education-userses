#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Fri Jan 18 22:36:09 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

from get_sensor import QMC5883L
import math
from time import sleep

""" Essa classe tem como função criar funções para manipulação
do sensor magnético"""
class SensorMagnetico:
    def __init__(self,quant_leitura):
        self.quant_leitura=quant_leitura


 ##Função obter dados, ela acessa o módulo do sensor criando uma 
##instancia para sua manipulação

    def obtem_dados(self):
        quant_leitura=self.quant_leitura
        valor=[]
        sensor = QMC5883L()## Sensor é uma instancia
        for i in range(quant_leitura):
            ## linha alterada pois essa função esta com a calibração
            ##m = sensor.get_magnet()
            m=sensor.get_magnet_raw()
            sleep(0.1)
            valor.append(m)        
        return valor   

## Essa função devolve o valor numerico do ponto cardeal    
    def ponto_cardeal(self):
        matriz=self.obtem_dados()  
        soma=0
        normaliza=[]
        h=0
        g=0
        a=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x-=9500
            y-=800
            ##---------------------------------------------------------------
            b = math.degrees(math.atan2(y, x))
            ##print("O valor de b puro é ", b)
            if b < 0:
                b += 360.0
            normaliza.append(b)
        normaliza.sort()
        ##print(normaliza)
        maior=max(normaliza)
        menor=min(normaliza)
        if (maior-menor)>80:
            ##self.corrige_vetor_proximo_zero(normaliza)
            ##normaliza.sort
            for numero in normaliza:
                if numero<20:
                    h+=1
                    ##print("O valor de h é : ", h)
                else:
                    g+=1
                    ##print("O valor de g é: ",g)
            if h > g:
                for n in range(len(normaliza)):
                    if normaliza[a]<20:                        
                        del (normaliza[a])
                        
            else:
                for n in range(len(normaliza)):
                    if normaliza[-1]>20:
                        del (normaliza[-1])
                        
        ##print("O vetor normalizado é ", normaliza)                
        soma=sum(normaliza)
        if (len(normaliza))==0:
            media=0
            return media
        else:
            media=soma/(len(normaliza))
            return media               
                

    ################################################################## 
    def medicao_nivel(self):
        matriz=self.obtem_dados()  
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x-=9500
            y-=800
            #################################################
            
            z_corrigido=self.corrige_z(x,z)
            ##---------------------------------------------------------------
            ##Alterado de Y para x
            b = math.degrees(math.atan2(z_corrigido, x))
            if b < 0:
                b += 360.0
            soma+=b  
        media=soma/(len(matriz))
        return media
    ###############################################################    
    def medicao_eixo_y(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x-=9500
            y-=800
            ##---------------------------------------------------------------
            soma+=y
        media=soma/(len(matriz))
        return media

    def medicao_eixo_x(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O 650 somado a média é para calibrar o sensor
            x-=9500
            y-=800
            ##---------------------------------------------------------------
            soma+=x
        media=soma/(len(matriz))
        return media
        
##############################################################################
    
    """Essas funções serão utilizadas para o calculo da inclinação no pachage
        nivelamento_usando_coordenadas"""           
    def inclinacao_eixo_z(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            z_corrigido=z
            soma+=z_corrigido
        media=soma/(len(matriz))
        return media

    def inclinacao_eixo_y(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            soma+=y
        media=soma/(len(matriz))
        return media

    def inclinacao_eixo_x(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            soma+=x
        media=soma/(len(matriz))
        return media
    
    
        
