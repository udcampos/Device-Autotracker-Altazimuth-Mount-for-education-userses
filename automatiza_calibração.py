#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado em Tue Oct  1 18:25:57 2019

@Produzido no Debian e Spyder3

@author: Ubiratan de Campos
Ponto de calibração
horario e antihorario
"""
from Motor_half_step import Motor as mt
from Motor_drive_novo import Motor as mv
##from aciona_motor_v2 import TestaMotor as tm
from nivelamento_usando_coordenadas_motor_horizontal_novo_v1 import EncontraNorte as en


class PontoCalibração:
    def cria_objeto_motor_horizontal_horario(self):
        movimento_horizontal_horario=mv("horario", 25, 6000,100)
        movimento_horizontal_horario.automatiza_rotacao()
        return True
        
    def cria_objeto_motor_horizontal_anti_horario(self):
        movimento_horizontal_anti_horario=mv("anti", 25, 6000, 100)
        movimento_horizontal_anti_horario.automatiza_rotacao()
        return True
        
    def cria_objeto_motor_vertical_horario(self):
        movimento_vertical=mt(12,20,16,21)
        movimento_vertical.horario(100,6000)
        return True
        
    def calibracao(self):
        calibracao=en(21.45)
        calibracao.automatiza_correcao()
        return (print("Acabou"))
     
    def horario(self):
        valor_horizontal=self.cria_objeto_motor_horizontal_horario()
        if valor_horizontal==True:
            valor_vertical=self.cria_objeto_motor_vertical_horario()
            if valor_vertical==True:
                self.calibracao()
            else:
                print("Deu algo errado")
        else:
            print("Deu algo errado")
            
    def anti_horario(self):
        valor_horizontal=self.cria_objeto_motor_horizontal_anti_horario()
        if valor_horizontal==True:
            valor_vertical=self.cria_objeto_motor_vertical_horario()
            if valor_vertical==True:
                self.calibracao()
            else:
                print("Deu algo errado")
        else:
            print("Deu algo errado")       
         
def main():
    x= PontoCalibração()
    print("digite o sentido de sentido que que rodar")
    print("1 para horário e 2 para anti_horario")
    n= int(input("Entre com o valor: "))
    if n==1:
        x.horario()
        return True
    else:
        x.anti_horario()
        return True
        
        


if __name__ == "__main__":
    main()

    
     
