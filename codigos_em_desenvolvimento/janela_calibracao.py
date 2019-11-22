#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sun Jan 20 15:13:20 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

##from calibracao_telescopio import SensorMagnetico
import tkinter as tk
from nivelamento_usando_coordenadas import EncontraNorte as enorte
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
        self.fr4= tk.Frame(instancia_tk,bg='white')
        self.fr4.pack()
        #___________Mensagens____________________
        #cria as mensagens que serão exibidas
        self.mensagem="A calibração é uma etapa fundamental para observação"
        self.mensagem1=""
        self.mensagem2="É necessário inserir o valor da declinação Magnética da sua região"
        self.mensagem3="Use esse site: https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml#declination"
        self.mensagem4="Insira o valor da declinação"
        self.mens1=tk.Message(self.fr1, text=self.mensagem,width=600,bg='lightyellow', font=('times', 18, 'bold'))
        self.mens1.pack()
        self.mens2=tk.Message(self.fr1, text=self.mensagem1,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens2.pack()
        self.mens3= tk.Message(self.fr1, text=self.mensagem2,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens3.pack()
        self.mens4= tk.Message(self.fr1, text=self.mensagem3,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens4.pack()
        self.mens5= tk.Message(self.fr1, text=self.mensagem1,width=600,bg='white',font=('times', 12, 'italic'))
        self.mens5.pack()
        self.mens7= tk.Message(self.fr4, text=" ",width=600,bg='white',font=('times', 12, 'italic'))
        self.mens7.pack()
        
        #____________Botões______________________
        #cria os botões da interface
        # O bt1(sair)será o padrão todas janelas
        self.bt1=tk.Button(self.fr2, text="SAIR",font=('blue'),
                           width=10,height=2,bg="red",
                           command=instancia_tk.destroy)
        self.bt1.pack()
        
        
        self.bt2=tk.Button(self.fr3, text="Acha o Norte Geografico",
                           width=20,height=2,bg="lightgreen",
                           command=self.encontra_norte)
        self.mens6= tk.Message(self.fr3, text=self.mensagem4,width=600,bg='white',font=('times', 14, 'bold'))
        self.mens6.pack(padx=2, pady=5, side="left")
        self.ed1=tk.Entry(self.fr3, text=" ",bg="white",width=5)
        self.ed1.pack(side="left")
        self.bt2.pack()
        
        
                
        
        #___________Funções______________________
    
    def entrada_declinacao(self):
        if(str(self.ed1.get()).isnumeric()):
            self.mens7["text"]=" "
            self.mens7["bg"]="white"
            return True
        else:
            self.mens7["text"]="Digite um numero inteiro"
            self.mens7["bg"]="red"

    def encontra_norte(self):
        
            if self.entrada_declinacao()==True:
                declinacao= int(self.ed1.get())
                ##self.mens7["text"]=" "
                norte=enorte(declinacao)
                norte.automatiza_correcao()
                return True
            
##Função principal (starta a aplicação)            
    
def main():
    janela=tk.Tk()
    Calibracao(janela)
    janela.geometry("600x400+100+100")
    janela['bg']= 'white'
    janela.mainloop()

if __name__== "__main__":
    main()

## Opções de tamanho de botão width=100,height=40
##command=self.encontra_norte

