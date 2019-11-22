#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sat Feb  2 13:28:48 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

##Importa as classes dos outros arquivos
from calibracao_telescopio import SensorMagnetico as sm
from Motor import Motor as mt
##from time import sleep
import math

"""Essa é a classe responsável em encontrar o norte
geográfico, já levando em consideração a declinação do
lugar"""

class EncontraNorte:
    
    ## Função construtora
    def __init__(self,declinacao):                 
        self.motor_horizontal=mt(13,25,19,26)
        self.motor_vertical=mt(12,20,16,21)
        self.declinacao=declinacao

    ## Função que le o sensor de posição motor horizontal 
    def le_sensor_posicao(self):
        objeto=sm(10)
        valor=objeto.ponto_cardeal()
        return valor
        
    ## Função que le o sensor de nivel motor vertical
    def le_sensor_nivel(selt):        
        objeto=sm(10)
        valor=objeto.medicao_nivel()
        return valor

    ## Função que le o sensor no eixo y
    def le_sensor_eixo_y(self):
        objeto=sm(10)
        valor=objeto.medicao_eixo_y()
        return valor

    ## Função que le o sensor no eixo x
    def le_sensor_eixo_x(self):
        objeto=sm(10)
        valor=objeto.medicao_eixo_x()
        return valor

    ## Função que le o sensor no eixo x
    def le_sensor_eixo_z(self):
        objeto=sm(10)
        valor=objeto.medicao_eixo_z()
        return valor
         
    ##Essa função coloca o sensor na posição calibrada para o nivelamento.
    def corrige_posicao(self):
        teste=self.le_sensor_posicao()
        print(teste)
        ##Posição determinada nos levantamentos, para
        ## corrigir o nível
        if teste<10 or teste>16:                        
            ##Condições para girar no sentido anti_horario (não enrolar os cabos)
            if teste>16 and teste<180:
                verificacao=self.avalia_lado_anti_horario()
                if verificacao==True:
                    self.motor_horizontal.anti_horario(20,18)
                    self.corrige_posicao()
                else:
                    self.motor_horizontal.horario(20,60)
                    self.corrige_posicao()
            ##Condições para girar no sentido horario (não enrolar os cabos)
            elif teste<10 or teste>180:
                verificacao=self.avalia_lado_horario()
                if verificacao==True:
                    self.motor_horizontal.horario(20,30)
                    self.corrige_posicao()
                else:
                    self.motor_horizontal.anti_horario(20,60)
                    self.corrige_posicao()

                    
        return True  
         
   ## Essa função corrige o nivel do telescópio, o algoritimo foi feito apos estudo matemático
    def corrige_nivel(self):
        diferenca,quadrado=self.calcula_funcao_ordem9()
        print(diferenca,quadrado)
        
        ## Condições para corrigir o nível quando o telescopio esta acima do nivel
        if (diferenca>0.5) and (diferenca<3.5) and quadrado>0:
            print(diferenca,quadrado)
            return True

        elif (diferenca>3.5) and (diferenca<15) and quadrado>12.25:
            self.motor_vertical.anti_horario(20,4)
            self.corrige_nivel()

        elif diferenca>15 and diferenca<30 and quadrado>225:
            self.motor_vertical.anti_horario(20,100)
            self.corrige_nivel()

        elif diferenca<-20 and quadrado>8000:
            self.motor_vertical.anti_horario(20,220)
            self.corrige_nivel()
        elif diferenca>-50 and quadrado>20000:
            self.motor_vertical.anti_horario(20,260)                    
            self.corrige_nivel()    
        ## Condições para corrigir o nível quando o telescopio esta abaixo do nivel
        else:
            self.motor_vertical.horario(20,360)
            self.corrige_nivel()
            
        return True      
    
    ## As duas funções abaixo verifica o lado que o telescopio deve rodar 
    def avalia_lado_anti_horario(self):
        contador=0
        vetor=[]
        while contador<10:
            vetor.append(int(self.le_sensor_posicao()))
            self.motor_horizontal.anti_horario(20,18)
            contador+=1
        if (vetor[0]+vetor[1])<(vetor[-1]+vetor[-2]):

        
            return False
        else:            
            return True

    def avalia_lado_horario(self):
        contador=0
        vetor=[]
        while contador<10:
            vetor.append(int(self.le_sensor_posicao()))
            self.motor_horizontal.horario(20,18)
            contador+=1
        if (vetor[-1]+vetor[-2])<(vetor[0]+vetor[1]):
            return False
        else:            
            return True  
        
    ## Essa função automatiza o nivelamento do telescopio   
    def automatiza_correcao(self):               
        posicao= self.corrige_posicao()
        ##print(posicao)
        if posicao==True:
            nivel= self.corrige_nivel()
            ##print(nivel)
            if nivel!=True:
                print("Alguma coisa saiu errado")                
            else:
                self.aponta_norte()
                return True                
        else:
            print("Alguma coisa saiu errado")
            return False          
        
    ## Função utilizada para levantamento de dados            
    def varias_leituras(self):
        a=0
        while a<430:
            e=self.le_sensor_nivel()
            f=self.le_sensor_posicao()
            #b=self.le_sensor_eixo_x()
            #c=self.le_sensor_eixo_y()
            #d=self.le_sensor_eixo_z()
            self.motor_horizontal.anti_horario(30,8)
            #print(a,",",b,",",c,",",d)
            print(a,",",f,",",e)
            a+=1
        return True
   ## Função de ajuste da curva dos eixos yx e zx
    def calcula_funcao_ordem9(self):
        planoxy=self.le_sensor_posicao()
        planoxz= self.le_sensor_nivel()
        valor=planoxy
        a0=21.4610662325283*math.pow(valor,0)
        a1=1.47333759745332 *math.pow(valor,1)
        a2=-0.0943808915362651 *math.pow(valor,2)
        a3=0.00247786753246764 *math.pow(valor,3)
        a4=-0.0000282147428962676 *math.pow(valor,4)
        a5= 0.000000170339028694675 *math.pow(valor,5)
        a6= -0.000000000575895043780493 *math.pow(valor,6)
        a7= 0.00000000000104655259109254 *math.pow(valor,7)
        a8= -8.56044009980434e-16 *math.pow(valor,8)
        a9= 1.47616338731074e-19 *math.pow(valor,9)    
        resultado=a0+a1+a2+a3+a4+a5+a6+a7+a8+a9
        diferenca=resultado-planoxz
        quadrado=math.pow(diferenca,2)
        return (diferenca,quadrado)
    ## Essa função encontra o norte geográfico usando a declinação local (São Paulo ~21º) 
    def aponta_norte(self):
         ## O valor da declinação será digitado no form de entrada
        ## E vai depender do local onde o observador esta
        declinacao=self.declinacao
        ## Esse valor de entrada depende da posiçao do sensor 
        ## O norte vai estar no ponto 0, porém no protótipo
        ## O telescópio esta defazado de 90° em relação ao 0 do sensor
        ## Dessa forma o Norte estará na posição 90.
        defasagem_telescopio_sensor=0 ## Valor pode ser alterado        
        ## A referencia e a declinação encontram o norte geografico        
        referencia= defasagem_telescopio_sensor+declinacao
        valor=self.le_sensor_posicao()
        if valor>(referencia-1) and valor<(referencia+1):
            return True
        elif valor<(referencia+1):
            self.motor_horizontal.horario(20,2)
            self.aponta_norte()
        elif valor>(referencia-1):
            self.motor_horizontal.anti_horario(20,2)
            self.aponta_norte()
        return True















        """valor=self.le_sensor_posicao()
        if valor>110 and valor<111:
            return True
        elif valor<110:
            self.motor_horizontal.horario(60,1)
            self.aponta_norte()
        elif valor>111:
            self.motor_horizontal.anti_horario(60,1)
            self.aponta_norte()
        return True"""
