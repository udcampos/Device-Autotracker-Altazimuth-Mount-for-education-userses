from time import sleep
from automatiza_calibração import PontoCalibração as pc


def horario(quant,temp):
    a=0
    print(" A quantidade de medições será: " ,quant)
    
    while a<quant:
        print("A medição agora é a: ",a)
        roda=pc()
        print("rodando horario")
        roda.horario()
        sleep(temp)
        print("rodando anti_horario")
        roda.anti_horario()
        sleep(temp)
        a+=2
    return(print("O ciclo acabou"))


def anti_horario(quant,temp):
    a=0
    
    while a<quant:
        print("A medição agora é a: ",a)
        roda=pc()
        print("rodando anti_horario")
        roda.anti_horario()
        sleep(temp)
        print("rodando horario")
        roda.horario()
        sleep(temp)
        a+=2
    return(print("O ciclo acabou"))
