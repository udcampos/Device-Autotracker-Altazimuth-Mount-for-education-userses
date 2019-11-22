#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sun Jan 13 22:41:56 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos

 Essa classe tem a função de controlar os motores de passos, usando o 
 driver A4988, e o motor de passo WS17-0035-04-4.
 Vamos usar para este teste de apenas 1 motor duas saidas a BCN 20 e 21

"""
import RPi.GPIO as gpio
from time import sleep

class Motor:
    def __init__(self,direcao,aciona_passo,quantidade_passos,tempo_passo):
        self.direcao=direcao
        self.aciona_passo=aciona_passo
        self.quantidade_passos=quantidade_passos
        self.tempo_passo=tempo_passo
        
    def sentido_rotacao(self):
        self.set_mod()
        if self.direcao== ("horario"):            
            gpio.output(19,gpio.HIGH)
        else:            
            gpio.output(19,gpio.LOW)
        return True
        
    def aciona_passos(self):
        self.set_mod()
        contagem=0
        tempo=self.tempo_passo/10000.0
        while contagem<self.quantidade_passos:
            #print("Passo: ",contagem)
            gpio.output(self.aciona_passo,gpio.HIGH)
            sleep(tempo)
            gpio.output(self.aciona_passo,gpio.LOW)
            sleep(tempo)
            contagem+=1
        print("O motor deu esses passos: ",contagem) 
        gpio.cleanup()
        return True    
        
    
    def automatiza_rotacao(self):
        rotacao=self.sentido_rotacao()
        if rotacao==True:
            aciona_motor=self.aciona_passos()
            if aciona_motor==True:
                print("O motor rodou no sentido: ",self.direcao)
            else:
                print("Algo deu errado")
        else:
            print("Algo deu errado")     
        
            
    def set_mod(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(19, gpio.OUT)
        gpio.setup(self.aciona_passo, gpio.OUT)
        
        
        
        
