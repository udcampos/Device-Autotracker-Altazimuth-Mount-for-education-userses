import math

def nivelamento(matriz):
        matriz=matriz
        somab=0
        somac=0
        for vetor in matriz:
            x,y,z=vetor
            ##------------------------- Alterações para compensar sensor--------
            ## O valor de 650 corrige o eixo x e 350 o eixo y
            x+=650
            y+=350
            ##---------------------------------------------------------------
            b = math.degrees(math.atan2(y, x))
            c = math.degrees(math.atan2(z,y))
            print(b)
            if b<0:
                b+=360.0
                somab+=b                
            else:
                somab+=b
            if c<0:
                c+=360.0
                somac+=c                
            else:
                somac+=c
            
        mediab=somab/(len(matriz))
        mediac=somac/(len(matriz))
        return mediab, mediac
