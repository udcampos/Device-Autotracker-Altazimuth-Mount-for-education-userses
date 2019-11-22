"""Esse código ímplementa a função da chave fim de curso para acertar o
nível do telescópio....
   Desenvolvido por Ubiratan de Campos"""

import RPi.GPIO as gpio
from time import sleep


class fim_curso:

    def configuracao_gpio(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(27,gpio.IN,pull_up_down=gpio.PUD_UP) 

    def estado(self):
        self.configuracao_gpio()       
        estado_fim_curso=gpio.input(27)
        return estado_fim_curso
        
       
            
        

