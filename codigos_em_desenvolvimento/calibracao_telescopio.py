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

## Essa função devolve o média das medições realizadas no eixo Z
    def nivelamento(self):
        matriz=self.obtem_dados()
        somab=0
        somac=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            #x+=1950
            #x+=1600            
            #y+=900
            #y+=600
            ##---------------------------------------------------------------
            b = math.degrees(math.atan2(y, x))
            #####################################################
            ##z+=4600
            z_corrigido=self.corrige_z(x,z)
            c = math.degrees(math.atan2(z_corrigido,x))
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
        normaliza=[]
        h=0
        g=0
        a=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            #x+=1950
            ##x+=1600            
            #y+=900
            ##y+=600
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
            


    """def corrige_vetor_proximo_zero(self,normaliza):
        h=0
        g=0
        a=0
        vetor=normaliza
        vetor.sort
        for numero in vetor:
            if numero<20:
                h+=1
                print("O valor de h é : ", h)
            else:
                g+=1
                print("O valor de g é: ",g)
            if h > g:
                for numero in normaliza:
                    if numero<20:
                        
                        
                        
            else:
                for numero in normaliza:
                    if numero>20:
                        del normaliza[a]
                        a+=1"""
                
                

    ################################################################## 
    def medicao_nivel(self):
        matriz=self.obtem_dados()  
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            #x+=1950
            #x+=1600
            #y+=900
            ##y+=600
            #################################################
            ##z+=4600
            z_corrigido=self.corrige_z(x,z)
            ##---------------------------------------------------------------
            ##Alterado de Y para x
            b = math.degrees(math.atan2(z_corrigido, x))
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
            #x+=1950
            ##x+=1600
            #y+=900
            ##y+=600
            ##---------------------------------------------------------------
            #z+=4600
            z_corrigido=self.corrige_z(x,z)
            soma+=z_corrigido
        media=soma/(len(matriz))
        return media

    def medicao_eixo_y(self):
        matriz=self.obtem_dados()
        soma=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            #x+=1950
            ##x+=1600
            #y+=900
            ##y+=600
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
            #x+=1950
            ##x+=1600
            #y+=900
            ##y+=600
            ##---------------------------------------------------------------
            soma+=x
        media=soma/(len(matriz))
        return media
    
    
    ####################################################################
    def corrige_z(self,x,z):
        valor=x
        teste=z
        if valor<(-2500):
            resultado=int(teste*(0.93))
            return resultado
        elif valor<(-2000):
            resultado=int(teste*(0.95))
            return resultado
        elif valor<(-1500):
            resultado=int(teste*(0.96))
            return resultado
        elif valor<(-1000):
            resultado=int(teste*(0.97))
            return resultado
        elif valor<(-500):
            resultado=int(teste*(0.98))
            return resultado
        elif valor>(2500):
            resultado=int(teste*1.07)
            return resultado
        elif valor>(2000):
            resultado=int(teste*1.06)
            return resultado
        elif valor>(1500):
            resultado=int(teste*1.05)
            return resultado
        elif valor>(1000):
            resultado=int(teste*1.04)
            return resultado
        elif valor>(500):
            resultado=int(teste*1.03)
            return resultado
        else:
            return teste
        ##return teste
        
        
            

    
        
