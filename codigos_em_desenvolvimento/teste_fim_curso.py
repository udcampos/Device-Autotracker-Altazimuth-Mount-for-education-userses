##Esse código tem como função verificar o fim de curso do nivelamento

import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setup(27,gpio.IN,pull_up_down=gpio.PUD_UP)

while True:
    input_state=gpio.input(27)
    if input_state==False:
        print("Botão Pressionado")
        sleep(1)

"""estado_fim_curso=gpio.input(27)
print (estado_fim_curso)"""
