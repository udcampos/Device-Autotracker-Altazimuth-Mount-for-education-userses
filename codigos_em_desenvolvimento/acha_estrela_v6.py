#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
################################################################################################################################################
@ Criado em Março 2019

@ Produzido no Debian

@ author: Ubiratan de Campos

Essa classe define os métodos utilizados para mirar o telescópio em direção
à um objeto no céu, vale ressaltar que o algoritimo usado, utiliza integralmente
os  dados enviados pelo Stellarium. 
Para obter os dados do Stellarium, é necessário ativar o remote control, 
que é um plugin do stellarium. Porém o sistema só funciona corretamente, 
se o Stellarium e esse aplicativo forem abertos no mesmo terminal. 
Há dois métodos utilizados para achar objetos no céu, o acha_primeira_estrela
e o acha_próxima_estrela.
A versão 3, incrementa na função próxima estrela. a capacidade de achar o menor 
caminho no azimute para o próximo objeto .
O ângulo por passo no dispositivo novo é de 0.0087890625° por passo, que é igual
a 31.64 segundos de arco.Não foi arredondado o valor acima pois o arredondamento da
quantidade de passos é dado a função round.O total de passos com a relação de engrena-
gens de 10 vezes será de 40960 passos/360º.
Nota V5: - Corrigido o algulo do pulo, para retornar sempre 1 passo
         - Acrescentado nos motores a função de ajustar as engrenagens.
         - Introduzida a função verifica_coordenada_proxima_estrela,
         com o objetivo de corrigir as coordenadas depois do acompa-
         nhamento.
Nota V6: -Durante o acompanhamento o motor não consegue pular um passo, vou adequar para que a quantidade de passos seja adequada
         - Melhorar a precisão do azimute. Para isso o algoritimo vai fazer duas verificações, 1 para posicionar e outra para corrigir caso a estrela
         tenha se deslocado.

###############################################################################

"""

from valores_api_stellarium import InformacoesStellarium as info
from Motor_half_step import Motor
from time import sleep

class AchaEstrela:

    """ Construtor, esses vetores são "memórias" que armazenam os valores do 
    azimute e da altura, essas memórias serão utilizadas por todas as 
    funções"""
    def __init__(self):
        self.vetor_guarda_azimute=[]
        self.vetor_guarda_altura=[]
        self.vetor_acompanha_azimute=[]
        self.vetor_acompanha_altura=[]
        self.passos_corrigidos_azimute=0
        self.passos_corrigidos_altura=0
        self.ultimo_valor_se_corrige_passos_azimute=0
        self.ultimo_valor_se_corrige_passos_altura=0
        self.angulo_passo_azimute=0.0087890625
        self.angulo_passo_altura= 0.0087890625        
        self.tempo_passo=130
        self.passos_ajuste=200
        self.passos_minimos_acompanhamento=8
    
    """ Essa função recebe os valores da função coordenadas_horizontais e 
         troca alguns caracteres por espaços, replace=substitui"""    
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
        print(round(azimute_decimal,8))
        return round(azimute_decimal,8)
   
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
        print(round(altura_decimal,8))     
        return round(altura_decimal,8)
    
    ## Essa função retorna o nome do objeto 
    def nome_objeto(self):
        objeto=info()
        nome=objeto.nome_objeto()
        return nome
    
    ########################################################################
    ########################################################################### 
    """ Codigo copiado e adaptado do aciona_motor.py
    Essa parte do codigo considera que cada passo é igual a 0.0087890625 
    graus decimais.A função aciona motor, faz os movimentos necessários 
    no motor selecionado."""
    
    ## Esssas funções controlam os motores para o apntamento.
    
    ## Essa função movimenta o motor do azimute sentido anti_horario
    def aciona_motor_horizontal_anti_horario(self,azimute):
        a=self.tempo_passo ## Velocidade do movimento do motor
        ap=self.angulo_passo_azimute ## Angulo por passo
        pa=self.passos_ajuste## Movimento para ajuste da engrenagens
        #b é a quantidade de passos 1passo= 0.0087890625º
        print("O azimute para calculo é: ",azimute)         
        ##A função **round** faz uma aproximação inteira do valor         
        b=(round(azimute/ap))          
        c=b+pa  ## Variável para ajustar as engrenagens do motor
        ## Se a quantidade de passos é diferente de zero, o motor é acionado
        if b!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.anti_horario(a,c)  
            motor_horizontal.horario(a,pa) ##Ajuste da engrenagem do motor                  
            print("o motor horizontal foi acionado no sentido anti-horário",a,b)
            return True
        else:
            return False
    
     ## Essa função movimenta o motor do azimute sentido horario
    def aciona_motor_horizontal_horario(self,azimute):
        a=self.tempo_passo
        ap=self.angulo_passo_azimute
        pa=self.passos_ajuste
        print("O azimute para calculo é: ",azimute)
        b=(round(azimute/ap)) 
        c=b+pa       
        if b!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.horario(a,c)
            motor_horizontal.anti_horario(a,pa)            
            print("o motor horizontal foi acionado no sentido horário",a,b)
            return True
        else:
            return False

    ## Essa função movimenta o motor da altura no sentido anti_horario            
    def aciona_motor_vertical_anti_horario(self,altura):
        a=self.tempo_passo 
        ap=self.angulo_passo_azimute
        pa=self.passos_ajuste
        print("A altura para calculo é: ",altura)
        b=(round(altura/ap)) 
        c=b+pa       
        if b!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.anti_horario(a,c)
            motor_vertical.horario(a,pa)            
            print("o motor vertical foi acionado no sentido anti-horário",a,b)
            return True
        else:
            return False
           
     ## Essa função movimenta o motor da altura no sentido horario 
    def aciona_motor_vertical_horario(self,altura):
        a=self.tempo_passo
        ap=ap=self.angulo_passo_altura
        pa=self.passos_ajuste 
        print("A altura para calculo é: ",altura)
        b=round(altura/ap)
        c=b+pa        
        if b!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.horario(a,c)
            motor_vertical.anti_horario(a,pa)            
            print("o motor vertical foi acionado no sentido horário",a,b)
            return True 
        else:
            return False
    
    ###########################################################################
   
    
    ## Essas funções controlam os motores durante o acompanhamento
    
    ## Essa função movimenta o motor do azimute sentido anti_horario
    def aciona_motor_horizontal_anti_horario_acompanhamento(self):
        a=self.tempo_passo ## Velocidade do movimento do motor
        passos=self.passos_minimos_acompanhamento
        print("A quatidade de passos é: ", self.passos_minimos_acompanhamento)
        if passos!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.anti_horario(a,passos)                               
            print("o motor horizontal foi acionado no sentido anti-horário",a,passos)
            return True
        else:
            return False
    
     ## Essa função movimenta o motor do azimute sentido horario
    def aciona_motor_horizontal_horario_acompanhamento(self):
        a=self.tempo_passo
        passos=self.passos_minimos_acompanhamento
        print("A quatidade de passos é: ", self.passos_minimos_acompanhamento)
        if passos!=0:
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.horario(a,passos)                      
            print("o motor horizontal foi acionado no sentido horário",a,passos)
            return True
        else:
            return False

    ## Essa função movimenta o motor da altura no sentido anti_horario            
    def aciona_motor_vertical_anti_horario_acompanhamento(self):
        a=self.tempo_passo 
        passos=self.passos_minimos_acompanhamento              
        if passos!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.anti_horario(a,passos)                       
            print("o motor vertical foi acionado no sentido anti-horário",a,passos)
            return True
        else:
            return False
           
     ## Essa função movimenta o motor da altura no sentido horario 
    def aciona_motor_vertical_horario_acompanhamento(self):
        a=self.tempo_passo
        passos=self.passos_minimos_acompanhamento        
        if passos!=0:
            motor_vertical=Motor(12,20,16,21)       
            motor_vertical.horario(a,passos)                     
            print("o motor vertical foi acionado no sentido horário",a,passos)
            return True 
        else:
            return False
     
    ############################################################################################################################
    

    ## Essas funções são usadas como memória             
    def vetor_azimute(self,azimute):
        self.vetor_guarda_azimute.append(azimute)
        vetor=self.vetor_guarda_azimute        
        return vetor
    
    ## Essa função guarda os valores da altura
    def vetor_altura(self,altura):
        self.vetor_guarda_altura.append(altura)
        vetor=self.vetor_guarda_altura
        return vetor
############################################################################ 
    """Essa função faz o apontamento para o primeiro objeto, 
       recebe os valores de altura e azimute decimal. Apartir desses valores
       Ele calcula a diferença entre o ponto inicial e a estrela que será
       observada"""
    def primeira_estrela(self):
        azimute=self.azimute_decimal()
        ## Guarda o valor no em um vetor
        self.vetor_azimute(azimute)  
        ## Define o lado que vai rodar     
        if azimute<180:
            resultado=self.aciona_motor_horizontal_horario(azimute)            
            if resultado==True:
                ############Alteração verificação do azimute#####################################
                azimute1=self.azimute_decimal()
                if azimute>azimute1:
                    del self.vetor_guarda_azimute[-1]
                    self.vetor_azimute(azimute1)
                    diferenca=azimute-azimute1
                    resultado=self.aciona_motor_horizontal_anti_horario(diferenca)                    
                    if resultado==True:
                        altura=self.altura_decimal()
                        self.vetor_altura(altura)
                        self.aciona_motor_vertical_horario(altura)
                        return True
                    else:
                        print("algo deu errado")
                        return False
            
                elif azimute<azimute1:
                    del self.vetor_guarda_azimute[-1]
                    self.vetor_azimute(azimute1)
                    diferenca=azimute1-azimute
                    resultado=self.aciona_motor_horizontal_horario(diferenca)               
                
                    if resultado==True:
                        altura=self.altura_decimal()
                        self.vetor_altura(altura)
                        self.aciona_motor_vertical_horario(altura)
                        return True
                    
                    else:
                        print("algo deu errado")
                        return False

                else:
                    if resultado==True:
                       altura=self.altura_decimal()
                       self.vetor_altura(altura)
                       self.aciona_motor_vertical_horario(altura)
                       return True
            else:
                print("algo deu errado")
                return False                     
                
                
        else:
            ## Se não girar de um lado, gira do outro
            valor=360-azimute
            resultado=self.aciona_motor_horizontal_anti_horario(valor)
            if resultado==True:
                azimute1=self.azimute_decimal()
                if azimute>azimute1:
                    del self.vetor_guarda_azimute[-1]
                    self.vetor_azimute(azimute1)
                    diferenca=azimute-azimute1
                    resultado=self.aciona_motor_horizontal_anti_horario(diferenca)
                    
                    if resultado==True:
                        altura=self.altura_decimal()
                        self.vetor_altura(altura)
                        self.aciona_motor_vertical_horario(altura)
                        return True
                    else:
                        print("algo deu errado")
                        return False

                elif azimute<azimute1:
                    del self.vetor_guarda_azimute[-1]
                    self.vetor_azimute(azimute1)
                    diferenca=azimute1-azimute
                    resultado=self.aciona_motor_horizontal_horario(diferenca)
                    if resultado==True:
                        altura=self.altura_decimal()
                        self.vetor_altura(altura)
                        self.aciona_motor_vertical_horario(altura)
                        return True
                    else:
                        print("algo deu errado")
                        return False

            else:
                if resultado==True:
                    altura=self.altura_decimal()
                    self.vetor_altura(altura)
                    self.aciona_motor_vertical_horario(altura)
                    return True

                else:
                    print("algo deu errado")
                    return False    
                
                

    #############################################################################################################################################
    """ Funções para troca do objeto, cabe ressaltar que a troca só acontece 
    se o objeto for selecionado no Stellarium. Caso o usuário encontre algum 
    problema na troca, vale a pena voltar ao inicio, encontrando a posição 
    inicial"""
    
    ## Essa analisa qual é a metade da circunferência que os ângulos estão       
    def analisa_metade_azimute(self,valor):
        if valor>=0 and valor<180:
            return 1
        elif valor>=180 and valor<360:
            return 2    
        else:
            return 0
        
    """Devolve para a função define_posicao_proxima_estrela, qual é a posição
    da estrela que o telescópio esta posicionado, e da próxima estrela a ser
    posicionado"""
    def analisa_posicao_estrelas(self,vetor_azimute,azimute_decimal):        
        metade_azimute_primeira_estrela=self.analisa_metade_azimute(vetor_azimute[-2])
        metade_azimute_segunda_estrela=self.analisa_metade_azimute(vetor_azimute[-1])
        ##print(metade_azimute_primeira_estrela,metade_azimute_segunda_estrela)
        return metade_azimute_primeira_estrela,metade_azimute_segunda_estrela    
    
    
    """ Essa função acha a próxima estrela, usando o caminho mais curto
    para posicionar o azimute"""    
    def define_azimute_proxima_estrela(self,azimute_acompanhamento):
        azimute=self.azimute_decimal()
        if azimute_acompanhamento!=0:        
            self.vetor_azimute(azimute_acompanhamento)            
        ##recebe a memória guardada no vetor       
        vetor_azimute=self.vetor_azimute(azimute)
        #print(vetor_azimute)
        """Se o valor do azimute da próxima estrela estiver na mesma metade 
           da circunferência, significa que que não há necessidade
           de definir o caminho mais curto, já que todos os angulos serão meno-
           res que 180°"""
        e1,e2=self.analisa_posicao_estrelas(vetor_azimute,azimute)
        if e1==e2:
            if vetor_azimute[-2]>vetor_azimute[-1]:
                print("Os valores usados para o calculo do azimute foram")
                print(vetor_azimute[-2],vetor_azimute[-1])
                resultado=vetor_azimute[-2]-vetor_azimute[-1] 
                print(resultado)
                ##print ("1. e1=e2 Move motor anti_horário",passos)
                self.aciona_motor_horizontal_anti_horario(resultado)
            else:
                print("Os valores usados para o calculo do azimute foram")
                print(vetor_azimute[-2],vetor_azimute[-1])
                resultado=vetor_azimute[-1]-vetor_azimute[-2]
                print(resultado)                 
                self.aciona_motor_horizontal_horario(resultado)
                
        """ Se o valor do azimute da próxima estrela estiver na outra metade
        da circunferência, é necessário fazer uma compensação para encontrar o
        caminho mais curto"""
        if (e1==2 and e2==1):
            if (vetor_azimute[-2]-vetor_azimute[-1])<=180:
                if vetor_azimute[-2]>vetor_azimute[-1]:
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    resultado=vetor_azimute[-2]-vetor_azimute[-1]
                    print(resultado)
                    
                    self.aciona_motor_horizontal_anti_horario(resultado)
                    return True
                else:
                    resultado=vetor_azimute[-1]-vetor_azimute[-2]
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (resultado)
                    self.aciona_motor_horizontal_horario(resultado)
                    return True
            else:
                if vetor_azimute[-2]>270 and vetor_azimute[-1]<90:
                    a=360-vetor_azimute[-2]
                    b=vetor_azimute[-1]
                    angulo_resultante=a+b
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (angulo_resultante)
                    self.aciona_motor_horizontal_horario(angulo_resultante)
                    return True
                
                elif vetor_azimute[-2]>90 and vetor_azimute[-1]<270:
                    a=360-vetor_azimute[-2]
                    b=vetor_azimute[-1]
                    angulo_resultante=a+b
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (angulo_resultante)
                    self.aciona_motor_horizontal_horario(angulo_resultante)
                    return True
        """ Se o valor do azimute da próxima estrela estiver na outra metade
        da circunferência, é necessário fazer uma compensação para encontrar o
        caminho mais curto"""            
        if e2==2 and e1==1:
            if (vetor_azimute[-1]-vetor_azimute[-2])<=180:
                if vetor_azimute[-2]>vetor_azimute[-1]:
                    resultado=vetor_azimute[-2]-vetor_azimute[-1]
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (resultado)
                    self.aciona_motor_horizontal_anti_horario(resultado)
                    return True
                else:
                    resultado=vetor_azimute[-1]-vetor_azimute[-2]
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (resultado)
                    self.aciona_motor_horizontal_horario(resultado)
                    return True
            else:
                if vetor_azimute[-1]>270 and vetor_azimute[-2]<90:
                    a=360-vetor_azimute[-1]
                    b=vetor_azimute[-2]
                    angulo_resultante=a+b
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (angulo_resultante)
                    self.aciona_motor_horizontal_anti_horario(angulo_resultante)
                    return True
                    
        
                elif vetor_azimute[-1]>90 and vetor_azimute[-2]<270:
                    a=360-vetor_azimute[-1]
                    b=vetor_azimute[-2]
                    angulo_resultante=a+b
                    print("Os valores usados para o calculo do azimute foram")
                    print(vetor_azimute[-2],vetor_azimute[-1])
                    print (angulo_resultante)
                    self.aciona_motor_horizontal_anti_horario(angulo_resultante)
                    return True
            
## Essa função corrige o altura para um segundo objeto a ser encontrado  
    def define_altura_proxima_estrela(self,altura_acompanhamento):
        altura=self.altura_decimal()
        if altura_acompanhamento!=0:        
            self.vetor_altura(altura_acompanhamento) 
        vetor_altura=self.vetor_altura(altura)
        print (vetor_altura)
        if len(vetor_altura)>1:
            if vetor_altura[-1]>vetor_altura[-2]:
                altura=vetor_altura[-1]-vetor_altura[-2]
                self.aciona_motor_vertical_horario(altura)
                return True
            else:
                altura=vetor_altura[-2]-vetor_altura[-1]
                self.aciona_motor_vertical_anti_horario(altura)
                return True

    ## Essa função usa as funções anteriores para encontrar a próxima estrela
    def proxima_estrela(self):
        self.zera_memoria_passos()
        #verifica se houve acompanhamento
        altura_acompanhamento,azimute_acompanhamento=self.verifica_coordenada_proxima_estrela()
        self.define_azimute_proxima_estrela(azimute_acompanhamento)
        self.define_altura_proxima_estrela(altura_acompanhamento)
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
        sleep(1)       ## Aqui é necessário ser o mesmo angulo corrigido, já que o resultado deve ser o pulo de 1 passo  
        self.vetor_acompanha_azimute.append(self.azimute_decimal())
        valor_correcao=(self.angulo_passo_azimute*self.passos_minimos_acompanhamento)
        ## Compara para verifica se o primeiro é maior que o ultimo 
        if self.vetor_acompanha_azimute[0]>self.vetor_acompanha_azimute[-1]:
            print("O valor da correção é: ", valor_correcao)
            print("A diferença do azimute é: ", (self.vetor_acompanha_azimute[0]-self.vetor_acompanha_azimute[-1]))
            ##Faz uma comparação para verificar se a subtração dos valores da para movimentar um passo
            if (self.vetor_acompanha_azimute[0]-self.vetor_acompanha_azimute[-1])<valor_correcao :
                sleep(0.1)           
            else:
                self.aciona_motor_horizontal_anti_horario_acompanhamento()
                self.passos_corrigidos_azimute-=1
                ##Quando corrige os passos, é guardado a ultima posição da estrela.
                self.ultimo_valor_se_corrige_passos_azimute=self.vetor_acompanha_azimute[-1]
                self.vetor_acompanha_azimute=[]
        else:
            if (self.vetor_acompanha_azimute[-1]-self.vetor_acompanha_azimute[0])<valor_correcao:
                sleep(0.1)
            else:
                self.aciona_motor_horizontal_horario_acompanhamento()
                self.passos_corrigidos_azimute+=1
                self.ultimo_valor_se_corrige_passos_azimute=self.vetor_acompanha_azimute[-1]
                self.vetor_acompanha_azimute=[]       
    
## Essa função corrige a altura do objeto em tempo real     
    def acompanha_estrela_altura(self):
        self.vetor_acompanha_altura.append(self.altura_decimal())       
        sleep(1)  
        ## Aqui é necessário ser o mesmo angulo corrigido, já que o resultado deve ser o pulo de 1 passo      
        valor_correcao=(self.angulo_passo_azimute*self.passos_minimos_acompanhamento)      
        self.vetor_acompanha_altura.append(self.altura_decimal())
        print(self.vetor_acompanha_altura)
        if self.vetor_acompanha_altura[0]>self.vetor_acompanha_altura[-1]:
            print("O valor da correção é: ", valor_correcao)
            print("A diferença da altura é: ", (self.vetor_acompanha_altura[0]-self.vetor_acompanha_altura[-1]))
            if (self.vetor_acompanha_altura[0]-self.vetor_acompanha_altura[-1])<valor_correcao:
                sleep(1)            
            else:                
                self.aciona_motor_vertical_anti_horario_acompanhamento()
                self.passos_corrigidos_altura-=1
                ##Quando corrige os passos, é guardado a ultima posição da estrela.
                self.ultimo_valor_se_corrige_passos_altura=self.vetor_acompanha_altura[-1]
                self.vetor_acompanha_altura=[]
                
        else:
            print("O valor da correção é: ", valor_correcao)
            print("A diferença da altura é: ", (self.vetor_acompanha_altura[-1]-self.vetor_acompanha_altura[0]))
            if (self.vetor_acompanha_altura[-1]-self.vetor_acompanha_altura[0])<valor_correcao:
                sleep(1)                
            else:
                self.aciona_motor_vertical_horario_acompanhamento()
                self.passos_corrigidos_altura+=1
                self.ultimo_valor_se_corrige_passos_altura=self.vetor_acompanha_altura[-1]
                self.vetor_acompanha_altura=[]
        
    ##Essa função usa as duas anteriores para acompanhar o objeto em tempo real
    def acompanha_estrela(self):  
                nome_atual=self.nome_objeto()
                print("O nome do objeto selecionado é: ", nome_atual)                                              
                memoria= nome_atual
                self.zera_memoria_passos()
                ##while memoria=="" or memoria==nome_atual:
                while memoria==nome_atual:
                    self.acompanha_estrela_azimute()
                    self.acompanha_estrela_altura()
                    print("Os passos pulados no azimute foram ", self.passos_corrigidos_azimute)
                    print("Os passos pulados na altura foram ", self.passos_corrigidos_altura)                     
                    memoria=self.nome_objeto()
                    #print("O nome do objeto atual é: ",memoria)
                print("O objeto foi alterado para", memoria)
                
     ##Essa função envia os valores da correção para a proxima_estrela
     
    def verifica_coordenada_proxima_estrela(self):
        if self.vetor_acompanha_altura!=[]:
            ultima_altura_vetor=self.vetor_acompanha_altura[-1]
        else:
            ultima_altura_vetor=0
        if self.vetor_acompanha_azimute!=[]:
             ultimo_azimute_vetor= self.vetor_acompanha_azimute[-1]
        else:
             ultimo_azimute_vetor=0
        ultimo_valor_altura= self.ultimo_valor_se_corrige_passos_altura
        ultimo_valor_azimute=self.ultimo_valor_se_corrige_passos_azimute
        if ultima_altura_vetor!=0 and ultimo_azimute_vetor!=0:
            return (ultima_altura_vetor, ultimo_azimute_vetor)
        elif ultima_altura_vetor!=0 and ultimo_azimute_vetor==0:
            return (ultima_altura_vetor,ultimo_valor_azimute)
        elif ultima_altura_vetor==0 and ultimo_azimute_vetor!=0:
            return (ultimo_valor_altura,ultimo_azimute_vetor)
        else:
            return (0,0)
                
    ############################################################################################################################################################        
                
    ## Essa função zera todas as memórias.       
    def zera_memoria_total(self):
        self.passos_corrigidos_altura=0
        self.passos_corrigidos_azimute=0
        self.vetor_acompanha_altura=[]
        self.vetor_acompanha_azimute=[]
        self.vetor_guarda_altura=[]
        self.vetor_guarda_azimute=[] 
        
    def zera_memoria_passos(self):
        self.passos_corrigidos_altura=0
        self.passos_corrigidos_azimute=0
        
    
            
        
        
        
        
       
