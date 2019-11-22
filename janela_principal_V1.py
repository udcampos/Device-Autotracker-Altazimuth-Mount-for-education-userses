#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Sun Jan 20 16:12:32 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
"""

import tkinter as tk
import aciona_motor_v2
import janela_calibracao_V3
import janela_acha_estrela_V1

class JanelaPai:

    ##def __init__(self):           

    def cria_janela_componentes(self):
        janela=tk.Tk()
        janela.title("Janela Principal")       
        bt1=tk.Button(janela, text="Testa Motor", width=30,bg="yellow",command=self.executa_botao1)
        bt1.place(x=80, y=100)
        bt2=tk.Button(janela, text="SAIR", bg="red",command=janela.destroy)
        bt2.pack(side="bottom")
        bt3=tk.Button(janela, text="Encontra o Norte", width=30,bg="yellow",command=self.executa_botao3)
        bt3.place(x=80, y=130)
        bt4=tk.Button(janela, text="Acha Estrela", width=30,bg="yellow",command=self.executa_botao4)
        bt4.place(x=80, y=160)
  
        
        janela.geometry("400x300+800+650")
        janela.mainloop()        
      
    def __del__(self):
        pass

    def executa_botao1(self):
        aciona_motor_v2.main()

    def executa_botao3(self):
        janela_calibracao_V3.main()

    def executa_botao4(self):
        janela_acha_estrela_V1.main()

def main():
    raiz=JanelaPai()
    raiz.cria_janela_componentes()

if __name__ == "__main__":
    main()
    
        
        
    
        
        
        

##tkinter.TclError: bad side "TOP": must be top, bottom, left, or right
"""def chama_janela():
    import teste
   
def fecha_janela():
    chama_janela()
    janela.destroy()
    
bt=tk.Button(janela, text="chama_janela", command=fecha_janela)
bt.pack()


janela.geometry("400x500+100+100")
janela.mainloop()"""
