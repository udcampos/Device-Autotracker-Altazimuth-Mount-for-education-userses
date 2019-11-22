from Motor_half_step import Motor
from acha_estrela_v6 import AchaEstrela as ae


def automatiza_motor_anti_horario():
    x=ae()
    #x.passos_minimos_acompanhamento=10
    a=0
    while a<1:
        x.aciona_motor_horizontal_anti_horario_acompanhamento()
        a+=1
    return True

def automatiza_motor_horario():
    x=ae()
    #x.passos_minimos_acompanhamento=10
    a=0
    while a<1:
        x.aciona_motor_horizontal_horario_acompanhamento()
        a+=1
    return True
