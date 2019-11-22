'''
Created on 26 de set de 2019

@author: bira
'''
#########################################################################
## Importações 

import RPi.GPIO as gpio
from time import sleep
########################################################################



class Motor:
    '''
    Essa classe tem como função criar os métodos de controle dos motores de passo
    '''


    def __init__(self, bobina_A1, bobina_A2, bobina_B1, bobina_B2):
        '''
        A classe recebe os GPIOs da Raspberry que serão responsáveis em acionar os motores de passo
        '''
        self.bobina_A1 = bobina_A1
        self.bobina_A2 = bobina_A2
        self.bobina_B1 = bobina_B1
        self.bobina_B2 = bobina_B2
        
        
    def set_mod(self):        
        gpio.setmode(gpio.BCM)
        gpio.setup(self.bobina_A1, gpio.OUT)
        gpio.setup(self.bobina_A2, gpio.OUT)
        gpio.setup(self.bobina_B1, gpio.OUT)        
        gpio.setup(self.bobina_B2, gpio.OUT)
        #print("Decide modo")     
     
        ## Essa classe liga as saidas das GPIOs   
    def define_passos(self, w1, w2, w3, w4):
        self.set_mod()        
        gpio.output(self.bobina_A1, w1)
        gpio.output(self.bobina_A2, w2)
        gpio.output(self.bobina_B1, w3)
        gpio.output(self.bobina_B2, w4)
        #print("w1: ", w1, "w2: ", w2, "w3: ", w3, "w4: ", w4)
        
        
    def passo_1(self):
        self.define_passos(1, 0, 0, 1)
        #print("passo 1")
        return True
        
    def passo_2(self):
        self.define_passos(0, 0, 0, 1)
        #print("passo 2")
        return True
    
    def passo_3(self):
        self.define_passos(0, 1, 0, 1)
        #print("passo 3")
        return True  
      
    def passo_4(self):
        self.define_passos(0, 1, 0, 0)
        #print("passo 4")
        return True
    
    def passo_5(self):
        self.define_passos(0, 1, 1, 0)
        #print("passo 5")
        return True
    
    def passo_6(self):
        self.define_passos(0, 0, 1, 0)
        #print("passo 6")
        return True
    
    def passo_7(self):
        self.define_passos(1, 0, 1, 0)
        #print("passo 7")
        return True
    
    def passo_8(self):
        self.define_passos(1, 0, 0, 0)
        #print("passo 8")
        return True
        
    def horario(self,tempo,passos):
        #print("horario")
        tempo= (tempo/10000)
        contagem=0
        #print("o valor de passos é: ", passos)
        for passo in range(passos,0,-1):
            #print(" O passo atual é: ", passo)            
            if contagem==0:
                self.passo_1()
                sleep(tempo)
            
            elif contagem==1:
                self.passo_2()
                sleep(tempo)
                
            elif contagem==2:
                self.passo_3()
                sleep(tempo)
                
            if contagem==3:
                self.passo_4()
                sleep(tempo)
                
            if contagem==4:
                self.passo_5()
                sleep(tempo)
                
            if contagem==5:
                self.passo_6()
                sleep(tempo) 
                
            if contagem==6:
                self.passo_7()
                sleep(tempo)
                
            if contagem==7:
                self.passo_8()
                sleep(tempo)                
                contagem=0
                continue           
            
            contagem=contagem+1
        gpio.cleanup()  


    def anti_horario(self,tempo,passos):
        #print("anti_horario")
        tempo= (tempo/10000)
        contagem=0
        #print("o valor de passos é: ", passos)
        for passo in range(passos,0,-1):
            #print(" O passo atual é: ", passo)                        
            if contagem==0:
                self.passo_8()
                sleep(tempo)
            
            elif contagem==1:
                self.passo_7()
                sleep(tempo)
                
            elif contagem==2:
                self.passo_6()
                sleep(tempo)
                
            if contagem==3:
                self.passo_5()
                sleep(tempo)
                
            if contagem==4:
                self.passo_4()
                sleep(tempo)
                
            if contagem==5:
                self.passo_3()
                sleep(tempo)
                
            if contagem==6:
                self.passo_2()
                sleep(tempo)
                
            if contagem==7:
                self.passo_1()
                sleep(tempo)
                contagem=0
                continue           
            
            contagem=contagem+1
          
        gpio.cleanup()
