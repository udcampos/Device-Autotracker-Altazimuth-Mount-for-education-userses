#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sun Jan 20 15:13:20 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

##from calibracao_telescopio import SensorMagnetico
import tkinter as tk
from nivelamento_usando_coordenadas_v6 import EncontraNorte as enorte
from time import sleep



##Classe padrão para criar interface do tkinter
class Calibracao:
    
    def __init__(self, instancia_tk):
        
        #da um titulo para a instância criada
        instancia_tk.title("Calibração do Telescopio")
        
        #__________Frames________________________
        # cria os frames da interface        
        # No fr1 ficarão as mensagens sobre a janela
        self.fr1=tk.Frame(instancia_tk,bg='white')
        self.fr1.pack()
        # No fr2 ficará o botão sair
        self.fr2=tk.Frame(instancia_tk,bg='white')
        self.fr2.pack(side="bottom")
        #No fr3 ficará as entradas e botões 
        self.fr3=tk.Frame(instancia_tk,bg='white')
        self.fr3.pack()
        # Frame de mensagem
        self.fr4= tk.Frame(instancia_tk,bg='white')
        self.fr4.pack()
        #Frame de espaço
        self.fr5= tk.Frame(instancia_tk,bg='white')
        self.fr5.pack()
        ## Frame dos botões de ajuste fino
        self.fr6= tk.Frame(instancia_tk,bg='white')
        self.fr6.pack()
        
        #___________Mensagens____________________
        #cria o texto das mensagens que serão exibidas
        self.mensagem="A calibração é uma etapa fundamental para observação"
        self.mensagem1=""
        self.mensagem2="É necessário inserir o valor da declinação Magnética da sua região"
        self.mensagem3="Use esse site: https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml#declination"
        self.mensagem4="Insira o valor da declinação"
        self.mensagem8="Ajuste fino do nivelamento"
        self.mensagem9="Usar apenas se necessário"
        # Insere o texto da mensagem
        self.mens1=tk.Message(self.fr1, text=self.mensagem,width=600,bg='lightyellow', font=('times', 18, 'bold'))
        self.mens1.pack()
        # Insere o texto da mensagem1
        self.mens2=tk.Message(self.fr1, text=self.mensagem1,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens2.pack()
        # Insere o texto da mensagem2
        self.mens3= tk.Message(self.fr1, text=self.mensagem2,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens3.pack()
        # Insere o texto da mensagem3
        self.mens4= tk.Message(self.fr1, text=self.mensagem3,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens4.pack()
        # Insere o texto da mensagem1
        self.mens5= tk.Message(self.fr1, text=self.mensagem1,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens5.pack()
        # Insere um texto vazio, pois vai interagir com o código
        self.mens7= tk.Message(self.fr4, text=" ",width=600,bg='white',font=('times', 12, 'italic'))
        self.mens7.pack()
        #Insere a mensagem 8 e 9, no frame 6
        self.mens8=tk.Message(self.fr6, text=self.mensagem8,width=600,bg='white',font=('times', 12, 'italic','bold'))
        self.mens8.pack()
        self.mens9=tk.Message(self.fr6, text=self.mensagem9,width=600,bg='white',font=('times', 12, 'italic','bold'))
        self.mens9.pack()
        
        
        
        #____________Botões______________________
        #cria os botões da interface
        # O bt1(sair)será o padrão todas janelas
        self.bt1=tk.Button(self.fr2, text="SAIR",font=('blue'),
                           width=10,height=2,bg="red",
                           command=instancia_tk.destroy)
        self.bt1.pack()        
         
        ## Insere texto da mensagem4
        self.mens6= tk.Message(self.fr3, text=self.mensagem4,width=600,bg='white',font=('times', 14, 'bold'))
        self.mens6.pack(padx=2, pady=5, side="left")
        self.ed1=tk.Entry(self.fr3, text=" ",bg="white",width=5)
        self.ed1.pack(side="left")

        ##cria o botão que inicia a calibração da posição
        self.bt2=tk.Button(self.fr3, text="Acha o Norte Geografico",
                           width=20,height=2,bg="lightgreen",
                           command=self.encontra_norte)
        self.bt2.pack()
        
        ###############################################################################################################################

        # Preenche o frame 8, com os botões de ajuste fino
        self.bt3=tk.Button(self.fr6, text="1 passo para cima",
                           width=20,height=2,bg="lightblue",
                           command=self.um_passo_para_cima)
        self.bt3.pack()

        self.bt4=tk.Button(self.fr6, text="1 passo para baixo",
                           width=20,height=2,bg="yellow",
                           command=self.um_passo_para_baixo)
        self.bt4.pack()
                
        
        #___________Funções______________________
    
    #Essa função define a entrada da declinação
    def entrada_declinacao(self):
        string= str(self.ed1.get())
        teste=self.verifica_entrada(string)
        if teste==True:
            self.mens7["text"]=" "
            self.mens7["bg"]="white"
            return True
        else:
            self.mens7["text"]="Digite um numero inteiro"
            self.mens7["bg"]="red"

    #Essa função testa a entrada ed1 e verifica se é um numero
    def verifica_entrada(self,string):
        try:
            float(string)
            return True
        except ValueError:
            return False            

    #Essa função inicia o nivelamento 
    def encontra_norte(self):
        
            if self.entrada_declinacao()==True:
                declinacao= float(self.ed1.get())
                ##self.mens7["text"]=" "
                norte=enorte(declinacao)
                norte.automatiza_correcao()
                return True

    # Essa função faz o motor dar um passo para cima
    def um_passo_para_baixo(self):
        norte=enorte(21)
        norte.motor_vertical.anti_horario(70,1)
        return True
    
    # Essa função faz o motor dar um passo para cima
    def um_passo_para_cima(self):
        norte=enorte(21)
        norte.motor_vertical.horario(70,1)
        return True
     
            
##Função principal (starta a aplicação)            
    
def main():
    janela=tk.Tk()
    Calibracao(janela)
    janela.geometry("600x500+100+100")
    janela['bg']= 'white'
    janela.mainloop()

if __name__== "__main__":
    main()

## Opções de tamanho de botão width=100,height=40
##command=self.encontra_norte

