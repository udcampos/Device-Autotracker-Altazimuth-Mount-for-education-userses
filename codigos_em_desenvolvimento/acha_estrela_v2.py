#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
################################################################################################################################################
@ Criado em Março 2019

@ Produzido no Debian

@ author: Ubiratan de Campos

Essa classe define os métodos utilizados para mirar o telescópio para um
objeto no céu, vale ressaltar que o algoritimo usado, utiliza integralmente
os  dados enviados pelo Stellarium. Para obter os dados do Stellarium, é necessá-
rio ativar o remote control, que é um plugin do stellarium. Há um bug no debian,
pois esse pllugin não corrige as informações em tempo real, felizmente esse bug
não apareceu no Raspberry Pi. Outra caracteristica utilizada, é a de utilizar
o nome próximo ao real do que será executado.. Ex. A função corrige coordenadas ]
ela realmente corrige as informações que veem do Stelarium.
O ângulo por passo no dispositivo novo é de 0,112º por passo, que é igual á 6 minutos e
43 segundos de arco.
###################################################################################################################################################

"""

from valores_api_stellarium import InformacoesStellarium as info
from Motor import Motor
from time import sleep

class AchaEstrela:

    ## Construtor, esses vetores serão as memórias onde serão armazenados os valores, fica no método construtor, pois servirá 
    ## para todas as funções da classe
    def __init__(self):
        self.vetor_guarda_azimute=[]
        self.vetor_guarda_altura=[]
        self.vetor_acompanha_azimute=[]
        self.vetor_acompanha_altura=[]
        self.passos_corrigidos_azimute=0
        self.passos_corrigidos_altura=0
    
   ## Essa função recebe os valores da função coordenadas_horizontais e troca alguns caracteres por espaços, replace=substitui    
    def corrige_coordenadas(self):
        objeto=info()
        valor=objeto.coordenadas_horizontais()
        valor.replace("\ ","" )
        valor.replace('"',"")
        return valor

    ##Essa função transforma os valores do azimute de texto para angulo decimal    
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
   
    ## Essa função transforma os valores de altura de texto para angulo decimal    
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
    
    ## Essa função retorna o nome do objeto 
    def nome_objeto(self):
        objeto=info()
        nome=objeto.nome_objeto()
        return nome
   
    ####################################################################################################### 
    ## Codigo copiado e adaptado do aciona_motor.py
    ## Essa parte do codigo considera que cada passa é igual a 0,692307692 graus decimais. 
    ## A função aciona motor, faz os movimentos necessários no motor selecionado.
    def aciona_motor_horizontal_anti_horario(self,azimute):
        a=30
        #b é a quantidade de passos 1passo=0,692307692 no dispositivo velho
        ## o b no dispositivo novo é de 0,111940298
        b=round(azimute/0.111940298)
        if b!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.anti_horario(a,b)
            return True
        else:
            return False
    
    def aciona_motor_horizontal_horario(self,azimute):
        a=30
        #b é a quantidade de passos 1passo=0,692307692
        ## o b no dispositivo novo é de 0,111940298
        b=round(azimute/0.111940298)
        if b!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.horario(a,b)
            return True
        else:
            return False

    ##### Essa função nunca será usada, pois o objeto nunca ficará abaixo do horizonte            
    def aciona_motor_vertical_anti_horario(self,altura):
        a=30
        #b é a q## o b no dispositivo novo é de 0,111940298
        ##Quantidade de passos 1passo=0,692307692
        
        b=round(altura/0.111940298)
        if b!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.anti_horario(a,b)
            return True
        else:
            return False
           

    def aciona_motor_vertical_horario(self,altura):
        a=30
        #b é a quantidade de passos 1passo=0,692307692
        ## o b no dispositivo novo é de 0,111940298
        
        b=round(altura/0.111940298)
        if b!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.horario(a,b)
            return True 
        else:
            return False
    
    ####################################################################################################################

    ## Essa função guarda os valores do azimute             
    def vetor_azimute(self,azimute):
        self.vetor_guarda_azimute.append(azimute)
        vetor=self.vetor_guarda_azimute        
        return vetor
    
    ## Essa função guarda os valores da altura
    def vetor_altura(self,altura):
         self.vetor_guarda_altura.append(altura)
         vetor=self.vetor_guarda_altura
         return vetor
    
    ## Essa função faz o apontamento para o primeiro objeto, ele recebe os valores de altura e azimute decimal
    def primeira_estrela(self):
        azimute=self.azimute_decimal()
        ## Guarda o valor no em um vetor
        self.vetor_azimute(azimute)  
        ## Define o lado que vai rodar     
        if azimute<180:
            resultado=self.aciona_motor_horizontal_horario(azimute)            
            if resultado==True:
                ##sleep(2)
                ## A altura só vai girar de um lado, acima do horizonte ou horário 
                altura=self.altura_decimal()
                self.vetor_altura(altura)
                self.aciona_motor_vertical_horario(altura)        
        else:
            ## Se não girar de um lado, gira do outro
            azimute=360-azimute
            resultado=self.aciona_motor_horizontal_anti_horario(azimute)
            if resultado==True:
                ##sleep(2)
                altura=self.altura_decimal()
                self.vetor_altura(altura)
                self.aciona_motor_vertical_horario(altura)

    #############################################################################################################################################
    """ Funções para troca do objeto, cabe ressaltar que a troca só acontece se o objeto for
        selecionado no Stellarium. Caso o usuário encontre algum problema na troca, vale a
        pena voltar ao inicio, encontrando a posição inicial"""
    
    ## Essa função corrige o azimute para o segundo objeto a ser encontrado       
    def define_posicao_proxima_estrela(self):
        azimute=self.azimute_decimal() 
        ##recebe a memória guardada no vetor       
        vetor_azimute=self.vetor_azimute(azimute)
        print(vetor_azimute)
        ## Se for maior que 1 significa que teve acompanhamento, a correção será a partir da ultima coordenada
        if len(vetor_azimute)>1:
            ## Essa comparação é para definir qual lado deve rodar  
            if vetor_azimute[-1]>vetor_azimute[-2]:
                ## O azimute recebe o valor de quantos passos deve ser corrigido
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
    
     ## Essa função corrige o altura para um segundo objeto a ser encontrado  
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

    ## Essa função usa as funções anteriores para encontrar a próxima estrela
    def proxima_estrela(self):
         self.define_posicao_proxima_estrela()
         self.define_altura_proxima_estrela()
         return True
    
    #####################################################################################################################################################################       
    """ Funções de acompanhamento do objeto, elas recebem os dados do stellarium em tempo
        real e os converte em movimento dos motores, cabe ressaltar que a correção,
        só ocorre quando o ângulo correnspondente ao passo do motor, ou a uma relação
        de engrenagens. Caso o projeto original seja alterado, os valores também devem
        ser corrigidos."""

    ## Essa função corrige o azimute do objeto em tempo real                     
    def acompanha_estrela_azimute(self):
        ## O valor obtido do stellarium em tempo real, é guardado no vetor, que servirá de memória
        self.vetor_acompanha_azimute.append(self.azimute_decimal())
        sleep(1)
        azimute=1        
        self.vetor_acompanha_azimute.append(self.azimute_decimal())
        ## Compara para verifica se o primeiro é maior que o ultimo 
        if self.vetor_acompanha_azimute[0]>self.vetor_acompanha_azimute[-1]:
            ##Faz uma comparação para verificar se a subtração dos valores da para movimentar um passo
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
    
     ## Essa função corrige a altura do objeto em tempo real     
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
        
    ##Essa função usa as duas anteriores para acompanhar o objeto em tempo real
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
                
    ############################################################################################################################################################        
                
    ## Essa função zera todas as memórias.       
    def zera_memoria(self):
        self.passos_corrigidos_altura=0
        self.passos_corrigidos_azimute=0
        self.vetor_acompanha_altura=[]
        self.vetor_acompanha_azimute=[]
        self.vetor_guarda_altura=[]
        self.vetor_guarda_azimute=[] 
            
        
        
        
        
       
