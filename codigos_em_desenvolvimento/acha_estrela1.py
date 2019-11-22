#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Tue Mar  5 11:04:53 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

from valores_api_stellarium import InformacoesStellarium as info
from Motor import Motor
from time import sleep

class AchaEstrela:

    def __init__(self):
        self.vetor_guarda_azimute=[]
        self.vetor_guarda_altura=[]
        self.vetor_acompanha_azimute=[]
        self.vetor_acompanha_altura=[]
        self.passos_corrigidos_azimute=0
        self.passos_corrigidos_altura=0
    
    def corrige_coordenadas(self):
        objeto=info()
        valor=objeto.coordenadas_horizontais()
        valor.replace("\ ","" )
        valor.replace('"',"")
        return valor
    
    def azimute_decimal(self):
        valor=self.corrige_coordenadas()
        a=0
        while valor[a]!="/":
            a+=1
            azimute=valor[1:a] 
        b=0
        while azimute[b]!="°":
            b+=1
        azimute_angulo_string=azimute[0:b] 
        azimute_minuto_string=azimute[b+1:b+3]
        azimute_segundo_string=azimute[b+4:b+8]   
        azimute_angulo=float(azimute_angulo_string)
        azimute_minuto=float(azimute_minuto_string)/60
        azimute_segundo=float(azimute_segundo_string)/3600
        azimute_decimal=azimute_angulo+azimute_minuto+ azimute_segundo
        print(azimute_decimal)
        return azimute_decimal
    
    def altura_decimal(self):
        valor=self.corrige_coordenadas()
        a=0
        while valor[a]!="/":
            a+=1
        altura=valor[a+2:] 
        c=0
        while altura[c]!="°":
            c+=1
        altura_angulo_string=altura[0:c] 
        altura_minuto_string=altura[c+1:c+3]
        altura_segundo_string=altura[c+4:c+8]
        altura_angulo=float(altura_angulo_string)
        altura_minuto=float(altura_minuto_string)/60
        altura_segundo=float(altura_segundo_string)/3600
        altura_decimal=altura_angulo+altura_minuto+ altura_segundo 
        print(altura_decimal)     
        return altura_decimal


    def nome_objeto(self):
        objeto=info()
        nome=objeto.nome_objeto()
        return nome
    
    ## Codigo copiado e adaptado do aciona_motor.py
    ## Essa parte do codigo considera o 
    
   
       
        ## A função aciona motor faz o movimento do motor
    def aciona_motor_horizontal_anti_horario(self,azimute):
        a=50
        #b é a quantidade de passos 1passo=0,692307692
        b=int(azimute/0.692307692)
        if b!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.anti_horario(a,b)
            return True
        else:
            return False
    
    def aciona_motor_horizontal_horario(self,azimute):
        a=50
        #b é a quantidade de passos 1passo=0,692307692
        b=int(azimute/0.692307692)
        if b!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.horario(a,b)
            return True
        else:
            return False
            
    def aciona_motor_vertical_anti_horario(self,altura):
        a=50
        #b é a quantidade de passos 1passo=0,692307692
        b=int(altura/0.692307692)
        if b!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.anti_horario(a,b)
            return True
        else:
            return False
           

    def aciona_motor_vertical_horario(self,altura):
        a=50
        #b é a quantidade de passos 1passo=0,692307692
        b=int(altura/0.692307692)
        if b!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.horario(a,b)
            return True 
        else:
            return False
            
    def vetor_azimute(self,azimute):
        self.vetor_guarda_azimute.append(azimute)
        vetor=self.vetor_guarda_azimute        
        return vetor
    
    def vetor_altura(self,altura):
         self.vetor_guarda_altura.append(altura)
         vetor=self.vetor_guarda_altura
         return vetor
   
    def primeira_estrela(self):
        azimute=self.azimute_decimal()
        self.vetor_azimute(azimute)       
        if azimute<180:
            resultado=self.aciona_motor_horizontal_horario(azimute)            
            if resultado==True:
                sleep(2)
                altura=self.altura_decimal()
                self.vetor_altura(altura)
                self.aciona_motor_vertical_horario(altura)        
        else:
            azimute=360-azimute
            resultado=self.aciona_motor_horizontal_anti_horario(azimute)
            if resultado==True:
                sleep(2)
                altura=self.altura_decimal()
                self.vetor_altura(altura)
                self.aciona_motor_vertical_horario(altura)
       
    def define_posicao_proxima_estrela(self):
        azimute=self.azimute_decimal()        
        vetor_azimute=self.vetor_azimute(azimute)
        print(vetor_azimute)
        if len(vetor_azimute)>1:
            if vetor_azimute[-1]>vetor_azimute[-2]:
                azimute=vetor_azimute[-1]-vetor_azimute[-2]
                resultado=self.aciona_motor_horizontal_horario(azimute)
                if resultado==True:
                    sleep(2)
                    self.define_posicao_proxima_estrela()                
            else:
                azimute=vetor_azimute[-2]-vetor_azimute[-1]
                resultado=self.aciona_motor_horizontal_anti_horario(azimute) 
                if resultado==True:
                    sleep(2)
                    self.define_posicao_proxima_estrela()    
    
   
    def define_altura_proxima_estrela(self):
        altura=self.altura_decimal()
        vetor_altura=self.vetor_altura(altura)
        print (vetor_altura)
        if len(vetor_altura)>1:
            if vetor_altura[-1]>vetor_altura[-2]:
                altura=vetor_altura[-1]-vetor_altura[-2]
                self.aciona_motor_vertical_horario(altura)
            else:
                altura=vetor_altura[-2]-vetor_altura[-1]
                self.aciona_motor_vertical_anti_horario(altura)
           
                        
    def acompanha_estrela_azimute(self):
        self.vetor_acompanha_azimute.append(self.azimute_decimal())
        sleep(1)
        azimute=1        
        self.vetor_acompanha_azimute.append(self.azimute_decimal())
        if self.vetor_acompanha_azimute[0]>self.vetor_acompanha_azimute[-1]:
            if (self.vetor_acompanha_azimute[0]-self.vetor_acompanha_azimute[-1])<0.7:
                sleep(1)           
            else:
                self.aciona_motor_horizontal_anti_horario(azimute)
                self.passos_corrigidos_azimute-=1
                self.vetor_acompanha_azimute=[]
        else:
           if (self.vetor_acompanha_azimute[-1]-self.vetor_acompanha_azimute[0])<0.7:
                sleep(1)
           else:
                self.aciona_motor_horizontal_horario(azimute)
                self.passos_corrigidos_azimute+=1
                self.vetor_acompanha_azimute=[]       
        
    def acompanha_estrela_altura(self):
        self.vetor_acompanha_altura.append(self.altura_decimal())
        sleep(1)        
        altura=1        
        self.vetor_acompanha_altura.append(self.altura_decimal())
        if self.vetor_acompanha_altura[0]>self.vetor_acompanha_altura[-1]:
            if (self.vetor_acompanha_altura[0]-self.vetor_acompanha_altura[-1])<0.7:
                sleep(1)            
            else:                
                self.aciona_motor_vertical_anti_horario(altura)
                self.passos_corrigidos_altura-=1
                self.vetor_acompanha_altura=[]
                
        else:
           if (self.vetor_acompanha_altura[-1]-self.vetor_acompanha_altura[0])<0.7:
                sleep(1)                
           else:
                self.aciona_motor_vertical_horario(altura)
                self.passos_corrigidos_altura+=1
                self.vetor_acompanha_altura=[]
        
    
    def acompanha_estrela(self):  
                nome_atual=self.nome_objeto()
                print("O nome do objeto selecionado é: ", nome_atual)
                memoria= ""
                while memoria=="" or memoria==nome_atual:
                    self.acompanha_estrela_azimute()
                    self.acompanha_estrela_altura()
                    print("Os passos pulados no azimute foram ", self.passos_corrigidos_azimute)
                    print("Os passos pulados na altura foram ", self.passos_corrigidos_altura)
                    memoria=self.nome_objeto()
                print("O objeto foi alterado para", memoria)
                
            
                

            
        
        
        
        
       
