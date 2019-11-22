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
            m = sensor.get_magnet()
            sleep(0.1)
            valor.append(m)
        return valor

## Essa função devolve o média das medições realizadas no eixo Z
    def nivelamento(self):
        matriz=self.obtem_dados()
        somab=0
        somac=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x+=650
            y+=350
            ##---------------------------------------------------------------
            b = math.degrees(math.atan2(y, x))
            c = math.degrees(math.atan2(z,y))
            if b<0:
                b+=360.0
                somab+=b                
            else:
                somab+=b
            if c<0:
                c+=360.0
                somac+=c                
            else:
                somac+=c
            
        mediab=somab/(len(matriz))
        mediac=somac/(len(matriz))
        return mediab, mediac

## Essa função devolve o valor numerico do ponto cardeal    
    def ponto_cardeal(self):
        matriz=self.obtem_dados()  
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x+=650
            y+=350
            ##---------------------------------------------------------------
            b = math.degrees(math.atan2(y, x))
            if b < 0:
                b += 360.0
            soma+=b  
        media=soma/(len(matriz))
        return media


    def medicao_nivel(self):
        matriz=self.obtem_dados()  
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x+=650
            y+=350
            ##---------------------------------------------------------------
            b = math.degrees(math.atan2(z, y))
            if b < 0:
                b += 360.0
            soma+=b  
        media=soma/(len(matriz))
        return media

    def medicao_eixo_z(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x+=650
            y+=350
            ##---------------------------------------------------------------
            soma+=z
        media=soma/(len(matriz))
        return media

    def medicao_eixo_y(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x+=650
            y+=350
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
            x+=650
            y+=350
            ##---------------------------------------------------------------
            soma+=x
        media=soma/(len(matriz))
        return media
            

    
        
