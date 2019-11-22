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
        valor=round(valor,1)
        return valor
        
    ## Função que le o sensor de nivel motor vertical
    def le_sensor_nivel(selt):        
        objeto=sm(10)
        valor=objeto.medicao_nivel()
        valor=round(valor,1)
        return valor

    ## Função que le o sensor no eixo y
    def le_sensor_eixo_y(self):
        objeto=sm(10)
        valor=objeto.medicao_eixo_y()
        valor=round(valor,1)
        return valor

    ## Função que le o sensor no eixo x
    def le_sensor_eixo_x(self):
        objeto=sm(10)
        valor=objeto.medicao_eixo_x()
        valor=round(valor,1)
        return valor

    ## Função que le o sensor no eixo x
    def le_sensor_eixo_z(self):
        objeto=sm(10)
        valor=objeto.medicao_eixo_z()
        valor=round(valor,1)
        return valor
         
    ##Essa função coloca o sensor na posição calibrada para o nivelamento.
    def corrige_posicao(self):
        teste=self.le_sensor_posicao()
        print(teste)
        ##Posição determinada nos levantamentos, para
        ## corrigir o nível
        if teste<340 or teste>350:                        
            ##Condições para girar no sentido anti_horario (não enrolar os cabos)
            if teste>350 or teste<180:
                verificacao=self.avalia_lado_anti_horario()
                if verificacao==True:
                    self.motor_horizontal.anti_horario(20,18)
                    self.corrige_posicao()
                else:
                    self.motor_horizontal.horario(20,60)
                    self.corrige_posicao()
            ##Condições para girar no sentido horario (não enrolar os cabos)
            elif teste<340 or teste>180:
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
        if (diferenca>0) and (diferenca<1) and quadrado>0:
            print(diferenca,quadrado)
            return True

        elif (diferenca>1) and (diferenca<20) and quadrado>1:
            self.motor_vertical.anti_horario(20,3)
            self.corrige_nivel()

        elif diferenca>15 and diferenca<100 and quadrado>225:
            self.motor_vertical.anti_horario(20,130)
            self.corrige_nivel()

        elif diferenca<-20 and quadrado>8000:
            self.motor_vertical.anti_horario(20,220)
            self.corrige_nivel()
        elif diferenca<-50 and quadrado>20000:
            self.motor_vertical.anti_horario(20,260)                    
            self.corrige_nivel()    
        ## Condições para corrigir o nível quando o telescopio esta abaixo do nivel
        else:
            self.motor_vertical.horario(20,360)
            self.corrige_nivel()
        return True

    """def verifica_nivel_inicio(self):
        diferenca,quadrado=self.calcula_funcao_ordem9()
        print(diferenca,quadrado)
        if diferenca<-10 and quadrado>100:
            self.motor_vertical.anti_horario(20,100)            
            self.verifica_nivel_inicio()
        else:
            return False"""       
        
    
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
        ##self.verifica_nivel_inicio()
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
        ##430 uma volta
        while a<430:
            e=self.le_sensor_nivel()
            f=self.le_sensor_posicao()
            #b=self.le_sensor_eixo_x()
            #c=self.le_sensor_eixo_y()
            #d=self.le_sensor_eixo_z()
            ##Alterado de 8 passos para 15
            self.motor_horizontal.anti_horario(20,8)
            #print(a,",",b,",",c,",",d)
            print(a,",",f,",",e)
            a+=1
        return True
   ## Função de ajuste da curva dos eixos yx e zx
    def calcula_funcao_ordem9(self):
        planoxy=self.le_sensor_posicao()
        planoxz= self.le_sensor_nivel()
        valor=planoxy
        a0=40.9633973721647*math.pow(valor,0)
        a1=0.709458976163196 *math.pow(valor,1)
        a2=-0.0457336723081271 *math.pow(valor,2)
        a3=0.00130236019227568 *math.pow(valor,3)
        a4=-0.0000154794767447295 *math.pow(valor,4)
        a5= 0.0000000988673871403368 *math.pow(valor,5)
        a6= -0.000000000366285310802548 *math.pow(valor,6)
        a7= 0.000000000000776704092312208 *math.pow(valor,7)
        a8= -8.56238851377937e-16 *math.pow(valor,8)
        a9= 3.67390459439629e-19 *math.pow(valor,9)    
        resultado=a0+a1+a2+a3+a4+a5+a6+a7+a8+a9
        diferenca=resultado-planoxz
        quadrado=math.pow(diferenca,2)
        return (diferenca,quadrado)
    ## Essa função encontra o norte geográfico usando a declinação local (São Paulo ~21º) 
    def aponta_norte(self):
         ## O valor da declinação será digitado no form de entrada
        ## E vai depender do local onde o observador esta
        self.motor_horizontal.horario(20,350)
        declinacao=self.declinacao
        print(" A declinação é : " ,declinacao)
        ## Esse valor de entrada depende da posiçao do sensor 
        ## O norte vai estar no ponto 0, porém no protótipo
        ## O telescópio esta defazado de 90° em relação ao 0 do sensor
        ## Dessa forma o Norte estará na posição 90.
        defasagem_telescopio_sensor=self.le_sensor_posicao() ## Valor pode ser alterado        
        ## A referencia e a declinação encontram o norte geografico
        while defasagem_telescopio_sensor<=declinacao:            
            self.motor_horizontal.horario(40,1)
            defasagem_telescopio_sensor=self.le_sensor_posicao()
            print("A defasagem é :" ,defasagem_telescopio_sensor)
        print(defasagem_telescopio_sensor)
        return True
            
            
      




        """print(defasagem_telescopio_sensor)
        referencia= declinação-defasagem_telescopio_sensor
        ##valor=self.le_sensor_posicao()
        if valor>(referencia-1) and valor<(referencia+1):
            return True
        elif valor<(referencia+1):
            self.motor_horizontal.horario(20,2)
            self.aponta_norte()
        elif valor>(referencia-1):
            self.motor_horizontal.anti_horario(20,2)
            self.aponta_norte()
        return True















        valor=self.le_sensor_posicao()
        if valor>110 and valor<111:
            return True
        elif valor<110:
            self.motor_horizontal.horario(60,1)
            self.aponta_norte()
        elif valor>111:
            self.motor_horizontal.anti_horario(60,1)
            self.aponta_norte()
        return True"""
