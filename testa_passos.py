#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sun Oct  6 07:56:02 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
Esse programa tem a finalidade de verificar qual é a quantidade minima de passos para o deslocamento

"""

from Motor_half_step import Motor as mt
from time import sleep

def passos_motor_horizontal_horario(quant, passos):
    motor_horizontal= mt(13,25,19,26)
    temp=130
    a=0
    while a<quant:
        motor_horizontal.horario(temp,passos)
        sleep(0.5)
        a+=1
        print("O quantidade de passos foi: ",a)
    return (print("O ciclo acabou"))
    
    
def passos_motor_horizontal_anti_horario(quant, passos):
    motor_horizontal= mt(13,25,19,26)
    temp=130
    a=0
    while a<quant:
        motor_horizontal.anti_horario(temp,passos)
        sleep(0.5)
        a+=1
        print("O quantidade de passos foi: ",a)
    return (print("O ciclo acabou"))    
    
    
    
def passos_motor_vertical_horario(quant, passos):
   motor_vertical=mt(12,20,16,21)
   temp=130
   a=0
   while a<quant:
       motor_vertical.horario(temp,passos)
       sleep(0.5)
       a+=1
       print("O quantidade de passos foi: ",a)
   return (print("O ciclo acabou"))   
    
def passos_motor_vertical_anti_horario(quant, passos):
   motor_vertical=mt(12,20,16,21)
   temp=130
   a=0
   while a<quant:
       motor_vertical.anti_horario(temp,passos)
       sleep(0.5)
       a+=1
       print("O quantidade de passos foi: ",a)
   return (print("O ciclo acabou"))    
    
    
    
