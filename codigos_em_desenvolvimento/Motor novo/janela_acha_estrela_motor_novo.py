#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em Maio 20 2019

@Produzido no Debian e IDLE3

@author: Ubiratan de Campos

@ Esse é o código da janela acha estrela, que tem a função de interagir com o usuário, a fim de apontar o
dispositivo para um objeto qualquer, previamente selecionado no Stellarium.
"""


import tkinter as tk
from acha_estrela_motor_novo_v1 import AchaEstrela as acha
from Motor_half_step import Motor
from Motor_drive_novo import Motor as mv
from time import sleep



##Classe padrão para criar interface do tkinter
class LocalizaObjeto:
    
    def __init__(self, instancia_tk):
        
        #da um titulo para a instância criada
        instancia_tk.title("Localiza Objeto")
        self.objeto=acha()
        self.valor_primeiro_objeto=False
        
        #__________Frames________________________
        # cria os frames da interface        
        # No fr1 ficarão as mensagens sobre a janela
        self.fr1=tk.Frame(instancia_tk,bg='white')
        self.fr1.pack()
        # No fr2 ficará o botão sair, esse frame ficara na parte inferior da janela
        self.fr2=tk.Frame(instancia_tk,bg='white')
        self.fr2.pack(side="bottom")
        #No fr3 ficará os botões de ajuste fino, ficará na parte direita da janela 
        self.fr3=tk.Frame(instancia_tk,bg='white')
        self.fr3.pack(side="right")
        # No fr4 será dado um espaço, que ficará no extremo direito da janela
        self.fr4= tk.Frame(instancia_tk,bg='white')
        self.fr4.pack(side='left')
        #Frame ficarão dos botões da operação de achar estrelas..., que ficará a direita da janela
        self.fr5= tk.Frame(instancia_tk,bg='white')
        self.fr5.pack(side='left')
        
        
        #___________Mensagens____________________
        #cria o texto das mensagens que serão exibidas
        self.mensagem="Janela de Apontamento"
        self.mensagem1="Antes de começar o trabalho, não esqueça de selecionar o objeto na interface do Stellarium"
        self.mensagem2="Ajuste Fino"
        self.mensagem3="  "
        self.mensagem4="Posiciona Telescópio"
        self.mensagem8="Se quiser mudar de objeto, tem que selecioná-lo no Stellarium"
        # Insere o texto da mensagem
        self.mens1=tk.Message(self.fr1, text=self.mensagem,width=600,bg='lightyellow', font=('times', 18, 'bold'))
        self.mens1.pack()
        # Insere o texto da mensagem1
        self.mens2=tk.Message(self.fr1, text=self.mensagem1,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens2.pack()
        # Insere o texto da mensagem2
        self.mens3= tk.Message(self.fr3, text=self.mensagem2,width=600,bg='white',font=('times', 14, 'bold'))
        self.mens3.pack()
        # Insere o texto da mensagem3
        self.mens4= tk.Message(self.fr4, text=self.mensagem3,width=600,bg='white',font=('times', 20, 'italic'))
        self.mens4.pack()
        # Insere o texto da mensagem1
        self.mens5= tk.Message(self.fr5, text=self.mensagem4,width=600,bg='white',font=('times', 15, 'italic'))
        self.mens5.pack()
        # Insere um texto vazio, pois vai interagir com o código
        self.mens7= tk.Message(self.fr1, text=self.mensagem8,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens7.pack()        
        
        
        #____________Botões______________________##############################################################

        #cria os botões da interface
        # O bt1(sair)será o padrão todas janelas
        self.bt1=tk.Button(self.fr2, text="SAIR",font=('blue'),
                           width=10,height=2,bg="red",
                           command=instancia_tk.destroy)
        self.bt1.pack()               
      

        #cria os botões para o apontamento bt6, bt7, bt8 no frame 4 que esta na direita
        self.bt6=tk.Button(self.fr5, text="Acha 1ª Objeto",
                           width=20,height=2,bg="lightgreen",
                           command=self.primeiro_objeto)
        self.bt6.pack()

        self.bt7=tk.Button(self.fr5, text="Acha Proximo Objeto",
                           width=20,height=2,bg="lightgreen",
                           command=self.proximo_objeto)
        self.bt7.pack()

        self.bt8=tk.Button(self.fr5, text="Acompanha Objeto",
                           width=20,height=2,bg="lightgreen",
                           command=self.acompanha_objeto)
        self.bt8.pack()
        
       

        # Preenche o frame 3, com os botões bt2,bt3,bt4,bt5 dos ajustes finos, no frame 3 que esta a esquerda
        self.bt2=tk.Button(self.fr3, text="1 passo para cima",
                           width=15,height=2,bg="lightblue",
                           command=self.um_passo_para_cima)
        self.bt2.pack()

        self.bt3=tk.Button(self.fr3, text="1 passo para baixo",
                           width=15,height=2,bg="yellow",
                           command=self.um_passo_para_baixo)
        self.bt3.pack()

        self.bt4=tk.Button(self.fr3, text="1 passo para direita",
                           width=15,height=2,bg="lightgreen",
                           command=self.um_passo_para_direita)
        self.bt4.pack()

        self.bt5=tk.Button(self.fr3, text="1 passo para esquerda",
                           width=15,height=2,bg="lightpink",
                           command=self.um_passo_para_esquerda)
        self.bt5.pack()
                
        
        #___________Funções______________________#########################################################################################
    
    
    #Essa função retorna o nome do objeto
    def nome_objeto(self):
        nome=self.objeto.nome_objeto()
        return nome

    #Essa função executa os comandos para encontrar o primeiro objeto 
    def primeiro_objeto(self):
        if self.valor_primeiro_objeto==False:
            self.objeto.primeira_estrela()
            self.valor_primeiro_objeto=True
            return 1
        else:
            return 0

    # Essa função executa os comandos para achar o segundo objeto
    def proximo_objeto(self):
        print("A trava é: ", self.valor_primeiro_objeto)
        if self.valor_primeiro_objeto==True:
            self.objeto.proxima_estrela()
            return 1
        else:
            return 0

    # Essa função executa os camandos para acompanhar o objeto
    def acompanha_objeto(self):
        self.objeto.acompanha_estrela()
        return 1
         
     
            

    # Essa função executa o comando fino para o motor
    def um_passo_para_baixo(self):        
        passos=self.objeto.passos_minimos_acompanhamento
        motor_vertical=Motor(12,20,16,21)
        motor_vertical.anti_horario(130,passos)
        print(passos)
        return True
    
    # Essa função faz o motor dar um passo para cima
    def um_passo_para_cima(self):
        passos=self.objeto.passos_minimos_acompanhamento
        motor_vertical=Motor(12,20,16,21)
        motor_vertical.horario(130,passos)
        print(passos)
        return True

    # Essa funçao faz o motor dar um passo para direita
    def um_passo_para_direita(self):
        passos=self.objeto.passos_minimos_acompanhamento
        motor_horizontal_horario=mv("horario", 25, passos,130)         
        motor_horizontal_horario.automatiza_rotacao()
        print(passos)
        return True

    # Essa funçao faz o motor dar um passo para esquerda
    def um_passo_para_esquerda(self):
        passos=self.objeto.passos_minimos_acompanhamento
        motor_horizontal_anti_horario=mv("anti", 25, passos, 130)        
        motor_horizontal_anti_horario.automatiza_rotacao()
        print(passos)
        return True
    


###########################################################################################################################################################

##Função principal (starta a aplicação)            
    
def main():
    janela=tk.Tk()
    LocalizaObjeto(janela)
    janela.geometry("600x400+650+600")
    janela['bg']= 'white'
    janela.mainloop()

if __name__== "__main__":
    main()

## Opções de tamanho de botão width=100,height=40
##command=self.encontra_norte

