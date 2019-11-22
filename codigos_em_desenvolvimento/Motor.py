#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sun Jan 13 22:41:56 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""
import RPi.GPIO as GPIO
from time import sleep

class Motor:
    def __init__(self,bobina_A1,bobina_A2,bobina_B1,bobina_B2):
        self.bobina_A1=bobina_A1
        self.bobina_A2=bobina_A2
        self.bobina_B1=bobina_B1
        self.bobina_B2=bobina_B2
        
    def define_passos(self,w1, w2, w3, w4):
        self.set_mod()
        GPIO.output(self.bobina_A1, w1)
        GPIO.output(self.bobina_A2, w2)
        GPIO.output(self.bobina_B1, w3)
        GPIO.output(self.bobina_B2, w4)    

    ## Programação full-step ( completo mais torque )
    def horario_full(self,tempo,passos):
        tempo=(tempo/1000.0)
        for i in range(0, passos):
            self.define_passos(1,0,0,1)
            sleep(tempo)
            self.define_passos(0,1,0,1)
            sleep(tempo)
            self.define_passos(0,1,1,0)
            sleep(tempo)
            self.define_passos(1,0,1,0)
            sleep(tempo)
            GPIO.cleanup()
        
    def anti_horario_full(self,tempo,passos):
        tempo=(tempo/1000.0)
        for i in range(0, passos):
            self.define_passos(1,0,1,0)
            sleep(tempo)
            self.define_passos(0,1,1,0)
            sleep(tempo)
            self.define_passos(0,1,0,1)
            sleep(tempo)
            self.define_passos(1,0,0,1)
            sleep(tempo)
            GPIO.cleanup()
      
    ## Programação Normal-step ( menos torque )
    def horario_normal(self,tempo,passos):
        tempo=(tempo/1000.0)
        for i in range(0, passos):
            self.define_passos(0,0,0,1)
            sleep(tempo)
            self.define_passos(0,1,0,0)
            sleep(tempo)
            self.define_passos(0,0,1,0)
            sleep(tempo)
            self.define_passos(1,0,0,0)
            sleep(tempo)
            GPIO.cleanup()
        
    def anti_horario_normal(self,tempo,passos):
        tempo=(tempo/1000.0)
        for i in range(0, passos):
            self.define_passos(1,0,0,0)
            sleep(tempo)
            self.define_passos(0,0,1,0)
            sleep(tempo)
            self.define_passos(0,1,0,0)
            sleep(tempo)
            self.define_passos(0,0,0,1)
            sleep(tempo)
            GPIO.cleanup()

     ##Programação half-step ( mais preciso?)
    def horario_half(self,tempo,passos):
        tempo=(tempo/1000.0)
        for i in range(0, passos):
            self.define_passos(1,0,0,1)
            sleep(tempo)
            self.define_passos(0,0,0,1)
            sleep(tempo)
            self.define_passos(0,1,0,1)
            sleep(tempo)
            self.define_passos(0,1,0,0)
            sleep(tempo)
            self.define_passos(0,1,1,0)
            sleep(tempo)
            self.define_passos(0,0,1,0)
            sleep(tempo)
            self.define_passos(1,0,1,0)
            sleep(tempo)
            self.define_passos(1,0,0,0)
            sleep(tempo)
            GPIO.cleanup()
            
    def anti_horario_half(self,tempo,passos):
        tempo=(tempo/1000.0)
        for i in range(0, passos):
            self.define_passos(1,0,0,0)
            sleep(tempo)
            self.define_passos(1,0,1,0)
            sleep(tempo)
            self.define_passos(0,0,1,0)
            sleep(tempo)
            self.define_passos(0,1,1,0)
            sleep(tempo)
            self.define_passos(0,1,0,0)
            sleep(tempo)
            self.define_passos(0,1,0,1)
            sleep(tempo)
            self.define_passos(0,0,0,1)
            sleep(tempo)
            self.define_passos(1,0,0,1)
            sleep(tempo)
            GPIO.cleanup()            
            
    def set_mod(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bobina_A1, GPIO.OUT)
        GPIO.setup(self.bobina_A2, GPIO.OUT)
        GPIO.setup(self.bobina_B1, GPIO.OUT)        
        GPIO.setup(self.bobina_B2, GPIO.OUT)
        
        
        
