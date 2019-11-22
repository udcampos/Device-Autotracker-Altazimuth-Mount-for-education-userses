#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Wed Jan 23 12:26:13 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

""" Essa classe irá manipular os motores, quando for necessário testar 
alguma funcionalidade"""

from Motor import Motor
import tkinter as tk
from chave_fim_de_curso import fim_curso as fc 

class TestaMotor:
        
    def __init__(self, instancia_tk):
        
        #da um titulo para a instância criada
        instancia_tk.title("Aciona Motores")
        
        #__________Frames________________________
        # cria os frames da interface        
        # No fr1 ficará a mensagem principal
        self.fr1=tk.Frame(instancia_tk)
        self.fr1.pack()
        # No fr2 ficará o botão sair na parte inferior da janela
        self.fr2=tk.Frame(instancia_tk)
        self.fr2.pack(side="bottom")
        #No fr3 e fr4 ficarão as mensagens das entradas e as entradas 
        self.fr3=tk.Frame(instancia_tk)
        self.fr3.pack()
        self.fr4=tk.Frame(instancia_tk)
        self.fr4.pack()       
        # no fr5 e fr6 ficarão os botões que vão acionar cada motor
        self.fr5=tk.Frame(instancia_tk)
        self.fr5.pack()
        self.fr6=tk.Frame(instancia_tk)
        self.fr6.pack()
        
        
        
        #___________ Frame 1______________________________________
        #cria as mensagens que serão exibidas
        self.mensagem="Essa janela será usada para testar os motores"
        self.mensagem1=""        
        ##Mensagem 1 ( geral sobre a janela)
        self.mens1=tk.Message(self.fr1, text=self.mensagem,
                              width=400,font=('times', 16, 'italic'))
        self.mens1.pack()
        ##Mensagem 2( retorna uma mensagem de digitação errada)
        self.mens2=tk.Message(self.fr1, text=self.mensagem1,width=400)
        self.mens2.pack()
        
        # ____________Frame 2___________________________________
         ##O bt(sair)será o padrão todas janelas
        self.bt=tk.Button(self.fr2, text="sair",
                           width=10,height=2,bg="red",
                           command=instancia_tk.destroy)
        self.bt.pack()
        
        #__________Frame 3________________________________________
        # Mensagem e entrada de valores do tempo de cada paço
        self.espaço=tk.Message(self.fr3,
                               text="Só digite numeros Inteiros ",
                               font=('times', 16, 'bold'),fg="red",
                               pady=5,width=400)
        self.espaço.pack()
        self.mensagem2="Digite aqui o tempo em ms de cada passo (>10) "
        self.mens3=tk.Message(self.fr3,text=self.mensagem2,
                              width=400,font=('times', 12, 'bold'))
        self.mens3.pack(side="left")
        self.ed1=tk.Entry(self.fr3,bg="white",width=20,font=10)
        self.ed1.pack()
        
        #__________Frame 4_________________________________________
        # Mensagem e entrada de valores da quantidade de passos
        self.mensagem3="Digite aqui a quantidade de passos"
        self.mens4=tk.Message(self.fr4, text=self.mensagem3,
                              width=400,font=('times', 12, 'bold'))
        self.mens4.pack(side="left")
        self.ed2=tk.Entry(self.fr4,bg="white",width=29,font=10)
        self.ed2.pack()
        self.mens7=tk.Message(self.fr4,text=" ",width=400,
                              font=('times', 12, 'bold'),fg="red")
        #________Frame 5______________________________________
        #_______mensagem de botões de acionamento motor horizontal
        self.espaço=tk.Message(self.fr5,text=" ",pady=30)
        self.espaço.pack()
        self.mensagem4="Controle motor horizontal"
        self.mens5=tk.Message(self.fr5, text=self.mensagem4,
                              width=200, font=('times', 14, 'italic'))
        self.mens5.pack()
        self.bt1=tk.Button(self.fr5,text="horário",bg="#00D4FF",
                           width=20,
                           command=self.aciona_motor_horizontal_horario)
        self.bt1.pack()
        self.bt2=tk.Button(self.fr5,text="anti-horário",bg="yellow",
                           width=20, 
                           command=self.aciona_motor_horizontal_anti_horario)
        self.bt2.pack()
        
        #________Frame 6______________________________________
        #_______mensagem de botões de acionamento motor vertical
        self.mensagem5="Controle motor vertical"       
        self.mens6=tk.Message(self.fr5, text=self.mensagem5,
                              width=200,font=('times', 14, 'italic'))
        self.mens6.pack()
        self.bt3=tk.Button(self.fr5,text="horário",bg="#00D4FF",width=20,
                           command=self.aciona_motor_vertical_horario)
        self.bt3.pack()
        self.bt4=tk.Button(self.fr5,text="anti-horário",bg="yellow",width=20,
                           command=self.aciona_motor_vertical_anti_horario)
        self.bt4.pack()
        
        #________Funções_______________________________________
        ## A função valores verifica se os valores digitados estão corretos
    def valores(self):
        if(str(self.ed1.get()).isnumeric() and str(self.ed2.get()).isnumeric()):
            a=int(self.ed1.get())
            b=int(self.ed2.get())
            self.mens7["text"]=" "
            return a,b
        else:
            self.mens7["text"]="Digite um numero inteiro"
            pass
       
        ## A função aciona motor faz o movimento do motor
    def aciona_motor_horizontal_anti_horario(self): 
            a,b= self.valores()    
            if (a>=10) and (b!=0): 
                ##motor_horizontal= Motor(13,19,25,26)
                motor_horizontal= Motor(13,25,19,26)
                motor_horizontal.anti_horario(a,b) 
                self.mens7["text"]="Motor:Horizontal(anti-horário)" 
            else:
                self.mens7["text"]= "Tempo > 10 e Passos = inteiro"
                pass
    def aciona_motor_horizontal_horario(self):
        a,b=self.valores()
        if (a>=10) and (b!=0):
            motor_horizontal=Motor(13,25,19,26)
            motor_horizontal.horario(a,b)
            self.mens7["text"]="Motor:Horizontal(horário)"
        else:
            self.mens7["text"]= "Tempo > 10 e Passos = inteiro"
            pass
            
    def aciona_motor_vertical_anti_horario(self):
        a,b=self.valores()  
        if (a>=10) and (b!=0):
            objeto=fc() 
            estado_chave=objeto.estado()
            print(estado_chave)
            while estado_chave==1 and b>0:
                z=1
                motor_vertical=Motor(12,20,16,21)       
                motor_vertical.anti_horario(a,z)
                b-=1
                estado_chave=objeto.estado()
                print(b,estado_chave)
            self.mens7["text"]="Motor:Vertical(anti-horário)"
            print(estado_chave)
        else:
            self.mens7["text"]= "Tempo > 10 e Passos = inteiro"
           

    def aciona_motor_vertical_horario(self):
        a,b=self.valores()
        if (a>=10) and (b!=0):
            ##motor_vertical=Motor(12,20,16,21)
            motor_vertical=Motor(12,20,16,21)
            motor_vertical.horario(a,b)
            self.mens7["text"]="Motor:Vertical(anti-horário)"         
        else:
             self.mens7["text"]= "Tempo > 10 e Passos = inteiro"

##Função principal ( starta a aplicação)

def main():
    janela=tk.Tk()
    TestaMotor(janela)
    janela.geometry("700x600+100+100")
    janela.mainloop()        
        
        

if __name__ == "__main__":
    main()
        
          
