#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Wed Feb 13 21:26:56 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

import math



def calcula_funcao_ordem9():
    planoxy=float(input("Digite o valor do plano xy:  " ))   
    valor=planoxy
    a0=88.1575100539239*math.pow(valor,0)
    a1=-0.64665137294853 *math.pow(valor,1)
    a2=-0.0387549933829135 *math.pow(valor,2)
    a3=0.0015447039143533 *math.pow(valor,3)
    a4=-0.0000247364827447227 *math.pow(valor,4)
    a5= 0.000000212639983427239 *math.pow(valor,5)
    a6= -0.00000000104073966101066 *math.pow(valor,6)
    a7= 0.00000000000290217214415884 *math.pow(valor,7)
    a8= -4.29921031116736e-15 *math.pow(valor,8)
    a9= 2.62869195092606e-18 *math.pow(valor,9)
    
    resultado=a0+a1+a2+a3+a4+a5+a6+a7+a8+a9
    print(resultado)
    return (resultado)
 
def calcula_funcao_ordem20():
    planoxy=float(input("Digite o valor do plano xy:  " ))   
    valor=planoxy
    a0=92.419402298599138*math.pow(valor,0)
    a1=-2.2762519788829940 *math.pow(valor,1)
    a2=0.10873348584524611 *math.pow(valor,2)
    a3= -4.1013719026635649e-3 *math.pow(valor,3)
    a4= 8.8176475259915790e-5 *math.pow(valor,4)
    a5= -1.0755343968860089e-6 *math.pow(valor,5)
    a6= 7.3940484683668280e-9 *math.pow(valor,6)
    a7= -2.4862069160038227e-11 *math.pow(valor,7)
    a8= 6.5915453521361734e-15 *math.pow(valor,8)
    a9= 1.6873907998746912e-16 *math.pow(valor,9)
    a10= 1.5988996194330106e-19 *math.pow(valor,10)
    a11= -3.5071988767992747e-21 *math.pow(valor,11)
    a12=6.6246955720193066e-24 *math.pow(valor,12)
    a13= 3.7112865791266440e-27*math.pow(valor,13)
    a14= 2.3474281132432659e-29 *math.pow(valor,14)
    a15= -2.0225175221267357e-31 *math.pow(valor,15)
    a16=2.5686231678718131e-34 *math.pow(valor,16)
    a17=-2.8422883297234192e-38*math.pow(valor,17)
    a18= 1.5988206655488263e-39 *math.pow(valor,18)
    a19= -5.3012038942292367e-42 *math.pow(valor,19)
    a20= 4.5251862257715511e-45 *math.pow(valor,20)
        
    resultado1=a0+a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11
    resultado2=a12+a13+a14+a15+a16+a17+a18+a19+a20
    resultado=resultado1+resultado2
    print(resultado)
    return (resultado)
    
##calcula_funcao_ordem20()
calcula_funcao_ordem9()
