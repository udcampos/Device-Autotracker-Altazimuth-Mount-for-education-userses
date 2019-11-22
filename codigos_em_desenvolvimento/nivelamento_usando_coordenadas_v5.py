#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em Sat Feb  2 13:28:48 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

##Importa as classes dos outros arquivos
from calibracao_telescopio_v2 import SensorMagnetico as sm
from Motor_half_step import Motor as mt
import math
from chave_fim_de_curso import fim_curso as fc

"""!Notas Versão 4: Essa é a classe responsável em encontrar o norte
geográfico, já levando em consideração a declinação do
lugar, a versão 4 implementa a função fim_curso. 
   !Notas Versão 5: O objetivo dessa versão é agilizar o processo de achar o
   norte, já que no campo esse processo foi muito demorado.
   foram retiradas as linhas não usadas, e alterada as funções corrige_posicao e
   aponta_norte"""

class EncontraNorte:
    
    ## Função construtora
    def __init__(self,declinacao):                 
        self.motor_horizontal=mt(13,25,19,26)
        self.motor_vertical=mt(12,20,16,21)
        self.declinacao=declinacao
    
    ###########################################################################
    
    ## Função que le o sensor de posição motor horizontal 
    def le_sensor_posicao(self,amostras):
        objeto=sm(amostras)
        valor=objeto.ponto_cardeal()
        valor=round(valor,1)
        return valor
        
    ## Função que le o sensor de nivel motor vertical
    def le_sensor_nivel(self,amostras):        
        objeto=sm(amostras)
        valor=objeto.medicao_nivel()
        valor=round(valor,1)
        return valor

    ## Função que le o sensor no eixo y
    def le_sensor_eixo_y(self,amostras):
        objeto=sm(amostras)
        valor=objeto.medicao_eixo_y()
        valor=round(valor,1)
        return valor

    ## Função que le o sensor no eixo x
    def le_sensor_eixo_x(self,amostras):
        objeto=sm(amostras)
        valor=objeto.medicao_eixo_x()
        valor=round(valor,1)
        return valor

    ## Função que le o sensor no eixo x
    def le_sensor_eixo_z(self,amostras):
        objeto=sm(amostras)
        valor=objeto.medicao_eixo_z()
        valor=round(valor,1)
        return valor
    
    ##########################################################################
         
    ##Essa função coloca o sensor na posição calibrada para o nivelamento.        
    def corrige_posicao(self):
        amostras=5
        velocidade=100
        teste=self.le_sensor_posicao(amostras)
        print(teste)
        while teste<340 or teste>350:
            if teste<340 and teste>=170:
                diferenca=340-teste
                passos=round (diferenca/0.0087890625)
                self.motor_horizontal.horario(velocidade,passos)
                teste=self.le_sensor_posicao(amostras)
                print ("Esta na posição 1")
            
            elif teste>350:
                diferenca=teste-350
                passos= round (diferenca/0.0087890625)
                self.motor_horizontal.anti_horario(velocidade,passos)
                teste=self.le_sensor_posicao(amostras)
                print ("Esta na posição 2")

            else:
                diferenca=teste+10
                passos=round(diferenca/0.0087890625)
                self.motor_horizontal.anti_horario(velocidade,passos)
                teste=self.le_sensor_posicao(amostras)
                print ("Esta na posição 3")

        return True
       
        
    ## Essa função corrige o nivel do telescópio, o algoritimo foi feito apos estudo matemático
    def corrige_nivel(self):
        diferenca,quadrado=self.calcula_funcao_ordem9()
        print(diferenca,quadrado)
        velocidade=100
        ## Condições para corrigir o nível quando o telescopio esta acima do nivel
        if (diferenca>15) and (diferenca<19) and quadrado>0:
            print(diferenca,quadrado)
            return True
        elif (diferenca>19) and (diferenca<20) and quadrado>361:
            self.motor_vertical.anti_horario(velocidade,48)
            self.corrige_nivel()
        elif diferenca>20 and diferenca<100 and quadrado>400:
            self.motor_vertical.anti_horario(velocidade,180)
            self.corrige_nivel()
        elif diferenca<-20 and quadrado>500:
            self.motor_vertical.anti_horario(velocidade,1320)
            self.corrige_nivel()
        elif diferenca<-50 and quadrado>20000:
            self.motor_vertical.anti_horario(velocidade,2080)                    
            self.corrige_nivel()    
    ## Condições para corrigir o nível quando o telescopio esta abaixo do nivel
        else:            
            self.motor_vertical.horario(130,800)
            self.corrige_nivel()
        return True       
      
    ## Essa função implementa a chave_fim_de_curso
    def corrige_nivel_fim_curso(self):
        objeto=fc()
        estado_chave=objeto.estado()
        while estado_chave==1:
            self.motor_vertical.anti_horario(100,10)
            estado_chave=objeto.estado()
        print("Chegou no fim")
        return True

    def verifica_chave(self):
        objeto=fc()
        estado_chave=objeto.estado()
        if estado_chave==1:
            return False
        else:
            return True    
        
    ## Essa função automatiza o nivelamento do telescopio   
    def automatiza_correcao(self):
    ##self.verifica_nivel_inicio()
        posicao= self.corrige_posicao()
        chave=self.verifica_chave()
    ##print(posicao)
        if posicao==True and chave==False:
            nivel= self.corrige_nivel()
            self.corrige_nivel_fim_curso()            
    ##print(nivel)            
            if nivel!=True:
                print("Alguma coisa saiu errado")                
            else:
                self.aponta_norte()
                return True                
        elif posicao==True and chave==True:
            print("Esta nivelado")
            self.aponta_norte()
            return False          
        else:
            print("Alguma coisa saiu errado")
            return False
        
    ## Função utilizada para levantamento de dados            
    def varias_leituras(self):
        a=0
        ##430 uma volta
        while a<840:
            amostras=5
            #e=self.le_sensor_nivel(amostras)
            #f=self.le_sensor_posicao(amostras)
            b=self.le_sensor_eixo_x(amostras)
            c=self.le_sensor_eixo_y(amostras)
            d=self.le_sensor_eixo_z(amostras)
            ##Alterado de 8 passos para 15
            self.motor_horizontal.horario(100,50)
            print(a,",",b,",",c,",",d)
            #print(a,",",f,",",e)
            ##print(a)
            a+=1
        return True
    
    ## Função de ajuste da curva dos eixos yx e zx
    def calcula_funcao_ordem9(self):
        amostras=3
        planoxy=self.le_sensor_posicao(amostras)
        planoxz= self.le_sensor_nivel(amostras)
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
        amostras=15
        velocidade=100        
        valor=360-(self.le_sensor_posicao(amostras))
        print("O angulo para corrigir é: ",valor)
        declinacao=(self.declinacao)
        passos=round(((declinacao+valor)-0.5)/0.0087890625)
        print("os passos são: ", passos)
        self.motor_horizontal.horario(velocidade,passos)
        print(" A declinação é : " ,declinacao)
        ## Esse valor de entrada depende da posiçao do sensor 
        ## O norte vai estar no ponto 0, porém no protótipo
        ## O telescópio esta defazado de 90° em relação ao 0 do sensor
        ## Dessa forma o Norte estará na posição 90.
        
        defasagem_telescopio_sensor=self.le_sensor_posicao(amostras)         
        ## A referencia e a declinação encontram o norte geografico
        while defasagem_telescopio_sensor<=declinacao:
            amostras=25
            self.motor_horizontal.horario(velocidade,10)
            defasagem_telescopio_sensor=self.le_sensor_posicao(amostras)
            print("A defasagem é :" ,defasagem_telescopio_sensor)
        print(defasagem_telescopio_sensor)
        return True
            
            
      




        















        
